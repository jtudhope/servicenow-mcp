"""
UI Action tools for the ServiceNow MCP server.

This module provides tools for generating and managing UI Actions including
addition and modification of existing UI actions.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateUIActionParams(BaseModel):
    """Parameters for creating a UI action."""

    name: str = Field(..., description="Name of the UI action")
    table: str = Field(..., description="Table the UI action applies to")
    action_name: str = Field(..., description="Action name (button text)")
    script: str = Field(..., description="Client script for the UI action")
    condition: Optional[str] = Field(None, description="Condition script to show/hide the action")
    onclick: Optional[str] = Field(None, description="OnClick script for the action")
    form_button: Optional[bool] = Field(True, description="Whether to show on form")
    list_banner_button: Optional[bool] = Field(False, description="Whether to show on list banner")
    list_choice: Optional[bool] = Field(False, description="Whether to show in list choice menu")
    list_context_menu: Optional[bool] = Field(False, description="Whether to show in list context menu")
    active: Optional[bool] = Field(True, description="Whether the UI action is active")
    order: Optional[int] = Field(100, description="Order of the UI action")
    hint: Optional[str] = Field(None, description="Tooltip hint for the action")
    client: Optional[bool] = Field(True, description="Whether this is a client-side action")
    isolate_script: Optional[bool] = Field(True, description="Whether to isolate the script")


class UpdateUIActionParams(BaseModel):
    """Parameters for updating a UI action."""

    ui_action_id: str = Field(..., description="UI Action ID or sys_id")
    name: Optional[str] = Field(None, description="Name of the UI action")
    action_name: Optional[str] = Field(None, description="Action name (button text)")
    script: Optional[str] = Field(None, description="Client script for the UI action")
    condition: Optional[str] = Field(None, description="Condition script to show/hide the action")
    onclick: Optional[str] = Field(None, description="OnClick script for the action")
    form_button: Optional[bool] = Field(None, description="Whether to show on form")
    list_banner_button: Optional[bool] = Field(None, description="Whether to show on list banner")
    list_choice: Optional[bool] = Field(None, description="Whether to show in list choice menu")
    list_context_menu: Optional[bool] = Field(None, description="Whether to show in list context menu")
    active: Optional[bool] = Field(None, description="Whether the UI action is active")
    order: Optional[int] = Field(None, description="Order of the UI action")
    hint: Optional[str] = Field(None, description="Tooltip hint for the action")
    client: Optional[bool] = Field(None, description="Whether this is a client-side action")
    isolate_script: Optional[bool] = Field(None, description="Whether to isolate the script")


class ListUIActionsParams(BaseModel):
    """Parameters for listing UI actions."""

    table: Optional[str] = Field(None, description="Filter by table")
    active: Optional[bool] = Field(None, description="Filter by active status")
    limit: int = Field(10, description="Maximum number of UI actions to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Search query for UI actions")


class GetUIActionParams(BaseModel):
    """Parameters for getting a specific UI action."""

    ui_action_id: str = Field(..., description="UI Action ID or sys_id")


class DeleteUIActionParams(BaseModel):
    """Parameters for deleting a UI action."""

    ui_action_id: str = Field(..., description="UI Action ID or sys_id")


class UIActionResponse(BaseModel):
    """Response from UI action operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    ui_action_id: Optional[str] = Field(None, description="ID of the UI action")
    sys_id: Optional[str] = Field(None, description="System ID of the UI action")
    data: Optional[Dict[str, Any]] = Field(None, description="UI action data")


