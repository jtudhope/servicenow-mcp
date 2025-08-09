# Employee Center Quick Link Management in ServiceNow MCP

The Employee Center Quick Link Management tools provide comprehensive functionality for managing quick links in the ServiceNow Employee Center Service Portal through the `sn_ex_sp_quick_link` table.

## Available Tools

### create_quick_link

Create a new employee center quick link with customizable content types.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Quick link name |
| content_type | string | Yes | Content type (page, external_link, knowledge, catalog_item) |
| active | boolean | No | Whether the quick link is active (default: true) |
| override_title | string | No | Override title for display |
| override_short_desc | string | No | Override short description |
| page | string | No | Service Portal page sys_id (for page content type) |
| external_link | string | No | External link sys_id (for external_link content type) |
| knowledge | string | No | Knowledge article sys_id (for knowledge content type) |
| catalog_item | string | No | Catalog item sys_id (for catalog_item content type) |
| icon_url | string | No | Icon URL for the quick link |
| background_image_url | string | No | Background image URL |
| additional_query_params | string | No | Additional query parameters for the page |

#### Example

```python
result = create_quick_link({
    "name": "Employee Handbook",
    "content_type": "knowledge",
    "active": true,
    "override_title": "Employee Handbook",
    "override_short_desc": "Access the complete employee handbook",
    "knowledge": "kb123456789",
    "icon_url": "https://example.com/handbook-icon.png"
})
```

### update_quick_link

Update an existing employee center quick link.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| quick_link_id | string | Yes | Quick link sys_id to update |
| name | string | No | Updated quick link name |
| content_type | string | No | Updated content type |
| active | boolean | No | Updated active status |
| override_title | string | No | Updated override title |
| override_short_desc | string | No | Updated override short description |
| page | string | No | Updated Service Portal page sys_id |
| external_link | string | No | Updated external link sys_id |
| knowledge | string | No | Updated knowledge article sys_id |
| catalog_item | string | No | Updated catalog item sys_id |
| icon_url | string | No | Updated icon URL |
| background_image_url | string | No | Updated background image URL |
| additional_query_params | string | No | Updated additional query parameters |

### list_quick_links

List employee center quick links with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| active | boolean | No | Filter by active status |
| content_type | string | No | Filter by content type |
| limit | integer | No | Maximum number of quick links to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query string |

### get_quick_link

Get detailed information about a specific employee center quick link.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| quick_link_id | string | Yes | Quick link sys_id to retrieve |

### delete_quick_link

Delete an employee center quick link.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| quick_link_id | string | Yes | Quick link sys_id to delete |

## Content Types

The quick links support four main content types:

1. **page** - Links to Service Portal pages
2. **external_link** - Links to external URLs
3. **knowledge** - Links to knowledge articles
4. **catalog_item** - Links to service catalog items

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| quick_link | object | Quick link data (for single operations) |
| quick_links | array | List of quick links (for list operations) |
| total_count | integer | Total count for list operations |

## Example Usage Scenarios

### Creating a Knowledge Article Quick Link
```python
create_quick_link({
    "name": "IT Policies",
    "content_type": "knowledge",
    "knowledge": "kb_article_sys_id",
    "override_title": "IT Security Policies",
    "override_short_desc": "View company IT security policies",
    "icon_url": "https://company.com/security-icon.png"
})
```

### Creating a Service Catalog Quick Link
```python
create_quick_link({
    "name": "Request Laptop",
    "content_type": "catalog_item", 
    "catalog_item": "catalog_item_sys_id",
    "override_title": "New Laptop Request",
    "background_image_url": "https://company.com/laptop-bg.jpg"
})
```

### Creating an External Link Quick Link
```python
create_quick_link({
    "name": "Company Portal",
    "content_type": "external_link",
    "external_link": "external_link_sys_id",
    "override_title": "Employee Portal"
})
```
