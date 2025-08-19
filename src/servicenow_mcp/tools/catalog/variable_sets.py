"""
Variable Sets Management tools for the ServiceNow MCP server.

This module provides tools for managing Variable Sets that are stored in the item_option_new_set table.
A Variable Set is a reusable collection of Catalog Variables that you can group together and then 
attach to one or more catalog items or record producers.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


# Create Variable Set
class CreateVariableSetParams(BaseModel):
    """Parameters for creating a variable set."""

    title: str = Field(..., description="Title of the variable set")
    internal_name: str = Field(..., description="Internal name of the variable set")
    description: Optional[str] = Field(None, description="Description of the variable set")
    order: Optional[int] = Field(100, description="Display order of the variable set")
    display_title: Optional[bool] = Field(False, description="Whether to display the title")
    layout: Optional[str] = Field("normal", description="Layout of the variable set")
    read_roles: Optional[List[str]] = Field(None, description="Roles required to read the variable set")
    write_roles: Optional[List[str]] = Field(None, description="Roles required to write the variable set")
    create_roles: Optional[List[str]] = Field(None, description="Roles required to create the variable set")
    set_attributes: Optional[str] = Field(None, description="Variable set attributes")


class CreateVariableSetResponse(BaseModel):
    """Response from create variable set operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_set_id: Optional[str] = Field(None, description="System ID of the created variable set")
    variable_set_data: Optional[Dict[str, Any]] = Field(None, description="Details of the created variable set")


