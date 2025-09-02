"""
Email Template tools for the ServiceNow MCP server.

This module provides tools for managing email templates stored in the 
sysevent_email_template table.
"""

import logging
from typing import Optional, List, Dict, Any

import requests

from servicenow_mcp.auth.session_manager import get_session
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateEmailTemplateParams(BaseModel):
    """Parameters for creating an email template."""

    name: str = Field(..., description="Name of the email template")
    subject: str = Field(..., description="Subject line for emails using this template")
    message_html: str = Field(..., description="HTML message content of the email template")
    message: Optional[str] = Field(None, description="Plain text message content (optional)")
    category: Optional[str] = Field(None, description="Category or classification of the template")
    active: bool = Field(True, description="Whether the email template is active")
    description: Optional[str] = Field(None, description="Description of the email template")
    advanced: bool = Field(False, description="Whether this is an advanced template")
    application: Optional[str] = Field(None, description="Application scope for the template")
    condition: Optional[str] = Field(None, description="Condition script for when to use this template")
    content_type: str = Field("text/html", description="Content type of the template (text/html, text/plain)")
    sys_class_name: str = Field("sysevent_email_template", description="System class name for the template")


class UpdateEmailTemplateParams(BaseModel):
    """Parameters for updating an email template."""

    template_id: str = Field(..., description="Email template ID or sys_id")
    name: Optional[str] = Field(None, description="Updated name of the email template")
    subject: Optional[str] = Field(None, description="Updated subject line")
    message_html: Optional[str] = Field(None, description="Updated HTML message content")
    message: Optional[str] = Field(None, description="Updated plain text message content")
    category: Optional[str] = Field(None, description="Updated category or classification")
    active: Optional[bool] = Field(None, description="Updated active status")
    description: Optional[str] = Field(None, description="Updated description")
    advanced: Optional[bool] = Field(None, description="Updated advanced template setting")
    application: Optional[str] = Field(None, description="Updated application scope")
    condition: Optional[str] = Field(None, description="Updated condition script")
    content_type: Optional[str] = Field(None, description="Updated content type")


class ListEmailTemplatesParams(BaseModel):
    """Parameters for listing email templates."""

    category: Optional[str] = Field(None, description="Filter by category")
    active: Optional[bool] = Field(None, description="Filter by active status")
    advanced: Optional[bool] = Field(None, description="Filter by advanced template status")
    application: Optional[str] = Field(None, description="Filter by application scope")
    content_type: Optional[str] = Field(None, description="Filter by content type")
    name_contains: Optional[str] = Field(None, description="Filter by name containing text")
    limit: int = Field(10, description="Maximum number of templates to return")
    offset: int = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query string")


class GetEmailTemplateParams(BaseModel):
    """Parameters for getting a specific email template."""

    template_id: str = Field(..., description="Email template ID or sys_id")


class DeleteEmailTemplateParams(BaseModel):
    """Parameters for deleting an email template."""

    template_id: str = Field(..., description="Email template ID or sys_id")


class CloneEmailTemplateParams(BaseModel):
    """Parameters for cloning an email template."""

    template_id: str = Field(..., description="Email template ID or sys_id to clone")
    new_name: str = Field(..., description="Name for the cloned template")
    new_subject: Optional[str] = Field(None, description="Subject for the cloned template (optional)")


class EmailTemplateResponse(BaseModel):
    """Response from email template operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    template_id: Optional[str] = Field(None, description="Email template sys_id")
    template_data: Optional[Dict[str, Any]] = Field(None, description="Email template data")


class ListEmailTemplatesResponse(BaseModel):
    """Response from list email templates operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    templates: List[Dict[str, Any]] = Field(default_factory=list, description="List of email templates")
    total_count: int = Field(0, description="Total number of email templates")


