"""
Connected Content tools for the ServiceNow MCP server.

This module provides tools for managing Connected Content relationships that are 
stored in the m2m_connected_content table. In ServiceNow, the m2m_connected_content 
table is a many-to-many relationship table that links Connected Content records 
to other records in the platform like knowledge articles, catalog items, topics, 
and quick links.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateConnectedContentParams(BaseModel):
    """Parameters for creating a connected content relationship."""

    topic: str = Field(..., description="Topic sys_id (required)")
    content_type: str = Field(..., description="Content type configuration sys_id (required)")
    catalog_item: Optional[str] = Field(None, description="Catalog item sys_id for catalog content connections")
    knowledge: Optional[str] = Field(None, description="Knowledge article sys_id for knowledge content connections")
    quick_link: Optional[str] = Field(None, description="Quick link sys_id for quick link content connections")
    order: Optional[int] = Field(100, description="Display order for the connection")
    popularity: Optional[float] = Field(None, description="Popularity score for the content")
    content_display_value: Optional[str] = Field(None, description="Display value for the connected content")
    alphabetical_order: Optional[int] = Field(None, description="Alphabetical ordering value")
    sys_domain: Optional[str] = Field("global", description="Domain for the connection")
    sys_domain_path: Optional[str] = Field("/", description="Domain path for the connection")


class UpdateConnectedContentParams(BaseModel):
    """Parameters for updating a connected content relationship."""

    connection_id: str = Field(..., description="Connected content relationship sys_id")
    order: Optional[int] = Field(None, description="Updated display order")
    popularity: Optional[float] = Field(None, description="Updated popularity score")
    content_display_value: Optional[str] = Field(None, description="Updated display value")
    alphabetical_order: Optional[int] = Field(None, description="Updated alphabetical ordering")


class ListConnectedContentParams(BaseModel):
    """Parameters for listing connected content relationships."""

    limit: int = Field(10, description="Maximum number of connections to return")
    offset: int = Field(0, description="Offset for pagination")
    topic: Optional[str] = Field(None, description="Filter by topic sys_id")
    content_type: Optional[str] = Field(None, description="Filter by content type sys_id")
    catalog_item: Optional[str] = Field(None, description="Filter by catalog item sys_id")
    knowledge: Optional[str] = Field(None, description="Filter by knowledge article sys_id")
    quick_link: Optional[str] = Field(None, description="Filter by quick link sys_id")
    sys_domain: Optional[str] = Field(None, description="Filter by domain")
    query: Optional[str] = Field(None, description="Additional query string")


class GetConnectedContentParams(BaseModel):
    """Parameters for getting a connected content relationship."""

    connection_id: str = Field(..., description="Connected content relationship sys_id")


class DeleteConnectedContentParams(BaseModel):
    """Parameters for deleting a connected content relationship."""

    connection_id: str = Field(..., description="Connected content relationship sys_id")


class BulkConnectContentParams(BaseModel):
    """Parameters for bulk connecting multiple content items to a topic."""

    topic: str = Field(..., description="Topic sys_id to connect content to")
    connections: List[Dict[str, Any]] = Field(..., description="List of content connections to create")


class ConnectedContentResponse(BaseModel):
    """Response from connected content operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_connected_content(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateConnectedContentParams,
) -> ConnectedContentResponse:
    """
    Create a new connected content relationship in the m2m_connected_content table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the connected content relationship

    Returns:
        Response containing the result of the connection creation
    """
    logger.info(f"Creating connected content relationship for topic: {params.topic}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/m2m_connected_content"
    
    # Prepare request body
    body = {
        "topic": params.topic,
        "content_type": params.content_type,
        "order": params.order,
        "sys_domain": params.sys_domain,
        "sys_domain_path": params.sys_domain_path,
    }
    
    # Add optional content references (exactly one should be provided)
    if params.catalog_item:
        body["catalog_item"] = params.catalog_item
    if params.knowledge:
        body["knowledge"] = params.knowledge
    if params.quick_link:
        body["quick_link"] = params.quick_link
    
    # Add optional fields
    if params.popularity is not None:
        body["popularity"] = params.popularity
    if params.content_display_value:
        body["content_display_value"] = params.content_display_value
    if params.alphabetical_order is not None:
        body["alphabetical_order"] = params.alphabetical_order
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        connection = result.get("result", {})
        
        # Format the response
        formatted_connection = {
            "sys_id": connection.get("sys_id", ""),
            "topic": connection.get("topic", ""),
            "content_type": connection.get("content_type", ""),
            "catalog_item": connection.get("catalog_item", ""),
            "knowledge": connection.get("knowledge", ""),
            "quick_link": connection.get("quick_link", ""),
            "order": connection.get("order", ""),
            "popularity": connection.get("popularity", ""),
            "content_display_value": connection.get("content_display_value", ""),
            "alphabetical_order": connection.get("alphabetical_order", ""),
            "sys_domain": connection.get("sys_domain", ""),
            "sys_domain_path": connection.get("sys_domain_path", ""),
            "sys_created_on": connection.get("sys_created_on", ""),
            "sys_updated_on": connection.get("sys_updated_on", ""),
        }
        
        return ConnectedContentResponse(
            success=True,
            message=f"Created connected content relationship for topic: {params.topic}",
            data=formatted_connection,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating connected content: {str(e)}")
        return ConnectedContentResponse(
            success=False,
            message=f"Error creating connected content: {str(e)}",
            data=None,
        )


def update_connected_content(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateConnectedContentParams,
) -> ConnectedContentResponse:
    """
    Update an existing connected content relationship in the m2m_connected_content table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the connected content relationship

    Returns:
        Response containing the result of the connection update
    """
    logger.info(f"Updating connected content relationship: {params.connection_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/m2m_connected_content/{params.connection_id}"
    
    # Prepare request body with only provided fields
    body = {}
    
    if params.order is not None:
        body["order"] = params.order
    if params.popularity is not None:
        body["popularity"] = params.popularity
    if params.content_display_value is not None:
        body["content_display_value"] = params.content_display_value
    if params.alphabetical_order is not None:
        body["alphabetical_order"] = params.alphabetical_order
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        connection = result.get("result", {})
        
        # Format the response
        formatted_connection = {
            "sys_id": connection.get("sys_id", ""),
            "topic": connection.get("topic", ""),
            "content_type": connection.get("content_type", ""),
            "catalog_item": connection.get("catalog_item", ""),
            "knowledge": connection.get("knowledge", ""),
            "quick_link": connection.get("quick_link", ""),
            "order": connection.get("order", ""),
            "popularity": connection.get("popularity", ""),
            "content_display_value": connection.get("content_display_value", ""),
            "alphabetical_order": connection.get("alphabetical_order", ""),
            "sys_domain": connection.get("sys_domain", ""),
            "sys_domain_path": connection.get("sys_domain_path", ""),
            "sys_created_on": connection.get("sys_created_on", ""),
            "sys_updated_on": connection.get("sys_updated_on", ""),
        }
        
        return ConnectedContentResponse(
            success=True,
            message=f"Updated connected content relationship: {params.connection_id}",
            data=formatted_connection,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating connected content: {str(e)}")
        return ConnectedContentResponse(
            success=False,
            message=f"Error updating connected content: {str(e)}",
            data=None,
        )


def list_connected_content(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListConnectedContentParams,
) -> Dict[str, Any]:
    """
    List connected content relationships from the m2m_connected_content table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing connected content

    Returns:
        Dictionary containing connections and metadata
    """
    logger.info("Listing connected content relationships")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/m2m_connected_content"
    
    # Prepare query parameters
    query_parts = []
    
    if params.topic:
        query_parts.append(f"topic={params.topic}")
    
    if params.content_type:
        query_parts.append(f"content_type={params.content_type}")
    
    if params.catalog_item:
        query_parts.append(f"catalog_item={params.catalog_item}")
    
    if params.knowledge:
        query_parts.append(f"knowledge={params.knowledge}")
    
    if params.quick_link:
        query_parts.append(f"quick_link={params.quick_link}")
    
    if params.sys_domain:
        query_parts.append(f"sys_domain={params.sys_domain}")
    
    if params.query:
        query_parts.append(params.query)
    
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,topic,content_type,catalog_item,knowledge,quick_link,order,popularity,content_display_value,alphabetical_order,sys_domain,sys_domain_path,sys_created_on,sys_updated_on",
    }
    
    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        connections = result.get("result", [])
        
        # Format the response
        formatted_connections = []
        for connection in connections:
            formatted_connections.append({
                "sys_id": connection.get("sys_id", ""),
                "topic": connection.get("topic", ""),
                "content_type": connection.get("content_type", ""),
                "catalog_item": connection.get("catalog_item", ""),
                "knowledge": connection.get("knowledge", ""),
                "quick_link": connection.get("quick_link", ""),
                "order": connection.get("order", ""),
                "popularity": connection.get("popularity", ""),
                "content_display_value": connection.get("content_display_value", ""),
                "alphabetical_order": connection.get("alphabetical_order", ""),
                "sys_domain": connection.get("sys_domain", ""),
                "sys_domain_path": connection.get("sys_domain_path", ""),
                "sys_created_on": connection.get("sys_created_on", ""),
                "sys_updated_on": connection.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_connections)} connected content relationships",
            "connections": formatted_connections,
            "total": len(formatted_connections),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing connected content: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing connected content: {str(e)}",
            "connections": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_connected_content(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetConnectedContentParams,
) -> ConnectedContentResponse:
    """
    Get a specific connected content relationship from the m2m_connected_content table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the connected content relationship

    Returns:
        Response containing the connection data
    """
    logger.info(f"Getting connected content relationship: {params.connection_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/m2m_connected_content/{params.connection_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,topic,content_type,catalog_item,knowledge,quick_link,order,popularity,content_display_value,alphabetical_order,sys_domain,sys_domain_path,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        connection = result.get("result", {})
        
        # Format the response
        formatted_connection = {
            "sys_id": connection.get("sys_id", ""),
            "topic": connection.get("topic", ""),
            "content_type": connection.get("content_type", ""),
            "catalog_item": connection.get("catalog_item", ""),
            "knowledge": connection.get("knowledge", ""),
            "quick_link": connection.get("quick_link", ""),
            "order": connection.get("order", ""),
            "popularity": connection.get("popularity", ""),
            "content_display_value": connection.get("content_display_value", ""),
            "alphabetical_order": connection.get("alphabetical_order", ""),
            "sys_domain": connection.get("sys_domain", ""),
            "sys_domain_path": connection.get("sys_domain_path", ""),
            "sys_created_on": connection.get("sys_created_on", ""),
            "sys_updated_on": connection.get("sys_updated_on", ""),
        }
        
        return ConnectedContentResponse(
            success=True,
            message=f"Retrieved connected content relationship: {params.connection_id}",
            data=formatted_connection,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting connected content: {str(e)}")
        return ConnectedContentResponse(
            success=False,
            message=f"Error getting connected content: {str(e)}",
            data=None,
        )


def delete_connected_content(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteConnectedContentParams,
) -> ConnectedContentResponse:
    """
    Delete a connected content relationship from the m2m_connected_content table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the connected content relationship

    Returns:
        Response containing the result of the connection deletion
    """
    logger.info(f"Deleting connected content relationship: {params.connection_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/m2m_connected_content/{params.connection_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return ConnectedContentResponse(
            success=True,
            message=f"Deleted connected content relationship: {params.connection_id}",
            data={"deleted_connection_id": params.connection_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting connected content: {str(e)}")
        return ConnectedContentResponse(
            success=False,
            message=f"Error deleting connected content: {str(e)}",
            data=None,
        )


def bulk_connect_content(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkConnectContentParams,
) -> ConnectedContentResponse:
    """
    Bulk connect multiple content items to a topic in the m2m_connected_content table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for bulk connecting content

    Returns:
        Response containing the result of the bulk connections
    """
    logger.info(f"Bulk connecting {len(params.connections)} content items to topic: {params.topic}")
    
    successful_connections = []
    failed_connections = []
    
    for connection_def in params.connections:
        try:
            # Create individual connection parameters
            create_params = CreateConnectedContentParams(
                topic=params.topic,
                content_type=connection_def.get("content_type"),
                catalog_item=connection_def.get("catalog_item"),
                knowledge=connection_def.get("knowledge"),
                quick_link=connection_def.get("quick_link"),
                order=connection_def.get("order", 100),
                popularity=connection_def.get("popularity"),
                content_display_value=connection_def.get("content_display_value"),
                alphabetical_order=connection_def.get("alphabetical_order"),
                sys_domain=connection_def.get("sys_domain", "global"),
                sys_domain_path=connection_def.get("sys_domain_path", "/"),
            )
            
            # Create the connection
            result = create_connected_content(config, auth_manager, create_params)
            
            if result.success:
                successful_connections.append(result.data)
            else:
                failed_connections.append({
                    "connection": connection_def,
                    "error": result.message
                })
                
        except Exception as e:
            failed_connections.append({
                "connection": connection_def,
                "error": str(e)
            })
    
    success_count = len(successful_connections)
    failure_count = len(failed_connections)
    
    if failure_count == 0:
        return ConnectedContentResponse(
            success=True,
            message=f"Successfully connected {success_count} content items to topic",
            data={
                "successful_connections": successful_connections,
                "success_count": success_count,
                "failure_count": failure_count
            },
        )
    elif success_count == 0:
        return ConnectedContentResponse(
            success=False,
            message=f"Failed to connect all {failure_count} content items",
            data={
                "failed_connections": failed_connections,
                "success_count": success_count,
                "failure_count": failure_count
            },
        )
    else:
        return ConnectedContentResponse(
            success=True,
            message=f"Partially successful: {success_count} succeeded, {failure_count} failed",
            data={
                "successful_connections": successful_connections,
                "failed_connections": failed_connections,
                "success_count": success_count,
                "failure_count": failure_count
            },
        )