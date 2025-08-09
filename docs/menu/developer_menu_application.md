# Application Menu Items in ServiceNow MCP

## Overview

The Application Menu tools allow developers to manage menu items that appear in ServiceNow's navigation interface, including the All menu and other navigation areas. These tools enable creating custom menu entries that provide access to tables, modules, reports, or other functionality within the ServiceNow platform.

## Available Tools

### create_application_menu

Creates a new application menu item that appears in the ServiceNow navigation interface.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Display title of the menu item (appears in the interface) |
| name | string | No | Internal name of the menu item (for reference) |
| description | string | No | Description of the menu item |
| active | boolean | No | Whether the menu item is active and visible (default: true) |
| category | string | No | Category sys_id for grouping menu items |
| roles | array | No | List of roles required to access this menu item |
| order | float | No | Display order (lower numbers appear first) |
| hint | string | No | Tooltip text displayed on hover |
| device_type | string | No | Device type compatibility ("browser", "mobile", "tablet", default: "browser") |
| view_name | string | No | View name for the menu item |
| sys_overrides | string | No | Sys_id of menu item this overrides |
| sys_domain | string | No | Domain for the menu item (default: "global") |
| sys_domain_path | string | No | Domain path for the menu item (default: "/") |

#### Example

```python
result = create_application_menu({
    "title": "Custom Reports",
    "name": "custom_reports",
    "description": "Access to custom reporting dashboard",
    "active": true,
    "category": "reporting_category_id",
    "roles": ["admin", "report_viewer"],
    "order": 100,
    "hint": "Click to access custom reports and analytics",
    "device_type": "browser"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the created menu item |
| menu_item | object | Complete menu item details |

---

### update_application_menu

Updates an existing application menu item with new settings.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| menu_id | string | Yes | Application menu sys_id to update |
| title | string | No | Updated display title |
| name | string | No | Updated internal name |
| description | string | No | Updated description |
| active | boolean | No | Updated active status |
| category | string | No | Updated category sys_id |
| roles | array | No | Updated list of required roles |
| order | float | No | Updated display order |
| hint | string | No | Updated tooltip text |
| device_type | string | No | Updated device type |
| view_name | string | No | Updated view name |
| sys_overrides | string | No | Updated override reference |

#### Example

```python
result = update_application_menu({
    "menu_id": "a1b2c3d4e5f6g7h8i9j0",
    "title": "Updated Custom Reports",
    "active": false,
    "order": 200,
    "hint": "Updated tooltip for custom reports"
})
```

---

### list_application_menus

Lists application menu items from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| active | boolean | No | Filter by active status |
| category | string | No | Filter by category sys_id |
| device_type | string | No | Filter by device type |
| title | string | No | Filter by title (contains search) |
| limit | integer | No | Maximum number of menu items to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query filter |

#### Example

```python
result = list_application_menus({
    "active": true,
    "device_type": "browser",
    "title": "Report",
    "limit": 25,
    "offset": 0
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| menu_items | array | List of menu item objects |
| total_count | integer | Total number of menu items found |

---

### get_application_menu

Retrieves detailed information about a specific application menu item.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| menu_id | string | Yes | Application menu sys_id |

#### Example

```python
result = get_application_menu({
    "menu_id": "a1b2c3d4e5f6g7h8i9j0"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the menu item |
| menu_item | object | Complete menu item details |

---

### delete_application_menu

Permanently deletes an application menu item from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| menu_id | string | Yes | Application menu sys_id to delete |

#### Example

```python
result = delete_application_menu({
    "menu_id": "a1b2c3d4e5f6g7h8i9j0"
})
```

#### Response

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| sys_id | string | System ID of the deleted menu item |

---

## Common Use Cases

### 1. Custom Table Access

Create menu items that provide quick access to custom tables or modules.

```python
# Create menu for custom asset tracking table
create_application_menu({
    "title": "Asset Tracking",
    "name": "asset_tracking",
    "description": "Manage and track organizational assets",
    "active": true,
    "category": "inventory_category",
    "roles": ["asset_manager", "admin"],
    "order": 50,
    "hint": "Access asset tracking and management tools"
})
```

### 2. Reporting Dashboard Access

Set up menu items for custom reports and analytics dashboards.

```python
create_application_menu({
    "title": "Executive Dashboard",
    "name": "exec_dashboard", 
    "description": "High-level metrics and KPIs for executives",
    "active": true,
    "category": "reporting_category",
    "roles": ["executive", "manager", "admin"],
    "order": 10,
    "hint": "View executive-level performance metrics",
    "device_type": "browser"
})
```

### 3. Administrative Tools

Create menu items for specialized administrative functions.

```python
create_application_menu({
    "title": "System Maintenance",
    "name": "system_maintenance",
    "description": "Tools for system maintenance and cleanup",
    "active": true,
    "category": "admin_category",
    "roles": ["admin", "system_administrator"],
    "order": 999,
    "hint": "Access system maintenance utilities",
    "device_type": "browser"
})
```

### 4. Mobile-Specific Menus

Create menu items optimized for mobile devices.

```python
create_application_menu({
    "title": "Field Service",
    "name": "field_service_mobile",
    "description": "Mobile access to field service tools",
    "active": true,
    "category": "mobile_category",
    "roles": ["field_technician", "service_manager"],
    "order": 20,
    "hint": "Mobile tools for field service operations",
    "device_type": "mobile"
})
```

## Best Practices

### 1. Menu Organization
- Use meaningful, descriptive titles
- Group related items using categories
- Set appropriate display orders for logical grouping
- Keep menu hierarchies shallow and intuitive

### 2. Role-Based Access
- Assign appropriate roles to control menu visibility
- Use principle of least privilege
- Consider creating role-specific menu views
- Test menu access with different user roles

### 3. User Experience
- Write clear, concise hints/tooltips
- Use consistent naming conventions
- Order items by frequency of use
- Consider device-specific menu layouts

### 4. Performance and Maintenance
- Regularly review and update menu structures
- Remove unused or obsolete menu items
- Monitor menu performance and user engagement
- Keep menu descriptions current and accurate

## Menu Categories

Common category types for organizing menu items:

- **Admin Tools**: Administrative functions and system management
- **Reports**: Reporting tools and dashboards
- **Service Management**: ITSM-related functionality
- **Custom Applications**: Custom-developed applications
- **Integrations**: Third-party system integrations
- **Mobile Tools**: Mobile-optimized functionality

## Device Type Considerations

### Browser Menus
- Full feature set available
- Support for complex navigation
- Optimized for desktop/laptop use
- Can include detailed tooltips and descriptions

### Mobile Menus
- Simplified navigation
- Touch-optimized interface
- Limited screen real estate
- Focus on essential functions

### Tablet Menus
- Hybrid approach between browser and mobile
- Support for both touch and traditional interaction
- Medium screen real estate
- Balance of features and usability

## Integration with Other Tools

Application menus work well with other ServiceNow MCP tools:

- **ACLs**: Control access to menu items based on roles
- **UI Actions**: Add custom actions to menu-accessible forms
- **Categories**: Organize menus into logical groupings
- **Tables**: Create menus that directly access custom tables
- **Workflows**: Link menu items to workflow-driven processes

## Troubleshooting

### Common Issues

1. **Menu not visible**
   - Check if menu is active
   - Verify user has required roles
   - Confirm category permissions
   - Check device type compatibility

2. **Incorrect menu order**
   - Review order values (lower = higher priority)
   - Check for duplicate order values
   - Verify category-based grouping
   - Test with different user contexts

3. **Access denied errors**
   - Verify role assignments
   - Check ACL configurations
   - Confirm domain permissions
   - Review sys_overrides settings

4. **Mobile display issues**
   - Confirm device_type setting
   - Test on actual mobile devices
   - Check responsive design compatibility
   - Verify mobile-specific roles

## Natural Language Commands for Claude

Users can interact with application menus using natural language:

- "Create a menu item for custom reports that only admins can see"
- "Add a new menu entry for the field service mobile app"
- "List all active menu items in the reporting category"
- "Update the asset management menu to change its display order"
- "Show me the details of the executive dashboard menu item"
- "Delete the old maintenance tools menu that's no longer used"
- "Create a menu for help desk tickets that appears first in the list"
- "Add a menu item for system administrators to access cleanup tools"
- "Find all menu items that mobile users can access"
- "Set up a menu entry for the new project management dashboard"