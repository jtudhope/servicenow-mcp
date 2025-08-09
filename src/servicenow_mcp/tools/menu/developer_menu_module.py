# Create a new file: src/servicenow_mcp/tools/application_modules.py

"""
Application module menu tools for the ServiceNow MCP server.

This module provides tools for managing application module menu items,
which are usually children of application menu items in the sys_app_module table.
"""

import logging
from typing import Optional, List

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateAppModuleParams(BaseModel):
    """Parameters for creating an application module."""

    title: str = Field(..., description="Display title of the module")
    application: str = Field(..., description="Application menu sys_id or name this module belongs to")
    name: Optional[str] = Field(None, description="Table name for list modules")
    link_type: Optional[str] = Field("LIST", description="Link type (LIST, FORM, HOMEPAGE, etc.)")
    order: Optional[int] = Field(None, description="Order for display sequence")
    roles: Optional[str] = Field(None, description="Comma-separated list of required roles")
    active: Optional[bool] = Field(True, description="Whether the module is active")
    filter: Optional[str] = Field(None, description="Filter conditions for list modules")
    query: Optional[str] = Field(None, description="Additional query arguments")
    hint: Optional[str] = Field(None, description="Tooltip hint for the module")
    window_name: Optional[str] = Field(None, description="Window name for opening links")
    view_name: Optional[str] = Field(None, description="View name for list/form modules")
    mobile_title: Optional[str] = Field(None, description="Title for mobile display")
    mobile_view_name: Optional[str] = Field("Mobile", description="Mobile view name")
    device_type: Optional[str] = Field(None, description="Device type (browser, mobile, etc.)")
    uncancelable: Optional[bool] = Field(False, description="Whether module is uncancelable")
    override_menu_roles: Optional[bool] = Field(False, description="Override application menu roles")


class UpdateAppModuleParams(BaseModel):
    """Parameters for updating an application module."""

    module_id: str = Field(..., description="Module sys_id to update")
    title: Optional[str] = Field(None, description="Updated display title")
    application: Optional[str] = Field(None, description="Updated application menu sys_id")
    name: Optional[str] = Field(None, description="Updated table name")
    link_type: Optional[str] = Field(None, description="Updated link type")
    order: Optional[int] = Field(None, description="Updated order")
    roles: Optional[str] = Field(None, description="Updated roles")
    active: Optional[bool] = Field(None, description="Updated active status")
    filter: Optional[str] = Field(None, description="Updated filter conditions")
    query: Optional[str] = Field(None, description="Updated query arguments")
    hint: Optional[str] = Field(None, description="Updated hint")
    window_name: Optional[str] = Field(None, description="Updated window name")
    view_name: Optional[str] = Field(None, description="Updated view name")
    mobile_title: Optional[str] = Field(None, description="Updated mobile title")
    mobile_view_name: Optional[str] = Field(None, description="Updated mobile view name")
    device_type: Optional[str] = Field(None, description="Updated device type")
    uncancelable: Optional[bool] = Field(None, description="Updated uncancelable status")
    override_menu_roles: Optional[bool] = Field(None, description="Updated override menu roles")


