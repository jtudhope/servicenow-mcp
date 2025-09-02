"""
Email notification action tools for the ServiceNow MCP server.

This module provides tools for managing outbound email notification actions in ServiceNow.
Developers can create, update, list, and manage email notifications that are triggered
by system events to notify users or groups.
"""

import logging
from typing import Optional, List, Dict, Any

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateEmailNotificationParams(BaseModel):
    """Parameters for creating an email notification action."""

    name: str = Field(..., description="Name of the email notification")
    table: str = Field(..., description="Table that triggers the notification")
    event_name: str = Field(..., description="Event name that triggers the notification (e.g., 'incident.state')")
    active: Optional[bool] = Field(True, description="Whether the notification is active")
    subject: Optional[str] = Field(None, description="Email subject line")
    message: Optional[str] = Field(None, description="Email message body")
    message_html: Optional[str] = Field(None, description="HTML version of email message")
    from_address: Optional[str] = Field(None, description="From email address")
    reply_to: Optional[str] = Field(None, description="Reply-to email address")
    recipient_users: Optional[List[str]] = Field(None, description="List of user sys_ids to notify")
    recipient_fields: Optional[List[str]] = Field(None, description="List of field names containing users/groups to notify")
    condition: Optional[str] = Field(None, description="Condition query for when to send notification")
    advanced_condition: Optional[str] = Field(None, description="Advanced condition script")
    weight: Optional[int] = Field(0, description="Weight for notification processing order")
    category: Optional[str] = Field(None, description="Notification category sys_id")
    template: Optional[str] = Field(None, description="Email template sys_id")
    content_type: Optional[str] = Field("text/html", description="Content type (text/html, text/plain)")
    importance: Optional[str] = Field(None, description="Email importance level")
    include_attachments: Optional[bool] = Field(False, description="Whether to include attachments")
    force_delivery: Optional[bool] = Field(False, description="Force delivery even if user preferences say no")
    exclude_delegates: Optional[bool] = Field(False, description="Exclude delegate users from notification")
    mandatory: Optional[bool] = Field(False, description="Whether notification is mandatory")
    subscribable: Optional[bool] = Field(False, description="Whether users can subscribe to this notification")
    digestable: Optional[bool] = Field(False, description="Whether notification can be digested")
    digest_subject: Optional[str] = Field(None, description="Subject for digest emails")
    digest_text: Optional[str] = Field(None, description="Text for digest emails")
    digest_reply_to: Optional[str] = Field(None, description="Reply-to for digest emails")
    digest_template: Optional[str] = Field(None, description="Template for digest emails")
    sms_alternate: Optional[str] = Field(None, description="SMS alternate message")
    style: Optional[str] = Field(None, description="Email stationery style sys_id")
    action_insert: Optional[bool] = Field(False, description="Trigger on record insert")
    action_update: Optional[bool] = Field(False, description="Trigger on record update")
    action_delete: Optional[bool] = Field(False, description="Trigger on record delete")
    event_parm_1: Optional[bool] = Field(False, description="Event parameter 1 contains recipient")
    event_parm_2: Optional[bool] = Field(False, description="Event parameter 2 contains recipient")
    affected_field_on_event: Optional[str] = Field(None, description="Specific field that triggers the event")
    enable_dynamic_translation: Optional[bool] = Field(False, description="Enable dynamic translation for multi-language support")
    push_message_only: Optional[bool] = Field(False, description="Send only push notification, not email")
    message_list: Optional[List[str]] = Field(None, description="List of push message sys_ids")
    item: Optional[str] = Field("event.parm1", description="Item reference for the notification")
    item_table: Optional[str] = Field(None, description="Table for the item reference")


