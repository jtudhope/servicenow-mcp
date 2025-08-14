"""
Attachment Management tools for the ServiceNow MCP server.

This module provides tools for managing attachments using the ServiceNow Attachment API.
It handles upload, retrieval, listing, and deletion of file attachments to ServiceNow records.
"""

import base64
import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class UploadAttachmentParams(BaseModel):
    """Parameters for uploading an attachment using binary data."""

    table_name: str = Field(..., description="Name of the table to attach the file to")
    table_sys_id: str = Field(..., description="Sys_id of the record to attach the file to")
    file_name: str = Field(..., description="Name to give the attachment")
    file_data: str = Field(..., description="Base64 encoded file data")
    content_type: str = Field(..., description="Content type of the file (e.g., image/jpeg, image/png)")
    creation_time: Optional[str] = Field(None, description="Creation date and time of the attachment")
    encryption_context: Optional[str] = Field(None, description="Sys_id of an encryption context record")


class UploadMultipartAttachmentParams(BaseModel):
    """Parameters for uploading an attachment using multipart form data."""

    table_name: str = Field(..., description="Name of the table to attach the file to")
    table_sys_id: str = Field(..., description="Sys_id of the record to attach the file to")
    file_name: str = Field(..., description="Name to give the attachment")
    file_data: str = Field(..., description="Base64 encoded file data")
    content_type: str = Field(..., description="Content type of the file (e.g., image/jpeg, image/png)")


class ListAttachmentsParams(BaseModel):
    """Parameters for listing attachments."""

    limit: int = Field(1000, description="Maximum number of attachments to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Encoded query for filtering attachments")
    table_name: Optional[str] = Field(None, description="Filter by table name")
    table_sys_id: Optional[str] = Field(None, description="Filter by table sys_id")
    file_name: Optional[str] = Field(None, description="Filter by file name")
    content_type: Optional[str] = Field(None, description="Filter by content type")


class GetAttachmentParams(BaseModel):
    """Parameters for getting attachment metadata."""

    attachment_id: str = Field(..., description="Sys_id of the attachment")


class DownloadAttachmentParams(BaseModel):
    """Parameters for downloading attachment binary data."""

    attachment_id: str = Field(..., description="Sys_id of the attachment")
    accept_type: str = Field("*/*", description="Accept header for response type (e.g., image/*, */*)")


class DeleteAttachmentParams(BaseModel):
    """Parameters for deleting an attachment."""

    attachment_id: str = Field(..., description="Sys_id of the attachment to delete")


