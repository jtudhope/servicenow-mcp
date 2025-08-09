# Application Module Menu Tools in ServiceNow MCP

The Application Module Menu tools provide comprehensive management capabilities for ServiceNow application module menu items. These modules are typically children of application menu items and appear in the All menu navigation structure.

## Available Tools

### create_app_module

Creates a new application module menu item under an existing application menu.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Display title of the module |
| application | string | Yes | Application menu sys_id or name this module belongs to |
| name | string | No | Table name for list modules |
| link_type | string | No | Link type (LIST, FORM, HOMEPAGE, etc.) - defaults to "LIST" |
| order | integer | No | Order for display sequence |
| roles | string | No | Comma-separated list of required roles |
| active | boolean | No | Whether the module is active - defaults to true |
| filter | string | No | Filter conditions for list modules |
| query | string | No | Additional query arguments |
| hint | string | No | Tooltip hint for the module |
| window_name | string | No | Window name for opening links |
| view_name | string | No | View name for list/form modules |
| mobile_title | string | No | Title for mobile display |
| mobile_view_name | string | No | Mobile view name - defaults to "Mobile" |
| device_type | string | No | Device type (browser, mobile, etc.) |
| uncancelable | boolean | No | Whether module is uncancelable |
| override_menu_roles | boolean | No | Override application menu roles |

#### Example

```python
# Create a new list module for incidents
result = create_app_module({
    "title": "All Incidents",
    "application": "incident_management_app_sys_id",
    "name": "incident",
    "link_type": "LIST",
    "roles": "itil,admin",
    "filter": "active=true",
    "order": 100,
    "hint": "View all active incidents"
})
```

### update_app_module

Updates an existing application module menu item.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| module_id | string | Yes | Module sys_id to update |
| title | string | No | Updated display title |
| application | string | No | Updated application menu sys_id |
| name | string | No | Updated table name |
| link_type | string | No | Updated link type |
| order | integer | No | Updated order |
| roles | string | No | Updated roles |
| active | boolean | No | Updated active status |
| filter | string | No | Updated filter conditions |
| query | string | No | Updated query arguments |
| hint | string | No | Updated hint |
| window_name | string | No | Updated window name |
| view_name | string | No | Updated view name |
| mobile_title | string | No | Updated mobile title |
| mobile_view_name | string | No | Updated mobile view name |
| device_type | string | No | Updated device type |
| uncancelable | boolean | No | Updated uncancelable status |
| override_menu_roles | boolean | No | Updated override menu roles |

#### Example

```python
# Update module title and add roles
result = update_app_module({
    "module_id": "existing_module_sys_id",
    "title": "Critical Incidents Only",
    "filter": "active=true^priority=1",
    "roles": "incident_manager,admin"
})
```

### list_app_modules

Lists application modules with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| application | string | No | Filter by application menu sys_id |
| active | boolean | No | Filter by active status |
| name | string | No | Filter by table name |
| link_type | string | No | Filter by link type |
| roles | string | No | Filter by required roles |
| limit | integer | No | Maximum number of modules to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query string |

#### Example

```python
# List all active modules for a specific application
result = list_app_modules({
    "application": "incident_management_app_sys_id",
    "active": True,
    "limit": 20
})
```

### get_app_module

Retrieves details of a specific application module by its sys_id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| module_id | string | Yes | Module sys_id to retrieve |

#### Example

```python
# Get specific module details
result = get_app_module("module_sys_id_here")
```

### delete_app_module

Deletes an application module menu item.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| module_id | string | Yes | Module sys_id to delete |

#### Example

```python
# Delete a module
result = delete_app_module("module_sys_id_here")
```

## Response Format

All tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | Message describing the result |
| module | object | Module data for single operations (optional) |
| modules | array | List of modules for list operations (optional) |
| sys_id | string | System ID of created/updated module (optional) |

## Common Link Types

| Link Type | Description |
|-----------|-------------|
| LIST | Opens a list view of records |
| FORM | Opens a form view |
| HOMEPAGE | Links to a homepage/dashboard |
| NEW | Opens a new record form |
| REPORT | Links to a report |
| URL | External URL link |
| ASSESSMENT | Links to an assessment |
| TIMELINE | Links to a timeline page |

## Usage Examples

### Creating a Complete Menu Structure

```python
# First, create modules for an incident management application
incidents_list = create_app_module({
    "title": "All Incidents",
    "application": "incident_app_sys_id",
    "name": "incident",
    "link_type": "LIST",
    "order": 100,
    "roles": "itil"
})

new_incident = create_app_module({
    "title": "Create New Incident", 
    "application": "incident_app_sys_id",
    "name": "incident",
    "link_type": "NEW",
    "order": 200,
    "roles": "itil"
})

incident_reports = create_app_module({
    "title": "Incident Reports",
    "application": "incident_app_sys_id", 
    "name": "incident",
    "link_type": "REPORT",
    "order": 300,
    "roles": "itil,report_user"
})
```

### Managing Module Visibility with Roles

```python
# Create admin-only module
admin_module = create_app_module({
    "title": "System Configuration",
    "application": "system_app_sys_id",
    "name": "sys_properties",
    "link_type": "LIST", 
    "roles": "admin",
    "hint": "Configure system properties"
})

# Create module that overrides parent menu roles
public_module = create_app_module({
    "title": "Service Catalog",
    "application": "admin_app_sys_id",
    "name": "sc_cat_item",
    "link_type": "LIST",
    "override_menu_roles": True,
    "roles": ""  # No roles required
})
```

## Best Practices

1. **Consistent Ordering**: Use incremental order values (100, 200, 300) to allow easy insertion of new modules
2. **Role Management**: Be specific with roles and use `override_menu_roles` when modules should have different access than their parent application
3. **Mobile Support**: Provide `mobile_title` and `mobile_view_name` for better mobile experience
4. **Filtering**: Use appropriate filters for list modules to show only relevant records
5. **Hints**: Provide helpful hint text to guide users

## Troubleshooting

### Common Issues

1. **Module not appearing**: Check if the module is active and the user has required roles
2. **Wrong parent application**: Verify the application sys_id is correct
3. **Filter errors**: Ensure filter syntax follows ServiceNow query format
4. **Role conflicts**: Check if `override_menu_roles` should be used

### Error Messages

- "Failed to create application module": Check required parameters and application sys_id
- "Module not found": Verify the module_id exists and is accessible
- "Access denied": User lacks required roles to perform the operation