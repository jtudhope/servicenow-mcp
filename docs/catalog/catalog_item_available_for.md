# Catalog Item Available For Management in ServiceNow MCP

## Overview

The Catalog Item Available For tools provide comprehensive management of Catalog Item Availability rules in ServiceNow. These rules are stored in the `sc_cat_item_user_criteria_mtom` (available for) and `sc_cat_item_user_criteria_no_mtom` (not available for) tables. In ServiceNow, "Available For" on a Catalog Item controls who can see and request that item in the Service Catalog, enabling precise access control and user targeting for catalog offerings.

## Tools

### add_available_for

Add an available for rule to a catalog item, allowing specific user criteria to access the item.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item_id | string | Yes | Catalog item sys_id |
| user_criteria_id | string | Yes | User criteria sys_id to make the item available for |

#### Example

```python
# Example usage of add_available_for
result = add_available_for({
    "catalog_item_id": "b0c4030ac0a8000001c9dd3394009c96",
    "user_criteria_id": "a1b2c3d4e5f6000001c9dd3394009c97"
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created availability rule data including sys_id |

### remove_available_for

Remove an available for rule from a catalog item, revoking access for specific user criteria.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item_id | string | Yes | Catalog item sys_id |
| user_criteria_id | string | Yes | User criteria sys_id to remove from available for |

#### Example

```python
# Example usage of remove_available_for
result = remove_available_for({
    "catalog_item_id": "b0c4030ac0a8000001c9dd3394009c96",
    "user_criteria_id": "a1b2c3d4e5f6000001c9dd3394009c97"
})
```

### add_not_available_for

Add a not available for rule to a catalog item, explicitly denying access for specific user criteria.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item_id | string | Yes | Catalog item sys_id |
| user_criteria_id | string | Yes | User criteria sys_id to make the item not available for |

#### Example

```python
# Example usage of add_not_available_for
result = add_not_available_for({
    "catalog_item_id": "b0c4030ac0a8000001c9dd3394009c96",
    "user_criteria_id": "a1b2c3d4e5f6000001c9dd3394009c97"
})
```

### remove_not_available_for

Remove a not available for rule from a catalog item, removing explicit denial of access.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item_id | string | Yes | Catalog item sys_id |
| user_criteria_id | string | Yes | User criteria sys_id to remove from not available for |

#### Example

```python
# Example usage of remove_not_available_for
result = remove_not_available_for({
    "catalog_item_id": "b0c4030ac0a8000001c9dd3394009c96",
    "user_criteria_id": "a1b2c3d4e5f6000001c9dd3394009c97"
})
```

### list_available_for

List available for or not available for rules for a catalog item.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item_id | string | Yes | Catalog item sys_id |
| rule_type | string | No | Type of rules to list (available or not_available, default: available) |
| limit | integer | No | Maximum number of rules to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |

#### Example

```python
# Example usage of list_available_for
result = list_available_for({
    "catalog_item_id": "b0c4030ac0a8000001c9dd3394009c96",
    "rule_type": "available",
    "limit": 20,
    "offset": 0
})
```

### bulk_update_available_for

Bulk update available for rules for a catalog item, replacing all existing rules with new ones.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| catalog_item_id | string | Yes | Catalog item sys_id |
| available_for_criteria | array | No | List of user criteria sys_ids to make available for |
| not_available_for_criteria | array | No | List of user criteria sys_ids to make not available for |

#### Example

```python
# Example usage of bulk_update_available_for
result = bulk_update_available_for({
    "catalog_item_id": "b0c4030ac0a8000001c9dd3394009c96",
    "available_for_criteria": ["a1b2c3d4e5f6000001c9dd3394009c97", "b2c3d4e5f6a7000001c9dd3394009c98"],
    "not_available_for_criteria": ["c3d4e5f6a7b8000001c9dd3394009c99"]
})
```

## Common Use Cases

### Department-Based Catalog Access

Restrict catalog items to specific departments:

```python
# Make laptop requests available only to IT and Engineering departments
result = add_available_for({
    "catalog_item_id": "laptop_request_item_id",
    "user_criteria_id": "it_department_criteria_id"
})

