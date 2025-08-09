# File: src/servicenow_mcp/tools/portal/portal_rows.py

"""
Portal UI Row Management tools for the ServiceNow MCP server.

This module provides tools for managing portal row configurations in the sp_row table,
including creating, updating, listing, and cloning portal rows.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreatePortalRowParams(BaseModel):
    """Parameters for creating a portal row."""

    sp_container: Optional[str] = Field(None, description="Container sys_id that this row belongs to")
    sp_column: Optional[str] = Field(None, description="Column sys_id that this row belongs to")
    class_name: Optional[str] = Field(None, description="CSS class name for styling")
    order: Optional[int] = Field(None, description="Display order within the container/column")
    semantic_tag: Optional[str] = Field(None, description="Semantic HTML tag (e.g., 'section', 'article', 'div')")


class UpdatePortalRowParams(BaseModel):
    """Parameters for updating a portal row."""

    row_id: str = Field(..., description="Row sys_id to update")
    sp_container: Optional[str] = Field(None, description="Updated container sys_id")
    sp_column: Optional[str] = Field(None, description="Updated column sys_id")
    class_name: Optional[str] = Field(None, description="Updated CSS class name")
    order: Optional[int] = Field(None, description="Updated display order")
    semantic_tag: Optional[str] = Field(None, description="Updated semantic HTML tag")


class ListPortalRowsParams(BaseModel):
    """Parameters for listing portal rows."""

    limit: int = Field(10, description="Maximum number of rows to return")
    offset: int = Field(0, description="Offset for pagination")
    sp_container: Optional[str] = Field(None, description="Filter by container sys_id")
    sp_column: Optional[str] = Field(None, description="Filter by column sys_id")
    semantic_tag: Optional[str] = Field(None, description="Filter by semantic tag")
    query: Optional[str] = Field(None, description="Additional query string")


class ClonePortalRowParams(BaseModel):
    """Parameters for cloning a portal row."""

    source_row_id: str = Field(..., description="Source row sys_id to clone")
    target_container: Optional[str] = Field(None, description="Target container sys_id for the cloned row")
    target_column: Optional[str] = Field(None, description="Target column sys_id for the cloned row")
    copy_class_name: Optional[bool] = Field(True, description="Whether to copy CSS class name from source")
    new_order: Optional[int] = Field(None, description="Order for the cloned row (auto-calculated if not provided)")
    copy_semantic_tag: Optional[bool] = Field(True, description="Whether to copy semantic tag from source")


class GetPortalRowParams(BaseModel):
    """Parameters for getting a specific portal row."""

    row_id: str = Field(..., description="Row sys_id to retrieve")


class DeletePortalRowParams(BaseModel):
    """Parameters for deleting a portal row."""

    row_id: str = Field(..., description="Row sys_id to delete")


class ReorderPortalRowsParams(BaseModel):
    """Parameters for reordering portal rows."""

    container_id: Optional[str] = Field(None, description="Container sys_id to reorder rows within")
    column_id: Optional[str] = Field(None, description="Column sys_id to reorder rows within")
    row_order: List[str] = Field(..., description="List of row sys_ids in desired order")


class PortalRowResponse(BaseModel):
    """Response from portal row operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    row_id: Optional[str] = Field(None, description="Row sys_id")
    row_data: Optional[Dict[str, Any]] = Field(None, description="Row data")
    rows: Optional[List[Dict[str, Any]]] = Field(None, description="List of rows for list operations")
    total_count: Optional[int] = Field(None, description="Total count for list operations")


