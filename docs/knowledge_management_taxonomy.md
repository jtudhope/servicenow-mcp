# Taxonomy Management in ServiceNow MCP

## Overview

The Taxonomy tools provide comprehensive management of hierarchical classification structures in ServiceNow. These taxonomies are stored in the `taxonomy` table and serve as controlled vocabularies that other parts of the platform can reference. In ServiceNow, taxonomies enable standardized categorization and organization of content, knowledge articles, and other system data.

## Tools

### create_taxonomy

Create a new taxonomy in the taxonomy table for hierarchical classification structures.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the taxonomy (must be unique) |
| description | string | No | Description of the taxonomy |
| active | boolean | No | Whether the taxonomy is active (default: true) |
| managers | string | No | User criteria sys_id for taxonomy managers |
| sys_domain | string | No | Domain for the taxonomy (default: "global") |
| sys_domain_path | string | No | Domain path for the taxonomy (default: "/") |

#### Example

```python
# Example usage of create_taxonomy
result = create_taxonomy({
    "name": "IT Service Categories",
    "description": "Hierarchical classification for IT services and support categories",
    "active": true,
    "managers": "user_criteria_sys_id_for_it_managers"
})
```

#### Response

The tool returns a TaxonomyResponse with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created taxonomy data including sys_id and all fields |

### update_taxonomy

Update an existing taxonomy in the taxonomy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| taxonomy_id | string | Yes | Taxonomy sys_id |
| name | string | No | Updated name of the taxonomy |
| description | string | No | Updated description |
| active | boolean | No | Updated active status |
| managers | string | No | Updated user criteria sys_id for managers |
| sys_domain | string | No | Updated domain |
| sys_domain_path | string | No | Updated domain path |

#### Example

```python
# Example usage of update_taxonomy
result = update_taxonomy({
    "taxonomy_id": "a1b2c3d4e5f6000001c9dd3394009c96",
    "description": "Updated classification for IT services including cloud and on-premise categories",
    "active": true
})
```

### list_taxonomies

List taxonomies from the taxonomy table with filtering and pagination options.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of taxonomies to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| active | boolean | No | Filter by active status |
| name_contains | string | No | Filter by name containing text |
| sys_domain | string | No | Filter by domain |
| query | string | No | Additional query string |

#### Example

```python
# Example usage of list_taxonomies
result = list_taxonomies({
    "limit": 20,
    "active": true,
    "name_contains": "IT",
    "offset": 0
})
```

#### Response

Returns a dictionary with:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| taxonomies | array | List of taxonomy objects |
| total | integer | Total number of taxonomies returned |
| limit | integer | Limit used for the query |
| offset | integer | Offset used for the query |

### get_taxonomy

Get a specific taxonomy from the taxonomy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| taxonomy_id | string | Yes | Taxonomy sys_id or name |

#### Example

```python
# Example usage of get_taxonomy
result = get_taxonomy({
    "taxonomy_id": "a1b2c3d4e5f6000001c9dd3394009c96"
})
```

### delete_taxonomy

Delete a taxonomy from the taxonomy table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| taxonomy_id | string | Yes | Taxonomy sys_id |

#### Example

```python
# Example usage of delete_taxonomy
result = delete_taxonomy({
    "taxonomy_id": "a1b2c3d4e5f6000001c9dd3394009c96"
})
```

### clone_taxonomy

Clone an existing taxonomy to create a duplicate with a new name.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| taxonomy_id | string | Yes | Source taxonomy sys_id |
| new_name | string | Yes | Name for the cloned taxonomy |
| new_description | string | No | Description for the cloned taxonomy |

#### Example

```python
# Example usage of clone_taxonomy
result = clone_taxonomy({
    "taxonomy_id": "a1b2c3d4e5f6000001c9dd3394009c96",
    "new_name": "IT Service Categories - Development Environment",
    "new_description": "Development version of IT service taxonomy for testing"
})
```

## Common Use Cases

### Knowledge Management Classification

Create taxonomies for organizing knowledge articles:

```python
# Create a knowledge article classification taxonomy
result = create_taxonomy({
    "name": "Knowledge Article Topics",
    "description": "Hierarchical classification for organizing knowledge base articles by topic and department",
    "active": true
})
```

### Service Catalog Organization

Structure service catalog offerings:

```python
# Create a service catalog taxonomy
result = create_taxonomy({
    "name": "Service Catalog Hierarchy",
    "description": "Classification structure for organizing service catalog items by department and service type",
    "active": true,
    "managers": "service_catalog_managers_criteria_id"
})
```

### Asset Classification

Organize IT assets and configuration items:

```python
# Create an asset classification taxonomy
result = create_taxonomy({
    "name": "IT Asset Categories",
    "description": "Hierarchical classification for IT assets including hardware, software, and network components",
    "active": true
})
```

