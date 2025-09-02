"""
Assignment Rule tools for the ServiceNow MCP server.

This module provides tools for managing default assignment rules stored in the 
sysrule_assignment table.
"""

import logging
from typing import Optional, List, Dict, Any

import requests

from servicenow_mcp.auth.session_manager import get_session
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateAssignmentRuleParams(BaseModel):
    """Parameters for creating an assignment rule."""

    name: str = Field(..., description="Name of the assignment rule")
    table: str = Field(..., description="Table the rule applies to")
    script: str = Field(..., description="Assignment script that determines assignment logic")
    condition: Optional[str] = Field(None, description="Condition query for when to apply the rule")
    order: Optional[int] = Field(None, description="Execution order of the rule (lower numbers run first)")
    active: bool = Field(True, description="Whether the assignment rule is active")
    description: Optional[str] = Field(None, description="Description of the assignment rule")
    inherited: bool = Field(False, description="Whether rule applies to extended tables")
    when_to_apply: str = Field("async", description="When to apply rule (sync, async, both)")


class UpdateAssignmentRuleParams(BaseModel):
    """Parameters for updating an assignment rule."""

    rule_id: str = Field(..., description="Assignment rule ID or sys_id")
    name: Optional[str] = Field(None, description="Updated name of the assignment rule")
    table: Optional[str] = Field(None, description="Updated table the rule applies to")
    script: Optional[str] = Field(None, description="Updated assignment script")
    condition: Optional[str] = Field(None, description="Updated condition query")
    order: Optional[int] = Field(None, description="Updated execution order")
    active: Optional[bool] = Field(None, description="Updated active status")
    description: Optional[str] = Field(None, description="Updated description")
    inherited: Optional[bool] = Field(None, description="Updated inherited setting")
    when_to_apply: Optional[str] = Field(None, description="Updated when to apply setting")


class ListAssignmentRulesParams(BaseModel):
    """Parameters for listing assignment rules."""

    table: Optional[str] = Field(None, description="Filter by table")
    active: Optional[bool] = Field(None, description="Filter by active status")
    inherited: Optional[bool] = Field(None, description="Filter by inherited status")
    when_to_apply: Optional[str] = Field(None, description="Filter by when to apply setting")
    limit: int = Field(10, description="Maximum number of rules to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetAssignmentRuleParams(BaseModel):
    """Parameters for getting a specific assignment rule."""

    rule_id: str = Field(..., description="Assignment rule ID or sys_id")


class DeleteAssignmentRuleParams(BaseModel):
    """Parameters for deleting an assignment rule."""

    rule_id: str = Field(..., description="Assignment rule ID or sys_id")


class AssignmentRuleResponse(BaseModel):
    """Response from assignment rule operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    rule_id: Optional[str] = Field(None, description="Assignment rule sys_id")
    rule_data: Optional[Dict[str, Any]] = Field(None, description="Assignment rule data")


class ListAssignmentRulesResponse(BaseModel):
    """Response from list assignment rules operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    rules: List[Dict[str, Any]] = Field(default_factory=list, description="List of assignment rules")
    total_count: int = Field(0, description="Total number of assignment rules")


def create_assignment_rule(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateAssignmentRuleParams,
) -> AssignmentRuleResponse:
    """
    Create a new assignment rule in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the assignment rule.

    Returns:
        Response with assignment rule creation result.
    """
    api_url = f"{config.api_url}/table/sysrule_assignment"

    # Build request data
    data = {
        "name": params.name,
        "table": params.table,
        "script": params.script,
        "active": params.active,
        "inherited": params.inherited,
        "when_to_apply": params.when_to_apply,
    }

    if params.condition:
        data["condition"] = params.condition
    if params.order is not None:
        data["order"] = params.order
    if params.description:
        data["description"] = params.description

    try:
        session = get_session()
        
        response = session.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )

        logger.info("Received Response from ServiceNow")
        logger.info(response.cookies)
        logger.info(response.headers)
        logger.info("Received Response from ServiceNow Complete")

        response.raise_for_status()

        result = response.json().get("result", {})

        return AssignmentRuleResponse(
            success=True,
            message="Assignment rule created successfully",
            rule_id=result.get("sys_id"),
            rule_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create assignment rule: {e}")
        return AssignmentRuleResponse(
            success=False,
            message=f"Failed to create assignment rule: {str(e)}",
        )


def update_assignment_rule(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateAssignmentRuleParams,
) -> AssignmentRuleResponse:
    """
    Update an existing assignment rule in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the assignment rule.

    Returns:
        Response with assignment rule update result.
    """
    api_url = f"{config.api_url}/table/sysrule_assignment/{params.rule_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.table is not None:
        data["table"] = params.table
    if params.script is not None:
        data["script"] = params.script
    if params.condition is not None:
        data["condition"] = params.condition
    if params.order is not None:
        data["order"] = params.order
    if params.active is not None:
        data["active"] = params.active
    if params.description is not None:
        data["description"] = params.description
    if params.inherited is not None:
        data["inherited"] = params.inherited
    if params.when_to_apply is not None:
        data["when_to_apply"] = params.when_to_apply

    try:
        session = get_session()
        response = session.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AssignmentRuleResponse(
            success=True,
            message="Assignment rule updated successfully",
            rule_id=result.get("sys_id"),
            rule_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update assignment rule: {e}")
        return AssignmentRuleResponse(
            success=False,
            message=f"Failed to update assignment rule: {str(e)}",
        )


def list_assignment_rules(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListAssignmentRulesParams,
) -> ListAssignmentRulesResponse:
    """
    List assignment rules from ServiceNow with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing assignment rules.

    Returns:
        Response with list of assignment rules.
    """
    api_url = f"{config.api_url}/table/sysrule_assignment"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build encoded query
    query_parts = []
    
    if params.table:
        query_parts.append(f"table={params.table}")
    if params.active is not None:
        query_parts.append(f"active={params.active}")
    if params.inherited is not None:
        query_parts.append(f"inherited={params.inherited}")
    if params.when_to_apply:
        query_parts.append(f"when_to_apply={params.when_to_apply}")
    if params.query:
        query_parts.append(params.query)

    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)

    try:
        session = get_session()
        response = session.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return ListAssignmentRulesResponse(
            success=True,
            message=f"Found {len(result)} assignment rules",
            rules=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list assignment rules: {e}")
        return ListAssignmentRulesResponse(
            success=False,
            message=f"Failed to list assignment rules: {str(e)}",
        )


def get_assignment_rule(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetAssignmentRuleParams,
) -> AssignmentRuleResponse:
    """
    Get a specific assignment rule from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the assignment rule.

    Returns:
        Response with assignment rule data.
    """
    api_url = f"{config.api_url}/table/sysrule_assignment/{params.rule_id}"

    try:
        session = get_session()
        response = session.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AssignmentRuleResponse(
            success=True,
            message="Assignment rule retrieved successfully",
            rule_id=result.get("sys_id"),
            rule_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get assignment rule: {e}")
        return AssignmentRuleResponse(
            success=False,
            message=f"Failed to get assignment rule: {str(e)}",
        )


def delete_assignment_rule(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteAssignmentRuleParams,
) -> AssignmentRuleResponse:
    """
    Delete an assignment rule from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the assignment rule.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sysrule_assignment/{params.rule_id}"

    try:
        session = get_session()
        response = session.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return AssignmentRuleResponse(
            success=True,
            message="Assignment rule deleted successfully",
            rule_id=params.rule_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete assignment rule: {e}")
        return AssignmentRuleResponse(
            success=False,
            message=f"Failed to delete assignment rule: {str(e)}",
        )