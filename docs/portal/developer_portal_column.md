# Portal UI Column Management in ServiceNow MCP

The Portal UI Column Management tools provide comprehensive functionality for managing Service Portal columns in ServiceNow's `sp_column` table. These tools enable developers to create, update, list, clone, delete, and reorder portal columns programmatically. Columns are crucial layout components that provide Bootstrap-based responsive grid functionality within Service Portal rows.

## Available Tools

### 1. create_portal_column

Creates a new portal column in the `sp_column` table with configurable responsive properties.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sp_row | string | Yes | Row sys_id that this column belongs to |
| class_name | string | No | CSS class name for styling |
| order | integer | No | Display order within the row |
| size | integer | No | Bootstrap column size for medium devices (1-12) |
| size_xs | integer | No | Bootstrap column size for extra small devices (1-12) |
| size_sm | integer | No | Bootstrap column size for small devices (1-12) |
| size_lg | integer | No | Bootstrap column size for large devices (1-12) |
| semantic_tag | string | No | Semantic HTML tag (e.g., 'aside', 'article', 'div') |

#### Example

```python
result = create_portal_column({
    "sp_row": "row_sys_id_123",
    "class_name": "sidebar-column",
    "size": 4,
    "size_sm": 12,
    "size_xs": 12,
    "order": 1,
    "semantic_tag": "aside"
})
```

### 2. update_portal_column

Updates an existing portal column in the `sp_column` table by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| column_id | string | Yes | Column sys_id to update |
| sp_row | string | No | Updated row sys_id |
| class_name | string | No | Updated CSS class name |
| order | integer | No | Updated display order |
| size | integer | No | Updated Bootstrap column size for medium devices (1-12) |
| size_xs | integer | No | Updated Bootstrap column size for extra small devices (1-12) |
| size_sm | integer | No | Updated Bootstrap column size for small devices (1-12) |
| size_lg | integer | No | Updated Bootstrap column size for large devices (1-12) |
| semantic_tag | string | No | Updated semantic HTML tag |

#### Example

```python
result = update_portal_column({
    "column_id": "column_sys_id_123",
    "size": 6,
    "size_sm": 12,
    "class_name": "main-content-column",
    "semantic_tag": "main"
})
```

### 3. list_portal_columns

Lists portal columns from the `sp_column` table with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of columns to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| sp_row | string | No | Filter by row sys_id |
| semantic_tag | string | No | Filter by semantic tag |
| size_filter | string | No | Filter by size range (e.g., '>=6' or '=12') |
| query | string | No | Additional query string |

#### Example

```python
result = list_portal_columns({
    "limit": 20,
    "sp_row": "row_sys_id_123",
    "size_filter": ">=6"
})
```

### 4. get_portal_column

Gets detailed information about a specific portal column by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| column_id | string | Yes | Column sys_id to retrieve |

#### Example

```python
result = get_portal_column({
    "column_id": "column_sys_id_123"
})
```

### 5. clone_portal_column

Clones an existing portal column to create a duplicate with optional modifications.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_column_id | string | Yes | Source column sys_id to clone |
| target_row | string | Yes | Target row sys_id for the cloned column |
| copy_class_name | boolean | No | Whether to copy CSS class name from source (default: true) |
| copy_sizes | boolean | No | Whether to copy all responsive sizes from source (default: true) |
| copy_semantic_tag | boolean | No | Whether to copy semantic tag from source (default: true) |
| new_order | integer | No | Order for the cloned column (auto-calculated if not provided) |
| override_sizes | object | No | Override specific sizes (e.g., {'size': 6, 'size_sm': 12}) |

#### Example

```python
result = clone_portal_column({
    "source_column_id": "existing_column_sys_id",
    "target_row": "new_row_sys_id",
    "copy_class_name": True,
    "copy_sizes": False,
    "override_sizes": {
        "size": 8,
        "size_sm": 12,
        "size_xs": 12
    }
})
```

### 6. delete_portal_column

Deletes a portal column from the `sp_column` table by sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| column_id | string | Yes | Column sys_id to delete |

#### Example

```python
result = delete_portal_column({
    "column_id": "column_sys_id_to_delete"
})
```

### 7. reorder_portal_columns

Reorders portal columns within a row by updating their order values.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| row_id | string | Yes | Row sys_id to reorder columns within |
| column_order | array[string] | Yes | List of column sys_ids in desired order |

#### Example

```python
result = reorder_portal_columns({
    "row_id": "row_sys_id_123",
    "column_order": ["col1_sys_id", "col3_sys_id", "col2_sys_id"]
})
```

### 8. create_responsive_grid

Creates a responsive grid layout by generating multiple columns with specified configurations in a single operation.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sp_row | string | Yes | Row sys_id to create columns in |
| grid_layout | array[object] | Yes | List of column configurations |

#### Example

```python
result = create_responsive_grid({
    "sp_row": "row_sys_id_123",
    "grid_layout": [
        {
            "size": 3,
            "size_sm": 12,
            "class_name": "sidebar",
            "semantic_tag": "aside"
        },
        {
            "size": 6,
            "size_sm": 12,
            "class_name": "main-content",
            "semantic_tag": "main"
        },
        {
            "size": 3,
            "size_sm": 12,
            "class_name": "widgets",
            "semantic_tag": "aside"
        }
    ]
})
```

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| column_id | string | Column sys_id (when applicable) |
| column_data | object | Column data (for create, update, get, clone operations) |
| columns | array[object] | List of columns (for list operations and responsive grid) |
| total_count | integer | Total count (for list operations) |

