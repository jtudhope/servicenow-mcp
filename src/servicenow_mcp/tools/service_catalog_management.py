"""
Service Catalog Management tools for the ServiceNow MCP server.

This module provides tools for managing service catalogs (sc_catalog table) in ServiceNow.
"""

import logging
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class ListServiceCatalogsParams(BaseModel):
    """Parameters for listing service catalogs."""
    
    limit: int = Field(10, description="Maximum number of catalogs to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Search query for catalog title or description")
    active: bool = Field(True, description="Whether to only return active catalogs")


class GetServiceCatalogParams(BaseModel):
    """Parameters for getting a specific service catalog."""
    
    catalog_id: str = Field(..., description="Catalog ID or sys_id")


class CreateServiceCatalogParams(BaseModel):
    """Parameters for creating a new service catalog."""
    
    title: str = Field(..., description="Title of the catalog")
    description: Optional[str] = Field(None, description="Description of the catalog")
    active: bool = Field(True, description="Whether the catalog is active")
    background_color: Optional[str] = Field(None, description="Background color for the catalog")
    desktop: bool = Field(True, description="Whether the catalog is available on desktop")
    mobile: bool = Field(True, description="Whether the catalog is available on mobile")


class UpdateServiceCatalogParams(BaseModel):
    """Parameters for updating a service catalog."""
    
    catalog_id: str = Field(..., description="Catalog ID or sys_id")
    title: Optional[str] = Field(None, description="Title of the catalog")
    description: Optional[str] = Field(None, description="Description of the catalog")
    active: Optional[bool] = Field(None, description="Whether the catalog is active")
    background_color: Optional[str] = Field(None, description="Background color for the catalog")
    desktop: Optional[bool] = Field(None, description="Whether the catalog is available on desktop")
    mobile: Optional[bool] = Field(None, description="Whether the catalog is available on mobile")


class DeleteServiceCatalogParams(BaseModel):
    """Parameters for deleting a service catalog."""
    
    catalog_id: str = Field(..., description="Catalog ID or sys_id")


