# Choice Management in ServiceNow MCP

## Overview

The Choice Management tools provide comprehensive functionality for managing choices in ServiceNow choice fields. These tools allow you to create, update, list, retrieve, delete, and bulk manage choice options for dropdown fields, enabling dynamic configuration of choice lists.

## Available Tools

### create_choice

Creates a new choice option for a choice field in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | Yes | Table name containing the choice field |
| element | string | Yes | Field/element name for the choice |
| label | string | Yes | Display label for the choice option |
| value | string | Yes | Stored value for the choice option |
| sequence | integer | No | Display order sequence (lower numbers appear first) |
| inactive | boolean | No | Whether the choice is inactive/disabled (default: false) |
| hint | string | No | Tooltip hint text for the choice |
| dependent_value | string | No | Parent choice value for dependent choices |
| language | string | No | Language code for the choice (default: en) |

#### Example

```python
result = create_choice({
    "table": "incident",
    "element": "priority",
    "label": "Critical",
    "value": "1",
    "sequence": 10,
    "inactive": false,
    "hint": "Critical priority - immediate attention required",
    "language": "en"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| choice_id | string | sys_id of the created choice |
| value | string | Value of the created choice |
| data | object | Complete choice data from ServiceNow |

### update_choice

Updates an existing choice option in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| choice_id | string | Yes | Choice sys_id to update |
| label | string | No | Updated display label |
| value | string | No | Updated stored value |
| sequence | integer | No | Updated display order sequence |
| inactive | boolean | No | Updated inactive status |
| hint | string | No | Updated tooltip hint text |
| dependent_value | string | No | Updated parent choice value |

#### Example

```python
result = update_choice({
    "choice_id": "choice_sys_id_here",
    "label": "Ultra Critical",
    "sequence": 5,
    "hint": "Ultra critical priority - escalate immediately"
})
```

### list_choices

Lists all choice options for a specific field from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | Yes | Table name containing the choice field |
| element | string | Yes | Field/element name for the choices |
| active_only | boolean | No | Whether to only return active choices (default: true) |
| include_dependent | boolean | No | Whether to include dependent choices (default: true) |
| language | string | No | Language code to filter choices (default: en) |
| limit | integer | No | Maximum number of choices to return (default: 50) |
| offset | integer | No | Offset for pagination (default: 0) |

#### Example

```python
result = list_choices({
    "table": "incident",
    "element": "priority",
    "active_only": true,
    "language": "en",
    "limit": 100
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| choices | array | List of choice objects ordered by sequence |
| total_count | integer | Total number of choices returned |

### get_choice

Retrieves a specific choice option by its sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| choice_id | string | Yes | Choice sys_id to retrieve |

#### Example

```python
result = get_choice({
    "choice_id": "choice_sys_id_here"
})
```

### delete_choice

Deletes a choice option from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| choice_id | string | Yes | Choice sys_id to delete |

#### Example

```python
result = delete_choice({
    "choice_id": "choice_sys_id_here"
})
```

### bulk_create_choices

Creates multiple choice options at once for a choice field.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | Yes | Table name containing the choice field |
| element | string | Yes | Field/element name for the choices |
| choices | array | Yes | List of choice definitions |
| language | string | No | Language code for the choices (default: en) |

#### Choice Definition Format

Each choice in the `choices` array should contain:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| label | string | Yes | Display label for the choice |
| value | string | Yes | Stored value for the choice |
| sequence | integer | No | Display order sequence |
| inactive | boolean | No | Whether the choice is inactive |
| hint | string | No | Tooltip hint text |
| dependent_value | string | No | Parent choice value |

#### Example

```python
result = bulk_create_choices({
    "table": "incident",
    "element": "severity",
    "choices": [
        {
            "label": "Severity 1 - Critical",
            "value": "1",
            "sequence": 10,
            "hint": "System down or major functionality unavailable"
        },
        {
            "label": "Severity 2 - High",
            "value": "2", 
            "sequence": 20,
            "hint": "Significant impact on business operations"
        },
        {
            "label": "Severity 3 - Medium",
            "value": "3",
            "sequence": 30,
            "hint": "Minor impact on business operations"
        },
        {
            "label": "Severity 4 - Low",
            "value": "4",
            "sequence": 40,
            "hint": "Minimal or no impact on business operations"
        }
    ],
    "language": "en"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether all operations were successful |
| message | string | Summary message of the bulk operation |
| created_count | integer | Number of choices created successfully |
| failed_count | integer | Number of choices that failed to create |
| details | array | Detailed results for each choice |

### reorder_choices

Reorders choice options by updating their sequence values.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | Yes | Table name containing the choice field |
| element | string | Yes | Field/element name for the choices |
| choice_order | array | Yes | List of choice values in desired order |

#### Example

```python
result = reorder_choices({
    "table": "incident",
    "element": "priority",
    "choice_order": ["1", "2", "3", "4", "5"]  # Critical to Low
})
```

## Common Use Cases

### Basic Choice Management
1. **Priority Levels**: Create priority choices for incidents, requests, etc.
2. **Status Values**: Define workflow status options
3. **Category Options**: Set up categorization choices
4. **Approval States**: Configure approval workflow options

### Advanced Scenarios
1. **Dependent Choices**: Create hierarchical choice relationships
2. **Localization**: Manage choices in multiple languages
3. **Dynamic Updates**: Bulk update choice sets based on business changes
4. **Choice Reordering**: Adjust display order for better user experience

## Dependent Choices

ServiceNow supports dependent choices where the available options in one field depend on the selection in another field.

### Example: State/City Dependency

```python
# Create parent choices (states)
create_choice({
    "table": "u_location",
    "element": "state",
    "label": "California",
    "value": "CA"
})

# Create dependent choices (cities)
create_choice({
    "table": "u_location", 
    "element": "city",
    "label": "San Francisco",
    "value": "SF",
    "dependent_value": "CA"  # Only show when CA is selected
})
```

## Choice Sequencing

The `sequence` field controls the display order of choices:
- Lower numbers appear first
- Use increments of 10 (10, 20, 30...) for flexibility
- Allows inserting new choices between existing ones

## Language Support

ServiceNow supports multilingual choice labels:
- Each choice can have translations for different languages
- Use the `language` parameter to specify locale (e.g., "en", "fr", "de")
- Same value can have different labels per language

## Best Practices

### Choice Design
1. **Consistent Values**: Use consistent value formats across similar fields
2. **Meaningful Labels**: Use clear, descriptive labels for user clarity
3. **Logical Ordering**: Order choices logically (by priority, alphabetically, etc.)
4. **Value Stability**: Avoid changing values once in use - only update labels
5. **Hint Usage**: Provide helpful hints for complex or ambiguous choices

### Performance Considerations
1. **Bulk Operations**: Use `bulk_create_choices` for multiple choices
2. **Pagination**: Use appropriate limits when listing large choice sets
3. **Active Filtering**: Filter inactive choices when not needed
4. **Caching**: ServiceNow caches choices for performance

### Data Integrity
1. **Value Uniqueness**: Ensure choice values are unique within a field
2. **Reference Validation**: Verify dependent_value references exist
3. **Sequence Gaps**: Leave gaps in sequence numbers for future insertions
4. **Backup**: Document choice configurations before bulk changes

## Error Handling

All tools return a standardized response format with a `success` field. When `success` is `false`, the `message` field contains details about the error.

Common error scenarios:
- Invalid table or element names
- Duplicate choice values
- Missing required parameters
- Invalid dependent_value references
- Permission denied
- API rate limits

## Security Considerations

1. **Access Controls**: Ensure appropriate permissions for choice modification
2. **Change Management**: Track choice modifications for audit purposes
3. **Impact Assessment**: Consider downstream effects of choice changes
4. **User Training**: Communicate choice changes to end users
5. **Rollback Plans**: Have procedures for reverting problematic changes

## Integration Examples

### Workflow Integration
Choices often integrate with business rules, workflows, and UI policies:

```python
# Create status choices for approval workflow
bulk_create_choices({
    "table": "u_approval_request",
    "element": "approval_status",
    "choices": [
        {"label": "Draft", "value": "draft", "sequence": 10},
        {"label": "Submitted", "value": "submitted", "sequence": 20},
        {"label": "Under Review", "value": "review", "sequence": 30},
        {"label": "Approved", "value": "approved", "sequence": 40},
        {"label": "Rejected", "value": "rejected", "sequence": 50}
    ]
})
```

### Dynamic Choice Updates
Update choices based on configuration changes:

```python
# Reorder priorities based on new business requirements
reorder_choices({
    "table": "incident",
    "element": "priority", 
    "choice_order": ["critical", "high", "medium", "low", "planning"]
})
```