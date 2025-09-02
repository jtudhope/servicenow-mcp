"""
Table tools for the ServiceNow MCP server.

This module provides tools for creating and managing custom tables and table columns in ServiceNow.
"""

import logging
from typing import Optional, List, Dict, Any

import requests

from servicenow_mcp.auth.session_manager import get_session

from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateTableParams(BaseModel):
    """Parameters for creating a custom table."""

    name: str = Field(..., description="Internal name of the table (e.g., u_custom_table)")
    label: str = Field(..., description="Display label for the table")
    is_extendable: bool = Field(True, description="Whether the table can be extended")
    access: str = Field("public", description="Access level for the table (public, protected, package_private)")
    scope: Optional[str] = Field(None, description="Application scope for the table")
    super_class: str = Field("", description="Parent table to extend from (leave empty for base table)")
    user_role: Optional[str] = Field(None, description="Role required to access this table")
    create_access_controls: bool = Field(True, description="Whether to create default access controls")
    create_module: bool = Field(True, description="Whether to create application menu module")
    number_ref: bool = Field(False, description="Whether to add a number reference field")
    audit: bool = Field(True, description="Whether to enable auditing for the table")


class CreateTableColumnParams(BaseModel):
    """Parameters for creating a table column."""

    table_name: str = Field(..., description="Name of the table to add the column to")
    column_name: str = Field(..., description="Internal name of the column")
    column_label: str = Field(..., description="Display label for the column")
    type: str = Field(..., description="Data type of the column (string, integer, boolean, reference, etc.)")
    max_length: Optional[int] = Field(None, description="Maximum length for string fields")
    mandatory: bool = Field(False, description="Whether the field is required")
    read_only: bool = Field(False, description="Whether the field is read-only")
    reference_table: Optional[str] = Field(None, description="Referenced table for reference fields")
    reference_qualifier: Optional[str] = Field(None, description="Reference qualifier for reference fields")
    choice_list: Optional[List[str]] = Field(None, description="List of choices for choice fields")
    default_value: Optional[str] = Field(None, description="Default value for the field")
    help_text: Optional[str] = Field(None, description="Help text for the field")


class UpdateTableParams(BaseModel):
    """Parameters for updating a table."""

    table_name: str = Field(..., description="Name of the table to update")
    label: Optional[str] = Field(None, description="Updated display label")
    is_extendable: Optional[bool] = Field(None, description="Updated extendable setting")
    access: Optional[str] = Field(None, description="Updated access level")
    user_role: Optional[str] = Field(None, description="Updated role requirement")
    audit: Optional[bool] = Field(None, description="Updated audit setting")


class UpdateTableColumnParams(BaseModel):
    """Parameters for updating a table column."""

    table_name: str = Field(..., description="Name of the table containing the column")
    column_name: str = Field(..., description="Name of the column to update")
    column_label: Optional[str] = Field(None, description="Updated display label")
    max_length: Optional[int] = Field(None, description="Updated maximum length")
    mandatory: Optional[bool] = Field(None, description="Updated mandatory setting")
    read_only: Optional[bool] = Field(None, description="Updated read-only setting")
    reference_qualifier: Optional[str] = Field(None, description="Updated reference qualifier")
    default_value: Optional[str] = Field(None, description="Updated default value")
    help_text: Optional[str] = Field(None, description="Updated help text")


class ListTablesParams(BaseModel):
    """Parameters for listing tables."""

    query: Optional[str] = Field(None, description="Search query for tables")
    scope: Optional[str] = Field(None, description="Filter by application scope")
    super_class: Optional[str] = Field(None, description="Filter by parent table")
    user_table: bool = Field(True, description="Filter to user-created tables only")
    limit: int = Field(10, description="Maximum number of tables to return")
    offset: int = Field(0, description="Offset for pagination")


class ListTableColumnsParams(BaseModel):
    """Parameters for listing table columns."""

    table_name: str = Field(..., description="Name of the table to list columns for")
    active: bool = Field(True, description="Filter to active columns only")
    limit: int = Field(50, description="Maximum number of columns to return")
    offset: int = Field(0, description="Offset for pagination")


class GetTableParams(BaseModel):
    """Parameters for getting table details."""

    table_name: str = Field(..., description="Name of the table to retrieve")


class GetTableColumnParams(BaseModel):
    """Parameters for getting table column details."""

    table_name: str = Field(..., description="Name of the table")
    column_name: str = Field(..., description="Name of the column")


