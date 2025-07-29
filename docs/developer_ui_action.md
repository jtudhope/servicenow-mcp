# Developer Toolbox in ServiceNow MCP

## UI Action Management

The UI Action tools provide comprehensive functionality for creating, updating, listing, retrieving, and deleting UI Actions in ServiceNow. UI Actions are interactive elements that appear on forms, lists, and related lists to provide users with specific actions they can perform.

### Create UI Action

Creates a new UI Action in ServiceNow with the specified configuration.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Internal name of the UI action |
| table | string | Yes | Table the UI action applies to |
| action_name | string | Yes | Display name (button text) for the action |
| script | string | Yes | Client-side JavaScript to execute |
| condition | string | No | Script to determine when the action is visible |
| onclick | string | No | OnClick script for the action |
| form_button | boolean | No | Whether to show on form (default: true) |
| list_banner_button | boolean | No | Whether to show on list banner (default: false) |
| list_choice | boolean | No | Whether to show in list choice menu (default: false) |
| list_context_menu | boolean | No | Whether to show in list context menu (default: false) |
| active | boolean | No | Whether the UI action is active (default: true) |
| order | integer | No | Display order of the UI action (default: 100) |
| hint | string | No | Tooltip hint for the action |
| client | boolean | No | Whether this is a client-side action (default: true) |
| isolate_script | boolean | No | Whether to isolate the script (default: true) |

#### Example

```python
# Example usage of create_ui_action
result = create_ui_action({
    "name": "custom_approval_action",
    "table": "incident",
    "action_name": "Quick Approve",
    "script": "alert('Approved!'); g_form.setValue('state', '6');",
    "condition": "gs.hasRole('approver')",
    "form_button": true,
    "order": 50,
    "hint": "Quickly approve this incident"
})
```

### Update UI Action

Updates an existing UI Action in ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ui_action_id | string | Yes | UI Action ID or sys_id to update |
| name | string | No | Internal name of the UI action |
| action_name | string | No | Display name (button text) for the action |
| script | string | No | Client-side JavaScript to execute |
| condition | string | No | Script to determine when the action is visible |
| onclick | string | No | OnClick script for the action |
| form_button | boolean | No | Whether to show on form |
| list_banner_button | boolean | No | Whether to show on list banner |
| list_choice | boolean | No | Whether to show in list choice menu |
| list_context_menu | boolean | No | Whether to show in list context menu |
| active | boolean | No | Whether the UI action is active |
| order | integer | No | Display order of the UI action |
| hint | string | No | Tooltip hint for the action |
| client | boolean | No | Whether this is a client-side action |
| isolate_script | boolean | No | Whether to isolate the script |

#### Example

```python
# Example usage of update_ui_action
result = update_ui_action({
    "ui_action_id": "a1b2c3d4e5f6",
    "script": "alert('Updated script!'); g_form.setValue('state', '7');",
    "active": false,
    "hint": "Updated tooltip"
})
```

### List UI Actions

Retrieves a list of UI Actions from ServiceNow with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table | string | No | Filter by table name |
| active | boolean | No | Filter by active status |
| limit | integer | No | Maximum number of UI actions to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Search query for name, action_name, or table |

#### Example

```python
# Example usage of list_ui_actions
result = list_ui_actions({
    "table": "incident",
    "active": true,
    "limit": 20,
    "query": "approval"
})
```

### Get UI Action

Retrieves a specific UI Action by its ID.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ui_action_id | string | Yes | UI Action ID or sys_id |

#### Example

```python
# Example usage of get_ui_action
result = get_ui_action({
    "ui_action_id": "a1b2c3d4e5f6"
})
```

### Delete UI Action

Deletes a UI Action from ServiceNow.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ui_action_id | string | Yes | UI Action ID or sys_id to delete |

#### Example

```python
# Example usage of delete_ui_action
result = delete_ui_action({
    "ui_action_id": "a1b2c3d4e5f6"
})
```

### Response Format

All UI Action tools return responses with the following structure:

#### Single UI Action Operations (Create, Update, Get, Delete)

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| ui_action_id | string | The UI Action number (for create/update operations) |
| sys_id | string | The system ID of the UI action |
| data | object | Complete UI action data (for get operations) |

#### List Operations

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| ui_actions | array | Array of UI action objects |
| total_count | integer | Total number of UI actions matching the criteria |

## Common Use Cases

### Creating a Custom Form Button

Create a UI action that appears as a button on incident forms to perform a specific action:

```javascript
// UI Action script example
function customAction() {
    if (g_form.getValue('state') == '2') {
        g_form.setValue('state', '6');
        g_form.setValue('work_notes', 'Incident resolved via custom action');
        g_form.save();
    } else {
        alert('This action can only be used on In Progress incidents');
    }
}
customAction();
```

### Creating a Conditional UI Action

Create a UI action that only appears for users with specific roles:

```javascript
// Condition script example
gs.hasRole('incident_manager') || gs.hasRole('admin')
```

### Bulk Operations UI Action

Create a UI action for list views to perform bulk operations:

```javascript
// List banner button script example
var selectedRecords = g_list.getChecked();
if (selectedRecords.length > 0) {
    // Perform bulk operation
    for (var i = 0; i < selectedRecords.length; i++) {
        // Process each selected record
    }
} else {
    alert('Please select at least one record');
}
```

## Best Practices

1. **Use meaningful names**: Choose descriptive names for both the internal name and action_name
2. **Add conditions**: Use condition scripts to control when UI actions are visible
3. **Set appropriate order**: Use the order field to control the sequence of buttons
4. **Provide hints**: Add helpful tooltips using the hint parameter
5. **Test thoroughly**: Always test UI actions in different contexts (form, list, etc.)
6. **Consider security**: Use condition scripts to enforce role-based access
7. **Isolate scripts**: Keep isolate_script enabled to prevent conflicts with other scripts