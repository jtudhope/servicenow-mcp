"""
Taxonomy tools for the ServiceNow MCP server.

This module provides tools for managing Taxonomies that are stored in the taxonomy table.
In ServiceNow, the taxonomy table (taxonomy) is a system table used to store hierarchical 
classification structures — essentially "controlled vocabularies" that other parts of the 
platform can reference.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateTaxonomyParams(BaseModel):
    """Parameters for creating a taxonomy."""

    name: str = Field(..., description="Name of the taxonomy (required, unique)")
    description: Optional[str] = Field(None, description="Description of the taxonomy")
    active: Optional[bool] = Field(True, description="Whether the taxonomy is active")
    managers: Optional[str] = Field(None, description="User criteria sys_id for taxonomy managers")
    sys_domain: Optional[str] = Field("global", description="Domain for the taxonomy")
    sys_domain_path: Optional[str] = Field("/", description="Domain path for the taxonomy")


class UpdateTaxonomyParams(BaseModel):
    """Parameters for updating a taxonomy."""

    taxonomy_id: str = Field(..., description="Taxonomy sys_id")
    name: Optional[str] = Field(None, description="Updated name of the taxonomy")
    description: Optional[str] = Field(None, description="Updated description")
    active: Optional[bool] = Field(None, description="Updated active status")
    managers: Optional[str] = Field(None, description="Updated user criteria sys_id for managers")
    sys_domain: Optional[str] = Field(None, description="Updated domain")
    sys_domain_path: Optional[str] = Field(None, description="Updated domain path")


class ListTaxonomiesParams(BaseModel):
    """Parameters for listing taxonomies."""

    limit: int = Field(10, description="Maximum number of taxonomies to return")
    offset: int = Field(0, description="Offset for pagination")
    active: Optional[bool] = Field(None, description="Filter by active status")
    name_contains: Optional[str] = Field(None, description="Filter by name containing text")
    sys_domain: Optional[str] = Field(None, description="Filter by domain")
    query: Optional[str] = Field(None, description="Additional query string")


class GetTaxonomyParams(BaseModel):
    """Parameters for getting a taxonomy."""

    taxonomy_id: str = Field(..., description="Taxonomy sys_id or name")


class DeleteTaxonomyParams(BaseModel):
    """Parameters for deleting a taxonomy."""

    taxonomy_id: str = Field(..., description="Taxonomy sys_id")


class CloneTaxonomyParams(BaseModel):
    """Parameters for cloning a taxonomy."""

    taxonomy_id: str = Field(..., description="Source taxonomy sys_id")
    new_name: str = Field(..., description="Name for the cloned taxonomy")
    new_description: Optional[str] = Field(None, description="Description for the cloned taxonomy")


class TaxonomyResponse(BaseModel):
    """Response from taxonomy operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_taxonomy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateTaxonomyParams,
) -> TaxonomyResponse:
    """
    Create a new taxonomy in the taxonomy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the taxonomy

    Returns:
        Response containing the result of the taxonomy creation
    """
    logger.info(f"Creating taxonomy: {params.name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/taxonomy"
    
    # Prepare request body
    body = {
        "name": params.name,
        "active": params.active,
        "sys_domain": params.sys_domain,
        "sys_domain_path": params.sys_domain_path,
    }
    
    if params.description:
        body["description"] = params.description
    
    if params.managers:
        body["managers"] = params.managers
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        taxonomy = result.get("result", {})
        
        # Format the response
        formatted_taxonomy = {
            "sys_id": taxonomy.get("sys_id", ""),
            "name": taxonomy.get("name", ""),
            "description": taxonomy.get("description", ""),
            "active": taxonomy.get("active", ""),
            "managers": taxonomy.get("managers", ""),
            "sys_domain": taxonomy.get("sys_domain", ""),
            "sys_domain_path": taxonomy.get("sys_domain_path", ""),
            "sys_created_on": taxonomy.get("sys_created_on", ""),
            "sys_updated_on": taxonomy.get("sys_updated_on", ""),
        }
        
        return TaxonomyResponse(
            success=True,
            message=f"Created taxonomy: {params.name}",
            data=formatted_taxonomy,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating taxonomy: {str(e)}")
        return TaxonomyResponse(
            success=False,
            message=f"Error creating taxonomy: {str(e)}",
            data=None,
        )


def update_taxonomy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateTaxonomyParams,
) -> TaxonomyResponse:
    """
    Update an existing taxonomy in the taxonomy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the taxonomy

    Returns:
        Response containing the result of the taxonomy update
    """
    logger.info(f"Updating taxonomy: {params.taxonomy_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/taxonomy/{params.taxonomy_id}"
    
    # Prepare request body with only provided fields
    body = {}
    
    if params.name is not None:
        body["name"] = params.name
    if params.description is not None:
        body["description"] = params.description
    if params.active is not None:
        body["active"] = params.active
    if params.managers is not None:
        body["managers"] = params.managers
    if params.sys_domain is not None:
        body["sys_domain"] = params.sys_domain
    if params.sys_domain_path is not None:
        body["sys_domain_path"] = params.sys_domain_path
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        taxonomy = result.get("result", {})
        
        # Format the response
        formatted_taxonomy = {
            "sys_id": taxonomy.get("sys_id", ""),
            "name": taxonomy.get("name", ""),
            "description": taxonomy.get("description", ""),
            "active": taxonomy.get("active", ""),
            "managers": taxonomy.get("managers", ""),
            "sys_domain": taxonomy.get("sys_domain", ""),
            "sys_domain_path": taxonomy.get("sys_domain_path", ""),
            "sys_created_on": taxonomy.get("sys_created_on", ""),
            "sys_updated_on": taxonomy.get("sys_updated_on", ""),
        }
        
        return TaxonomyResponse(
            success=True,
            message=f"Updated taxonomy: {params.taxonomy_id}",
            data=formatted_taxonomy,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating taxonomy: {str(e)}")
        return TaxonomyResponse(
            success=False,
            message=f"Error updating taxonomy: {str(e)}",
            data=None,
        )


def list_taxonomies(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListTaxonomiesParams,
) -> Dict[str, Any]:
    """
    List taxonomies from the taxonomy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing taxonomies

    Returns:
        Dictionary containing taxonomies and metadata
    """
    logger.info("Listing taxonomies")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/taxonomy"
    
    # Prepare query parameters
    query_parts = []
    
    if params.active is not None:
        query_parts.append(f"active={params.active}")
    
    if params.name_contains:
        query_parts.append(f"nameLIKE{params.name_contains}")
    
    if params.sys_domain:
        query_parts.append(f"sys_domain={params.sys_domain}")
    
    if params.query:
        query_parts.append(params.query)
    
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,description,active,managers,sys_domain,sys_domain_path,sys_created_on,sys_updated_on",
    }
    
    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        taxonomies = result.get("result", [])
        
        # Format the response
        formatted_taxonomies = []
        for taxonomy in taxonomies:
            formatted_taxonomies.append({
                "sys_id": taxonomy.get("sys_id", ""),
                "name": taxonomy.get("name", ""),
                "description": taxonomy.get("description", ""),
                "active": taxonomy.get("active", ""),
                "managers": taxonomy.get("managers", ""),
                "sys_domain": taxonomy.get("sys_domain", ""),
                "sys_domain_path": taxonomy.get("sys_domain_path", ""),
                "sys_created_on": taxonomy.get("sys_created_on", ""),
                "sys_updated_on": taxonomy.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_taxonomies)} taxonomies",
            "taxonomies": formatted_taxonomies,
            "total": len(formatted_taxonomies),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing taxonomies: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing taxonomies: {str(e)}",
            "taxonomies": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_taxonomy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetTaxonomyParams,
) -> TaxonomyResponse:
    """
    Get a specific taxonomy from the taxonomy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the taxonomy

    Returns:
        Response containing the taxonomy data
    """
    logger.info(f"Getting taxonomy: {params.taxonomy_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/taxonomy/{params.taxonomy_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,description,active,managers,sys_domain,sys_domain_path,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        taxonomy = result.get("result", {})
        
        # Format the response
        formatted_taxonomy = {
            "sys_id": taxonomy.get("sys_id", ""),
            "name": taxonomy.get("name", ""),
            "description": taxonomy.get("description", ""),
            "active": taxonomy.get("active", ""),
            "managers": taxonomy.get("managers", ""),
            "sys_domain": taxonomy.get("sys_domain", ""),
            "sys_domain_path": taxonomy.get("sys_domain_path", ""),
            "sys_created_on": taxonomy.get("sys_created_on", ""),
            "sys_updated_on": taxonomy.get("sys_updated_on", ""),
        }
        
        return TaxonomyResponse(
            success=True,
            message=f"Retrieved taxonomy: {params.taxonomy_id}",
            data=formatted_taxonomy,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting taxonomy: {str(e)}")
        return TaxonomyResponse(
            success=False,
            message=f"Error getting taxonomy: {str(e)}",
            data=None,
        )


def delete_taxonomy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteTaxonomyParams,
) -> TaxonomyResponse:
    """
    Delete a taxonomy from the taxonomy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the taxonomy

    Returns:
        Response containing the result of the taxonomy deletion
    """
    logger.info(f"Deleting taxonomy: {params.taxonomy_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/taxonomy/{params.taxonomy_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return TaxonomyResponse(
            success=True,
            message=f"Deleted taxonomy: {params.taxonomy_id}",
            data={"deleted_taxonomy_id": params.taxonomy_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting taxonomy: {str(e)}")
        return TaxonomyResponse(
            success=False,
            message=f"Error deleting taxonomy: {str(e)}",
            data=None,
        )


def clone_taxonomy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CloneTaxonomyParams,
) -> TaxonomyResponse:
    """
    Clone an existing taxonomy in the taxonomy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for cloning the taxonomy

    Returns:
        Response containing the result of the taxonomy cloning
    """
    logger.info(f"Cloning taxonomy: {params.taxonomy_id}")
    
    try:
        # First, get the source taxonomy
        get_params = GetTaxonomyParams(taxonomy_id=params.taxonomy_id)
        source_result = get_taxonomy(config, auth_manager, get_params)
        
        if not source_result.success:
            return TaxonomyResponse(
                success=False,
                message=f"Failed to retrieve source taxonomy: {source_result.message}",
                data=None,
            )
        
        source_taxonomy = source_result.data
        
        # Create the clone with new name
        create_params = CreateTaxonomyParams(
            name=params.new_name,
            description=params.new_description or source_taxonomy.get("description"),
            active=source_taxonomy.get("active", True),
            managers=source_taxonomy.get("managers"),
            sys_domain=source_taxonomy.get("sys_domain", "global"),
            sys_domain_path=source_taxonomy.get("sys_domain_path", "/"),
        )
        
        return create_taxonomy(config, auth_manager, create_params)
    
    except Exception as e:
        logger.error(f"Error cloning taxonomy: {str(e)}")
        return TaxonomyResponse(
            success=False,
            message=f"Error cloning taxonomy: {str(e)}",
            data=None,
        )