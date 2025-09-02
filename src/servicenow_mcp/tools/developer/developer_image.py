"""
Image Management tools for the ServiceNow MCP server.

This module provides tools for managing images that are stored in the db_image table.
It can handle image uploads and creation in the ServiceNow database.
"""

import base64
import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateImageParams(BaseModel):
    """Parameters for creating an image in db_image table."""

    name: str = Field(..., description="Name of the image")
    image_data: str = Field(..., description="Base64 encoded image data")
    content_type: Optional[str] = Field(None, description="MIME type of the image (e.g., 'image/png', 'image/jpeg')")
    table_name: Optional[str] = Field(None, description="Table name this image is associated with")
    table_sys_id: Optional[str] = Field(None, description="Sys ID of the record this image is associated with")
    image_type: Optional[str] = Field("attachment", description="Type of image (attachment, logo, icon, etc.)")
    size_bytes: Optional[int] = Field(None, description="Size of the image in bytes")
    size_compressed: Optional[int] = Field(None, description="Compressed size of the image in bytes")
    width: Optional[int] = Field(None, description="Width of the image in pixels")
    height: Optional[int] = Field(None, description="Height of the image in pixels")
    format: Optional[str] = Field(None, description="Image format (e.g., 'PNG', 'JPEG')")
    category: Optional[str] = Field(None, description="Image category")
    active: Optional[bool] = Field(True, description="Whether the image is active")


class UpdateImageParams(BaseModel):
    """Parameters for updating an image in db_image table."""

    image_id: str = Field(..., description="Image sys_id")
    name: Optional[str] = Field(None, description="Name of the image")
    image_data: Optional[str] = Field(None, description="Base64 encoded image data")
    content_type: Optional[str] = Field(None, description="MIME type of the image")
    table_name: Optional[str] = Field(None, description="Table name this image is associated with")
    table_sys_id: Optional[str] = Field(None, description="Sys ID of the record this image is associated with")
    image_type: Optional[str] = Field(None, description="Type of image")
    width: Optional[int] = Field(None, description="Width of the image in pixels")
    height: Optional[int] = Field(None, description="Height of the image in pixels")
    format: Optional[str] = Field(None, description="Image format (e.g., 'PNG', 'JPEG')")
    category: Optional[str] = Field(None, description="Image category")
    active: Optional[bool] = Field(None, description="Whether the image is active")


class ListImagesParams(BaseModel):
    """Parameters for listing images from db_image table."""

    limit: int = Field(10, description="Maximum number of images to return")
    offset: int = Field(0, description="Offset for pagination")
    table_name: Optional[str] = Field(None, description="Filter by table name")
    table_sys_id: Optional[str] = Field(None, description="Filter by table sys_id")
    image_type: Optional[str] = Field(None, description="Filter by image type")
    content_type: Optional[str] = Field(None, description="Filter by content type")
    category: Optional[str] = Field(None, description="Filter by image category")
    active: Optional[bool] = Field(None, description="Filter by active status")
    query: Optional[str] = Field(None, description="Search query for image name")


class GetImageParams(BaseModel):
    """Parameters for getting a specific image."""

    image_id: str = Field(..., description="Image sys_id")
    include_data: bool = Field(False, description="Whether to include base64 image data in response")


class DeleteImageParams(BaseModel):
    """Parameters for deleting an image."""

    image_id: str = Field(..., description="Image sys_id")