class ListAppModulesParams(BaseModel):
    """Parameters for listing application modules."""

    application: Optional[str] = Field(None, description="Filter by application menu sys_id")
    active: Optional[bool] = Field(None, description="Filter by active status")
    name: Optional[str] = Field(None, description="Filter by table name")
    link_type: Optional[str] = Field(None, description="Filter by link type")
    roles: Optional[str] = Field(None, description="Filter by required roles")
    limit: int = Field(10, description="Maximum number of modules to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class AppModuleResponse(BaseModel):
    """Response from application module operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    module: Optional[dict] = Field(None, description="Module data for single operations")
    modules: Optional[List[dict]] = Field(None, description="List of modules for list operations")
    sys_id: Optional[str] = Field(None, description="System ID of created/updated module")


def create_app_module(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateAppModuleParams,
) -> AppModuleResponse:
    """
    Create a new application module menu item.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the module.

    Returns:
        Response with created module information.
    """
    api_url = f"{config.api_url}/table/sys_app_module"

    # Build request data
    data = {
        "title": params.title,
        "application": params.application,
        "link_type": params.link_type,
        "active": params.active,
    }

    # Add optional fields
    if params.name:
        data["name"] = params.name
    if params.order is not None:
        data["order"] = params.order
    if params.roles:
        data["roles"] = params.roles
    if params.filter:
        data["filter"] = params.filter
    if params.query:
        data["query"] = params.query
    if params.hint:
        data["hint"] = params.hint
    if params.window_name:
        data["window_name"] = params.window_name
    if params.view_name:
        data["view_name"] = params.view_name
    if params.mobile_title:
        data["mobile_title"] = params.mobile_title
    if params.mobile_view_name:
        data["mobile_view_name"] = params.mobile_view_name
    if params.device_type:
        data["device_type"] = params.device_type
    if params.uncancelable is not None:
        data["uncancelable"] = params.uncancelable
    if params.override_menu_roles is not None:
        data["override_menu_roles"] = params.override_menu_roles

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AppModuleResponse(
            success=True,
            message="Application module created successfully",
            module=result,
            sys_id=result.get("sys_id"),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create application module: {e}")
        return AppModuleResponse(
            success=False,
            message=f"Failed to create application module: {str(e)}",
        )


def update_app_module(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateAppModuleParams,
) -> AppModuleResponse:
    """
    Update an existing application module.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the module.

    Returns:
        Response with updated module information.
    """
    api_url = f"{config.api_url}/table/sys_app_module/{params.module_id}"

    # Build request data with only non-None fields
    data = {}
    
    if params.title is not None:
        data["title"] = params.title
    if params.application is not None:
        data["application"] = params.application
    if params.name is not None:
        data["name"] = params.name
    if params.link_type is not None:
        data["link_type"] = params.link_type
    if params.order is not None:
        data["order"] = params.order
    if params.roles is not None:
        data["roles"] = params.roles
    if params.active is not None:
        data["active"] = params.active
    if params.filter is not None:
        data["filter"] = params.filter
    if params.query is not None:
        data["query"] = params.query
    if params.hint is not None:
        data["hint"] = params.hint
    if params.window_name is not None:
        data["window_name"] = params.window_name
    if params.view_name is not None:
        data["view_name"] = params.view_name
    if params.mobile_title is not None:
        data["mobile_title"] = params.mobile_title
    if params.mobile_view_name is not None:
        data["mobile_view_name"] = params.mobile_view_name
    if params.device_type is not None:
        data["device_type"] = params.device_type
    if params.uncancelable is not None:
        data["uncancelable"] = params.uncancelable
    if params.override_menu_roles is not None:
        data["override_menu_roles"] = params.override_menu_roles

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AppModuleResponse(
            success=True,
            message="Application module updated successfully",
            module=result,
            sys_id=result.get("sys_id"),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update application module: {e}")
        return AppModuleResponse(
            success=False,
            message=f"Failed to update application module: {str(e)}",
        )


def list_app_modules(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListAppModulesParams,
) -> AppModuleResponse:
    """
    List application modules with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing modules.

    Returns:
        Response with list of modules.
    """
    api_url = f"{config.api_url}/table/sys_app_module"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build filter conditions
    filters = []
    if params.application:
        filters.append(f"application={params.application}")
    if params.active is not None:
        filters.append(f"active={params.active}")
    if params.name:
        filters.append(f"name={params.name}")
    if params.link_type:
        filters.append(f"link_type={params.link_type}")
    if params.roles:
        filters.append(f"rolesLIKE{params.roles}")
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

        return AppModuleResponse(
            success=True,
            message=f"Retrieved {len(result)} application modules",
            modules=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list application modules: {e}")
        return AppModuleResponse(
            success=False,
            message=f"Failed to list application modules: {str(e)}",
        )


def get_app_module(
    config: ServerConfig,
    auth_manager: AuthManager,
    module_id: str,
) -> AppModuleResponse:
    """
    Get a specific application module by sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        module_id: Module sys_id to retrieve.

    Returns:
        Response with module information.
    """
    api_url = f"{config.api_url}/table/sys_app_module/{module_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AppModuleResponse(
            success=True,
            message="Application module retrieved successfully",
            module=result,
            sys_id=result.get("sys_id"),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get application module: {e}")
        return AppModuleResponse(
            success=False,
            message=f"Failed to get application module: {str(e)}",
        )


def delete_app_module(
    config: ServerConfig,
    auth_manager: AuthManager,
    module_id: str,
) -> AppModuleResponse:
    """
    Delete an application module.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        module_id: Module sys_id to delete.

    Returns:
        Response indicating success or failure.
    """
    api_url = f"{config.api_url}/table/sys_app_module/{module_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return AppModuleResponse(
            success=True,
            message="Application module deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete application module: {e}")
        return AppModuleResponse(
            success=False,
            message=f"Failed to delete application module: {str(e)}",
        )