"""
Inbound Email Action tools for the ServiceNow MCP server.

This module provides tools for creating, updating, and deleting Inbound Email Actions in ServiceNow.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateInboundEmailActionParams(BaseModel):
    """Parameters for creating an inbound email action."""

    name: str = Field(..., description="Name of the inbound email action")
    action_type: str = Field(..., description="Type of action (script, table_api, etc.)")
    script: Optional[str] = Field(None, description="Script content for the email action")
    table: Optional[str] = Field(None, description="Target table for table API actions")
    active: bool = Field(True, description="Whether the email action is active")
    order: Optional[int] = Field(None, description="Execution order of the action")
    description: Optional[str] = Field(None, description="Description of the email action")
    condition: Optional[str] = Field(None, description="Condition script to determine when action runs")
    stop_processing: bool = Field(False, description="Stop processing further actions after this one")


class UpdateInboundEmailActionParams(BaseModel):
    """Parameters for updating an inbound email action."""

    action_id: str = Field(..., description="Inbound email action ID or sys_id")
    name: Optional[str] = Field(None, description="Updated name of the inbound email action")
    action_type: Optional[str] = Field(None, description="Updated type of action")
    script: Optional[str] = Field(None, description="Updated script content")
    table: Optional[str] = Field(None, description="Updated target table")
    active: Optional[bool] = Field(None, description="Updated active status")
    order: Optional[int] = Field(None, description="Updated execution order")
    description: Optional[str] = Field(None, description="Updated description")
    condition: Optional[str] = Field(None, description="Updated condition script")
    stop_processing: Optional[bool] = Field(None, description="Updated stop processing flag")


class ListInboundEmailActionsParams(BaseModel):
    """Parameters for listing inbound email actions."""

    query: Optional[str] = Field(None, description="Search query for email actions")
    active: Optional[bool] = Field(None, description="Filter by active status")
    action_type: Optional[str] = Field(None, description="Filter by action type")
    table: Optional[str] = Field(None, description="Filter by target table")
    limit: int = Field(10, description="Maximum number of email actions to return")
    offset: int = Field(0, description="Offset for pagination")


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
    sys_id: Optional[str] = Field(None, description="System ID of the email action")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class InboundEmailActionListResponse(BaseModel):
    """Response from listing inbound email actions."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    actions: List[Dict[str, Any]] = Field(default_factory=list, description="List of email actions")
    total_count: int = Field(0, description="Total number of actions")


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
        Response with inbound email action creation result.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action"

    # Build request data
    data = {
        "name": params.name,
        "type": params.action_type,
        "active": params.active,
        "stop_processing": params.stop_processing,
    }

    if params.script:
        data["script"] = params.script
    if params.table:
        data["table"] = params.table
    if params.order is not None:
        data["order"] = params.order
    if params.description:
        data["description"] = params.description
    if params.condition:
        data["condition"] = params.condition

    # Make request
    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return InboundEmailActionResponse(
            success=True,
            message="Inbound email action created successfully",
            action_id=result.get("name", ""),
            sys_id=result.get("sys_id", ""),
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
        Response with inbound email action update result.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action/{params.action_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.action_type is not None:
        data["type"] = params.action_type
    if params.script is not None:
        data["script"] = params.script
    if params.table is not None:
        data["table"] = params.table
    if params.active is not None:
        data["active"] = params.active
    if params.order is not None:
        data["order"] = params.order
    if params.description is not None:
        data["description"] = params.description
    if params.condition is not None:
        data["condition"] = params.condition
    if params.stop_processing is not None:
        data["stop_processing"] = params.stop_processing

    # Make request
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
            action_id=result.get("name", ""),
            sys_id=result.get("sys_id", ""),
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
) -> InboundEmailActionListResponse:
    """
    List inbound email actions from ServiceNow with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing inbound email actions.

    Returns:
        Response with list of inbound email actions.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build query filters
    filters = []
    
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    
    if params.action_type:
        filters.append(f"type={params.action_type}")
    
    if params.table:
        filters.append(f"table={params.table}")
    
    if params.query:
        # Search in name and description
        filters.append(f"nameLIKE{params.query}^ORdescriptionLIKE{params.query}")

    if filters:
        query_params["sysparm_query"] = "^".join(filters)

    # Make request
    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return InboundEmailActionListResponse(
            success=True,
            message=f"Retrieved {len(result)} inbound email actions",
            actions=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list inbound email actions: {e}")
        return InboundEmailActionListResponse(
            success=False,
            message=f"Failed to list inbound email actions: {str(e)}",
            actions=[],
            total_count=0,
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
        params: Parameters for getting the inbound email action.

    Returns:
        Response with inbound email action data.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action/{params.action_id}"

    # Make request
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
            action_id=result.get("name", ""),
            sys_id=result.get("sys_id", ""),
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
        params: Parameters for deleting the inbound email action.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action/{params.action_id}"

    # Make request
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