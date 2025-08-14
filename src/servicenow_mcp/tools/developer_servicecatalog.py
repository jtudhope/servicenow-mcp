"""
Service Catalog Management tools for the ServiceNow MCP server.

This module provides tools for managing service catalogs in the sc_catalog table.
It handles creation, updating, listing, retrieval, and deletion of service catalogs.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateServiceCatalogParams(BaseModel):
    """Parameters for creating a service catalog."""

    title: str = Field(..., description="Title of the service catalog")
    description: Optional[str] = Field(None, description="Description of the service catalog")
    active: bool = Field(True, description="Whether the catalog is active")
    desktop: bool = Field(True, description="Whether the catalog is available on desktop")
    mobile: bool = Field(True, description="Whether the catalog is available on mobile")
    enable_wish_list: bool = Field(False, description="Whether to enable wish list functionality")
    enable_request_cart: bool = Field(True, description="Whether to enable request cart functionality")
    manager: Optional[str] = Field(None, description="Manager sys_id for the catalog")
    editors: Optional[str] = Field(None, description="Editors sys_id (comma-separated)")


class UpdateServiceCatalogParams(BaseModel):
    """Parameters for updating a service catalog."""

    catalog_id: str = Field(..., description="Service catalog sys_id")
    title: Optional[str] = Field(None, description="Title of the service catalog")
    description: Optional[str] = Field(None, description="Description of the service catalog")
    active: Optional[bool] = Field(None, description="Whether the catalog is active")
    desktop: Optional[bool] = Field(None, description="Whether the catalog is available on desktop")
    mobile: Optional[bool] = Field(None, description="Whether the catalog is available on mobile")
    enable_wish_list: Optional[bool] = Field(None, description="Whether to enable wish list functionality")
    enable_request_cart: Optional[bool] = Field(None, description="Whether to enable request cart functionality")
    manager: Optional[str] = Field(None, description="Manager sys_id for the catalog")
    editors: Optional[str] = Field(None, description="Editors sys_id (comma-separated)")


class ListServiceCatalogsParams(BaseModel):
    """Parameters for listing service catalogs."""

    limit: int = Field(10, description="Maximum number of catalogs to return")
    offset: int = Field(0, description="Offset for pagination")
    active: Optional[bool] = Field(None, description="Filter by active status")
    desktop: Optional[bool] = Field(None, description="Filter by desktop availability")
    mobile: Optional[bool] = Field(None, description="Filter by mobile availability")
    manager: Optional[str] = Field(None, description="Filter by manager sys_id")
    query: Optional[str] = Field(None, description="Search query for catalog title or description")


class GetServiceCatalogParams(BaseModel):
    """Parameters for getting a specific service catalog."""

    catalog_id: str = Field(..., description="Service catalog sys_id")


class DeleteServiceCatalogParams(BaseModel):
    """Parameters for deleting a service catalog."""

    catalog_id: str = Field(..., description="Service catalog sys_id")


class ServiceCatalogResponse(BaseModel):
    """Response from service catalog operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_service_catalog(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateServiceCatalogParams,
) -> ServiceCatalogResponse:
    """
    Create a new service catalog in the sc_catalog table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the service catalog

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating service catalog: {params.title}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_catalog"
    
    # Prepare request body
    body = {
        "title": params.title,
        "active": str(params.active).lower(),
        "desktop": str(params.desktop).lower(),
        "mobile": str(params.mobile).lower(),
        "enable_wish_list": str(params.enable_wish_list).lower(),
        "enable_request_cart": str(params.enable_request_cart).lower(),
    }
    
    if params.description is not None:
        body["description"] = params.description
    if params.manager is not None:
        body["manager"] = params.manager
    if params.editors is not None:
        body["editors"] = params.editors
    
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
            "desktop": catalog.get("desktop", ""),
            "mobile": catalog.get("mobile", ""),
            "enable_wish_list": catalog.get("enable_wish_list", ""),
            "enable_request_cart": catalog.get("enable_request_cart", ""),
            "manager": catalog.get("manager", ""),
            "editors": catalog.get("editors", ""),
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
    Update an existing service catalog in the sc_catalog table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the service catalog

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
    if params.desktop is not None:
        body["desktop"] = str(params.desktop).lower()
    if params.mobile is not None:
        body["mobile"] = str(params.mobile).lower()
    if params.enable_wish_list is not None:
        body["enable_wish_list"] = str(params.enable_wish_list).lower()
    if params.enable_request_cart is not None:
        body["enable_request_cart"] = str(params.enable_request_cart).lower()
    if params.manager is not None:
        body["manager"] = params.manager
    if params.editors is not None:
        body["editors"] = params.editors
    
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
            "desktop": catalog.get("desktop", ""),
            "mobile": catalog.get("mobile", ""),
            "enable_wish_list": catalog.get("enable_wish_list", ""),
            "enable_request_cart": catalog.get("enable_request_cart", ""),
            "manager": catalog.get("manager", ""),
            "editors": catalog.get("editors", ""),
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


def list_service_catalogs(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListServiceCatalogsParams,
) -> Dict[str, Any]:
    """
    List service catalogs from the sc_catalog table.

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
        "sysparm_fields": "sys_id,title,description,active,desktop,mobile,enable_wish_list,enable_request_cart,manager,editors,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    if params.desktop is not None:
        filters.append(f"desktop={str(params.desktop).lower()}")
    if params.mobile is not None:
        filters.append(f"mobile={str(params.mobile).lower()}")
    if params.manager:
        filters.append(f"manager={params.manager}")
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
                "desktop": catalog.get("desktop", ""),
                "mobile": catalog.get("mobile", ""),
                "enable_wish_list": catalog.get("enable_wish_list", ""),
                "enable_request_cart": catalog.get("enable_request_cart", ""),
                "manager": catalog.get("manager", ""),
                "editors": catalog.get("editors", ""),
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
    Get a specific service catalog from the sc_catalog table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the service catalog

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
        "sysparm_fields": "sys_id,title,description,active,desktop,mobile,enable_wish_list,enable_request_cart,manager,editors,sys_created_on,sys_updated_on",
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
            "desktop": catalog.get("desktop", ""),
            "mobile": catalog.get("mobile", ""),
            "enable_wish_list": catalog.get("enable_wish_list", ""),
            "enable_request_cart": catalog.get("enable_request_cart", ""),
            "manager": catalog.get("manager", ""),
            "editors": catalog.get("editors", ""),
            "sys_created_on": catalog.get("sys_created_on", ""),
            "sys_updated_on": catalog.get("sys_updated_on", ""),
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


def delete_service_catalog(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteServiceCatalogParams,
) -> ServiceCatalogResponse:
    """
    Delete a service catalog from the sc_catalog table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the service catalog

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