class AttachmentResponse(BaseModel):
    """Response from attachment operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def upload_attachment(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UploadAttachmentParams,
) -> AttachmentResponse:
    """
    Upload a file attachment using binary data to the ServiceNow Attachment API.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for uploading the attachment

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Uploading attachment: {params.file_name} to {params.table_name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/attachment/file"
    
    # Prepare query parameters
    query_params = {
        "table_name": params.table_name,
        "table_sys_id": params.table_sys_id,
        "file_name": params.file_name,
    }
    
    if params.creation_time:
        query_params["creation_time"] = params.creation_time
    if params.encryption_context:
        query_params["encryption_context"] = params.encryption_context
    
    # Decode base64 file data
    try:
        file_bytes = base64.b64decode(params.file_data)
    except Exception as e:
        logger.error(f"Failed to decode base64 file data: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Failed to decode base64 file data: {str(e)}",
            data=None,
        )
    
    # Prepare headers
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = params.content_type
    
    try:
        response = requests.post(
            url, 
            params=query_params,
            headers=headers, 
            data=file_bytes
        )
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        attachment = result.get("result", {})
        
        # Format the response
        formatted_attachment = {
            "sys_id": attachment.get("sys_id", ""),
            "file_name": attachment.get("file_name", ""),
            "content_type": attachment.get("content_type", ""),
            "table_name": attachment.get("table_name", ""),
            "table_sys_id": attachment.get("table_sys_id", ""),
            "size_bytes": attachment.get("size_bytes", ""),
            "size_compressed": attachment.get("size_compressed", ""),
            "download_link": attachment.get("download_link", ""),
            "compressed": attachment.get("compressed", ""),
            "sys_created_on": attachment.get("sys_created_on", ""),
            "sys_created_by": attachment.get("sys_created_by", ""),
        }
        
        return AttachmentResponse(
            success=True,
            message=f"Uploaded attachment: {params.file_name}",
            data=formatted_attachment,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error uploading attachment: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Error uploading attachment: {str(e)}",
            data=None,
        )


def upload_multipart_attachment(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UploadMultipartAttachmentParams,
) -> AttachmentResponse:
    """
    Upload a file attachment using multipart form data to the ServiceNow Attachment API.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for uploading the attachment

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Uploading multipart attachment: {params.file_name} to {params.table_name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/attachment/upload"
    
    # Decode base64 file data
    try:
        file_bytes = base64.b64decode(params.file_data)
    except Exception as e:
        logger.error(f"Failed to decode base64 file data: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Failed to decode base64 file data: {str(e)}",
            data=None,
        )
    
    # Prepare headers
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    # Note: Content-Type will be set automatically by requests for multipart data
    
    # Prepare multipart form data
    files = {
        'uploadFile': (params.file_name, file_bytes, params.content_type)
    }
    
    data = {
        'table_name': params.table_name,
        'table_sys_id': params.table_sys_id
    }
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            files=files,
            data=data
        )
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        attachment = result.get("result", {})
        
        # Format the response
        formatted_attachment = {
            "sys_id": attachment.get("sys_id", ""),
            "file_name": attachment.get("file_name", ""),
            "content_type": attachment.get("content_type", ""),
            "table_name": attachment.get("table_name", ""),
            "table_sys_id": attachment.get("table_sys_id", ""),
            "size_bytes": attachment.get("size_bytes", ""),
            "size_compressed": attachment.get("size_compressed", ""),
            "download_link": attachment.get("download_link", ""),
            "compressed": attachment.get("compressed", ""),
            "sys_created_on": attachment.get("sys_created_on", ""),
            "sys_created_by": attachment.get("sys_created_by", ""),
        }
        
        return AttachmentResponse(
            success=True,
            message=f"Uploaded multipart attachment: {params.file_name}",
            data=formatted_attachment,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error uploading multipart attachment: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Error uploading multipart attachment: {str(e)}",
            data=None,
        )


def list_attachments(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListAttachmentsParams,
) -> Dict[str, Any]:
    """
    List attachments from the ServiceNow Attachment API.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing attachments

    Returns:
        Dictionary containing attachments and metadata
    """
    logger.info("Listing attachments")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/attachment"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }
    
    # Build query filters
    filters = []
    if params.table_name:
        filters.append(f"table_name={params.table_name}")
    if params.table_sys_id:
        filters.append(f"table_sys_id={params.table_sys_id}")
    if params.file_name:
        filters.append(f"file_name={params.file_name}")
    if params.content_type:
        filters.append(f"content_type={params.content_type}")
    if params.query:
        filters.append(params.query)
    
    if filters:
        query_params["sysparm_query"] = "^".join(filters)
    
    # Prepare headers
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        attachments = result.get("result", [])
        
        # Format the response
        formatted_attachments = []
        for attachment in attachments:
            formatted_attachments.append({
                "sys_id": attachment.get("sys_id", ""),
                "file_name": attachment.get("file_name", ""),
                "content_type": attachment.get("content_type", ""),
                "table_name": attachment.get("table_name", ""),
                "table_sys_id": attachment.get("table_sys_id", ""),
                "size_bytes": attachment.get("size_bytes", ""),
                "size_compressed": attachment.get("size_compressed", ""),
                "download_link": attachment.get("download_link", ""),
                "compressed": attachment.get("compressed", ""),
                "image_width": attachment.get("image_width", ""),
                "image_height": attachment.get("image_height", ""),
                "average_image_color": attachment.get("average_image_color", ""),
                "sys_created_on": attachment.get("sys_created_on", ""),
                "sys_created_by": attachment.get("sys_created_by", ""),
                "sys_updated_on": attachment.get("sys_updated_on", ""),
                "sys_updated_by": attachment.get("sys_updated_by", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_attachments)} attachments",
            "attachments": formatted_attachments,
            "total": len(formatted_attachments),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing attachments: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing attachments: {str(e)}",
            "attachments": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_attachment(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetAttachmentParams,
) -> AttachmentResponse:
    """
    Get attachment metadata from the ServiceNow Attachment API.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the attachment

    Returns:
        Response containing the attachment metadata
    """
    logger.info(f"Getting attachment: {params.attachment_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/attachment/{params.attachment_id}"
    
    # Prepare headers
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        attachment = result.get("result", {})
        
        if not attachment:
            return AttachmentResponse(
                success=False,
                message=f"Attachment not found: {params.attachment_id}",
                data=None,
            )
        
        # Format the response
        formatted_attachment = {
            "sys_id": attachment.get("sys_id", ""),
            "file_name": attachment.get("file_name", ""),
            "content_type": attachment.get("content_type", ""),
            "table_name": attachment.get("table_name", ""),
            "table_sys_id": attachment.get("table_sys_id", ""),
            "size_bytes": attachment.get("size_bytes", ""),
            "size_compressed": attachment.get("size_compressed", ""),
            "download_link": attachment.get("download_link", ""),
            "compressed": attachment.get("compressed", ""),
            "image_width": attachment.get("image_width", ""),
            "image_height": attachment.get("image_height", ""),
            "average_image_color": attachment.get("average_image_color", ""),
            "sys_created_on": attachment.get("sys_created_on", ""),
            "sys_created_by": attachment.get("sys_created_by", ""),
            "sys_updated_on": attachment.get("sys_updated_on", ""),
            "sys_updated_by": attachment.get("sys_updated_by", ""),
        }
        
        return AttachmentResponse(
            success=True,
            message=f"Retrieved attachment: {attachment.get('file_name', '')}",
            data=formatted_attachment,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting attachment: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Error getting attachment: {str(e)}",
            data=None,
        )


def download_attachment(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DownloadAttachmentParams,
) -> AttachmentResponse:
    """
    Download attachment binary data from the ServiceNow Attachment API.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for downloading the attachment

    Returns:
        Response containing the base64 encoded attachment data
    """
    logger.info(f"Downloading attachment: {params.attachment_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/attachment/{params.attachment_id}/file"
    
    # Prepare headers
    headers = auth_manager.get_headers()
    headers["Accept"] = params.accept_type
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Encode binary data as base64
        file_data_base64 = base64.b64encode(response.content).decode('utf-8')
        
        # Get metadata from response headers
        metadata = {}
        if 'X-Attachment-Metadata' in response.headers:
            metadata['attachment_metadata'] = response.headers['X-Attachment-Metadata']
        
        # Format the response
        formatted_response = {
            "file_data_base64": file_data_base64,
            "content_type": response.headers.get('Content-Type', ''),
            "content_length": len(response.content),
            "metadata": metadata,
        }
        
        return AttachmentResponse(
            success=True,
            message=f"Downloaded attachment: {params.attachment_id}",
            data=formatted_response,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading attachment: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Error downloading attachment: {str(e)}",
            data=None,
        )


def delete_attachment(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteAttachmentParams,
) -> AttachmentResponse:
    """
    Delete an attachment from the ServiceNow Attachment API.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the attachment

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting attachment: {params.attachment_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/attachment/{params.attachment_id}"
    
    # Prepare headers
    headers = auth_manager.get_headers()
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return AttachmentResponse(
            success=True,
            message=f"Deleted attachment: {params.attachment_id}",
            data={"deleted_attachment_id": params.attachment_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting attachment: {str(e)}")
        return AttachmentResponse(
            success=False,
            message=f"Error deleting attachment: {str(e)}",
            data=None,
        )