class UpdateEmailNotificationParams(BaseModel):
    """Parameters for updating an email notification action."""

    notification_id: str = Field(..., description="Email notification sys_id")
    name: Optional[str] = Field(None, description="Updated name of the email notification")
    table: Optional[str] = Field(None, description="Updated table that triggers the notification")
    event_name: Optional[str] = Field(None, description="Updated event name")
    active: Optional[bool] = Field(None, description="Updated active status")
    subject: Optional[str] = Field(None, description="Updated email subject line")
    message: Optional[str] = Field(None, description="Updated email message body")
    message_html: Optional[str] = Field(None, description="Updated HTML version of email message")
    from_address: Optional[str] = Field(None, description="Updated from email address")
    reply_to: Optional[str] = Field(None, description="Updated reply-to email address")
    recipient_users: Optional[List[str]] = Field(None, description="Updated list of user sys_ids to notify")
    recipient_fields: Optional[List[str]] = Field(None, description="Updated list of field names containing users/groups to notify")
    condition: Optional[str] = Field(None, description="Updated condition query")
    advanced_condition: Optional[str] = Field(None, description="Updated advanced condition script")
    weight: Optional[int] = Field(None, description="Updated weight for processing order")
    category: Optional[str] = Field(None, description="Updated notification category sys_id")
    template: Optional[str] = Field(None, description="Updated email template sys_id")
    content_type: Optional[str] = Field(None, description="Updated content type")
    importance: Optional[str] = Field(None, description="Updated email importance level")
    include_attachments: Optional[bool] = Field(None, description="Updated include attachments setting")
    force_delivery: Optional[bool] = Field(None, description="Updated force delivery setting")
    exclude_delegates: Optional[bool] = Field(None, description="Updated exclude delegates setting")
    mandatory: Optional[bool] = Field(None, description="Updated mandatory setting")
    subscribable: Optional[bool] = Field(None, description="Updated subscribable setting")
    digestable: Optional[bool] = Field(None, description="Updated digestable setting")
    digest_subject: Optional[str] = Field(None, description="Updated digest subject")
    digest_text: Optional[str] = Field(None, description="Updated digest text")
    digest_reply_to: Optional[str] = Field(None, description="Updated digest reply-to")
    digest_template: Optional[str] = Field(None, description="Updated digest template")
    sms_alternate: Optional[str] = Field(None, description="Updated SMS alternate message")
    style: Optional[str] = Field(None, description="Updated email stationery style")
    action_insert: Optional[bool] = Field(None, description="Updated trigger on insert setting")
    action_update: Optional[bool] = Field(None, description="Updated trigger on update setting")
    action_delete: Optional[bool] = Field(None, description="Updated trigger on delete setting")
    event_parm_1: Optional[bool] = Field(None, description="Updated event parameter 1 setting")
    event_parm_2: Optional[bool] = Field(None, description="Updated event parameter 2 setting")
    affected_field_on_event: Optional[str] = Field(None, description="Updated affected field setting")
    enable_dynamic_translation: Optional[bool] = Field(None, description="Updated dynamic translation setting")
    push_message_only: Optional[bool] = Field(None, description="Updated push message only setting")
    message_list: Optional[List[str]] = Field(None, description="Updated push message list")
    item: Optional[str] = Field(None, description="Updated item reference")
    item_table: Optional[str] = Field(None, description="Updated item table")


class ListEmailNotificationsParams(BaseModel):
    """Parameters for listing email notification actions."""

    active: Optional[bool] = Field(None, description="Filter by active status")
    table: Optional[str] = Field(None, description="Filter by table name")
    event_name: Optional[str] = Field(None, description="Filter by event name")
    category: Optional[str] = Field(None, description="Filter by category")
    limit: Optional[int] = Field(10, description="Maximum number of notifications to return")
    offset: Optional[int] = Field(0, description="Offset for pagination")
    query: Optional[str] = Field(None, description="Additional query filter")


class GetEmailNotificationParams(BaseModel):
    """Parameters for getting a specific email notification action."""

    notification_id: str = Field(..., description="Email notification sys_id")


class DeleteEmailNotificationParams(BaseModel):
    """Parameters for deleting an email notification action."""

    notification_id: str = Field(..., description="Email notification sys_id")


class EmailNotificationResponse(BaseModel):
    """Response from email notification operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    sys_id: Optional[str] = Field(None, description="System ID of the notification")
    notification: Optional[Dict[str, Any]] = Field(None, description="Notification details")


class EmailNotificationListResponse(BaseModel):
    """Response from listing email notifications."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    notifications: List[Dict[str, Any]] = Field(..., description="List of notifications")
    total_count: Optional[int] = Field(None, description="Total number of notifications")


