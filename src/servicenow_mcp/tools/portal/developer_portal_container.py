"""
Portal Container tools for the ServiceNow MCP server.

This module provides tools for managing portal container configurations
in the sp_container table, including creating, updating, listing, and cloning containers.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreatePortalContainerParams(BaseModel):
    """Parameters for creating a portal container."""
    
    name: str = Field(..., description="Name of the container")
    sp_page: str = Field(..., description="Page sys_id that this container belongs to")
    order: Optional[int] = Field(None, description="Display order within the page")
    class_name: Optional[str] = Field(None, description="Parent CSS class name")
    container_class_name: Optional[str] = Field(None, description="Container CSS class name")
    width: Optional[str] = Field("container", description="Width setting (container, container-fluid, etc.)")
    background_color: Optional[str] = Field(None, description="Background color")
    background_image: Optional[str] = Field(None, description="Background image attachment")
    background_style: Optional[str] = Field("default", description="Background style")
    bootstrap_alt: Optional[bool] = Field(False, description="Use Bootstrap alternative")
    subheader: Optional[bool] = Field(False, description="Move to header")
    title: Optional[str] = Field(None, description="Screen reader title")
    semantic_tag: Optional[str] = Field(None, description="Semantic HTML tag")


class UpdatePortalContainerParams(BaseModel):
    """Parameters for updating a portal container."""
    
    container_id: str = Field(..., description="Container sys_id to update")
    name: Optional[str] = Field(None, description="Updated name of the container")
    sp_page: Optional[str] = Field(None, description="Updated page sys_id")
    order: Optional[int] = Field(None, description="Updated display order")
    class_name: Optional[str] = Field(None, description="Updated parent CSS class name")
    container_class_name: Optional[str] = Field(None, description="Updated container CSS class name")
    width: Optional[str] = Field(None, description="Updated width setting")
    background_color: Optional[str] = Field(None, description="Updated background color")
    background_image: Optional[str] = Field(None, description="Updated background image")
    background_style: Optional[str] = Field(None, description="Updated background style")
    bootstrap_alt: Optional[bool] = Field(None, description="Updated Bootstrap alternative setting")
    subheader: Optional[bool] = Field(None, description="Updated move to header setting")
    title: Optional[str] = Field(None, description="Updated screen reader title")
    semantic_tag: Optional[str] = Field(None, description="Updated semantic HTML tag")


class ListPortalContainersParams(BaseModel):
    """Parameters for listing portal containers."""
    
    sp_page: Optional[str] = Field(None, description="Filter by page sys_id")
    semantic_tag: Optional[str] = Field(None, description="Filter by semantic tag")
    width: Optional[str] = Field(None, description="Filter by width setting")
    limit: int = Field(10, description="Maximum number of containers to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetPortalContainerParams(BaseModel):
    """Parameters for getting a specific portal container."""
    
    container_id: str = Field(..., description="Container sys_id or name to retrieve")


class ClonePortalContainerParams(BaseModel):
    """Parameters for cloning a portal container."""
    
    source_container_id: str = Field(..., description="Source container sys_id to clone")
    new_name: str = Field(..., description="Name for the cloned container")
    target_page: str = Field(..., description="Target page sys_id for the cloned container")
    copy_background: bool = Field(True, description="Whether to copy background settings from source")
    copy_styling: bool = Field(True, description="Whether to copy styling from source")
    new_order: Optional[int] = Field(None, description="Order for the cloned container (auto-calculated if not provided)")


class DeletePortalContainerParams(BaseModel):
    """Parameters for deleting a portal container."""
    
    container_id: str = Field(..., description="Container sys_id to delete")


class ReorderPortalContainersParams(BaseModel):
    """Parameters for reordering portal containers within a page."""
    
    page_id: str = Field(..., description="Page sys_id to reorder containers within")
    container_order: List[str] = Field(..., description="List of container sys_ids in desired order")


class PortalContainerResponse(BaseModel):
    """Response from portal container operations."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    container: Optional[Dict[str, Any]] = Field(None, description="Container data")
    containers: Optional[List[Dict[str, Any]]] = Field(None, description="List of containers")
    total_count: Optional[int] = Field(None, description="Total count of containers")


