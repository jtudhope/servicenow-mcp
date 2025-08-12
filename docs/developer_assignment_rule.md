# Assignment Rule Management in ServiceNow MCP

## Assignment Rule Management

This tool provides comprehensive management of assignment rules in ServiceNow, allowing developers to create, update, list, get, and delete assignment rules that determine how records are automatically assigned within the platform.

Assignment rules in ServiceNow are stored in the `sysrule_assignment` table and contain JavaScript logic that determines how records should be assigned to users or groups based on specified conditions.

## Available Tools

### create_assignment_rule

Creates a new assignment rule in the ServiceNow instance.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the assignment rule |
| table | string | Yes | Table the rule applies to |
| script | string | Yes | Assignment script that determines assignment logic |
| condition | string | No | Condition query for when to apply the rule |
| order | integer | No | Execution order of the rule (lower numbers run first) |
| active | boolean | No | Whether the assignment rule is active (default: true) |
| description | string | No | Description of the assignment rule |
| inherited | boolean | No | Whether rule applies to extended tables (default: false) |
| when_to_apply | string | No | When to apply rule: "sync", "async", or "both" (default: "async") |

**Example:**

```python
result = create_assignment_rule({
    "name": "Incident P1 Assignment",
    "table": "incident",
    "script": "if (current.priority == '1') { current.assigned_to = 'admin'; }",
    "condition": "priority=1",
    "order": 100,
    "active": true,
    "description": "Auto-assign P1 incidents to admin",
    "when_to_apply": "sync"
})
```

### update_assignment_rule

Updates an existing assignment rule in ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| rule_id | string | Yes | Assignment rule ID or sys_id |
| name | string | No | Updated name of the assignment rule |
| table | string | No | Updated table the rule applies to |
| script | string | No | Updated assignment script |
| condition | string | No | Updated condition query |
| order | integer | No | Updated execution order |
| active | boolean | No | Updated active status |
| description | string | No | Updated description |
| inherited | boolean | No | Updated inherited setting |
| when_to_apply | string | No | Updated when to apply setting |

**Example:**

```python
result = update_assignment_rule({
    "rule_id": "abc123",
    "name": "Updated Incident P1 Assignment",
    "active": false,
    "description": "Temporarily disabled P1 assignment rule"
})
```

### list_assignment_rules

Lists assignment rules from ServiceNow with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | No | Filter by table |
| active | boolean | No | Filter by active status |
| inherited | boolean | No | Filter by inherited status |
| when_to_apply | string | No | Filter by when to apply setting |
| limit | integer | No | Maximum number of rules to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query string |

**Example:**

```python
result = list_assignment_rules({
    "table": "incident",
    "active": true,
    "limit": 20
})
```

### get_assignment_rule

Retrieves a specific assignment rule by sys_id.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| rule_id | string | Yes | Assignment rule ID or sys_id |

**Example:**

```python
result = get_assignment_rule({
    "rule_id": "abc123"
})
```

### delete_assignment_rule

Deletes an assignment rule from ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| rule_id | string | Yes | Assignment rule ID or sys_id |

**Example:**

```python
result = delete_assignment_rule({
    "rule_id": "abc123"
})
```

## Response Format

All assignment rule tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| rule_id | string | Assignment rule sys_id (for create/update/get operations) |
| rule_data | object | Assignment rule data (for create/update/get operations) |
| rules | array | List of assignment rules (for list operations) |
| total_count | integer | Total number of rules (for list operations) |

## Common Use Cases

### Creating Simple Assignment Rules

Create rules that assign records based on field values:

```python
# Assign VIP users to senior support team
create_assignment_rule({
    "name": "VIP User Assignment",
    "table": "incident",
    "script": "if (current.caller_id.vip == true) { current.assignment_group = 'senior_support_group'; }",
    "condition": "caller_id.vip=true",
    "active": true
})
```

### Round Robin Assignment

Create rules that distribute workload evenly:

```python
create_assignment_rule({
    "name": "Round Robin Assignment",
    "table": "incident",
    "script": "// Round robin logic here\nvar users = ['user1', 'user2', 'user3'];\nvar count = new GlideAggregate('incident');\ncount.query();\nvar index = count.getRowCount() % users.length;\ncurrent.assigned_to = users[index];",
    "order": 200,
    "when_to_apply": "async"
})
```

### Time-based Assignment

Create rules that assign based on time of day or business hours:

```python
create_assignment_rule({
    "name": "After Hours Assignment",
    "table": "incident",
    "script": "var now = new GlideDateTime();\nvar hour = now.getHour();\nif (hour < 8 || hour > 17) {\n  current.assignment_group = 'after_hours_support';\n}",
    "condition": "active=true",
    "when_to_apply": "sync"
})
```

## Best Practices

1. **Order Matters**: Use the `order` field to control execution sequence. Lower numbers execute first.

2. **Condition Optimization**: Use specific conditions to avoid unnecessary script execution.

3. **Sync vs Async**: Use `sync` for immediate assignment, `async` for background processing.

4. **Testing**: Always test assignment rules in a development environment first.

5. **Documentation**: Use descriptive names and descriptions for maintainability.

6. **Error Handling**: Include error handling in assignment scripts to prevent failures.

## Error Handling

The tools include comprehensive error handling for common scenarios:

- Invalid rule IDs
- Missing required parameters
- ServiceNow API connectivity issues
- Authentication failures

## Security Considerations

- Assignment rules execute with system privileges
- Ensure proper input validation in rule scripts
- Avoid hardcoding sensitive information
- Test rules thoroughly before activating in production