# Catalog Client Scripts Management in ServiceNow MCP

## Overview

The Catalog Client Scripts tools provide comprehensive management of Catalog Client Scripts in ServiceNow. Catalog Client Scripts are stored in the `catalog_script_client` table and represent JavaScript that runs in the user's browser to control behavior on Service Catalog items, record producers, or order guide forms. These scripts enhance the user experience by providing dynamic client-side functionality.

## Tools

### create_catalog_client_script

Create a new catalog client script in the catalog_script_client table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the catalog client script |
| script | string | Yes | Client script content |
| cat_item | string | No | Catalog item sys_id this script applies to |
| variable_set | string | No | Variable set sys_id this script applies to |
| cat_variable | string | No | Variable this script applies to |
| applies_to | string | No | What this script applies to |
| applies_catalog | boolean | No | Whether this script applies to catalog (default: false) |
| applies_req_item | boolean | No | Whether this script applies to requested items (default: false) |
| applies_sc_task | boolean | No | Whether this script applies to SC tasks (default: false) |
| applies_target_record | boolean | No | Whether this script applies to target records (default: false) |
| va_supported | boolean | No | Whether virtual agent is supported (default: false) |
| active | boolean | No | Whether the script is active (default: true) |
| ui_type | string | No | UI type for the script |
| type | string | No | Type of script |

#### Example

```python
# Example usage of create_catalog_client_script
result = create_catalog_client_script({
    "name": "Priority Field Validation",
    "script": "function onChange(control, oldValue, newValue, isLoading) { if (newValue == 'high') { alert('High priority requires approval'); } }",
    "cat_item": "b0c4030ac0a8000001c9dd3394009c96",
    "cat_variable": "priority",
    "applies_catalog": true,
    "active": true
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created catalog client script data including sys_id |

### update_catalog_client_script

Update an existing catalog client script in the catalog_script_client table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| script_id | string | Yes | Catalog client script sys_id |
| name | string | No | Updated name of the script |
| script | string | No | Updated client script content |
| cat_item | string | No | Updated catalog item sys_id |
| variable_set | string | No | Updated variable set sys_id |
| cat_variable | string | No | Updated variable |
| applies_to | string | No | Updated applies to value |
| applies_catalog | boolean | No | Updated applies to catalog setting |
| applies_req_item | boolean | No | Updated applies to requested items setting |
| applies_sc_task | boolean | No | Updated applies to SC tasks setting |
| applies_target_record | boolean | No | Updated applies to target records setting |
| va_supported | boolean | No | Updated virtual agent support setting |
| active | boolean | No | Updated active status |
| ui_type | string | No | Updated UI type |
| type | string | No | Updated script type |

#### Example

```python
# Example usage of update_catalog_client_script
result = update_catalog_client_script({
    "script_id": "abc123def456ghi789",
    "name": "Enhanced Priority Field Validation",
    "script": "function onChange(control, oldValue, newValue, isLoading) { if (newValue == 'high') { alert('High priority requires manager approval'); showField('manager_approval'); } }",
    "active": true
})
```

### list_catalog_client_scripts

List catalog client scripts from the catalog_script_client table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of scripts to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| cat_item | string | No | Filter by catalog item sys_id |
| variable_set | string | No | Filter by variable set sys_id |
| cat_variable | string | No | Filter by variable |
| active | boolean | No | Filter by active status |
| query | string | No | Search query for script details |

#### Example

```python
# Example usage of list_catalog_client_scripts
result = list_catalog_client_scripts({
    "limit": 20,
    "cat_item": "b0c4030ac0a8000001c9dd3394009c96",
    "active": true,
    "query": "validation"
})
```

### get_catalog_client_script

Get a specific catalog client script from the catalog_script_client table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| script_id | string | Yes | Catalog client script sys_id |

#### Example

```python
# Example usage of get_catalog_client_script
result = get_catalog_client_script({
    "script_id": "abc123def456ghi789"
})
```

### delete_catalog_client_script

Delete a catalog client script from the catalog_script_client table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| script_id | string | Yes | Catalog client script sys_id |

#### Example

```python
# Example usage of delete_catalog_client_script
result = delete_catalog_client_script({
    "script_id": "abc123def456ghi789"
})
```

### clone_catalog_client_script

Clone an existing catalog client script in the catalog_script_client table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| script_id | string | Yes | Source catalog client script sys_id |
| new_name | string | Yes | Name for the cloned script |

#### Example

```python
# Example usage of clone_catalog_client_script
result = clone_catalog_client_script({
    "script_id": "abc123def456ghi789",
    "new_name": "Cloned Priority Field Validation"
})
```

## Common Use Cases

### Field Validation Scripts

Create client scripts to validate form field input on catalog items:

```python
# Create a script to validate email format
result = create_catalog_client_script({
    "name": "Email Format Validation",
    "script": """
function onChange(control, oldValue, newValue, isLoading) {
    if (newValue && !isValidEmail(newValue)) {
        alert('Please enter a valid email address');
        g_form.setValue('email', oldValue);
    }
}

function isValidEmail(email) {
    var re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return re.test(email);
}
    """,
    "cat_item": "email_request_item_id",
    "cat_variable": "email_address",
    "applies_catalog": true,
    "active": true
})
```

### Dynamic Field Display

Control field visibility based on user selections:

```python
# Create a script to show/hide fields based on request type
result = create_catalog_client_script({
    "name": "Dynamic Field Display",
    "script": """
function onChange(control, oldValue, newValue, isLoading) {
    if (newValue == 'laptop') {
        g_form.setVisible('operating_system', true);
        g_form.setVisible('memory_size', true);
    } else {
        g_form.setVisible('operating_system', false);
        g_form.setVisible('memory_size', false);
    }
}
    """,
    "cat_item": "hardware_request_item_id",
    "cat_variable": "device_type",
    "applies_catalog": true,
    "active": true
})
```

### Auto-Population Scripts

Automatically populate fields based on other field values:

```python
# Create a script to auto-populate department based on user selection
result = create_catalog_client_script({
    "name": "Auto-populate Department",
    "script": """
function onChange(control, oldValue, newValue, isLoading) {
    if (newValue) {
        var ga = new GlideAjax('UserUtils');
        ga.addParam('sysparm_name', 'getDepartment');
        ga.addParam('sysparm_user_id', newValue);
        ga.getXML(function(response) {
            var answer = response.responseXML.documentElement.getAttribute('answer');
            g_form.setValue('department', answer);
        });
    }
}
    """,
    "cat_item": "access_request_item_id",
    "cat_variable": "requested_for",
    "applies_catalog": true,
    "active": true
})
```

## Best Practices

1. **Use meaningful script names** that clearly describe the script's purpose
2. **Test thoroughly** across different browsers and devices
3. **Minimize performance impact** by avoiding heavy operations in onChange events
4. **Handle errors gracefully** to prevent breaking the user experience
5. **Use specific targeting** with cat_item or cat_variable to avoid conflicts
6. **Document complex logic** within script comments for maintenance
7. **Validate user input** before processing to ensure data integrity
8. **Consider mobile compatibility** when writing client scripts

## Script Scope Settings

Configure when and where scripts execute:

- **applies_catalog**: Script runs on the service catalog
- **applies_req_item**: Script runs on requested items
- **applies_sc_task**: Script runs on service catalog tasks
- **applies_target_record**: Script runs on target records
- **va_supported**: Script is compatible with Virtual Agent

## Error Handling

All tools return structured responses with success indicators and error messages:

```python
if result["success"]:
    print(f"Operation successful: {result['message']}")
    # Process result data
