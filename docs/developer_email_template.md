# Email Template Management in ServiceNow MCP

## Email Template Management

This tool provides comprehensive management of email templates in ServiceNow, allowing developers to create, update, list, get, delete, and clone email templates that are used by notifications, workflows, and other ServiceNow components.

Email templates in ServiceNow are stored in the `sysevent_email_template` table and contain HTML/text content that can be dynamically populated with data from ServiceNow records.

## Available Tools

### create_email_template

Creates a new email template in the ServiceNow instance.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the email template |
| subject | string | Yes | Subject line for emails using this template |
| message_html | string | Yes | HTML message content of the email template |
| message | string | No | Plain text message content (optional) |
| category | string | No | Category or classification of the template |
| active | boolean | No | Whether the email template is active (default: true) |
| description | string | No | Description of the email template |
| advanced | boolean | No | Whether this is an advanced template (default: false) |
| application | string | No | Application scope for the template |
| condition | string | No | Condition script for when to use this template |
| content_type | string | No | Content type of the template (default: "text/html") |
| sys_class_name | string | No | System class name for the template (default: "sysevent_email_template") |

**Example:**

```python
result = create_email_template({
    "name": "Incident Resolution Notification",
    "subject": "Your incident ${number} has been resolved",
    "message_html": "<h2>Incident Resolved</h2><p>Dear ${caller_id.name},</p><p>Your incident <strong>${number}</strong> has been resolved.</p><p>Resolution: ${resolution_notes}</p>",
    "message": "Dear ${caller_id.name}, Your incident ${number} has been resolved. Resolution: ${resolution_notes}",
    "category": "incident",
    "active": true,
    "description": "Template for incident resolution notifications",
    "content_type": "text/html"
})
```

### update_email_template

Updates an existing email template in ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | Email template ID or sys_id |
| name | string | No | Updated name of the email template |
| subject | string | No | Updated subject line |
| message_html | string | No | Updated HTML message content |
| message | string | No | Updated plain text message content |
| category | string | No | Updated category or classification |
| active | boolean | No | Updated active status |
| description | string | No | Updated description |
| advanced | boolean | No | Updated advanced template setting |
| application | string | No | Updated application scope |
| condition | string | No | Updated condition script |
| content_type | string | No | Updated content type |

**Example:**

```python
result = update_email_template({
    "template_id": "abc123",
    "subject": "UPDATED: Your incident ${number} has been resolved",
    "message_html": "<h2>Incident Resolved - Updated</h2><p>Dear ${caller_id.name},</p><p>Your incident <strong>${number}</strong> has been resolved.</p>",
    "active": true
})
```

### list_email_templates

Lists email templates from ServiceNow with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| category | string | No | Filter by category |
| active | boolean | No | Filter by active status |
| advanced | boolean | No | Filter by advanced template status |
| application | string | No | Filter by application scope |
| content_type | string | No | Filter by content type |
| name_contains | string | No | Filter by name containing text |
| limit | integer | No | Maximum number of templates to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query string |

**Example:**

```python
result = list_email_templates({
    "category": "incident",
    "active": true,
    "limit": 20
})
```

### get_email_template

Retrieves a specific email template by sys_id.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | Email template ID or sys_id |

**Example:**

```python
result = get_email_template({
    "template_id": "abc123"
})
```

### delete_email_template

Deletes an email template from ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | Email template ID or sys_id |

**Example:**

```python
result = delete_email_template({
    "template_id": "abc123"
})
```

### clone_email_template

Creates a copy of an existing email template with a new name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | Email template ID or sys_id to clone |
| new_name | string | Yes | Name for the cloned template |
| new_subject | string | No | Subject for the cloned template (optional) |

**Example:**

```python
result = clone_email_template({
    "template_id": "abc123",
    "new_name": "Incident Resolution Notification - Copy",
    "new_subject": "COPY: Your incident ${number} has been resolved"
})
```

## Response Format

