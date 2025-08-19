"""
Catalog Variable Management tools for the ServiceNow MCP server.

This module provides tools for managing catalog variables in the item_option_new table,
including creating, updating, listing, and deleting catalog variables for catalog items.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


# Create Catalog Variable
class CreateCatalogVariableParams(BaseModel):
    """Parameters for creating a catalog variable."""

    catalog_item_id: str = Field(..., description="The sys_id of the catalog item")
    name: str = Field(..., description="The name of the variable (internal name)")
    type: str = Field(..., description="The type of variable (e.g., string, integer, boolean, reference)")
    label: str = Field(..., description="The display label for the variable")
    mandatory: Optional[bool] = Field(False, description="Whether the variable is required")
    max_length: Optional[int] = Field(None, description="Maximum length for string fields")
    min: Optional[int] = Field(None, description="Minimum value for numeric fields")
    max: Optional[int] = Field(None, description="Maximum value for numeric fields")
    default_value: Optional[str] = Field(None, description="Default value for the variable")
    description: Optional[str] = Field(None, description="Description of the variable")
    help_text: Optional[str] = Field(None, description="Help text to display with the variable")
    order: Optional[int] = Field(None, description="Display order of the variable")
    reference_table: Optional[str] = Field(None, description="For reference fields, the table to reference")
    reference_qualifier: Optional[str] = Field(None, description="For reference fields, the query to filter reference options")
    field: Optional[str] = Field(None, description="Field name for the variable")
    map_to_field: Optional[str] = Field(None, description="Target field to map this variable to")
    choice_field: Optional[str] = Field(None, description="Choice field for dependent choices")
    choice_table: Optional[str] = Field(None, description="Choice table for choice fields")
    show_help: Optional[bool] = Field(None, description="Whether to show help icon for the variable")
    show_help_on_load: Optional[bool] = Field(None, description="Whether to show help expanded when form loads")


class CreateCatalogVariableResponse(BaseModel):
    """Response from create catalog variable operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_id: Optional[str] = Field(None, description="System ID of the created variable")
    variable_data: Optional[Dict[str, Any]] = Field(None, description="Details of the created variable")


