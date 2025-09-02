"""
ACL tools for the ServiceNow MCP server.

This module provides tools for generating and managing ACLs including addition 
and modification of existing ACLs.
"""

import logging
from typing import Optional, List, Dict, Any

import requests

from servicenow_mcp.auth.session_manager import get_session
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateACLParams(BaseModel):
    """Parameters for creating an ACL."""

    name: str = Field(..., description="Name of the ACL")
    table: str = Field(..., description="Table the ACL applies to")
    operation: str = Field("read", description="Operation type (read, write, create, delete)")
    type: str = Field("record", description="ACL type (record, field)")
    field: Optional[str] = Field(None, description="Field name for field-level ACLs")
    script: Optional[str] = Field(None, description="Script content for the ACL")
    condition: Optional[str] = Field(None, description="Condition for the ACL")
    roles: Optional[str] = Field(None, description="Comma-separated list of roles")
    active: bool = Field(True, description="Whether the ACL is active")
    admin_overrides: bool = Field(True, description="Whether admin role overrides this ACL")
    advanced: bool = Field(False, description="Whether this is an advanced ACL")
    description: Optional[str] = Field(None, description="Description of the ACL")


class UpdateACLParams(BaseModel):
    """Parameters for updating an ACL."""

    acl_id: str = Field(..., description="ACL ID or sys_id")
    name: Optional[str] = Field(None, description="Name of the ACL")
    table: Optional[str] = Field(None, description="Table the ACL applies to")
    operation: Optional[str] = Field(None, description="Operation type (read, write, create, delete)")
    type: Optional[str] = Field(None, description="ACL type (record, field)")
    field: Optional[str] = Field(None, description="Field name for field-level ACLs")
    script: Optional[str] = Field(None, description="Script content for the ACL")
    condition: Optional[str] = Field(None, description="Condition for the ACL")
    roles: Optional[str] = Field(None, description="Comma-separated list of roles")
    active: Optional[bool] = Field(None, description="Whether the ACL is active")
    admin_overrides: Optional[bool] = Field(None, description="Whether admin role overrides this ACL")
    advanced: Optional[bool] = Field(None, description="Whether this is an advanced ACL")
    description: Optional[str] = Field(None, description="Description of the ACL")


class ListACLsParams(BaseModel):
    """Parameters for listing ACLs."""

    table: Optional[str] = Field(None, description="Filter by table")
    operation: Optional[str] = Field(None, description="Filter by operation")
    type: Optional[str] = Field(None, description="Filter by ACL type")
    active: Optional[bool] = Field(None, description="Filter by active status")
    limit: int = Field(10, description="Maximum number of ACLs to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetACLParams(BaseModel):
    """Parameters for getting a specific ACL."""

    acl_id: str = Field(..., description="ACL ID or sys_id")


class DeleteACLParams(BaseModel):
    """Parameters for deleting an ACL."""

    acl_id: str = Field(..., description="ACL ID or sys_id")


class ACLResponse(BaseModel):
    """Response from ACL operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    acl_id: Optional[str] = Field(None, description="ACL sys_id")
    acl_data: Optional[Dict[str, Any]] = Field(None, description="ACL data")


class ListACLsResponse(BaseModel):
    """Response from list ACLs operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    acls: List[Dict[str, Any]] = Field(default_factory=list, description="List of ACLs")
    total_count: int = Field(0, description="Total number of ACLs")


def create_acl(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateACLParams,
) -> ACLResponse:
    """
    Create a new ACL in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the ACL.

    Returns:
        Response with ACL creation result.
    """
    api_url = f"{config.api_url}/table/sys_security_acl"

    # Build request data
    data = {
        "name": params.name,
        "table": params.table,
        "operation": params.operation,
        "type": params.type,
        "active": params.active,
        "admin_overrides": params.admin_overrides,
        "advanced": params.advanced,
    }

    if params.field:
        data["field"] = params.field
    if params.script:
        data["script"] = params.script
    if params.condition:
        data["condition"] = params.condition
    if params.roles:
        data["roles"] = params.roles
    if params.description:
        data["description"] = params.description

    try:
        
        session = get_session() 
        
        response = session.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )

        logger.info("Received Response from ServiceNow")
        logger.info(response.cookies);
        logger.info(response.headers);
        logger.info("Received Response from ServiceNow COmplete")

        response.raise_for_status()

        result = response.json().get("result", {})

        return ACLResponse(
            success=True,
            message="ACL created successfully",
            acl_id=result.get("sys_id"),
            acl_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create ACL: {e}")
        return ACLResponse(
            success=False,
            message=f"Failed to create ACL: {str(e)}",
        )


def update_acl(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateACLParams,
) -> ACLResponse:
    """
    Update an existing ACL in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the ACL.

    Returns:
        Response with ACL update result.
    """
    api_url = f"{config.api_url}/table/sys_security_acl/{params.acl_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.table is not None:
        data["table"] = params.table
    if params.operation is not None:
        data["operation"] = params.operation
    if params.type is not None:
        data["type"] = params.type
    if params.field is not None:
        data["field"] = params.field
    if params.script is not None:
        data["script"] = params.script
    if params.condition is not None:
        data["condition"] = params.condition
    if params.roles is not None:
        data["roles"] = params.roles
    if params.active is not None:
        data["active"] = params.active
    if params.admin_overrides is not None:
        data["admin_overrides"] = params.admin_overrides
    if params.advanced is not None:
        data["advanced"] = params.advanced
    if params.description is not None:
        data["description"] = params.description

    try:
        session = get_session()
        response = session.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return ACLResponse(
            success=True,
            message="ACL updated successfully",
            acl_id=result.get("sys_id"),
            acl_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update ACL: {e}")
        return ACLResponse(
            success=False,
            message=f"Failed to update ACL: {str(e)}",
        )


def list_acls(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListACLsParams,
) -> ListACLsResponse:
    """
    List ACLs from ServiceNow with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing ACLs.

    Returns:
        Response with list of ACLs.
    """
    api_url = f"{config.api_url}/table/sys_security_acl"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build encoded query
    query_parts = []
    
    if params.table:
        query_parts.append(f"table={params.table}")
    if params.operation:
        query_parts.append(f"operation={params.operation}")
    if params.type:
        query_parts.append(f"type={params.type}")
    if params.active is not None:
        query_parts.append(f"active={params.active}")
    if params.query:
        query_parts.append(params.query)

    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)

    try:
        session = get_session()
        response = session.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return ListACLsResponse(
            success=True,
            message=f"Found {len(result)} ACLs",
            acls=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list ACLs: {e}")
        return ListACLsResponse(
            success=False,
            message=f"Failed to list ACLs: {str(e)}",
        )


def get_acl(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetACLParams,
) -> ACLResponse:
    """
    Get a specific ACL from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the ACL.

    Returns:
        Response with ACL data.
    """
    api_url = f"{config.api_url}/table/sys_security_acl/{params.acl_id}"

    try:
        session = get_session()
        response = session.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return ACLResponse(
            success=True,
            message="ACL retrieved successfully",
            acl_id=result.get("sys_id"),
            acl_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get ACL: {e}")
        return ACLResponse(
            success=False,
            message=f"Failed to get ACL: {str(e)}",
        )


def delete_acl(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteACLParams,
) -> ACLResponse:
    """
    Delete an ACL from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the ACL.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sys_security_acl/{params.acl_id}"

    try:
        session = get_session()
        response = session.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return ACLResponse(
            success=True,
            message="ACL deleted successfully",
            acl_id=params.acl_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete ACL: {e}")
        return ACLResponse(
            success=False,
            message=f"Failed to delete ACL: {str(e)}",
        )