def create_variable_set(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateVariableSetParams,
) -> CreateVariableSetResponse:
    """
    Create a new variable set in the item_option_new_set table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the variable set.

    Returns:
        Response with creation result and variable set details.
    """
    api_url = f"{config.api_url}/table/item_option_new_set"

    # Build request data
    data = {
        "title": params.title,
        "internal_name": params.internal_name,
        "type": "one_to_one",  # Default type for variable sets
    }

    # Add optional fields
    if params.description:
        data["description"] = params.description
    if params.order is not None:
        data["order"] = params.order
    if params.display_title is not None:
        data["display_title"] = params.display_title
    if params.layout:
        data["layout"] = params.layout
    if params.read_roles:
        data["read_roles"] = ",".join(params.read_roles)
    if params.write_roles:
        data["write_roles"] = ",".join(params.write_roles)
    if params.create_roles:
        data["create_roles"] = ",".join(params.create_roles)
    if params.set_attributes:
        data["set_attributes"] = params.set_attributes

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return CreateVariableSetResponse(
            success=True,
            message="Variable set created successfully",
            variable_set_id=result.get("sys_id"),
            variable_set_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create variable set: {e}")
        return CreateVariableSetResponse(
            success=False,
            message=f"Failed to create variable set: {str(e)}",
        )


# List Variable Sets
class ListVariableSetsParams(BaseModel):
    """Parameters for listing variable sets."""

    title_contains: Optional[str] = Field(None, description="Filter by title containing text")
    internal_name_contains: Optional[str] = Field(None, description="Filter by internal name containing text")
    include_details: Optional[bool] = Field(True, description="Whether to include detailed information about each variable set")
    limit: Optional[int] = Field(50, description="Maximum number of variable sets to return")
    offset: Optional[int] = Field(0, description="Offset for pagination")


class ListVariableSetsResponse(BaseModel):
    """Response from list variable sets operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_sets: List[Dict[str, Any]] = Field(default=[], description="List of variable sets")
    total_count: Optional[int] = Field(None, description="Total number of variable sets")


def list_variable_sets(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListVariableSetsParams,
) -> ListVariableSetsResponse:
    """
    List variable sets from the item_option_new_set table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing variable sets.

    Returns:
        Response with list of variable sets.
    """
    api_url = f"{config.api_url}/table/item_option_new_set"
    
    # Build query parameters
    query_params = {
        "sysparm_limit": str(params.limit),
        "sysparm_offset": str(params.offset),
        "sysparm_display_value": "true" if params.include_details else "false",
    }
    
    # Build query filter
    query_parts = []
    if params.title_contains:
        query_parts.append(f"titleLIKE{params.title_contains}")
    if params.internal_name_contains:
        query_parts.append(f"internal_nameLIKE{params.internal_name_contains}")

    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return ListVariableSetsResponse(
            success=True,
            message=f"Retrieved {len(result)} variable sets",
            variable_sets=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list variable sets: {e}")
        return ListVariableSetsResponse(
            success=False,
            message=f"Failed to list variable sets: {str(e)}",
        )


# Update Variable Set
class UpdateVariableSetParams(BaseModel):
    """Parameters for updating a variable set."""

    variable_set_id: str = Field(..., description="The sys_id of the variable set to update")
    title: Optional[str] = Field(None, description="Title of the variable set")
    internal_name: Optional[str] = Field(None, description="Internal name of the variable set")
    description: Optional[str] = Field(None, description="Description of the variable set")
    order: Optional[int] = Field(None, description="Display order of the variable set")
    display_title: Optional[bool] = Field(None, description="Whether to display the title")
    layout: Optional[str] = Field(None, description="Layout of the variable set")
    read_roles: Optional[List[str]] = Field(None, description="Roles required to read the variable set")
    write_roles: Optional[List[str]] = Field(None, description="Roles required to write the variable set")
    create_roles: Optional[List[str]] = Field(None, description="Roles required to create the variable set")
    set_attributes: Optional[str] = Field(None, description="Variable set attributes")


class UpdateVariableSetResponse(BaseModel):
    """Response from update variable set operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_set_data: Optional[Dict[str, Any]] = Field(None, description="Updated variable set details")


def update_variable_set(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateVariableSetParams,
) -> UpdateVariableSetResponse:
    """
    Update an existing variable set in the item_option_new_set table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the variable set.

    Returns:
        Response with update result and variable set details.
    """
    api_url = f"{config.api_url}/table/item_option_new_set/{params.variable_set_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.title is not None:
        data["title"] = params.title
    if params.internal_name is not None:
        data["internal_name"] = params.internal_name
    if params.description is not None:
        data["description"] = params.description
    if params.order is not None:
        data["order"] = params.order
    if params.display_title is not None:
        data["display_title"] = params.display_title
    if params.layout is not None:
        data["layout"] = params.layout
    if params.read_roles is not None:
        data["read_roles"] = ",".join(params.read_roles)
    if params.write_roles is not None:
        data["write_roles"] = ",".join(params.write_roles)
    if params.create_roles is not None:
        data["create_roles"] = ",".join(params.create_roles)
    if params.set_attributes is not None:
        data["set_attributes"] = params.set_attributes

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return UpdateVariableSetResponse(
            success=True,
            message="Variable set updated successfully",
            variable_set_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update variable set: {e}")
        return UpdateVariableSetResponse(
            success=False,
            message=f"Failed to update variable set: {str(e)}",
        )


# Delete Variable Set
class DeleteVariableSetParams(BaseModel):
    """Parameters for deleting a variable set."""

    variable_set_id: str = Field(..., description="The sys_id of the variable set to delete")


class DeleteVariableSetResponse(BaseModel):
    """Response from delete variable set operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")


def delete_variable_set(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteVariableSetParams,
) -> DeleteVariableSetResponse:
    """
    Delete a variable set from the item_option_new_set table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the variable set.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/item_option_new_set/{params.variable_set_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return DeleteVariableSetResponse(
            success=True,
            message="Variable set deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete variable set: {e}")
        return DeleteVariableSetResponse(
            success=False,
            message=f"Failed to delete variable set: {str(e)}",
        )


# Get Variable Set Details
class GetVariableSetParams(BaseModel):
    """Parameters for getting a variable set."""

    variable_set_id: str = Field(..., description="The sys_id of the variable set to retrieve")


class GetVariableSetResponse(BaseModel):
    """Response from get variable set operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_set_data: Optional[Dict[str, Any]] = Field(None, description="Variable set details")


def get_variable_set(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetVariableSetParams,
) -> GetVariableSetResponse:
    """
    Get detailed information about a specific variable set.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the variable set.

    Returns:
        Response with variable set details.
    """
    api_url = f"{config.api_url}/table/item_option_new_set/{params.variable_set_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return GetVariableSetResponse(
            success=True,
            message="Variable set retrieved successfully",
            variable_set_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get variable set: {e}")
        return GetVariableSetResponse(
            success=False,
            message=f"Failed to get variable set: {str(e)}",
        )