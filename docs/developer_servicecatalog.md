# Service Catalog Management in ServiceNow MCP

## Overview

The Service Catalog Management tools provide functionality to manage service catalogs stored in the `sc_catalog` table in ServiceNow. These tools allow developers to create, update, list, retrieve, and delete service catalogs that organize catalog items and provide structure for the ServiceNow Service Portal and employee experience.

## Service Catalog Management Tools

### create_service_catalog

Create a new service catalog in the sc_catalog table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Title of the service catalog |
| description | string | No | Description of the service catalog |
| active | boolean | No | Whether the catalog is active (default: true) |
| desktop | boolean | No | Whether the catalog is available on desktop (default: true) |
| mobile | boolean | No | Whether the catalog is available on mobile (default: true) |
| enable_wish_list | boolean | No | Whether to enable wish list functionality (default: false) |
| enable_request_cart | boolean | No | Whether to enable request cart functionality (default: true) |
| manager | string | No | Manager sys_id for the catalog |
| editors | string | No | Editors sys_id (comma-separated) |

#### Example

```python
result = create_service_catalog({
    "title": "IT Services Catalog",
    "description": "Catalog containing all IT-related services and requests",
    "active": true,
    "desktop": true,
    "mobile": true,
    "enable_wish_list": true,
    "enable_request_cart": true,
    "manager": "a1b2c3d4e5f6g7h8i9j0",
    "editors": "x1y2z3a4b5c6d7e8f9g0,m1n2o3p4q5r6s7t8u9v0"
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created service catalog details including sys_id, title, settings, etc. |

### update_service_catalog

Update an existing service catalog in the sc_catalog table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_id | string | Yes | Service catalog sys_id |
| title | string | No | Title of the service catalog |
| description | string | No | Description of the service catalog |
| active | boolean | No | Whether the catalog is active |
| desktop | boolean | No | Whether the catalog is available on desktop |
| mobile | boolean | No | Whether the catalog is available on mobile |
| enable_wish_list | boolean | No | Whether to enable wish list functionality |
| enable_request_cart | boolean | No | Whether to enable request cart functionality |
| manager | string | No | Manager sys_id for the catalog |
| editors | string | No | Editors sys_id (comma-separated) |

#### Example

```python
result = update_service_catalog({
    "catalog_id": "12345678901234567890123456789012",
    "title": "Updated IT Services Catalog",
    "description": "Updated description for IT services",
    "enable_wish_list": false
})
```

### list_service_catalogs

List service catalogs from the sc_catalog table with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of catalogs to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| active | boolean | No | Filter by active status |
| desktop | boolean | No | Filter by desktop availability |
| mobile | boolean | No | Filter by mobile availability |
| manager | string | No | Filter by manager sys_id |
| query | string | No | Search query for catalog title or description |

#### Example

```python
result = list_service_catalogs({
    "limit": 20,
    "active": true,
    "desktop": true,
    "query": "IT"
})
```

### get_service_catalog

Get a specific service catalog from the sc_catalog table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_id | string | Yes | Service catalog sys_id |

#### Example

```python
result = get_service_catalog({
    "catalog_id": "12345678901234567890123456789012"
})
```

### delete_service_catalog

Delete a service catalog from the sc_catalog table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_id | string | Yes | Service catalog sys_id |

#### Example

```python
result = delete_service_catalog({
    "catalog_id": "12345678901234567890123456789012"
})
```

## Use Cases

### Organizing Service Offerings
Create and manage different catalogs to organize service offerings by department, category, or business unit (e.g., IT Services, HR Services, Facilities).

### Multi-Channel Access
Configure catalogs for different access channels, enabling or disabling desktop and mobile access based on user needs and service requirements.

### Wish List and Cart Features
Enable wish list functionality for users to save items for later consideration, and configure request cart capabilities for bulk ordering.

### Access Control and Management
Assign managers and editors to catalogs to control who can modify catalog content and oversee service offerings.

### Service Portal Integration
Create catalogs that integrate seamlessly with ServiceNow Service Portal for enhanced user experience.

## Best Practices

### Catalog Organization
- Create logical groupings based on business units or service types
- Use clear, descriptive titles and comprehensive descriptions
- Maintain consistent naming conventions across catalogs

### Access Management
- Assign appropriate managers with oversight responsibilities
- Grant editor access to subject matter experts for relevant services
- Regularly review and update access permissions

### User Experience
- Enable mobile access for catalogs with services suitable for mobile users
- Consider enabling wish lists for complex or expensive services
- Configure request carts appropriately based on ordering workflows

### Lifecycle Management
- Regularly review catalog usage and effectiveness
- Archive or deactivate unused catalogs
- Monitor performance and user feedback

## Security Considerations

### Access Controls
- Implement appropriate role-based access controls for catalog management
- Ensure managers and editors have legitimate business needs for access
- Regular audit of catalog permissions and assignments

### Data Validation
- Validate all input data for proper formatting and content
- Implement proper error handling for API interactions
- Monitor for unauthorized catalog modifications

## Error Handling

All service catalog management tools return a consistent response structure with success/failure indicators and descriptive error messages. Common error scenarios include:

- Invalid catalog ID or non-existent catalogs
- Insufficient permissions for catalog operations
- Data validation failures (invalid sys_ids, etc.)
- Network or API connectivity issues
- Constraint violations (e.g., deleting catalogs with dependencies)

## Integration Points

### Service Portal
Service catalogs integrate directly with ServiceNow Service Portal, affecting navigation, categorization, and user experience.

### Catalog Items
Catalogs serve as containers for catalog items and categories, affecting how services are organized and presented.

### User Interface
Catalogs determine what appears in various ServiceNow interfaces including native UI and Service Portal.

### Reporting and Analytics
Catalog configuration affects reporting capabilities and analytics around service usage and user behavior.

## Example Natural Language Commands for Claude

Users can interact with the service catalog management tools using natural language prompts:

- "Create a new service catalog for HR services"
- "List all active service catalogs"
- "Update the IT catalog to enable wish list functionality"
- "Get details for the catalog with ID 12345"
- "Delete the unused training catalog"
- "Show me all catalogs available on mobile"
- "Find catalogs managed by John Smith"
- "Create a catalog for facilities management services"