class ServiceCatalogResponse(BaseModel):
    """Response from service catalog operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def list_service_catalogs(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListServiceCatalogsParams,
) -> Dict[str, Any]:
    """
    List service catalogs from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing service catalogs

    Returns:
        Dictionary containing service catalogs and metadata
    """
    logger.info("Listing service catalogs")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_catalog"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Add filters
    filters = []
    if params.active:
        filters.append("active=true")
    if params.query:
        filters.append(f"titleLIKE{params.query}^ORdescriptionLIKE{params.query}")
    
    if filters:
        query_params["sysparm_query"] = "^".join(filters)
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        catalogs = result.get("result", [])
        
        # Format the response
        formatted_catalogs = []
        for catalog in catalogs:
            formatted_catalogs.append({
                "sys_id": catalog.get("sys_id", ""),
                "title": catalog.get("title", ""),
                "description": catalog.get("description", ""),
                "active": catalog.get("active", ""),
                "background_color": catalog.get("background_color", ""),
                "desktop": catalog.get("desktop", ""),
                "mobile": catalog.get("mobile", ""),
                "sys_created_on": catalog.get("sys_created_on", ""),
                "sys_updated_on": catalog.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_catalogs)} service catalogs",
            "catalogs": formatted_catalogs,
            "total": len(formatted_catalogs),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing service catalogs: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing service catalogs: {str(e)}",
            "catalogs": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_service_catalog(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetServiceCatalogParams,
) -> ServiceCatalogResponse:
    """
    Get a specific service catalog from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting a service catalog

    Returns:
        Response containing the service catalog details
    """
    logger.info(f"Getting service catalog: {params.catalog_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_catalog/{params.catalog_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        catalog = result.get("result", {})
        
        if not catalog:
            return ServiceCatalogResponse(
                success=False,
                message=f"Service catalog not found: {params.catalog_id}",
                data=None,
            )
        
        # Format the response
        formatted_catalog = {
            "sys_id": catalog.get("sys_id", ""),
            "title": catalog.get("title", ""),
            "description": catalog.get("description", ""),
            "active": catalog.get("active", ""),
            "background_color": catalog.get("background_color", ""),
            "desktop": catalog.get("desktop", ""),
            "mobile": catalog.get("mobile", ""),
            "sys_created_on": catalog.get("sys_created_on", ""),
            "sys_updated_on": catalog.get("sys_updated_on", ""),
            "sys_created_by": catalog.get("sys_created_by", ""),
            "sys_updated_by": catalog.get("sys_updated_by", ""),
        }
        
        return ServiceCatalogResponse(
            success=True,
            message=f"Retrieved service catalog: {catalog.get('title', '')}",
            data=formatted_catalog,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting service catalog: {str(e)}")
        return ServiceCatalogResponse(
            success=False,
            message=f"Error getting service catalog: {str(e)}",
            data=None,
        )


def create_service_catalog(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateServiceCatalogParams,
) -> ServiceCatalogResponse:
    """
    Create a new service catalog in ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating a service catalog

    Returns:
        Response containing the result of the operation
    """
    logger.info("Creating new service catalog")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_catalog"
    
    # Prepare request body
    body = {
        "title": params.title,
        "active": str(params.active).lower(),
        "desktop": str(params.desktop).lower(),
        "mobile": str(params.mobile).lower(),
    }
    
    if params.description is not None:
        body["description"] = params.description
    if params.background_color is not None:
        body["background_color"] = params.background_color
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        catalog = result.get("result", {})
        
        # Format the response
        formatted_catalog = {
            "sys_id": catalog.get("sys_id", ""),
            "title": catalog.get("title", ""),
            "description": catalog.get("description", ""),
            "active": catalog.get("active", ""),
            "background_color": catalog.get("background_color", ""),
            "desktop": catalog.get("desktop", ""),
            "mobile": catalog.get("mobile", ""),
            "sys_created_on": catalog.get("sys_created_on", ""),
        }
        
        return ServiceCatalogResponse(
            success=True,
            message=f"Created service catalog: {params.title}",
            data=formatted_catalog,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating service catalog: {str(e)}")
        return ServiceCatalogResponse(
            success=False,
            message=f"Error creating service catalog: {str(e)}",
            data=None,
        )


def update_service_catalog(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateServiceCatalogParams,
) -> ServiceCatalogResponse:
    """
    Update an existing service catalog in ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating a service catalog

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating service catalog: {params.catalog_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_catalog/{params.catalog_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.title is not None:
        body["title"] = params.title
    if params.description is not None:
        body["description"] = params.description
    if params.active is not None:
        body["active"] = str(params.active).lower()
    if params.background_color is not None:
        body["background_color"] = params.background_color
    if params.desktop is not None:
        body["desktop"] = str(params.desktop).lower()
    if params.mobile is not None:
        body["mobile"] = str(params.mobile).lower()
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        catalog = result.get("result", {})
        
        # Format the response
        formatted_catalog = {
            "sys_id": catalog.get("sys_id", ""),
            "title": catalog.get("title", ""),
            "description": catalog.get("description", ""),
            "active": catalog.get("active", ""),
            "background_color": catalog.get("background_color", ""),
            "desktop": catalog.get("desktop", ""),
            "mobile": catalog.get("mobile", ""),
            "sys_updated_on": catalog.get("sys_updated_on", ""),
        }
        
        return ServiceCatalogResponse(
            success=True,
            message=f"Updated service catalog: {params.catalog_id}",
            data=formatted_catalog,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating service catalog: {str(e)}")
        return ServiceCatalogResponse(
            success=False,
            message=f"Error updating service catalog: {str(e)}",
            data=None,
        )


def delete_service_catalog(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteServiceCatalogParams,
) -> ServiceCatalogResponse:
    """
    Delete a service catalog from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting a service catalog

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting service catalog: {params.catalog_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_catalog/{params.catalog_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return ServiceCatalogResponse(
            success=True,
            message=f"Deleted service catalog: {params.catalog_id}",
            data={"deleted_catalog_id": params.catalog_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting service catalog: {str(e)}")
        return ServiceCatalogResponse(
            success=False,
            message=f"Error deleting service catalog: {str(e)}",
            data=None,
        )