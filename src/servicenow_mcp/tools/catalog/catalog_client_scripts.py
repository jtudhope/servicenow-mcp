"""
Catalog Client Scripts tools for the ServiceNow MCP server.

This module provides tools for managing Catalog Client Scripts that are stored in the catalog_script_client table.
Catalog Client Scripts are JavaScript that runs in the user's browser to control behavior on Service Catalog items,
record producers, or order guide forms.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateCatalogClientScriptParams(BaseModel):
    """Parameters for creating a catalog client script."""

    name: str = Field(..., description="Name of the catalog client script")
    script: str = Field(..., description="Client script content")
    cat_item: Optional[str] = Field(None, description="Catalog item sys_id this script applies to")
    variable_set: Optional[str] = Field(None, description="Variable set sys_id this script applies to")
    cat_variable: Optional[str] = Field(None, description="Variable this script applies to")
    applies_to: Optional[str] = Field(None, description="What this script applies to")
    applies_catalog: Optional[bool] = Field(False, description="Whether this script applies to catalog")
    applies_req_item: Optional[bool] = Field(False, description="Whether this script applies to requested items")
    applies_sc_task: Optional[bool] = Field(False, description="Whether this script applies to SC tasks")
    applies_target_record: Optional[bool] = Field(False, description="Whether this script applies to target records")
    va_supported: Optional[bool] = Field(False, description="Whether virtual agent is supported")
    active: Optional[bool] = Field(True, description="Whether the script is active")
    ui_type: Optional[str] = Field(None, description="UI type for the script")
    type: Optional[str] = Field(None, description="Type of script")


class UpdateCatalogClientScriptParams(BaseModel):
    """Parameters for updating a catalog client script."""

    script_id: str = Field(..., description="Catalog client script sys_id")
    name: Optional[str] = Field(None, description="Updated name of the script")
    script: Optional[str] = Field(None, description="Updated client script content")
    cat_item: Optional[str] = Field(None, description="Updated catalog item sys_id")
    variable_set: Optional[str] = Field(None, description="Updated variable set sys_id")
    cat_variable: Optional[str] = Field(None, description="Updated variable")
    applies_to: Optional[str] = Field(None, description="Updated applies to value")
    applies_catalog: Optional[bool] = Field(None, description="Updated applies to catalog setting")
    applies_req_item: Optional[bool] = Field(None, description="Updated applies to requested items setting")
    applies_sc_task: Optional[bool] = Field(None, description="Updated applies to SC tasks setting")
    applies_target_record: Optional[bool] = Field(None, description="Updated applies to target records setting")
    va_supported: Optional[bool] = Field(None, description="Updated virtual agent support setting")
    active: Optional[bool] = Field(None, description="Updated active status")
    ui_type: Optional[str] = Field(None, description="Updated UI type")
    type: Optional[str] = Field(None, description="Updated script type")


class ListCatalogClientScriptsParams(BaseModel):
    """Parameters for listing catalog client scripts."""

    limit: int = Field(10, description="Maximum number of scripts to return")
    offset: int = Field(0, description="Offset for pagination")
    cat_item: Optional[str] = Field(None, description="Filter by catalog item sys_id")
    variable_set: Optional[str] = Field(None, description="Filter by variable set sys_id")
    cat_variable: Optional[str] = Field(None, description="Filter by variable")
    active: Optional[bool] = Field(None, description="Filter by active status")
    query: Optional[str] = Field(None, description="Search query for script details")


class GetCatalogClientScriptParams(BaseModel):
    """Parameters for getting a specific catalog client script."""

    script_id: str = Field(..., description="Catalog client script sys_id")


class DeleteCatalogClientScriptParams(BaseModel):
    """Parameters for deleting a catalog client script."""

    script_id: str = Field(..., description="Catalog client script sys_id")


class CatalogClientScriptResponse(BaseModel):
    """Response from catalog client script operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_catalog_client_script(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateCatalogClientScriptParams,
) -> CatalogClientScriptResponse:
    """
    Create a new catalog client script in the catalog_script_client table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the catalog client script

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating catalog client script: {params.name}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_script_client"
    
    # Prepare request body
    body = {
        "name": params.name,
        "script": params.script,
        "active": params.active if params.active is not None else True,
        "applies_catalog": params.applies_catalog if params.applies_catalog is not None else False,
        "applies_req_item": params.applies_req_item if params.applies_req_item is not None else False,
        "applies_sc_task": params.applies_sc_task if params.applies_sc_task is not None else False,
        "applies_target_record": params.applies_target_record if params.applies_target_record is not None else False,
        "va_supported": params.va_supported if params.va_supported is not None else False,
    }
    
    if params.cat_item is not None:
        body["cat_item"] = params.cat_item
    if params.variable_set is not None:
        body["variable_set"] = params.variable_set
    if params.cat_variable is not None:
        body["cat_variable"] = params.cat_variable
    if params.applies_to is not None:
        body["applies_to"] = params.applies_to
    if params.ui_type is not None:
        body["ui_type"] = params.ui_type
    if params.type is not None:
        body["type"] = params.type
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        script = result.get("result", {})
        
        # Format the response
        formatted_script = {
            "sys_id": script.get("sys_id", ""),
            "name": script.get("name", ""),
            "script": script.get("script", ""),
            "cat_item": script.get("cat_item", ""),
            "variable_set": script.get("variable_set", ""),
            "cat_variable": script.get("cat_variable", ""),
            "applies_to": script.get("applies_to", ""),
            "applies_catalog": script.get("applies_catalog", ""),
            "applies_req_item": script.get("applies_req_item", ""),
            "applies_sc_task": script.get("applies_sc_task", ""),
            "applies_target_record": script.get("applies_target_record", ""),
            "va_supported": script.get("va_supported", ""),
            "active": script.get("active", ""),
            "ui_type": script.get("ui_type", ""),
            "type": script.get("type", ""),
            "sys_created_on": script.get("sys_created_on", ""),
        }
        
        return CatalogClientScriptResponse(
            success=True,
            message=f"Created catalog client script: {params.name}",
            data=formatted_script,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating catalog client script: {str(e)}")
        return CatalogClientScriptResponse(
            success=False,
            message=f"Error creating catalog client script: {str(e)}",
            data=None,
        )


def update_catalog_client_script(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateCatalogClientScriptParams,
) -> CatalogClientScriptResponse:
    """
    Update an existing catalog client script in the catalog_script_client table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the catalog client script

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating catalog client script: {params.script_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_script_client/{params.script_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.name is not None:
        body["name"] = params.name
    if params.script is not None:
        body["script"] = params.script
    if params.cat_item is not None:
        body["cat_item"] = params.cat_item
    if params.variable_set is not None:
        body["variable_set"] = params.variable_set
    if params.cat_variable is not None:
        body["cat_variable"] = params.cat_variable
    if params.applies_to is not None:
        body["applies_to"] = params.applies_to
    if params.applies_catalog is not None:
        body["applies_catalog"] = params.applies_catalog
    if params.applies_req_item is not None:
        body["applies_req_item"] = params.applies_req_item
    if params.applies_sc_task is not None:
        body["applies_sc_task"] = params.applies_sc_task
    if params.applies_target_record is not None:
        body["applies_target_record"] = params.applies_target_record
    if params.va_supported is not None:
        body["va_supported"] = params.va_supported
    if params.active is not None:
        body["active"] = params.active
    if params.ui_type is not None:
        body["ui_type"] = params.ui_type
    if params.type is not None:
        body["type"] = params.type
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        script = result.get("result", {})
        
        # Format the response
        formatted_script = {
            "sys_id": script.get("sys_id", ""),
            "name": script.get("name", ""),
            "script": script.get("script", ""),
            "cat_item": script.get("cat_item", ""),
            "variable_set": script.get("variable_set", ""),
            "cat_variable": script.get("cat_variable", ""),
            "applies_to": script.get("applies_to", ""),
            "applies_catalog": script.get("applies_catalog", ""),
            "applies_req_item": script.get("applies_req_item", ""),
            "applies_sc_task": script.get("applies_sc_task", ""),
            "applies_target_record": script.get("applies_target_record", ""),
            "va_supported": script.get("va_supported", ""),
            "active": script.get("active", ""),
            "ui_type": script.get("ui_type", ""),
            "type": script.get("type", ""),
            "sys_updated_on": script.get("sys_updated_on", ""),
        }
        
        return CatalogClientScriptResponse(
            success=True,
            message=f"Updated catalog client script: {params.script_id}",
            data=formatted_script,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating catalog client script: {str(e)}")
        return CatalogClientScriptResponse(
            success=False,
            message=f"Error updating catalog client script: {str(e)}",
            data=None,
        )


def list_catalog_client_scripts(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListCatalogClientScriptsParams,
) -> Dict[str, Any]:
    """
    List catalog client scripts from the catalog_script_client table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing catalog client scripts

    Returns:
        Dictionary containing catalog client scripts and metadata
    """
    logger.info("Listing catalog client scripts")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_script_client"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,cat_item,variable_set,cat_variable,applies_to,applies_catalog,applies_req_item,applies_sc_task,applies_target_record,va_supported,active,ui_type,type,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.cat_item:
        filters.append(f"cat_item={params.cat_item}")
    if params.variable_set:
        filters.append(f"variable_set={params.variable_set}")
    if params.cat_variable:
        filters.append(f"cat_variableLIKE{params.cat_variable}")
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    if params.query:
        filters.append(f"nameLIKE{params.query}^ORcat_variableLIKE{params.query}")
    
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
        scripts = result.get("result", [])
        
        # Format the response
        formatted_scripts = []
        for script in scripts:
            formatted_scripts.append({
                "sys_id": script.get("sys_id", ""),
                "name": script.get("name", ""),
                "cat_item": script.get("cat_item", ""),
                "variable_set": script.get("variable_set", ""),
                "cat_variable": script.get("cat_variable", ""),
                "applies_to": script.get("applies_to", ""),
                "applies_catalog": script.get("applies_catalog", ""),
                "applies_req_item": script.get("applies_req_item", ""),
                "applies_sc_task": script.get("applies_sc_task", ""),
                "applies_target_record": script.get("applies_target_record", ""),
                "va_supported": script.get("va_supported", ""),
                "active": script.get("active", ""),
                "ui_type": script.get("ui_type", ""),
                "type": script.get("type", ""),
                "sys_created_on": script.get("sys_created_on", ""),
                "sys_updated_on": script.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_scripts)} catalog client scripts",
            "scripts": formatted_scripts,
            "total": len(formatted_scripts),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing catalog client scripts: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing catalog client scripts: {str(e)}",
            "scripts": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_catalog_client_script(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetCatalogClientScriptParams,
) -> CatalogClientScriptResponse:
    """
    Get a specific catalog client script from the catalog_script_client table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the catalog client script

    Returns:
        Response containing the catalog client script details
    """
    logger.info(f"Getting catalog client script: {params.script_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_script_client/{params.script_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,name,script,cat_item,variable_set,cat_variable,applies_to,applies_catalog,applies_req_item,applies_sc_task,applies_target_record,va_supported,active,ui_type,type,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        script = result.get("result", {})
        
        if not script:
            return CatalogClientScriptResponse(
                success=False,
                message=f"Catalog client script not found: {params.script_id}",
                data=None,
            )
        
        # Format the response
        formatted_script = {
            "sys_id": script.get("sys_id", ""),
            "name": script.get("name", ""),
            "script": script.get("script", ""),
            "cat_item": script.get("cat_item", ""),
            "variable_set": script.get("variable_set", ""),
            "cat_variable": script.get("cat_variable", ""),
            "applies_to": script.get("applies_to", ""),
            "applies_catalog": script.get("applies_catalog", ""),
            "applies_req_item": script.get("applies_req_item", ""),
            "applies_sc_task": script.get("applies_sc_task", ""),
            "applies_target_record": script.get("applies_target_record", ""),
            "va_supported": script.get("va_supported", ""),
            "active": script.get("active", ""),
            "ui_type": script.get("ui_type", ""),
            "type": script.get("type", ""),
            "sys_created_on": script.get("sys_created_on", ""),
            "sys_updated_on": script.get("sys_updated_on", ""),
        }
        
        return CatalogClientScriptResponse(
            success=True,
            message=f"Retrieved catalog client script: {script.get('name', '')}",
            data=formatted_script,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting catalog client script: {str(e)}")
        return CatalogClientScriptResponse(
            success=False,
            message=f"Error getting catalog client script: {str(e)}",
            data=None,
        )


def delete_catalog_client_script(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteCatalogClientScriptParams,
) -> CatalogClientScriptResponse:
    """
    Delete a catalog client script from the catalog_script_client table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the catalog client script

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting catalog client script: {params.script_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/catalog_script_client/{params.script_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return CatalogClientScriptResponse(
            success=True,
            message=f"Deleted catalog client script: {params.script_id}",
            data={"deleted_script_id": params.script_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting catalog client script: {str(e)}")
        return CatalogClientScriptResponse(
            success=False,
            message=f"Error deleting catalog client script: {str(e)}",
            data=None,
        )


def clone_catalog_client_script(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: Dict[str, Any],
) -> CatalogClientScriptResponse:
    """
    Clone an existing catalog client script in the catalog_script_client table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters containing script_id and new_name

    Returns:
        Response containing the result of the operation
    """
    source_script_id = params.get("script_id")
    new_name = params.get("new_name")
    
    if not source_script_id or not new_name:
        return CatalogClientScriptResponse(
            success=False,
            message="Both script_id and new_name are required for cloning",
            data=None,
        )
    
    logger.info(f"Cloning catalog client script: {source_script_id} as {new_name}")
    
    # First, get the source script
    get_params = GetCatalogClientScriptParams(script_id=source_script_id)
    source_response = get_catalog_client_script(config, auth_manager, get_params)
    
    if not source_response.success or not source_response.data:
        return CatalogClientScriptResponse(
            success=False,
            message=f"Could not retrieve source script: {source_script_id}",
            data=None,
        )
    
    # Create the cloned script
    source_data = source_response.data
    create_params = CreateCatalogClientScriptParams(
        name=new_name,
        script=source_data.get("script", ""),
        cat_item=source_data.get("cat_item"),
        variable_set=source_data.get("variable_set"),
        cat_variable=source_data.get("cat_variable"),
        applies_to=source_data.get("applies_to"),
        applies_catalog=bool(source_data.get("applies_catalog")),
        applies_req_item=bool(source_data.get("applies_req_item")),
        applies_sc_task=bool(source_data.get("applies_sc_task")),
        applies_target_record=bool(source_data.get("applies_target_record")),
        va_supported=bool(source_data.get("va_supported")),
        active=bool(source_data.get("active")),
        ui_type=source_data.get("ui_type"),
        type=source_data.get("type"),
    )
    
    return create_catalog_client_script(config, auth_manager, create_params)