"""
Choice tools for the ServiceNow MCP server.

This module provides tools for managing choices for choice table columns in ServiceNow.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateChoiceParams(BaseModel):
    """Parameters for creating a choice."""

    table: str = Field(..., description="Table name containing the choice field")
    element: str = Field(..., description="Field/element name for the choice")
    label: str = Field(..., description="Display label for the choice option")
    value: str = Field(..., description="Stored value for the choice option")
    sequence: Optional[int] = Field(None, description="Display order sequence (lower numbers appear first)")
    inactive: bool = Field(False, description="Whether the choice is inactive/disabled")
    hint: Optional[str] = Field(None, description="Tooltip hint text for the choice")
    dependent_value: Optional[str] = Field(None, description="Parent choice value for dependent choices")
    language: str = Field("en", description="Language code for the choice (default: en)")


class UpdateChoiceParams(BaseModel):
    """Parameters for updating a choice."""

    choice_id: str = Field(..., description="Choice sys_id to update")
    label: Optional[str] = Field(None, description="Updated display label")
    value: Optional[str] = Field(None, description="Updated stored value")
    sequence: Optional[int] = Field(None, description="Updated display order sequence")
    inactive: Optional[bool] = Field(None, description="Updated inactive status")
    hint: Optional[str] = Field(None, description="Updated tooltip hint text")
    dependent_value: Optional[str] = Field(None, description="Updated parent choice value")


class ListChoicesParams(BaseModel):
    """Parameters for listing choices."""

    table: str = Field(..., description="Table name containing the choice field")
    element: str = Field(..., description="Field/element name for the choices")
    active_only: bool = Field(True, description="Whether to only return active choices")
    include_dependent: bool = Field(True, description="Whether to include dependent choices")
    language: str = Field("en", description="Language code to filter choices")
    limit: int = Field(50, description="Maximum number of choices to return")
    offset: int = Field(0, description="Offset for pagination")


class GetChoiceParams(BaseModel):
    """Parameters for getting a specific choice."""

    choice_id: str = Field(..., description="Choice sys_id to retrieve")


class DeleteChoiceParams(BaseModel):
    """Parameters for deleting a choice."""

    choice_id: str = Field(..., description="Choice sys_id to delete")


class BulkCreateChoicesParams(BaseModel):
    """Parameters for creating multiple choices at once."""

    table: str = Field(..., description="Table name containing the choice field")
    element: str = Field(..., description="Field/element name for the choices")
    choices: List[Dict[str, Any]] = Field(..., description="List of choice definitions")
    language: str = Field("en", description="Language code for the choices (default: en)")


class ReorderChoicesParams(BaseModel):
    """Parameters for reordering choices."""

    table: str = Field(..., description="Table name containing the choice field")
    element: str = Field(..., description="Field/element name for the choices")
    choice_order: List[str] = Field(..., description="List of choice values in desired order")


class ChoiceResponse(BaseModel):
    """Response from choice operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    choice_id: Optional[str] = Field(None, description="sys_id of the choice")
    value: Optional[str] = Field(None, description="Value of the choice")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class ChoiceListResponse(BaseModel):
    """Response from listing choices."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    choices: List[Dict[str, Any]] = Field(default_factory=list, description="List of choices")
    total_count: int = Field(0, description="Total number of choices")


class BulkChoiceResponse(BaseModel):
    """Response from bulk choice operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    created_count: int = Field(0, description="Number of choices created successfully")
    failed_count: int = Field(0, description="Number of choices that failed to create")
    details: List[Dict[str, Any]] = Field(default_factory=list, description="Detailed results for each choice")


