# src/servicenow_mcp/tools/portal_config.py

"""
Portal Configuration Management tools for the ServiceNow MCP server.

This module provides tools for managing portal configurations in ServiceNow,
including creating, updating, and retrieving portal settings.
"""

import logging
from typing import Optional, List

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreatePortalParams(BaseModel):
    """Parameters for creating a portal."""

    title: str = Field(..., description="Display title of the portal")
    url_suffix: str = Field(..., description="URL suffix for the portal (must be unique)")
    homepage: Optional[str] = Field(None, description="Homepage page sys_id")
    login_page: Optional[str] = Field(None, description="Login page sys_id")
    notfound_page: Optional[str] = Field(None, description="404 not found page sys_id")
    theme: Optional[str] = Field(None, description="Theme sys_id")
    dark_theme: Optional[str] = Field(None, description="Dark theme sys_id")
    sc_catalog: Optional[str] = Field(None, description="Service catalog sys_id")
    kb_knowledge_base: Optional[str] = Field(None, description="Knowledge base sys_id")
    logo: Optional[str] = Field(None, description="Logo image attachment")
    icon: Optional[str] = Field(None, description="Icon image attachment")
    sp_rectangle_menu: Optional[str] = Field(None, description="Main menu sys_id")
    default: Optional[bool] = Field(False, description="Whether this is the default portal")
    inactive: Optional[bool] = Field(False, description="Whether the portal is inactive")
    hide_portal_name: Optional[bool] = Field(False, description="Hide portal name in header")
    rtl_enabled: Optional[bool] = Field(False, description="Support right-to-left languages")
    enable_favorites: Optional[bool] = Field(False, description="Enable favorites functionality")
    enable_ais: Optional[bool] = Field(False, description="Enable AI Search")
    enable_certificate_based_authentication: Optional[bool] = Field(False, description="Enable certificate-based authentication")


class UpdatePortalParams(BaseModel):
    """Parameters for updating a portal."""

    portal_id: str = Field(..., description="Portal sys_id to update")
    title: Optional[str] = Field(None, description="Updated display title of the portal")
    url_suffix: Optional[str] = Field(None, description="Updated URL suffix for the portal")
    homepage: Optional[str] = Field(None, description="Updated homepage page sys_id")
    login_page: Optional[str] = Field(None, description="Updated login page sys_id")
    notfound_page: Optional[str] = Field(None, description="Updated 404 not found page sys_id")
    theme: Optional[str] = Field(None, description="Updated theme sys_id")
    dark_theme: Optional[str] = Field(None, description="Updated dark theme sys_id")
    sc_catalog: Optional[str] = Field(None, description="Updated service catalog sys_id")
    kb_knowledge_base: Optional[str] = Field(None, description="Updated knowledge base sys_id")
    logo: Optional[str] = Field(None, description="Updated logo image attachment")
    icon: Optional[str] = Field(None, description="Updated icon image attachment")
    sp_rectangle_menu: Optional[str] = Field(None, description="Updated main menu sys_id")
    default: Optional[bool] = Field(None, description="Updated default portal status")
    inactive: Optional[bool] = Field(None, description="Updated inactive status")
    hide_portal_name: Optional[bool] = Field(None, description="Updated hide portal name setting")
    rtl_enabled: Optional[bool] = Field(None, description="Updated RTL language support")
    enable_favorites: Optional[bool] = Field(None, description="Updated favorites functionality")
    enable_ais: Optional[bool] = Field(None, description="Updated AI Search setting")
    enable_certificate_based_authentication: Optional[bool] = Field(None, description="Updated certificate-based authentication")


