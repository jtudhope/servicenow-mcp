"""
Service Catalog tools for the ServiceNow MCP server.

This module provides tools for querying and viewing the service catalog in ServiceNow.
"""

import logging
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class ListCatalogItemsParams(BaseModel):
    """Parameters for listing service catalog items."""
    
    limit: int = Field(10, description="Maximum number of catalog items to return")
    offset: int = Field(0, description="Offset for pagination")
    category: Optional[str] = Field(None, description="Filter by category")
    query: Optional[str] = Field(None, description="Search query for catalog items")
    active: bool = Field(True, description="Whether to only return active catalog items")


class GetCatalogItemParams(BaseModel):
    """Parameters for getting a specific service catalog item."""
    
    item_id: str = Field(..., description="Catalog item ID or sys_id")


class ListCatalogCategoriesParams(BaseModel):
    """Parameters for listing service catalog categories."""
    
    limit: int = Field(10, description="Maximum number of categories to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Search query for categories")
    active: bool = Field(True, description="Whether to only return active categories")


class CatalogResponse(BaseModel):
    """Response from catalog operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


class CreateCatalogCategoryParams(BaseModel):
    """Parameters for creating a new service catalog category."""
    
    title: str = Field(..., description="Title of the category")
    description: Optional[str] = Field(None, description="Description of the category")
    parent: Optional[str] = Field(None, description="Parent category sys_id")
    icon: Optional[str] = Field(None, description="Icon for the category")
    active: bool = Field(True, description="Whether the category is active")
    order: Optional[int] = Field(None, description="Order of the category")
    sc_catalog: Optional[str] = Field(None, description="Catalog sys_id this category belongs to")


class UpdateCatalogCategoryParams(BaseModel):
    """Parameters for updating a service catalog category."""
    
    category_id: str = Field(..., description="Category ID or sys_id")
    title: Optional[str] = Field(None, description="Title of the category")
    description: Optional[str] = Field(None, description="Description of the category")
    parent: Optional[str] = Field(None, description="Parent category sys_id")
    icon: Optional[str] = Field(None, description="Icon for the category")
    active: Optional[bool] = Field(None, description="Whether the category is active")
    order: Optional[int] = Field(None, description="Order of the category")
    sc_catalog: Optional[str] = Field(None, description="Catalog sys_id this category belongs to")


class MoveCatalogItemsParams(BaseModel):
    """Parameters for moving catalog items between categories."""
    
    item_ids: List[str] = Field(..., description="List of catalog item IDs to move")
    target_category_id: str = Field(..., description="Target category ID to move items to")


class CreateCatalogItemParams(BaseModel):
    """Parameters for creating a new service catalog item."""
    
    name: str = Field(..., description="Name of the catalog item")
    short_description: str = Field(..., description="Short description of the catalog item")
    description: Optional[str] = Field(None, description="Detailed description of the catalog item")
    category: str = Field(..., description="Category sys_id for the catalog item")
    sc_catalogs: Optional[str] = Field(None, description="Catalog sys_id this item belongs to")
    active: bool = Field(True, description="Whether the catalog item is active")
    order: Optional[int] = Field(None, description="Display order of the catalog item")
    price: Optional[str] = Field(None, description="Price of the catalog item")
    list_price: Optional[str] = Field(None, description="List price of the catalog item")
    cost: Optional[str] = Field(None, description="Cost of the catalog item")
    recurring_price: Optional[str] = Field(None, description="Recurring price of the catalog item")
    recurring_frequency: Optional[str] = Field(None, description="Recurring frequency")
    billable: Optional[bool] = Field(None, description="Whether the item is billable")
    picture: Optional[str] = Field(None, description="Picture for the catalog item")
    icon: Optional[str] = Field(None, description="Icon for the catalog item")
    image: Optional[str] = Field(None, description="Image for the catalog item")
    mobile_picture: Optional[str] = Field(None, description="Mobile picture for the catalog item")
    group: Optional[str] = Field(None, description="Fulfillment group sys_id")
    workflow: Optional[str] = Field(None, description="Workflow sys_id")
    delivery_plan: Optional[str] = Field(None, description="Delivery plan sys_id")
    delivery_time: Optional[str] = Field(None, description="Delivery time")
    roles: Optional[str] = Field(None, description="Required roles")
    access_type: Optional[str] = Field(None, description="Access type (restricted, public, etc.)")
    availability: Optional[str] = Field(None, description="Availability setting")
    hide_sp: Optional[bool] = Field(None, description="Hide on Service Portal")
    no_cart: Optional[bool] = Field(None, description="Hide cart functionality")
    no_order: Optional[bool] = Field(None, description="Hide order functionality") 
    no_search: Optional[bool] = Field(None, description="Hide from search")
    location: Optional[str] = Field(None, description="Location sys_id")
    model: Optional[str] = Field(None, description="Model sys_id")
    vendor: Optional[str] = Field(None, description="Vendor sys_id")
    entitlement_script: Optional[str] = Field(None, description="Entitlement script")
    fulfillment_automation_level: Optional[str] = Field(None, description="Fulfillment automation level")
    no_wishlist_v2: Optional[bool] = Field(None, description="Hide 'Add to Wish List'")
    no_cart_v2: Optional[bool] = Field(None, description="Hide 'Add to Cart'")
    no_delivery_time_v2: Optional[bool] = Field(None, description="Hide Delivery time")
    no_attachment_v2: Optional[bool] = Field(None, description="Hide Attachment")
    no_save_as_draft: Optional[bool] = Field(None, description="Hide 'Save as Draft'")
    no_quantity_v2: Optional[bool] = Field(None, description="Hide Quantity")
    request_method: Optional[str] = Field(None, description="Request method")
    mandatory_attachment: Optional[bool] = Field(None, description="Mandatory Attachment")
    show_variable_help_on_load: Optional[bool] = Field(None, description="Expand help for all questions")
    make_item_non_conversational: Optional[bool] = Field(None, description="Make the item non-conversational in VA")
    taxonomy_topic: Optional[str] = Field(None, description="Taxonomy topic sys_id")
    sc_template: Optional[str] = Field(None, description="Associated template sys_id")


class UpdateCatalogItemParams(BaseModel):
    """Parameters for updating an existing service catalog item."""
    
    item_id: str = Field(..., description="Catalog item ID or sys_id")
    name: Optional[str] = Field(None, description="Name of the catalog item")
    short_description: Optional[str] = Field(None, description="Short description of the catalog item")
    description: Optional[str] = Field(None, description="Detailed description of the catalog item")
    category: Optional[str] = Field(None, description="Category sys_id for the catalog item")
    sc_catalogs: Optional[str] = Field(None, description="Catalog sys_id this item belongs to")
    active: Optional[bool] = Field(None, description="Whether the catalog item is active")
    order: Optional[int] = Field(None, description="Display order of the catalog item")
    price: Optional[str] = Field(None, description="Price of the catalog item")
    list_price: Optional[str] = Field(None, description="List price of the catalog item")
    cost: Optional[str] = Field(None, description="Cost of the catalog item")
    recurring_price: Optional[str] = Field(None, description="Recurring price of the catalog item")
    recurring_frequency: Optional[str] = Field(None, description="Recurring frequency")
    billable: Optional[bool] = Field(None, description="Whether the item is billable")
    picture: Optional[str] = Field(None, description="Picture for the catalog item")
    icon: Optional[str] = Field(None, description="Icon for the catalog item")
    image: Optional[str] = Field(None, description="Image for the catalog item")
    mobile_picture: Optional[str] = Field(None, description="Mobile picture for the catalog item")
    group: Optional[str] = Field(None, description="Fulfillment group sys_id")
    workflow: Optional[str] = Field(None, description="Workflow sys_id")
    delivery_plan: Optional[str] = Field(None, description="Delivery plan sys_id")
    delivery_time: Optional[str] = Field(None, description="Delivery time")
    roles: Optional[str] = Field(None, description="Required roles")
    access_type: Optional[str] = Field(None, description="Access type (restricted, public, etc.)")
    availability: Optional[str] = Field(None, description="Availability setting")
    hide_sp: Optional[bool] = Field(None, description="Hide on Service Portal")
    no_cart: Optional[bool] = Field(None, description="Hide cart functionality")
    no_order: Optional[bool] = Field(None, description="Hide order functionality") 
    no_search: Optional[bool] = Field(None, description="Hide from search")
    location: Optional[str] = Field(None, description="Location sys_id")
    model: Optional[str] = Field(None, description="Model sys_id")
    vendor: Optional[str] = Field(None, description="Vendor sys_id")
    entitlement_script: Optional[str] = Field(None, description="Entitlement script")
    fulfillment_automation_level: Optional[str] = Field(None, description="Fulfillment automation level")
    no_wishlist_v2: Optional[bool] = Field(None, description="Hide 'Add to Wish List'")
    no_cart_v2: Optional[bool] = Field(None, description="Hide 'Add to Cart'")
    no_delivery_time_v2: Optional[bool] = Field(None, description="Hide Delivery time")
    no_attachment_v2: Optional[bool] = Field(None, description="Hide Attachment")
    no_save_as_draft: Optional[bool] = Field(None, description="Hide 'Save as Draft'")
    no_quantity_v2: Optional[bool] = Field(None, description="Hide Quantity")
    request_method: Optional[str] = Field(None, description="Request method")
    mandatory_attachment: Optional[bool] = Field(None, description="Mandatory Attachment")
    show_variable_help_on_load: Optional[bool] = Field(None, description="Expand help for all questions")
    make_item_non_conversational: Optional[bool] = Field(None, description="Make the item non-conversational in VA")
    taxonomy_topic: Optional[str] = Field(None, description="Taxonomy topic sys_id")
    sc_template: Optional[str] = Field(None, description="Associated template sys_id")


class DeleteCatalogItemParams(BaseModel):
    """Parameters for deleting a service catalog item."""
    
    item_id: str = Field(..., description="Catalog item ID or sys_id")


def list_catalog_items(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListCatalogItemsParams,
) -> Dict[str, Any]:
    """
    List service catalog items from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing catalog items

    Returns:
        Dictionary containing catalog items and metadata
    """
    logger.info("Listing service catalog items")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Add filters
    filters = []
    if params.active:
        filters.append("active=true")
    if params.category:
        filters.append(f"category={params.category}")
    if params.query:
        filters.append(f"short_descriptionLIKE{params.query}^ORnameLIKE{params.query}")
    
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
        items = result.get("result", [])
        
        # Format the response
        formatted_items = []
        for item in items:
            formatted_items.append({
                "sys_id": item.get("sys_id", ""),
                "name": item.get("name", ""),
                "short_description": item.get("short_description", ""),
                "category": item.get("category", ""),
                "price": item.get("price", ""),
                "picture": item.get("picture", ""),
                "active": item.get("active", ""),
                "order": item.get("order", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_items)} catalog items",
            "items": formatted_items,
            "total": len(formatted_items),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing catalog items: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing catalog items: {str(e)}",
            "items": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_catalog_item(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetCatalogItemParams,
) -> CatalogResponse:
    """
    Get a specific service catalog item from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting a catalog item

    Returns:
        Response containing the catalog item details
    """
    logger.info(f"Getting service catalog item: {params.item_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item/{params.item_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        item = result.get("result", {})
        
        if not item:
            return CatalogResponse(
                success=False,
                message=f"Catalog item not found: {params.item_id}",
                data=None,
            )
        
        # Format the response
        formatted_item = {
            "sys_id": item.get("sys_id", ""),
            "name": item.get("name", ""),
            "short_description": item.get("short_description", ""),
            "description": item.get("description", ""),
            "category": item.get("category", ""),
            "price": item.get("price", ""),
            "picture": item.get("picture", ""),
            "active": item.get("active", ""),
            "order": item.get("order", ""),
            "delivery_time": item.get("delivery_time", ""),
            "availability": item.get("availability", ""),
            "variables": get_catalog_item_variables(config, auth_manager, params.item_id),
        }
        
        return CatalogResponse(
            success=True,
            message=f"Retrieved catalog item: {item.get('name', '')}",
            data=formatted_item,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting catalog item: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error getting catalog item: {str(e)}",
            data=None,
        )


def get_catalog_item_variables(
    config: ServerConfig,
    auth_manager: AuthManager,
    item_id: str,
) -> List[Dict[str, Any]]:
    """
    Get variables for a specific service catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        item_id: Catalog item ID or sys_id

    Returns:
        List of variables for the catalog item
    """
    logger.info(f"Getting variables for catalog item: {item_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/item_option_new"
    
    # Prepare query parameters
    query_params = {
        "sysparm_query": f"cat_item={item_id}^ORDERBYorder",
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        variables = result.get("result", [])
        
        # Format the response
        formatted_variables = []
        for variable in variables:
            formatted_variables.append({
                "sys_id": variable.get("sys_id", ""),
                "name": variable.get("name", ""),
                "label": variable.get("question_text", ""),
                "type": variable.get("type", ""),
                "mandatory": variable.get("mandatory", ""),
                "default_value": variable.get("default_value", ""),
                "help_text": variable.get("help_text", ""),
                "order": variable.get("order", ""),
            })
        
        return formatted_variables
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting catalog item variables: {str(e)}")
        return []


def list_catalog_categories(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListCatalogCategoriesParams,
) -> Dict[str, Any]:
    """
    List service catalog categories from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing catalog categories

    Returns:
        Dictionary containing catalog categories and metadata
    """
    logger.info("Listing service catalog categories")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_category"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
    }
    
    # Add filters
    filters = []
    if params.active:
        filters.append("active=true")
    if params.query:
        filters.append(f"titleLIKE{params.query}^ORdescriptionLIKE{params.query}")
    
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
        categories = result.get("result", [])
        
        # Format the response
        formatted_categories = []
        for category in categories:
            formatted_categories.append({
                "sys_id": category.get("sys_id", ""),
                "title": category.get("title", ""),
                "description": category.get("description", ""),
                "parent": category.get("parent", ""),
                "icon": category.get("icon", ""),
                "active": category.get("active", ""),
                "order": category.get("order", ""),
                "sc_catalog": category.get("sc_catalog", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_categories)} catalog categories",
            "categories": formatted_categories,
            "total": len(formatted_categories),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing catalog categories: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing catalog categories: {str(e)}",
            "categories": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def create_catalog_category(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateCatalogCategoryParams,
) -> CatalogResponse:
    """
    Create a new service catalog category in ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating a catalog category

    Returns:
        Response containing the result of the operation
    """
    logger.info("Creating new service catalog category")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_category"
    
    # Prepare request body
    body = {
        "title": params.title,
    }
    
    if params.description is not None:
        body["description"] = params.description
    if params.parent is not None:
        body["parent"] = params.parent
    if params.icon is not None:
        body["icon"] = params.icon
    if params.active is not None:
        body["active"] = str(params.active).lower()
    if params.order is not None:
        body["order"] = str(params.order)
    if params.sc_catalog is not None:
        body["sc_catalog"] = params.sc_catalog
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        category = result.get("result", {})
        
        # Format the response
        formatted_category = {
            "sys_id": category.get("sys_id", ""),
            "title": category.get("title", ""),
            "description": category.get("description", ""),
            "parent": category.get("parent", ""),
            "icon": category.get("icon", ""),
            "active": category.get("active", ""),
            "order": category.get("order", ""),
            "sc_catalog": category.get("sc_catalog", ""),
        }
        
        return CatalogResponse(
            success=True,
            message=f"Created catalog category: {params.title}",
            data=formatted_category,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating catalog category: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error creating catalog category: {str(e)}",
            data=None,
        )


def update_catalog_category(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateCatalogCategoryParams,
) -> CatalogResponse:
    """
    Update an existing service catalog category in ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating a catalog category

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating service catalog category: {params.category_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_category/{params.category_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.title is not None:
        body["title"] = params.title
    if params.description is not None:
        body["description"] = params.description
    if params.parent is not None:
        body["parent"] = params.parent
    if params.icon is not None:
        body["icon"] = params.icon
    if params.active is not None:
        body["active"] = str(params.active).lower()
    if params.order is not None:
        body["order"] = str(params.order)
    if params.sc_catalog is not None:
        body["sc_catalog"] = params.sc_catalog
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        category = result.get("result", {})
        
        # Format the response
        formatted_category = {
            "sys_id": category.get("sys_id", ""),
            "title": category.get("title", ""),
            "description": category.get("description", ""),
            "parent": category.get("parent", ""),
            "icon": category.get("icon", ""),
            "active": category.get("active", ""),
            "order": category.get("order", ""),
            "sc_catalog": category.get("sc_catalog", ""),
        }
        
        return CatalogResponse(
            success=True,
            message=f"Updated catalog category: {params.category_id}",
            data=formatted_category,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating catalog category: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error updating catalog category: {str(e)}",
            data=None,
        )


def move_catalog_items(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: MoveCatalogItemsParams,
) -> CatalogResponse:
    """
    Move catalog items to a different category.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for moving catalog items

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Moving {len(params.item_ids)} catalog items to category: {params.target_category_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item"
    
    # Make the API request for each item
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    success_count = 0
    failed_items = []
    
    try:
        for item_id in params.item_ids:
            item_url = f"{url}/{item_id}"
            body = {
                "category": params.target_category_id
            }
            
            try:
                response = requests.patch(item_url, headers=headers, json=body)
                response.raise_for_status()
                success_count += 1
            except requests.exceptions.RequestException as e:
                logger.error(f"Error moving catalog item {item_id}: {str(e)}")
                failed_items.append({"item_id": item_id, "error": str(e)})
        
        # Prepare the response
        if success_count == len(params.item_ids):
            return CatalogResponse(
                success=True,
                message=f"Successfully moved {success_count} catalog items to category {params.target_category_id}",
                data={"moved_items_count": success_count},
            )
        elif success_count > 0:
            return CatalogResponse(
                success=True,
                message=f"Partially moved catalog items. {success_count} succeeded, {len(failed_items)} failed.",
                data={
                    "moved_items_count": success_count,
                    "failed_items": failed_items,
                },
            )
        else:
            return CatalogResponse(
                success=False,
                message="Failed to move any catalog items",
                data={"failed_items": failed_items},
            )
    
    except Exception as e:
        logger.error(f"Error moving catalog items: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error moving catalog items: {str(e)}",
            data=None,
        )


def create_catalog_item(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateCatalogItemParams,
) -> CatalogResponse:
    """
    Create a new service catalog item in ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating a catalog item

    Returns:
        Response containing the result of the operation
    """
    logger.info("Creating new service catalog item")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item"
    
    # Prepare request body with required parameters
    body = {
        "name": params.name,
        "short_description": params.short_description,
        "category": params.category,
    }
    
    # Add optional parameters if provided
    if params.description is not None:
        body["description"] = params.description
    if params.sc_catalogs is not None:
        body["sc_catalogs"] = params.sc_catalogs
    if params.active is not None:
        body["active"] = str(params.active).lower()
    if params.order is not None:
        body["order"] = str(params.order)
    if params.price is not None:
        body["price"] = params.price
    if params.list_price is not None:
        body["list_price"] = params.list_price
    if params.cost is not None:
        body["cost"] = params.cost
    if params.recurring_price is not None:
        body["recurring_price"] = params.recurring_price
    if params.recurring_frequency is not None:
        body["recurring_frequency"] = params.recurring_frequency
    if params.billable is not None:
        body["billable"] = str(params.billable).lower()
    if params.picture is not None:
        body["picture"] = params.picture
    if params.icon is not None:
        body["icon"] = params.icon
    if params.image is not None:
        body["image"] = params.image
    if params.mobile_picture is not None:
        body["mobile_picture"] = params.mobile_picture
    if params.group is not None:
        body["group"] = params.group
    if params.workflow is not None:
        body["workflow"] = params.workflow
    if params.delivery_plan is not None:
        body["delivery_plan"] = params.delivery_plan
    if params.delivery_time is not None:
        body["delivery_time"] = params.delivery_time
    if params.roles is not None:
        body["roles"] = params.roles
    if params.access_type is not None:
        body["access_type"] = params.access_type
    if params.availability is not None:
        body["availability"] = params.availability
    if params.hide_sp is not None:
        body["hide_sp"] = str(params.hide_sp).lower()
    if params.no_cart is not None:
        body["no_cart"] = str(params.no_cart).lower()
    if params.no_order is not None:
        body["no_order"] = str(params.no_order).lower()
    if params.no_search is not None:
        body["no_search"] = str(params.no_search).lower()
    if params.location is not None:
        body["location"] = params.location
    if params.model is not None:
        body["model"] = params.model
    if params.vendor is not None:
        body["vendor"] = params.vendor
    if params.entitlement_script is not None:
        body["entitlement_script"] = params.entitlement_script
    if params.fulfillment_automation_level is not None:
        body["fulfillment_automation_level"] = params.fulfillment_automation_level
    if params.no_wishlist_v2 is not None:
        body["no_wishlist_v2"] = str(params.no_wishlist_v2).lower()
    if params.no_cart_v2 is not None:
        body["no_cart_v2"] = str(params.no_cart_v2).lower()
    if params.no_delivery_time_v2 is not None:
        body["no_delivery_time_v2"] = str(params.no_delivery_time_v2).lower()
    if params.no_attachment_v2 is not None:
        body["no_attachment_v2"] = str(params.no_attachment_v2).lower()
    if params.no_save_as_draft is not None:
        body["no_save_as_draft"] = str(params.no_save_as_draft).lower()
    if params.no_quantity_v2 is not None:
        body["no_quantity_v2"] = str(params.no_quantity_v2).lower()
    if params.request_method is not None:
        body["request_method"] = params.request_method
    if params.mandatory_attachment is not None:
        body["mandatory_attachment"] = str(params.mandatory_attachment).lower()
    if params.show_variable_help_on_load is not None:
        body["show_variable_help_on_load"] = str(params.show_variable_help_on_load).lower()
    if params.make_item_non_conversational is not None:
        body["make_item_non_conversational"] = str(params.make_item_non_conversational).lower()
    if params.taxonomy_topic is not None:
        body["taxonomy_topic"] = params.taxonomy_topic
    if params.sc_template is not None:
        body["sc_template"] = params.sc_template
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        catalog_item = result.get("result", {})
        
        # Format the response
        formatted_item = {
            "sys_id": catalog_item.get("sys_id", ""),
            "name": catalog_item.get("name", ""),
            "short_description": catalog_item.get("short_description", ""),
            "category": catalog_item.get("category", ""),
            "sc_catalogs": catalog_item.get("sc_catalogs", ""),
            "active": catalog_item.get("active", ""),
            "order": catalog_item.get("order", ""),
            "price": catalog_item.get("price", ""),
        }
        
        return CatalogResponse(
            success=True,
            message=f"Created catalog item: {params.name}",
            data=formatted_item,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating catalog item: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error creating catalog item: {str(e)}",
            data=None,
        )


def update_catalog_item(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateCatalogItemParams,
) -> CatalogResponse:
    """
    Update an existing service catalog item in ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating a catalog item

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating service catalog item: {params.item_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item/{params.item_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.name is not None:
        body["name"] = params.name
    if params.short_description is not None:
        body["short_description"] = params.short_description
    if params.description is not None:
        body["description"] = params.description
    if params.category is not None:
        body["category"] = params.category
    if params.sc_catalogs is not None:
        body["sc_catalogs"] = params.sc_catalogs
    if params.active is not None:
        body["active"] = str(params.active).lower()
    if params.order is not None:
        body["order"] = str(params.order)
    if params.price is not None:
        body["price"] = params.price
    if params.list_price is not None:
        body["list_price"] = params.list_price
    if params.cost is not None:
        body["cost"] = params.cost
    if params.recurring_price is not None:
        body["recurring_price"] = params.recurring_price
    if params.recurring_frequency is not None:
        body["recurring_frequency"] = params.recurring_frequency
    if params.billable is not None:
        body["billable"] = str(params.billable).lower()
    if params.picture is not None:
        body["picture"] = params.picture
    if params.icon is not None:
        body["icon"] = params.icon
    if params.image is not None:
        body["image"] = params.image
    if params.mobile_picture is not None:
        body["mobile_picture"] = params.mobile_picture
    if params.group is not None:
        body["group"] = params.group
    if params.workflow is not None:
        body["workflow"] = params.workflow
    if params.delivery_plan is not None:
        body["delivery_plan"] = params.delivery_plan
    if params.delivery_time is not None:
        body["delivery_time"] = params.delivery_time
    if params.roles is not None:
        body["roles"] = params.roles
    if params.access_type is not None:
        body["access_type"] = params.access_type
    if params.availability is not None:
        body["availability"] = params.availability
    if params.hide_sp is not None:
        body["hide_sp"] = str(params.hide_sp).lower()
    if params.no_cart is not None:
        body["no_cart"] = str(params.no_cart).lower()
    if params.no_order is not None:
        body["no_order"] = str(params.no_order).lower()
    if params.no_search is not None:
        body["no_search"] = str(params.no_search).lower()
    if params.location is not None:
        body["location"] = params.location
    if params.model is not None:
        body["model"] = params.model
    if params.vendor is not None:
        body["vendor"] = params.vendor
    if params.entitlement_script is not None:
        body["entitlement_script"] = params.entitlement_script
    if params.fulfillment_automation_level is not None:
        body["fulfillment_automation_level"] = params.fulfillment_automation_level
    if params.no_wishlist_v2 is not None:
        body["no_wishlist_v2"] = str(params.no_wishlist_v2).lower()
    if params.no_cart_v2 is not None:
        body["no_cart_v2"] = str(params.no_cart_v2).lower()
    if params.no_delivery_time_v2 is not None:
        body["no_delivery_time_v2"] = str(params.no_delivery_time_v2).lower()
    if params.no_attachment_v2 is not None:
        body["no_attachment_v2"] = str(params.no_attachment_v2).lower()
    if params.no_save_as_draft is not None:
        body["no_save_as_draft"] = str(params.no_save_as_draft).lower()
    if params.no_quantity_v2 is not None:
        body["no_quantity_v2"] = str(params.no_quantity_v2).lower()
    if params.request_method is not None:
        body["request_method"] = params.request_method
    if params.mandatory_attachment is not None:
        body["mandatory_attachment"] = str(params.mandatory_attachment).lower()
    if params.show_variable_help_on_load is not None:
        body["show_variable_help_on_load"] = str(params.show_variable_help_on_load).lower()
    if params.make_item_non_conversational is not None:
        body["make_item_non_conversational"] = str(params.make_item_non_conversational).lower()
    if params.taxonomy_topic is not None:
        body["taxonomy_topic"] = params.taxonomy_topic
    if params.sc_template is not None:
        body["sc_template"] = params.sc_template
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        catalog_item = result.get("result", {})
        
        # Format the response
        formatted_item = {
            "sys_id": catalog_item.get("sys_id", ""),
            "name": catalog_item.get("name", ""),
            "short_description": catalog_item.get("short_description", ""),
            "category": catalog_item.get("category", ""),
            "sc_catalogs": catalog_item.get("sc_catalogs", ""),
            "active": catalog_item.get("active", ""),
            "order": catalog_item.get("order", ""),
            "price": catalog_item.get("price", ""),
        }
        
        return CatalogResponse(
            success=True,
            message=f"Updated catalog item: {params.item_id}",
            data=formatted_item,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating catalog item: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error updating catalog item: {str(e)}",
            data=None,
        )


def delete_catalog_item(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteCatalogItemParams,
) -> CatalogResponse:
    """
    Delete a service catalog item from ServiceNow.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting a catalog item

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting service catalog item: {params.item_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item/{params.item_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return CatalogResponse(
            success=True,
            message=f"Deleted catalog item: {params.item_id}",
            data={"deleted_item_id": params.item_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting catalog item: {str(e)}")
        return CatalogResponse(
            success=False,
            message=f"Error deleting catalog item: {str(e)}",
            data=None,
        )