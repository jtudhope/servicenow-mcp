# File: src/servicenow_mcp/tools/portal_columns.py

"""
Portal UI Column Management tools for the ServiceNow MCP server.

This module provides tools for managing portal column configurations in the sp_column table,
including creating, updating, listing, and cloning portal columns.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreatePortalColumnParams(BaseModel):
    """Parameters for creating a portal column."""

    sp_row: str = Field(..., description="Row sys_id that this column belongs to")
    class_name: Optional[str] = Field(None, description="CSS class name for styling")
    order: Optional[int] = Field(None, description="Display order within the row")
    size: Optional[int] = Field(None, description="Bootstrap column size for medium devices (1-12)")
    size_xs: Optional[int] = Field(None, description="Bootstrap column size for extra small devices (1-12)")
    size_sm: Optional[int] = Field(None, description="Bootstrap column size for small devices (1-12)")
    size_lg: Optional[int] = Field(None, description="Bootstrap column size for large devices (1-12)")
    semantic_tag: Optional[str] = Field(None, description="Semantic HTML tag (e.g., 'aside', 'article', 'div')")


class UpdatePortalColumnParams(BaseModel):
    """Parameters for updating a portal column."""

    column_id: str = Field(..., description="Column sys_id to update")
    sp_row: Optional[str] = Field(None, description="Updated row sys_id")
    class_name: Optional[str] = Field(None, description="Updated CSS class name")
    order: Optional[int] = Field(None, description="Updated display order")
    size: Optional[int] = Field(None, description="Updated Bootstrap column size for medium devices (1-12)")
    size_xs: Optional[int] = Field(None, description="Updated Bootstrap column size for extra small devices (1-12)")
    size_sm: Optional[int] = Field(None, description="Updated Bootstrap column size for small devices (1-12)")
    size_lg: Optional[int] = Field(None, description="Updated Bootstrap column size for large devices (1-12)")
    semantic_tag: Optional[str] = Field(None, description="Updated semantic HTML tag")


class ListPortalColumnsParams(BaseModel):
    """Parameters for listing portal columns."""

    limit: int = Field(10, description="Maximum number of columns to return")
    offset: int = Field(0, description="Offset for pagination")
    sp_row: Optional[str] = Field(None, description="Filter by row sys_id")
    semantic_tag: Optional[str] = Field(None, description="Filter by semantic tag")
    size_filter: Optional[str] = Field(None, description="Filter by size range (e.g., '>=6' or '=12')")
    query: Optional[str] = Field(None, description="Additional query string")


class ClonePortalColumnParams(BaseModel):
    """Parameters for cloning a portal column."""

    source_column_id: str = Field(..., description="Source column sys_id to clone")
    target_row: str = Field(..., description="Target row sys_id for the cloned column")
    copy_class_name: Optional[bool] = Field(True, description="Whether to copy CSS class name from source")
    copy_sizes: Optional[bool] = Field(True, description="Whether to copy all responsive sizes from source")
    copy_semantic_tag: Optional[bool] = Field(True, description="Whether to copy semantic tag from source")
    new_order: Optional[int] = Field(None, description="Order for the cloned column (auto-calculated if not provided)")
    override_sizes: Optional[Dict[str, int]] = Field(None, description="Override specific sizes (e.g., {'size': 6, 'size_sm': 12})")


class GetPortalColumnParams(BaseModel):
    """Parameters for getting a specific portal column."""

    column_id: str = Field(..., description="Column sys_id to retrieve")


class DeletePortalColumnParams(BaseModel):
    """Parameters for deleting a portal column."""

    column_id: str = Field(..., description="Column sys_id to delete")


class ReorderPortalColumnsParams(BaseModel):
    """Parameters for reordering portal columns."""

    row_id: str = Field(..., description="Row sys_id to reorder columns within")
    column_order: List[str] = Field(..., description="List of column sys_ids in desired order")


class CreateResponsiveGridParams(BaseModel):
    """Parameters for creating a responsive grid layout."""

    sp_row: str = Field(..., description="Row sys_id to create columns in")
    grid_layout: List[Dict[str, Any]] = Field(..., description="List of column configurations")


class PortalColumnResponse(BaseModel):
    """Response from portal column operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    column_id: Optional[str] = Field(None, description="Column sys_id")
    column_data: Optional[Dict[str, Any]] = Field(None, description="Column data")
    columns: Optional[List[Dict[str, Any]]] = Field(None, description="List of columns for list operations")
    total_count: Optional[int] = Field(None, description="Total count for list operations")


