"""
Employee Center Widget Instance Management tools for the ServiceNow MCP server.

This module provides tools for managing widget instances - variations in widget 
configurations on various portals including the Employee Center.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field
import json

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateWidgetInstanceParams(BaseModel):
    """Parameters for creating a widget instance."""

    sp_widget: str = Field(..., description="Widget sys_id that this instance references")
    sp_column: Optional[str] = Field(None, description="Column sys_id where the widget instance is placed")
    title: Optional[str] = Field(None, description="Display title for the widget instance")
    short_description: Optional[str] = Field(None, description="Short description of the widget instance")
    order: Optional[int] = Field(1, description="Display order within the column")
    active: Optional[bool] = Field(True, description="Whether the widget instance is active")
    id: Optional[str] = Field(None, description="Unique identifier for the widget instance")
    widget_parameters: Optional[str] = Field(None, description="JSON-formatted widget configuration parameters")
    class_name: Optional[str] = Field(None, description="Bootstrap class name for styling")
    color: Optional[str] = Field("default", description="Bootstrap color scheme")
    size: Optional[str] = Field("md", description="Bootstrap size (xs, sm, md, lg)")
    glyph: Optional[str] = Field(None, description="Icon/glyph for the widget instance")
    css: Optional[str] = Field(None, description="Custom CSS for the widget instance")
    url: Optional[str] = Field(None, description="URL/HREF for navigation widgets")
    roles: Optional[List[str]] = Field(None, description="Roles required to view this widget instance")


class UpdateWidgetInstanceParams(BaseModel):
    """Parameters for updating a widget instance."""

    instance_id: str = Field(..., description="Widget instance sys_id to update")
    sp_widget: Optional[str] = Field(None, description="Updated widget sys_id")
    sp_column: Optional[str] = Field(None, description="Updated column sys_id")
    title: Optional[str] = Field(None, description="Updated display title")
    short_description: Optional[str] = Field(None, description="Updated short description")
    order: Optional[int] = Field(None, description="Updated display order")
    active: Optional[bool] = Field(None, description="Updated active status")
    id: Optional[str] = Field(None, description="Updated unique identifier")
    widget_parameters: Optional[str] = Field(None, description="Updated JSON widget parameters")
    class_name: Optional[str] = Field(None, description="Updated Bootstrap class name")
    color: Optional[str] = Field(None, description="Updated Bootstrap color")
    size: Optional[str] = Field(None, description="Updated Bootstrap size")
    glyph: Optional[str] = Field(None, description="Updated icon/glyph")
    css: Optional[str] = Field(None, description="Updated custom CSS")
    url: Optional[str] = Field(None, description="Updated URL/HREF")
    roles: Optional[List[str]] = Field(None, description="Updated roles")


class ListWidgetInstancesParams(BaseModel):
    """Parameters for listing widget instances."""

    sp_widget: Optional[str] = Field(None, description="Filter by widget sys_id")
    sp_column: Optional[str] = Field(None, description="Filter by column sys_id")
    active: Optional[bool] = Field(None, description="Filter by active status")
    limit: Optional[int] = Field(10, description="Maximum number of instances to return")
    offset: Optional[int] = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query filter")


class GetWidgetInstanceParams(BaseModel):
    """Parameters for getting a specific widget instance."""

    instance_id: str = Field(..., description="Widget instance sys_id or ID to retrieve")


class DeleteWidgetInstanceParams(BaseModel):
    """Parameters for deleting a widget instance."""

    instance_id: str = Field(..., description="Widget instance sys_id to delete")


class CloneWidgetInstanceParams(BaseModel):
    """Parameters for cloning a widget instance."""

    source_instance_id: str = Field(..., description="Source widget instance sys_id to clone")
    target_column: Optional[str] = Field(None, description="Target column sys_id for the cloned instance")
    title: Optional[str] = Field(None, description="Title for the cloned instance")
    widget_parameters: Optional[str] = Field(None, description="Updated parameters for the cloned instance")


class BulkUpdateWidgetInstancesParams(BaseModel):
    """Parameters for bulk updating widget instances."""

    instance_ids: List[str] = Field(..., description="List of widget instance sys_ids to update")
    updates: Dict[str, Any] = Field(..., description="Fields and values to update")


class WidgetInstanceResponse(BaseModel):
    """Response from widget instance operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    instance: Optional[Dict[str, Any]] = Field(None, description="Widget instance data")
    instances: Optional[List[Dict[str, Any]]] = Field(None, description="Multiple widget instances")
    total_count: Optional[int] = Field(None, description="Total count for list operations")