def create_portal_container(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalContainerParams,
) -> PortalContainerResponse:
    """
    Create a new portal container in the sp_container table.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the container.
    
    Returns:
        Response with the created container information.
    """
    api_url = f"{config.api_url}/table/sp_container"
    
    # Build request data
    data = {
        "name": params.name,
        "sp_page": params.sp_page,
    }
    
    # Add optional fields
    if params.order is not None:
        data["order"] = params.order
    if params.class_name:
        data["class_name"] = params.class_name
    if params.container_class_name:
        data["container_class_name"] = params.container_class_name
    if params.width:
        data["width"] = params.width
    if params.background_color:
        data["background_color"] = params.background_color
    if params.background_image:
        data["background_image"] = params.background_image
    if params.background_style:
        data["background_style"] = params.background_style
    if params.bootstrap_alt is not None:
        data["bootstrap_alt"] = params.bootstrap_alt
    if params.subheader is not None:
        data["subheader"] = params.subheader
    if params.title:
        data["title"] = params.title
    if params.semantic_tag:
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
        
        return PortalContainerResponse(
            success=True,
            message="Portal container created successfully",
            container=result,
        )
        
    except requests.RequestException as e:
        logger.error(f"Failed to create portal container: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to create portal container: {str(e)}",
        )


def update_portal_container(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdatePortalContainerParams,
) -> PortalContainerResponse:
    """
    Update an existing portal container in the sp_container table.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the container.
    
    Returns:
        Response with the updated container information.
    """
    api_url = f"{config.api_url}/table/sp_container/{params.container_id}"
    
    # Build request data with only provided fields
    data = {}
    
    if params.name:
        data["name"] = params.name
    if params.sp_page:
        data["sp_page"] = params.sp_page
    if params.order is not None:
        data["order"] = params.order
    if params.class_name is not None:
        data["class_name"] = params.class_name
    if params.container_class_name is not None:
        data["container_class_name"] = params.container_class_name
    if params.width is not None:
        data["width"] = params.width
    if params.background_color is not None:
        data["background_color"] = params.background_color
    if params.background_image is not None:
        data["background_image"] = params.background_image
    if params.background_style is not None:
        data["background_style"] = params.background_style
    if params.bootstrap_alt is not None:
        data["bootstrap_alt"] = params.bootstrap_alt
    if params.subheader is not None:
        data["subheader"] = params.subheader
    if params.title is not None:
        data["title"] = params.title
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
        
        return PortalContainerResponse(
            success=True,
            message="Portal container updated successfully",
            container=result,
        )
        
    except requests.RequestException as e:
        logger.error(f"Failed to update portal container: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to update portal container: {str(e)}",
        )


def list_portal_containers(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalContainersParams,
) -> PortalContainerResponse:
    """
    List portal containers from the sp_container table with optional filtering.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing containers.
    
    Returns:
        Response with list of containers.
    """
    api_url = f"{config.api_url}/table/sp_container"
    
    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
    }
    
    # Build query conditions
    query_conditions = []
    
    if params.sp_page:
        query_conditions.append(f"sp_page={params.sp_page}")
    if params.semantic_tag:
        query_conditions.append(f"semantic_tag={params.semantic_tag}")
    if params.width:
        query_conditions.append(f"width={params.width}")
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
        
        return PortalContainerResponse(
            success=True,
            message=f"Retrieved {len(result)} portal containers",
            containers=result,
            total_count=len(result),
        )
        
    except requests.RequestException as e:
        logger.error(f"Failed to list portal containers: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to list portal containers: {str(e)}",
        )


