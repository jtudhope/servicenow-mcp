# File: src/servicenow_mcp/tools/portal_pages.py

"""
Portal UI Page Configuration Management tools for the ServiceNow MCP server.

This module provides tools for managing portal page configurations in the sp_page table,
including creating, updating, listing, and cloning portal pages.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreatePortalPageParams(BaseModel):
    """Parameters for creating a portal page."""

    id: str = Field(..., description="Unique identifier for the page")
    title: str = Field(..., description="Display title of the page")
    short_description: Optional[str] = Field(None, description="Short description of the page")
    css: Optional[str] = Field(None, description="Page-specific CSS styling")
    public: Optional[bool] = Field(False, description="Whether the page is publicly accessible")
    roles: Optional[List[str]] = Field(None, description="List of roles required to access this page")
    internal: Optional[bool] = Field(False, description="Whether this is an internal page")
    draft: Optional[bool] = Field(False, description="Whether the page is in draft mode")
    omit_watcher: Optional[bool] = Field(False, description="Whether to omit watcher functionality")
    dynamic_title_structure: Optional[str] = Field(None, description="Dynamic page title structure")
    category: Optional[str] = Field("custom", description="Page category")
    use_seo_script: Optional[bool] = Field(False, description="Whether to use SEO script")
    seo_script: Optional[str] = Field(None, description="SEO script sys_id reference")
    human_readable_url_structure: Optional[str] = Field(None, description="Human readable URL structure")


class UpdatePortalPageParams(BaseModel):
    """Parameters for updating a portal page."""

    page_id: str = Field(..., description="Page ID or sys_id to update")
    title: Optional[str] = Field(None, description="Updated display title")
    short_description: Optional[str] = Field(None, description="Updated short description")
    css: Optional[str] = Field(None, description="Updated page-specific CSS")
    public: Optional[bool] = Field(None, description="Updated public accessibility")
    roles: Optional[List[str]] = Field(None, description="Updated roles list")
    internal: Optional[bool] = Field(None, description="Updated internal status")
    draft: Optional[bool] = Field(None, description="Updated draft status")
    omit_watcher: Optional[bool] = Field(None, description="Updated omit watcher setting")
    dynamic_title_structure: Optional[str] = Field(None, description="Updated dynamic title structure")
    category: Optional[str] = Field(None, description="Updated page category")
    use_seo_script: Optional[bool] = Field(None, description="Updated SEO script usage")
    seo_script: Optional[str] = Field(None, description="Updated SEO script reference")
    human_readable_url_structure: Optional[str] = Field(None, description="Updated URL structure")


class ListPortalPagesParams(BaseModel):
    """Parameters for listing portal pages."""

    limit: int = Field(10, description="Maximum number of pages to return")
    offset: int = Field(0, description="Offset for pagination")
    category: Optional[str] = Field(None, description="Filter by category")
    public: Optional[bool] = Field(None, description="Filter by public status")
    draft: Optional[bool] = Field(None, description="Filter by draft status")
    internal: Optional[bool] = Field(None, description="Filter by internal status")
    query: Optional[str] = Field(None, description="Additional query string")


class ClonePortalPageParams(BaseModel):
    """Parameters for cloning a portal page."""

    source_page_id: str = Field(..., description="Source page ID or sys_id to clone")
    new_page_id: str = Field(..., description="New unique ID for the cloned page")
    new_title: str = Field(..., description="Title for the cloned page")
    new_short_description: Optional[str] = Field(None, description="Short description for the cloned page")
    copy_css: Optional[bool] = Field(True, description="Whether to copy CSS from source")
    copy_roles: Optional[bool] = Field(True, description="Whether to copy roles from source")


class GetPortalPageParams(BaseModel):
    """Parameters for getting a specific portal page."""

    page_id: str = Field(..., description="Page ID or sys_id to retrieve")


class DeletePortalPageParams(BaseModel):
    """Parameters for deleting a portal page."""

    page_id: str = Field(..., description="Page ID or sys_id to delete")


class PortalPageResponse(BaseModel):
    """Response from portal page operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    page_id: Optional[str] = Field(None, description="Page sys_id")
    page_data: Optional[Dict[str, Any]] = Field(None, description="Page data")
    pages: Optional[List[Dict[str, Any]]] = Field(None, description="List of pages for list operations")
    total_count: Optional[int] = Field(None, description="Total count for list operations")