def create_widget_instance(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateWidgetInstanceParams,
) -> WidgetInstanceResponse:
    """
    Create a new widget instance in ServiceNow Employee Center.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating widget instance.

    Returns:
        Response with created widget instance details.
    """
    api_url = f"{config.api_url}/table/sp_instance"

    # Build request data
    data = {
        "sp_widget": params.sp_widget,
        "active": params.active,
    }

    # Add optional fields
    if params.sp_column:
        data["sp_column"] = params.sp_column
    if params.title:
        data["title"] = params.title
    if params.short_description:
        data["short_description"] = params.short_description
    if params.order is not None:
        data["order"] = params.order
    if params.id:
        data["id"] = params.id
    if params.widget_parameters:
        data["widget_parameters"] = params.widget_parameters
    if params.class_name:
        data["class_name"] = params.class_name
    if params.color:
        data["color"] = params.color
    if params.size:
        data["size"] = params.size
    if params.glyph:
        data["glyph"] = params.glyph
    if params.css:
        data["css"] = params.css
    if params.url:
        data["url"] = params.url
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

        return WidgetInstanceResponse(
            success=True,
            message="Widget instance created successfully",
            instance=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create widget instance: {e}")
        return WidgetInstanceResponse(
            success=False,
            message=f"Failed to create widget instance: {str(e)}",
        )


def update_widget_instance(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateWidgetInstanceParams,
) -> WidgetInstanceResponse:
    """
    Update an existing widget instance in ServiceNow Employee Center.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating widget instance.

    Returns:
        Response with updated widget instance details.
    """
    api_url = f"{config.api_url}/table/sp_instance/{params.instance_id}"

    # Build update data with only provided fields
    data = {}
    
    if params.sp_widget:
        data["sp_widget"] = params.sp_widget
    if params.sp_column:
        data["sp_column"] = params.sp_column
    if params.title is not None:
        data["title"] = params.title
    if params.short_description is not None:
        data["short_description"] = params.short_description
    if params.order is not None:
        data["order"] = params.order
    if params.active is not None:
        data["active"] = params.active
    if params.id is not None:
        data["id"] = params.id
    if params.widget_parameters is not None:
        data["widget_parameters"] = params.widget_parameters
    if params.class_name is not None:
        data["class_name"] = params.class_name
    if params.color is not None:
        data["color"] = params.color
    if params.size is not None:
        data["size"] = params.size
    if params.glyph is not None:
        data["glyph"] = params.glyph
    if params.css is not None:
        data["css"] = params.css
    if params.url is not None:
        data["url"] = params.url
    if params.roles is not None:
        data["roles"] = ",".join(params.roles) if params.roles else ""

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return WidgetInstanceResponse(
            success=True,
            message="Widget instance updated successfully",
            instance=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update widget instance: {e}")
        return WidgetInstanceResponse(
            success=False,
            message=f"Failed to update widget instance: {str(e)}",
        )


def list_widget_instances(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListWidgetInstancesParams,
) -> WidgetInstanceResponse:
    """
    List widget instances from ServiceNow Employee Center with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing widget instances.

    Returns:
        Response with list of widget instances.
    """
    api_url = f"{config.api_url}/table/sp_instance"
    
    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build filter conditions
    filters = []
    if params.sp_widget:
        filters.append(f"sp_widget={params.sp_widget}")
    if params.sp_column:
        filters.append(f"sp_column={params.sp_column}")
    if params.active is not None:
        filters.append(f"active={params.active}")
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

        data = response.json()
        instances = data.get("result", [])

        # Get total count from headers if available
        total_count = len(instances)
        if "x-total-count" in response.headers:
            total_count = int(response.headers["x-total-count"])

        return WidgetInstanceResponse(
            success=True,
            message=f"Retrieved {len(instances)} widget instances",
            instances=instances,
            total_count=total_count,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list widget instances: {e}")
        return WidgetInstanceResponse(
            success=False,
            message=f"Failed to list widget instances: {str(e)}",
        )


def get_widget_instance(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetWidgetInstanceParams,
) -> WidgetInstanceResponse:
    """
    Get a specific widget instance from ServiceNow Employee Center.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting widget instance.

    Returns:
        Response with widget instance details.
    """
    api_url = f"{config.api_url}/table/sp_instance/{params.instance_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return WidgetInstanceResponse(
            success=True,
            message="Widget instance retrieved successfully",
            instance=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get widget instance: {e}")
        return WidgetInstanceResponse(
            success=False,
            message=f"Failed to get widget instance: {str(e)}",
        )


def delete_widget_instance(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteWidgetInstanceParams,
) -> WidgetInstanceResponse:
    """
    Delete a widget instance from ServiceNow Employee Center.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting widget instance.

    Returns:
        Response confirming deletion.
    """
    api_url = f"{config.api_url}/table/sp_instance/{params.instance_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return WidgetInstanceResponse(
            success=True,
            message="Widget instance deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete widget instance: {e}")
        return WidgetInstanceResponse(
            success=False,
            message=f"Failed to delete widget instance: {str(e)}",
        )


def clone_widget_instance(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CloneWidgetInstanceParams,
) -> WidgetInstanceResponse:
    """
    Clone an existing widget instance to create a new instance with modified configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for cloning widget instance.

    Returns:
        Response with cloned widget instance details.
    """
    # First, get the source instance
    get_params = GetWidgetInstanceParams(instance_id=params.source_instance_id)
    source_response = get_widget_instance(config, auth_manager, get_params)
    
    if not source_response.success:
        return WidgetInstanceResponse(
            success=False,
            message=f"Failed to get source instance: {source_response.message}",
        )

    source_instance = source_response.instance
    
    # Create new instance data based on source
    create_params = CreateWidgetInstanceParams(
        sp_widget=source_instance.get("sp_widget", {}).get("value", ""),
        sp_column=params.target_column or source_instance.get("sp_column", {}).get("value"),
        title=params.title or f"Copy of {source_instance.get('title', '')}",
        short_description=source_instance.get("short_description", ""),
        order=source_instance.get("order", 1),
        active=source_instance.get("active", True),
        widget_parameters=params.widget_parameters or source_instance.get("widget_parameters", ""),
        class_name=source_instance.get("class_name", ""),
        color=source_instance.get("color", "default"),
        size=source_instance.get("size", "md"),
        glyph=source_instance.get("glyph", ""),
        css=source_instance.get("css", ""),
        url=source_instance.get("url", ""),
        roles=source_instance.get("roles", "").split(",") if source_instance.get("roles") else None,
    )

    return create_widget_instance(config, auth_manager, create_params)


def bulk_update_widget_instances(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkUpdateWidgetInstancesParams,
) -> WidgetInstanceResponse:
    """
    Bulk update multiple widget instances with the same changes.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for bulk updating widget instances.

    Returns:
        Response with summary of bulk update operation.
    """
    successful_updates = []
    failed_updates = []

    for instance_id in params.instance_ids:
        try:
            # Create update params for this instance
            update_params = UpdateWidgetInstanceParams(
                instance_id=instance_id,
                **params.updates
            )
            
            result = update_widget_instance(config, auth_manager, update_params)
            
            if result.success:
                successful_updates.append(instance_id)
            else:
                failed_updates.append({"instance_id": instance_id, "error": result.message})
                
        except Exception as e:
            failed_updates.append({"instance_id": instance_id, "error": str(e)})

    success = len(failed_updates) == 0
    message = f"Updated {len(successful_updates)} instances successfully"
    if failed_updates:
        message += f", {len(failed_updates)} failed"

    return WidgetInstanceResponse(
        success=success,
        message=message,
        instances=[
            {"successful_updates": successful_updates, "failed_updates": failed_updates}
        ]
    )