# Inbound Email Actions in ServiceNow MCP

## Overview

Inbound email actions determine how ServiceNow processes incoming emails. These tools allow you to create, update, list, get, and delete inbound email actions in the `sysevent_in_email_action` table.

## Tools Available

### create_inbound_email_action

Creates a new inbound email action in ServiceNow that determines how incoming emails should be processed.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the inbound email action |
| action_type | string | Yes | Type of action (script, table_api, etc.) |
| active | boolean | No | Whether the email action is active (default: true) |
| condition | string | No | Condition script to determine when action runs |
| script | string | No | Script content for the email action |
| table | string | No | Target table for table API actions |
| order | integer | No | Execution order of the action |
| stop_processing | boolean | No | Stop processing further actions after this one (default: false) |
| description | string | No | Description of the email action |

#### Example

```python
# Create a new inbound email action
result = create_inbound_email_action({
    "name": "Process Support Emails",
    "action_type": "script",
    "active": True,
    "script": "// Process incoming support emails\ngs.info('Processing email: ' + email.subject);",
    "description": "Processes incoming support emails and creates incidents",
    "order": 100
})
```

### update_inbound_email_action

Updates an existing inbound email action.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Inbound email action ID or sys_id |
| name | string | No | Updated name of the inbound email action |
| action_type | string | No | Updated type of action |
| active | boolean | No | Updated active status |
| condition | string | No | Updated condition script |
| script | string | No | Updated script content |
| table | string | No | Updated target table |
| order | integer | No | Updated execution order |
| stop_processing | boolean | No | Updated stop processing flag |
| description | string | No | Updated description |

#### Example

```python
# Update an inbound email action
result = update_inbound_email_action({
    "action_id": "12345678901234567890123456789012",
    "active": False,
    "description": "Temporarily disabled for maintenance"
})
```

### list_inbound_email_actions

Lists inbound email actions from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| active | boolean | No | Filter by active status |
| action_type | string | No | Filter by action type |
| table | string | No | Filter by target table |
| limit | integer | No | Maximum number of email actions to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Search query for email actions |

#### Example

```python
# List active script-type inbound email actions
result = list_inbound_email_actions({
    "active