### Incident Categorization

Create structured incident classification:

```python
# Create incident categorization taxonomy
result = create_taxonomy({
    "name": "Incident Classification",
    "description": "Standardized hierarchy for categorizing incidents by impact area and service affected",
    "active": true,
    "managers": "incident_managers_criteria_id"
})
```

### Document Management

Organize documents and attachments:

```python
# Create document classification taxonomy
result = create_taxonomy({
    "name": "Document Categories",
    "description": "Classification structure for organizing corporate documents and policies",
    "active": true
})
```

## Best Practices

1. **Use descriptive names** that clearly indicate the taxonomy's purpose and scope
2. **Plan hierarchy levels** before creating to ensure logical organization
3. **Set appropriate managers** using user criteria for proper access control
4. **Document taxonomy structure** in the description field for future reference
5. **Regular maintenance** - review and update taxonomies as business needs evolve
6. **Domain management** - use appropriate domains for multi-tenant environments
7. **Version control** - use cloning for creating test versions of production taxonomies
8. **Consistent naming conventions** across related taxonomies
9. **Active status management** - deactivate obsolete taxonomies rather than deleting

## Taxonomy Hierarchy Best Practices

When designing taxonomy hierarchies:

1. **Start broad, get specific** - Top levels should be general categories, with specificity increasing at lower levels
2. **Limit depth** - Generally 3-5 levels maximum for usability
3. **Avoid overlap** - Categories should be mutually exclusive where possible
4. **Future-proof** - Design with expansion in mind
5. **User-friendly terms** - Use terminology familiar to end users
6. **Balanced breadth** - Avoid categories with too many or too few subcategories

## Integration with Other ServiceNow Features

Taxonomies integrate with various ServiceNow modules:

- **Knowledge Management** - Categorize articles and content
- **Service Catalog** - Organize catalog items and categories
- **ITSM** - Classify incidents, problems, and changes
- **Asset Management** - Categorize CIs and assets
- **Portal and Navigation** - Structure menu systems
- **Reporting** - Enable consistent categorization for analytics
- **Search** - Improve content discoverability

## Domain-Based Access Control

Manage taxonomy access across domains:

```python
# Create domain-specific taxonomy
result = create_taxonomy({
    "name": "Finance Department Processes",
    "description": "Classification for finance-specific processes and procedures",
    "sys_domain": "finance_domain_id",
    "sys_domain_path": "/finance/",
    "managers": "finance_managers_criteria_id"
})
```

## Example Natural Language Commands for Claude

- "Create a taxonomy for IT service categories with proper management access"
- "List all active taxonomies in the system with their descriptions"
- "Update the knowledge article taxonomy to include new AI and automation categories"
- "Clone the production incident classification taxonomy for testing environment"
- "Show me details of the asset management taxonomy"
- "Deactivate the old service catalog hierarchy taxonomy"
- "Create a document classification system for HR policies and procedures"

## Error Handling

All taxonomy tools return structured responses with success indicators:

```python
if result["success"]:
    print(f"Operation successful: {result['message']}")
    # Process result data
    taxonomy_data = result.get("data", {})
    print(f"Taxonomy ID: {taxonomy_data.get('sys_id')}")
else:
    print(f"Operation failed: {result['message']}")
    # Handle error appropriately
```

## Troubleshooting

Common issues and solutions:

1. **Duplicate name errors** - Taxonomy names must be unique across the system
2. **Permission issues** - Ensure proper domain access and manager permissions
3. **Reference errors** - Check if taxonomy is referenced by other records before deletion
4. **Domain restrictions** - Verify domain access when working with domain-scoped taxonomies
5. **Manager criteria** - Ensure user criteria references are valid and active

## Advanced Usage

### Bulk Taxonomy Management

```python
# Create multiple related taxonomies
taxonomies = [
    {
        "name": "Hardware Assets",
        "description": "Classification for physical IT assets"
    },
    {
        "name": "Software Assets", 
        "description": "Classification for software and licenses"
    },
    {
        "name": "Network Assets",
        "description": "Classification for network infrastructure"
    }
]

for taxonomy_def in taxonomies:
    result = create_taxonomy(taxonomy_def)
    if result["success"]:
        print(f"Created taxonomy: {taxonomy_def['name']}")
    else:
        print(f"Failed to create {taxonomy_def['name']}: {result['message']}")
```

### Taxonomy Versioning Strategy

```python
# Create versioned taxonomy for major updates
result = clone_taxonomy({
    "taxonomy_id": "production_taxonomy_id",
    "new_name": "Service Categories v2.0",
    "new_description": "Updated service taxonomy with cloud services and automation categories"
})
```

The taxonomy tools provide a robust foundation for creating and managing hierarchical classification structures that enhance organization, searchability, and consistency across ServiceNow implementations.