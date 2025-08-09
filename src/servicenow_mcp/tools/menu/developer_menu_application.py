"""
Application menu tools for the ServiceNow MCP server.

This module provides tools for managing application menu items in ServiceNow.
Developers can create, update, list, and manage menu items that appear in the
All menu and other navigation areas of the ServiceNow interface.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateApplicationMenuParams(BaseModel):
    """Parameters for creating an application menu item."""

    title: str = Field(..., description="Display title of the menu item")
    name: Optional[str] = Field(None, description="Internal name of the menu item")
    description: Optional[str] = Field(None, description="Description of the menu item")
    active: Optional[bool] = Field(True, description="Whether the menu item is active")
    category: Optional[str] = Field(None, description="Category sys_id for grouping menu items")
    roles: Optional[List[str]] = Field(None, description="List of roles required to access this menu item")
    order: Optional[float] = Field(None, description="Display order (lower numbers appear first)")
    hint: Optional[str] = Field(None, description="Tooltip text displayed on hover")
    device_type: Optional[str] = Field("browser", description="Device type (browser, mobile, tablet)")
    view_name: Optional[str] = Field(None, description="View name for the menu item")
    sys_overrides: Optional[str] = Field(None, description="Sys_id of menu item this overrides")
    sys_domain: Optional[str] = Field("global", description="Domain for the menu item")
    sys_domain_path: Optional[str] = Field("/", description="Domain path for the menu item")


class UpdateApplicationMenuParams(BaseModel):
    """Parameters for updating an application menu item."""

    menu_id: str = Field(..., description="Application menu sys_id to update")
    title: Optional[str] = Field(None, description="Updated display title")
    name: Optional[str] = Field(None, description="Updated internal name")
    description: Optional[str] = Field(None, description="Updated description")
    active: Optional[bool] = Field(None, description="Updated active status")
    category: Optional[str] = Field(None, description="Updated category sys_id")
    roles: Optional[List[str]] = Field(None, description="Updated list of required roles")
    order: Optional[float] = Field(None, description="Updated display order")
    hint: Optional[str] = Field(None, description="Updated tooltip text")
    device_type: Optional[str] = Field(None, description="Updated device type")
    view_name: Optional[str] = Field(None, description="Updated view name")
    sys_overrides: Optional[str] = Field(None, description="Updated override reference")


class ListApplicationMenusParams(BaseModel):
    """Parameters for listing application menu items."""

    active: Optional[bool] = Field(None, description="Filter by active status")
    category: Optional[str] = Field(None, description="Filter by category sys_id")
    device_type: Optional[str] = Field(None, description="Filter by device type")
    title: Optional[str] = Field(None, description="Filter by title (contains)")
    limit: Optional[int] = Field(10, description="Maximum number of menu items to return")
    offset: Optional[int] = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query filter")


class GetApplicationMenuParams(BaseModel):
    """Parameters for getting a specific application menu item."""

    menu_id: str = Field(..., description="Application menu sys_id")


class DeleteApplicationMenuParams(BaseModel):
    """Parameters for deleting an application menu item."""

    menu_id: str = Field(..., description="Application menu sys_id to delete")


class ApplicationMenuResponse(BaseModel):
    """Response from application menu operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    sys_id: Optional[str] = Field(None, description="System ID of the menu item")
    menu_item: Optional[Dict[str, Any]] = Field(None, description="Menu item details")


