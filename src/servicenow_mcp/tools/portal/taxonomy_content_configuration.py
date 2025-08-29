"""
Taxonomy Content Configuration tools for the ServiceNow MCP server.

This module provides tools for managing records stored in the taxonomy_content_configuration table.
In ServiceNow, this table manages the options to be selected in Connected Content records' "Content Type" field.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateTaxonomyContentConfigParams(BaseModel):
    """Parameters for creating a taxonomy content configuration."""

    name: str = Field(..., description="Name of the content configuration")
    active: Optional[bool] = Field(True, description="Whether the configuration is active")
    description: Optional[str] = Field(None, description="Description of the content configuration")
    table_name: Optional[str] = Field(None, description="Table name associated with this content type")
    display_name: Optional[str] = Field(None, description="Display name for the content type")
    order: Optional[int] = Field(None, description="Display order")


class UpdateTaxonomyContentConfigParams(BaseModel):
    """Parameters for updating a taxonomy content configuration."""

    config_id: str = Field(..., description="Taxonomy content configuration sys_id")
    name: Optional[str] = Field(None, description="Updated name of the content configuration")
    active: Optional[bool] = Field(None, description="Updated active status")
    description: Optional[str] = Field(None, description="Updated description")
    table_name: Optional[str] = Field(None, description="Updated table name")
    display_name: Optional[str] = Field(None, description="Updated display name")
    order: Optional[int] = Field(None, description="Updated display order")


class ListTaxonomyContentConfigParams(BaseModel):
    """Parameters for listing taxonomy content configurations."""

    active: Optional[bool] = Field(None, description="Filter by active status")
    table_name: Optional[str] = Field(None, description="Filter by table name")
    limit: int = Field(10, description="Maximum number of configurations to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetTaxonomyContentConfigParams(BaseModel):
    """Parameters for getting a specific taxonomy content configuration."""

    config_id: str = Field(..., description="Taxonomy content configuration sys_id or name")


class DeleteTaxonomyContentConfigParams(BaseModel):
    """Parameters for deleting a taxonomy content configuration."""

    config_id: str = Field(..., description="Taxonomy content configuration sys_id")


class TaxonomyContentConfigResponse(BaseModel):
    """Response from taxonomy content configuration operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Configuration data")


class TaxonomyContentConfigListResponse(BaseModel):
    """Response from list taxonomy content configuration operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    configurations: List[Dict[str, Any]] = Field(default_factory=list, description="List of configurations")
    total: int = Field(0, description="Total number of configurations")
    limit: int = Field(0, description="Limit used")
    offset: int = Field(0, description="Offset used")


def create_taxonomy_content_configuration(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateTaxonomyContentConfigParams,
) -> TaxonomyContentConfigResponse:
    """
    Create a new taxonomy content configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the taxonomy content configuration.

    Returns:
        Response with creation result.
    """
    api_url = f"{config.api_url}/table/taxonomy_content_configuration"

    # Build request data
    data = {
        "name": params.name,
        "active": str(params.active).lower(),
    }

    if params.description:
        data["description"] = params.description
    if params.table_name:
        data["table_name"] = params.table_name
    if params.display_name:
        data["display_name"] = params.display_name
    if params.order is not None:
        data["order"] = str(params.order)

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return TaxonomyContentConfigResponse(
            success=True,
            message=f"Created taxonomy content configuration: {result.get('sys_id', 'unknown')}",
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create taxonomy content configuration: {e}")
        return TaxonomyContentConfigResponse(
            success=False,
            message=f"Failed to create taxonomy content configuration: {str(e)}",
        )


def update_taxonomy_content_configuration(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateTaxonomyContentConfigParams,
) -> TaxonomyContentConfigResponse:
    """
    Update an existing taxonomy content configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the taxonomy content configuration.

    Returns:
        Response with update result.
    """
    api_url = f"{config.api_url}/table/taxonomy_content_configuration/{params.config_id}"

    # Build request data
    data = {}

    if params.name is not None:
        data["name"] = params.name
    if params.active is not None:
        data["active"] = str(params.active).lower()
    if params.description is not None:
        data["description"] = params.description
    if params.table_name is not None:
        data["table_name"] = params.table_name
    if params.display_name is not None:
        data["display_name"] = params.display_name
    if params.order is not None:
        data["order"] = str(params.order)

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return TaxonomyContentConfigResponse(
            success=True,
            message=f"Updated taxonomy content configuration: {params.config_id}",
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update taxonomy content configuration: {e}")
        return TaxonomyContentConfigResponse(
            success=False,
            message=f"Failed to update taxonomy content configuration: {str(e)}",
        )


def list_taxonomy_content_configurations(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListTaxonomyContentConfigParams,
) -> TaxonomyContentConfigListResponse:
    """
    List taxonomy content configurations with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing configurations.

    Returns:
        Response with list of configurations.
    """
    api_url = f"{config.api_url}/table/taxonomy_content_configuration"

    # Build query parameters
    query_params = {
        "sysparm_limit": str(params.limit),
        "sysparm_offset": str(params.offset),
    }

    # Build query conditions
    query_conditions = []

    if params.active is not None:
        query_conditions.append(f"active={str(params.active).lower()}")
    if params.table_name:
        query_conditions.append(f"table_name={params.table_name}")
    if params.query:
        query_conditions.append(params.query)

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
        total_count = len(result)

        return TaxonomyContentConfigListResponse(
            success=True,
            message=f"Retrieved {total_count} taxonomy content configurations",
            configurations=result,
            total=total_count,
            limit=params.limit,
            offset=params.offset,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list taxonomy content configurations: {e}")
        return TaxonomyContentConfigListResponse(
            success=False,
            message=f"Failed to list taxonomy content configurations: {str(e)}",
        )


def get_taxonomy_content_configuration(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetTaxonomyContentConfigParams,
) -> TaxonomyContentConfigResponse:
    """
    Get a specific taxonomy content configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the configuration.

    Returns:
        Response with configuration data.
    """
    api_url = f"{config.api_url}/table/taxonomy_content_configuration/{params.config_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return TaxonomyContentConfigResponse(
            success=True,
            message=f"Retrieved taxonomy content configuration: {params.config_id}",
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get taxonomy content configuration: {e}")
        return TaxonomyContentConfigResponse(
            success=False,
            message=f"Failed to get taxonomy content configuration: {str(e)}",
        )


def delete_taxonomy_content_configuration(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteTaxonomyContentConfigParams,
) -> TaxonomyContentConfigResponse:
    """
    Delete a taxonomy content configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the configuration.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/taxonomy_content_configuration/{params.config_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return TaxonomyContentConfigResponse(
            success=True,
            message=f"Deleted taxonomy content configuration: {params.config_id}",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete taxonomy content configuration: {e}")
        return TaxonomyContentConfigResponse(
            success=False,
            message=f"Failed to delete taxonomy content configuration: {str(e)}",
        )