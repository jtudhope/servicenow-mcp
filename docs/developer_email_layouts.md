# Email Layouts Management in ServiceNow MCP

The Email Layouts tools provide comprehensive functionality for managing email layouts in ServiceNow's sys_email_layout table. Email layouts define branding and formatting that wraps around email templates and notifications, providing consistent visual design across all email communications.

## Available Tools

### create_email_layout

Create a new email layout with HTML content and optional advanced XML configuration.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the email layout |
| layout | string | Yes | HTML layout content for the email |
| description | string | No | Description of the email layout |
| advanced | boolean | No | Whether this is an advanced layout (default: false) |
| advanced_layout | string | No | Advanced XML layout content |

**Example:**
```python
result = create_email_layout({
    "name": "Corporate Branding Layout",
    "description": "Standard corporate email layout with logo and footer",
    "layout": "<html><head><title>Email</title></head><body><div class='header'>{{header}}</div><div class='content'>{{content}}</div><div class='footer'>{{footer}}</div></body></html>",
    "advanced": false
})
```

### update_email_layout

Update an existing email layout by sys_id.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| layout_id | string | Yes | Email layout sys_id |
| name | string | No | Updated name of the email layout |
| description | string | No | Updated description |
| layout | string | No | Updated HTML layout content |
| advanced | boolean | No | Updated advanced layout flag |
| advanced_layout | string | No | Updated advanced XML layout content |

**Example:**
```python
result = update_email_layout({
    "layout_id": "a1b2c3d4e5f6g7h8i9j0",
    "name": "Updated Corporate Layout",
    "description": "Updated description with new branding guidelines",
    "layout": "<html><head><title>Email</title></head><body><div class='new-header'>{{header}}</div><div class='content'>{{content}}</div><div class='new-footer'>{{footer}}</div></body></html>"
})
```

### list_email_layouts

Retrieve a list of email layouts with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of layouts to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| advanced | boolean | No | Filter by advanced layout status |
| query | string | No | Search query for layout name or description |

**Example:**
```python
result = list_email_layouts({
    "limit": 20,
    "advanced": false,
    "query": "corporate"
})
```

### get_email_layout

Retrieve detailed information about a specific email layout.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| layout_id | string | Yes | Email layout sys_id |

**Example:**
```python
result = get_email_layout({
    "layout_id": "a1b2c3d4e5f6g7h8i9j0"
})
```

### delete_email_layout

Remove an email layout from the system.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| layout_id | string | Yes | Email layout sys_id |

**Example:**
```python
result = delete_email_layout({
    "layout_id": "a1b2c3d4e5f6g7h8i9j0"
})
```

### clone_email_layout

Create a copy of an existing email layout with a new name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| layout_id | string | Yes | Source email layout sys_id |
| new_name | string | Yes | Name for the cloned layout |

**Example:**
```python
result = clone_email_layout({
    "layout_id": "a1b2c3d4e5f6g7h8i9j0",
    "new_name": "Corporate Layout - Copy"
})
```

## Response Format

All email layout tools return responses with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | Email layout data (for create, update, get operations) |

### Email Layout Data Structure

When returning email layout data, the following fields are included:

| Field | Type | Description |
|-------|------|-------------|
| sys_id | string | Unique system identifier |
| name | string | Layout name |
| description | string | Layout description |
| layout | string | HTML layout content |
| advanced | string | Advanced layout flag ("true"/"false") |
| advanced_layout | string | Advanced XML layout content |
| sys_created_on | string | Creation timestamp |
| sys_updated_on | string | Last update timestamp |

## Use Cases

### Email Branding and Consistency
- Create standardized layouts for different departments or communication types
- Ensure consistent branding across all email communications
- Maintain corporate visual identity in automated notifications

### Template Management
- Develop reusable layout templates for different email categories
- Separate content from presentation for easier maintenance
- Support both simple HTML and advanced XML layouts

### Multi-tenant Environments
- Create department-specific or client-specific email layouts
- Manage branding variations for different business units
- Implement branded communications for service portals

## Best Practices

1. **Naming Conventions**: Use descriptive names that indicate the layout's purpose and target audience
2. **HTML Structure**: Include placeholder variables (e.g., {{content}}, {{header}}) for dynamic content injection
3. **Responsive Design**: Design layouts that work across different email clients and devices
4. **Testing**: Test layouts across different email clients before deployment
5. **Version Control**: Use descriptive names and clone existing layouts when making changes
6. **Documentation**: Maintain clear descriptions explaining each layout's intended use

## Example Natural Language Commands

Users can interact with email layouts using natural language prompts:

- "Create a new email layout for our quarterly newsletter"
- "Show me all email layouts that contain 'corporate' in the name"
- "Update the header section of the main email layout"
- "Clone the existing layout and modify it for the marketing team"
- "Delete the old layout that's no longer being used"
- "Get details about the layout used for incident notifications"