class ApplicationMenuListResponse(BaseModel):
    """Response from listing application menu items."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    menu_items: List[Dict[str, Any]] = Field(..., description="List of menu items")
    total_count: Optional[int] = Field(None, description="Total number of menu items")


def create_application_menu(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateApplicationMenuParams,
) -> ApplicationMenuResponse:
    """
    Create a new application menu item in ServiceNow.

    This function creates a menu item that appears in the All menu and other
    navigation areas. Developers can use this to add custom menu entries that
    provide access to tables, modules, or other functionality.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the application menu item.

    Returns:
        Response with the created menu item details.
    """
    api_url = f"{config.api_url}/table/sys_app_application"

    # Build request data with all the menu fields
    data = {
        "title": params.title,
        "active": params.active,
        "device_type": params.device_type,
        "sys_domain": params.sys_domain,
        "sys_domain_path": params.sys_domain_path,
    }

    # Add optional fields
    optional_fields = {
        "name": params.name,
        "description": params.description,
        "category": params.category,
        "order": params.order,
        "hint": params.hint,
        "view_name": params.view_name,
        "sys_overrides": params.sys_overrides,
    }

    # Add non-null optional fields
    for field, value in optional_fields.items():
        if value is not None:
            data[field] = value

    # Handle roles list
    if params.roles:
        data["roles"] = ",".join(params.roles)

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return ApplicationMenuResponse(
            success=True,
            message="Application menu item created successfully",
            sys_id=result.get("sys_id"),
            menu_item=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create application menu item: {e}")
        return ApplicationMenuResponse(
            success=False,
            message=f"Failed to create application menu item: {str(e)}",
        )


def update_application_menu(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateApplicationMenuParams,
) -> ApplicationMenuResponse:
    """
    Update an existing application menu item in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the application menu item.

    Returns:
        Response with the updated menu item details.
    """
    api_url = f"{config.api_url}/table/sys_app_application/{params.menu_id}"

    # Build update data with only non-None fields
    data = {}
    
    # Map all possible update fields
    field_mapping = {
        "title": params.title,
        "name": params.name,
        "description": params.description,
        "active": params.active,
        "category": params.category,
        "order": params.order,
        "hint": params.hint,
        "device_type": params.device_type,
        "view_name": params.view_name,
        "sys_overrides": params.sys_overrides,
    }

    # Add non-None fields to data
    for field, value in field_mapping.items():
        if value is not None:
            data[field] = value

    # Handle roles list
    if params.roles is not None:
        data["roles"] = ",".join(params.roles)

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return ApplicationMenuResponse(
            success=True,
            message="Application menu item updated successfully",
            sys_id=result.get("sys_id"),
            menu_item=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update application menu item: {e}")
        return ApplicationMenuResponse(
            success=False,
            message=f"Failed to update application menu item: {str(e)}",
        )


def list_application_menus(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListApplicationMenusParams,
) -> ApplicationMenuListResponse:
    """
    List application menu items from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing application menu items.

    Returns:
        Response with the list of menu items.
    """
    api_url = f"{config.api_url}/table/sys_app_application"
    
    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }
    
    # Build filter conditions
    filters = []
    
    if params.active is not None:
        filters.append(f"active={params.active}")
    
    if params.category:
        filters.append(f"category={params.category}")
    
    if params.device_type:
        filters.append(f"device_type={params.device_type}")
    
    if params.title:
        filters.append(f"titleLIKE{params.title}")
    
    if params.query:
        filters.append(params.query)
    
    if filters:
        query_params["sysparm_query"] = "^".join(filters)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return ApplicationMenuListResponse(
            success=True,
            message=f"Retrieved {len(result)} application menu items",
            menu_items=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list application menu items: {e}")
        return ApplicationMenuListResponse(
            success=False,
            message=f"Failed to list application menu items: {str(e)}",
            menu_items=[],
        )


def get_application_menu(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetApplicationMenuParams,
) -> ApplicationMenuResponse:
    """
    Get a specific application menu item from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the application menu item.

    Returns:
        Response with the menu item details.
    """
    api_url = f"{config.api_url}/table/sys_app_application/{params.menu_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return ApplicationMenuResponse(
            success=True,
            message="Application menu item retrieved successfully",
            sys_id=result.get("sys_id"),
            menu_item=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get application menu item: {e}")
        return ApplicationMenuResponse(
            success=False,
            message=f"Failed to get application menu item: {str(e)}",
        )


def delete_application_menu(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteApplicationMenuParams,
) -> ApplicationMenuResponse:
    """
    Delete an application menu item from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the application menu item.

    Returns:
        Response confirming the deletion.
    """
    api_url = f"{config.api_url}/table/sys_app_application/{params.menu_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return ApplicationMenuResponse(
            success=True,
            message="Application menu item deleted successfully",
            sys_id=params.menu_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete application menu item: {e}")
        return ApplicationMenuResponse(
            success=False,
            message=f"Failed to delete application menu item: {str(e)}",
        )