def create_catalog_variable(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateCatalogVariableParams,
) -> CreateCatalogVariableResponse:
    """
    Create a new catalog variable in the item_option_new table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the catalog variable.

    Returns:
        Response with creation result and variable details.
    """
    api_url = f"{config.api_url}/table/item_option_new"

    # Build request data
    data = {
        "cat_item": params.catalog_item_id,
        "name": params.name,
        "type": params.type,
        "question_text": params.label,
        "mandatory": params.mandatory,
    }

    # Add optional fields
    if params.max_length:
        data["max_length"] = params.max_length
    if params.min is not None:
        data["min"] = params.min
    if params.max is not None:
        data["max"] = params.max
    if params.default_value:
        data["default_value"] = params.default_value
    if params.description:
        data["description"] = params.description
    if params.help_text:
        data["help_text"] = params.help_text
    if params.order is not None:
        data["order"] = params.order
    if params.reference_table:
        data["reference"] = params.reference_table
    if params.reference_qualifier:
        data["reference_qual"] = params.reference_qualifier
    if params.field:
        data["field"] = params.field
    if params.map_to_field:
        data["map_to_field"] = params.map_to_field
    if params.choice_field:
        data["choice_field"] = params.choice_field
    if params.choice_table:
        data["choice_table"] = params.choice_table
    if params.show_help is not None:
        data["show_help"] = params.show_help
    if params.show_help_on_load is not None:
        data["show_help_on_load"] = params.show_help_on_load

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return CreateCatalogVariableResponse(
            success=True,
            message="Catalog variable created successfully",
            variable_id=result.get("sys_id"),
            variable_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create catalog variable: {e}")
        return CreateCatalogVariableResponse(
            success=False,
            message=f"Failed to create catalog variable: {str(e)}",
        )


# List Catalog Variables
class ListCatalogVariablesParams(BaseModel):
    """Parameters for listing catalog variables."""

    catalog_item_id: str = Field(..., description="The sys_id of the catalog item")
    include_details: Optional[bool] = Field(True, description="Whether to include detailed information about each variable")
    limit: Optional[int] = Field(None, description="Maximum number of variables to return")
    offset: Optional[int] = Field(None, description="Offset for pagination")


class ListCatalogVariablesResponse(BaseModel):
    """Response from list catalog variables operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variables: List[Dict[str, Any]] = Field(default=[], description="List of catalog variables")
    total_count: Optional[int] = Field(None, description="Total number of variables")


def list_catalog_variables(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListCatalogVariablesParams,
) -> ListCatalogVariablesResponse:
    """
    List catalog variables for a specific catalog item.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing catalog variables.

    Returns:
        Response with list of catalog variables.
    """
    api_url = f"{config.api_url}/table/item_option_new"
    
    # Build query parameters
    query_params = {
        "sysparm_query": f"cat_item={params.catalog_item_id}",
        "sysparm_display_value": "true" if params.include_details else "false",
    }
    
    if params.limit:
        query_params["sysparm_limit"] = str(params.limit)
    if params.offset:
        query_params["sysparm_offset"] = str(params.offset)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return ListCatalogVariablesResponse(
            success=True,
            message=f"Retrieved {len(result)} catalog variables",
            variables=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list catalog variables: {e}")
        return ListCatalogVariablesResponse(
            success=False,
            message=f"Failed to list catalog variables: {str(e)}",
        )


# Update Catalog Variable
class UpdateCatalogVariableParams(BaseModel):
    """Parameters for updating a catalog variable."""

    variable_id: str = Field(..., description="The sys_id of the variable to update")
    name: Optional[str] = Field(None, description="The name of the variable (internal name)")
    type: Optional[str] = Field(None, description="The type of variable")
    label: Optional[str] = Field(None, description="The display label for the variable")
    mandatory: Optional[bool] = Field(None, description="Whether the variable is required")
    max_length: Optional[int] = Field(None, description="Maximum length for string fields")
    min: Optional[int] = Field(None, description="Minimum value for numeric fields")
    max: Optional[int] = Field(None, description="Maximum value for numeric fields")
    default_value: Optional[str] = Field(None, description="Default value for the variable")
    description: Optional[str] = Field(None, description="Description of the variable")
    help_text: Optional[str] = Field(None, description="Help text to display with the variable")
    order: Optional[int] = Field(None, description="Display order of the variable")
    reference_table: Optional[str] = Field(None, description="For reference fields, the table to reference")
    reference_qualifier: Optional[str] = Field(None, description="For reference fields, the query to filter reference options")
    field: Optional[str] = Field(None, description="Field name for the variable")
    map_to_field: Optional[str] = Field(None, description="Target field to map this variable to")
    choice_field: Optional[str] = Field(None, description="Choice field for dependent choices")
    choice_table: Optional[str] = Field(None, description="Choice table for choice fields")
    show_help: Optional[bool] = Field(None, description="Whether to show help icon for the variable")
    show_help_on_load: Optional[bool] = Field(None, description="Whether to show help expanded when form loads")


class UpdateCatalogVariableResponse(BaseModel):
    """Response from update catalog variable operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_data: Optional[Dict[str, Any]] = Field(None, description="Updated variable details")


def update_catalog_variable(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateCatalogVariableParams,
) -> UpdateCatalogVariableResponse:
    """
    Update an existing catalog variable in the item_option_new table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the catalog variable.

    Returns:
        Response with update result and variable details.
    """
    api_url = f"{config.api_url}/table/item_option_new/{params.variable_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.type is not None:
        data["type"] = params.type
    if params.label is not None:
        data["question_text"] = params.label
    if params.mandatory is not None:
        data["mandatory"] = params.mandatory
    if params.max_length is not None:
        data["max_length"] = params.max_length
    if params.min is not None:
        data["min"] = params.min
    if params.max is not None:
        data["max"] = params.max
    if params.default_value is not None:
        data["default_value"] = params.default_value
    if params.description is not None:
        data["description"] = params.description
    if params.help_text is not None:
        data["help_text"] = params.help_text
    if params.order is not None:
        data["order"] = params.order
    if params.reference_table is not None:
        data["reference"] = params.reference_table
    if params.reference_qualifier is not None:
        data["reference_qual"] = params.reference_qualifier
    if params.field is not None:
        data["field"] = params.field
    if params.map_to_field is not None:
        data["map_to_field"] = params.map_to_field
    if params.choice_field is not None:
        data["choice_field"] = params.choice_field
    if params.choice_table is not None:
        data["choice_table"] = params.choice_table
    if params.show_help is not None:
        data["show_help"] = params.show_help
    if params.show_help_on_load is not None:
        data["show_help_on_load"] = params.show_help_on_load

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return UpdateCatalogVariableResponse(
            success=True,
            message="Catalog variable updated successfully",
            variable_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update catalog variable: {e}")
        return UpdateCatalogVariableResponse(
            success=False,
            message=f"Failed to update catalog variable: {str(e)}",
        )


# Delete Catalog Variable
class DeleteCatalogVariableParams(BaseModel):
    """Parameters for deleting a catalog variable."""

    variable_id: str = Field(..., description="The sys_id of the variable to delete")


class DeleteCatalogVariableResponse(BaseModel):
    """Response from delete catalog variable operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")


def delete_catalog_variable(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteCatalogVariableParams,
) -> DeleteCatalogVariableResponse:
    """
    Delete a catalog variable from the item_option_new table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the catalog variable.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/item_option_new/{params.variable_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return DeleteCatalogVariableResponse(
            success=True,
            message="Catalog variable deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete catalog variable: {e}")
        return DeleteCatalogVariableResponse(
            success=False,
            message=f"Failed to delete catalog variable: {str(e)}",
        )


# Get Catalog Variable Details
class GetCatalogVariableParams(BaseModel):
    """Parameters for getting a catalog variable."""

    variable_id: str = Field(..., description="The sys_id of the variable to retrieve")


class GetCatalogVariableResponse(BaseModel):
    """Response from get catalog variable operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    variable_data: Optional[Dict[str, Any]] = Field(None, description="Variable details")


def get_catalog_variable(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetCatalogVariableParams,
) -> GetCatalogVariableResponse:
    """
    Get detailed information about a specific catalog variable.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the catalog variable.

    Returns:
        Response with variable details.
    """
    api_url = f"{config.api_url}/table/item_option_new/{params.variable_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return GetCatalogVariableResponse(
            success=True,
            message="Catalog variable retrieved successfully",
            variable_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get catalog variable: {e}")
        return GetCatalogVariableResponse(
            success=False,
            message=f"Failed to get catalog variable: {str(e)}",
        )