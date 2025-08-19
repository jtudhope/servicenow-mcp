"""
Catalog UI Policy tools for the ServiceNow MCP server.

This module provides tools for managing Catalog UI Policies that are stored in the catalog_ui_policy table.
Catalog Policies are a set of rules that dynamically changes how fields behave on a Service Catalog item 
or record producer form — without writing client-side JavaScript.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateCatalogUIPolicyParams(BaseModel):
    """Parameters for creating a catalog UI policy."""

    name: str = Field(..., description="Name of the catalog UI policy")
    catalog_item: Optional[str] = Field(None, description="Catalog item sys_id this policy applies to")
    variable_set: Optional[str] = Field(None, description="Variable set sys_id this policy applies to")
    applies_to: Optional[str] = Field("item", description="What the policy applies to (item, variable_set)")
    description: Optional[str] = Field(None, description="Description of the UI policy")
    active: Optional[bool] = Field(True, description="Whether the UI policy is active")
    applies_catalog: Optional[bool] = Field(True, description="Applies on a Catalog Item view")
    applies_req_item: Optional[bool] = Field(False, description="Applies on Requested Items")
    applies_sc_task: Optional[bool] = Field(False, description="Applies on Catalog Tasks")
    applies_target_record: Optional[bool] = Field(False, description="Applies on the Target Record")
    catalog_conditions: Optional[str] = Field(None, description="Catalog conditions in JSON format")


class UpdateCatalogUIPolicyParams(BaseModel):
    """Parameters for updating a catalog UI policy."""

    policy_id: str = Field(..., description="Catalog UI policy sys_id")
    name: Optional[str] = Field(None, description="Updated name of the catalog UI policy")
    catalog_item: Optional[str] = Field(None, description="Updated catalog item sys_id")
    variable_set: Optional[str] = Field(None, description="Updated variable set sys_id")
    applies_to: Optional[str] = Field(None, description="Updated applies to value")
    description: Optional[str] = Field(None, description="Updated description")
    active: Optional[bool] = Field(None, description="Updated active status")
    applies_catalog: Optional[bool] = Field(None, description="Updated applies on catalog item view")
    applies_req_item: Optional[bool] = Field(None, description="Updated applies on requested items")
    applies_sc_task: Optional[bool] = Field(None, description="Updated applies on catalog tasks")
    applies_target_record: Optional[bool] = Field(None, description="Updated applies on target record")
    catalog_conditions: Optional[str] = Field(None, description="Updated catalog conditions")


class ListCatalogUIPoliciesParams(BaseModel):
    """Parameters for listing catalog UI policies."""

    limit: int = Field(10, description="Maximum number of policies to return")
    offset: int = Field(0, description="Offset for pagination")
    active: Optional[bool] = Field(None, description="Filter by active status")
    catalog_item: Optional[str] = Field(None, description="Filter by catalog item sys_id")
    applies_to: Optional[str] = Field(None, description="Filter by applies to value")
    query: Optional[str] = Field(None, description="Search query for policy name or description")


class GetCatalogUIPolicyParams(BaseModel):
    """Parameters for getting a specific catalog UI policy."""

    policy_id: str = Field(..., description="Catalog UI policy sys_id")


class DeleteCatalogUIPolicyParams(BaseModel):
    """Parameters for deleting a catalog UI policy."""

    policy_id: str = Field(..., description="Catalog UI policy sys_id")


class CatalogUIPolicyResponse(BaseModel):
    """Response from catalog UI policy operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_catalog_ui_policy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateCatalogUIPolicyParams,
) -> CatalogUIPolicyResponse:
    """
    Create a new catalog UI policy in the catalog_ui_policy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the catalog UI policy

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating catalog UI policy: {params.name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy"
    
    # Prepare request body
    body = {
        "sys_name": params.name,
        "applies_to": params.applies_to or "item",
        "active": str(params.active).lower() if params.active is not None else "true",
        "applies_catalog": str(params.applies_catalog).lower() if params.applies_catalog is not None else "true",
        "applies_req_item": str(params.applies_req_item).lower() if params.applies_req_item is not None else "false",
        "applies_sc_task": str(params.applies_sc_task).lower() if params.applies_sc_task is not None else "false",
        "applies_target_record": str(params.applies_target_record).lower() if params.applies_target_record is not None else "false",
    }
    
    if params.catalog_item is not None:
        body["catalog_item"] = params.catalog_item
    if params.variable_set is not None:
        body["variable_set"] = params.variable_set
    if params.description is not None:
        body["description"] = params.description
    if params.catalog_conditions is not None:
        body["catalog_conditions"] = params.catalog_conditions
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        policy = result.get("result", {})
        
        # Format the response
        formatted_policy = {
            "sys_id": policy.get("sys_id", ""),
            "sys_name": policy.get("sys_name", ""),
            "catalog_item": policy.get("catalog_item", ""),
            "variable_set": policy.get("variable_set", ""),
            "applies_to": policy.get("applies_to", ""),
            "description": policy.get("description", ""),
            "active": policy.get("active", ""),
            "applies_catalog": policy.get("applies_catalog", ""),
            "applies_req_item": policy.get("applies_req_item", ""),
            "applies_sc_task": policy.get("applies_sc_task", ""),
            "applies_target_record": policy.get("applies_target_record", ""),
            "catalog_conditions": policy.get("catalog_conditions", ""),
            "sys_created_on": policy.get("sys_created_on", ""),
        }
        
        return CatalogUIPolicyResponse(
            success=True,
            message=f"Created catalog UI policy: {params.name}",
            data=formatted_policy,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating catalog UI policy: {str(e)}")
        return CatalogUIPolicyResponse(
            success=False,
            message=f"Error creating catalog UI policy: {str(e)}",
            data=None,
        )


def update_catalog_ui_policy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateCatalogUIPolicyParams,
) -> CatalogUIPolicyResponse:
    """
    Update an existing catalog UI policy in the catalog_ui_policy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the catalog UI policy

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating catalog UI policy: {params.policy_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy/{params.policy_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.name is not None:
        body["sys_name"] = params.name
    if params.catalog_item is not None:
        body["catalog_item"] = params.catalog_item
    if params.variable_set is not None:
        body["variable_set"] = params.variable_set
    if params.applies_to is not None:
        body["applies_to"] = params.applies_to
    if params.description is not None:
        body["description"] = params.description
    if params.active is not None:
        body["active"] = str(params.active).lower()
    if params.applies_catalog is not None:
        body["applies_catalog"] = str(params.applies_catalog).lower()
    if params.applies_req_item is not None:
        body["applies_req_item"] = str(params.applies_req_item).lower()
    if params.applies_sc_task is not None:
        body["applies_sc_task"] = str(params.applies_sc_task).lower()
    if params.applies_target_record is not None:
        body["applies_target_record"] = str(params.applies_target_record).lower()
    if params.catalog_conditions is not None:
        body["catalog_conditions"] = params.catalog_conditions
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        policy = result.get("result", {})
        
        # Format the response
        formatted_policy = {
            "sys_id": policy.get("sys_id", ""),
            "sys_name": policy.get("sys_name", ""),
            "catalog_item": policy.get("catalog_item", ""),
            "variable_set": policy.get("variable_set", ""),
            "applies_to": policy.get("applies_to", ""),
            "description": policy.get("description", ""),
            "active": policy.get("active", ""),
            "applies_catalog": policy.get("applies_catalog", ""),
            "applies_req_item": policy.get("applies_req_item", ""),
            "applies_sc_task": policy.get("applies_sc_task", ""),
            "applies_target_record": policy.get("applies_target_record", ""),
            "catalog_conditions": policy.get("catalog_conditions", ""),
            "sys_updated_on": policy.get("sys_updated_on", ""),
        }
        
        return CatalogUIPolicyResponse(
            success=True,
            message=f"Updated catalog UI policy: {params.policy_id}",
            data=formatted_policy,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating catalog UI policy: {str(e)}")
        return CatalogUIPolicyResponse(
            success=False,
            message=f"Error updating catalog UI policy: {str(e)}",
            data=None,
        )


def list_catalog_ui_policies(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListCatalogUIPoliciesParams,
) -> Dict[str, Any]:
    """
    List catalog UI policies from the catalog_ui_policy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing catalog UI policies

    Returns:
        Dictionary containing catalog UI policies and metadata
    """
    logger.info("Listing catalog UI policies")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,sys_name,catalog_item,variable_set,applies_to,description,active,applies_catalog,applies_req_item,applies_sc_task,applies_target_record,catalog_conditions,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    if params.catalog_item:
        filters.append(f"catalog_item={params.catalog_item}")
    if params.applies_to:
        filters.append(f"applies_to={params.applies_to}")
    if params.query:
        filters.append(f"sys_nameLIKE{params.query}^ORdescriptionLIKE{params.query}")
    
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
        policies = result.get("result", [])
        
        # Format the response
        formatted_policies = []
        for policy in policies:
            formatted_policies.append({
                "sys_id": policy.get("sys_id", ""),
                "sys_name": policy.get("sys_name", ""),
                "catalog_item": policy.get("catalog_item", ""),
                "variable_set": policy.get("variable_set", ""),
                "applies_to": policy.get("applies_to", ""),
                "description": policy.get("description", ""),
                "active": policy.get("active", ""),
                "applies_catalog": policy.get("applies_catalog", ""),
                "applies_req_item": policy.get("applies_req_item", ""),
                "applies_sc_task": policy.get("applies_sc_task", ""),
                "applies_target_record": policy.get("applies_target_record", ""),
                "catalog_conditions": policy.get("catalog_conditions", ""),
                "sys_created_on": policy.get("sys_created_on", ""),
                "sys_updated_on": policy.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_policies)} catalog UI policies",
            "policies": formatted_policies,
            "total": len(formatted_policies),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing catalog UI policies: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing catalog UI policies: {str(e)}",
            "policies": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_catalog_ui_policy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetCatalogUIPolicyParams,
) -> CatalogUIPolicyResponse:
    """
    Get a specific catalog UI policy from the catalog_ui_policy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the catalog UI policy

    Returns:
        Response containing the catalog UI policy details
    """
    logger.info(f"Getting catalog UI policy: {params.policy_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy/{params.policy_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,sys_name,catalog_item,variable_set,applies_to,description,active,applies_catalog,applies_req_item,applies_sc_task,applies_target_record,catalog_conditions,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        policy = result.get("result", {})
        
        if not policy:
            return CatalogUIPolicyResponse(
                success=False,
                message=f"Catalog UI policy not found: {params.policy_id}",
                data=None,
            )
        
        # Format the response
        formatted_policy = {
            "sys_id": policy.get("sys_id", ""),
            "sys_name": policy.get("sys_name", ""),
            "catalog_item": policy.get("catalog_item", ""),
            "variable_set": policy.get("variable_set", ""),
            "applies_to": policy.get("applies_to", ""),
            "description": policy.get("description", ""),
            "active": policy.get("active", ""),
            "applies_catalog": policy.get("applies_catalog", ""),
            "applies_req_item": policy.get("applies_req_item", ""),
            "applies_sc_task": policy.get("applies_sc_task", ""),
            "applies_target_record": policy.get("applies_target_record", ""),
            "catalog_conditions": policy.get("catalog_conditions", ""),
            "sys_created_on": policy.get("sys_created_on", ""),
            "sys_updated_on": policy.get("sys_updated_on", ""),
        }
        
        return CatalogUIPolicyResponse(
            success=True,
            message=f"Retrieved catalog UI policy: {policy.get('sys_name', '')}",
            data=formatted_policy,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting catalog UI policy: {str(e)}")
        return CatalogUIPolicyResponse(
            success=False,
            message=f"Error getting catalog UI policy: {str(e)}",
            data=None,
        )


def delete_catalog_ui_policy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteCatalogUIPolicyParams,
) -> CatalogUIPolicyResponse:
    """
    Delete a catalog UI policy from the catalog_ui_policy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the catalog UI policy

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting catalog UI policy: {params.policy_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_ui_policy/{params.policy_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return CatalogUIPolicyResponse(
            success=True,
            message=f"Deleted catalog UI policy: {params.policy_id}",
            data={"deleted_policy_id": params.policy_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting catalog UI policy: {str(e)}")
        return CatalogUIPolicyResponse(
            success=False,
            message=f"Error deleting catalog UI policy: {str(e)}",
            data=None,
        )


def clone_catalog_ui_policy(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: Dict[str, Any],
) -> CatalogUIPolicyResponse:
    """
    Clone an existing catalog UI policy in the catalog_ui_policy table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters containing policy_id and new_name

    Returns:
        Response containing the result of the operation
    """
    source_policy_id = params.get("policy_id")
    new_name = params.get("new_name")
    
    if not source_policy_id or not new_name:
        return CatalogUIPolicyResponse(
            success=False,
            message="Both policy_id and new_name are required for cloning",
            data=None,
        )
    
    logger.info(f"Cloning catalog UI policy: {source_policy_id} as {new_name}")
    
    # First, get the source policy
    get_params = GetCatalogUIPolicyParams(policy_id=source_policy_id)
    source_response = get_catalog_ui_policy(config, auth_manager, get_params)
    
    if not source_response.success or not source_response.data:
        return CatalogUIPolicyResponse(
            success=False,
            message=f"Could not retrieve source policy: {source_policy_id}",
            data=None,
        )
    
    # Create the cloned policy
    source_data = source_response.data
    create_params = CreateCatalogUIPolicyParams(
        name=new_name,
        catalog_item=source_data.get("catalog_item"),
        variable_set=source_data.get("variable_set"),
        applies_to=source_data.get("applies_to"),
        description=source_data.get("description"),
        active=source_data.get("active") == "true",
        applies_catalog=source_data.get("applies_catalog") == "true",
        applies_req_item=source_data.get("applies_req_item") == "true",
        applies_sc_task=source_data.get("applies_sc_task") == "true",
        applies_target_record=source_data.get("applies_target_record") == "true",
        catalog_conditions=source_data.get("catalog_conditions"),
    )
    
    return create_catalog_ui_policy(config, auth_manager, create_params)