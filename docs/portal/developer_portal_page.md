# Portal UI Page Configuration Management in ServiceNow MCP

The Portal UI Page Configuration Management tools provide comprehensive functionality for managing Service Portal pages in ServiceNow's `sp_page` table. These tools enable developers to create, update, list, clone, and delete portal pages programmatically.

## Available Tools

### 1. create_portal_page

Creates a new portal page in the `sp_page` table with configurable properties.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier for the page |
| title | string | Yes | Display title of the page |
| short_description | string | No | Short description of the page |
| css | string | No | Page-specific CSS styling |
| public | boolean | No | Whether the page is publicly accessible (default: false) |
| roles | array[string] | No | List of roles required to access this page |
| internal | boolean | No | Whether this is an internal page (default: false) |
| draft | boolean | No | Whether the page is in draft mode (default: false) |
| omit_watcher | boolean | No | Whether to omit watcher functionality (default: false) |
| dynamic_title_structure | string | No | Dynamic page title structure |
| category | string | No | Page category (default: "custom") |
| use_seo_script | boolean | No | Whether to use SEO script (default: false) |
| seo_script | string | No | SEO script sys_id reference |
| human_readable_url_structure | string | No | Human readable URL structure |

#### Example

```python
result = create_portal_page({
    "id": "my_custom_page",
    "title": "My Custom Page",
    "short_description": "A custom portal page for our application",
    "public": True,
    "roles": ["admin", "sp_user"],
    "css": ".custom-page { background: #f5f5f5; }",
    "category": "custom"
})
```

### 2. update_portal_page

Updates an existing portal page in the `sp_page` table by ID or sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_id | string | Yes | Page ID or sys_id to update |
| title | string | No | Updated display title |
| short_description | string | No | Updated short description |
| css | string | No | Updated page-specific CSS |
| public | boolean | No | Updated public accessibility |
| roles | array[string] | No | Updated roles list |
| internal | boolean | No | Updated internal status |
| draft | boolean | No | Updated draft status |
| omit_watcher | boolean | No | Updated omit watcher setting |
| dynamic_title_structure | string | No | Updated dynamic title structure |
| category | string | No | Updated page category |
| use_seo_script | boolean | No | Updated SEO script usage |
| seo_script | string | No | Updated SEO script reference |
| human_readable_url_structure | string | No | Updated URL structure |

#### Example

```python
result = update_portal_page({
    "page_id": "my_custom_page",
    "title": "Updated Custom Page",
    "draft": False,
    "public": True
})
```

### 3. list_portal_pages

Lists portal pages from the `sp_page` table with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of pages to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| category | string | No | Filter by category |
| public | boolean | No | Filter by public status |
| draft | boolean | No | Filter by draft status |
| internal | boolean | No | Filter by internal status |
| query | string | No | Additional query string |

#### Example

```python
result = list_portal_pages({
    "limit": 20,
    "category": "custom",
    "draft": False,
    "public": True
})
```

### 4. get_portal_page

Gets detailed information about a specific portal page by ID or sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_id | string | Yes | Page ID or sys_id to retrieve |

#### Example

```python
result = get_portal_page({
    "page_id": "my_custom_page"
})
```

### 5. clone_portal_page

Clones an existing portal page to create a duplicate with optional modifications.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_page_id | string | Yes | Source page ID or sys_id to clone |
| new_page_id | string | Yes | New unique ID for the cloned page |
| new_title | string | Yes | Title for the cloned page |
| new_short_description | string | No | Short description for the cloned page |
| copy_css | boolean | No | Whether to copy CSS from source (default: true) |
| copy_roles | boolean | No | Whether to copy roles from source (default: true) |

#### Example

```python
result = clone_portal_page({
    "source_page_id": "existing_page",
    "new_page_id": "cloned_page",
    "new_title": "Cloned Page Title",
    "new_short_description": "This is a clone of the existing page",
    "copy_css": True,
    "copy_roles": False
})
```

### 6. delete_portal_page

Deletes a portal page from the `sp_page` table by ID or sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_id | string | Yes | Page ID or sys_id to delete |

#### Example

```python
result = delete_portal_page({
    "page_id": "page_to_delete"
})
```

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| page_id | string | Page sys_id (when applicable) |
| page_data | object | Page data (for create, update, get, clone operations) |
| pages | array[object] | List of pages (for list operations) |
| total_count | integer | Total count (for list operations) |

## Common Use Cases

### Creating a Public Landing Page

```python
# Create a public landing page with custom styling
result = create_portal_page({
    "id": "company_landing",
    "title": "Company Landing Page",
    "short_description": "Main landing page for external users",
    "public": True,
    "css": """
        .landing-header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
        }
        .landing-content {
            max-width: 1200px;
            margin: 0 auto;
        }
    """,
    "category": "public"
})
```

### Setting Up Role-Based Access Pages

```python
# Create an admin dashboard page
result = create_portal_page({
    "id": "admin_dashboard",
    "title": "Administrator Dashboard",
    "short_description": "Administrative controls and monitoring",
    "public": False,
    "roles": ["admin", "sp_admin"],
    "internal": True,
    "category": "administrative"
})
```

### Cloning Pages for Development

```python
# Clone a production page for development
result = clone_portal_page({
    "source_page_id": "prod_homepage",
    "new_page_id": "dev_homepage",
    "new_title": "Development Homepage",
    "new_short_description": "Development version of the homepage",
    "copy_css": True,
    "copy_roles": False
})
```

### Managing Page Lifecycle

```python
# Create as draft, then publish
create_result = create_portal_page({
    "id": "new_feature_page",
    "title": "New Feature Page",
    "draft": True,
    "public": False
})

# Later, publish the page
update_result = update_portal_page({
    "page_id": "new_feature_page",
    "draft": False,
    "public": True
})
```

## Best Practices

1. **Use meaningful page IDs**: Choose descriptive, consistent naming conventions for page IDs
2. **Start with drafts**: Create new pages as drafts first to test before making them live
3. **Manage roles carefully**: Ensure proper role-based access control for sensitive pages
4. **Clone for variations**: Use cloning to create variations of existing pages efficiently
5. **Monitor page performance**: Use CSS optimization and avoid overly complex styling
6. **Maintain consistency**: Use consistent categories and naming patterns across your portal

## Error Handling

All tools include comprehensive error handling for common scenarios:

- Page not found errors
- Duplicate ID conflicts
- Network connectivity issues
- Permission-related errors
- Invalid parameter validation

Always check the `success` field in the response and handle errors appropriately in your application logic.