def create_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateChoiceParams,
) -> ChoiceResponse:
    """
    Create a new choice for a choice field in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the choice.

    Returns:
        Response with choice creation result.
    """
    api_url = f"{config.api_url}/table/sys_choice"

    # Build request data
    data = {
        "name": params.table,
        "element": params.element,
        "label": params.label,
        "value": params.value,
        "inactive": params.inactive,
        "language": params.language,
    }

    if params.sequence is not None:
        data["sequence"] = params.sequence
    if params.hint:
        data["hint"] = params.hint
    if params.dependent_value:
        data["dependent_value"] = params.dependent_value

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

        return ChoiceResponse(
            success=True,
            message="Choice created successfully",
            choice_id=result.get("sys_id", ""),
            value=result.get("value", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create choice: {e}")
        return ChoiceResponse(
            success=False,
            message=f"Failed to create choice: {str(e)}",
        )


def update_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateChoiceParams,
) -> ChoiceResponse:
    """
    Update an existing choice in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the choice.

    Returns:
        Response with choice update result.
    """
    api_url = f"{config.api_url}/table/sys_choice/{params.choice_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.label is not None:
        data["label"] = params.label
    if params.value is not None:
        data["value"] = params.value
    if params.sequence is not None:
        data["sequence"] = params.sequence
    if params.inactive is not None:
        data["inactive"] = params.inactive
    if params.hint is not None:
        data["hint"] = params.hint
    if params.dependent_value is not None:
        data["dependent_value"] = params.dependent_value

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

        return ChoiceResponse(
            success=True,
            message="Choice updated successfully",
            choice_id=result.get("sys_id", ""),
            value=result.get("value", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update choice: {e}")
        return ChoiceResponse(
            success=False,
            message=f"Failed to update choice: {str(e)}",
        )


def list_choices(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListChoicesParams,
) -> ChoiceListResponse:
    """
    List choices for a specific field from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing choices.

    Returns:
        Response with list of choices.
    """
    api_url = f"{config.api_url}/table/sys_choice"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_orderby": "sequence,label",  # Order by sequence first, then label
    }

    # Build query filters
    filters = [
        f"name={params.table}",
        f"element={params.element}",
        f"language={params.language}",
    ]
    
    if params.active_only:
        filters.append("inactive=false")

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

        return ChoiceListResponse(
            success=True,
            message=f"Retrieved {len(result)} choices for {params.table}.{params.element}",
            choices=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list choices: {e}")
        return ChoiceListResponse(
            success=False,
            message=f"Failed to list choices: {str(e)}",
            choices=[],
            total_count=0,
        )


def get_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetChoiceParams,
) -> ChoiceResponse:
    """
    Get a specific choice from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the choice.

    Returns:
        Response with choice data.
    """
    api_url = f"{config.api_url}/table/sys_choice/{params.choice_id}"

    # Make request
    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return ChoiceResponse(
            success=True,
            message="Choice retrieved successfully",
            choice_id=result.get("sys_id", ""),
            value=result.get("value", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get choice: {e}")
        return ChoiceResponse(
            success=False,
            message=f"Failed to get choice: {str(e)}",
        )


def delete_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteChoiceParams,
) -> ChoiceResponse:
    """
    Delete a choice from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the choice.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sys_choice/{params.choice_id}"

    # Make request
    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return ChoiceResponse(
            success=True,
            message="Choice deleted successfully",
            choice_id=params.choice_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete choice: {e}")
        return ChoiceResponse(
            success=False,
            message=f"Failed to delete choice: {str(e)}",
        )


def bulk_create_choices(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkCreateChoicesParams,
) -> BulkChoiceResponse:
    """
    Create multiple choices at once for a choice field.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for bulk creating choices.

    Returns:
        Response with bulk creation results.
    """
    api_url = f"{config.api_url}/table/sys_choice"
    created_count = 0
    failed_count = 0
    details = []

    for i, choice_data in enumerate(params.choices):
        # Build request data for each choice
        data = {
            "name": params.table,
            "element": params.element,
            "language": params.language,
            "label": choice_data.get("label", ""),
            "value": choice_data.get("value", ""),
            "inactive": choice_data.get("inactive", False),
        }

        # Add optional fields if provided
        if "sequence" in choice_data:
            data["sequence"] = choice_data["sequence"]
        if "hint" in choice_data:
            data["hint"] = choice_data["hint"]
        if "dependent_value" in choice_data:
            data["dependent_value"] = choice_data["dependent_value"]

        # Make individual request
        try:
            response = requests.post(
                api_url,
                json=data,
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            response.raise_for_status()
            result = response.json().get("result", {})
            
            created_count += 1
            details.append({
                "index": i,
                "success": True,
                "value": choice_data.get("value", ""),
                "sys_id": result.get("sys_id", ""),
                "message": "Created successfully"
            })

        except requests.RequestException as e:
            failed_count += 1
            details.append({
                "index": i,
                "success": False,
                "value": choice_data.get("value", ""),
                "message": f"Failed: {str(e)}"
            })
            logger.error(f"Failed to create choice {i}: {e}")

    return BulkChoiceResponse(
        success=failed_count == 0,
        message=f"Bulk choice creation completed: {created_count} created, {failed_count} failed",
        created_count=created_count,
        failed_count=failed_count,
        details=details,
    )


def reorder_choices(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ReorderChoicesParams,
) -> ChoiceResponse:
    """
    Reorder choices by updating their sequence values.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for reordering choices.

    Returns:
        Response with reordering result.
    """
    # First, get all existing choices for the field
    list_url = f"{config.api_url}/table/sys_choice"
    list_params = {
        "sysparm_query": f"name={params.table}^element={params.element}",
        "sysparm_fields": "sys_id,value,sequence"
    }

    try:
        # Get existing choices
        list_response = requests.get(
            list_url,
            params=list_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        list_response.raise_for_status()
        existing_choices = list_response.json().get("result", [])

        # Create a mapping of value to sys_id
        value_to_id = {choice["value"]: choice["sys_id"] for choice in existing_choices}

        # Update sequence for each choice in the specified order
        updated_count = 0
        for i, value in enumerate(params.choice_order):
            if value in value_to_id:
                choice_id = value_to_id[value]
                update_url = f"{config.api_url}/table/sys_choice/{choice_id}"
                
                update_response = requests.patch(
                    update_url,
                    json={"sequence": (i + 1) * 10},  # Use increments of 10 for flexibility
                    headers=auth_manager.get_headers(),
                    timeout=config.timeout,
                )
                update_response.raise_for_status()
                updated_count += 1

        return ChoiceResponse(
            success=True,
            message=f"Successfully reordered {updated_count} choices",
            data={"updated_count": updated_count, "total_requested": len(params.choice_order)}
        )

    except requests.RequestException as e:
        logger.error(f"Failed to reorder choices: {e}")
        return ChoiceResponse(
            success=False,
            message=f"Failed to reorder choices: {str(e)}",
        )