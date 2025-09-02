"""
Inbound Email Actions tools for the ServiceNow MCP server.

This module provides comprehensive tools for creating and managing inbound email actions in ServiceNow.
Inbound email actions determine how ServiceNow processes incoming emails and supports ALL available
fields in the sysevent_in_email_action table.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateInboundEmailActionParams(BaseModel):
    """Parameters for creating an inbound email action with ALL available fields."""

    # Core required fields
    name: str = Field(..., description="Name of the inbound email action")
    action: str = Field(..., description="Action type (record_action, script, table_api, etc.)")
    
    # Essential configuration fields
    active: bool = Field(default=True, description="Whether the email action is active")
    type: str = Field(default="new", description="Type of email (new, reply, forward)")
    table: Optional[str] = Field(None, description="Target table for the action")
    event_name: str = Field(default="email.read", description="Event name that triggers this action")
    
    # Processing control fields
    stop_processing: bool = Field(default=False, description="Stop processing further actions after this one")
    condition_script: Optional[str] = Field(None, description="Condition script to determine when action runs")
    filter_condition: Optional[str] = Field(None, description="Filter condition for email processing")
    
    # Script and template fields
    script: Optional[str] = Field(None, description="JavaScript script content for the email action")
    template: Optional[str] = Field(None, description="Field actions template for dynamic processing")
    
    # Assignment and user fields
    from_user: Optional[str] = Field(None, description="From user reference (sys_id)")
    assignment_operator: Optional[str] = Field(None, description="Assignment operator for the action")
    required_roles: Optional[str] = Field(None, description="Required roles to execute this action")
    
    # Email content fields
    reply_email: Optional[str] = Field(None, description="Reply email HTML content only used for action types of reply_email")
    
    # System metadata fields (usually auto-managed but can be set)
    description: Optional[str] = Field(None, description="Description of the email action")
    order: Optional[int] = Field(None, description="Execution order of the action")


class UpdateInboundEmailActionParams(BaseModel):
    """Parameters for updating an inbound email action with ALL available fields."""

    action_id: str = Field(..., description="Inbound email action ID or sys_id")
    
    # All updatable fields (making them optional for updates)
    name: Optional[str] = Field(None, description="Updated name of the inbound email action")
    action: Optional[str] = Field(None, description="Updated action type")
    active: Optional[bool] = Field(None, description="Updated active status")
    type: Optional[str] = Field(None, description="Updated email type")
    table: Optional[str] = Field(None, description="Updated target table")
    event_name: Optional[str] = Field(None, description="Updated event name")
    stop_processing: Optional[bool] = Field(None, description="Updated stop processing flag")
    condition_script: Optional[str] = Field(None, description="Updated condition script")
    filter_condition: Optional[str] = Field(None, description="Updated filter condition")
    script: Optional[str] = Field(None, description="Updated script content")
    template: Optional[str] = Field(None, description="Updated field actions template")
    from_user: Optional[str] = Field(None, description="Updated from user reference")
    assignment_operator: Optional[str] = Field(None, description="Updated assignment operator")
    required_roles: Optional[str] = Field(None, description="Updated required roles")
    reply_email: Optional[str] = Field(None, description="Updated reply email content")
    description: Optional[str] = Field(None, description="Updated description")
    order: Optional[int] = Field(None, description="Updated execution order")


class ListInboundEmailActionsParams(BaseModel):
    """Parameters for listing inbound email actions."""

    active: Optional[bool] = Field(None, description="Filter by active status")
    action: Optional[str] = Field(None, description="Filter by action type")
    type: Optional[str] = Field(None, description="Filter by email type")
    table: Optional[str] = Field(None, description="Filter by target table")
    event_name: Optional[str] = Field(None, description="Filter by event name")
    limit: int = Field(default=10, description="Maximum number of email actions to return")
    offset: int = Field(default=0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Search query for email actions")


class GetInboundEmailActionParams(BaseModel):
    """Parameters for getting a specific inbound email action."""

    action_id: str = Field(..., description="Inbound email action ID or sys_id")


class DeleteInboundEmailActionParams(BaseModel):
    """Parameters for deleting an inbound email action."""

    action_id: str = Field(..., description="Inbound email action ID or sys_id")


class InboundEmailActionResponse(BaseModel):
    """Response from inbound email action operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    action_id: Optional[str] = Field(None, description="ID of the email action")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


