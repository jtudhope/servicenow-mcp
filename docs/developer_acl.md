# ACL Management in ServiceNow MCP

## Overview

The ACL (Access Control List) tools provide comprehensive functionality for creating, updating, listing, and managing ACLs in ServiceNow. ACLs control access to data at the table and field level based on conditions, roles, and scripts.

## Available Tools

### create_acl

Creates a new ACL in ServiceNow with the specified parameters.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the ACL |
| table | string | Yes | Table the ACL applies to |
| operation | string | No | Operation type (read, write, create, delete). Default: "read" |
| type | string | No | ACL type (record, field). Default: "record" |
| field | string | No | Field name for field-level ACLs |
| script | string | No | Script content for the ACL |
| condition | string | No | Condition for the ACL |
| roles | string | No | Comma-separated list of roles |
| active | boolean | No | Whether the ACL is active. Default: true |
| admin_overrides | boolean | No | Whether admin role overrides this ACL. Default: true |
| advanced | boolean | No | Whether this is an advanced ACL. Default: false |
| description | string | No | Description of the ACL |

#### Example

```python
result = create_acl({
    "name": "Incident Read Access",
    "table": "incident",
    "operation": "read",
    "type": "record",
    "script": "current.state != 7",
    "roles": "itil,incident_manager",
    "active": true,
    "description": "Allow ITIL users to read non-closed incidents"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| acl_id | string | The sys_id of the created ACL |
| acl_data | object | Complete ACL data from ServiceNow |

### update_acl

Updates an existing ACL in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| acl_id | string | Yes | ACL ID or sys_id |
| name | string | No | Name of the ACL |
| table | string | No | Table the ACL applies to |
| operation | string | No | Operation type (read, write, create, delete) |
| type | string | No | ACL type (record, field) |
| field | string | No | Field name for field-level ACLs |
| script | string | No | Script content for the ACL |
| condition | string | No | Condition for the ACL |
| roles | string | No | Comma-separated list of roles |
| active | boolean | No | Whether the ACL is active |
| admin_overrides | boolean | No | Whether admin role overrides this ACL |
| advanced | boolean | No | Whether this is an advanced ACL |
| description | string | No | Description of the ACL |

#### Example

```python
result = update_acl({
    "acl_id": "abc123def456",
    "script": "current.state != 7 && current.assigned_to == gs.getUserID()",
    "active": false,
    "description": "Updated ACL to restrict to assigned users only"
})
```

### list_acls

Lists ACLs from ServiceNow with optional filtering and pagination.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | No | Filter by table |
| operation | string | No | Filter by operation |
| type | string | No | Filter by ACL type |
| active | boolean | No | Filter by active status |
| limit | integer | No | Maximum number of ACLs to return. Default: 10 |
| offset | integer | No | Offset for pagination. Default: 0 |
| query | string | No | Additional query string |

#### Example

```python
result = list_acls({
    "table": "incident",
    "active": true,
    "limit": 20,
    "offset": 0
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| acls | array | List of ACL objects |
| total_count | integer | Total number of ACLs returned |

### get_acl

Retrieves a specific ACL by its sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| acl_id | string | Yes | ACL ID or sys_id |

#### Example

```python
result = get_acl({
    "acl_id": "abc123def456"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| acl_id | string | The sys_id of the ACL |
| acl_data | object | Complete ACL data from ServiceNow |

### delete_acl

Deletes an ACL from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| acl_id | string | Yes | ACL ID or sys_id |

#### Example

```python
result = delete_acl({
    "acl_id": "abc123def456"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| acl_id | string | The sys_id of the deleted ACL |

## Common ACL Patterns

### Table-Level Read ACL
```python
create_acl({
    "name": "Incident Read - ITIL Users",
    "table": "incident",
    "operation": "read",
    "type": "record",
    "roles": "itil",
    "script": "current.state != 7"
})
```

### Field-Level Write ACL
```python
create_acl({
    "name": "Incident Priority Write - Manager Only",
    "table": "incident",
    "operation": "write",
    "type": "field",
    "field": "priority",
    "roles": "incident_manager",
    "script": "gs.hasRole('incident_manager')"
})
```

### Conditional ACL with Script
```python
create_acl({
    "name": "Problem Write - Own Records",
    "table": "problem",
    "operation": "write",
    "type": "record",
    "script": "current.assigned_to == gs.getUserID() || gs.hasRole('problem_manager')"
})
```

## Best Practices

1. **Use descriptive names**: ACL names should clearly indicate their purpose
2. **Test scripts thoroughly**: Always test ACL scripts in a development environment
3. **Consider performance**: Complex scripts can impact system performance
4. **Use roles appropriately**: Leverage existing roles rather than creating user-specific ACLs
5. **Document conditions**: Use the description field to explain complex logic
6. **Regular review**: Periodically review ACLs to ensure they're still needed

## Common Operations

### Finding ACLs for a table
```python
list_acls({
    "table": "incident",
    "active": true
})
```

### Disabling an ACL temporarily
```python
update_acl({
    "acl_id": "abc123def456",
    "active": false
})
```

### Creating role-based access
```python
create_acl({
    "name": "Change Request Read - CAB Members",
    "table": "change_request", 
    "operation": "read",
    "roles": "change_advisory_board",
    "active": true
})
```