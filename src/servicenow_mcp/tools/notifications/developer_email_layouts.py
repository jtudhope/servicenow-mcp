"""
Email Layouts tools for the ServiceNow MCP server.

This module provides tools for managing email layouts that are stored in the sys_email_layout table.
Email layouts are used to define branding for all email templates and email notifications used in the system,
essentially a wrapper.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateEmailLayoutParams(BaseModel):
    """Parameters for creating an email layout."""

    name: str = Field(..., description="Name of the email layout")
    description: Optional[str] = Field(None, description="Description of the email layout")
    layout: str = Field(..., description="HTML layout content for the email")
    advanced: Optional[bool] = Field(False, description="Whether this is an advanced layout")
    advanced_layout: Optional[str] = Field(None, description="Advanced XML layout content")


class UpdateEmailLayoutParams(BaseModel):
    """Parameters for updating an email layout."""

    layout_id: str = Field(..., description="Email layout sys_id")
    name: Optional[str] = Field(None, description="Updated name of the email layout")
    description: Optional[str] = Field(None, description="Updated description of the email layout")
    layout: Optional[str] = Field(None, description="Updated HTML layout content")
    advanced: Optional[bool] = Field(None, description="Updated advanced layout flag")
    advanced_layout: Optional[str] = Field(None, description="Updated advanced XML layout content")


class ListEmailLayoutsParams(BaseModel):
    """Parameters for listing email layouts."""

    limit: int = Field(10, description="Maximum number of layouts to return")
    offset: int = Field(0, description="Offset for pagination")
    advanced: Optional[bool] = Field(None, description="Filter by advanced layout status")
    query: Optional[str] = Field(None, description="Search query for layout name or description")


class GetEmailLayoutParams(BaseModel):
    """Parameters for getting a specific email layout."""

    layout_id: str = Field(..., description="Email layout sys_id")


class DeleteEmailLayoutParams(BaseModel):
    """Parameters for deleting an email layout."""

    layout_id: str = Field(..., description="Email layout sys_id")


class EmailLayoutResponse(BaseModel):
    """Response from email layout operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_email_layout(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateEmailLayoutParams,
) -> EmailLayoutResponse:
    """
    Create a new email layout in the sys_email_layout table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the email layout

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating email layout: {params.name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_email_layout"
    
    # Prepare request body
    body = {
        "name": params.name,
        "layout": params.layout,
        "advanced": str(params.advanced).lower() if params.advanced is not None else "false",
    }
    
    if params.description is not None:
        body["description"] = params.description
    if params.advanced_layout is not None:
        body["advanced_layout"] = params.advanced_layout
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        layout = result.get("result", {})
        
        # Format the response
        formatted_layout = {
            "sys_id": layout.get("sys_id", ""),
            "name": layout.get("name", ""),
            "description": layout.get("description", ""),
            "layout": layout.get("layout", ""),
            "advanced": layout.get("advanced", ""),
            "advanced_layout": layout.get("advanced_layout", ""),
            "sys_created_on": layout.get("sys_created_on", ""),
        }
        
        return EmailLayoutResponse(
            success=True,
            message=f"Created email layout: {params.name}",
            data=formatted_layout,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating email layout: {str(e)}")
        return EmailLayoutResponse(
            success=False,
            message=f"Error creating email layout: {str(e)}",
            data=None,
        )


def update_email_layout(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateEmailLayoutParams,
) -> EmailLayoutResponse:
    """
    Update an existing email layout in the sys_email_layout table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the email layout

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating email layout: {params.layout_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_email_layout/{params.layout_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.name is not None:
        body["name"] = params.name
    if params.description is not None:
        body["description"] = params.description
    if params.layout is not None:
        body["layout"] = params.layout
    if params.advanced is not None:
        body["advanced"] = str(params.advanced).lower()
    if params.advanced_layout is not None:
        body["advanced_layout"] = params.advanced_layout
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        layout = result.get("result", {})
        
        # Format the response
        formatted_layout = {
            "sys_id": layout.get("sys_id", ""),
            "name": layout.get("name", ""),
            "description": layout.get("description", ""),
            "layout": layout.get("layout", ""),
            "advanced": layout.get("advanced", ""),
            "advanced_layout": layout.get("advanced_layout", ""),
            "sys_updated_on": layout.get("sys_updated_on", ""),
        }
        
        return EmailLayoutResponse(
            success=True,
            message=f"Updated email layout: {params.layout_id}",
            data=formatted_layout,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating email layout: {str(e)}")
        return EmailLayoutResponse(
            success=False,
            message=f"Error updating email layout: {str(e)}",
            data=None,
        )


def list_email_layouts(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListEmailLayoutsParams,
) -> Dict[str, Any]:
    """
    List email layouts from the sys_email_layout table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing email layouts

    Returns:
        Dictionary containing email layouts and metadata
    """
    logger.info("Listing email layouts")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_email_layout"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,description,layout,advanced,advanced_layout,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.advanced is not None:
        filters.append(f"advanced={str(params.advanced).lower()}")
    if params.query:
        filters.append(f"nameLIKE{params.query}^ORdescriptionLIKE{params.query}")
    
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
        layouts = result.get("result", [])
        
        # Format the response
        formatted_layouts = []
        for layout in layouts:
            formatted_layouts.append({
                "sys_id": layout.get("sys_id", ""),
                "name": layout.get("name", ""),
                "description": layout.get("description", ""),
                "layout": layout.get("layout", ""),
                "advanced": layout.get("advanced", ""),
                "advanced_layout": layout.get("advanced_layout", ""),
                "sys_created_on": layout.get("sys_created_on", ""),
                "sys_updated_on": layout.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_layouts)} email layouts",
            "layouts": formatted_layouts,
            "total": len(formatted_layouts),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing email layouts: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing email layouts: {str(e)}",
            "layouts": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_email_layout(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetEmailLayoutParams,
) -> EmailLayoutResponse:
    """
    Get a specific email layout from the sys_email_layout table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the email layout

    Returns:
        Response containing the email layout details
    """
    logger.info(f"Getting email layout: {params.layout_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_email_layout/{params.layout_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,description,layout,advanced,advanced_layout,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        layout = result.get("result", {})
        
        if not layout:
            return EmailLayoutResponse(
                success=False,
                message=f"Email layout not found: {params.layout_id}",
                data=None,
            )
        
        # Format the response
        formatted_layout = {
            "sys_id": layout.get("sys_id", ""),
            "name": layout.get("name", ""),
            "description": layout.get("description", ""),
            "layout": layout.get("layout", ""),
            "advanced": layout.get("advanced", ""),
            "advanced_layout": layout.get("advanced_layout", ""),
            "sys_created_on": layout.get("sys_created_on", ""),
            "sys_updated_on": layout.get("sys_updated_on", ""),
        }
        
        return EmailLayoutResponse(
            success=True,
            message=f"Retrieved email layout: {layout.get('name', '')}",
            data=formatted_layout,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting email layout: {str(e)}")
        return EmailLayoutResponse(
            success=False,
            message=f"Error getting email layout: {str(e)}",
            data=None,
        )


def delete_email_layout(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteEmailLayoutParams,
) -> EmailLayoutResponse:
    """
    Delete an email layout from the sys_email_layout table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the email layout

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting email layout: {params.layout_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_email_layout/{params.layout_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return EmailLayoutResponse(
            success=True,
            message=f"Deleted email layout: {params.layout_id}",
            data={"deleted_layout_id": params.layout_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting email layout: {str(e)}")
        return EmailLayoutResponse(
            success=False,
            message=f"Error deleting email layout: {str(e)}",
            data=None,
        )


def clone_email_layout(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: Dict[str, Any],
) -> EmailLayoutResponse:
    """
    Clone an existing email layout in the sys_email_layout table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters containing layout_id and new_name

    Returns:
        Response containing the result of the operation
    """
    source_layout_id = params.get("layout_id")
    new_name = params.get("new_name")
    
    if not source_layout_id or not new_name:
        return EmailLayoutResponse(
            success=False,
            message="Both layout_id and new_name are required for cloning",
            data=None,
        )
    
    logger.info(f"Cloning email layout: {source_layout_id} as {new_name}")
    
    # First, get the source layout
    get_params = GetEmailLayoutParams(layout_id=source_layout_id)
    source_response = get_email_layout(config, auth_manager, get_params)
    
    if not source_response.success or not source_response.data:
        return EmailLayoutResponse(
            success=False,
            message=f"Could not retrieve source layout: {source_layout_id}",
            data=None,
        )
    
    # Create the cloned layout
    source_data = source_response.data
    create_params = CreateEmailLayoutParams(
        name=new_name,
        description=source_data.get("description", ""),
        layout=source_data.get("layout", ""),
        advanced=source_data.get("advanced") == "true",
        advanced_layout=source_data.get("advanced_layout", ""),
    )
    
    return create_email_layout(config, auth_manager, create_params)