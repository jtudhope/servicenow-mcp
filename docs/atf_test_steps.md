# ATF Test Step Management in ServiceNow MCP

## Overview

The ATF Test Step tools provide comprehensive functionality for managing ATF test steps in ServiceNow. These tools allow you to create, read, update, delete, clone, and reorder test steps that make up ATF tests through the MCP interface. Test steps are stored in the `sys_atf_step` table and define the individual actions that comprise an automated test.

## Available ATF Test Step Tools

### create_atf_test_step

Creates a new ATF test step in ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| test | string | Yes | Test sys_id this step belongs to |
| step_config | string | Yes | Step configuration sys_id |
| display_name | string | No | Display name for the test step |
| description | string | No | Description of the test step |
| notes | string | No | Additional notes for the test step |
| order | integer | No | Execution order of the step |
| table | string | No | Table this step operates on |
| timeout | integer | No | Timeout for step execution (in seconds) |
| inputs | string | No | JSON string of input parameters |
| callable_outputs | string | No | JSON string of callable outputs |
| active | boolean | No | Whether the step is active (default: true) |
| snapshot | string | No | Snapshot data for the step |

**Example:**
```python
result = create_atf_test_step({
    "test": "test_sys_id_123",
    "step_config": "step_config_sys_id_456",
    "display_name": "Login to Portal",
    "description": "Automated login step for user authentication",
    "order": 1,
    "timeout": 30
})
```

### update_atf_test_step

Updates an existing ATF test step in ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| step_id | string | Yes | ATF test step sys_id |
| display_name | string | No | Updated display name |
| description | string | No | Updated description |
| notes | string | No | Updated notes |
| order | integer | No | Updated execution order |
| table | string | No | Updated table reference |
| timeout | integer | No | Updated timeout value |
| inputs | string | No | Updated input parameters (JSON string) |
| callable_outputs | string | No | Updated callable outputs (JSON string) |
| active | boolean | No | Updated active status |
| snapshot | string | No | Updated snapshot data |

**Example:**
```python
result = update_atf_test_step({
    "step_id": "step_sys_id_789",
    "description": "Updated login step with enhanced validation",
    "timeout": 45,
    "active": true
})
```

### get_atf_test_step

Retrieves details of a specific ATF test step.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| step_id | string | Yes | ATF test step sys_id |

**Example:**
```python
result = get_atf_test_step({
    "step_id": "step_sys_id_789"
})
```

### list_atf_test_steps

Lists ATF test steps with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| test | string | No | Filter by test sys_id |
| active | boolean | No | Filter by active status |
| step_config | string | No | Filter by step configuration sys_id |
| table | string | No | Filter by table name |
| limit | integer | No | Maximum number of steps to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Additional query string |

**Example:**
```python
result = list_atf_test_steps({
    "test": "test_sys_id_123",
    "active": true,
    "limit": 20
})
```

### delete_atf_test_step

Deletes an ATF test step from ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| step_id | string | Yes | ATF test step sys_id |

**Example:**
```python
result = delete_atf_test_step({
    "step_id": "step_sys_id_789"
})
```

### clone_atf_test_step

Creates a copy of an existing ATF test step.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_step_id | string | Yes | Source test step sys_id to clone |
| target_test | string | No | Target test sys_id (defaults to same test) |
| new_display_name | string | No | Display name for the cloned step |
| new_order | integer | No | Order for the cloned step |

**Example:**
```python
result = clone_atf_test_step({
    "source_step_id": "step_sys_id_789",
    "target_test": "different_test_sys_id",
    "new_display_name": "Cloned Login Step",
    "new_order": 5
})
```

### reorder_atf_test_steps

Reorders ATF test steps within a test by updating their order values.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| test | string | Yes | Test sys_id to reorder steps within |
| step_order | array | Yes | List of step sys_ids in desired execution order |

**Example:**
```python
result = reorder_atf_test_steps({
    "test": "test_sys_id_123",
    "step_order": ["step1_sys_id", "step3_sys_id", "step2_sys_id"]
})
```

## Response Structure

All ATF test step operations return structured responses with consistent fields:

### Standard Response Fields

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| step_id | string | ATF test step sys_id (when applicable) |
| display_name | string | Test step display name (when applicable) |
| data | object | Additional response data |

