"""
User Role Management tools for the ServiceNow MCP server.

This module provides tools for managing user-role associations in ServiceNow
using the sys_user_has_role table.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class AssignUserRoleParams(BaseModel):
    """Parameters for assigning a role to a user."""

    user_id: str = Field(..., description="User ID or sys_id to assign role to")
    role_id: str = Field(..., description="Role ID or sys_id to assign")
    granted_by: Optional[str] = Field(None, description="User who granted the role (sys_id)")


class RemoveUserRoleParams(BaseModel):
    """Parameters for removing a role from a user."""

    user_id: str = Field(..., description="User ID or sys_id to remove role from")
    role_id: str = Field(..., description="Role ID or sys_id to remove")


class ListUserRolesParams(BaseModel):
    """Parameters for listing user roles."""

    user_id: Optional[str] = Field(None, description="User ID or sys_id to filter by")
    role_id: Optional[str] = Field(None, description="Role ID or sys_id to filter by")
    limit: int = Field(10, description="Maximum number of records to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class BulkAssignRolesParams(BaseModel):
    """Parameters for bulk assigning roles to users."""

    assignments: List[Dict[str, str]] = Field(
        ..., 
        description="List of user-role assignments, each with 'user_id' and 'role_id'"
    )
    granted_by: Optional[str] = Field(None, description="User who granted the roles (sys_id)")


class BulkRemoveRolesParams(BaseModel):
    """Parameters for bulk removing roles from users."""

    removals: List[Dict[str, str]] = Field(
        ..., 
        description="List of user-role removals, each with 'user_id' and 'role_id'"
    )


class UserRoleResponse(BaseModel):
    """Response from user role operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    sys_id: Optional[str] = Field(None, description="System ID of the created/modified record")


class UserRoleListResponse(BaseModel):
    """Response from listing user roles."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    roles: List[Dict[str, Any]] = Field(default_factory=list, description="List of user role assignments")
    total_count: Optional[int] = Field(None, description="Total number of records available")


class BulkUserRoleResponse(BaseModel):
    """Response from bulk user role operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    successful_operations: int = Field(0, description="Number of successful operations")
    failed_operations: int = Field(0, description="Number of failed operations")
    errors: List[str] = Field(default_factory=list, description="List of error messages")


