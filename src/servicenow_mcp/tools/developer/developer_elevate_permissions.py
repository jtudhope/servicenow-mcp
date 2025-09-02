"""
Security Elevation tools for the ServiceNow MCP server.

This module provides tools for elevating login sessions with specific roles.
"""

import logging
from typing import Optional

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

from servicenow_mcp.auth.session_manager import get_session

logger = logging.getLogger(__name__)

class SecurityElevationParams(BaseModel):
    """Parameters for security_elevation."""

    roles: str = Field(..., description="Comma-separated list of roles to elevate to (e.g., 'security_admin', 'admin')")


class SecurityElevationResponse(BaseModel):
    """Response from security_elevation operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    elevated_roles: Optional[str] = Field(None, description="The roles that were elevated to")


def security_elevation(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: SecurityElevationParams,
) -> SecurityElevationResponse:
    """
    Elevate the current login session to specified roles.

    This function allows users to temporarily elevate their privileges by impersonating
    specific roles such as security_admin. This is useful for performing administrative
    tasks that require elevated permissions.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for security_elevation.

    Returns:
        Response with elevation status and elevated roles.
    """
    api_url = f"{config.instance_url}/api/now/ui/impersonate/role"

    # Build request data
    data = {
        "roles": params.roles,
    }
    
    # Make request
    try:
        
        session = get_session(); 

        response = session.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        logger.info("Received Response from ServiceNow")
        logger.info(response.cookies);
        logger.info(response.headers);
        logger.info("Received Response from ServiceNow COmplete")

        # The API typically returns success status
        result = response.json() if response.content else {}

        return SecurityElevationResponse(
            success=True,
            message=f"Security elevation completed successfully for roles: {params.roles}",
            elevated_roles=params.roles,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to elevate security privileges: {e}")
        return SecurityElevationResponse(
            success=False,
            message=f"Failed to elevate security privileges: {str(e)}",
            elevated_roles=None,
        )