def create_email_template(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateEmailTemplateParams,
) -> EmailTemplateResponse:
    """
    Create a new email template in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the email template.

    Returns:
        Response with email template creation result.
    """
    api_url = f"{config.api_url}/table/sysevent_email_template"

    # Build request data
    data = {
        "name": params.name,
        "subject": params.subject,
        "message_html": params.message_html,
        "active": params.active,
        "advanced": params.advanced,
        "content_type": params.content_type,
        "sys_class_name": params.sys_class_name,
    }

    if params.message:
        data["message"] = params.message
    if params.category:
        data["category"] = params.category
    if params.description:
        data["description"] = params.description
    if params.application:
        data["application"] = params.application
    if params.condition:
        data["condition"] = params.condition

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

        return EmailTemplateResponse(
            success=True,
            message="Email template created successfully",
            template_id=result.get("sys_id"),
            template_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create email template: {e}")
        return EmailTemplateResponse(
            success=False,
            message=f"Failed to create email template: {str(e)}",
        )


def update_email_template(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateEmailTemplateParams,
) -> EmailTemplateResponse:
    """
    Update an existing email template in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the email template.

    Returns:
        Response with email template update result.
    """
    api_url = f"{config.api_url}/table/sysevent_email_template/{params.template_id}"

    # Build request data with only provided fields
    data = {}
    
    if params.name is not None:
        data["name"] = params.name
    if params.subject is not None:
        data["subject"] = params.subject
    if params.message_html is not None:
        data["message_html"] = params.message_html
    if params.message is not None:
        data["message"] = params.message
    if params.category is not None:
        data["category"] = params.category
    if params.active is not None:
        data["active"] = params.active
    if params.description is not None:
        data["description"] = params.description
    if params.advanced is not None:
        data["advanced"] = params.advanced
    if params.application is not None:
        data["application"] = params.application
    if params.condition is not None:
        data["condition"] = params.condition
    if params.content_type is not None:
        data["content_type"] = params.content_type

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

        return EmailTemplateResponse(
            success=True,
            message="Email template updated successfully",
            template_id=result.get("sys_id"),
            template_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update email template: {e}")
        return EmailTemplateResponse(
            success=False,
            message=f"Failed to update email template: {str(e)}",
        )


def list_email_templates(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListEmailTemplatesParams,
) -> ListEmailTemplatesResponse:
    """
    List email templates from ServiceNow with optional filtering.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing email templates.

    Returns:
        Response with list of email templates.
    """
    api_url = f"{config.api_url}/table/sysevent_email_template"

    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }

    # Build encoded query
    query_parts = []
    
    if params.category:
        query_parts.append(f"category={params.category}")
    if params.active is not None:
        query_parts.append(f"active={params.active}")
    if params.advanced is not None:
        query_parts.append(f"advanced={params.advanced}")
    if params.application:
        query_parts.append(f"application={params.application}")
    if params.content_type:
        query_parts.append(f"content_type={params.content_type}")
    if params.name_contains:
        query_parts.append(f"nameLIKE{params.name_contains}")
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

        return ListEmailTemplatesResponse(
            success=True,
            message=f"Found {len(result)} email templates",
            templates=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list email templates: {e}")
        return ListEmailTemplatesResponse(
            success=False,
            message=f"Failed to list email templates: {str(e)}",
        )


def get_email_template(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetEmailTemplateParams,
) -> EmailTemplateResponse:
    """
    Get a specific email template from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the email template.

    Returns:
        Response with email template data.
    """
    api_url = f"{config.api_url}/table/sysevent_email_template/{params.template_id}"

    try:
        session = get_session()
        response = session.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return EmailTemplateResponse(
            success=True,
            message="Email template retrieved successfully",
            template_id=result.get("sys_id"),
            template_data=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get email template: {e}")
        return EmailTemplateResponse(
            success=False,
            message=f"Failed to get email template: {str(e)}",
        )


def delete_email_template(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteEmailTemplateParams,
) -> EmailTemplateResponse:
    """
    Delete an email template from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the email template.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/sysevent_email_template/{params.template_id}"

    try:
        session = get_session()
        response = session.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return EmailTemplateResponse(
            success=True,
            message="Email template deleted successfully",
            template_id=params.template_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete email template: {e}")
        return EmailTemplateResponse(
            success=False,
            message=f"Failed to delete email template: {str(e)}",
        )


def clone_email_template(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CloneEmailTemplateParams,
) -> EmailTemplateResponse:
    """
    Clone an existing email template in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for cloning the email template.

    Returns:
        Response with cloned email template result.
    """
    # First get the original template
    get_params = GetEmailTemplateParams(template_id=params.template_id)
    original_response = get_email_template(config, auth_manager, get_params)
    
    if not original_response.success:
        return EmailTemplateResponse(
            success=False,
            message=f"Failed to retrieve original template: {original_response.message}",
        )

    original_data = original_response.template_data
    if not original_data:
        return EmailTemplateResponse(
            success=False,
            message="Original template data not found",
        )

    # Create new template based on original
    create_params = CreateEmailTemplateParams(
        name=params.new_name,
        subject=params.new_subject or original_data.get("subject", ""),
        message_html=original_data.get("message_html", ""),
        message=original_data.get("message"),
        category=original_data.get("category"),
        active=original_data.get("active", True),
        description=f"Cloned from: {original_data.get('name', 'Unknown')}",
        advanced=original_data.get("advanced", False),
        application=original_data.get("application"),
        condition=original_data.get("condition"),
        content_type=original_data.get("content_type", "text/html"),
        sys_class_name=original_data.get("sys_class_name", "sysevent_email_template"),
    )

    return create_email_template(config, auth_manager, create_params)