def create_portal_row(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalRowParams,
) -> PortalRowResponse:
    """
    Create a new portal row in the sp_row table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the portal row.

    Returns:
        Response with creation result and row details.
    """
    api_url = f"{config.api_url}/table/sp_row"

    # Build request data - at least one of sp_container or sp_column is typically required
    data = {}

    if params.sp_container is not None:
        data["sp_container"] = params.sp_container
    if params.sp_column is not None:
        data["sp_column"] = params.sp_column
    if params.class_name is not None:
        data["class_name"] = params.class_name
    if params.order is not None:
        data["order"] = params.order
    if params.semantic_tag is not None:
        data["semantic_tag"] = params.semantic_tag

    # Validate that at least container or column is specified
    if not params.sp_container and not params.sp_column:
        return PortalRowResponse(
            success=False,
            message="Either sp_container or sp_column must be specified when creating a row",
        )

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalRowResponse(
            success=True,
            message="Portal row created successfully",
            row_id=result.get("sys_id"),
            row_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create portal row: {e}")
        return PortalRowResponse(
            success=False,
            message=f"Failed to create portal row: {str(e)}",
        )


def update_portal_row(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdatePortalRowParams,
) -> PortalRowResponse:
    """
    Update an existing portal row in the sp_row table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the portal row.

    Returns:
        Response with update result and row details.
    """
    api_url = f"{config.api_url}/table/sp_row/{params.row_id}"

    # Build update data
    data = {}
    
    if params.sp_container is not None:
        data["sp_container"] = params.sp_container
    if params.sp_column is not None:
        data["sp_column"] = params.sp_column
    if params.class_name is not None:
        data["class_name"] = params.class_name
    if params.order is not None:
        data["order"] = params.order
    if params.semantic_tag is not None:
        data["semantic_tag"] = params.semantic_tag

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalRowResponse(
            success=True,
            message="Portal row updated successfully",
            row_id=result.get("sys_id"),
            row_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update portal row: {e}")
        return PortalRowResponse(
            success=False,
            message=f"Failed to update portal row: {str(e)}",
        )


def list_portal_rows(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalRowsParams,
) -> PortalRowResponse:
    """
    List portal rows from the sp_row table with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing portal rows.

    Returns:
        Response with list of rows and pagination details.
    """
    api_url = f"{config.api_url}/table/sp_row"

    # Build query parameters
    query_parts = []
    
    if params.sp_container is not None:
        query_parts.append(f"sp_container={params.sp_container}")
    if params.sp_column is not None:
        query_parts.append(f"sp_column={params.sp_column}")
    if params.semantic_tag is not None:
        query_parts.append(f"semantic_tag={params.semantic_tag}")
    if params.query:
        query_parts.append(params.query)

    query_string = "^".join(query_parts) if query_parts else ""

    request_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_count": "true",
        "sysparm_display_value": "true",
    }
    
    if query_string:
        request_params["sysparm_query"] = query_string

    try:
        response = requests.get(
            api_url,
            params=request_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])
        total_count = int(response.headers.get("X-Total-Count", 0))

        return PortalRowResponse(
            success=True,
            message=f"Retrieved {len(result)} portal rows",
            rows=result,
            total_count=total_count,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list portal rows: {e}")
        return PortalRowResponse(
            success=False,
            message=f"Failed to list portal rows: {str(e)}",
        )


def get_portal_row(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalRowParams,
) -> PortalRowResponse:
    """
    Get a specific portal row by sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the portal row.

    Returns:
        Response with row details.
    """
    api_url = f"{config.api_url}/table/sp_row/{params.row_id}"

    try:
        response = requests.get(
            api_url,
            params={"sysparm_display_value": "true"},
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalRowResponse(
            success=True,
            message="Portal row retrieved successfully",
            row_id=result.get("sys_id"),
            row_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get portal row: {e}")
        return PortalRowResponse(
            success=False,
            message=f"Failed to get portal row: {str(e)}",
        )


def clone_portal_row(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ClonePortalRowParams,
) -> PortalRowResponse:
    """
    Clone an existing portal row to create a duplicate with modifications.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for cloning the portal row.

    Returns:
        Response with cloned row details.
    """
    # First, get the source row
    get_params = GetPortalRowParams(row_id=params.source_row_id)
    source_result = get_portal_row(config, auth_manager, get_params)
    
    if not source_result.success:
        return PortalRowResponse(
            success=False,
            message=f"Failed to find source row: {source_result.message}",
        )

    source_data = source_result.row_data
    
    # Create clone data based on source
    clone_data = {}

    # Use target container/column if specified, otherwise use source values
    if params.target_container is not None:
        clone_data["sp_container"] = params.target_container
    elif source_data.get("sp_container"):
        clone_data["sp_container"] = source_data["sp_container"]["value"] if isinstance(source_data["sp_container"], dict) else source_data["sp_container"]

    if params.target_column is not None:
        clone_data["sp_column"] = params.target_column
    elif source_data.get("sp_column"):
        clone_data["sp_column"] = source_data["sp_column"]["value"] if isinstance(source_data["sp_column"], dict) else source_data["sp_column"]

    # Conditionally copy class name and semantic tag
    if params.copy_class_name and source_data.get("class_name"):
        clone_data["class_name"] = source_data["class_name"]
    
    if params.copy_semantic_tag and source_data.get("semantic_tag"):
        clone_data["semantic_tag"] = source_data["semantic_tag"]

    # Set order
    if params.new_order is not None:
        clone_data["order"] = params.new_order
    # If no order specified, let ServiceNow auto-calculate it

    # Validate that at least container or column is specified
    if not clone_data.get("sp_container") and not clone_data.get("sp_column"):
        return PortalRowResponse(
            success=False,
            message="Either target_container, target_column, or source row must have container/column specified",
        )

    # Create the cloned row
    api_url = f"{config.api_url}/table/sp_row"

    try:
        response = requests.post(
            api_url,
            json=clone_data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalRowResponse(
            success=True,
            message=f"Portal row cloned successfully from {params.source_row_id}",
            row_id=result.get("sys_id"),
            row_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to clone portal row: {e}")
        return PortalRowResponse(
            success=False,
            message=f"Failed to clone portal row: {str(e)}",
        )


def delete_portal_row(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalRowParams,
) -> PortalRowResponse:
    """
    Delete a portal row by sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the portal row.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sp_row/{params.row_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return PortalRowResponse(
            success=True,
            message="Portal row deleted successfully",
            row_id=params.row_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete portal row: {e}")
        return PortalRowResponse(
            success=False,
            message=f"Failed to delete portal row: {str(e)}",
        )


def reorder_portal_rows(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ReorderPortalRowsParams,
) -> PortalRowResponse:
    """
    Reorder portal rows within a container or column.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for reordering the portal rows.

    Returns:
        Response with reordering result.
    """
    if not params.container_id and not params.column_id:
        return PortalRowResponse(
            success=False,
            message="Either container_id or column_id must be specified for reordering",
        )

    updated_rows = []
    failed_updates = []

    # Update each row with its new order
    for index, row_id in enumerate(params.row_order):
        new_order = index + 1  # Start from 1
        
        update_params = UpdatePortalRowParams(
            row_id=row_id,
            order=new_order
        )
        
        result = update_portal_row(config, auth_manager, update_params)
        
        if result.success:
            updated_rows.append(row_id)
        else:
            failed_updates.append(f"Row {row_id}: {result.message}")

    if failed_updates:
        return PortalRowResponse(
            success=False,
            message=f"Failed to reorder some rows: {'; '.join(failed_updates)}",
        )

    return PortalRowResponse(
        success=True,
        message=f"Successfully reordered {len(updated_rows)} portal rows",
    )