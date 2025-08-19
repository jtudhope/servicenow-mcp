"""
Topic tools for the ServiceNow MCP server.

This module provides tools for managing Topics that are stored in the topic table.
In ServiceNow, the topic table stores knowledge or community "topic" definitions — 
essentially labels or categories you can attach to content to make it easier to find, 
filter, and organize.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateTopicParams(BaseModel):
    """Parameters for creating a topic."""

    name: str = Field(..., description="Name of the topic (required)")
    taxonomy: str = Field(..., description="Taxonomy sys_id that this topic belongs to (required)")
    description: Optional[str] = Field(None, description="Description of the topic")
    parent_topic: Optional[str] = Field(None, description="Parent topic sys_id for hierarchical structure")
    order: Optional[int] = Field(None, description="Display order within the taxonomy")
    active: Optional[bool] = Field(True, description="Whether the topic is active")
    topic_based_navigation: Optional[bool] = Field(False, description="Enable topic-based navigation")
    icon_url: Optional[str] = Field(None, description="URL for the topic icon")
    banner_image_url: Optional[str] = Field(None, description="URL for the topic banner image")
    topic_manager: Optional[str] = Field(None, description="Comma-separated list of user criteria sys_ids for topic managers")
    topic_contributor: Optional[str] = Field(None, description="Comma-separated list of user criteria sys_ids for topic contributors")
    available_for: Optional[str] = Field(None, description="Comma-separated list of user criteria sys_ids for who can see this topic")
    not_available_for: Optional[str] = Field(None, description="Comma-separated list of user criteria sys_ids for who cannot see this topic")
    enable_user_criteria_check: Optional[bool] = Field(False, description="Enable user criteria checking for visibility")
    template: Optional[str] = Field(None, description="Service Portal page template sys_id")
    apply_to_child_topics: Optional[bool] = Field(False, description="Apply template settings to child topics")


class UpdateTopicParams(BaseModel):
    """Parameters for updating a topic."""

    topic_id: str = Field(..., description="Topic sys_id")
    name: Optional[str] = Field(None, description="Updated name of the topic")
    description: Optional[str] = Field(None, description="Updated description")
    parent_topic: Optional[str] = Field(None, description="Updated parent topic sys_id")
    order: Optional[int] = Field(None, description="Updated display order")
    active: Optional[bool] = Field(None, description="Updated active status")
    topic_based_navigation: Optional[bool] = Field(None, description="Updated topic-based navigation setting")
    icon_url: Optional[str] = Field(None, description="Updated icon URL")
    banner_image_url: Optional[str] = Field(None, description="Updated banner image URL")
    topic_manager: Optional[str] = Field(None, description="Updated topic managers")
    topic_contributor: Optional[str] = Field(None, description="Updated topic contributors")
    available_for: Optional[str] = Field(None, description="Updated available for criteria")
    not_available_for: Optional[str] = Field(None, description="Updated not available for criteria")
    enable_user_criteria_check: Optional[bool] = Field(None, description="Updated user criteria check setting")
    template: Optional[str] = Field(None, description="Updated template")
    apply_to_child_topics: Optional[bool] = Field(None, description="Updated apply to child topics setting")


class ListTopicsParams(BaseModel):
    """Parameters for listing topics."""

    limit: int = Field(10, description="Maximum number of topics to return")
    offset: int = Field(0, description="Offset for pagination")
    taxonomy: Optional[str] = Field(None, description="Filter by taxonomy sys_id")
    parent_topic: Optional[str] = Field(None, description="Filter by parent topic sys_id")
    active: Optional[bool] = Field(None, description="Filter by active status")
    name_contains: Optional[str] = Field(None, description="Filter by name containing text")
    topic_based_navigation: Optional[bool] = Field(None, description="Filter by topic-based navigation setting")
    query: Optional[str] = Field(None, description="Additional query string")


class GetTopicParams(BaseModel):
    """Parameters for getting a topic."""

    topic_id: str = Field(..., description="Topic sys_id or name")


class DeleteTopicParams(BaseModel):
    """Parameters for deleting a topic."""

    topic_id: str = Field(..., description="Topic sys_id")


class CloneTopicParams(BaseModel):
    """Parameters for cloning a topic."""

    topic_id: str = Field(..., description="Source topic sys_id")
    new_name: str = Field(..., description="Name for the cloned topic")
    new_description: Optional[str] = Field(None, description="Description for the cloned topic")
    new_taxonomy: Optional[str] = Field(None, description="Taxonomy for the cloned topic (defaults to source taxonomy)")


class TopicResponse(BaseModel):
    """Response from topic operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_topic(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateTopicParams,
) -> TopicResponse:
    """
    Create a new topic in the topic table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the topic

    Returns:
        Response containing the result of the topic creation
    """
    logger.info(f"Creating topic: {params.name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/topic"
    
    # Prepare request body
    body = {
        "name": params.name,
        "taxonomy": params.taxonomy,
        "active": params.active,
        "topic_based_navigation": params.topic_based_navigation,
        "enable_user_criteria_check": params.enable_user_criteria_check,
        "apply_to_child_topics": params.apply_to_child_topics,
    }
    
    # Add optional fields
    if params.description:
        body["description"] = params.description
    if params.parent_topic:
        body["parent_topic"] = params.parent_topic
    if params.order is not None:
        body["order"] = params.order
    if params.icon_url:
        body["icon_url"] = params.icon_url
    if params.banner_image_url:
        body["banner_image_url"] = params.banner_image_url
    if params.topic_manager:
        body["topic_manager"] = params.topic_manager
    if params.topic_contributor:
        body["topic_contributor"] = params.topic_contributor
    if params.available_for:
        body["available_for"] = params.available_for
    if params.not_available_for:
        body["not_available_for"] = params.not_available_for
    if params.template:
        body["template"] = params.template
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        topic = result.get("result", {})
        
        # Format the response
        formatted_topic = {
            "sys_id": topic.get("sys_id", ""),
            "name": topic.get("name", ""),
            "description": topic.get("description", ""),
            "taxonomy": topic.get("taxonomy", ""),
            "parent_topic": topic.get("parent_topic", ""),
            "topic_path": topic.get("topic_path", ""),
            "order": topic.get("order", ""),
            "active": topic.get("active", ""),
            "topic_based_navigation": topic.get("topic_based_navigation", ""),
            "icon_url": topic.get("icon_url", ""),
            "banner_image_url": topic.get("banner_image_url", ""),
            "topic_manager": topic.get("topic_manager", ""),
            "topic_contributor": topic.get("topic_contributor", ""),
            "available_for": topic.get("available_for", ""),
            "not_available_for": topic.get("not_available_for", ""),
            "enable_user_criteria_check": topic.get("enable_user_criteria_check", ""),
            "template": topic.get("template", ""),
            "apply_to_child_topics": topic.get("apply_to_child_topics", ""),
            "sys_created_on": topic.get("sys_created_on", ""),
            "sys_updated_on": topic.get("sys_updated_on", ""),
        }
        
        return TopicResponse(
            success=True,
            message=f"Created topic: {params.name}",
            data=formatted_topic,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating topic: {str(e)}")
        return TopicResponse(
            success=False,
            message=f"Error creating topic: {str(e)}",
            data=None,
        )


def update_topic(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateTopicParams,
) -> TopicResponse:
    """
    Update an existing topic in the topic table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the topic

    Returns:
        Response containing the result of the topic update
    """
    logger.info(f"Updating topic: {params.topic_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/topic/{params.topic_id}"
    
    # Prepare request body with only provided fields
    body = {}
    
    if params.name is not None:
        body["name"] = params.name
    if params.description is not None:
        body["description"] = params.description
    if params.parent_topic is not None:
        body["parent_topic"] = params.parent_topic
    if params.order is not None:
        body["order"] = params.order
    if params.active is not None:
        body["active"] = params.active
    if params.topic_based_navigation is not None:
        body["topic_based_navigation"] = params.topic_based_navigation
    if params.icon_url is not None:
        body["icon_url"] = params.icon_url
    if params.banner_image_url is not None:
        body["banner_image_url"] = params.banner_image_url
    if params.topic_manager is not None:
        body["topic_manager"] = params.topic_manager
    if params.topic_contributor is not None:
        body["topic_contributor"] = params.topic_contributor
    if params.available_for is not None:
        body["available_for"] = params.available_for
    if params.not_available_for is not None:
        body["not_available_for"] = params.not_available_for
    if params.enable_user_criteria_check is not None:
        body["enable_user_criteria_check"] = params.enable_user_criteria_check
    if params.template is not None:
        body["template"] = params.template
    if params.apply_to_child_topics is not None:
        body["apply_to_child_topics"] = params.apply_to_child_topics
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        topic = result.get("result", {})
        
        # Format the response
        formatted_topic = {
            "sys_id": topic.get("sys_id", ""),
            "name": topic.get("name", ""),
            "description": topic.get("description", ""),
            "taxonomy": topic.get("taxonomy", ""),
            "parent_topic": topic.get("parent_topic", ""),
            "topic_path": topic.get("topic_path", ""),
            "order": topic.get("order", ""),
            "active": topic.get("active", ""),
            "topic_based_navigation": topic.get("topic_based_navigation", ""),
            "icon_url": topic.get("icon_url", ""),
            "banner_image_url": topic.get("banner_image_url", ""),
            "topic_manager": topic.get("topic_manager", ""),
            "topic_contributor": topic.get("topic_contributor", ""),
            "available_for": topic.get("available_for", ""),
            "not_available_for": topic.get("not_available_for", ""),
            "enable_user_criteria_check": topic.get("enable_user_criteria_check", ""),
            "template": topic.get("template", ""),
            "apply_to_child_topics": topic.get("apply_to_child_topics", ""),
            "sys_created_on": topic.get("sys_created_on", ""),
            "sys_updated_on": topic.get("sys_updated_on", ""),
        }
        
        return TopicResponse(
            success=True,
            message=f"Updated topic: {params.topic_id}",
            data=formatted_topic,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating topic: {str(e)}")
        return TopicResponse(
            success=False,
            message=f"Error updating topic: {str(e)}",
            data=None,
        )


def list_topics(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListTopicsParams,
) -> Dict[str, Any]:
    """
    List topics from the topic table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing topics

    Returns:
        Dictionary containing topics and metadata
    """
    logger.info("Listing topics")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/topic"
    
    # Prepare query parameters
    query_parts = []
    
    if params.taxonomy:
        query_parts.append(f"taxonomy={params.taxonomy}")
    
    if params.parent_topic:
        query_parts.append(f"parent_topic={params.parent_topic}")
    
    if params.active is not None:
        query_parts.append(f"active={params.active}")
    
    if params.name_contains:
        query_parts.append(f"nameLIKE{params.name_contains}")
    
    if params.topic_based_navigation is not None:
        query_parts.append(f"topic_based_navigation={params.topic_based_navigation}")
    
    if params.query:
        query_parts.append(params.query)
    
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,description,taxonomy,parent_topic,topic_path,order,active,topic_based_navigation,icon_url,banner_image_url,topic_manager,topic_contributor,available_for,not_available_for,enable_user_criteria_check,template,apply_to_child_topics,sys_created_on,sys_updated_on",
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
        topics = result.get("result", [])
        
        # Format the response
        formatted_topics = []
        for topic in topics:
            formatted_topics.append({
                "sys_id": topic.get("sys_id", ""),
                "name": topic.get("name", ""),
                "description": topic.get("description", ""),
                "taxonomy": topic.get("taxonomy", ""),
                "parent_topic": topic.get("parent_topic", ""),
                "topic_path": topic.get("topic_path", ""),
                "order": topic.get("order", ""),
                "active": topic.get("active", ""),
                "topic_based_navigation": topic.get("topic_based_navigation", ""),
                "icon_url": topic.get("icon_url", ""),
                "banner_image_url": topic.get("banner_image_url", ""),
                "topic_manager": topic.get("topic_manager", ""),
                "topic_contributor": topic.get("topic_contributor", ""),
                "available_for": topic.get("available_for", ""),
                "not_available_for": topic.get("not_available_for", ""),
                "enable_user_criteria_check": topic.get("enable_user_criteria_check", ""),
                "template": topic.get("template", ""),
                "apply_to_child_topics": topic.get("apply_to_child_topics", ""),
                "sys_created_on": topic.get("sys_created_on", ""),
                "sys_updated_on": topic.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_topics)} topics",
            "topics": formatted_topics,
            "total": len(formatted_topics),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing topics: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing topics: {str(e)}",
            "topics": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_topic(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetTopicParams,
) -> TopicResponse:
    """
    Get a specific topic from the topic table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the topic

    Returns:
        Response containing the topic data
    """
    logger.info(f"Getting topic: {params.topic_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/topic/{params.topic_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,description,taxonomy,parent_topic,topic_path,order,active,topic_based_navigation,icon_url,banner_image_url,topic_manager,topic_contributor,available_for,not_available_for,enable_user_criteria_check,template,apply_to_child_topics,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        topic = result.get("result", {})
        
        # Format the response
        formatted_topic = {
            "sys_id": topic.get("sys_id", ""),
            "name": topic.get("name", ""),
            "description": topic.get("description", ""),
            "taxonomy": topic.get("taxonomy", ""),
            "parent_topic": topic.get("parent_topic", ""),
            "topic_path": topic.get("topic_path", ""),
            "order": topic.get("order", ""),
            "active": topic.get("active", ""),
            "topic_based_navigation": topic.get("topic_based_navigation", ""),
            "icon_url": topic.get("icon_url", ""),
            "banner_image_url": topic.get("banner_image_url", ""),
            "topic_manager": topic.get("topic_manager", ""),
            "topic_contributor": topic.get("topic_contributor", ""),
            "available_for": topic.get("available_for", ""),
            "not_available_for": topic.get("not_available_for", ""),
            "enable_user_criteria_check": topic.get("enable_user_criteria_check", ""),
            "template": topic.get("template", ""),
            "apply_to_child_topics": topic.get("apply_to_child_topics", ""),
            "sys_created_on": topic.get("sys_created_on", ""),
            "sys_updated_on": topic.get("sys_updated_on", ""),
        }
        
        return TopicResponse(
            success=True,
            message=f"Retrieved topic: {params.topic_id}",
            data=formatted_topic,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting topic: {str(e)}")
        return TopicResponse(
            success=False,
            message=f"Error getting topic: {str(e)}",
            data=None,
        )


def delete_topic(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteTopicParams,
) -> TopicResponse:
    """
    Delete a topic from the topic table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the topic

    Returns:
        Response containing the result of the topic deletion
    """
    logger.info(f"Deleting topic: {params.topic_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/topic/{params.topic_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return TopicResponse(
            success=True,
            message=f"Deleted topic: {params.topic_id}",
            data={"deleted_topic_id": params.topic_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting topic: {str(e)}")
        return TopicResponse(
            success=False,
            message=f"Error deleting topic: {str(e)}",
            data=None,
        )


def clone_topic(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CloneTopicParams,
) -> TopicResponse:
    """
    Clone an existing topic in the topic table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for cloning the topic

    Returns:
        Response containing the result of the topic cloning
    """
    logger.info(f"Cloning topic: {params.topic_id}")
    
    try:
        # First, get the source topic
        get_params = GetTopicParams(topic_id=params.topic_id)
        source_result = get_topic(config, auth_manager, get_params)
        
        if not source_result.success:
            return TopicResponse(
                success=False,
                message=f"Failed to retrieve source topic: {source_result.message}",
                data=None,
            )
        
        source_topic = source_result.data
        
        # Create the clone with new name
        create_params = CreateTopicParams(
            name=params.new_name,
            taxonomy=params.new_taxonomy or source_topic.get("taxonomy"),
            description=params.new_description or source_topic.get("description"),
            parent_topic=source_topic.get("parent_topic"),
            order=source_topic.get("order"),
            active=source_topic.get("active", True),
            topic_based_navigation=source_topic.get("topic_based_navigation", False),
            icon_url=source_topic.get("icon_url"),
            banner_image_url=source_topic.get("banner_image_url"),
            topic_manager=source_topic.get("topic_manager"),
            topic_contributor=source_topic.get("topic_contributor"),
            available_for=source_topic.get("available_for"),
            not_available_for=source_topic.get("not_available_for"),
            enable_user_criteria_check=source_topic.get("enable_user_criteria_check", False),
            template=source_topic.get("template"),
            apply_to_child_topics=source_topic.get("apply_to_child_topics", False),
        )
        
        return create_topic(config, auth_manager, create_params)
    
    except Exception as e:
        logger.error(f"Error cloning topic: {str(e)}")
        return TopicResponse(
            success=False,
            message=f"Error cloning topic: {str(e)}",
            data=None,
        )