class UIActionsListResponse(BaseModel):
    """Response from list UI actions operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    ui_actions: List[Dict[str, Any]] = Field(..., description="List of UI actions")
    total_count: int = Field(..., description="Total number of UI actions")


def create_ui_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateUIActionParams,
) -> UIActionResponse:
    """
    Create a new UI action in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the UI action.

    Returns:
        Response with created UI action information.
    """
    api_url = f"{config.api_url}/table/sys_ui_action"

    # Build request data
    data = {
        "name": params.name,
        "table": params.table,
        "action_name": params.action_name,
        "script": params.script,
        "form_button": params.form_button,
        "list_banner_button": params.list_banner_button,
        "list_choice": params.list_choice,
        "list_context_menu": params.list_context_menu,
        "active": params.active,
        "order": params.order,
        "client": params.client,
        "isolate_script": params.isolate_script,
    }

    # Add optional fields
    if params.condition:
        data["condition"] = params.condition
    if params.onclick:
        data["onclick"] = params.onclick
    if params.hint:
        data["hint"] = params.hint

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return UIActionResponse(
            success=True,
            message="UI Action created successfully",
            ui_action_id=result.get("number"),
            sys_id=result.get("sys_id"),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create UI action: {e}")
        return UIActionResponse(
            success=False,
            message=f"Failed to create UI action: {str(e)}",
        )


def update_ui_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateUIActionParams,
) -> UIActionResponse:
    """
    Update an existing UI action in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the UI action.

    Returns:
        Response with updated UI action information.
    """
    api_url = f"{config.api_url}/table/sys_ui_action/{params.ui_action_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.action_name is not None:
        data["action_name"] = params.action_name
    if params.script is not None:
        data["script"] = params.script
    if params.condition is not None:
        data["condition"] = params.condition
    if params.onclick is not None:
        data["onclick"] = params.onclick
    if params.form_button is not None:
        data["form_button"] = params.form_button
    if params.list_banner_button is not None:
        data["list_banner_button"] = params.list_banner_button
    if params.list_choice is not None:
        data["list_choice"] = params.list_choice
    if params.list_context_menu is not None:
        data["list_context_menu"] = params.list_context_menu
    if params.active is not None:
        data["active"] = params.active
    if params.order is not None:
        data["order"] = params.order
    if params.hint is not None:
        data["hint"] = params.hint
    if params.client is not None:
        data["client"] = params.client
    if params.isolate_script is not None:
        data["isolate_script"] = params.isolate_script

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return UIActionResponse(
            success=True,
            message="UI Action updated successfully",
            ui_action_id=result.get("number"),
            sys_id=result.get("sys_id"),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update UI action: {e}")
        return UIActionResponse(
            success=False,
            message=f"Failed to update UI action: {str(e)}",
        )


def list_ui_actions(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListUIActionsParams,
) -> UIActionsListResponse:
    """
    List UI actions from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing UI actions.

    Returns:
        Response with list of UI actions.
    """
    api_url = f"{config.api_url}/table/sys_ui_action"
    
    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }
    
    # Build query string
    query_conditions = []
    
    if params.table:
        query_conditions.append(f"table={params.table}")
    if params.active is not None:
        query_conditions.append(f"active={params.active}")
    if params.query:
        # Search in name, action_name, and table fields
        query_conditions.append(f"nameLIKE{params.query}^ORaction_nameLIKE{params.query}^ORtableLIKE{params.query}")
    
    if query_conditions:
        query_params["sysparm_query"] = "^".join(query_conditions)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])
        
        # Get total count for pagination
        count_response = requests.get(
            api_url,
            params={**query_params, "sysparm_display_value": "true", "sysparm_count": "true"},
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        count_response.raise_for_status()
        total_count = int(count_response.headers.get("X-Total-Count", len(result)))

        return UIActionsListResponse(
            success=True,
            message=f"Found {len(result)} UI actions",
            ui_actions=result,
            total_count=total_count,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list UI actions: {e}")
        return UIActionsListResponse(
            success=False,
            message=f"Failed to list UI actions: {str(e)}",
            ui_actions=[],
            total_count=0,
        )


def get_ui_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetUIActionParams,
) -> UIActionResponse:
    """
    Get a specific UI action from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the UI action.

    Returns:
        Response with UI action data.
    """
    api_url = f"{config.api_url}/table/sys_ui_action/{params.ui_action_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return UIActionResponse(
            success=True,
            message="UI Action retrieved successfully",
            ui_action_id=result.get("number"),
            sys_id=result.get("sys_id"),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get UI action: {e}")
        return UIActionResponse(
            success=False,
            message=f"Failed to get UI action: {str(e)}",
        )


def delete_ui_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteUIActionParams,
) -> UIActionResponse:
    """
    Delete a UI action from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the UI action.

    Returns:
        Response indicating success or failure.
    """
    api_url = f"{config.api_url}/table/sys_ui_action/{params.ui_action_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return UIActionResponse(
            success=True,
            message="UI Action deleted successfully",
            ui_action_id=params.ui_action_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete UI action: {e}")
        return UIActionResponse(
            success=False,
            message=f"Failed to delete UI action: {str(e)}",
        )