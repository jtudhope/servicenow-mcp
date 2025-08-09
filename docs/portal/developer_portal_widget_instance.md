# Employee Center Widget Instance Management in ServiceNow MCP

The Employee Center Widget Instance Management tools provide comprehensive functionality for managing widget instances - variations in widget configurations on various portals including the Employee Center. These tools allow you to create, update, list, clone, and manage widget instances that define how widgets appear and behave on portal pages.

## Overview

Widget instances (`sp_instance` table) are specific configurations of widgets that can be placed on portal pages. Each instance can have unique styling, parameters, placement, and behavior while referencing the same base widget. This enables flexible portal customization and reusable widget configurations.

## Available Tools

### 1. create_widget_instance

Create a new widget instance with specified configuration and styling.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sp_widget | string | Yes | Widget sys_id that this instance references |
| sp_column | string | No | Column sys_id where the widget instance is placed |
| title | string | No | Display title for the widget instance |
| short_description | string | No | Short description of the widget instance |
| order | integer | No | Display order within the column (default: 1) |
| active | boolean | No | Whether the widget instance is active (default: true) |
| id | string | No | Unique identifier for the widget instance |
| widget_parameters | string | No | JSON-formatted widget configuration parameters |
| class_name | string | No | Bootstrap class name for styling |
| color | string | No | Bootstrap color scheme (default: "default") |
| size | string | No | Bootstrap size: xs, sm, md, lg (default: "md") |
| glyph | string | No | Icon/glyph for the widget instance |
| css | string | No | Custom CSS for the widget instance |
| url | string | No | URL/HREF for navigation widgets |
| roles | array | No | Roles required to view this widget instance |

#### Example

```python
result = create_widget_instance({
    "sp_widget": "widget_sys_id_123",
    "sp_column": "column_sys_id_456", 
    "title": "Employee Quick Actions",
    "short_description": "Quick access to common employee tasks",
    "order": 1,
    "active": true,
    "widget_parameters": '{"max_items": 5, "show_icons": true}',
    "color": "primary",
    "size": "lg",
    "roles": ["employee", "manager"]
})
```

### 2. update_widget_instance

Update an existing widget instance's configuration, styling, or placement.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | Widget instance sys_id to update |
| sp_widget | string | No | Updated widget sys_id |
| sp_column | string | No | Updated column sys_id |
| title | string | No | Updated display title |
| short_description | string | No | Updated short description |
| order | integer | No | Updated display order |
| active | boolean | No | Updated active status |
| id | string | No | Updated unique identifier |
| widget_parameters | string | No | Updated JSON widget parameters |
| class_name | string | No | Updated Bootstrap class name |
| color | string | No | Updated Bootstrap color |
| size | string | No | Updated Bootstrap size |
| glyph | string | No | Updated icon/glyph |
| css | string | No | Updated custom CSS |
| url | string | No | Updated URL/HREF |
| roles | array | No | Updated roles |

#### Example

```python
result = update_widget_instance({
    "instance_id": "instance_sys_id_123",
    "title": "Updated Employee Actions",
    "active": false,
    "color": "danger",
    "widget_parameters": '{"max_items": 10, "show_icons": false}'
})
```

### 3. list_widget_instances

List widget instances with optional filtering by widget, column, or active status.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sp_widget | string | No | Filter by widget sys_id |
| sp_column | string | No | Filter by column sys_id |
| active | boolean | No | Filter by active status |
| limit | integer | No | Maximum number of instances to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query filter |

#### Example

```python
result = list_widget_instances({
    "sp_widget": "widget_sys_id_123",
    "active": true,
    "limit": 20
})
```

### 4. get_widget_instance

Get detailed information about a specific widget instance.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | Widget instance sys_id or ID to retrieve |

#### Example

```python
result = get_widget_instance({
    "instance_id": "instance_sys_id_123"
})
```

### 5. delete_widget_instance

Delete a widget instance from the portal.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | Widget instance sys_id to delete |

#### Example

```python
result = delete_widget_instance({
    "instance_id": "instance_sys_id_123"
})
```

### 6. clone_widget_instance

Clone an existing widget instance to create a duplicate with optional modifications.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_instance_id | string | Yes | Source widget instance sys_id to clone |
| target_column | string | No | Target column sys_id for the cloned instance |
| title | string | No | Title for the cloned instance |
| widget_parameters | string | No | Updated parameters for the cloned instance |

#### Example

```python
result = clone_widget_instance({
    "source_instance_id": "source_instance_123",
    "target_column": "new_column_456",
    "title": "Copy of Employee Actions",
    "widget_parameters": '{"max_items": 8}'
})
```

### 7. bulk_update_widget_instances

Bulk update multiple widget instances simultaneously with the same property changes.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_ids | array | Yes | List of widget instance sys_ids to update |
| updates | object | Yes | Fields and values to update |

#### Example

```python
result = bulk_update_widget_instances({
    "instance_ids": ["instance1", "instance2", "instance3"],
    "updates": {
        "active": false,
        "color": "warning",
        "size": "sm"
    }
})
```

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| instance | object | Single widget instance data (for create/get/update operations) |
| instances | array | Multiple widget instances (for list/bulk operations) |
| total_count | integer | Total count for list operations |

## Common Use Cases

### Portal Customization
- Create themed widget instances for different departments
- Configure widget parameters for specific use cases
- Apply custom styling and branding

### Content Management
- Clone successful widget configurations to new locations
- Bulk update widget properties across multiple instances
- Manage widget visibility based on user roles

### Development Workflow
- Test widget configurations in development environments
- Migrate widget instances between environments
- Version control widget configurations

## Widget Parameters

The `widget_parameters` field accepts JSON-formatted configuration that is specific to each widget type. Common parameter patterns include:

```json
{
    "title": "Custom Widget Title",
    "max_items": 10,
    "show_icons": true,
    "color_scheme": "dark",
    "refresh_interval": 30,
    "table": "incident",
    "filter": "active=true",
    "fields": ["number", "short_description", "state"]
}
```

## Bootstrap Styling

Widget instances support Bootstrap styling through several fields:

- **color**: primary, secondary, success, danger, warning, info, light, dark, default
- **size**: xs (extra small), sm (small), md (medium), lg (large)
- **class_name**: Additional Bootstrap classes for custom styling

## Error Handling

All tools include comprehensive error handling and will return detailed error messages for common issues such as:

- Invalid sys_id references
- Missing required parameters
- Permission errors
- Network connectivity issues
- Invalid JSON in widget_parameters

## Best Practices

1. **Use descriptive titles and descriptions** to make widget instances easily identifiable
2. **Test widget parameters** in a development environment before deploying to production
3. **Use roles appropriately** to control widget visibility based on user permissions
4. **Clone successful configurations** rather than recreating complex widget instances
5. **Use bulk operations** for efficiency when updating multiple instances
6. **Validate JSON** in widget_parameters to prevent configuration errors
7. **Monitor widget performance** and adjust parameters as needed for optimal user experience