All email template tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| template_id | string | Email template sys_id (for create/update/get/clone operations) |
| template_data | object | Email template data (for create/update/get/clone operations) |
| templates | array | List of email templates (for list operations) |
| total_count | integer | Total number of templates (for list operations) |

## Common Use Cases

### Creating Notification Templates

Create templates for various notification types:

```python
# Incident escalation template
create_email_template({
    "name": "Incident Escalation",
    "subject": "ESCALATION: Incident ${number} requires attention",
    "body_html": "<div style='color: red;'><h2>Escalation Notice</h2><p>Incident ${number} has been escalated to ${assignment_group}.</p><p>Priority: ${priority}</p><p>Description: ${short_description}</p></div>",
    "category": "incident",
    "table": "incident"
})
```

### Creating Welcome Email Templates

Create templates for user onboarding:

```python
create_email_template({
    "name": "New User Welcome",
    "subject": "Welcome to the ServiceNow Portal",
    "body_html": "<h1>Welcome ${first_name}!</h1><p>Your account has been created with username: <strong>${user_name}</strong></p><p>Please visit our portal to get started.</p>",
    "category": "user_management",
    "table": "sys_user"
})
```

### Creating Approval Templates

Create templates for approval workflows:

```python
create_email_template({
    "name": "Change Approval Request",
    "subject": "Approval Required: Change Request ${number}",
    "body_html": "<h2>Change Approval Request</h2><p>A change request requires your approval:</p><ul><li>Change: ${number}</li><li>Requested by: ${requested_by}</li><li>Description: ${short_description}</li><li>Risk: ${risk}</li></ul><p><a href='${approval_url}'>Click here to review and approve</a></p>",
    "category": "change_management",
    "table": "change_request"
})
```

## Template Variables

ServiceNow email templates support dynamic variables that get replaced with actual values:

### System Variables
- `${current.field_name}` - Field from the current record
- `${current.reference_field.display}` - Display value of reference field
- `${gs.getUserName()}` - Current user name
- `${gs.now()}` - Current date/time

### Common Record Variables
- `${number}` - Record number
- `${short_description}` - Short description
- `${caller_id.name}` - Caller's name
- `${assigned_to.name}` - Assignee's name
- `${assignment_group.name}` - Assignment group name

### URL Variables
- `${mail_script:link}` - Direct link to the record
- `${approval_url}` - Approval link (for approval workflows)

## Advanced Features

### HTML Formatting

Use HTML for rich email formatting:

```html
<div style="font-family: Arial, sans-serif;">
    <h2 style="color: #0066cc;">Service Request Update</h2>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <td><strong>Request:</strong></td>
            <td>${number}</td>
        </tr>
        <tr>
            <td><strong>Status:</strong></td>
            <td style="color: green;">${state}</td>
        </tr>
    </table>
</div>
```

### Conditional Content

Use mail scripts for conditional content:

```html
<p>Dear ${caller_id.name},</p>
${mail_script:
    if (current.priority == '1') {
        template.print('<p style="color: red;"><strong>HIGH PRIORITY</strong></p>');
    }
}
<p>Your request ${number} has been ${state}.</p>
```

## Best Practices

1. **Use Descriptive Names**: Choose clear, descriptive names that indicate the template's purpose.

2. **Include Plain Text**: Always provide a plain text version for accessibility and email client compatibility.

3. **Test Variables**: Test all dynamic variables to ensure they populate correctly.

4. **Mobile-Friendly**: Design HTML templates that work well on mobile devices.

5. **Brand Consistency**: Use consistent styling that matches your organization's branding.

6. **Version Control**: Use cloning to create template versions before making major changes.

## Error Handling

The tools include comprehensive error handling for common scenarios:

- Invalid template IDs
- Missing required parameters
- ServiceNow API connectivity issues
- Authentication failures
- Template cloning failures

## Security Considerations

- Email templates can contain sensitive information
- Use appropriate access controls for template management
- Avoid including passwords or tokens in templates
- Sanitize user input in dynamic content
- Test templates in non-production environments first