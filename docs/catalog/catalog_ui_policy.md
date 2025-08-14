# Catalog UI Policy Management in ServiceNow MCP

## Overview

The Catalog UI Policy tools provide comprehensive management of Catalog UI Policies in ServiceNow. Catalog UI Policies are stored in the `catalog_ui_policy` table and are a set of rules that dynamically change how fields behave on a Service Catalog item or record producer form — without writing client-side JavaScript.

## Tools

### create_catalog_ui_policy

Create a new catalog UI policy in the catalog_ui_policy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the catalog UI policy |
| catalog_item | string | No | Catalog item sys_id this policy applies to |
| variable_set | string | No | Variable set sys_id this policy applies to |
| applies_to | string | No | What the policy applies to (item, variable_set) |
| description | string | No | Description of the UI policy |
| active | boolean | No | Whether the UI policy is active (default: true) |
| applies_catalog | boolean | No | Applies on a Catalog Item view (default: true) |
| applies_req_item | boolean | No | Applies on Requested Items (default: false) |
| applies_sc_task | boolean | No | Applies on Catalog Tasks (default: false) |
| applies_target_record | boolean | No | Applies on the Target Record (default: false) |
| catalog_conditions | string | No | Catalog conditions in JSON format |

#### Example

```python
# Example usage of create_catalog_ui_policy
result = create_catalog_ui_policy({
    "name": "Hide Priority for Standard Requests",
    "catalog_item": "b0c4030ac0a8000001c9dd3394009c96",
    "applies_to": "item",
    "description": "Hides priority field for standard catalog requests",
    "active": true,
    "applies_catalog": true,
    "applies_req_item": false
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created catalog UI policy data including sys_id |

### update_catalog_ui_policy

Update an existing catalog UI policy in the catalog_ui_policy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| policy_id | string | Yes | Catalog UI policy sys_id |
| name | string | No | Updated name of the catalog UI policy |
| catalog_item | string | No | Updated catalog item sys_id |
| variable_set | string | No | Updated variable set sys_id |
| applies_to | string | No | Updated applies to value |
| description | string | No | Updated description |
| active | boolean | No | Updated active status |
| applies_catalog | boolean | No | Updated applies on catalog item view |
| applies_req_item | boolean | No | Updated applies on requested items |
| applies_sc_task | boolean | No | Updated applies on catalog tasks |
| applies_target_record | boolean | No | Updated applies on target record |
| catalog_conditions | string | No | Updated catalog conditions |

#### Example

```python
# Example usage of update_catalog_ui_policy
result = update_catalog_ui_policy({
    "policy_id": "abc123def456ghi789",
    "name": "Updated Policy Name",
    "active": false
})
```

### list_catalog_ui_policies

List catalog UI policies from the catalog_ui_policy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of policies to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| active | boolean | No | Filter by active status |
| catalog_item | string | No | Filter by catalog item sys_id |
| applies_to | string | No | Filter by applies to value |
| query | string | No | Search query for policy name or description |

#### Example

```python
# Example usage of list_catalog_ui_policies
result = list_catalog_ui_policies({
    "limit": 20,
    "active": true,
    "query": "priority"
})
```

### get_catalog_ui_policy

Get a specific catalog UI policy from the catalog_ui_policy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| policy_id | string | Yes | Catalog UI policy sys_id |

#### Example

```python
# Example usage of get_catalog_ui_policy
result = get_catalog_ui_policy({
    "policy_id": "abc123def456ghi789"
})
```

### delete_catalog_ui_policy

Delete a catalog UI policy from the catalog_ui_policy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| policy_id | string | Yes | Catalog UI policy sys_id |

#### Example

```python
# Example usage of delete_catalog_ui_policy
result = delete_catalog_ui_policy({
    "policy_id": "abc123def456ghi789"
})
```

### clone_catalog_ui_policy

Clone an existing catalog UI policy in the catalog_ui_policy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| policy_id | string | Yes | Source catalog UI policy sys_id |
| new_name | string | Yes | Name for the cloned policy |

#### Example

```python
# Example usage of clone_catalog_ui_policy
result = clone_catalog_ui_policy({
    "policy_id": "abc123def456ghi789",
    "new_name": "Cloned Priority Policy"
})
```

## Common Use Cases

### Creating Field Visibility Rules

Catalog UI Policies are commonly used to control field visibility based on user selections:

```python
# Create a policy to show/hide fields based on request type
result = create_catalog_ui_policy({
    "name": "Request Type Conditional Fields",
    "catalog_item": "hardware_request_item_id",
    "description": "Show additional fields for hardware requests",
    "applies_catalog": true,
    "catalog_conditions": "{\"condition\":\"request_type=hardware\"}"
})
```

### Managing Form Behavior

Control how forms behave in different contexts:

```python
# Create a policy that applies only to requested items view
result = create_catalog_ui_policy({
    "name": "Requested Items Read-only Policy",
    "catalog_item": "software_request_item_id",
    "description": "Make certain fields read-only in requested items",
    "applies_catalog": false,
    "applies_req_item": true
})
```

## Best Practices

1. **Use descriptive names** for your UI policies to make them easy to identify and maintain
2. **Set appropriate scope** using the applies_* flags to ensure policies apply only where needed
3. **Test thoroughly** across different contexts (catalog view, requested items, tasks)
4. **Document conditions** clearly in the description field for future maintenance
5. **Use clone functionality** to create variations of existing policies efficiently

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

Catalog UI Policies work closely with:
- **Catalog Items** - Use `list_catalog_items` to find items to apply policies to
- **Catalog Variables** - Use `list_catalog_variables` to understand form structure
- **Service Catalog** - Policies enhance the user experience in catalog forms

## Example Natural Language Commands for Claude

- "Create a catalog UI policy to hide the priority field for standard requests"
- "List all active catalog UI policies for the hardware request catalog item"
- "Update the policy to make it apply to requested items as well"
- "Clone the existing priority policy for use with software requests"
- "Show me all catalog UI policies that apply to catalog tasks"
- "Create a policy that shows additional fields when request type is 'urgent'"