class TableResponse(BaseModel):
    """Response from table operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    table_name: Optional[str] = Field(None, description="Name of the table")
    sys_id: Optional[str] = Field(None, description="System ID of the table")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class TableListResponse(BaseModel):
    """Response from listing tables."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    tables: List[Dict[str, Any]] = Field(default_factory=list, description="List of tables")
    total_count: int = Field(0, description="Total number of tables")


class TableColumnResponse(BaseModel):
    """Response from table column operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    column_name: Optional[str] = Field(None, description="Name of the column")
    sys_id: Optional[str] = Field(None, description="System ID of the column")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class TableColumnListResponse(BaseModel):
    """Response from listing table columns."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    columns: List[Dict[str, Any]] = Field(default_factory=list, description="List of columns")
    total_count: int = Field(0, description="Total number of columns")


def create_table(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateTableParams,
) -> TableResponse:
    """
    Create a new custom table in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the table.

    Returns:
        Response with table creation result.
    """
    api_url = f"{config.api_url}/table/sys_db_object"

    # Build request data
    data = {
        "name": params.name,
        "label": params.label,
        "is_extendable": params.is_extendable,
        "access": params.access,
        "super_class": params.super_class,
        "create_access_controls": params.create_access_controls,
        "create_module": params.create_module,
        "number_ref": params.number_ref,
        "audit": params.audit,
    }

    if params.scope:
        data["sys_scope"] = params.scope
    if params.user_role:
        data["user_role"] = params.user_role

    # Make request
    try:
        session = get_session() 
        response = session.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return TableResponse(
            success=True,
            message="Table created successfully",
            table_name=result.get("name", ""),
            sys_id=result.get("sys_id", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create table: {e}")
        return TableResponse(
            success=False,
            message=f"Failed to create table: {str(e)}",
        )


def create_table_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateTableColumnParams,
) -> TableColumnResponse:
    """
    Create a new column in a table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the table column.

    Returns:
        Response with table column creation result.
    """
    api_url = f"{config.api_url}/table/sys_dictionary"

    # Build request data
    data = {
        "name": params.table_name,
        "element": params.column_name,
        "column_label": params.column_label,
        "internal_type": params.type,
        "mandatory": params.mandatory,
        "read_only": params.read_only,
    }

    if params.max_length is not None:
        data["max_length"] = params.max_length
    if params.reference_table:
        data["reference"] = params.reference_table
    if params.reference_qualifier:
        data["reference_qual"] = params.reference_qualifier
    if params.default_value:
        data["default_value"] = params.default_value
    if params.help_text:
        data["help"] = params.help_text

    # Handle choice lists
    if params.choice_list and params.type == "choice":
        # Note: Choice creation requires additional API calls to sys_choice table
        # This would need to be implemented separately after column creation
        pass

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

        return TableColumnResponse(
            success=True,
            message="Table column created successfully",
            column_name=result.get("element", ""),
            sys_id=result.get("sys_id", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create table column: {e}")
        return TableColumnResponse(
            success=False,
            message=f"Failed to create table column: {str(e)}",
        )


def update_table(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateTableParams,
) -> TableResponse:
    """
    Update an existing table in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the table.

    Returns:
        Response with table update result.
    """
    # First, get the table sys_id
    get_url = f"{config.api_url}/table/sys_db_object"
    get_params = {"sysparm_query": f"name={params.table_name}"}

    try:
        get_response = requests.get(
            get_url,
            params=get_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        get_response.raise_for_status()
        tables = get_response.json().get("result", [])
        
        if not tables:
            return TableResponse(
                success=False,
                message=f"Table '{params.table_name}' not found",
            )

        table_sys_id = tables[0]["sys_id"]
        api_url = f"{config.api_url}/table/sys_db_object/{table_sys_id}"

        # Build request data with only provided fields
        data = {}
        
        if params.label is not None:
            data["label"] = params.label
        if params.is_extendable is not None:
            data["is_extendable"] = params.is_extendable
        if params.access is not None:
            data["access"] = params.access
        if params.user_role is not None:
            data["user_role"] = params.user_role
        if params.audit is not None:
            data["audit"] = params.audit

        # Make request
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return TableResponse(
            success=True,
            message="Table updated successfully",
            table_name=result.get("name", ""),
            sys_id=result.get("sys_id", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update table: {e}")
        return TableResponse(
            success=False,
            message=f"Failed to update table: {str(e)}",
        )


def update_table_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateTableColumnParams,
) -> TableColumnResponse:
    """
    Update an existing table column in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the table column.

    Returns:
        Response with table column update result.
    """
    # First, get the column sys_id
    get_url = f"{config.api_url}/table/sys_dictionary"
    get_params = {"sysparm_query": f"name={params.table_name}^element={params.column_name}"}

    try:
        get_response = requests.get(
            get_url,
            params=get_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        get_response.raise_for_status()
        columns = get_response.json().get("result", [])
        
        if not columns:
            return TableColumnResponse(
                success=False,
                message=f"Column '{params.column_name}' not found in table '{params.table_name}'",
            )

        column_sys_id = columns[0]["sys_id"]
        api_url = f"{config.api_url}/table/sys_dictionary/{column_sys_id}"

        # Build request data with only provided fields
        data = {}
        
        if params.column_label is not None:
            data["column_label"] = params.column_label
        if params.max_length is not None:
            data["max_length"] = params.max_length
        if params.mandatory is not None:
            data["mandatory"] = params.mandatory
        if params.read_only is not None:
            data["read_only"] = params.read_only
        if params.reference_qualifier is not None:
            data["reference_qual"] = params.reference_qualifier
        if params.default_value is not None:
            data["default_value"] = params.default_value
        if params.help_text is not None:
            data["help"] = params.help_text

        # Make request
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return TableColumnResponse(
            success=True,
            message="Table column updated successfully",
            column_name=result.get("element", ""),
            sys_id=result.get("sys_id", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update table column: {e}")
        return TableColumnResponse(
            success=False,
            message=f"Failed to update table column: {str(e)}",
        )


def list_tables(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListTablesParams,
) -> TableListResponse:
    """
    List tables from ServiceNow with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing tables.

    Returns:
        Response with list of tables.
    """
    api_url = f"{config.api_url}/table/sys_db_object"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build query filters
    filters = []
    
    if params.user_table:
        # Filter to user-created tables (typically start with 'u_')
        filters.append("nameLIKEu_")
    
    if params.scope:
        filters.append(f"sys_scope={params.scope}")
    
    if params.super_class:
        filters.append(f"super_class={params.super_class}")
    
    if params.query:
        # Search in name and label
        filters.append(f"nameLIKE{params.query}^ORlabelLIKE{params.query}")

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

        return TableListResponse(
            success=True,
            message=f"Retrieved {len(result)} tables",
            tables=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list tables: {e}")
        return TableListResponse(
            success=False,
            message=f"Failed to list tables: {str(e)}",
            tables=[],
            total_count=0,
        )


def list_table_columns(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListTableColumnsParams,
) -> TableColumnListResponse:
    """
    List columns from a specific table in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing table columns.

    Returns:
        Response with list of table columns.
    """
    api_url = f"{config.api_url}/table/sys_dictionary"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_query": f"name={params.table_name}",
    }

    if params.active:
        query_params["sysparm_query"] += "^active=true"

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

        return TableColumnListResponse(
            success=True,
            message=f"Retrieved {len(result)} columns for table '{params.table_name}'",
            columns=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list table columns: {e}")
        return TableColumnListResponse(
            success=False,
            message=f"Failed to list table columns: {str(e)}",
            columns=[],
            total_count=0,
        )


def get_table(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetTableParams,
) -> TableResponse:
    """
    Get details of a specific table from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the table.

    Returns:
        Response with table data.
    """
    api_url = f"{config.api_url}/table/sys_db_object"
    query_params = {"sysparm_query": f"name={params.table_name}"}

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
        
        if not result:
            return TableResponse(
                success=False,
                message=f"Table '{params.table_name}' not found",
            )

        table_data = result[0]

        return TableResponse(
            success=True,
            message="Table retrieved successfully",
            table_name=table_data.get("name", ""),
            sys_id=table_data.get("sys_id", ""),
            data=table_data,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get table: {e}")
        return TableResponse(
            success=False,
            message=f"Failed to get table: {str(e)}",
        )


def get_table_column(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetTableColumnParams,
) -> TableColumnResponse:
    """
    Get details of a specific table column from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the table column.

    Returns:
        Response with table column data.
    """
    api_url = f"{config.api_url}/table/sys_dictionary"
    query_params = {"sysparm_query": f"name={params.table_name}^element={params.column_name}"}

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
        
        if not result:
            return TableColumnResponse(
                success=False,
                message=f"Column '{params.column_name}' not found in table '{params.table_name}'",
            )

        column_data = result[0]

        return TableColumnResponse(
            success=True,
            message="Table column retrieved successfully",
            column_name=column_data.get("element", ""),
            sys_id=column_data.get("sys_id", ""),
            data=column_data,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get table column: {e}")
        return TableColumnResponse(
            success=False,
            message=f"Failed to get table column: {str(e)}",
        )