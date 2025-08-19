# Catalog UI Policy Action Management in ServiceNow MCP

## Overview

The Catalog UI Policy Action tools provide comprehensive management of Catalog UI Policy Actions in ServiceNow. Catalog UI Policy Actions are stored in the `catalog_ui_policy_action` table and represent a set of actions that can be taken as a result of a Catalog UI Policy. These actions define what happens to specific form fields when UI policy conditions are met.

## Tools

### create_catalog_ui_policy_action

Create a new catalog UI policy action in the catalog_ui_policy_action table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item | string | No | Catalog item sys_id this action applies to |
| variable_set | string | No | Variable set sys_id this action applies to |
| catalog_variable | string | No | Variable name this action applies to |
| variable | string | Yes | Name of the variable |
| order | integer | No | Order of execution for this action (default: 100) |

#### Example

```python
# Example usage of create_catalog_ui_policy_action
result = create_catalog_ui_policy_action({
    "catalog_item": "b0c4030ac0a8000001c9dd3394009c96",
    "variable": "priority",
    "catalog_variable": "priority_field",
    "order": 100
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created catalog UI policy action data including sys_id |

### update_catalog_ui_policy_action

Update an existing catalog UI policy action in the catalog_ui_policy_action table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Catalog UI policy action sys_id |
| catalog_item | string | No | Updated catalog item sys_id |
| variable_set | string | No | Updated variable set sys_id |
| catalog_variable | string | No | Updated variable name |
| variable | string | No | Updated name of the variable |
| order | integer | No | Updated order of execution |

#### Example

```python
# Example usage of update_catalog_ui_policy_action
result = update_catalog_ui_policy_action({
    "action_id": "abc123def456ghi789",
    "variable": "updated_priority",
    "order": 150
})
```

### list_catalog_ui_policy_actions

List catalog UI policy actions from the catalog_ui_policy_action table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of actions to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| catalog_item | string | No | Filter by catalog item sys_id |
| variable_set | string | No | Filter by variable set sys_id |
| variable | string | No | Filter by variable name |
| query | string | No | Search query for action details |

#### Example

```python
# Example usage of list_catalog_ui_policy_actions
result = list_catalog_ui_policy_actions({
    "limit": 20,
    "catalog_item": "b0c4030ac0a8000001c9dd3394009c96",
    "query": "priority"
})
```

### get_catalog_ui_policy_action

Get a specific catalog UI policy action from the catalog_ui_policy_action table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Catalog UI policy action sys_id |

#### Example

```python
# Example usage of get_catalog_ui_policy_action
result = get_catalog_ui_policy_action({
    "action_id": "abc123def456ghi789"
})
```

### delete_catalog_ui_policy_action

Delete a catalog UI policy action from the catalog_ui_policy_action table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Catalog UI policy action sys_id |

#### Example

```python
# Example usage of delete_catalog_ui_policy_action
result = delete_catalog_ui_policy_action({
    "action_id": "abc123def456ghi789"
})
```

### clone_catalog_ui_policy_action

Clone an existing catalog UI policy action in the catalog_ui_policy_action table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action_id | string | Yes | Source catalog UI policy action sys_id |
| new_variable | string | Yes | Variable name for the cloned action |

#### Example

```python
# Example usage of clone_catalog_ui_policy_action
result = clone_catalog_ui_policy_action({
    "action_id": "abc123def456ghi789",
    "new_variable": "cloned_priority"
})
```

## Common Use Cases

### Creating Field Actions

Catalog UI Policy Actions are commonly used to define what happens to fields when UI policy conditions are met:

```python
# Create an action to hide a field
result = create_catalog_ui_policy_action({
    "catalog_item": "hardware_request_item_id",
    "variable": "urgency",
    "catalog_variable": "urgency_field",
    "order": 100
})
```

### Managing Field Visibility

Control field visibility based on policy conditions:

```python
# Create an action for a specific variable set
result = create_catalog_ui_policy_action({
    "variable_set": "hardware_variables_set_id",
    "variable": "warranty_period",
    "catalog_variable": "warranty_field",
    "order": 200
})
```

### Ordering Actions

Use the order parameter to control action execution sequence:

```python
# Create actions with specific execution order
actions = [
    {
        "variable": "priority",
        "catalog_variable": "priority_field",
        "order": 100
    },
    {
        "variable": "urgency", 
        "catalog_variable": "urgency_field",
        "order": 200
    }
]

for action_data in actions:
    result = create_catalog_ui_policy_action(action_data)
```

## Best Practices

1. **Use meaningful variable names** that clearly identify the field being acted upon
2. **Set appropriate execution order** using the order parameter for predictable behavior
3. **Group related actions** by using consistent ordering schemes (e.g., 100, 200, 300)
4. **Test thoroughly** to ensure actions work correctly with their associated UI policies
5. **Document relationships** between UI policies and their actions for maintenance
6. **Use clone functionality** to create similar actions for different variables efficiently

## Relationship with UI Policies

Catalog UI Policy Actions work in conjunction with Catalog UI Policies:

1. **UI Policies** define the conditions (when)
2. **UI Policy Actions** define the behavior (what happens)

Together they create dynamic form behavior without requiring client-side scripting.

## Error Handling

All tools return structured responses with success indicators and error messages:

```python
if result["success"]:
    print(f"Operation successful: {result['message']}")
    # Process result data
else:
    print(f"Operation failed: {result['message']}")
    # Handle error
```

## Integration with Other Tools

Catalog UI Policy Actions work closely with:
- **Catalog UI Policies** - Use `list_catalog_ui_policies` to find policies these actions belong to
- **Catalog Variables** - Use `list_catalog_variables` to understand available form fields
- **Catalog Items** - Actions are specific to catalog items and their forms

## Example Natural Language Commands for Claude

- "Create a catalog UI policy action to hide the priority field"
- "List all UI policy actions for the hardware request catalog item"
- "Update the action order for the urgency field action"
- "Clone the existing priority action for use with the severity field"
- "Show me all policy actions that affect the warranty_period variable"
- "Create actions to hide multiple fields when request type is 'standard'"
- "Delete the obsolete UI policy action for the discontinued field"