def create_email_notification(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateEmailNotificationParams,
) -> EmailNotificationResponse:
    """
    Create a new email notification action in ServiceNow.

    This function creates an outbound email notification that triggers when specified
    events occur on a table. Developers can use this to set up system notifications
    for various business processes.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the email notification.

    Returns:
        Response with the created notification details.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action"

    # Build request data with all the notification fields
    data = {
        "name": params.name,
        "collection": params.table,
        "event_name": params.event_name,
        "active": params.active,
    }

    # Add optional fields
    optional_fields = {
        "subject": params.subject,
        "message": params.message,
        "message_html": params.message_html,
        "from": params.from_address,
        "reply_to": params.reply_to,
        "condition": params.condition,
        "advanced_condition": params.advanced_condition,
        "weight": params.weight,
        "category": params.category,
        "template": params.template,
        "content_type": params.content_type,
        "importance": params.importance,
        "include_attachments": params.include_attachments,
        "force_delivery": params.force_delivery,
        "exclude_delegates": params.exclude_delegates,
        "mandatory": params.mandatory,
        "subscribable": params.subscribable,
        "digestable": params.digestable,
        "digest_subject": params.digest_subject,
        "digest_text": params.digest_text,
        "digest_reply_to": params.digest_reply_to,
        "digest_template": params.digest_template,
        "sms_alternate": params.sms_alternate,
        "style": params.style,
        "action_insert": params.action_insert,
        "event_parm_1": params.event_parm_1,
        "event_parm_2": params.event_parm_2,
        "affected_field_on_event": params.affected_field_on_event,
        "enable_dynamic_translation": params.enable_dynamic_translation,
        "push_message_only": params.push_message_only,
        "item": params.item,
        "item_table": params.item_table,
    }

    # Add non-null optional fields
    for field, value in optional_fields.items():
        if value is not None:
            data[field] = value

    # Handle list fields
    if params.recipient_users:
        data["recipient_users"] = ",".join(params.recipient_users)
    
    if params.recipient_fields:
        data["recipient_fields"] = ",".join(params.recipient_fields)
    
    if params.message_list:
        data["message_list"] = ",".join(params.message_list)

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return EmailNotificationResponse(
            success=True,
            message="Email notification created successfully",
            sys_id=result.get("sys_id"),
            notification=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create email notification: {e}")
        return EmailNotificationResponse(
            success=False,
            message=f"Failed to create email notification: {str(e)}",
        )


def update_email_notification(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateEmailNotificationParams,
) -> EmailNotificationResponse:
    """
    Update an existing email notification action in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the email notification.

    Returns:
        Response with the updated notification details.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action/{params.notification_id}"

    # Build update data with only non-None fields
    data = {}
    
    # Map all possible update fields
    field_mapping = {
        "name": params.name,
        "collection": params.table,
        "event_name": params.event_name,
        "active": params.active,
        "subject": params.subject,
        "message": params.message,
        "message_html": params.message_html,
        "from": params.from_address,
        "reply_to": params.reply_to,
        "condition": params.condition,
        "advanced_condition": params.advanced_condition,
        "weight": params.weight,
        "category": params.category,
        "template": params.template,
        "content_type": params.content_type,
        "importance": params.importance,
        "include_attachments": params.include_attachments,
        "force_delivery": params.force_delivery,
        "exclude_delegates": params.exclude_delegates,
        "mandatory": params.mandatory,
        "subscribable": params.subscribable,
        "digestable": params.digestable,
        "digest_subject": params.digest_subject,
        "digest_text": params.digest_text,
        "digest_reply_to": params.digest_reply_to,
        "digest_template": params.digest_template,
        "sms_alternate": params.sms_alternate,
        "style": params.style,
        "action_insert": params.action_insert,
        "event_parm_1": params.event_parm_1,
        "event_parm_2": params.event_parm_2,
        "affected_field_on_event": params.affected_field_on_event,
        "enable_dynamic_translation": params.enable_dynamic_translation,
        "push_message_only": params.push_message_only,
        "item": params.item,
        "item_table": params.item_table,
    }

    # Add non-None fields to data
    for field, value in field_mapping.items():
        if value is not None:
            data[field] = value

    # Handle list fields
    if params.recipient_users is not None:
        data["recipient_users"] = ",".join(params.recipient_users)
    
    if params.recipient_fields is not None:
        data["recipient_fields"] = ",".join(params.recipient_fields)
    
    if params.message_list is not None:
        data["message_list"] = ",".join(params.message_list)

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return EmailNotificationResponse(
            success=True,
            message="Email notification updated successfully",
            sys_id=result.get("sys_id"),
            notification=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update email notification: {e}")
        return EmailNotificationResponse(
            success=False,
            message=f"Failed to update email notification: {str(e)}",
        )


def list_email_notifications(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListEmailNotificationsParams,
) -> EmailNotificationListResponse:
    """
    List email notification actions from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing email notifications.

    Returns:
        Response with the list of notifications.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action"
    
    # Build query parameters
    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
    }
    
    # Build filter conditions
    filters = []
    
    if params.active is not None:
        filters.append(f"active={params.active}")
    
    if params.table:
        filters.append(f"collection={params.table}")
    
    if params.event_name:
        filters.append(f"event_name={params.event_name}")
    
    if params.category:
        filters.append(f"category={params.category}")
    
    if params.query:
        filters.append(params.query)
    
    if filters:
        query_params["sysparm_query"] = "^".join(filters)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return EmailNotificationListResponse(
            success=True,
            message=f"Retrieved {len(result)} email notifications",
            notifications=result,
            total_count=len(result),
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list email notifications: {e}")
        return EmailNotificationListResponse(
            success=False,
            message=f"Failed to list email notifications: {str(e)}",
            notifications=[],
        )


def get_email_notification(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetEmailNotificationParams,
) -> EmailNotificationResponse:
    """
    Get a specific email notification action from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for getting the email notification.

    Returns:
        Response with the notification details.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action/{params.notification_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return EmailNotificationResponse(
            success=True,
            message="Email notification retrieved successfully",
            sys_id=result.get("sys_id"),
            notification=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get email notification: {e}")
        return EmailNotificationResponse(
            success=False,
            message=f"Failed to get email notification: {str(e)}",
        )


def delete_email_notification(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: DeleteEmailNotificationParams,
) -> EmailNotificationResponse:
    """
    Delete an email notification action from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for deleting the email notification.

    Returns:
        Response confirming the deletion.
    """
    api_url = f"{config.api_url}/table/sysevent_email_action/{params.notification_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return EmailNotificationResponse(
            success=True,
            message="Email notification deleted successfully",
            sys_id=params.notification_id,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete email notification: {e}")
        return EmailNotificationResponse(
            success=False,
            message=f"Failed to delete email notification: {str(e)}",
        )