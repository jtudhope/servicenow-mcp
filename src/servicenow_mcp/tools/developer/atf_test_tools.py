"""
ATF (Automated Test Framework) tools for the ServiceNow MCP server.

This module provides tools for managing ATF tests stored in the sys_atf_test table,
including CRUD operations and test execution functionality.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.session_manager import get_session
from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateAtfTestParams(BaseModel):
    """Parameters for creating an ATF test."""

    name: str = Field(..., description="Name of the ATF test")
    description: Optional[str] = Field(None, description="Description of the ATF test")
    active: bool = Field(True, description="Whether the test is active")
    application: Optional[str] = Field(None, description="Scoped application sys_id")
    fail_on_server_error: bool = Field(False, description="Whether to fail the test on server error")
    enable_parameterized_testing: bool = Field(False, description="Whether to enable parameterized testing")
    copied_from: Optional[str] = Field(None, description="Source test sys_id if copied from another test")


class UpdateAtfTestParams(BaseModel):
    """Parameters for updating an ATF test."""

    test_id: str = Field(..., description="ATF test sys_id")
    name: Optional[str] = Field(None, description="Updated name of the ATF test")
    description: Optional[str] = Field(None, description="Updated description of the ATF test")
    active: Optional[bool] = Field(None, description="Updated active status")
    application: Optional[str] = Field(None, description="Updated scoped application sys_id")
    fail_on_server_error: Optional[bool] = Field(None, description="Updated fail on server error setting")
    enable_parameterized_testing: Optional[bool] = Field(None, description="Updated parameterized testing setting")


class GetAtfTestParams(BaseModel):
    """Parameters for getting an ATF test."""

    test_id: str = Field(..., description="ATF test sys_id")


class ListAtfTestsParams(BaseModel):
    """Parameters for listing ATF tests."""

    active: Optional[bool] = Field(None, description="Filter by active status")
    application: Optional[str] = Field(None, description="Filter by scoped application")
    name_contains: Optional[str] = Field(None, description="Filter by name containing text")
    limit: int = Field(10, description="Maximum number of tests to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class DeleteAtfTestParams(BaseModel):
    """Parameters for deleting an ATF test."""

    test_id: str = Field(..., description="ATF test sys_id")


class RunAtfTestParams(BaseModel):
    """Parameters for running an ATF test."""

    test_id: str = Field(..., description="ATF test sys_id to execute")
    suite_id: Optional[str] = Field(None, description="Optional test suite sys_id to run as part of")


class GetAtfTestResultsParams(BaseModel):
    """Parameters for getting ATF test results."""

    test_id: Optional[str] = Field(None, description="ATF test sys_id to get results for")
    suite_result_id: Optional[str] = Field(None, description="Suite result sys_id to get results for")
    limit: int = Field(10, description="Maximum number of results to return")
    offset: int = Field(0, description="Offset for pagination")


class AtfTestResponse(BaseModel):
    """Response from ATF test operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    test_id: Optional[str] = Field(None, description="ATF test sys_id")
    test_name: Optional[str] = Field(None, description="ATF test name")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class AtfTestListResponse(BaseModel):
    """Response from listing ATF tests."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    tests: List[Dict[str, Any]] = Field(default_factory=list, description="List of ATF tests")
    total_count: int = Field(0, description="Total number of tests")


class AtfTestExecutionResponse(BaseModel):
    """Response from ATF test execution."""

    success: bool = Field(..., description="Whether the execution was triggered successfully")
    message: str = Field(..., description="Message describing the result")
    execution_id: Optional[str] = Field(None, description="Execution tracker sys_id")
    status: Optional[str] = Field(None, description="Execution status")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional execution data")


class AtfTestResultsResponse(BaseModel):
    """Response from getting ATF test results."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="List of test results")
    total_count: int = Field(0, description="Total number of results")


