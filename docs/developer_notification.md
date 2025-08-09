# Email Notification Actions in ServiceNow MCP

## Overview

The Email Notification Actions tools allow developers to manage outbound email notifications in ServiceNow. These notifications are triggered by system events and can notify users or groups when specific conditions are met. This is essential for keeping stakeholders informed about important changes in the system.

## Available Tools

### create_email_notification

Creates a new email notification action that triggers when specified events occur on a table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the email notification |
| table | string | Yes | Table that triggers the notification (e.g., "incident", "change_request") |
| event_name | string | Yes | Event name that triggers the notification (e.g., "incident.state", "change_request.approved") |
| active | boolean | No | Whether the notification is active (default: true) |
| subject | string | No | Email subject line (supports variables like ${number}) |
| message | string | No | Plain text email message body |
| message_html | string | No | HTML version of email message |
| from_address | string | No | From email address |
| reply_to | string | No | Reply-to email address |
| recipient_users | array | No | List of user sys_ids to notify |
| recipient_fields | array | No | List of field names containing users/groups to notify |
| condition | string | No | Condition query for when to send notification |
| advanced_condition | string | No | Advanced condition script |
| weight | integer | No | Weight for notification processing order (default: 0) |
| category | string | No | Notification category sys_id |
| template | string | No | Email template sys_id |
| content_type | string | No | Content type ("text/html" or "text/plain", default: "text/html") |
| importance | string | No | Email importance level |
| include_attachments | boolean | No | Whether to include attachments (default: false) |
| force_delivery | boolean | No | Force delivery even if user preferences say no (default: false) |
| exclude_delegates | boolean | No | Exclude delegate users from notification (default: false) |
| mandatory | boolean | No | Whether notification is mandatory (default: false) |
| subscribable | boolean | No | Whether users can subscribe to this notification (default: false) |
| digestable | boolean | No | Whether notification can be digested (default: false) |
| digest_subject | string | No | Subject for digest emails |
| digest_text | string | No | Text for digest emails |
| digest_reply_to | string | No | Reply-to for digest emails |
| digest_template | string | No | Template for digest emails |
| sms_alternate | string | No | SMS alternate message |
| style | string | No | Email stationery style sys_id |
| action_insert | boolean | No | Trigger on record insert (default: false) |
| action_update | boolean | No | Trigger on record update (default: false) |
| action_delete | boolean | No | Trigger on record delete (default: false) |
| event_parm_1 | boolean | No | Event parameter 1 contains recipient (default: false) |
| event_parm_2 | boolean | No | Event parameter 2 contains recipient (default: false) |
| affected_field_on_event | string | No | Specific field that triggers the event |
| enable_dynamic_translation | boolean | No | Enable dynamic translation for multi-language support (default: false) |
| push_message_only | boolean | No | Send only push notification, not email (default: false) |
| message_list | array | No | List of push message sys_ids |
| item | string | No | Item reference for the notification (default: "event.parm1") |
| item_table | string | No | Table for the item reference |

#### Example