def create_portal_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalColumnParams,
) -> PortalColumnResponse:
    """
    Create a new portal column in the sp_column table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the portal column.

    Returns:
        Response with creation result and column details.
    """
    api_url = f"{config.api_url}/table/sp_column"

    # Build request data
    data = {
        "sp_row": params.sp_row,
    }

    # Add optional fields
    if params.class_name is not None:
        data["class_name"] = params.class_name
    if params.order is not None:
        data["order"] = params.order
    if params.size is not None:
        data["size"] = params.size
    if params.size_xs is not None:
        data["size_xs"] = params.size_xs
    if params.size_sm is not None:
        data["size_sm"] = params.size_sm
    if params.size_lg is not None:
        data["size_lg"] = params.size_lg
    if params.semantic_tag is not None:
        data["semantic_tag"] = params.semantic_tag

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalColumnResponse(
            success=True,
            message="Portal column created successfully",
            column_id=result.get("sys_id"),
            column_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create portal column: {e}")
        return PortalColumnResponse(
            success=False,
            message=f"Failed to create portal column: {str(e)}",
        )


def update_portal_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdatePortalColumnParams,
) -> PortalColumnResponse:
    """
    Update an existing portal column in the sp_column table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the portal column.

    Returns:
        Response with update result and column details.
    """
    api_url = f"{config.api_url}/table/sp_column/{params.column_id}"

    # Build update data
    data = {}
    
    if params.sp_row is not None:
        data["sp_row"] = params.sp_row
    if params.class_name is not None:
        data["class_name"] = params.class_name
    if params.order is not None:
        data["order"] = params.order
    if params.size is not None:
        data["size"] = params.size
    if params.size_xs is not None:
        data["size_xs"] = params.size_xs
    if params.size_sm is not None:
        data["size_sm"] = params.size_sm
    if params.size_lg is not None:
        data["size_lg"] = params.size_lg
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

        return PortalColumnResponse(
            success=True,
            message="Portal column updated successfully",
            column_id=result.get("sys_id"),
            column_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update portal column: {e}")
        return PortalColumnResponse(
            success=False,
            message=f"Failed to update portal column: {str(e)}",
        )


def list_portal_columns(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalColumnsParams,
) -> PortalColumnResponse:
    """
    List portal columns from the sp_column table with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing portal columns.

    Returns:
        Response with list of columns and pagination details.
    """
    api_url = f"{config.api_url}/table/sp_column"

    # Build query parameters
    query_parts = []
    
    if params.sp_row is not None:
        query_parts.append(f"sp_row={params.sp_row}")
    if params.semantic_tag is not None:
        query_parts.append(f"semantic_tag={params.semantic_tag}")
    if params.size_filter is not None:
        # Handle size filtering (e.g., ">=6", "=12", "<8")
        query_parts.append(f"size{params.size_filter}")
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

        return PortalColumnResponse(
            success=True,
            message=f"Retrieved {len(result)} portal columns",
            columns=result,
            total_count=total_count,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list portal columns: {e}")
        return PortalColumnResponse(
            success=False,
            message=f"Failed to list portal columns: {str(e)}",
        )


def get_portal_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalColumnParams,
) -> PortalColumnResponse:
    """
    Get a specific portal column by sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the portal column.

    Returns:
        Response with column details.
    """
    api_url = f"{config.api_url}/table/sp_column/{params.column_id}"

    try:
        response = requests.get(
            api_url,
            params={"sysparm_display_value": "true"},
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalColumnResponse(
            success=True,
            message="Portal column retrieved successfully",
            column_id=result.get("sys_id"),
            column_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get portal column: {e}")
        return PortalColumnResponse(
            success=False,
            message=f"Failed to get portal column: {str(e)}",
        )


def clone_portal_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ClonePortalColumnParams,
) -> PortalColumnResponse:
    """
    Clone an existing portal column to create a duplicate with modifications.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for cloning the portal column.

    Returns:
        Response with cloned column details.
    """
    # First, get the source column
    get_params = GetPortalColumnParams(column_id=params.source_column_id)
    source_result = get_portal_column(config, auth_manager, get_params)
    
    if not source_result.success:
        return PortalColumnResponse(
            success=False,
            message=f"Failed to find source column: {source_result.message}",
        )

    source_data = source_result.column_data
    
    # Create clone data based on source
    clone_data = {
        "sp_row": params.target_row,
    }

    # Conditionally copy properties
    if params.copy_class_name and source_data.get("class_name"):
        clone_data["class_name"] = source_data["class_name"]
    
    if params.copy_semantic_tag and source_data.get("semantic_tag"):
        clone_data["semantic_tag"] = source_data["semantic_tag"]

    # Handle responsive sizes
    if params.copy_sizes:
        # Copy all size fields from source
        for size_field in ["size", "size_xs", "size_sm", "size_lg"]:
            if source_data.get(size_field):
                clone_data[size_field] = source_data[size_field]

    # Apply size overrides if specified
    if params.override_sizes:
        for size_field, size_value in params.override_sizes.items():
            if size_field in ["size", "size_xs", "size_sm", "size_lg"]:
                clone_data[size_field] = size_value

    # Set order
    if params.new_order is not None:
        clone_data["order"] = params.new_order
    # If no order specified, let ServiceNow auto-calculate it

    # Create the cloned column
    api_url = f"{config.api_url}/table/sp_column"

    try:
        response = requests.post(
            api_url,
            json=clone_data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalColumnResponse(
            success=True,
            message=f"Portal column cloned successfully from {params.source_column_id}",
            column_id=result.get("sys_id"),
            column_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to clone portal column: {e}")
        return PortalColumnResponse(
            success=False,
            message=f"Failed to clone portal column: {str(e)}",
        )


def delete_portal_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalColumnParams,
) -> PortalColumnResponse:
    """
    Delete a portal column by sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the portal column.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sp_column/{params.column_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return PortalColumnResponse(
            success=True,
            message="Portal column deleted successfully",
            column_id=params.column_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete portal column: {e}")
        return PortalColumnResponse(
            success=False,
            message=f"Failed to delete portal column: {str(e)}",
        )


def reorder_portal_columns(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ReorderPortalColumnsParams,
) -> PortalColumnResponse:
    """
    Reorder portal columns within a row.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for reordering the portal columns.

    Returns:
        Response with reordering result.
    """
    updated_columns = []
    failed_updates = []

    # Update each column with its new order
    for index, column_id in enumerate(params.column_order):
        new_order = index + 1  # Start from 1
        
        update_params = UpdatePortalColumnParams(
            column_id=column_id,
            order=new_order
        )
        
        result = update_portal_column(config, auth_manager, update_params)
        
        if result.success:
            updated_columns.append(column_id)
        else:
            failed_updates.append(f"Column {column_id}: {result.message}")

    if failed_updates:
        return PortalColumnResponse(
            success=False,
            message=f"Failed to reorder some columns: {'; '.join(failed_updates)}",
        )

    return PortalColumnResponse(
        success=True,
        message=f"Successfully reordered {len(updated_columns)} portal columns",
    )


def create_responsive_grid(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateResponsiveGridParams,
) -> PortalColumnResponse:
    """
    Create a responsive grid layout by creating multiple columns with specified configurations.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the responsive grid.

    Returns:
        Response with grid creation result.
    """
    created_columns = []
    failed_creations = []

    # Create each column in the grid
    for index, column_config in enumerate(params.grid_layout):
        # Build column parameters
        column_params = CreatePortalColumnParams(
            sp_row=params.sp_row,
            order=index + 1,
            **column_config
        )
        
        result = create_portal_column(config, auth_manager, column_params)
        
        if result.success:
            created_columns.append(result.column_id)
        else:
            failed_creations.append(f"Column {index + 1}: {result.message}")

    if failed_creations:
        return PortalColumnResponse(
            success=False,
            message=f"Failed to create some columns: {'; '.join(failed_creations)}",
        )

    return PortalColumnResponse(
        success=True,
        message=f"Successfully created {len(created_columns)} columns in responsive grid",
        columns=created_columns,
    )