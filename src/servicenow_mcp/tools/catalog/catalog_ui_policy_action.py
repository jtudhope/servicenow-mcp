"""
Catalog UI Policy Action tools for the ServiceNow MCP server.

This module provides tools for managing Catalog UI Policy Actions that are stored in the catalog_ui_policy_action table.
Catalog UI Policy Actions are a set of actions that can be taken as a result of a Catalog UI Policy.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateCatalogUIPolicyActionParams(BaseModel):
    """Parameters for creating a catalog UI policy action."""

    catalog_item: Optional[str] = Field(None, description="Catalog item sys_id this action applies to")
    variable_set: Optional[str] = Field(None, description="Variable set sys_id this action applies to")
    catalog_variable: Optional[str] = Field(None, description="Variable name this action applies to")
    variable: str = Field(..., description="Name of the variable")
    order: Optional[int] = Field(100, description="Order of execution for this action")


class UpdateCatalogUIPolicyActionParams(BaseModel):
    """Parameters for updating a catalog UI policy action."""

    action_id: str = Field(..., description="Catalog UI policy action sys_id")
    catalog_item: Optional[str] = Field(None, description="Updated catalog item sys_id")
    variable_set: Optional[str] = Field(None, description="Updated variable set sys_id")
    catalog_variable: Optional[str] = Field(None, description="Updated variable name")
    variable: Optional[str] = Field(None, description="Updated name of the variable")
    order: Optional[int] = Field(None, description="Updated order of execution")


class ListCatalogUIPolicyActionsParams(BaseModel):
    """Parameters for listing catalog UI policy actions."""

    limit: int = Field(10, description="Maximum number of actions to return")
    offset: int = Field(0, description="Offset for pagination")
    catalog_item: Optional[str] = Field(None, description="Filter by catalog item sys_id")
    variable_set: Optional[str] = Field(None, description="Filter by variable set sys_id")
    variable: Optional[str] = Field(None, description="Filter by variable name")
    query: Optional[str] = Field(None, description="Search query for action details")


class GetCatalogUIPolicyActionParams(BaseModel):
    """Parameters for getting a specific catalog UI policy action."""

    action_id: str = Field(..., description="Catalog UI policy action sys_id")


class DeleteCatalogUIPolicyActionParams(BaseModel):
    """Parameters for deleting a catalog UI policy action."""

    action_id: str = Field(..., description="Catalog UI policy action sys_id")


class CatalogUIPolicyActionResponse(BaseModel):
    """Response from catalog UI policy action operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_catalog_ui_policy_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateCatalogUIPolicyActionParams,
) -> CatalogUIPolicyActionResponse:
    """
    Create a new catalog UI policy action in the catalog_ui_policy_action table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the catalog UI policy action

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating catalog UI policy action for variable: {params.variable}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy_action"
    
    # Prepare request body
    body = {
        "variable": params.variable,
        "order": params.order or 100,
    }
    
    if params.catalog_item is not None:
        body["catalog_item"] = params.catalog_item
    if params.variable_set is not None:
        body["variable_set"] = params.variable_set
    if params.catalog_variable is not None:
        body["catalog_variable"] = params.catalog_variable
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        action = result.get("result", {})
        
        # Format the response
        formatted_action = {
            "sys_id": action.get("sys_id", ""),
            "catalog_item": action.get("catalog_item", ""),
            "variable_set": action.get("variable_set", ""),
            "catalog_variable": action.get("catalog_variable", ""),
            "variable": action.get("variable", ""),
            "order": action.get("order", ""),
            "sys_created_on": action.get("sys_created_on", ""),
        }
        
        return CatalogUIPolicyActionResponse(
            success=True,
            message=f"Created catalog UI policy action for variable: {params.variable}",
            data=formatted_action,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating catalog UI policy action: {str(e)}")
        return CatalogUIPolicyActionResponse(
            success=False,
            message=f"Error creating catalog UI policy action: {str(e)}",
            data=None,
        )


def update_catalog_ui_policy_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateCatalogUIPolicyActionParams,
) -> CatalogUIPolicyActionResponse:
    """
    Update an existing catalog UI policy action in the catalog_ui_policy_action table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the catalog UI policy action

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating catalog UI policy action: {params.action_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy_action/{params.action_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.catalog_item is not None:
        body["catalog_item"] = params.catalog_item
    if params.variable_set is not None:
        body["variable_set"] = params.variable_set
    if params.catalog_variable is not None:
        body["catalog_variable"] = params.catalog_variable
    if params.variable is not None:
        body["variable"] = params.variable
    if params.order is not None:
        body["order"] = params.order
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        action = result.get("result", {})
        
        # Format the response
        formatted_action = {
            "sys_id": action.get("sys_id", ""),
            "catalog_item": action.get("catalog_item", ""),
            "variable_set": action.get("variable_set", ""),
            "catalog_variable": action.get("catalog_variable", ""),
            "variable": action.get("variable", ""),
            "order": action.get("order", ""),
            "sys_updated_on": action.get("sys_updated_on", ""),
        }
        
        return CatalogUIPolicyActionResponse(
            success=True,
            message=f"Updated catalog UI policy action: {params.action_id}",
            data=formatted_action,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating catalog UI policy action: {str(e)}")
        return CatalogUIPolicyActionResponse(
            success=False,
            message=f"Error updating catalog UI policy action: {str(e)}",
            data=None,
        )


def list_catalog_ui_policy_actions(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListCatalogUIPolicyActionsParams,
) -> Dict[str, Any]:
    """
    List catalog UI policy actions from the catalog_ui_policy_action table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing catalog UI policy actions

    Returns:
        Dictionary containing catalog UI policy actions and metadata
    """
    logger.info("Listing catalog UI policy actions")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy_action"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,catalog_item,variable_set,catalog_variable,variable,order,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.catalog_item:
        filters.append(f"catalog_item={params.catalog_item}")
    if params.variable_set:
        filters.append(f"variable_set={params.variable_set}")
    if params.variable:
        filters.append(f"variableLIKE{params.variable}")
    if params.query:
        filters.append(f"variableLIKE{params.query}^ORcatalog_variableLIKE{params.query}")
    
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
        actions = result.get("result", [])
        
        # Format the response
        formatted_actions = []
        for action in actions:
            formatted_actions.append({
                "sys_id": action.get("sys_id", ""),
                "catalog_item": action.get("catalog_item", ""),
                "variable_set": action.get("variable_set", ""),
                "catalog_variable": action.get("catalog_variable", ""),
                "variable": action.get("variable", ""),
                "order": action.get("order", ""),
                "sys_created_on": action.get("sys_created_on", ""),
                "sys_updated_on": action.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_actions)} catalog UI policy actions",
            "actions": formatted_actions,
            "total": len(formatted_actions),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing catalog UI policy actions: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing catalog UI policy actions: {str(e)}",
            "actions": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_catalog_ui_policy_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetCatalogUIPolicyActionParams,
) -> CatalogUIPolicyActionResponse:
    """
    Get a specific catalog UI policy action from the catalog_ui_policy_action table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the catalog UI policy action

    Returns:
        Response containing the catalog UI policy action details
    """
    logger.info(f"Getting catalog UI policy action: {params.action_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy_action/{params.action_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,catalog_item,variable_set,catalog_variable,variable,order,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        action = result.get("result", {})
        
        if not action:
            return CatalogUIPolicyActionResponse(
                success=False,
                message=f"Catalog UI policy action not found: {params.action_id}",
                data=None,
            )
        
        # Format the response
        formatted_action = {
            "sys_id": action.get("sys_id", ""),
            "catalog_item": action.get("catalog_item", ""),
            "variable_set": action.get("variable_set", ""),
            "catalog_variable": action.get("catalog_variable", ""),
            "variable": action.get("variable", ""),
            "order": action.get("order", ""),
            "sys_created_on": action.get("sys_created_on", ""),
            "sys_updated_on": action.get("sys_updated_on", ""),
        }
        
        return CatalogUIPolicyActionResponse(
            success=True,
            message=f"Retrieved catalog UI policy action: {action.get('variable', '')}",
            data=formatted_action,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting catalog UI policy action: {str(e)}")
        return CatalogUIPolicyActionResponse(
            success=False,
            message=f"Error getting catalog UI policy action: {str(e)}",
            data=None,
        )


def delete_catalog_ui_policy_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteCatalogUIPolicyActionParams,
) -> CatalogUIPolicyActionResponse:
    """
    Delete a catalog UI policy action from the catalog_ui_policy_action table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the catalog UI policy action

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting catalog UI policy action: {params.action_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy_action/{params.action_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return CatalogUIPolicyActionResponse(
            success=True,
            message=f"Deleted catalog UI policy action: {params.action_id}",
            data={"deleted_action_id": params.action_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting catalog UI policy action: {str(e)}")
        return CatalogUIPolicyActionResponse(
            success=False,
            message=f"Error deleting catalog UI policy action: {str(e)}",
            data=None,
        )


def clone_catalog_ui_policy_action(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: Dict[str, Any],
) -> CatalogUIPolicyActionResponse:
    """
    Clone an existing catalog UI policy action in the catalog_ui_policy_action table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters containing action_id and new_variable

    Returns:
        Response containing the result of the operation
    """
    source_action_id = params.get("action_id")
    new_variable = params.get("new_variable")
    
    if not source_action_id or not new_variable:
        return CatalogUIPolicyActionResponse(
            success=False,
            message="Both action_id and new_variable are required for cloning",
            data=None,
        )
    
    logger.info(f"Cloning catalog UI policy action: {source_action_id} as {new_variable}")
    
    # First, get the source action
    get_params = GetCatalogUIPolicyActionParams(action_id=source_action_id)
    source_response = get_catalog_ui_policy_action(config, auth_manager, get_params)
    
    if not source_response.success or not source_response.data:
        return CatalogUIPolicyActionResponse(
            success=False,
            message=f"Could not retrieve source action: {source_action_id}",
            data=None,
        )
    
    # Create the cloned action
    source_data = source_response.data
    create_params = CreateCatalogUIPolicyActionParams(
        catalog_item=source_data.get("catalog_item"),
        variable_set=source_data.get("variable_set"),
        catalog_variable=source_data.get("catalog_variable"),
        variable=new_variable,
        order=int(source_data.get("order", "100")),
    )
    
    return create_catalog_ui_policy_action(config, auth_manager, create_params)