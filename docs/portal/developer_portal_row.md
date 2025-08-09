# Portal UI Row Management in ServiceNow MCP

The Portal UI Row Management tools provide comprehensive functionality for managing Service Portal rows in ServiceNow's `sp_row` table. These tools enable developers to create, update, list, clone, delete, and reorder portal rows programmatically. Rows are fundamental layout components in Service Portal that contain columns and help structure page content.

## Available Tools

### 1. create_portal_row

Creates a new portal row in the `sp_row` table with configurable properties.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sp_container | string | No* | Container sys_id that this row belongs to |
| sp_column | string | No* | Column sys_id that this row belongs to |
| class_name | string | No | CSS class name for styling |
| order | integer | No | Display order within the container/column |
| semantic_tag | string | No | Semantic HTML tag (e.g., 'section', 'article', 'div') |

*Note: Either `sp_container` or `sp_column` must be specified.

#### Example

```python
result = create_portal_row({
    "sp_container": "container_sys_id_123",
    "class_name": "hero-section",
    "order": 1,
    "semantic_tag": "section"
})
```

### 2. update_portal_row

Updates an existing portal row in the `sp_row` table by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| row_id | string | Yes | Row sys_id to update |
| sp_container | string | No | Updated container sys_id |
| sp_column | string | No | Updated column sys_id |
| class_name | string | No | Updated CSS class name |
| order | integer | No | Updated display order |
| semantic_tag | string | No | Updated semantic HTML tag |

#### Example

```python
result = update_portal_row({
    "row_id": "row_sys_id_123",
    "class_name": "updated-hero-section",
    "order": 2,
    "semantic_tag": "article"
})
```

### 3. list_portal_rows

Lists portal rows from the `sp_row` table with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of rows to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| sp_container | string | No | Filter by container sys_id |
| sp_column | string | No | Filter by column sys_id |
| semantic_tag | string | No | Filter by semantic tag |
| query | string | No | Additional query string |

#### Example

```python
result = list_portal_rows({
    "limit": 20,
    "sp_container": "container_sys_id_123",
    "semantic_tag": "section"
})
```

### 4. get_portal_row

Gets detailed information about a specific portal row by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| row_id | string | Yes | Row sys_id to retrieve |

#### Example

```python
result = get_portal_row({
    "row_id": "row_sys_id_123"
})
```

### 5. clone_portal_row

Clones an existing portal row to create a duplicate with optional modifications.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_row_id | string | Yes | Source row sys_id to clone |
| target_container | string | No | Target container sys_id for the cloned row |
| target_column | string | No | Target column sys_id for the cloned row |
| copy_class_name | boolean | No | Whether to copy CSS class name from source (default: true) |
| new_order | integer | No | Order for the cloned row (auto-calculated if not provided) |
| copy_semantic_tag | boolean | No | Whether to copy semantic tag from source (default: true) |

#### Example

```python
result = clone_portal_row({
    "source_row_id": "existing_row_sys_id",
    "target_container": "new_container_sys_id",
    "copy_class_name": True,
    "copy_semantic_tag": False,
    "new_order": 3
})
```

### 6. delete_portal_row

Deletes a portal row from the `sp_row` table by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| row_id | string | Yes | Row sys_id to delete |

#### Example

```python
result = delete_portal_row({
    "row_id": "row_sys_id_to_delete"
})
```

### 7. reorder_portal_rows

Reorders portal rows within a container or column by updating their order values.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| container_id | string | No* | Container sys_id to reorder rows within |
| column_id | string | No* | Column sys_id to reorder rows within |
| row_order | array[string] | Yes | List of row sys_ids in desired order |

*Note: Either `container_id` or `column_id` must be specified.

#### Example

```python
result = reorder_portal_rows({
    "container_id": "container_sys_id_123",
    "row_order": ["row1_sys_id", "row3_sys_id", "row2_sys_id"]
})
```

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| row_id | string | Row sys_id (when applicable) |
| row_data | object | Row data (for create, update, get, clone operations) |
| rows | array[object] | List of rows (for list operations) |
| total_count | integer | Total count (for list operations) |

