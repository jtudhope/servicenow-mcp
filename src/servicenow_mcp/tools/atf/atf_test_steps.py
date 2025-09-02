"""
ATF Test Steps tools for the ServiceNow MCP server.

This module provides tools for managing ATF (Automated Test Framework) test steps that are stored 
in the sys_atf_step table. ATF test steps are individual actions within an ATF test that define 
specific operations to be performed during automated testing.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateAtfTestStepParams(BaseModel):
    """Parameters for creating an ATF test step."""

    test: str = Field(..., description="Test sys_id this step belongs to")
    step_config: str = Field(..., description="Step config sys_id that defines the step type")
    display_name: Optional[str] = Field(None, description="Display name for the test step")
    description: Optional[str] = Field(None, description="Description of the test step")
    notes: Optional[str] = Field(None, description="Notes for the test step")
    order: Optional[int] = Field(None, description="Execution order of the step within the test")
    table: Optional[str] = Field(None, description="Target table for the test step")
    timeout: Optional[str] = Field(None, description="Timeout duration for the step (e.g., '30 seconds')")
    inputs: Optional[str] = Field(None, description="Input variables for the step (JSON format)")
    callable_outputs: Optional[str] = Field(None, description="Reusable output variables (JSON format)")
    active: Optional[bool] = Field(True, description="Whether the test step is active")
    snapshot: Optional[str] = Field(None, description="Snapshot sys_id for UI-based steps")


class UpdateAtfTestStepParams(BaseModel):
    """Parameters for updating an ATF test step."""

    step_id: str = Field(..., description="ATF test step sys_id")
    display_name: Optional[str] = Field(None, description="Updated display name")
    description: Optional[str] = Field(None, description="Updated description")
    notes: Optional[str] = Field(None, description="Updated notes")
    order: Optional[int] = Field(None, description="Updated execution order")
    table: Optional[str] = Field(None, description="Updated target table")
    timeout: Optional[str] = Field(None, description="Updated timeout duration")
    inputs: Optional[str] = Field(None, description="Updated input variables (JSON format)")
    callable_outputs: Optional[str] = Field(None, description="Updated reusable output variables (JSON format)")
    active: Optional[bool] = Field(None, description="Updated active status")
    snapshot: Optional[str] = Field(None, description="Updated snapshot sys_id")


class ListAtfTestStepsParams(BaseModel):
    """Parameters for listing ATF test steps."""

    limit: int = Field(10, description="Maximum number of steps to return")
    offset: int = Field(0, description="Offset for pagination")
    test: Optional[str] = Field(None, description="Filter by test sys_id")
    step_config: Optional[str] = Field(None, description="Filter by step config sys_id")
    table: Optional[str] = Field(None, description="Filter by target table")
    active: Optional[bool] = Field(None, description="Filter by active status")
    query: Optional[str] = Field(None, description="Search query for step details")


class GetAtfTestStepParams(BaseModel):
    """Parameters for getting a specific ATF test step."""

    step_id: str = Field(..., description="ATF test step sys_id")


class DeleteAtfTestStepParams(BaseModel):
    """Parameters for deleting an ATF test step."""

    step_id: str = Field(..., description="ATF test step sys_id")


class CloneAtfTestStepParams(BaseModel):
    """Parameters for cloning an ATF test step."""

    source_step_id: str = Field(..., description="Source test step sys_id to clone")
    target_test: Optional[str] = Field(None, description="Target test sys_id (defaults to same test)")
    new_display_name: Optional[str] = Field(None, description="Display name for the cloned step")
    new_order: Optional[int] = Field(None, description="Execution order for the cloned step")


class ReorderAtfTestStepsParams(BaseModel):
    """Parameters for reordering ATF test steps."""

    test_id: str = Field(..., description="Test sys_id to reorder steps within")
    step_order: List[str] = Field(..., description="List of step sys_ids in desired execution order")


class AtfTestStepResponse(BaseModel):
    """Response from ATF test step operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