## Bootstrap Grid System

ServiceNow Service Portal uses Bootstrap's 12-column grid system with responsive breakpoints:

| Size | Breakpoint | Description |
|------|------------|-------------|
| size_xs | <576px | Extra small devices (phones) |
| size_sm | ≥576px | Small devices (landscape phones) |
| size (md) | ≥768px | Medium devices (tablets) |
| size_lg | ≥992px | Large devices (desktops) |

Column sizes range from 1-12, where 12 represents full width.

## Common Use Cases

### Creating Responsive Layouts

```python
# Create a two-column layout: sidebar and main content
result = create_responsive_grid({
    "sp_row": "homepage_row",
    "grid_layout": [
        {
            "size": 3,        # 1/4 width on desktop
            "size_sm": 12,    # Full width on mobile
            "class_name": "sidebar-column",
            "semantic_tag": "aside"
        },
        {
            "size": 9,        # 3/4 width on desktop
            "size_sm": 12,    # Full width on mobile
            "class_name": "main-content-column",
            "semantic_tag": "main"
        }
    ]
})
```

### Cloning Column Layouts

```python
# Clone a successful column layout to another row
result = clone_portal_column({
    "source_column_id": "successful_column_layout",
    "target_row": "new_page_row",
    "copy_class_name": True,
    "copy_sizes": True,
    "copy_semantic_tag": True
})
```

### Creating Equal-Width Columns

```python
# Create three equal columns
equal_columns = []
for i in range(3):
    equal_columns.append({
        "size": 4,        # 4 out of 12 = 1/3 width
        "size_sm": 12,    # Full width on mobile
        "class_name": f"equal-column-{i+1}"
    })

result = create_responsive_grid({
    "sp_row": "features_row",
    "grid_layout": equal_columns
})
```

### Mobile-First Design

```python
# Create mobile-first responsive columns
result = create_portal_column({
    "sp_row": "responsive_row",
    "size_xs": 12,    # Full width on phones
    "size_sm": 6,     # Half width on small tablets
    "size": 4,        # 1/3 width on medium devices
    "size_lg": 3,     # 1/4 width on large desktops
    "class_name": "responsive-column"
})
```

### Content-Specific Layouts

```python
# Blog post layout with content and sidebar
blog_layout = [
    {
        "size": 8,
        "size_sm": 12,
        "class_name": "blog-content",
        "semantic_tag": "article"
    },
    {
        "size": 4,
        "size_sm": 12,
        "class_name": "blog-sidebar",
        "semantic_tag": "aside"
    }
]

result = create_responsive_grid({
    "sp_row": "blog_row",
    "grid_layout": blog_layout
})
```

### Updating Column Responsiveness

```python
# Update a column to be more mobile-friendly
result = update_portal_column({
    "column_id": "desktop_only_column",
    "size_xs": 12,  # Full width on mobile
    "size_sm": 6,   # Half width on tablets
    "size": 4       # Keep 1/3 width on desktop
})
```

## Best Practices

1. **Mobile-First Approach**: Always consider mobile layout first, then enhance for larger screens
2. **Use Semantic Tags**: Choose appropriate semantic tags (main, aside, article, section) for better accessibility
3. **Maintain 12-Column Total**: Ensure column sizes within a row sum to 12 for proper layout
4. **Consistent Breakpoints**: Use consistent responsive breakpoints across your portal
5. **Meaningful CSS Classes**: Use descriptive class names that reflect content purpose, not just layout
6. **Test Across Devices**: Verify responsive behavior on different screen sizes
7. **Clone for Consistency**: Use cloning to maintain consistent layouts across different pages
8. **Batch Creation**: Use `create_responsive_grid` for creating multiple related columns efficiently

## Responsive Design Patterns

### Common Layout Patterns

1. **Sidebar Layout**: 3/9 or 4/8 column split with mobile stacking
2. **Three Column**: 3/6/3 layout with mobile stacking
3. **Card Grid**: Equal width columns that stack on mobile
4. **Content + Ads**: 8/4 split for content and advertising
5. **Dashboard**: Multiple equal columns for widget placement

### Example Bootstrap Classes

The Service Portal automatically generates Bootstrap classes based on your size settings:
- `col-xs-12 col-sm-6 col-md-4 col-lg-3` for a progressive layout
- `col-md-6` for half-width on medium devices and up
- `col-xs-12` for full-width on all devices

## Error Handling

All tools include comprehensive error handling for common scenarios:

- Invalid sys_id references
- Invalid size values (outside 1-12 range)
- Missing row relationships
- Network connectivity issues
- Permission-related errors
- Bootstrap grid validation

Always check the `success` field in the response and handle errors appropriately in your application logic.

## Performance Considerations

- Use appropriate column counts to avoid overly complex layouts
- Consider the impact of many small columns on mobile devices
- Be mindful of content density in narrow columns
- Use semantic tags to improve accessibility and SEO
- Test layout performance across different devices and connection speeds