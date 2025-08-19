# Variable Sets Management in ServiceNow MCP

This document describes the tools available for managing Variable Sets in ServiceNow using the ServiceNow MCP server.

## Overview

Variable Sets are reusable collections of Catalog Variables that you can group together and then attach to one or more catalog items or record producers. They provide a way to standardize forms and reduce duplication across multiple catalog items. These tools allow you to create, list, update, and delete Variable Sets stored in the item_option_new_set table.

## Available Tools

### create_variable_set

Creates a new Variable Set in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Title of the variable set |
| internal_name | string | Yes | Internal name of the variable set |
| description | string | No | Description of the variable set |
| order | integer | No | Display order of the variable set (default: 100) |
| display_title | boolean | No | Whether to display the title (default: false) |
| layout | string | No | Layout of the variable set (default: "normal") |
| read_roles | array | No | Roles required to read the variable set |
| write_roles | array | No | Roles required to write the variable set |
| create_roles | array | No | Roles required to create the variable set |
| set_attributes | string | No | Variable set attributes |

#### Example

```python
result = create_variable_set({
    "title": "Standard Contact Information",
    "internal_name": "std_contact_info",
    "description": "Common contact fields used across multiple catalog items",
    "order": 100,
    "display_title": true,
    "layout": "normal",
    "read_roles": ["catalog_admin", "catalog_editor"]
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| variable_set_id | string | The sys_id of the created variable set |
| variable_set_data | object | Details of the created variable set |

### list_variable_sets

Lists Variable Sets from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title_contains | string | No | Filter by title containing text |
| internal_name_contains | string | No | Filter by internal name containing text |
| include_details | boolean | No | Whether to include detailed information (default: true) |
| limit | integer | No | Maximum number of variable sets to return (default: 50) |
| offset | integer | No | Offset for pagination (default: 0) |

#### Example

```python
result = list_variable_sets({
    "title_contains": "contact",
    "include_details": true,
    "limit": 20,
    "offset": 0
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| variable_sets | array | List of variable sets |
| total_count | integer | Total number of variable sets found |

### update_variable_set

Updates an existing Variable Set in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| variable_set_id | string | Yes | The sys_id of the variable set to update |
| title | string | No | Title of the variable set |
| internal_name | string | No | Internal name of the variable set |
| description | string | No | Description of the variable set |
| order | integer | No | Display order of the variable set |
| display_title | boolean | No | Whether to display the title |
| layout | string | No | Layout of the variable set |
| read_roles | array | No | Roles required to read the variable set |
| write_roles | array | No | Roles required to write the variable set |
| create_roles | array | No | Roles required to create the variable set |
| set_attributes | string | No | Variable set attributes |

#### Example

```python
result = update_variable_set({
    "variable_set_id": "abc123",
    "title": "Updated Contact Information",
    "description": "Updated description for contact fields",
    "order": 50,
    "display_title": false
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| variable_set_data | object | Updated variable set details |

### get_variable_set

Retrieves detailed information about a specific Variable Set.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| variable_set_id | string | Yes | The sys_id of the variable set to retrieve |

#### Example

```python
result = get_variable_set({
    "variable_set_id": "abc123"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| variable_set_data | object | Variable set details |

### delete_variable_set

Deletes a Variable Set from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| variable_set_id | string | Yes | The sys_id of the variable set to delete |

#### Example

```python
result = delete_variable_set({
    "variable_set_id": "abc123"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |

## Variable Set Layout Types

ServiceNow supports different layout types for Variable Sets:

| Layout | Description |
|--------|-------------|
| normal | Standard vertical layout with labels above fields |
| 2_column | Two-column layout for compact forms |
| label_left | Layout with labels to the left of fields |
| label_right | Layout with labels to the right of fields |

## Example Usage with Claude

Once the ServiceNow MCP server is configured with Claude, you can ask Claude to perform actions like:

- "Create a Variable Set for standard contact information fields"
- "List all Variable Sets containing 'approval' in the title"
- "Update the Variable Set with ID abc123 to change the title"
- "Show details for the employee onboarding Variable Set"
- "Delete the old contact information Variable Set"
- "Create a Variable Set for hardware request common fields with 2-column layout"
- "Find all Variable Sets that can be read by catalog_admin role"
- "Update the order of the standard approval Variable Set to display first"

## Best Practices

### Naming Conventions

1. **Title**: Use descriptive, user-friendly names
   - Good: "Standard Contact Information"
   - Bad: "contact_info"

2. **Internal Name**: Use consistent naming conventions
   - Good: "std_contact_info", "hrw_approval_fields"
   - Bad: "ContactInformation", "fields1"

### Organization

1. **Grouping**: Group related fields logically
   - Contact information fields together
   - Approval fields together
   - Technical specifications together

2. **Reusability**: Design Variable Sets to be reusable across multiple catalog items
   - Avoid item-specific fields in shared Variable Sets
   - Use generic field names when possible

### Security

1. **Role-based Access**: Use appropriate roles for read/write/create permissions
   - Limit creation to administrators
   - Allow catalog editors to read/write
   - Restrict sensitive fields to specific roles

## Troubleshooting

### Common Errors

1. **Error: `Title and internal_name are required`**
   - This error occurs when creating a Variable Set without providing both required fields.
   - Solution: Always include both `title` and `internal_name` when creating Variable Sets.

2. **Error: `Variable Set not found`**
   - This error occurs when trying to update, get, or delete a Variable Set that doesn't exist.
   - Solution: Verify the `variable_set_id` exists by listing Variable Sets first.

3. **Error: `Invalid layout type`**
   - This error occurs when providing an unsupported layout value.
   - Solution: Use one of the supported layout types: normal, 2_column, label_left, label_right.

4. **Error: `Role does not exist`**
   - This error occurs when specifying roles that don't exist in ServiceNow.
   - Solution: Verify role names exist in the sys_user_role table before assigning them.

5. **Error: `Duplicate internal_name`**
   - This error occurs when trying to create a Variable Set with an internal_name that already exists.
   - Solution: Use a unique internal_name or update the existing Variable Set instead.