### List Response Fields

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| steps | array | Array of ATF test step objects |
| total_count | integer | Total number of steps found |

### Clone Response Fields

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the cloning was successful |
| message | string | A message describing the result |
| original_step_id | string | Source step sys_id |
| cloned_step_id | string | New cloned step sys_id |
| data | object | Additional clone data |

## Common Use Cases

### Creating a Test Step Sequence
```python
# Create initial login step
login_step = create_atf_test_step({
    "test": "test_sys_id_123",
    "step_config": "login_config_sys_id",
    "display_name": "User Login",
    "description": "Authenticate user with credentials",
    "order": 1,
    "timeout": 30
})

# Create navigation step
nav_step = create_atf_test_step({
    "test": "test_sys_id_123", 
    "step_config": "navigate_config_sys_id",
    "display_name": "Navigate to Incidents",
    "description": "Navigate to incident list view",
    "order": 2,
    "timeout": 15
})
```

### Managing Step Lifecycle
```python
# List all steps for a test
steps = list_atf_test_steps({"test": "test_sys_id_123"})

# Update a step with new parameters
update_atf_test_step({
    "step_id": "step_sys_id",
    "description": "Enhanced step with additional validation",
    "timeout": 45
})

# Clone a step to another test
clone_atf_test_step({
    "source_step_id": "step_sys_id",
    "target_test": "other_test_sys_id",
    "new_display_name": "Copied Validation Step"
})
```

### Reordering Test Steps
```python
# Get current step order
current_steps = list_atf_test_steps({"test": "test_sys_id_123"})

# Reorder steps (move step 3 to position 1)
reorder_atf_test_steps({
    "test": "test_sys_id_123",
    "step_order": ["step3_sys_id", "step1_sys_id", "step2_sys_id"]
})
```

### Finding Steps by Configuration
```python
# Find all steps using a specific step configuration
config_steps = list_atf_test_steps({
    "step_config": "login_config_sys_id",
    "limit": 50
})
```

## Error Handling

All tools include comprehensive error handling and will return structured error responses:

```python
{
    "success": false,
    "message": "Detailed error message explaining what went wrong"
}
```

Common error scenarios:
- Invalid test or step sys_id
- Missing required parameters (test, step_config)
- Invalid step configuration
- Authentication/permission issues
- Network connectivity problems
- ServiceNow instance availability
- Step ordering conflicts

## Best Practices

1. **Step Naming**: Use descriptive display names that clearly indicate the step's purpose
2. **Documentation**: Always provide meaningful descriptions for complex test steps
3. **Ordering**: Plan step execution order carefully, especially for dependent operations
4. **Timeouts**: Set appropriate timeout values based on expected execution time
5. **Configuration Management**: Maintain consistent step configurations across similar tests
6. **Input Validation**: Ensure input parameters are properly formatted JSON when required
7. **Error Handling**: Include proper error handling in step configurations
8. **Reusability**: Use cloning to replicate common step patterns across tests

## ServiceNow Table Reference

The ATF test step tools work with these ServiceNow tables:
- `sys_atf_step` - Main ATF test step records
- `sys_atf_test` - Parent ATF test records
- `sys_atf_step_config` - Step configuration templates

## Field Types and Validation

### Key Field Types
- **test**: Reference to `sys_atf_test` table
- **step_config**: Reference to `sys_atf_step_config` table  
- **order**: Integer for execution sequence
- **timeout**: Integer in seconds
- **inputs**: JSON string for step parameters
- **callable_outputs**: JSON string for step outputs
- **active**: Boolean for step enablement
- **table**: String reference to ServiceNow table name

### JSON Field Formats
The `inputs` and `callable_outputs` fields expect JSON string format:
```python
{
    "inputs": '{"username": "test_user", "password": "test_pass"}',
    "callable_outputs": '{"login_result": "success", "session_id": "abc123"}'
}
```

## Natural Language Examples

Here are example natural language queries that would trigger these ATF test step tools:

- "Create a new ATF test step for user login"
- "Show me all test steps for the incident test"
- "Update the timeout for the navigation step"
- "Clone the login step to another test"
- "Reorder the test steps to put validation first"
- "List all active test steps using the form submission config"
- "Delete the obsolete validation step"
- "Get details for the step that handles user authentication"