def create_atf_test_step(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateAtfTestStepParams,
) -> AtfTestStepResponse:
    """
    Create a new ATF test step in the sys_atf_step table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for creating the ATF test step

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Creating ATF test step for test: {params.test}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_atf_step"
    
    # Prepare request body
    body = {
        "test": params.test,
        "step_config": params.step_config,
        "active": params.active if params.active is not None else True,
    }
    
    if params.display_name is not None:
        body["display_name"] = params.display_name
    if params.description is not None:
        body["description"] = params.description
    if params.notes is not None:
        body["notes"] = params.notes
    if params.order is not None:
        body["order"] = params.order
    if params.table is not None:
        body["table"] = params.table
    if params.timeout is not None:
        body["timeout"] = params.timeout
    if params.inputs is not None:
        body["inputs"] = params.inputs
    if params.callable_outputs is not None:
        body["callable_outputs"] = params.callable_outputs
    if params.snapshot is not None:
        body["snapshot"] = params.snapshot
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        step = result.get("result", {})
        
        # Format the response
        formatted_step = {
            "sys_id": step.get("sys_id", ""),
            "test": step.get("test", ""),
            "step_config": step.get("step_config", ""),
            "display_name": step.get("display_name", ""),
            "description": step.get("description", ""),
            "notes": step.get("notes", ""),
            "order": step.get("order", ""),
            "table": step.get("table", ""),
            "timeout": step.get("timeout", ""),
            "inputs": step.get("inputs", ""),
            "callable_outputs": step.get("callable_outputs", ""),
            "active": step.get("active", ""),
            "snapshot": step.get("snapshot", ""),
            "sys_created_on": step.get("sys_created_on", ""),
        }
        
        return AtfTestStepResponse(
            success=True,
            message=f"Created ATF test step: {step.get('display_name', 'Unnamed step')}",
            data=formatted_step,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating ATF test step: {str(e)}")
        return AtfTestStepResponse(
            success=False,
            message=f"Error creating ATF test step: {str(e)}",
            data=None,
        )


def update_atf_test_step(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateAtfTestStepParams,
) -> AtfTestStepResponse:
    """
    Update an existing ATF test step in the sys_atf_step table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for updating the ATF test step

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Updating ATF test step: {params.step_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_atf_step/{params.step_id}"
    
    # Prepare request body with only the provided parameters
    body = {}
    if params.display_name is not None:
        body["display_name"] = params.display_name
    if params.description is not None:
        body["description"] = params.description
    if params.notes is not None:
        body["notes"] = params.notes
    if params.order is not None:
        body["order"] = params.order
    if params.table is not None:
        body["table"] = params.table
    if params.timeout is not None:
        body["timeout"] = params.timeout
    if params.inputs is not None:
        body["inputs"] = params.inputs
    if params.callable_outputs is not None:
        body["callable_outputs"] = params.callable_outputs
    if params.active is not None:
        body["active"] = params.active
    if params.snapshot is not None:
        body["snapshot"] = params.snapshot
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.patch(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        step = result.get("result", {})
        
        # Format the response
        formatted_step = {
            "sys_id": step.get("sys_id", ""),
            "test": step.get("test", ""),
            "step_config": step.get("step_config", ""),
            "display_name": step.get("display_name", ""),
            "description": step.get("description", ""),
            "notes": step.get("notes", ""),
            "order": step.get("order", ""),
            "table": step.get("table", ""),
            "timeout": step.get("timeout", ""),
            "inputs": step.get("inputs", ""),
            "callable_outputs": step.get("callable_outputs", ""),
            "active": step.get("active", ""),
            "snapshot": step.get("snapshot", ""),
            "sys_updated_on": step.get("sys_updated_on", ""),
        }
        
        return AtfTestStepResponse(
            success=True,
            message=f"Updated ATF test step: {params.step_id}",
            data=formatted_step,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating ATF test step: {str(e)}")
        return AtfTestStepResponse(
            success=False,
            message=f"Error updating ATF test step: {str(e)}",
            data=None,
        )


def list_atf_test_steps(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListAtfTestStepsParams,
) -> Dict[str, Any]:
    """
    List ATF test steps from the sys_atf_step table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for listing ATF test steps

    Returns:
        Dictionary containing ATF test steps and metadata
    """
    logger.info("Listing ATF test steps")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_atf_step"
    
    # Prepare query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,test,step_config,display_name,description,notes,order,table,timeout,inputs,callable_outputs,active,snapshot,sys_created_on,sys_updated_on",
    }
    
    # Add filters
    filters = []
    if params.test:
        filters.append(f"test={params.test}")
    if params.step_config:
        filters.append(f"step_config={params.step_config}")
    if params.table:
        filters.append(f"table={params.table}")
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    if params.query:
        filters.append(f"display_nameLIKE{params.query}^ORdescriptionLIKE{params.query}^ORnotesLIKE{params.query}")
    
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
        steps = result.get("result", [])
        
        # Format the response
        formatted_steps = []
        for step in steps:
            formatted_steps.append({
                "sys_id": step.get("sys_id", ""),
                "test": step.get("test", ""),
                "step_config": step.get("step_config", ""),
                "display_name": step.get("display_name", ""),
                "description": step.get("description", ""),
                "notes": step.get("notes", ""),
                "order": step.get("order", ""),
                "table": step.get("table", ""),
                "timeout": step.get("timeout", ""),
                "inputs": step.get("inputs", ""),
                "callable_outputs": step.get("callable_outputs", ""),
                "active": step.get("active", ""),
                "snapshot": step.get("snapshot", ""),
                "sys_created_on": step.get("sys_created_on", ""),
                "sys_updated_on": step.get("sys_updated_on", ""),
            })
        
        return {
            "success": True,
            "message": f"Retrieved {len(formatted_steps)} ATF test steps",
            "steps": formatted_steps,
            "total": len(formatted_steps),
            "limit": params.limit,
            "offset": params.offset,
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing ATF test steps: {str(e)}")
        return {
            "success": False,
            "message": f"Error listing ATF test steps: {str(e)}",
            "steps": [],
            "total": 0,
            "limit": params.limit,
            "offset": params.offset,
        }


def get_atf_test_step(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetAtfTestStepParams,
) -> AtfTestStepResponse:
    """
    Get a specific ATF test step from the sys_atf_step table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for getting the ATF test step

    Returns:
        Response containing the ATF test step details
    """
    logger.info(f"Getting ATF test step: {params.step_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_atf_step/{params.step_id}"
    
    # Prepare query parameters
    query_params = {
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "sys_id,test,step_config,display_name,description,notes,order,table,timeout,inputs,callable_outputs,active,snapshot,copied_from,warning_message,sys_created_on,sys_updated_on",
    }
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        step = result.get("result", {})
        
        if not step:
            return AtfTestStepResponse(
                success=False,
                message=f"ATF test step not found: {params.step_id}",
                data=None,
            )
        
        # Format the response
        formatted_step = {
            "sys_id": step.get("sys_id", ""),
            "test": step.get("test", ""),
            "step_config": step.get("step_config", ""),
            "display_name": step.get("display_name", ""),
            "description": step.get("description", ""),
            "notes": step.get("notes", ""),
            "order": step.get("order", ""),
            "table": step.get("table", ""),
            "timeout": step.get("timeout", ""),
            "inputs": step.get("inputs", ""),
            "callable_outputs": step.get("callable_outputs", ""),
            "active": step.get("active", ""),
            "snapshot": step.get("snapshot", ""),
            "copied_from": step.get("copied_from", ""),
            "warning_message": step.get("warning_message", ""),
            "sys_created_on": step.get("sys_created_on", ""),
            "sys_updated_on": step.get("sys_updated_on", ""),
        }
        
        return AtfTestStepResponse(
            success=True,
            message=f"Retrieved ATF test step: {step.get('display_name', 'Unnamed step')}",
            data=formatted_step,
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting ATF test step: {str(e)}")
        return AtfTestStepResponse(
            success=False,
            message=f"Error getting ATF test step: {str(e)}",
            data=None,
        )


def delete_atf_test_step(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteAtfTestStepParams,
) -> AtfTestStepResponse:
    """
    Delete an ATF test step from the sys_atf_step table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for deleting the ATF test step

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Deleting ATF test step: {params.step_id}")
    
    # Build the API URL
    url = f"{config.instance_url}/api/now/table/sys_atf_step/{params.step_id}"
    
    # Make the API request
    headers = auth_manager.get_headers()
    headers["Accept"] = "application/json"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        return AtfTestStepResponse(
            success=True,
            message=f"Deleted ATF test step: {params.step_id}",
            data={"deleted_step_id": params.step_id},
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting ATF test step: {str(e)}")
        return AtfTestStepResponse(
            success=False,
            message=f"Error deleting ATF test step: {str(e)}",
            data=None,
        )


def clone_atf_test_step(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CloneAtfTestStepParams,
) -> AtfTestStepResponse:
    """
    Clone an existing ATF test step in the sys_atf_step table.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for cloning the ATF test step

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Cloning ATF test step: {params.source_step_id}")
    
    # First, get the source step
    get_params = GetAtfTestStepParams(step_id=params.source_step_id)
    source_response = get_atf_test_step(config, auth_manager, get_params)
    
    if not source_response.success or not source_response.data:
        return AtfTestStepResponse(
            success=False,
            message=f"Could not retrieve source step: {params.source_step_id}",
            data=None,
        )
    
    # Create the cloned step
    source_data = source_response.data
    target_test = params.target_test if params.target_test else source_data.get("test")
    
    create_params = CreateAtfTestStepParams(
        test=target_test,
        step_config=source_data.get("step_config", ""),
        display_name=params.new_display_name if params.new_display_name else f"{source_data.get('display_name', 'Unnamed step')} (Copy)",
        description=source_data.get("description"),
        notes=source_data.get("notes"),
        order=params.new_order if params.new_order else int(source_data.get("order", 0)) + 1,
        table=source_data.get("table"),
        timeout=source_data.get("timeout"),
        inputs=source_data.get("inputs"),
        callable_outputs=source_data.get("callable_outputs"),
        active=bool(source_data.get("active")),
        snapshot=source_data.get("snapshot"),
    )
    
    clone_response = create_atf_test_step(config, auth_manager, create_params)
    
    if clone_response.success and clone_response.data:
        # Update the cloned step to reference the source
        update_params = UpdateAtfTestStepParams(
            step_id=clone_response.data.get("sys_id", ""),
        )
        # Note: copied_from field is read-only, so we can't set it via API
        # This would typically be handled by ServiceNow's cloning mechanism
        
    return clone_response


def reorder_atf_test_steps(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ReorderAtfTestStepsParams,
) -> AtfTestStepResponse:
    """
    Reorder ATF test steps within a test by updating their order values.

    Args:
        config: Server configuration
        auth_manager: Authentication manager
        params: Parameters for reordering ATF test steps

    Returns:
        Response containing the result of the operation
    """
    logger.info(f"Reordering ATF test steps for test: {params.test_id}")
    
    try:
        updated_steps = []
        
        # Update each step with its new order
        for index, step_id in enumerate(params.step_order):
            new_order = (index + 1) * 100  # Leave gaps for future insertions
            
            update_params = UpdateAtfTestStepParams(
                step_id=step_id,
                order=new_order,
            )
            
            response = update_atf_test_step(config, auth_manager, update_params)
            if response.success:
                updated_steps.append({
                    "step_id": step_id,
                    "new_order": new_order,
                })
            else:
                return AtfTestStepResponse(
                    success=False,
                    message=f"Failed to reorder step {step_id}: {response.message}",
                    data=None,
                )
        
        return AtfTestStepResponse(
            success=True,
            message=f"Successfully reordered {len(updated_steps)} ATF test steps",
            data={
                "test_id": params.test_id,
                "updated_steps": updated_steps,
            },
        )
    
    except Exception as e:
        logger.error(f"Error reordering ATF test steps: {str(e)}")
        return AtfTestStepResponse(
            success=False,
            message=f"Error reordering ATF test steps: {str(e)}",
            data=None,
        )