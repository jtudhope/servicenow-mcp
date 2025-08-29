"""
Portal Taxonomy Associations tools for the ServiceNow MCP server.

This module provides tools for managing associations between Portals and Taxonomies 
stored in the m2m_sp_portal_taxonomy table. In ServiceNow, this association controls 
what taxonomies are available on a given portal.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreatePortalTaxonomyAssociationParams(BaseModel):
    """Parameters for creating a portal taxonomy association."""

    portal_id: str = Field(..., description="The sys_id of the portal")
    taxonomy_id: str = Field(..., description="The sys_id of the taxonomy")


class ListPortalTaxonomyAssociationsParams(BaseModel):
    """Parameters for listing portal taxonomy associations."""

    portal_id: Optional[str] = Field(None, description="Filter by portal sys_id")
    taxonomy_id: Optional[str] = Field(None, description="Filter by taxonomy sys_id")
    limit: Optional[int] = Field(None, description="Maximum number of associations to return")
    offset: Optional[int] = Field(None, description="Offset for pagination")


class DeletePortalTaxonomyAssociationParams(BaseModel):
    """Parameters for deleting a portal taxonomy association."""

    association_id: str = Field(..., description="The sys_id of the association to delete")


class GetPortalTaxonomyAssociationParams(BaseModel):
    """Parameters for getting a specific portal taxonomy association."""

    association_id: str = Field(..., description="The sys_id of the association to retrieve")


class UpdatePortalTaxonomyAssociationParams(BaseModel):
    """Parameters for updating a portal taxonomy association."""

    association_id: str = Field(..., description="The sys_id of the association to update")
    active: Optional[bool] = Field(None, description="Whether the association is active")
    order: Optional[int] = Field(None, description="Display order of the association")


class BulkCreatePortalTaxonomyAssociationsParams(BaseModel):
    """Parameters for bulk creating portal taxonomy associations."""

    portal_id: str = Field(..., description="The sys_id of the portal")
    taxonomy_ids: List[str] = Field(..., description="List of taxonomy sys_ids to associate with the portal")


def create_portal_taxonomy_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreatePortalTaxonomyAssociationParams,
) -> Dict[str, Any]:
    """
    Create a new portal taxonomy association in the m2m_sp_portal_taxonomy table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating portal taxonomy association.

    Returns:
        Response with created association details.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_taxonomy"

    data = {
        "sp_portal": params.portal_id,
        "taxonomy": params.taxonomy_id,
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

        return {
            "success": True,
            "message": f"Created portal taxonomy association: {result.get('sys_id', '')}",
            "data": result,
        }

    except requests.RequestException as e:
        logger.error(f"Failed to create portal taxonomy association: {e}")
        return {
            "success": False,
            "message": f"Failed to create portal taxonomy association: {str(e)}",
        }


def list_portal_taxonomy_associations(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListPortalTaxonomyAssociationsParams,
) -> Dict[str, Any]:
    """
    List portal taxonomy associations from the m2m_sp_portal_taxonomy table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing portal taxonomy associations.

    Returns:
        Response with list of associations.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_taxonomy"

    # Build query parameters
    query_params = {}
    
    # Build sysparm_query for filtering
    query_conditions = []
    if params.portal_id:
        query_conditions.append(f"sp_portal={params.portal_id}")
    if params.taxonomy_id:
        query_conditions.append(f"taxonomy={params.taxonomy_id}")
    
    if query_conditions:
        query_params["sysparm_query"] = "^".join(query_conditions)

    if params.limit is not None:
        query_params["sysparm_limit"] = str(params.limit)
    if params.offset is not None:
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

        return {
            "success": True,
            "message": f"Retrieved {len(result)} portal taxonomy associations",
            "associations": result,
            "total": len(result),
            "limit": params.limit,
            "offset": params.offset or 0,
        }

    except requests.RequestException as e:
        logger.error(f"Failed to list portal taxonomy associations: {e}")
        return {
            "success": False,
            "message": f"Failed to list portal taxonomy associations: {str(e)}",
        }


def delete_portal_taxonomy_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeletePortalTaxonomyAssociationParams,
) -> Dict[str, Any]:
    """
    Delete a portal taxonomy association from the m2m_sp_portal_taxonomy table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting portal taxonomy association.

    Returns:
        Response indicating success or failure.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_taxonomy/{params.association_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return {
            "success": True,
            "message": f"Deleted portal taxonomy association: {params.association_id}",
        }

    except requests.RequestException as e:
        logger.error(f"Failed to delete portal taxonomy association: {e}")
        return {
            "success": False,
            "message": f"Failed to delete portal taxonomy association: {str(e)}",
        }


def get_portal_taxonomy_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetPortalTaxonomyAssociationParams,
) -> Dict[str, Any]:
    """
    Get detailed information about a specific portal taxonomy association.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting portal taxonomy association.

    Returns:
        Response with association details.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_taxonomy/{params.association_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return {
            "success": True,
            "message": f"Retrieved portal taxonomy association: {params.association_id}",
            "data": result,
        }

    except requests.RequestException as e:
        logger.error(f"Failed to get portal taxonomy association: {e}")
        return {
            "success": False,
            "message": f"Failed to get portal taxonomy association: {str(e)}",
        }


def update_portal_taxonomy_association(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdatePortalTaxonomyAssociationParams,
) -> Dict[str, Any]:
    """
    Update an existing portal taxonomy association in the m2m_sp_portal_taxonomy table.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating portal taxonomy association.

    Returns:
        Response with updated association details.
    """
    api_url = f"{config.api_url}/table/m2m_sp_portal_taxonomy/{params.association_id}"

    # Build update data only for provided fields
    data = {}
    if params.active is not None:
        data["active"] = str(params.active).lower()
    if params.order is not None:
        data["order"] = str(params.order)

    if not data:
        return {
            "success": False,
            "message": "No fields provided for update",
        }

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return {
            "success": True,
            "message": f"Updated portal taxonomy association: {params.association_id}",
            "data": result,
        }

    except requests.RequestException as e:
        logger.error(f"Failed to update portal taxonomy association: {e}")
        return {
            "success": False,
            "message": f"Failed to update portal taxonomy association: {str(e)}",
        }


def bulk_create_portal_taxonomy_associations(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: BulkCreatePortalTaxonomyAssociationsParams,
) -> Dict[str, Any]:
    """
    Create multiple portal taxonomy associations in bulk.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for bulk creating portal taxonomy associations.

    Returns:
        Response with created associations details.
    """
    created_associations = []
    failed_associations = []

    for taxonomy_id in params.taxonomy_ids:
        try:
            create_params = CreatePortalTaxonomyAssociationParams(
                portal_id=params.portal_id,
                taxonomy_id=taxonomy_id
            )
            result = create_portal_taxonomy_association(config, auth_manager, create_params)
            
            if result["success"]:
                created_associations.append(result["data"])
            else:
                failed_associations.append({
                    "taxonomy_id": taxonomy_id,
                    "error": result["message"]
                })
                
        except Exception as e:
            failed_associations.append({
                "taxonomy_id": taxonomy_id,
                "error": str(e)
            })

    success_count = len(created_associations)
    failure_count = len(failed_associations)

    return {
        "success": failure_count == 0,
        "message": f"Created {success_count} associations, {failure_count} failed",
        "created_associations": created_associations,
        "failed_associations": failed_associations,
        "total_requested": len(params.taxonomy_ids),
        "total_created": success_count,
        "total_failed": failure_count,
    }