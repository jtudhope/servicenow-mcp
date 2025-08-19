"""
Catalog Item Available For tools for the ServiceNow MCP server.

This module provides tools for managing Catalog Item Availability rules that are stored in the 
sc_cat_item_user_criteria_mtom (available for) and sc_cat_item_user_criteria_no_mtom (not available for) tables.
In ServiceNow, "Available For" on a Catalog Item controls who can see and request that item in the Service Catalog.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class AddAvailableForParams(BaseModel):
    """Parameters for adding an available for rule to a catalog item."""

    catalog_item_id: str = Field(..., description="Catalog item sys_id")
    user_criteria_id: str = Field(..., description="User criteria sys_id to make the item available for")


class RemoveAvailableForParams(BaseModel):
    """Parameters for removing an available for rule from a catalog item."""

    catalog_item_id: str = Field(..., description="Catalog item sys_id")
    user_criteria_id: str = Field(..., description="User criteria sys_id to remove from available for")


class AddNotAvailableForParams(BaseModel):
    """Parameters for adding a not available for rule to a catalog item."""

    catalog_item_id: str = Field(..., description="Catalog item sys_id")
    user_criteria_id: str = Field(..., description="User criteria sys_id to make the item not available for")


class RemoveNotAvailableForParams(BaseModel):
    """Parameters for removing a not available for rule from a catalog item."""

    catalog_item_id: str = Field(..., description="Catalog item sys_id")
    user_criteria_id: str = Field(..., description="User criteria sys_id to remove from not available for")


class ListAvailableForParams(BaseModel):
    """Parameters for listing available for rules for a catalog item."""

    catalog_item_id: str = Field(..., description="Catalog item sys_id")
    rule_type: str = Field("available", description="Type of rules to list (available or not_available)")
    limit: int = Field(10, description="Maximum number of rules to return")
    offset: int = Field(0, description="Offset for pagination")


class AvailabilityRuleResponse(BaseModel):
    """Response from availability rule operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def add_available_for(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: AddAvailableForParams,
) -> AvailabilityRuleResponse:
    """
    Add an available for rule to a catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for adding the available for rule

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Adding available for rule to catalog item {params.catalog_item_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item_user_criteria_mtom"
    
    # Prepare request body
    body = {
        "sc_cat_item": params.catalog_item_id,
        "user_criteria": params.user_criteria_id,
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        rule = result.get("result", {})
        
        # Format the response
        formatted_rule = {
            "sys_id": rule.get("sys_id", ""),
            "sc_cat_item": rule.get("sc_cat_item", ""),
            "user_criteria": rule.get("user_criteria", ""),
            "sys_created_on": rule.get("sys_created_on", ""),
        }
        
        return AvailabilityRuleResponse(
            success=True,
            message=f"Added available for rule to catalog item {params.catalog_item_id}",
            data=formatted_rule,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding available for rule: {str(e)}")
        return AvailabilityRuleResponse(
            success=False,
            message=f"Error adding available for rule: {str(e)}",
            data=None,
        )


def remove_available_for(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: RemoveAvailableForParams,
) -> AvailabilityRuleResponse:
    """
    Remove an available for rule from a catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for removing the available for rule

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Removing available for rule from catalog item {params.catalog_item_id}")
    
    # First, find the rule to delete
    list_url = f"{config.instance_url}/api/now/table/sc_cat_item_user_criteria_mtom"
    query_params = {
        "sysparm_query": f"sc_cat_item={params.catalog_item_id}^user_criteria={params.user_criteria_id}",
        "sysparm_fields": "sys_id",
    }
    
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        # Find the rule
        response = requests.get(list_url, headers=headers, params=query_params)
        response.raise_for_status()
        
        result = response.json()
        rules = result.get("result", [])
        
        if not rules:
            return AvailabilityRuleResponse(
                success=False,
                message=f"Available for rule not found for catalog item {params.catalog_item_id} and user criteria {params.user_criteria_id}",
                data=None,
            )
        
        rule_id = rules[0]["sys_id"]
        
        # Delete the rule
        delete_url = f"{config.instance_url}/api/now/table/sc_cat_item_user_criteria_mtom/{rule_id}"
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()
        
        return AvailabilityRuleResponse(
            success=True,
            message=f"Removed available for rule from catalog item {params.catalog_item_id}",
            data={"deleted_rule_id": rule_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error removing available for rule: {str(e)}")
        return AvailabilityRuleResponse(
            success=False,
            message=f"Error removing available for rule: {str(e)}",
            data=None,
        )


def add_not_available_for(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: AddNotAvailableForParams,
) -> AvailabilityRuleResponse:
    """
    Add a not available for rule to a catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for adding the not available for rule

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Adding not available for rule to catalog item {params.catalog_item_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sc_cat_item_user_criteria_no_mtom"
    
    # Prepare request body
    body = {
        "sc_cat_item": params.catalog_item_id,
        "user_criteria": params.user_criteria_id,
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        rule = result.get("result", {})
        
        # Format the response
        formatted_rule = {
            "sys_id": rule.get("sys_id", ""),
            "sc_cat_item": rule.get("sc_cat_item", ""),
            "user_criteria": rule.get("user_criteria", ""),
            "sys_created_on": rule.get("sys_created_on", ""),
        }
        
        return AvailabilityRuleResponse(
            success=True,
            message=f"Added not available for rule to catalog item {params.catalog_item_id}",
            data=formatted_rule,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding not available for rule: {str(e)}")
        return AvailabilityRuleResponse(
            success=False,
            message=f"Error adding not available for rule: {str(e)}",
            data=None,
        )


def remove_not_available_for(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: RemoveNotAvailableForParams,
) -> AvailabilityRuleResponse:
    """
    Remove a not available for rule from a catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for removing the not available for rule

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Removing not available for rule from catalog item {params.catalog_item_id}")
    
    # First, find the rule to delete
    list_url = f"{config.instance_url}/api/now/table/sc_cat_item_user_criteria_no_mtom"
    query_params = {
        "sysparm_query": f"sc_cat_item={params.catalog_item_id}^user_criteria={params.user_criteria_id}",
        "sysparm_fields": "sys_id",
    }
    
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        # Find the rule
        response = requests.get(list_url, headers=headers, params=query_params)
        response.raise_for_status()
        
        result = response.json()
        rules = result.get("result", [])
        
        if not rules:
            return AvailabilityRuleResponse(
                success=False,
                message=f"Not available for rule not found for catalog item {params.catalog_item_id} and user criteria {params.user_criteria_id}",
                data=None,
            )
        
        rule_id = rules[0]["sys_id"]
        
        # Delete the rule
        delete_url = f"{config.instance_url}/api/now/table/sc_cat_item_user_criteria_no_mtom/{rule_id}"
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()
        
        return AvailabilityRuleResponse(
            success=True,
            message=f"Removed not available for rule from catalog item {params.catalog_item_id}",
            data={"deleted_rule_id": rule_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error removing not available for rule: {str(e)}")
        return AvailabilityRuleResponse(
            success=False,
            message=f"Error removing not available for rule: {str(e)}",
            data=None,
        )


def list_available_for(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListAvailableForParams,
) -> Dict[str, Any]:
    """
    List available for or not available for rules for a catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing availability rules

    Returns:
        Dictionary containing availability rules and metadata
    """
    logger.info(f"Listing {params.rule_type} rules for catalog item {params.catalog_item_id}")
    
    # Determine which table to query based on rule type
    if params.rule_type == "not_available":
        table_name = "sc_cat_item_user_criteria_no_mtom"
    else:
        table_name = "sc_cat_item_user_criteria_mtom"
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/{table_name}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_query": f"sc_cat_item={params.catalog_item_id}",
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,sc_cat_item,user_criteria,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        rules = result.get("result", [])
        
        # Format the response
        formatted_rules = []
        for rule in rules:
            formatted_rules.append({
                "sys_id": rule.get("sys_id", ""),
                "sc_cat_item": rule.get("sc_cat_item", ""),
                "user_criteria": rule.get("user_criteria", ""),
                "sys_created_on": rule.get("sys_created_on", ""),
                "sys_updated_on": rule.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_rules)} {params.rule_type} rules for catalog item {params.catalog_item_id}",
            "rules": formatted_rules,
            "total": len(formatted_rules),
            "limit": params.limit,
            "offset": params.offset,
            "rule_type": params.rule_type,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing {params.rule_type} rules: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing {params.rule_type} rules: {str(e)}",
            "rules": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
            "rule_type": params.rule_type,
        }


def bulk_update_available_for(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: Dict[str, Any],
) -> AvailabilityRuleResponse:
    """
    Bulk update available for rules for a catalog item.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters containing catalog_item_id, available_for_criteria, and not_available_for_criteria

    Returns:
        Response containing the result of the operation
    """
    catalog_item_id = params.get("catalog_item_id")
    available_for_criteria = params.get("available_for_criteria", [])
    not_available_for_criteria = params.get("not_available_for_criteria", [])
    
    if not catalog_item_id:
        return AvailabilityRuleResponse(
            success=False,
            message="catalog_item_id is required for bulk update",
            data=None,
        )
    
    logger.info(f"Bulk updating availability rules for catalog item {catalog_item_id}")
    
    try:
        # First, remove all existing rules
        for table_name in ["sc_cat_item_user_criteria_mtom", "sc_cat_item_user_criteria_no_mtom"]:
            list_url = f"{config.instance_url}/api/now/table/{table_name}"
            query_params = {
                "sysparm_query": f"sc_cat_item={catalog_item_id}",
                "sysparm_fields": "sys_id",
            }
            
            headers = auth_manager.get_headers()
            headers["Accept"] = "application/json"
            
            response = requests.get(list_url, headers=headers, params=query_params)
            response.raise_for_status()
            
            result = response.json()
            existing_rules = result.get("result", [])
            
            # Delete existing rules
            for rule in existing_rules:
                delete_url = f"{config.instance_url}/api/now/table/{table_name}/{rule['sys_id']}"
                requests.delete(delete_url, headers=headers)
        
        # Add new available for rules
        for criteria_id in available_for_criteria:
            add_params = AddAvailableForParams(
                catalog_item_id=catalog_item_id,
                user_criteria_id=criteria_id
            )
            add_available_for(config, auth_manager, add_params)
        
        # Add new not available for rules
        for criteria_id in not_available_for_criteria:
            add_params = AddNotAvailableForParams(
                catalog_item_id=catalog_item_id,
                user_criteria_id=criteria_id
            )
            add_not_available_for(config, auth_manager, add_params)
        
        return AvailabilityRuleResponse(
            success=True,
            message=f"Bulk updated availability rules for catalog item {catalog_item_id}",
            data={
                "catalog_item_id": catalog_item_id,
                "available_for_count": len(available_for_criteria),
                "not_available_for_count": len(not_available_for_criteria),
            },
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error bulk updating availability rules: {str(e)}")
        return AvailabilityRuleResponse(
            success=False,
            message=f"Error bulk updating availability rules: {str(e)}",
            data=None,
        )