def create_inbound_email_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateInboundEmailActionParams,
) -> InboundEmailActionResponse:
    """
    Create a new inbound email action in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the inbound email action.

    Returns:
        Response with created email action details.
    """
    api_url = f"{config.api_url}/table/sysevent_in_email_action"

    # Build request data with exact field names from the table
    data = {
        "name": params.name,
        "action": params.action,
        "active": params.active,
        "type": params.type,
        "event_name": params.event_name,
        "stop_processing": params.stop_processing,
    }

    # Add optional fields if provided
    if params.table:
        data["table"] = params.table
    if params.condition_script:
        data["condition_script"] = params.condition_script
    if params.filter_condition:
        data["filter_condition"] = params.filter_condition
    if params.script:
        data["script"] = params.script
    if params.template:
        data["template"] = params.template
    if params.from_user:
        data["from"] = params.from_user  # Note: field name is 'from' not 'from_user'
    if params.assignment_operator:
        data["assignment_operator"] = params.assignment_operator
    if params.required_roles:
        data["required_roles"] = params.required_roles
    if params.reply_email:
        data["reply_email"] = params.reply_email
    if params.description:
        data["description"] = params.description
    if params.order is not None:
        data["order"] = params.order

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})
        action_id = result.get("sys_id", "")

        return InboundEmailActionResponse(
            success=True,
            message="Inbound email action created successfully",
            action_id=action_id,
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create inbound email action: {e}")
        return InboundEmailActionResponse(
            success=False,
            message=f"Failed to create inbound email action: {str(e)}",
        )


def update_inbound_email_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateInboundEmailActionParams,
) -> InboundEmailActionResponse:
    """
    Update an existing inbound email action in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the inbound email action.

    Returns:
        Response with updated email action details.
    """
    api_url = f"{config.api_url}/table/sysevent_in_email_action/{params.action_id}"

    # Build request data with only non-None values
    data = {}
    if params.name is not None:
        data["name"] = params.name
    if params.action is not None:
        data["action"] = params.action
    if params.active is not None:
        data["active"] = params.active
    if params.type is not None:
        data["type"] = params.type
    if params.table is not None:
        data["table"] = params.table
    if params.event_name is not None:
        data["event_name"] = params.event_name
    if params.stop_processing is not None:
        data["stop_processing"] = params.stop_processing
    if params.condition_script is not None:
        data["condition_script"] = params.condition_script
    if params.filter_condition is not None:
        data["filter_condition"] = params.filter_condition
    if params.script is not None:
        data["script"] = params.script
    if params.template is not None:
        data["template"] = params.template
    if params.from_user is not None:
        data["from"] = params.from_user
    if params.assignment_operator is not None:
        data["assignment_operator"] = params.assignment_operator
    if params.required_roles is not None:
        data["required_roles"] = params.required_roles
    if params.reply_email is not None:
        data["reply_email"] = params.reply_email
    if params.description is not None:
        data["description"] = params.description
    if params.order is not None:
        data["order"] = params.order

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return InboundEmailActionResponse(
            success=True,
            message="Inbound email action updated successfully",
            action_id=params.action_id,
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update inbound email action: {e}")
        return InboundEmailActionResponse(
            success=False,
            message=f"Failed to update inbound email action: {str(e)}",
        )


def list_inbound_email_actions(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListInboundEmailActionsParams,
) -> InboundEmailActionResponse:
    """
    List inbound email actions from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing email actions.

    Returns:
        Response with list of email actions.
    """
    api_url = f"{config.api_url}/table/sysevent_in_email_action"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build encoded query
    query_conditions = []
    if params.active is not None:
        query_conditions.append(f"active={params.active}")
    if params.action:
        query_conditions.append(f"action={params.action}")
    if params.type:
        query_conditions.append(f"type={params.type}")
    if params.table:
        query_conditions.append(f"table={params.table}")
    if params.event_name:
        query_conditions.append(f"event_name={params.event_name}")
    if params.query:
        query_conditions.append(f"nameLIKE{params.query}^ORdescriptionLIKE{params.query}")

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

        return InboundEmailActionResponse(
            success=True,
            message=f"Retrieved {len(result)} inbound email actions",
            data={"actions": result, "count": len(result)},
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list inbound email actions: {e}")
        return InboundEmailActionResponse(
            success=False,
            message=f"Failed to list inbound email actions: {str(e)}",
        )


def get_inbound_email_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetInboundEmailActionParams,
) -> InboundEmailActionResponse:
    """
    Get a specific inbound email action from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the email action.

    Returns:
        Response with email action details.
    """
    api_url = f"{config.api_url}/table/sysevent_in_email_action/{params.action_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return InboundEmailActionResponse(
            success=True,
            message="Inbound email action retrieved successfully",
            action_id=params.action_id,
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get inbound email action: {e}")
        return InboundEmailActionResponse(
            success=False,
            message=f"Failed to get inbound email action: {str(e)}",
        )


def delete_inbound_email_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteInboundEmailActionParams,
) -> InboundEmailActionResponse:
    """
    Delete an inbound email action from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the email action.

    Returns:
        Response confirming deletion.
    """
    api_url = f"{config.api_url}/table/sysevent_in_email_action/{params.action_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return InboundEmailActionResponse(
            success=True,
            message="Inbound email action deleted successfully",
            action_id=params.action_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete inbound email action: {e}")
        return InboundEmailActionResponse(
            success=False,
            message=f"Failed to delete inbound email action: {str(e)}",
        )