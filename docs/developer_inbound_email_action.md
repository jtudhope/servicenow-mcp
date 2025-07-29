# Inbound Email Actions in ServiceNow MCP

## Overview

The Inbound Email Action tools provide comprehensive functionality for managing inbound email actions in ServiceNow. These tools allow you to create, update, list, retrieve, and delete email actions that process incoming emails automatically.

## Available Tools

### create_inbound_email_action

Creates a new inbound email action in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the inbound email action |
| action_type | string | Yes | Type of action (script, table_api, etc.) |
| script | string | No | Script content for the email action |
| table | string | No | Target table for table API actions |
| active | boolean | No | Whether the email action is active (default: true) |
| order | integer | No | Execution order of the action |
| description | string | No | Description of the email action |
| condition | string | No | Condition script to determine when action runs |
| stop_processing | boolean | No | Stop processing further actions after this one (default: false) |

#### Example

```python
result = create_inbound_email_action({
    "name": "Process Support Emails",
    "action_type": "script",
    "script": "// Process incoming support emails\nvar incident = new GlideRecord('incident');\nincident.initialize();\nincident.short_description = email.subject;\nincident.description = email.body_text;\nincident.caller_id = email.from;\nincident.insert();",
    "active": true,
    "order": 100,
    "description": "Automatically create incidents from support emails"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| action_id | string | Name/ID of the created email action |
| sys_id | string | System ID of the created email action |
| data | object | Complete email action data from ServiceNow |

### update_inbound_email_action

Updates an existing inbound email action in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Inbound email action ID or sys_id to update |
| name | string | No | Updated name of the inbound email action |
| action_type | string | No | Updated type of action |
| script | string | No | Updated script content |
| table | string | No | Updated target table |
| active | boolean | No | Updated active status |
| order | integer | No | Updated execution order |
| description | string | No | Updated description |
| condition | string | No | Updated condition script |
| stop_processing | boolean | No | Updated stop processing flag |

#### Example

```python
result = update_inbound_email_action({
    "action_id": "email_action_sys_id",
    "name": "Enhanced Support Email Processing",
    "script": "// Enhanced script with better error handling\ntry {\n  var incident = new GlideRecord('incident');\n  incident.initialize();\n  incident.short_description = email.subject;\n  incident.description = email.body_text;\n  incident.caller_id = email.from;\n  incident.priority = 3;\n  incident.insert();\n} catch (e) {\n  gs.error('Failed to create incident: ' + e.message);\n}",
    "active": true
})
```

### list_inbound_email_actions

Lists inbound email actions from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | No | Search query for email actions (searches name and description) |
| active | boolean | No | Filter by active status |
| action_type | string | No | Filter by action type (script, table_api, etc.) |
| table | string | No | Filter by target table |
| limit | integer | No | Maximum number of email actions to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |

#### Example

```python
result = list_inbound_email_actions({
    "query": "support",
    "active": true,
    "action_type": "script",
    "limit": 20
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| actions | array | List of inbound email action objects |
| total_count | integer | Total number of actions returned |

### get_inbound_email_action

Retrieves a specific inbound email action by its ID.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Inbound email action ID or sys_id |

#### Example

```python
result = get_inbound_email_action({
    "action_id": "email_action_sys_id"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| action_id | string | Name/ID of the email action |
| sys_id | string | System ID of the email action |
| data | object | Complete email action data from ServiceNow |

### delete_inbound_email_action

Deletes an inbound email action from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Inbound email action ID or sys_id to delete |

#### Example

```python
result = delete_inbound_email_action({
    "action_id": "email_action_sys_id"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| action_id | string | ID of the deleted email action |

## Common Use Cases

1. **Incident Creation**: Automatically create incidents from support emails
2. **Request Processing**: Process service requests submitted via email
3. **Email Routing**: Route emails to appropriate teams based on content
4. **Data Extraction**: Extract specific information from structured emails
5. **Notification Processing**: Handle email notifications and updates

## Action Types

### Script Actions
- **Type**: `script`
- **Description**: Execute custom JavaScript code to process emails
- **Use Case**: Complex email processing with custom business logic

### Table API Actions
- **Type**: `table_api`
- **Description**: Directly insert records into specified tables
- **Use Case**: Simple record creation from email data

### Other Action Types
- **Type**: `transform_map`
- **Description**: Use transform maps to process structured email data
- **Use Case**: Processing CSV attachments or structured email content

## Script Context Variables

When writing scripts for email actions, the following variables are available:

| Variable | Type | Description |
|----------|------|-------------|
| email | object | The email object containing all email data |
| email.subject | string | Email subject line |
| email.body_text | string | Plain text email body |
| email.body_html | string | HTML email body |
| email.from | string | Sender email address |
| email.to | string | Recipient email address |
| email.cc | string | CC recipients |
| email.attachments | array | Email attachments |

## Error Handling

All tools return a standardized response format with a `success` field. When `success` is `false`, the `message` field contains details about the error.

Common error scenarios:
- Invalid action_id (action not found)
- Missing required fields
- Script syntax errors
- Network connectivity issues
- Authentication failures
- ServiceNow API rate limits

## Best Practices

1. **Script Testing**: Test email action scripts thoroughly in a development environment
2. **Error Handling**: Include proper try-catch blocks in script actions
3. **Performance**: Keep scripts efficient to avoid email processing delays
4. **Security**: Validate and sanitize email data before processing
5. **Logging**: Include appropriate logging for troubleshooting
6. **Order Management**: Use the `order` parameter to control execution sequence
7. **Conditional Processing**: Use condition scripts to filter when actions should run
8. **Stop Processing**: Use `stop_processing` flag appropriately to prevent unnecessary action execution

## Security Considerations

1. **Input Validation**: Always validate email data before processing
2. **XSS Prevention**: Sanitize HTML content from email bodies
3. **Access Control**: Ensure email actions have appropriate access permissions
4. **Audit Trail**: Enable auditing for email action changes
5. **Sensitive Data**: Handle sensitive information in emails appropriately