class ImageResponse(BaseModel):
    """Response from image operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_image(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateImageParams,
) -> ImageResponse:
    """
    Create a new image in the db_image table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the image

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating image: {params.name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/db_image"
    
    # Prepare request body
    body = {
        "name": params.name,
        "image": params.image_data,
        "content_type": params.content_type,
    }
    
    if params.table_name is not None:
        body["table_name"] = params.table_name
    if params.table_sys_id is not None:
        body["table_sys_id"] = params.table_sys_id
    if params.image_type is not None:
        body["image_type"] = params.image_type
    if params.size_bytes is not None:
        body["size_bytes"] = str(params.size_bytes)
    if params.size_compressed is not None:
        body["size_compressed"] = str(params.size_compressed)
    if params.width is not None:
        body["width"] = str(params.width)
    if params.height is not None:
        body["height"] = str(params.height)
    if params.format is not None:
        body["format"] = params.format
    if params.category is not None:
        body["category"] = params.category
    if params.active is not None:
        body["active"] = str(params.active).lower()
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        image = result.get("result", {})
        
        # Format the response
        formatted_image = {
            "sys_id": image.get("sys_id", ""),
            "name": image.get("name", ""),
            "content_type": image.get("content_type", ""),
            "table_name": image.get("table_name", ""),
            "table_sys_id": image.get("table_sys_id", ""),
            "image_type": image.get("image_type", ""),
            "size_bytes": image.get("size_bytes", ""),
            "size_compressed": image.get("size_compressed", ""),
            "width": image.get("width", ""),
            "height": image.get("height", ""),
            "format": image.get("format", ""),
            "category": image.get("category", ""),
            "active": image.get("active", ""),
            "sys_created_on": image.get("sys_created_on", ""),
        }
        
        return ImageResponse(
            success=True,
            message=f"Created image: {params.name}",
            data=formatted_image,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating image: {str(e)}")
        return ImageResponse(
            success=False,
            message=f"Error creating image: {str(e)}",
            data=None,
        )


def update_image(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateImageParams,
) -> ImageResponse:
    """
    Update an existing image in the db_image table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the image

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating image: {params.image_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/db_image/{params.image_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.name is not None:
        body["name"] = params.name
    if params.image_data is not None:
        body["image"] = params.image_data
    if params.content_type is not None:
        body["content_type"] = params.content_type
    if params.table_name is not None:
        body["table_name"] = params.table_name
    if params.table_sys_id is not None:
        body["table_sys_id"] = params.table_sys_id
    if params.image_type is not None:
        body["image_type"] = params.image_type
    if params.width is not None:
        body["width"] = str(params.width)
    if params.height is not None:
        body["height"] = str(params.height)
    if params.format is not None:
        body["format"] = params.format
    if params.category is not None:
        body["category"] = params.category
    if params.active is not None:
        body["active"] = str(params.active).lower()
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        image = result.get("result", {})
        
        # Format the response
        formatted_image = {
            "sys_id": image.get("sys_id", ""),
            "name": image.get("name", ""),
            "content_type": image.get("content_type", ""),
            "table_name": image.get("table_name", ""),
            "table_sys_id": image.get("table_sys_id", ""),
            "image_type": image.get("image_type", ""),
            "size_bytes": image.get("size_bytes", ""),
            "size_compressed": image.get("size_compressed", ""),
            "width": image.get("width", ""),
            "height": image.get("height", ""),
            "format": image.get("format", ""),
            "category": image.get("category", ""),
            "active": image.get("active", ""),
            "sys_updated_on": image.get("sys_updated_on", ""),
        }
        
        return ImageResponse(
            success=True,
            message=f"Updated image: {params.image_id}",
            data=formatted_image,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating image: {str(e)}")
        return ImageResponse(
            success=False,
            message=f"Error updating image: {str(e)}",
            data=None,
        )


def list_images(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListImagesParams,
) -> Dict[str, Any]:
    """
    List images from the db_image table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing images

    Returns:
        Dictionary containing images and metadata
    """
    logger.info("Listing images")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/db_image"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,content_type,table_name,table_sys_id,image_type,size_bytes,size_compressed,width,height,format,category,active,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.table_name:
        filters.append(f"table_name={params.table_name}")
    if params.table_sys_id:
        filters.append(f"table_sys_id={params.table_sys_id}")
    if params.image_type:
        filters.append(f"image_type={params.image_type}")
    if params.content_type:
        filters.append(f"content_type={params.content_type}")
    if params.category:
        filters.append(f"category={params.category}")
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    if params.query:
        filters.append(f"nameLIKE{params.query}")
    
    if filters:
        query_params["sysparm_query"] = "^".join(filters)
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        images = result.get("result", [])
        
        # Format the response
        formatted_images = []
        for image in images:
            formatted_images.append({
                "sys_id": image.get("sys_id", ""),
                "name": image.get("name", ""),
                "content_type": image.get("content_type", ""),
                "table_name": image.get("table_name", ""),
                "table_sys_id": image.get("table_sys_id", ""),
                "image_type": image.get("image_type", ""),
                "size_bytes": image.get("size_bytes", ""),
                "size_compressed": image.get("size_compressed", ""),
                "width": image.get("width", ""),
                "height": image.get("height", ""),
                "format": image.get("format", ""),
                "category": image.get("category", ""),
                "active": image.get("active", ""),
                "sys_created_on": image.get("sys_created_on", ""),
                "sys_updated_on": image.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_images)} images",
            "images": formatted_images,
            "total": len(formatted_images),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing images: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing images: {str(e)}",
            "images": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_image(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetImageParams,
) -> ImageResponse:
    """
    Get a specific image from the db_image table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the image

    Returns:
        Response containing the image details
    """
    logger.info(f"Getting image: {params.image_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/db_image/{params.image_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Include image data if requested
    if params.include_data:
        query_params["sysparm_fields"] = "sys_id,name,content_type,table_name,table_sys_id,image_type,size_bytes,size_compressed,width,height,format,category,active,sys_created_on,sys_updated_on,image"
    else:
        query_params["sysparm_fields"] = "sys_id,name,content_type,table_name,table_sys_id,image_type,size_bytes,size_compressed,width,height,format,category,active,sys_created_on,sys_updated_on"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        image = result.get("result", {})
        
        if not image:
            return ImageResponse(
                success=False,
                message=f"Image not found: {params.image_id}",
                data=None,
            )
        
        # Format the response
        formatted_image = {
            "sys_id": image.get("sys_id", ""),
            "name": image.get("name", ""),
            "content_type": image.get("content_type", ""),
            "table_name": image.get("table_name", ""),
            "table_sys_id": image.get("table_sys_id", ""),
            "image_type": image.get("image_type", ""),
            "size_bytes": image.get("size_bytes", ""),
            "size_compressed": image.get("size_compressed", ""),
            "width": image.get("width", ""),
            "height": image.get("height", ""),
            "format": image.get("format", ""),
            "category": image.get("category", ""),
            "active": image.get("active", ""),
            "sys_created_on": image.get("sys_created_on", ""),
            "sys_updated_on": image.get("sys_updated_on", ""),
        }
        
        # Include image data if requested
        if params.include_data and "image" in image:
            formatted_image["image_data"] = image.get("image", "")
        
        return ImageResponse(
            success=True,
            message=f"Retrieved image: {image.get('name', '')}",
            data=formatted_image,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting image: {str(e)}")
        return ImageResponse(
            success=False,
            message=f"Error getting image: {str(e)}",
            data=None,
        )


def delete_image(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteImageParams,
) -> ImageResponse:
    """
    Delete an image from the db_image table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the image

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting image: {params.image_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/db_image/{params.image_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return ImageResponse(
            success=True,
            message=f"Deleted image: {params.image_id}",
            data={"deleted_image_id": params.image_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting image: {str(e)}")
        return ImageResponse(
            success=False,
            message=f"Error deleting image: {str(e)}",
            data=None,
        )