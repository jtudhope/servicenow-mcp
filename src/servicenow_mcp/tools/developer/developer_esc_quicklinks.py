"""
Employee Center Quick Link Management tools for the ServiceNow MCP server.

This module provides tools for managing quick links in the employee center
via the sn_ex_sp_quick_link table.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateQuickLinkParams(BaseModel):
    """Parameters for creating a quick link."""

    name: str = Field(..., description="Quick link name (required)")
    content_type: str = Field(..., description="Content type (page, external_link, knowledge, catalog_item)")
    active: Optional[bool] = Field(True, description="Whether the quick link is active")
    override_title: Optional[str] = Field(None, description="Override title for display")
    override_short_desc: Optional[str] = Field(None, description="Override short description")
    page: Optional[str] = Field(None, description="Service Portal page sys_id (for page content type)")
    external_link: Optional[str] = Field(None, description="External link sys_id (for external_link content type)")
    knowledge: Optional[str] = Field(None, description="Knowledge article sys_id (for knowledge content type)")
    catalog_item: Optional[str] = Field(None, description="Catalog item sys_id (for catalog_item content type)")
    icon_url: Optional[str] = Field(None, description="Icon URL for the quick link")
    background_image_url: Optional[str] = Field(None, description="Background image URL")
    additional_query_params: Optional[str] = Field(None, description="Additional query parameters for the page")


class UpdateQuickLinkParams(BaseModel):
    """Parameters for updating a quick link."""

    quick_link_id: str = Field(..., description="Quick link sys_id to update")
    name: Optional[str] = Field(None, description="Updated quick link name")
    content_type: Optional[str] = Field(None, description="Updated content type")
    active: Optional[bool] = Field(None, description="Updated active status")
    override_title: Optional[str] = Field(None, description="Updated override title")
    override_short_desc: Optional[str] = Field(None, description="Updated override short description")
    page: Optional[str] = Field(None, description="Updated Service Portal page sys_id")
    external_link: Optional[str] = Field(None, description="Updated external link sys_id")
    knowledge: Optional[str] = Field(None, description="Updated knowledge article sys_id")
    catalog_item: Optional[str] = Field(None, description="Updated catalog item sys_id")
    icon_url: Optional[str] = Field(None, description="Updated icon URL")
    background_image_url: Optional[str] = Field(None, description="Updated background image URL")
    additional_query_params: Optional[str] = Field(None, description="Updated additional query parameters")


class ListQuickLinksParams(BaseModel):
    """Parameters for listing quick links."""

    active: Optional[bool] = Field(None, description="Filter by active status")
    content_type: Optional[str] = Field(None, description="Filter by content type")
    limit: Optional[int] = Field(10, description="Maximum number of quick links to return")
    offset: Optional[int] = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetQuickLinkParams(BaseModel):
    """Parameters for getting a specific quick link."""

    quick_link_id: str = Field(..., description="Quick link sys_id or name to retrieve")


class DeleteQuickLinkParams(BaseModel):
    """Parameters for deleting a quick link."""

    quick_link_id: str = Field(..., description="Quick link sys_id to delete")


class QuickLinkResponse(BaseModel):
    """Response from quick link operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    quick_link: Optional[Dict[str, Any]] = Field(None, description="Quick link data")
    quick_links: Optional[List[Dict[str, Any]]] = Field(None, description="List of quick links")
    total_count: Optional[int] = Field(None, description="Total count for list operations")