## Common Use Cases

### Creating Layout Structure

```python
# Create main content row
main_row = create_portal_row({
    "sp_container": "homepage_container",
    "class_name": "main-content-row",
    "order": 1,
    "semantic_tag": "main"
})

# Create header row
header_row = create_portal_row({
    "sp_container": "homepage_container", 
    "class_name": "header-row",
    "order": 0,
    "semantic_tag": "header"
})
```

### Cloning Layout Components

```python
# Clone a successful row layout to another container
result = clone_portal_row({
    "source_row_id": "successful_layout_row",
    "target_container": "new_page_container",
    "copy_class_name": True,
    "copy_semantic_tag": True
})
```

### Reorganizing Page Layout

```python
# First, get all rows in a container
rows_result = list_portal_rows({
    "sp_container": "container_sys_id_123",
    "limit": 100
})

# Then reorder them based on new requirements
reorder_result = reorder_portal_rows({
    "container_id": "container_sys_id_123",
    "row_order": ["important_row", "secondary_row", "footer_row"]
})
```

### Semantic HTML Structure

```python
# Create semantically meaningful layout
header_row = create_portal_row({
    "sp_container": "page_container",
    "class_name": "page-header",
    "semantic_tag": "header",
    "order": 1
})

nav_row = create_portal_row({
    "sp_container": "page_container",
    "class_name": "main-navigation", 
    "semantic_tag": "nav",
    "order": 2
})

content_row = create_portal_row({
    "sp_container": "page_container",
    "class_name": "main-content",
    "semantic_tag": "main",
    "order": 3
})

footer_row = create_portal_row({
    "sp_container": "page_container",
    "class_name": "page-footer",
    "semantic_tag": "footer", 
    "order": 4
})
```

### Responsive Layout Management

```python
# Create rows with responsive CSS classes
mobile_row = create_portal_row({
    "sp_container": "responsive_container",
    "class_name": "d-block d-md-none mobile-only-row",
    "semantic_tag": "section",
    "order": 1
})

desktop_row = create_portal_row({
    "sp_container": "responsive_container",
    "class_name": "d-none d-md-block desktop-only-row",
    "semantic_tag": "section", 
    "order": 2
})
```

## Best Practices

1. **Use Semantic Tags**: Choose appropriate HTML5 semantic tags (header, nav, main, section, article, aside, footer) for better accessibility and SEO
2. **Consistent CSS Classes**: Use consistent, descriptive CSS class names that follow your organization's naming conventions
3. **Logical Ordering**: Set meaningful order values that reflect the visual and logical flow of content
4. **Container Hierarchy**: Understand the relationship between containers, rows, and columns in the Service Portal structure
5. **Clone for Consistency**: Use cloning to maintain consistent layouts across different pages or sections
6. **Clean Up**: Delete unused rows to keep your portal structure clean and maintainable
7. **Batch Operations**: Use reordering to efficiently reorganize multiple rows at once

## Portal Structure Hierarchy

Understanding the Service Portal structure hierarchy is crucial:

1. **Portal** → Contains pages
2. **Page** → Contains containers
3. **Container** → Contains rows
4. **Row** → Contains columns (sp_column)
5. **Column** → Contains widget instances

Rows serve as horizontal layout sections that can contain multiple columns, enabling flexible grid-based layouts.

## Error Handling

All tools include comprehensive error handling for common scenarios:

- Invalid sys_id references
- Missing required container/column relationships
- Network connectivity issues
- Permission-related errors
- Validation errors for required parameters

Always check the `success` field in the response and handle errors appropriately in your application logic.

## Performance Considerations

- When reordering many rows, consider the impact on page load times
- Use appropriate CSS classes to minimize custom styling overhead
- Be mindful of the visual hierarchy when setting order values
- Consider caching implications when frequently updating row configurations