else:
    print(f"Operation failed: {result['message']}")
    # Handle error
```

## Integration with Other Tools

Catalog Client Scripts work closely with:
- **Catalog Items** - Scripts enhance catalog item functionality
- **Catalog Variables** - Use `list_catalog_variables` to understand available form fields
- **Catalog UI Policies** - Client scripts and UI policies can work together for complex form behavior
- **Service Portal** - Scripts work in both platform UI and Service Portal

## Example Natural Language Commands for Claude

- "Create a client script to validate phone number format on the hardware request form"
- "List all active client scripts for the software license catalog item"
- "Update the email validation script to include domain restrictions"
- "Clone the existing field validation script for use with a different catalog item"
- "Show me all client scripts that affect the priority variable"
- "Create a script to auto-calculate total cost based on quantity and unit price"
- "Delete the obsolete validation script for the discontinued catalog item"

## JavaScript API Reference

Common ServiceNow client-side APIs used in catalog scripts:

- **g_form.getValue(fieldName)** - Get field value
- **g_form.setValue(fieldName, value)** - Set field value
- **g_form.setVisible(fieldName, visible)** - Show/hide field
- **g_form.setMandatory(fieldName, mandatory)** - Set field as required
- **g_form.setReadOnly(fieldName, readOnly)** - Make field read-only
- **g_form.addErrorMessage(message)** - Display error message
- **g_form.addInfoMessage(message)** - Display information message