def create_quick_link(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateQuickLinkParams,
) -> QuickLinkResponse:
    """
    Create a new employee center quick link.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the quick link.

    Returns:
        Response with the created quick link information.
    """
    api_url = f"{config.api_url}/table/sn_ex_sp_quick_link"

    # Build request data
    data = {
        "name": params.name,
        "content_type": params.content_type,
        "active": str(params.active).lower(),
    }

    # Add optional fields
    if params.override_title:
        data["override_title"] = params.override_title
    if params.override_short_desc:
        data["override_short_desc"] = params.override_short_desc
    if params.page:
        data["page"] = params.page
    if params.external_link:
        data["external_link"] = params.external_link
    if params.knowledge:
        data["knowledge"] = params.knowledge
    if params.catalog_item:
        data["catalog_item"] = params.catalog_item
    if params.icon_url:
        data["icon_url"] = params.icon_url
    if params.background_image_url:
        data["background_image_url"] = params.background_image_url
    if params.additional_query_params:
        data["additional_query_params"] = params.additional_query_params

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return QuickLinkResponse(
            success=True,
            message="Quick link created successfully",
            quick_link=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create quick link: {e}")
        return QuickLinkResponse(
            success=False,
            message=f"Failed to create quick link: {str(e)}",
        )


def update_quick_link(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateQuickLinkParams,
) -> QuickLinkResponse:
    """
    Update an existing employee center quick link.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the quick link.

    Returns:
        Response with the updated quick link information.
    """
    api_url = f"{config.api_url}/table/sn_ex_sp_quick_link/{params.quick_link_id}"

    # Build request data with only non-None fields
    data = {}
    if params.name is not None:
        data["name"] = params.name
    if params.content_type is not None:
        data["content_type"] = params.content_type
    if params.active is not None:
        data["active"] = str(params.active).lower()
    if params.override_title is not None:
        data["override_title"] = params.override_title
    if params.override_short_desc is not None:
        data["override_short_desc"] = params.override_short_desc
    if params.page is not None:
        data["page"] = params.page
    if params.external_link is not None:
        data["external_link"] = params.external_link
    if params.knowledge is not None:
        data["knowledge"] = params.knowledge
    if params.catalog_item is not None:
        data["catalog_item"] = params.catalog_item
    if params.icon_url is not None:
        data["icon_url"] = params.icon_url
    if params.background_image_url is not None:
        data["background_image_url"] = params.background_image_url
    if params.additional_query_params is not None:
        data["additional_query_params"] = params.additional_query_params

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return QuickLinkResponse(
            success=True,
            message="Quick link updated successfully",
            quick_link=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update quick link: {e}")
        return QuickLinkResponse(
            success=False,
            message=f"Failed to update quick link: {str(e)}",
        )


def list_quick_links(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListQuickLinksParams,
) -> QuickLinkResponse:
    """
    List employee center quick links with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing quick links.

    Returns:
        Response with the list of quick links.
    """
    api_url = f"{config.api_url}/table/sn_ex_sp_quick_link"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build query string
    query_parts = []
    if params.active is not None:
        query_parts.append(f"active={str(params.active).lower()}")
    if params.content_type:
        query_parts.append(f"content_type={params.content_type}")
    if params.query:
        query_parts.append(params.query)

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

        return QuickLinkResponse(
            success=True,
            message=f"Retrieved {len(result)} quick links",
            quick_links=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list quick links: {e}")
        return QuickLinkResponse(
            success=False,
            message=f"Failed to list quick links: {str(e)}",
        )


def get_quick_link(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetQuickLinkParams,
) -> QuickLinkResponse:
    """
    Get details of a specific employee center quick link.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the quick link.

    Returns:
        Response with the quick link details.
    """
    api_url = f"{config.api_url}/table/sn_ex_sp_quick_link/{params.quick_link_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return QuickLinkResponse(
            success=True,
            message="Quick link retrieved successfully",
            quick_link=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get quick link: {e}")
        return QuickLinkResponse(
            success=False,
            message=f"Failed to get quick link: {str(e)}",
        )


def delete_quick_link(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteQuickLinkParams,
) -> QuickLinkResponse:
    """
    Delete an employee center quick link.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the quick link.

    Returns:
        Response confirming the deletion.
    """
    api_url = f"{config.api_url}/table/sn_ex_sp_quick_link/{params.quick_link_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return QuickLinkResponse(
            success=True,
            message="Quick link deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete quick link: {e}")
        return QuickLinkResponse(
            success=False,
            message=f"Failed to delete quick link: {str(e)}",
        )
