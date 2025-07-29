# Table Management in ServiceNow MCP

## Overview

The Table Management tools provide comprehensive functionality for creating and managing custom tables and table columns in ServiceNow. These tools allow you to define database schema, create custom data structures, and manage table configurations programmatically.

## Available Tools

### create_table

Creates a new custom table in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Internal name of the table (e.g., u_custom_table) |
| label | string | Yes | Display label for the table |
| is_extendable | boolean | No | Whether the table can be extended (default: true) |
| access | string | No | Access level for the table (public, protected, package_private) (default: public) |
| scope | string | No | Application scope for the table |
| super_class | string | No | Parent table to extend from (leave empty for base table) |
| user_role | string | No | Role required to access this table |
| create_access_controls | boolean | No | Whether to create default access controls (default: true) |
| create_module | boolean | No | Whether to create application menu module (default: true) |
| number_ref | boolean | No | Whether to add a number reference field (default: false) |
| audit | boolean | No | Whether to enable auditing for the table (default: true) |

#### Example

```python
result = create_table({
    "name": "u_asset_tracking",
    "label": "Asset Tracking",
    "is_extendable": true,
    "access": "public",
    "super_class": "",
    "audit": true,
    "create_access_controls": true,
    "create_module": true
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| table_name | string | Name of the created table |
| sys_id | string | System ID of the created table |
| data | object | Complete table data from ServiceNow |

### create_table_column

Creates a new column in an existing table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table to add the column to |
| column_name | string | Yes | Internal name of the column |
| column_label | string | Yes | Display label for the column |
| type | string | Yes | Data type of the column (string, integer, boolean, reference, etc.) |
| max_length | integer | No | Maximum length for string fields |
| mandatory | boolean | No | Whether the field is required (default: false) |
| read_only | boolean | No | Whether the field is read-only (default: false) |
| reference_table | string | No | Referenced table for reference fields |
| reference_qualifier | string | No | Reference qualifier for reference fields |
| choice_list | array | No | List of choices for choice fields |
| default_value | string | No | Default value for the field |
| help_text | string | No | Help text for the field |

#### Example

```python
result = create_table_column({
    "table_name": "u_asset_tracking",
    "column_name": "u_asset_type",
    "column_label": "Asset Type",
    "type": "choice",
    "mandatory": true,
    "choice_list": ["Laptop", "Desktop", "Monitor", "Phone"],
    "help_text": "Select the type of asset being tracked"
})
```

### update_table

Updates an existing table's properties.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table to update |
| label | string | No | Updated display label |
| is_extendable | boolean | No | Updated extendable setting |
| access | string | No | Updated access level |
| user_role | string | No | Updated role requirement |
| audit | boolean | No | Updated audit setting |

#### Example

```python
result = update_table({
    "table_name": "u_asset_tracking",
    "label": "Enterprise Asset Tracking",
    "access": "protected",
    "audit": true
})
```

### update_table_column

Updates an existing table column's properties.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table containing the column |
| column_name | string | Yes | Name of the column to update |
| column_label | string | No | Updated display label |
| max_length | integer | No | Updated maximum length |
| mandatory | boolean | No | Updated mandatory setting |
| read_only | boolean | No | Updated read-only setting |
| reference_qualifier | string | No | Updated reference qualifier |
| default_value | string | No | Updated default value |
| help_text | string | No | Updated help text |

#### Example

```python
result = update_table_column({
    "table_name": "u_asset_tracking",
    "column_name": "u_asset_type",
    "column_label": "Asset Category",
    "mandatory": false,
    "help_text": "Select the category of asset being tracked"
})
```

### list_tables

Lists tables from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | No | Search query for tables (searches name and label) |
| scope | string | No | Filter by application scope |
| super_class | string | No | Filter by parent table |
| user_table | boolean | No | Filter to user-created tables only (default: true) |
| limit | integer | No | Maximum number of tables to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |

#### Example

```python
result = list_tables({
    "query": "asset",
    "user_table": true,
    "limit": 20
})
```

### list_table_columns

Lists columns from a specific table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table to list columns for |
| active | boolean | No | Filter to active columns only (default: true) |
| limit | integer | No | Maximum number of columns to return (default: 50) |
| offset | integer | No | Offset for pagination (default: 0) |

#### Example

```python
result = list_table_columns({
    "table_name": "u_asset_tracking",
    "active": true,
    "limit": 100
})
```

### get_table

Retrieves details of a specific table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table to retrieve |

#### Example

```python
result = get_table({
    "table_name": "u_asset_tracking"
})
```

### get_table_column

Retrieves details of a specific table column.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table |
| column_name | string | Yes | Name of the column |

#### Example

```python
result = get_table_column({
    "table_name": "u_asset_tracking",
    "column_name": "u_asset_type"
})
```

## Supported Data Types

### Basic Types
- **string**: Text fields with configurable max length
- **integer**: Numeric integer fields
- **boolean**: True/false fields
- **decimal**: Decimal number fields
- **date**: Date-only fields
- **date_time**: Date and time fields

### Advanced Types
- **reference**: Links to records in other tables
- **choice**: Dropdown with predefined options
- **email**: Email address validation
- **url**: URL validation
- **phone_number**: Phone number formatting
- **currency**: Monetary values
- **duration**: Time duration fields
- **password**: Encrypted password fields

### Large Content Types
- **html**: Rich text HTML content
- **xml**: XML formatted content
- **json**: JSON structured data
- **script**: JavaScript code fields

## Table Naming Conventions

### Custom Tables
- Must start with `u_` prefix (e.g., `u_asset_tracking`)
- Use lowercase letters and underscores
- Be descriptive but concise
- Avoid ServiceNow reserved words

### Column Naming
- Custom columns should start with `u_` prefix
- Use lowercase letters and underscores
- Be descriptive of the data stored
- Follow consistent naming patterns

## Access Control Levels

### Public
- **Description**: Accessible to all users with table access
- **Use Case**: General business data tables

### Protected
- **Description**: Restricted access with role requirements
- **Use Case**: Sensitive business data

### Package Private
- **Description**: Only accessible within the same application scope
- **Use Case**: Application-specific internal tables

## Best Practices

### Table Design
1. **Naming**: Use clear, descriptive names with proper prefixes
2. **Inheritance**: Extend existing tables when appropriate (e.g., task table)
3. **Indexing**: Consider performance implications of table size
4. **Access Controls**: Set appropriate security from creation
5. **Documentation**: Use descriptive labels and help text

### Column Design
1. **Data Types**: Choose appropriate types for data validation
2. **Constraints**: Set mandatory fields thoughtfully
3. **References**: Use reference fields for data integrity
4. **Defaults**: Provide sensible default values
5. **Help Text**: Include user guidance for complex fields

### Performance Considerations
1. **Indexing**: ServiceNow automatically indexes reference and choice fields
2. **String Length**: Set appropriate max lengths for performance
3. **Reference Qualifiers**: Use to limit reference field options
4. **Table Hierarchy**: Consider impact of table extension on queries

## Common Use Cases

1. **Custom Business Objects**: Create tables for organization-specific data
2. **Asset Management**: Track custom asset types and properties
3. **Configuration Items**: Extend CMDB with custom CI types
4. **Business Processes**: Support custom workflows with data tables
5. **Integration Data**: Store data from external systems

## Error Handling

All tools return a standardized response format with a `success` field. When `success` is `false`, the `message` field contains details about the error.

Common error scenarios:
- Invalid table/column names
- Duplicate table/column names
- Invalid data types
- Missing required parameters
- Permission denied
- API rate limits

## Security Considerations

1. **Access Controls**: Always configure appropriate ACLs
2. **Data Sensitivity**: Consider data classification requirements
3. **Audit Trail**: Enable auditing for sensitive tables
4. **Role Requirements**: Set appropriate role restrictions
5. **Field Encryption**: Use encrypted fields for sensitive data