def get_portal_container(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalContainerParams,
) -> PortalContainerResponse:
    """
    Get detailed information about a specific portal container.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the container.
    
    Returns:
        Response with container details.
    """
    api_url = f"{config.api_url}/table/sp_container/{params.container_id}"
    
    query_params = {
        "sysparm_display_value": "true",
    }
    
    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        
        result = response.json().get("result", {})
        
        return PortalContainerResponse(
            success=True,
            message="Portal container retrieved successfully",
            container=result,
        )
        
    except requests.RequestException as e:
        logger.error(f"Failed to get portal container: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to get portal container: {str(e)}",
        )


def clone_portal_container(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ClonePortalContainerParams,
) -> PortalContainerResponse:
    """
    Clone an existing portal container to create a duplicate with optional modifications.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for cloning the container.
    
    Returns:
        Response with the cloned container information.
    """
    # First, get the source container
    try:
        get_response = get_portal_container(
            config, 
            auth_manager, 
            GetPortalContainerParams(container_id=params.source_container_id)
        )
        
        if not get_response.success or not get_response.container:
            return PortalContainerResponse(
                success=False,
                message="Failed to retrieve source container for cloning",
            )
        
        source_container = get_response.container
        
        # Build data for the new container
        clone_data = CreatePortalContainerParams(
            name=params.new_name,
            sp_page=params.target_page,
            order=params.new_order,
        )
        
        # Copy styling if requested
        if params.copy_styling:
            if source_container.get("class_name"):
                clone_data.class_name = source_container["class_name"]
            if source_container.get("container_class_name"):
                clone_data.container_class_name = source_container["container_class_name"]
            if source_container.get("width"):
                clone_data.width = source_container["width"]
            if source_container.get("bootstrap_alt"):
                clone_data.bootstrap_alt = source_container["bootstrap_alt"]
            if source_container.get("semantic_tag"):
                clone_data.semantic_tag = source_container["semantic_tag"]
        
        # Copy background settings if requested
        if params.copy_background:
            if source_container.get("background_color"):
                clone_data.background_color = source_container["background_color"]
            if source_container.get("background_image"):
                clone_data.background_image = source_container["background_image"]
            if source_container.get("background_style"):
                clone_data.background_style = source_container["background_style"]
        
        # Copy other settings
        if source_container.get("subheader"):
            clone_data.subheader = source_container["subheader"]
        if source_container.get("title"):
            clone_data.title = f"{source_container['title']} (Clone)"
        
        # Create the cloned container
        return create_portal_container(config, auth_manager, clone_data)
        
    except Exception as e:
        logger.error(f"Failed to clone portal container: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to clone portal container: {str(e)}",
        )


def delete_portal_container(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalContainerParams,
) -> PortalContainerResponse:
    """
    Delete a portal container from the sp_container table.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the container.
    
    Returns:
        Response indicating success or failure.
    """
    api_url = f"{config.api_url}/table/sp_container/{params.container_id}"
    
    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        
        return PortalContainerResponse(
            success=True,
            message="Portal container deleted successfully",
        )
        
    except requests.RequestException as e:
        logger.error(f"Failed to delete portal container: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to delete portal container: {str(e)}",
        )


def reorder_portal_containers(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ReorderPortalContainersParams,
) -> PortalContainerResponse:
    """
    Reorder portal containers within a page by updating their order values.
    
    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for reordering containers.
    
    Returns:
        Response indicating success or failure.
    """
    try:
        success_count = 0
        
        for index, container_id in enumerate(params.container_order, 1):
            update_params = UpdatePortalContainerParams(
                container_id=container_id,
                order=index * 10  # Use increments of 10 for easier reordering
            )
            
            result = update_portal_container(config, auth_manager, update_params)
            if result.success:
                success_count += 1
        
        if success_count == len(params.container_order):
            return PortalContainerResponse(
                success=True,
                message=f"Successfully reordered {success_count} containers",
            )
        else:
            return PortalContainerResponse(
                success=False,
                message=f"Only {success_count} of {len(params.container_order)} containers were reordered",
            )
            
    except Exception as e:
        logger.error(f"Failed to reorder portal containers: {e}")
        return PortalContainerResponse(
            success=False,
            message=f"Failed to reorder portal containers: {str(e)}",
        )