```python
result = create_email_notification({
    "name": "High Priority Incident Notification",
    "table": "incident",
    "event_name": "incident.state",
    "active": true,
    "subject": "High Priority Incident ${number} Requires Attention",
    "message": "A high priority incident ${number} has been created and requires immediate attention. Priority: ${priority}, State: ${state}",
    "recipient_fields": ["assigned_to", "manager"],
    "condition": "priority=1^state=1",
    "content_type": "text/html",
    "include_attachments": false,
    "force_delivery": true,
    "weight": 100
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the created notification |
| notification | object | Complete notification details |

---

### update_email_notification

Updates an existing email notification action with new settings.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| notification_id | string | Yes | Email notification sys_id to update |
| name | string | No | Updated name of the email notification |
| table | string | No | Updated table that triggers the notification |
| event_name | string | No | Updated event name |
| active | boolean | No | Updated active status |
| subject | string | No | Updated email subject line |
| message | string | No | Updated email message body |
| message_html | string | No | Updated HTML version of email message |
| ... | ... | No | All fields from create_email_notification are available for update |

#### Example

```python
result = update_email_notification({
    "notification_id": "a1b2c3d4e5f6g7h8i9j0",
    "name": "Updated High Priority Incident Notification",
    "active": false,
    "subject": "URGENT: Incident ${number} Status Update",
    "force_delivery": true,
    "weight": 200
})
```

---

### list_email_notifications

Lists email notification actions from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| active | boolean | No | Filter by active status |
| table | string | No | Filter by table name |
| event_name | string | No | Filter by event name |
| category | string | No | Filter by category |
| limit | integer | No | Maximum number of notifications to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query filter |

#### Example

```python
result = list_email_notifications({
    "active": true,
    "table": "incident",
    "limit": 25,
    "offset": 0
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| notifications | array | List of notification objects |
| total_count | integer | Total number of notifications found |

---

### get_email_notification

Retrieves detailed information about a specific email notification action.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| notification_id | string | Yes | Email notification sys_id |

#### Example

```python
result = get_email_notification({
    "notification_id": "a1b2c3d4e5f6g7h8i9j0"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the notification |
| notification | object | Complete notification details |

---

### delete_email_notification

Permanently deletes an email notification action from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| notification_id | string | Yes | Email notification sys_id to delete |

#### Example

```python
result = delete_email_notification({
    "notification_id": "a1b2c3d4e5f6g7h8i9j0"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the deleted notification |

---

## Common Use Cases

### 1. Incident Escalation Notifications

Create notifications that trigger when incidents reach critical states or remain unresolved for too long.

```python
# High priority incident notification  
create_email_notification({
    "name": "Critical Incident Alert",
    "table": "incident",
    "event_name": "incident.state",
    "subject": "CRITICAL: Incident ${number} - ${short_description}",
    "message": "A critical incident has been reported. Please review immediately.",
    "recipient_fields": ["assigned_to", "manager"],
    "condition": "priority=1^state=2",
    "force_delivery": true,
    "importance": "high"
})
```

### 2. Change Approval Notifications

Notify approvers when change requests require their approval.

```python
create_email_notification({
    "name": "Change Approval Required",
    "table": "change_request", 
    "event_name": "change_request.state",
    "subject": "Change ${number} Requires Your Approval",
    "message": "Change request ${number} is pending your approval. Risk: ${risk}, Category: ${category}",
    "recipient_fields": ["approval_group"],
    "condition": "state=2^approval=requested",
    "template": "change_approval_template"
})
```

### 3. Service Request Updates

Keep requesters informed about the progress of their service requests.

```python
create_email_notification({
    "name": "Service Request Status Update",
    "table": "sc_request",
    "event_name": "sc_request.state", 
    "subject": "Your Service Request ${number} Status: ${state}",
    "message": "Your service request ${number} status has been updated to ${state}.",
    "recipient_fields": ["requested_for", "opened_by"],
    "condition": "state!=1",
    "subscribable": true,
    "digestable": true
})
```

### 4. Assignment Notifications

Notify users when they are assigned new work items.

```python
create_email_notification({
    "name": "New Assignment Notification",
    "table": "incident",
    "event_name": "incident.assigned_to",
    "subject": "You have been assigned incident ${number}",
    "message": "Incident ${number} has been assigned to you. Priority: ${priority}",
    "recipient_fields": ["assigned_to"],
    "condition": "assigned_to!=NULL",
    "action_update": true
})
```

## Best Practices

### 1. Notification Design
- Use clear, descriptive names for notifications
- Write informative subject lines with relevant variables
- Include essential information in the message body
- Consider both HTML and plain text versions

### 2. Recipient Management
- Use recipient_fields for dynamic recipients based on record data
- Use recipient_users for static recipients
- Consider excluding delegates to avoid duplicate notifications
- Use groups for role-based notifications

### 3. Conditions and Triggers
- Be specific with conditions to avoid spam
- Use advanced conditions for complex logic
- Test conditions thoroughly before activating
- Consider using weight to control processing order

### 4. Performance Optimization
- Use appropriate weights to prioritize important notifications
- Enable digest mode for high-volume notifications
- Consider push notifications for mobile users
- Use templates for consistent formatting

### 5. Maintenance
- Regularly review and update notification lists
- Deactivate unused notifications
- Monitor notification delivery metrics
- Keep message content current and relevant

## Troubleshooting

### Common Issues

1. **Notifications not sending**
   - Check if notification is active
   - Verify event name matches table events
   - Confirm condition logic is correct
   - Check recipient field values

2. **Too many notifications**
   - Review condition logic
   - Consider using digest mode
   - Check for duplicate notifications
   - Verify recipient lists

3. **Wrong recipients**
   - Verify recipient_fields point to correct user/group fields
   - Check recipient_users sys_ids are valid
   - Review advanced condition logic
   - Test with specific records

4. **Formatting issues**
   - Check content_type setting
   - Verify HTML syntax in message_html
   - Test template references
   - Review variable substitution

## Integration with Other Tools

Email notifications work well with other ServiceNow MCP tools:

- **Workflows**: Trigger notifications at specific workflow stages
- **Business Rules**: Coordinate with business logic
- **Templates**: Use email templates for consistent formatting
- **Categories**: Organize notifications by business function
- **ACLs**: Control who can modify notifications

## Natural Language Commands for Claude

Users can interact with email notifications using natural language:

- "Create a notification for high priority incidents that emails the assigned user and manager"
- "List all active notifications for the change request table"
- "Update the incident escalation notification to include attachments"
- "Show me the details of the change approval notification"
- "Delete the old service request notification that's no longer needed"
- "Set up email alerts when critical incidents are created"
- "Find notifications that send to the IT support group"
- "Create a digest notification for daily incident summaries"