result = add_available_for({
    "catalog_item_id": "laptop_request_item_id", 
    "user_criteria_id": "engineering_department_criteria_id"
})
```

### Role-Based Access Control

Control access based on user roles:

```python
# Make management tools available only to managers
result = add_available_for({
    "catalog_item_id": "management_tools_item_id",
    "user_criteria_id": "manager_role_criteria_id"
})

# Explicitly deny access to interns
result = add_not_available_for({
    "catalog_item_id": "management_tools_item_id",
    "user_criteria_id": "intern_role_criteria_id"
})
```

### Location-Based Restrictions

Limit catalog items to specific office locations:

```python
# Make office supplies available only to users in main office
result = add_available_for({
    "catalog_item_id": "office_supplies_item_id",
    "user_criteria_id": "main_office_location_criteria_id"
})

# Not available for remote workers
result = add_not_available_for({
    "catalog_item_id": "office_supplies_item_id",
    "user_criteria_id": "remote_worker_criteria_id"
})
```

### Bulk Configuration Management

Configure multiple availability rules at once:

```python
# Set up comprehensive access rules for a high-security catalog item
result = bulk_update_available_for({
    "catalog_item_id": "security_clearance_item_id",
    "available_for_criteria": [
        "security_team_criteria_id",
        "senior_management_criteria_id",
        "compliance_team_criteria_id"
    ],
    "not_available_for_criteria": [
        "contractor_criteria_id",
        "temporary_employee_criteria_id",
        "intern_criteria_id"
    ]
})
```

## Best Practices

1. **Use clear user criteria naming** that reflects the intended audience or restriction
2. **Test access rules thoroughly** with test users from different groups
3. **Document access restrictions** in catalog item descriptions for transparency
4. **Regular review and cleanup** of availability rules to remove obsolete restrictions
5. **Prefer positive rules** (available_for) over negative rules (not_available_for) when possible
6. **Consider inheritance** - parent category rules may affect child items
7. **Monitor usage patterns** to ensure rules aren't overly restrictive
8. **Use bulk operations** for managing multiple rules efficiently

## Access Rule Precedence

Understanding how ServiceNow evaluates availability rules:

1. **Not Available For rules take precedence** - if a user matches any "not available for" criteria, they cannot access the item regardless of "available for" rules
2. **Available For rules are inclusive** - if any "available for" rule matches, the user can access the item
3. **No rules means available to all** - items without any availability rules are visible to all users
4. **Multiple criteria evaluation** - users must match at least one available criteria and no not-available criteria

## Error Handling

All tools return structured responses with success indicators and error messages:

```python
if result["success"]:
    print(f"Operation successful: {result['message']}")
    # Process result data if available
else:
    print(f"Operation failed: {result['message']}")
    # Handle error appropriately
```

## Integration with Other Tools

Catalog Item Available For rules work closely with:
- **User Criteria Management** - Use `create_user_criteria` to define target audiences
- **Catalog Items** - Use `list_catalog_items` to find items needing access control
- **User Management** - Use `list_users` and `list_groups` to understand user populations
- **Service Portal** - Availability rules apply to both platform UI and Service Portal
- **Catalog Categories** - Category-level rules can complement item-level rules

## Example Natural Language Commands for Claude

- "Make the laptop request catalog item available only to IT department employees"
- "List all availability rules for the software license catalog item"
- "Remove access to the executive parking permit for contractors"
- "Set up the security clearance form to be available only to security team and senior management, but not available to temporary employees"
- "Show me which user criteria can access the mobile phone request item"
- "Bulk update the high-value equipment form to restrict access to managers and team leads only"
- "Remove all availability restrictions from the basic office supplies catalog item"

## User Criteria Reference

Common user criteria types that can be used with availability rules:

- **Department-based** - Target users by department affiliation
- **Role-based** - Target users by assigned roles
- **Location-based** - Target users by office location or site
- **Group membership** - Target users by group membership
- **Manager hierarchy** - Target users by reporting structure
- **Custom attributes** - Target users by custom user attributes
- **VIP status** - Target users by VIP or special designation flags

## Troubleshooting

Common issues and solutions:

1. **Rules not taking effect** - Check if catalog item cache needs clearing
2. **User can't see item unexpectedly** - Verify "not available for" rules aren't blocking access
3. **Too many users have access** - Review and tighten available for criteria
4. **Performance issues** - Optimize user criteria queries for large user populations
5. **Conflicting rules** - Remember that "not available for" always takes precedence