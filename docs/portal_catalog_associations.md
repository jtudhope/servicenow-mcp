# Portal Catalog Associations in ServiceNow MCP

## Overview

The Portal Catalog Association tools allow you to manage associations between ServiceNow portals and service catalogs through the `m2m_sp_portal_catalog` table. These associations control which service catalogs are available on specific portals, enabling fine-grained control over catalog visibility and access.

## Available Tools

### 1. create_portal_catalog_association

Creates a new association between a portal and a catalog.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| portal_id | string | Yes | The sys_id of the portal |
| catalog_id | string | Yes | The sys_id of the catalog |

#### Example

```python
# Create a portal catalog association
result = create_portal_catalog_association({
    "portal_id": "12345678-1234-5678-9012-123456789012",
    "catalog_id": "87654321-4321-8765-2109-876543210987"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| association_id | string | System ID of the created association |
| association_data | object | Details of the created association |

### 2. list_portal_catalog_associations

Lists portal catalog associations with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| portal_id | string | No | Filter by portal sys_id |
| catalog_id | string | No | Filter by catalog sys_id |
| limit | integer | No | Maximum number of associations to return |
| offset | integer | No | Offset for pagination |

#### Example

```python
# List all associations for a specific portal
result = list_portal_catalog_associations({
    "portal_id": "12345678-1234-5678-9012-123456789012",
    "limit": 50
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| associations | array | List of portal catalog associations |
| total_count | integer | Total number of associations returned |

### 3. get_portal_catalog_association

Retrieves detailed information about a specific portal catalog association.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| association_id | string | Yes | The sys_id of the association to retrieve |

#### Example

```python
# Get details of a specific association
result = get_portal_catalog_association({
    "association_id": "11111111-2222-3333-4444-555555555555"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| association_data | object | Association details |

### 4. delete_portal_catalog_association

Deletes a portal catalog association.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| association_id | string | Yes | The sys_id of the association to delete |

#### Example

```python
# Delete a portal catalog association
result = delete_portal_catalog_association({
    "association_id": "11111111-2222-3333-4444-555555555555"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |

### 5. bulk_create_portal_catalog_associations

Creates multiple portal catalog associations for a single portal in bulk.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| portal_id | string | Yes | The sys_id of the portal |
| catalog_ids | array | Yes | List of catalog sys_ids to associate with the portal |

#### Example

```python
# Associate multiple catalogs with a portal
result = bulk_create_portal_catalog_associations({
    "portal_id": "12345678-1234-5678-9012-123456789012",
    "catalog_ids": [
        "87654321-4321-8765-2109-876543210987",
        "11111111-2222-3333-4444-555555555555",
        "99999999-8888-7777-6666-555555555555"
    ]
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether all operations were successful |
| message | string | A message describing the result |
| created_associations | array | List of successfully created associations |
| failed_associations | array | List of failed associations with error details |

## Common Use Cases

### Setting Up Portal Catalog Access

1. **Create Initial Associations**: Use `create_portal_catalog_association` to establish basic catalog access for a portal
2. **Bulk Setup**: Use `bulk_create_portal_catalog_associations` to quickly associate multiple catalogs with a new portal
3. **Audit Existing Setup**: Use `list_portal_catalog_associations` to review current portal-catalog relationships

### Managing Portal Content

1. **Portal Migration**: List existing associations, then recreate them for a new portal
2. **Catalog Reorganization**: Remove old associations and create new ones as catalogs are restructured
3. **Access Control**: Add or remove catalog associations based on changing business requirements

### Troubleshooting

- **Portal shows no catalogs**: Use `list_portal_catalog_associations` to verify associations exist for the portal
- **Unexpected catalog visibility**: Check for duplicate or conflicting associations
- **Performance issues**: Review the number of catalogs associated with heavily-used portals

## Natural Language Examples

Users can interact with these tools using natural language prompts like:

- "Show me all catalogs associated with the Employee portal"
- "Associate the IT Services catalog with the Manager portal"
- "Remove the HR catalog from the Employee portal"
- "Create associations between the Customer portal and all public catalogs"
- "What catalogs are available on portal XYZ?"
- "Bulk associate catalogs A, B, and C with the new portal"

## Error Handling

All tools include comprehensive error handling for common scenarios:

- **Invalid portal_id or catalog_id**: Returns detailed error messages
- **Duplicate associations**: Handled gracefully with appropriate messaging
- **Permission issues**: Authentication and authorization errors are clearly reported
- **Network timeouts**: Connection issues are caught and reported

## Best Practices

1. **Verify IDs**: Always verify portal and catalog sys_ids before creating associations
2. **Use Bulk Operations**: For multiple associations, use `bulk_create_portal_catalog_associations` for better performance
3. **Regular Audits**: Periodically review associations to ensure they align with business requirements
4. **Test Changes**: Use `list_portal_catalog_associations` to verify changes before and after modifications
5. **Error Monitoring**: Check the success field in all responses and handle failures appropriately