def create_atf_test(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateAtfTestParams,
) -> AtfTestResponse:
    """
    Create a new ATF test in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the ATF test.

    Returns:
        Response with ATF test creation result.
    """
    api_url = f"{config.api_url}/table/sys_atf_test"

    # Build request data
    data = {
        "name": params.name,
        "active": params.active,
        "fail_on_server_error": params.fail_on_server_error,
        "enable_parameterized_testing": params.enable_parameterized_testing,
    }

    if params.description:
        data["description"] = params.description
    if params.application:
        data["sys_scope"] = params.application
    if params.copied_from:
        data["copied_from"] = params.copied_from

    # Make request
    try:
        session = get_session()
        response = session.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AtfTestResponse(
            success=True,
            message="ATF test created successfully",
            test_id=result.get("sys_id", ""),
            test_name=result.get("name", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create ATF test: {e}")
        return AtfTestResponse(
            success=False,
            message=f"Failed to create ATF test: {str(e)}",
        )


def update_atf_test(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateAtfTestParams,
) -> AtfTestResponse:
    """
    Update an existing ATF test in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the ATF test.

    Returns:
        Response with ATF test update result.
    """
    api_url = f"{config.api_url}/table/sys_atf_test/{params.test_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.description is not None:
        data["description"] = params.description
    if params.active is not None:
        data["active"] = params.active
    if params.application is not None:
        data["sys_scope"] = params.application
    if params.fail_on_server_error is not None:
        data["fail_on_server_error"] = params.fail_on_server_error
    if params.enable_parameterized_testing is not None:
        data["enable_parameterized_testing"] = params.enable_parameterized_testing

    # Make request
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

        return AtfTestResponse(
            success=True,
            message="ATF test updated successfully",
            test_id=result.get("sys_id", ""),
            test_name=result.get("name", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update ATF test: {e}")
        return AtfTestResponse(
            success=False,
            message=f"Failed to update ATF test: {str(e)}",
        )


def get_atf_test(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetAtfTestParams,
) -> AtfTestResponse:
    """
    Get details of a specific ATF test from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the ATF test.

    Returns:
        Response with ATF test data.
    """
    api_url = f"{config.api_url}/table/sys_atf_test/{params.test_id}"

    # Make request
    try:
        session = get_session()
        response = session.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        if not result:
            return AtfTestResponse(
                success=False,
                message=f"ATF test with ID '{params.test_id}' not found",
            )

        return AtfTestResponse(
            success=True,
            message="ATF test retrieved successfully",
            test_id=result.get("sys_id", ""),
            test_name=result.get("name", ""),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get ATF test: {e}")
        return AtfTestResponse(
            success=False,
            message=f"Failed to get ATF test: {str(e)}",
        )


def list_atf_tests(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListAtfTestsParams,
) -> AtfTestListResponse:
    """
    List ATF tests from ServiceNow with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing ATF tests.

    Returns:
        Response with list of ATF tests.
    """
    api_url = f"{config.api_url}/table/sys_atf_test"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build query filters
    filters = []
    
    if params.active is not None:
        filters.append(f"active={str(params.active).lower()}")
    
    if params.application:
        filters.append(f"sys_scope={params.application}")
    
    if params.name_contains:
        filters.append(f"nameLIKE{params.name_contains}")
    
    if params.query:
        # Additional custom query
        filters.append(params.query)

    if filters:
        query_params["sysparm_query"] = "^".join(filters)

    # Make request
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

        return AtfTestListResponse(
            success=True,
            message=f"Retrieved {len(result)} ATF tests",
            tests=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list ATF tests: {e}")
        return AtfTestListResponse(
            success=False,
            message=f"Failed to list ATF tests: {str(e)}",
            tests=[],
            total_count=0,
        )


def delete_atf_test(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteAtfTestParams,
) -> AtfTestResponse:
    """
    Delete an ATF test from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the ATF test.

    Returns:
        Response with ATF test deletion result.
    """
    api_url = f"{config.api_url}/table/sys_atf_test/{params.test_id}"

    # Make request
    try:
        session = get_session()
        response = session.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return AtfTestResponse(
            success=True,
            message="ATF test deleted successfully",
            test_id=params.test_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete ATF test: {e}")
        return AtfTestResponse(
            success=False,
            message=f"Failed to delete ATF test: {str(e)}",
        )


def run_atf_test(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: RunAtfTestParams,
) -> AtfTestExecutionResponse:
    """
    Execute an ATF test in ServiceNow.

    This function attempts to trigger test execution using ServiceNow's ATF API.
    Note: Test execution capabilities may vary based on ServiceNow version and configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for running the ATF test.

    Returns:
        Response with test execution result.
    """
    # ServiceNow ATF test execution is typically done via sys_atf_test_suite_result
    # or through direct API calls to the ATF execution endpoint
    api_url = f"{config.api_url}/api/now/atf/test/{params.test_id}/execute"
    
    # Alternative approach: Create a test suite result entry
    alt_api_url = f"{config.api_url}/table/sys_atf_test_suite_result"

    # Build request data
    data = {
        "test": params.test_id,
        "state": "waiting",
    }
    
    if params.suite_id:
        data["test_suite"] = params.suite_id

    # Make request - first try the direct execution API
    try:
        session = get_session()
        
        # Try direct execution endpoint first
        try:
            response = session.post(
                api_url,
                json={"test_id": params.test_id},
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            if response.status_code == 200:
                result = response.json()
                return AtfTestExecutionResponse(
                    success=True,
                    message="ATF test execution triggered successfully",
                    execution_id=result.get("execution_id"),
                    status=result.get("status", "running"),
                    data=result,
                )
        except requests.RequestException:
            # Fall back to creating test suite result
            pass
        
        # Fallback: Create test suite result entry
        response = session.post(
            alt_api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return AtfTestExecutionResponse(
            success=True,
            message="ATF test execution initiated successfully",
            execution_id=result.get("sys_id", ""),
            status=result.get("state", "waiting"),
            data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to execute ATF test: {e}")
        return AtfTestExecutionResponse(
            success=False,
            message=f"Failed to execute ATF test: {str(e)}",
        )


def get_atf_test_results(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetAtfTestResultsParams,
) -> AtfTestResultsResponse:
    """
    Get ATF test execution results from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting ATF test results.

    Returns:
        Response with ATF test results.
    """
    # Query the sys_atf_test_result table for test results
    api_url = f"{config.api_url}/table/sys_atf_test_result"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_fields": "sys_id,test,status,start_time,end_time,output,failure_count,error_count,step_count",
        "sysparm_display_value": "true",
    }

    # Build query filters
    filters = []
    
    if params.test_id:
        filters.append(f"test={params.test_id}")
    
    if params.suite_result_id:
        filters.append(f"parent={params.suite_result_id}")

    if filters:
        query_params["sysparm_query"] = "^".join(filters)

    # Make request
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

        return AtfTestResultsResponse(
            success=True,
            message=f"Retrieved {len(result)} ATF test results",
            results=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get ATF test results: {e}")
        return AtfTestResultsResponse(
            success=False,
            message=f"Failed to get ATF test results: {str(e)}",
            results=[],
            total_count=0,
        )