def create_portal_page(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalPageParams,
) -> PortalPageResponse:
    """
    Create a new portal page in the sp_page table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the portal page.

    Returns:
        Response with creation result and page details.
    """
    api_url = f"{config.api_url}/table/sp_page"

    # Build request data
    data = {
        "id": params.id,
        "title": params.title,
    }

    # Add optional fields
    if params.short_description is not None:
        data["short_description"] = params.short_description
    if params.css is not None:
        data["css"] = params.css
    if params.public is not None:
        data["public"] = params.public
    if params.roles is not None:
        data["roles"] = ",".join(params.roles)
    if params.internal is not None:
        data["internal"] = params.internal
    if params.draft is not None:
        data["draft"] = params.draft
    if params.omit_watcher is not None:
        data["omit_watcher"] = params.omit_watcher
    if params.dynamic_title_structure is not None:
        data["dynamic_title_structure"] = params.dynamic_title_structure
    if params.category is not None:
        data["category"] = params.category
    if params.use_seo_script is not None:
        data["use_seo_script"] = params.use_seo_script
    if params.seo_script is not None:
        data["seo_script"] = params.seo_script
    if params.human_readable_url_structure is not None:
        data["human_readable_url_structure"] = params.human_readable_url_structure

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalPageResponse(
            success=True,
            message="Portal page created successfully",
            page_id=result.get("sys_id"),
            page_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create portal page: {e}")
        return PortalPageResponse(
            success=False,
            message=f"Failed to create portal page: {str(e)}",
        )


def update_portal_page(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdatePortalPageParams,
) -> PortalPageResponse:
    """
    Update an existing portal page in the sp_page table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the portal page.

    Returns:
        Response with update result and page details.
    """
    # First, find the page by ID or sys_id
    search_url = f"{config.api_url}/table/sp_page"
    search_params = {"sysparm_query": f"id={params.page_id}^ORsys_id={params.page_id}", "sysparm_limit": 1}
    
    try:
        search_response = requests.get(
            search_url,
            params=search_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        search_response.raise_for_status()
        search_result = search_response.json().get("result", [])
        
        if not search_result:
            return PortalPageResponse(
                success=False,
                message=f"Portal page not found with ID: {params.page_id}",
            )
        
        sys_id = search_result[0]["sys_id"]
        api_url = f"{config.api_url}/table/sp_page/{sys_id}"

        # Build update data
        data = {}
        
        if params.title is not None:
            data["title"] = params.title
        if params.short_description is not None:
            data["short_description"] = params.short_description
        if params.css is not None:
            data["css"] = params.css
        if params.public is not None:
            data["public"] = params.public
        if params.roles is not None:
            data["roles"] = ",".join(params.roles)
        if params.internal is not None:
            data["internal"] = params.internal
        if params.draft is not None:
            data["draft"] = params.draft
        if params.omit_watcher is not None:
            data["omit_watcher"] = params.omit_watcher
        if params.dynamic_title_structure is not None:
            data["dynamic_title_structure"] = params.dynamic_title_structure
        if params.category is not None:
            data["category"] = params.category
        if params.use_seo_script is not None:
            data["use_seo_script"] = params.use_seo_script
        if params.seo_script is not None:
            data["seo_script"] = params.seo_script
        if params.human_readable_url_structure is not None:
            data["human_readable_url_structure"] = params.human_readable_url_structure

        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalPageResponse(
            success=True,
            message="Portal page updated successfully",
            page_id=result.get("sys_id"),
            page_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update portal page: {e}")
        return PortalPageResponse(
            success=False,
            message=f"Failed to update portal page: {str(e)}",
        )


def list_portal_pages(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalPagesParams,
) -> PortalPageResponse:
    """
    List portal pages from the sp_page table with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing portal pages.

    Returns:
        Response with list of pages and pagination details.
    """
    api_url = f"{config.api_url}/table/sp_page"

    # Build query parameters
    query_parts = []
    
    if params.category is not None:
        query_parts.append(f"category={params.category}")
    if params.public is not None:
        query_parts.append(f"public={params.public}")
    if params.draft is not None:
        query_parts.append(f"draft={params.draft}")
    if params.internal is not None:
        query_parts.append(f"internal={params.internal}")
    if params.query:
        query_parts.append(params.query)

    query_string = "^".join(query_parts) if query_parts else ""

    request_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_count": "true",
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

        return PortalPageResponse(
            success=True,
            message=f"Retrieved {len(result)} portal pages",
            pages=result,
            total_count=total_count,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list portal pages: {e}")
        return PortalPageResponse(
            success=False,
            message=f"Failed to list portal pages: {str(e)}",
        )


def get_portal_page(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalPageParams,
) -> PortalPageResponse:
    """
    Get a specific portal page by ID or sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the portal page.

    Returns:
        Response with page details.
    """
    api_url = f"{config.api_url}/table/sp_page"
    search_params = {"sysparm_query": f"id={params.page_id}^ORsys_id={params.page_id}", "sysparm_limit": 1}

    try:
        response = requests.get(
            api_url,
            params=search_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])
        
        if not result:
            return PortalPageResponse(
                success=False,
                message=f"Portal page not found with ID: {params.page_id}",
            )

        page_data = result[0]

        return PortalPageResponse(
            success=True,
            message="Portal page retrieved successfully",
            page_id=page_data.get("sys_id"),
            page_data=page_data,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get portal page: {e}")
        return PortalPageResponse(
            success=False,
            message=f"Failed to get portal page: {str(e)}",
        )


def clone_portal_page(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ClonePortalPageParams,
) -> PortalPageResponse:
    """
    Clone an existing portal page to create a duplicate with modifications.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for cloning the portal page.

    Returns:
        Response with cloned page details.
    """
    # First, get the source page
    get_params = GetPortalPageParams(page_id=params.source_page_id)
    source_result = get_portal_page(config, auth_manager, get_params)
    
    if not source_result.success:
        return PortalPageResponse(
            success=False,
            message=f"Failed to find source page: {source_result.message}",
        )

    source_data = source_result.page_data
    
    # Create clone data based on source
    clone_data = {
        "id": params.new_page_id,
        "title": params.new_title,
        "short_description": params.new_short_description or source_data.get("short_description", ""),
        "category": source_data.get("category", "custom"),
        "public": source_data.get("public", False),
        "internal": source_data.get("internal", False),
        "draft": True,  # Always create clones as drafts
        "omit_watcher": source_data.get("omit_watcher", False),
        "dynamic_title_structure": source_data.get("dynamic_title_structure", ""),
        "use_seo_script": source_data.get("use_seo_script", False),
        "human_readable_url_structure": source_data.get("human_readable_url_structure", ""),
    }

    # Conditionally copy CSS and roles
    if params.copy_css and source_data.get("css"):
        clone_data["css"] = source_data["css"]
    
    if params.copy_roles and source_data.get("roles"):
        clone_data["roles"] = source_data["roles"]

    if source_data.get("seo_script"):
        clone_data["seo_script"] = source_data["seo_script"]

    # Create the cloned page
    api_url = f"{config.api_url}/table/sp_page"

    try:
        response = requests.post(
            api_url,
            json=clone_data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalPageResponse(
            success=True,
            message=f"Portal page cloned successfully from {params.source_page_id}",
            page_id=result.get("sys_id"),
            page_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to clone portal page: {e}")
        return PortalPageResponse(
            success=False,
            message=f"Failed to clone portal page: {str(e)}",
        )


def delete_portal_page(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalPageParams,
) -> PortalPageResponse:
    """
    Delete a portal page by ID or sys_id.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the portal page.

    Returns:
        Response with deletion result.
    """
    # First, find the page by ID or sys_id
    search_url = f"{config.api_url}/table/sp_page"
    search_params = {"sysparm_query": f"id={params.page_id}^ORsys_id={params.page_id}", "sysparm_limit": 1}
    
    try:
        search_response = requests.get(
            search_url,
            params=search_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        search_response.raise_for_status()
        search_result = search_response.json().get("result", [])
        
        if not search_result:
            return PortalPageResponse(
                success=False,
                message=f"Portal page not found with ID: {params.page_id}",
            )
        
        sys_id = search_result[0]["sys_id"]
        api_url = f"{config.api_url}/table/sp_page/{sys_id}"

        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return PortalPageResponse(
            success=True,
            message=f"Portal page deleted successfully",
            page_id=sys_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete portal page: {e}")
        return PortalPageResponse(
            success=False,
            message=f"Failed to delete portal page: {str(e)}",
        )