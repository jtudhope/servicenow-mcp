"""
Portal Catalog Association tools for the ServiceNow MCP server.

This module provides tools for managing associations between portals and catalogs
stored in the m2m_sp_portal_catalog table. In ServiceNow, this association controls
what service catalogs are available on a given portal.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


# Create Portal Catalog Association
class CreatePortalCatalogAssociationParams(BaseModel):
    """Parameters for creating a portal catalog association."""

    portal_id: str = Field(..., description="The sys_id of the portal")
    catalog_id: str = Field(..., description="The sys_id of the catalog")


class CreatePortalCatalogAssociationResponse(BaseModel):
    """Response from create portal catalog association operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    association_id: Optional[str] = Field(None, description="System ID of the created association")
    association_data: Optional[Dict[str, Any]] = Field(None, description="Details of the created association")


def create_portal_catalog_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalCatalogAssociationParams,
) -> CreatePortalCatalogAssociationResponse:
    """
    Create a new portal catalog association in the m2m_sp_portal_catalog table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the portal catalog association.

    Returns:
        Response with creation result and association details.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_catalog"

    # Build request data
    data = {
        "sp_portal": params.portal_id,
        "sc_catalog": params.catalog_id,
    }

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return CreatePortalCatalogAssociationResponse(
            success=True,
            message="Portal catalog association created successfully",
            association_id=result.get("sys_id"),
            association_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create portal catalog association: {e}")
        return CreatePortalCatalogAssociationResponse(
            success=False,
            message=f"Failed to create portal catalog association: {str(e)}",
        )


# List Portal Catalog Associations
class ListPortalCatalogAssociationsParams(BaseModel):
    """Parameters for listing portal catalog associations."""

    portal_id: Optional[str] = Field(None, description="Filter by portal sys_id")
    catalog_id: Optional[str] = Field(None, description="Filter by catalog sys_id")
    limit: Optional[int] = Field(None, description="Maximum number of associations to return")
    offset: Optional[int] = Field(None, description="Offset for pagination")


class ListPortalCatalogAssociationsResponse(BaseModel):
    """Response from list portal catalog associations operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    associations: List[Dict[str, Any]] = Field(default=[], description="List of portal catalog associations")
    total_count: Optional[int] = Field(None, description="Total number of associations")


def list_portal_catalog_associations(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalCatalogAssociationsParams,
) -> ListPortalCatalogAssociationsResponse:
    """
    List portal catalog associations from the m2m_sp_portal_catalog table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing portal catalog associations.

    Returns:
        Response with list of portal catalog associations.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_catalog"
    
    # Build query parameters
    query_parts = []
    if params.portal_id:
        query_parts.append(f"sp_portal={params.portal_id}")
    if params.catalog_id:
        query_parts.append(f"sc_catalog={params.catalog_id}")
    
    query_params = {}
    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)
    
    query_params["sysparm_display_value"] = "true"
    
    if params.limit:
        query_params["sysparm_limit"] = str(params.limit)
    if params.offset:
        query_params["sysparm_offset"] = str(params.offset)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return ListPortalCatalogAssociationsResponse(
            success=True,
            message=f"Retrieved {len(result)} portal catalog associations",
            associations=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list portal catalog associations: {e}")
        return ListPortalCatalogAssociationsResponse(
            success=False,
            message=f"Failed to list portal catalog associations: {str(e)}",
        )


# Delete Portal Catalog Association
class DeletePortalCatalogAssociationParams(BaseModel):
    """Parameters for deleting a portal catalog association."""

    association_id: str = Field(..., description="The sys_id of the association to delete")


class DeletePortalCatalogAssociationResponse(BaseModel):
    """Response from delete portal catalog association operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")


def delete_portal_catalog_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalCatalogAssociationParams,
) -> DeletePortalCatalogAssociationResponse:
    """
    Delete a portal catalog association from the m2m_sp_portal_catalog table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the portal catalog association.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_catalog/{params.association_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return DeletePortalCatalogAssociationResponse(
            success=True,
            message="Portal catalog association deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete portal catalog association: {e}")
        return DeletePortalCatalogAssociationResponse(
            success=False,
            message=f"Failed to delete portal catalog association: {str(e)}",
        )


# Get Portal Catalog Association Details
class GetPortalCatalogAssociationParams(BaseModel):
    """Parameters for getting a portal catalog association."""

    association_id: str = Field(..., description="The sys_id of the association to retrieve")


class GetPortalCatalogAssociationResponse(BaseModel):
    """Response from get portal catalog association operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    association_data: Optional[Dict[str, Any]] = Field(None, description="Association details")


def get_portal_catalog_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalCatalogAssociationParams,
) -> GetPortalCatalogAssociationResponse:
    """
    Get detailed information about a specific portal catalog association.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the portal catalog association.

    Returns:
        Response with association details.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_catalog/{params.association_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return GetPortalCatalogAssociationResponse(
            success=True,
            message="Portal catalog association retrieved successfully",
            association_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get portal catalog association: {e}")
        return GetPortalCatalogAssociationResponse(
            success=False,
            message=f"Failed to get portal catalog association: {str(e)}",
        )


# Bulk Create Portal Catalog Associations
class BulkCreatePortalCatalogAssociationsParams(BaseModel):
    """Parameters for bulk creating portal catalog associations."""

    portal_id: str = Field(..., description="The sys_id of the portal")
    catalog_ids: List[str] = Field(..., description="List of catalog sys_ids to associate with the portal")


class BulkCreatePortalCatalogAssociationsResponse(BaseModel):
    """Response from bulk create portal catalog associations operation."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    created_associations: List[Dict[str, Any]] = Field(default=[], description="List of created associations")
    failed_associations: List[Dict[str, Any]] = Field(default=[], description="List of failed associations")


def bulk_create_portal_catalog_associations(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkCreatePortalCatalogAssociationsParams,
) -> BulkCreatePortalCatalogAssociationsResponse:
    """
    Create multiple portal catalog associations in bulk.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for bulk creating portal catalog associations.

    Returns:
        Response with bulk creation results.
    """
    created_associations = []
    failed_associations = []

    for catalog_id in params.catalog_ids:
        create_params = CreatePortalCatalogAssociationParams(
            portal_id=params.portal_id,
            catalog_id=catalog_id
        )
        
        result = create_portal_catalog_association(config, auth_manager, create_params)
        
        if result.success:
            created_associations.append({
                "portal_id": params.portal_id,
                "catalog_id": catalog_id,
                "association_id": result.association_id
            })
        else:
            failed_associations.append({
                "portal_id": params.portal_id,
                "catalog_id": catalog_id,
                "error": result.message
            })

    success = len(failed_associations) == 0
    message = f"Created {len(created_associations)} associations"
    if failed_associations:
        message += f", failed to create {len(failed_associations)} associations"

    return BulkCreatePortalCatalogAssociationsResponse(
        success=success,
        message=message,
        created_associations=created_associations,
        failed_associations=failed_associations,
    )