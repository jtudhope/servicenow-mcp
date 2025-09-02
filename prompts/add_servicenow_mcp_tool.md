# ServiceNow MCP Tool Creation Prompt

Use this prompt to guide the development of new tools for the ServiceNow MCP project. This structured approach ensures consistency in implementation, testing, and documentation.

## Background

The ServiceNow MCP (Model Completion Protocol) server allows Claude to interact with ServiceNow instances, retrieving data and performing actions through the ServiceNow API. Adding new tools expands the capabilities of this bridge.

## Required Files to Create/Modify

For each new tool, you need to:

1. Create/modify a tool module in `src/servicenow_mcp/tools/`
2. Update the tools `src/servicenow_mcp/tools/__init__.py` to expose the new tool
3. Update `src/servicenow_mcp/utils/tool_utils.py` to register the tool with the MCP server
4. Update documentation in the `docs/` directory
5. Update the `README.md` to include the new tool

## Implementation Steps

Please implement the following ServiceNow tool capability: {DESCRIBE_CAPABILITY_HERE}

Follow these steps to ensure a complete implementation:

### 1. Tool Module Implementation

The tool should be created in a subfolder within src/servicenow_mcp/tools/{tool_folder_name}, if the user fails to specify a folder BE SURE TO PROMPT them with the correct folder location to use. You can review the available folders and suggest a folder.

```python
# Create a new file or modify an existing module in src/servicenow_mcp/tools/


"""
{TOOL_NAME} tools for the ServiceNow MCP server.

This module provides tools for {TOOL_DESCRIPTION}.
"""

import logging
from typing import Optional, List

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class {ToolName}Params(BaseModel):
    """Parameters for {tool_name}."""

    # Define parameters with type annotations and descriptions
    param1: str = Field(..., description="Description of parameter 1")
    param2: Optional[str] = Field(None, description="Description of parameter 2")
    # Add more parameters as needed


class {ToolName}Response(BaseModel):
    """Response from {tool_name} operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    # Add more response fields as needed


def {tool_name}(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: {ToolName}Params,
) -> {ToolName}Response:
    """
    {Tool description with detailed explanation}.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for {tool_name}.

    Returns:
        Response with {description of response}.
    """
    api_url = f"{config.api_url}/table/{table_name}"

    # Build request data
    data = {
        # Map parameters to API request fields
        "field1": params.param1,
    }

    if params.param2:
        data["field2"] = params.param2
    # Add conditional fields as needed

    # Make request
    try:
        response = requests.post(  # or get, patch, delete as appropriate
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return {ToolName}Response(
            success=True,
            message="{Tool name} completed successfully",
            # Add more response fields from result as needed
        )

    except requests.RequestException as e:
        logger.error(f"Failed to {tool_name}: {e}")
        return {ToolName}Response(
            success=False,
            message=f"Failed to {tool_name}: {str(e)}",
        )
```

### 2. Update config/tool_packages.yaml

```python
# Add configuration for new tool to appropriate category, use the {tool_folder_name} as the category
platform_developer:
  # Script Includes
  - list_script_includes
  - get_script_include
  - create_script_include
  - update_script_include
  - delete_script_include
  - execute_script_include
```


### 2. Update tools/__init__.py

Add the folder to scan to import the tool if a new folder was created (otherwise the tool will automatically be identified)
```python
# Add import for new tool

subfolders = ['catalog', 'developer', 'foundation', 'agile', 'notifications', 'knowledge', 'menu', 'portal','{tool_folder_name}']
    
```

### 3. Update tool_utils.py


Add the folder to scan to import the tool if a new folder was created (otherwise the tool will automatically be identified)
```python
# Add import for new tool

subfolders = ['catalog', 'developer', 'foundation', 'agile', 'notifications', 'knowledge', 'menu', 'portal','{tool_folder_name}']
    
```



### 4. Update Documentation

Create or update a markdown file in `docs/` that explains the tool:

```markdown
# {Tool Category} in ServiceNow MCP

## {Tool Name}

{Detailed description of the tool}

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | Yes | Description of parameter 1 |
| param2 | string | No | Description of parameter 2 |
| ... | ... | ... | ... |

### Example

```python
# Example usage of {tool_name}
result = {tool_name}({
    "param1": "value1",
    "param2": "value2"
})
```

### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| ... | ... | ... |


### 5. Update README.md

Add the new tool to the appropriate section in README.md:

```markdown
#### {Tool Category} Tools

1. **existing_tool** - Description of existing tool
...
N. **{tool_name}** - {Brief description of the new tool}
```

Also add example usage to the "Example Usage with Claude" section:

```markdown
#### {Tool Category} Examples
- "Existing example query"
...
- "{Example natural language query that would use the new tool}"
```

## Documentation Guidelines

1. Use clear, concise language
2. Include all parameters and their descriptions
3. Provide usage examples
4. Document common errors and troubleshooting steps
5. Update README.md to showcase the new functionality

## Best Practices

1. Follow existing code patterns and style
2. Add appropriate error handling
3. Include detailed logging
4. Use meaningful variable and function names
5. Add type hints and docstrings
6. Keep functions focused and single-purpose

## Example Natural Language Commands for Claude

List examples of natural language prompts that users can give to Claude that would trigger the new tool:

- "Prompt example 1"
- "Prompt example 2"
- "Prompt example 3" 