class ListPortalsParams(BaseModel):
    """Parameters for listing portals."""

    active: Optional[bool] = Field(None, description="Filter by active status (opposite of inactive)")
    default: Optional[bool] = Field(None, description="Filter by default portal status")
    limit: int = Field(10, description="Maximum number of portals to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetPortalParams(BaseModel):
    """Parameters for getting a portal."""

    portal_id: str = Field(..., description="Portal sys_id or URL suffix to retrieve")


class DeletePortalParams(BaseModel):
    """Parameters for deleting a portal."""

    portal_id: str = Field(..., description="Portal sys_id to delete")


class PortalResponse(BaseModel):
    """Response from portal operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    portal_id: Optional[str] = Field(None, description="Portal sys_id")
    url_suffix: Optional[str] = Field(None, description="Portal URL suffix")


def create_portal(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalParams,
) -> PortalResponse:
    """
    Create a new portal configuration in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the portal.

    Returns:
        Response with created portal details.
    """
    api_url = f"{config.api_url}/table/sp_portal"

    # Build request data
    data = {
        "title": params.title,
        "url_suffix": params.url_suffix,
    }

    # Add optional fields
    optional_fields = [
        "homepage", "login_page", "notfound_page", "theme", "dark_theme",
        "sc_catalog", "kb_knowledge_base", "logo", "icon", "sp_rectangle_menu",
        "default", "inactive", "hide_portal_name", "rtl_enabled", 
        "enable_favorites", "enable_ais", "enable_certificate_based_authentication"
    ]
    
    for field in optional_fields:
        value = getattr(params, field, None)
        if value is not None:
            data[field] = str(value).lower() if isinstance(value, bool) else value

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalResponse(
            success=True,
            message="Portal created successfully",
            portal_id=result.get("sys_id"),
            url_suffix=result.get("url_suffix"),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create portal: {e}")
        return PortalResponse(
            success=False,
            message=f"Failed to create portal: {str(e)}",
        )


def update_portal(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdatePortalParams,
) -> PortalResponse:
    """
    Update an existing portal configuration in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the portal.

    Returns:
        Response with updated portal details.
    """
    api_url = f"{config.api_url}/table/sp_portal/{params.portal_id}"

    # Build request data with only provided fields
    data = {}
    
    optional_fields = [
        "title", "url_suffix", "homepage", "login_page", "notfound_page", "theme", 
        "dark_theme", "sc_catalog", "kb_knowledge_base", "logo", "icon", 
        "sp_rectangle_menu", "default", "inactive", "hide_portal_name", "rtl_enabled", 
        "enable_favorites", "enable_ais", "enable_certificate_based_authentication"
    ]
    
    for field in optional_fields:
        value = getattr(params, field, None)
        if value is not None:
            data[field] = str(value).lower() if isinstance(value, bool) else value

    if not data:
        return PortalResponse(
            success=False,
            message="No fields provided for update",
        )

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return PortalResponse(
            success=True,
            message="Portal updated successfully",
            portal_id=result.get("sys_id"),
            url_suffix=result.get("url_suffix"),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update portal: {e}")
        return PortalResponse(
            success=False,
            message=f"Failed to update portal: {str(e)}",
        )


def list_portals(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalsParams,
) -> dict:
    """
    List portal configurations from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing portals.

    Returns:
        Dictionary with portal list and metadata.
    """
    api_url = f"{config.api_url}/table/sp_portal"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_fields": "sys_id,title,url_suffix,default,inactive,theme,homepage,login_page",
    }

    # Build query conditions
    conditions = []
    
    if params.active is not None:
        # Active means NOT inactive
        if params.active:
            conditions.append("inactive=false^ORinactiveISEMPTY")
        else:
            conditions.append("inactive=true")
    
    if params.default is not None:
        conditions.append(f"default={str(params.default).lower()}")
    
    if params.query:
        conditions.append(params.query)
    
    if conditions:
        query_params["sysparm_query"] = "^".join(conditions)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        data = response.json()
        portals = data.get("result", [])

        return {
            "success": True,
            "message": f"Retrieved {len(portals)} portals",
            "portals": portals,
            "total_count": len(portals),
        }

    except requests.RequestException as e:
        logger.error(f"Failed to list portals: {e}")
        return {
            "success": False,
            "message": f"Failed to list portals: {str(e)}",
            "portals": [],
            "total_count": 0,
        }


def get_portal(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalParams,
) -> dict:
    """
    Get detailed information about a specific portal configuration.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the portal.

    Returns:
        Dictionary with portal details.
    """
    # Try to get portal by sys_id first, then by url_suffix
    api_url = f"{config.api_url}/table/sp_portal"
    
    # Check if portal_id looks like a sys_id (32 char hex)
    if len(params.portal_id) == 32:
        api_url = f"{api_url}/{params.portal_id}"
        query_params = {}
    else:
        # Search by url_suffix
        query_params = {
            "sysparm_query": f"url_suffix={params.portal_id}",
            "sysparm_limit": 1,
        }

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        data = response.json()
        
        if "result" in data and isinstance(data["result"], list):
            # Search result
            if not data["result"]:
                return {
                    "success": False,
                    "message": f"Portal not found: {params.portal_id}",
                }
            portal = data["result"][0]
        else:
            # Direct get result
            portal = data.get("result", {})

        return {
            "success": True,
            "message": "Portal retrieved successfully",
            "portal": portal,
        }

    except requests.RequestException as e:
        logger.error(f"Failed to get portal: {e}")
        return {
            "success": False,
            "message": f"Failed to get portal: {str(e)}",
        }


def delete_portal(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalParams,
) -> PortalResponse:
    """
    Delete a portal configuration from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the portal.

    Returns:
        Response with deletion status.
    """
    api_url = f"{config.api_url}/table/sp_portal/{params.portal_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return PortalResponse(
            success=True,
            message="Portal deleted successfully",
            portal_id=params.portal_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete portal: {e}")
        return PortalResponse(
            success=False,
            message=f"Failed to delete portal: {str(e)}",
        )