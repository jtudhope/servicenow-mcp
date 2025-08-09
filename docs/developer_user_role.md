# User Role Management in ServiceNow MCP

## Overview

The User Role Management tools provide comprehensive functionality for managing user-role associations in ServiceNow through the sys_user_has_role table. These tools allow you to assign roles to users, remove roles from users, list user role assignments, and perform bulk operations.

## Available Tools

### assign_user_role

Assigns a role to a user by creating a record in the sys_user_has_role table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | User ID or sys_id to assign role to |
| role_id | string | Yes | Role ID or sys_id to assign |
| granted_by | string | No | User who granted the role (sys_id) |

#### Example

```python
# Example usage of assign_user_role
result = assign_user_role({
    "user_id": "6816f79cc0a8016401c5a33be04be441",
    "role_id": "2831a114c611228501d4ea6c309d626d",
    "granted_by": "admin_user_sys_id"
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the created record |

###