# Portal Container Management in ServiceNow MCP

This document describes the Portal Container Management tools available in the ServiceNow MCP server. These tools allow you to manage portal container configurations in the `sp_container` table, including creating, updating, listing, cloning, and organizing containers within Service Portal pages.

## Overview

Portal containers are the foundational layout elements in ServiceNow Service Portals. They define the structure and styling of page sections, including background settings, CSS classes, width configurations, and semantic markup. The Portal Container Management tools provide comprehensive control over these elements.

## Available Tools

### create_portal_container

Creates a new portal container with configurable properties.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the container |
| sp_page | string | Yes | Page sys_id that this container belongs to |
| order | integer | No | Display order within the page |
| class_name | string | No | Parent CSS class name |
| container_class_name | string | No | Container CSS class name |
| width | string | No | Width setting (container, container-fluid, etc.) |
| background_color | string | No | Background color |
| background_image | string | No | Background image attachment |
| background_style | string | No | Background style |
| bootstrap_alt | boolean | No | Use Bootstrap alternative |
| subheader | boolean | No | Move to header |
| title | string | No | Screen reader title |
| semantic_tag | string | No | Semantic HTML tag |

#### Example

```python
result = create_portal_container({
    "name": "Main Content Container",
    "sp_page": "homepage_page_id",
    "order": 10,
    "width": "container-fluid",
    "semantic_tag": "main",
    "background_color": "#f8f9fa"
})
```

### update_portal_container

Updates an existing portal container by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| container_id | string | Yes | Container sys_id to update |
| name | string | No | Updated name of the container |
| sp_page | string | No | Updated page sys_id |
| order | integer | No | Updated display order |
| class_name | string | No | Updated parent CSS class name |
| container_class_name | string | No | Updated container CSS class name |
| width | string | No | Updated width setting |
| background_color | string | No | Updated background color |
| background_image | string | No | Updated background image |
| background_style | string | No | Updated background style |
| bootstrap_alt | boolean | No | Updated Bootstrap alternative setting |
| subheader | boolean | No | Updated move to header setting |
| title | string | No | Updated screen reader title |
| semantic_tag | string | No | Updated semantic HTML tag |

#### Example

```python
result = update_portal_container({
    "container_id": "container_sys_id",
    "name": "Updated Container Name",
    "width": "container",
    "background_color": "#ffffff"
})
```

### list_portal_containers

Lists portal containers with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sp_page | string | No | Filter by page sys_id |
| semantic_tag | string | No | Filter by semantic tag |
| width | string | No | Filter by width setting |
| limit | integer | No | Maximum number of containers to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query string |

#### Example

```python
result = list_portal_containers({
    "sp_page": "homepage_page_id",
    "limit": 20,
    "offset": 0
})
```

### get_portal_container

Retrieves detailed information about a specific portal container.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| container_id | string | Yes | Container sys_id or name to retrieve |

#### Example

```python
result = get_portal_container({
    "container_id": "container_sys_id"
})
```

### clone_portal_container

Clones an existing portal container to create a duplicate with optional modifications.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_container_id | string | Yes | Source container sys_id to clone |
| new_name | string | Yes | Name for the cloned container |
| target_page | string | Yes | Target page sys_id for the cloned container |
| copy_background | boolean | No | Whether to copy background settings (default: true) |
| copy_styling | boolean | No | Whether to copy styling from source (default: true) |
| new_order | integer | No | Order for the cloned container (auto-calculated if not provided) |

#### Example

```python
result = clone_portal_container({
    "source_container_id": "source_container_sys_id",
    "new_name": "Cloned Main Container",
    "target_page": "new_page_sys_id",
    "copy_background": true,
    "copy_styling": true
})
```

### delete_portal_container

Deletes a portal container from the sp_container table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| container_id | string | Yes | Container sys_id to delete |

#### Example

```python
result = delete_portal_container({
    "container_id": "container_sys_id"
})
```

### reorder_portal_containers

Reorders portal containers within a page by updating their order values.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_id | string | Yes | Page sys_id to reorder containers within |
| container_order | array | Yes | List of container sys_ids in desired order |

#### Example

```python
result = reorder_portal_containers({
    "page_id": "page_sys_id",
    "container_order": ["container1_id", "container2_id", "container3_id"]
})
```

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| container | object | Container data (for single container operations) |
| containers | array | List of containers (for list operations) |
| total_count | integer | Total count of containers (for list operations) |

## Common Use Cases

### Setting Up a New Page Layout

1. **Create containers** for different sections (header, content, footer)
2. **Configure styling** with appropriate CSS classes and semantic tags
3. **Set display order** to control layout flow
4. **Apply background styling** for visual design

### Reorganizing Page Structure

1. **List existing containers** for a page
2. **Update container properties** as needed
3. **Reorder containers** to change layout sequence
4. **Clone containers** to replicate layouts across pages

### Styling and Theming

1. **Update background settings** for visual consistency
2. **Apply CSS classes** for responsive design
3. **Set semantic tags** for accessibility and SEO
4. **Configure width settings** for layout control

## Best Practices

1. **Use semantic HTML tags** (main, section, aside, etc.) for better accessibility
2. **Set meaningful names** for containers to aid in identification
3. **Use consistent ordering** (increments of 10) for easy reordering
4. **Apply appropriate width settings** based on design requirements
5. **Consider responsive design** when setting CSS classes
6. **Test accessibility** with screen reader titles
7. **Use cloning** to maintain consistency across similar pages

## Error Handling

All tools include comprehensive error handling for common scenarios:

- **Invalid sys_ids**: Returns clear error messages
- **Missing required parameters**: Validates input before API calls
- **Network failures**: Handles connection and timeout errors
- **Permission issues**: Reports authentication and authorization errors
- **API limitations**: Manages ServiceNow API constraints

## Integration with Other Tools

Portal Container Management tools work seamlessly with:

- **Portal Page Management**: Containers belong to specific pages
- **Portal Row Management**: Containers contain rows for layout structure
- **Portal Widget Management**: Widgets are placed within container layouts
- **Portal Theme Management**: Containers inherit styling from themes