def assign_user_role(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: AssignUserRoleParams,
) -> UserRoleResponse:
    """
    Assign a role to a user by creating a record in sys_user_has_role table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for assigning user role.

    Returns:
        Response with assignment result.
    """
    api_url = f"{config.api_url}/table/sys_user_has_role"

    # Build request data
    data = {
        "user": params.user_id,
        "role": params.role_id,
    }

    if params.granted_by:
        data["granted_by"] = params.granted_by

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return UserRoleResponse(
            success=True,
            message="Role assigned to user successfully",
            sys_id=result.get("sys_id"),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to assign role to user: {e}")
        return UserRoleResponse(
            success=False,
            message=f"Failed to assign role to user: {str(e)}",
        )


def remove_user_role(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: RemoveUserRoleParams,
) -> UserRoleResponse:
    """
    Remove a role from a user by deleting the record from sys_user_has_role table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for removing user role.

    Returns:
        Response with removal result.
    """
    # First, find the sys_user_has_role record
    search_url = f"{config.api_url}/table/sys_user_has_role"
    search_params = {
        "sysparm_query": f"user={params.user_id}^role={params.role_id}",
        "sysparm_limit": 1,
    }

    try:
        # Find the record
        search_response = requests.get(
            search_url,
            params=search_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        search_response.raise_for_status()

        search_result = search_response.json().get("result", [])
        
        if not search_result:
            return UserRoleResponse(
                success=False,
                message="User role assignment not found",
            )

        # Delete the record
        record_sys_id = search_result[0]["sys_id"]
        delete_url = f"{config.api_url}/table/sys_user_has_role/{record_sys_id}"

        delete_response = requests.delete(
            delete_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        delete_response.raise_for_status()

        return UserRoleResponse(
            success=True,
            message="Role removed from user successfully",
            sys_id=record_sys_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to remove role from user: {e}")
        return UserRoleResponse(
            success=False,
            message=f"Failed to remove role from user: {str(e)}",
        )


def list_user_roles(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListUserRolesParams,
) -> UserRoleListResponse:
    """
    List user role assignments from sys_user_has_role table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing user roles.

    Returns:
        Response with list of user role assignments.
    """
    api_url = f"{config.api_url}/table/sys_user_has_role"

    # Build query parameters
    query_parts = []
    if params.user_id:
        query_parts.append(f"user={params.user_id}")
    if params.role_id:
        query_parts.append(f"role={params.role_id}")
    if params.query:
        query_parts.append(params.query)

    request_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "all",
        "sysparm_exclude_reference_link": "true",
    }

    if query_parts:
        request_params["sysparm_query"] = "^".join(query_parts)

    try:
        response = requests.get(
            api_url,
            params=request_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        # Get total count from headers if available
        total_count = None
        if "X-Total-Count" in response.headers:
            total_count = int(response.headers["X-Total-Count"])

        return UserRoleListResponse(
            success=True,
            message=f"Retrieved {len(result)} user role assignments",
            roles=result,
            total_count=total_count,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list user roles: {e}")
        return UserRoleListResponse(
            success=False,
            message=f"Failed to list user roles: {str(e)}",
        )


def bulk_assign_user_roles(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkAssignRolesParams,
) -> BulkUserRoleResponse:
    """
    Bulk assign roles to users by creating multiple records in sys_user_has_role table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for bulk assigning user roles.

    Returns:
        Response with bulk assignment results.
    """
    api_url = f"{config.api_url}/table/sys_user_has_role"
    
    successful_operations = 0
    failed_operations = 0
    errors = []

    for assignment in params.assignments:
        try:
            data = {
                "user": assignment["user_id"],
                "role": assignment["role_id"],
            }

            if params.granted_by:
                data["granted_by"] = params.granted_by

            response = requests.post(
                api_url,
                json=data,
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            response.raise_for_status()
            successful_operations += 1

        except requests.RequestException as e:
            failed_operations += 1
            error_msg = f"Failed to assign role {assignment['role_id']} to user {assignment['user_id']}: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)

    success = failed_operations == 0

    return BulkUserRoleResponse(
        success=success,
        message=f"Bulk assignment completed: {successful_operations} successful, {failed_operations} failed",
        successful_operations=successful_operations,
        failed_operations=failed_operations,
        errors=errors,
    )


def bulk_remove_user_roles(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkRemoveRolesParams,
) -> BulkUserRoleResponse:
    """
    Bulk remove roles from users by deleting multiple records from sys_user_has_role table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for bulk removing user roles.

    Returns:
        Response with bulk removal results.
    """
    successful_operations = 0
    failed_operations = 0
    errors = []

    for removal in params.removals:
        try:
            # Find the sys_user_has_role record
            search_url = f"{config.api_url}/table/sys_user_has_role"
            search_params = {
                "sysparm_query": f"user={removal['user_id']}^role={removal['role_id']}",
                "sysparm_limit": 1,
            }

            search_response = requests.get(
                search_url,
                params=search_params,
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            search_response.raise_for_status()

            search_result = search_response.json().get("result", [])
            
            if not search_result:
                failed_operations += 1
                error_msg = f"User role assignment not found for user {removal['user_id']} and role {removal['role_id']}"
                errors.append(error_msg)
                continue

            # Delete the record
            record_sys_id = search_result[0]["sys_id"]
            delete_url = f"{config.api_url}/table/sys_user_has_role/{record_sys_id}"

            delete_response = requests.delete(
                delete_url,
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            delete_response.raise_for_status()
            successful_operations += 1

        except requests.RequestException as e:
            failed_operations += 1
            error_msg = f"Failed to remove role {removal['role_id']} from user {removal['user_id']}: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)

    success = failed_operations == 0

    return BulkUserRoleResponse(
        success=success,
        message=f"Bulk removal completed: {successful_operations} successful, {failed_operations} failed",
        successful_operations=successful_operations,
        failed_operations=failed_operations,
        errors=errors,
    )