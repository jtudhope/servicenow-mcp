[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/osomai-servicenow-mcp-badge.png)](https://mseep.ai/app/osomai-servicenow-mcp)

# ServiceNow MCP Server

A Model Completion Protocol (MCP) server implementation for ServiceNow, allowing Claude to interact with ServiceNow instances.

<a href="https://glama.ai/mcp/servers/@osomai/servicenow-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@osomai/servicenow-mcp/badge" alt="ServiceNow Server MCP server" />
</a>

## Overview

This project implements an MCP server that enables Claude to connect to ServiceNow instances, retrieve data, and perform actions through the ServiceNow API. It serves as a bridge between Claude and ServiceNow, allowing for seamless integration.

## Features

- Connect to ServiceNow instances using various authentication methods (Basic, OAuth, API Key)
- Query ServiceNow records and tables
- Create, update, and delete ServiceNow records
- Execute ServiceNow scripts and workflows
- Access and query the ServiceNow Service Catalog
- Analyze and optimize the ServiceNow Service Catalog
- Debug mode for troubleshooting
- Support for both stdio and Server-Sent Events (SSE) communication

## Installation

### Prerequisites

- Python 3.11 or higher
- A ServiceNow instance with appropriate access credentials

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/servicenow-mcp.git
   cd servicenow-mcp
   ```

2. Create a virtual environment and install the package:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. Create a `.env` file with your ServiceNow credentials:
   ```
   SERVICENOW_INSTANCE_URL=https://your-instance.service-now.com
   SERVICENOW_USERNAME=your-username
   SERVICENOW_PASSWORD=your-password
   SERVICENOW_AUTH_TYPE=basic  # or oauth, api_key
   ```

## Usage

### Standard (stdio) Mode

To start the MCP server:

```
python -m servicenow_mcp.cli
```

Or with environment variables:

```
SERVICENOW_INSTANCE_URL=https://your-instance.service-now.com SERVICENOW_USERNAME=your-username SERVICENOW_PASSWORD=your-password SERVICENOW_AUTH_TYPE=basic python -m servicenow_mcp.cli
```

### Server-Sent Events (SSE) Mode

The ServiceNow MCP server can also run as a web server using Server-Sent Events (SSE) for communication, which allows for more flexible integration options.

#### Starting the SSE Server

You can start the SSE server using the provided CLI:

```
servicenow-mcp-sse --instance-url=https://your-instance.service-now.com --username=your-username --password=your-password
```

By default, the server will listen on `0.0.0.0:8080`. You can customize the host and port:

```
servicenow-mcp-sse --host=127.0.0.1 --port=8000
```

#### Connecting to the SSE Server

The SSE server exposes two main endpoints:

- `/sse` - The SSE connection endpoint
- `/messages/` - The endpoint for sending messages to the server

#### Example

See the `examples/sse_server_example.py` file for a complete example of setting up and running the SSE server.

```python
from servicenow_mcp.server import ServiceNowMCP
from servicenow_mcp.server_sse import create_starlette_app
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, AuthType, BasicAuthConfig
import uvicorn

# Create server configuration
config = ServerConfig(
    instance_url="https://your-instance.service-now.com",
    auth=AuthConfig(
        type=AuthType.BASIC,
        config=BasicAuthConfig(
            username="your-username",
            password="your-password"
        )
    ),
    debug=True,
)

# Create ServiceNow MCP server
servicenow_mcp = ServiceNowMCP(config)

# Create Starlette app with SSE transport
app = create_starlette_app(servicenow_mcp, debug=True)

# Start the web server
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## Tool Packaging (Optional)

To manage the number of tools exposed to the language model (especially in environments with limits), the ServiceNow MCP server supports loading subsets of tools called "packages". This is controlled via the `MCP_TOOL_PACKAGE` environment variable.

### Configuration

1.  **Environment Variable:** Set the `MCP_TOOL_PACKAGE` environment variable to the name of the desired package.
    ```bash
    export MCP_TOOL_PACKAGE=catalog_builder
    ```
2.  **Package Definitions:** The available packages and the tools they include are defined in `config/tool_packages.yaml`. You can customize this file to create your own packages.

### Behavior

-   If `MCP_TOOL_PACKAGE` is set to a valid package name defined in `config/tool_packages.yaml`, only the tools listed in that package will be loaded.
-   If `MCP_TOOL_PACKAGE` is **not set** or is empty, the `full` package (containing all tools) is loaded by default.
-   If `MCP_TOOL_PACKAGE` is set to an invalid package name, the `none` package is loaded (no tools except `list_tool_packages`), and a warning is logged.
-   Setting `MCP_TOOL_PACKAGE=none` explicitly loads no tools (except `list_tool_packages`).

### Available Packages (Default)

The default `config/tool_packages.yaml` includes the following role-based packages:

-   `service_desk`: Tools for incident handling and basic user/knowledge lookup.
-   `catalog_builder`: Tools for creating and managing service catalog items, categories, variables, and related scripting (UI Policies, User Criteria).
-   `change_coordinator`: Tools for managing the change request lifecycle, including tasks and approvals.
-   `knowledge_author`: Tools for creating and managing knowledge bases, categories, and articles.
-   `platform_developer`: Tools for server-side scripting (Script Includes), workflow development, and deployment (Changesets).
-   `system_administrator`: Tools for user/group management and viewing system logs.
-   `agile_management`: Tools for managing user stories, epics, scrum tasks, and projects.
-   `full`: Includes all available tools (default).
-   `none`: Includes no tools (except `list_tool_packages`).

### Introspection Tool

-   **`list_tool_packages`**: Lists all available tool package names defined in the configuration and shows the currently loaded package. This tool is available in all packages except `none`.

## Available Tools

**Note:** The availability of the following tools depends on the loaded tool package (see Tool Packaging section above). By default (`full` package), all tools are available.

#### Incident Management Tools

1. **create_incident** - Create a new incident in ServiceNow
2. **update_incident** - Update an existing incident in ServiceNow
3. **add_comment** - Add a comment to an incident in ServiceNow
4. **resolve_incident** - Resolve an incident in ServiceNow
5. **list_incidents** - List incidents from ServiceNow

#### Service Catalog Tools

1. **list_catalog_items** - List service catalog items from ServiceNow
2. **get_catalog_item** - Get a specific service catalog item from ServiceNow
3. **list_catalog_categories** - List service catalog categories from ServiceNow
4. **create_catalog_category** - Create a new service catalog category in ServiceNow
5. **update_catalog_category** - Update an existing service catalog category in ServiceNow
6. **move_catalog_items** - Move catalog items between categories in ServiceNow
7. **create_catalog_item_variable** - Create a new variable (form field) for a catalog item
8. **list_catalog_item_variables** - List all variables for a catalog item
9. **update_catalog_item_variable** - Update an existing variable for a catalog item
10. **list_catalogs** - List service catalogs from ServiceNow

#### Catalog Optimization Tools

1. **get_optimization_recommendations** - Get recommendations for optimizing the service catalog
2. **update_catalog_item** - Update a service catalog item

#### Change Management Tools

1. **create_change_request** - Create a new change request in ServiceNow
2. **update_change_request** - Update an existing change request
3. **list_change_requests** - List change requests with filtering options
4. **get_change_request_details** - Get detailed information about a specific change request
5. **add_change_task** - Add a task to a change request
6. **submit_change_for_approval** - Submit a change request for approval
7. **approve_change** - Approve a change request
8. **reject_change** - Reject a change request

#### Agile Management Tools

##### Story Management
1. **create_story** - Create a new user story in ServiceNow
2. **update_story** - Update an existing user story in ServiceNow
3. **list_stories** - List user stories with filtering options
4. **create_story_dependency** - Create a dependency between two stories
5. **delete_story_dependency** - Delete a dependency between stories

##### Epic Management
1. **create_epic** - Create a new epic in ServiceNow
2. **update_epic** - Update an existing epic in ServiceNow
3. **list_epics** - List epics from ServiceNow with filtering options

##### Scrum Task Management
1. **create_scrum_task** - Create a new scrum task in ServiceNow
2. **update_scrum_task** - Update an existing scrum task in ServiceNow
3. **list_scrum_tasks** - List scrum tasks from ServiceNow with filtering options

##### Project Management
1. **create_project** - Create a new project in ServiceNow
2. **update_project** - Update an existing project in ServiceNow
3. **list_projects** - List projects from ServiceNow with filtering options

#### Workflow Management Tools

1. **list_workflows** - List workflows from ServiceNow
2. **get_workflow** - Get a specific workflow from ServiceNow
3. **create_workflow** - Create a new workflow in ServiceNow
4. **update_workflow** - Update an existing workflow in ServiceNow
5. **delete_workflow** - Delete a workflow from ServiceNow

#### Script Include Management Tools

1. **list_script_includes** - List script includes from ServiceNow
2. **get_script_include** - Get a specific script include from ServiceNow
3. **create_script_include** - Create a new script include in ServiceNow
4. **update_script_include** - Update an existing script include in ServiceNow
5. **delete_script_include** - Delete a script include from ServiceNow

#### Changeset Management Tools

1. **list_changesets** - List changesets from ServiceNow with filtering options
2. **get_changeset_details** - Get detailed information about a specific changeset
3. **create_changeset** - Create a new changeset in ServiceNow
4. **update_changeset** - Update an existing changeset
5. **commit_changeset** - Commit a changeset
6. **publish_changeset** - Publish a changeset
7. **add_file_to_changeset** - Add a file to a changeset

#### Knowledge Base Management Tools

1. **create_knowledge_base** - Create a new knowledge base in ServiceNow
2. **list_knowledge_bases** - List knowledge bases with filtering options
3. **create_category** - Create a new category in a knowledge base
4. **create_article** - Create a new knowledge article in ServiceNow
5. **update_article** - Update an existing knowledge article in ServiceNow
6. **publish_article** - Publish a knowledge article in ServiceNow
7. **list_articles** - List knowledge articles with filtering options
8. **get_article** - Get a specific knowledge article by ID

#### User Management Tools

1. **create_user** - Create a new user in ServiceNow
2. **update_user** - Update an existing user in ServiceNow
3. **get_user** - Get a specific user by ID, username, or email
4. **list_users** - List users with filtering options
5. **create_group** - Create a new group in ServiceNow
6. **update_group** - Update an existing group in ServiceNow
7. **add_group_members** - Add members to a group in ServiceNow
8. **remove_group_members** - Remove members from a group in ServiceNow
9. **list_groups** - List groups with filtering options

#### UI Policy Tools

1. **create_ui_policy** - Creates a ServiceNow UI Policy, typically for a Catalog Item.
2. **create_ui_policy_action** - Creates an action associated with a UI Policy to control variable states (visibility, mandatory, etc.).


#### Developer Toolbox Tools

1. **create_ui_action** - Create a new UI action in ServiceNow with specified configuration
2. **update_ui_action** - Update an existing UI action's properties and behavior
3. **list_ui_actions** - List UI actions with filtering by table, active status, and search queries
4. **get_ui_action** - Retrieve detailed information about a specific UI action
5. **delete_ui_action** - Remove a UI action from ServiceNow

6. **create_inbound_email_action** - Create a new inbound email action
7. **update_inbound_email_action** - Update an existing inbound email action
8. **list_inbound_email_actions** - List and search inbound email actions
9. **get_inbound_email_action** - Get details of a specific inbound email action
10. **delete_inbound_email_action** - Delete an inbound email action

11. **create_table** - Create a new custom table
12. **create_table_column** - Create a new column in a table
13. **update_table** - Update an existing table
14. **update_table_column** - Update an existing table column
14. **list_tables** - List and search custom tables
16. **list_table_columns** - List columns in a specific table
17. **get_table** - Get details of a specific table
18. **get_table_column** - Get details of a specific table column

19. **create_choice** - Create a new choice for a choice field
20. **update_choice** - Update an existing choice option
21. **list_choices** - List all choices for a specific field
22. **get_choice** - Get details of a specific choice
23. **delete_choice** - Delete a choice option
24. **bulk_create_choices** - Create multiple choices at once
25. **reorder_choices** - Reorder choices by sequence

26. **create_assignment_rule** - Create a new assignment rule in ServiceNow
27. **update_assignment_rule** - Update an existing assignment rule
28. **list_assignment_rules** - List assignment rules with optional filtering
29. **get_assignment_rule** - Get details of a specific assignment rule
30. **delete_assignment_rule** - Delete an assignment rule from ServiceNow

31. **create_email_template** - Create a new email template in ServiceNow
32. **update_email_template** - Update an existing email template
33. **list_email_templates** - List email templates with optional filtering
34. **get_email_template** - Get details of a specific email template
35. **delete_email_template** - Delete an email template from ServiceNow
36. **clone_email_template** - Clone an existing email template

37. **create_image** - Create a new image in the db_image table with base64 encoded data
38. **update_image** - Update an existing image in the db_image table
39. **list_images** - List images from the db_image table with optional filtering
40. **get_image** - Get a specific image from the db_image table
41. **delete_image** - Delete an image from the db_image table

42. **create_service_catalog** - Create a new service catalog in the sc_catalog table
43. **update_service_catalog** - Update an existing service catalog in the sc_catalog table
44. **list_service_catalogs** - List service catalogs from the sc_catalog table with optional filtering
45. **get_service_catalog** - Get a specific service catalog from the sc_catalog table
46. **delete_service_catalog** - Delete a service catalog from the sc_catalog table

47. **upload_attachment** - Upload a file attachment using binary data to ServiceNow Attachment API
48. **upload_multipart_attachment** - Upload a file attachment using multipart form data
49. **list_attachments** - List attachments from ServiceNow Attachment API with optional filtering
50. **get_attachment** - Get attachment metadata from ServiceNow Attachment API
51. **download_attachment** - Download attachment binary data as base64 from ServiceNow
52. **delete_attachment** - Delete an attachment from ServiceNow Attachment API

53. **create_atf_test** - Create a new ATF (Automated Test Framework) test in ServiceNow
54. **update_atf_test** - Update an existing ATF test's properties and configuration
55. **get_atf_test** - Get detailed information about a specific ATF test
56. **list_atf_tests** - List ATF tests with optional filtering by name, application, and status
57. **delete_atf_test** - Delete an ATF test from ServiceNow
58. **run_atf_test** - Execute an ATF test and trigger test execution
59. **get_atf_test_results** - Get ATF test execution results and status

### Application Menu Items

1. **create_application_menu** - Create custom menu items that appear in the All menu and navigation areas
2. **update_application_menu** - Modify existing menu item properties including title, roles, order, and visibility
3. **list_application_menus** - List and filter menu items by category, device type, or active status
4. **get_application_menu** - Retrieve detailed information about a specific menu item
5. **delete_application_menu** - Remove menu items from the navigation interface

### Employee Center Quicklinks

1. **create_quick_link** - Create employee center quick links for Service Portal navigation
2. **update_quick_link** - Update existing employee center quick links
3. **list_quick_links** - List and filter employee center quick links  
4. **get_quick_link** - Get detailed information about specific quick links
5. **delete_quick_link** - Remove employee center quick links


#### Employee Center Widget Instance Management Tools

1. **create_widget_instance** - Create a new widget instance with specified configuration, styling, and placement parameters
2. **update_widget_instance** - Update an existing widget instance including configuration, styling, and placement properties  
3. **list_widget_instances** - List widget instances with optional filtering by widget, column, or active status
4. **get_widget_instance** - Get detailed information about a specific widget instance
5. **delete_widget_instance** - Delete a widget instance from portal pages
6. **clone_widget_instance** - Clone an existing widget instance with optional modifications to configuration and placement
7. **bulk_update_widget_instances** - Bulk update multiple widget instances simultaneously for efficient portal management


#### Portal UI Page Configuration Management Tools

1. **create_portal_page** - Create new portal pages in the sp_page table with configurable properties including title, CSS, roles, and visibility settings
2. **update_portal_page** - Update existing portal pages by ID or sys_id, modifying properties like title, CSS, roles, and other configuration options
3. **list_portal_pages** - List portal pages with optional filtering by category, public status, draft status, and other criteria
4. **get_portal_page** - Get detailed information about a specific portal page by ID or sys_id
5. **clone_portal_page** - Clone existing portal pages to create duplicates with optional modifications to title, description, CSS, and roles
6. **delete_portal_page** - Delete portal pages from the sp_page table by ID or sys_id


#### Portal UI Row Management Tools

1. **create_portal_row** - Create new portal rows in the sp_row table with configurable container, column, CSS class, order, and semantic tag properties
2. **update_portal_row** - Update existing portal rows by sys_id, modifying properties like container, column, CSS class, order, and semantic tag
3. **list_portal_rows** - List portal rows with optional filtering by container, column, semantic tag, and other criteria
4. **get_portal_row** - Get detailed information about a specific portal row by sys_id
5. **clone_portal_row** - Clone existing portal rows to create duplicates with optional modifications to container, column, CSS class, and semantic tag
6. **delete_portal_row** - Delete portal rows from the sp_row table by sys_id
7. **reorder_portal_rows** - Reorder portal rows within a container or column by updating their order values according to a specified sequence

#### Portal UI Column Management Tools

1. **create_portal_column** - Create new portal columns in the sp_column table with configurable row, CSS class, responsive Bootstrap sizes, order, and semantic tag properties
2. **update_portal_column** - Update existing portal columns by sys_id, modifying properties like row, CSS class, responsive sizes, order, and semantic tag
3. **list_portal_columns** - List portal columns with optional filtering by row, semantic tag, size ranges, and other criteria
4. **get_portal_column** - Get detailed information about a specific portal column by sys_id including responsive size configurations
5. **clone_portal_column** - Clone existing portal columns to create duplicates with optional modifications to row, CSS class, responsive sizes, and semantic tag
6. **delete_portal_column** - Delete portal columns from the sp_column table by sys_id
7. **reorder_portal_columns** - Reorder portal columns within a row by updating their order values according to a specified sequence
8. **create_responsive_grid** - Create responsive grid layouts by generating multiple columns with specified Bootstrap responsive configurations in a single operation

#### Portal Container Management Tools

1. **create_portal_container** - Create a new portal container with configurable page, styling, background, and layout properties
2. **update_portal_container** - Update an existing portal container's properties including styling, background, and layout settings
3. **list_portal_containers** - List portal containers with optional filtering by page, semantic tag, width, and other criteria
4. **get_portal_container** - Get detailed information about a specific portal container by sys_id or name
5. **clone_portal_container** - Clone an existing portal container with optional modifications to styling, background, and target page
6. **delete_portal_container** - Delete a portal container from the system
7. **reorder_portal_containers** - Reorder portal containers within a page by updating their sequence



### Using the MCP CLI

The ServiceNow MCP server can be installed with the MCP CLI, which provides a convenient way to register the server with Claude.

```bash
# Install the ServiceNow MCP server with environment variables from .env file
mcp install src/servicenow_mcp/server.py -f .env
```

This command will register the ServiceNow MCP server with Claude and configure it to use the environment variables from the .env file.

### Integration with Claude Desktop

To configure the ServiceNow MCP server in Claude Desktop:

1. Edit the Claude Desktop configuration file at `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the appropriate path for your OS:

```json
{
  "mcpServers": {
    "ServiceNow": {
      "command": "/Users/yourusername/dev/servicenow-mcp/.venv/bin/python",
      "args": [
        "-m",
        "servicenow_mcp.cli"
      ],
      "env": {
        "SERVICENOW_INSTANCE_URL": "https://your-instance.service-now.com",
        "SERVICENOW_USERNAME": "your-username",
        "SERVICENOW_PASSWORD": "your-password",
        "SERVICENOW_AUTH_TYPE": "basic"
      }
    }
  }
}
```

2. Restart Claude Desktop to apply the changes

### Example Usage with Claude

Below are some example natural language queries you can use with Claude to interact with ServiceNow via the MCP server:

#### Incident Management Examples
- "Create a new incident for a network outage in the east region"
- "Update the priority of incident INC0010001 to high"
- "Add a comment to incident INC0010001 saying the issue is being investigated"
- "Resolve incident INC0010001 with a note that the server was restarted"
- "List all high priority incidents assigned to the Network team"
- "List all active P1 incidents assigned to the Network team."

#### Service Catalog Examples
- "Show me all items in the service catalog"
- "List all service catalog categories"
- "Get details about the laptop request catalog item"
- "Show me all catalog items in the Hardware category"
- "Search for 'software' in the service catalog"
- "Create a new category called 'Cloud Services' in the service catalog"
- "Update the 'Hardware' category to rename it to 'IT Equipment'"
- "Move the 'Virtual Machine' catalog item to the 'Cloud Services' category"
- "Create a subcategory called 'Monitors' under the 'IT Equipment' category"
- "Reorganize our catalog by moving all software items to the 'Software' category"
- "Create a description field for the laptop request catalog item"
- "Add a dropdown field for selecting laptop models to catalog item"
- "List all form fields for the VPN access request catalog item"
- "Make the department field mandatory in the software request form"
- "Update the help text for the cost center field"
- "Show me all service catalogs in the system"
- "List all hardware catalog items."
- "Find the catalog item for 'New Laptop Request'."
- "Show me the variables for the 'New Laptop Request' item."
- "Create a new variable named 'department_code' for the 'New Hire Setup' catalog item. Make it a mandatory string field."

#### Catalog Optimization Examples
- "Analyze our service catalog and identify opportunities for improvement"
- "Find catalog items with poor descriptions that need improvement"
- "Identify catalog items with low usage that we might want to retire"
- "Find catalog items with high abandonment rates"
- "Optimize our Hardware category to improve user experience"

#### Change Management Examples
- "Create a change request for server maintenance to apply security patches tomorrow night"
- "Schedule a database upgrade for next Tuesday from 2 AM to 4 AM"
- "Add a task to the server maintenance change for pre-implementation checks"
- "Submit the server maintenance change for approval"
- "Approve the database upgrade change with comment: implementation plan looks thorough"
- "Show me all emergency changes scheduled for this week"
- "List all changes assigned to the Network team"
- "Create a normal change request to upgrade the production database server."
- "Update change CHG0012345, set the state to 'Implement'."

#### Agile Management Examples
- "Create a new user story for implementing a new reporting dashboard"
- "Update the 'Implement a new reporting dashboard' story to set it as blocked"
- "List all user stories assigned to the Data Analytics team"
- "Create a dependency between the 'Implement a new reporting dashboard' story and the 'Develop data extraction pipeline' story"
- "Delete the dependency between the 'Implement a new reporting dashboard' story and the 'Develop data extraction pipeline' story"
- "Create a new epic called 'Data Analytics Initiatives'"
- "Update the 'Data Analytics Initiatives' epic to set it as completed"
- "List all epics in the 'Data Analytics' project"
- "Create a new scrum task for the 'Implement a new reporting dashboard' story"
- "Update the 'Develop data extraction pipeline' scrum task to set it as completed"
- "List all scrum tasks in the 'Implement a new reporting dashboard' story"
- "Create a new project called 'Data Analytics Initiatives'"
- "Update the 'Data Analytics Initiatives' project to set it as completed"
- "List all projects in the 'Data Analytics' epic"

#### Workflow Management Examples
- "Show me all active workflows in ServiceNow"
- "Get details about the incident approval workflow"
- "List all versions of the change request workflow"
- "Show me all activities in the service catalog request workflow"
- "Create a new workflow for handling software license requests"
- "Update the description of the incident escalation workflow"
- "Activate the new employee onboarding workflow"
- "Deactivate the old password reset workflow"
- "Add an approval activity to the software license request workflow"
- "Update the notification activity in the incident escalation workflow"
- "Delete the unnecessary activity from the change request workflow"
- "Reorder the activities in the service catalog request workflow"

#### Changeset Management Examples
- "List all changesets in ServiceNow"
- "Show me all changesets created by developer 'john.doe'"
- "Get details about changeset 'sys_update_set_123'"
- "Create a new changeset for the 'HR Portal' application"
- "Update the description of changeset 'sys_update_set_123'"
- "Commit changeset 'sys_update_set_123' with message 'Fixed login issue'"
- "Publish changeset 'sys_update_set_123' to production"
- "Add a file to changeset 'sys_update_set_123'"
- "Show me all changes in changeset 'sys_update_set_123'"

#### Knowledge Base Examples
- "Create a new knowledge base for the IT department"
- "List all knowledge bases in the organization"
- "Create a category called 'Network Troubleshooting' in the IT knowledge base"
- "Write an article about VPN setup in the Network Troubleshooting category"
- "Update the VPN setup article to include mobile device instructions"
- "Publish the VPN setup article so it's visible to all users"
- "List all articles in the Network Troubleshooting category"
- "Show me the details of the VPN setup article"
- "Find knowledge articles containing 'password reset' in the IT knowledge base"
- "Create a subcategory called 'Wireless Networks' under the Network Troubleshooting category"

#### User Management Examples
- "Create a new user Dr. Alice Radiology in the Radiology department"
- "Update Bob's user record to make him the manager of Alice"
- "Assign the ITIL role to Bob so he can approve change requests"
- "List all users in the Radiology department"
- "Create a new group called 'Biomedical Engineering' for managing medical devices"
- "Add an admin user to the Biomedical Engineering group as a member"
- "Update the Biomedical Engineering group to change its manager"
- "Remove a user from the Biomedical Engineering group"
- "Find all active users in the system with 'doctor' in their title"
- "Create a user that will act as an approver for the Radiology department"
- "List all IT support groups in the system"

#### UI Policy Examples
- "Create a UI policy for the 'Software Request' item (sys_id: abc...) named 'Show Justification' that applies when 'software_cost' is greater than 100."
- "For the UI policy 'Show Justification' (sys_id: def...), add an action to make the 'business_justification' variable visible and mandatory."
- "Create another action for policy 'Show Justification' to hide the 'alternative_software' variable."

#### Developer Toolbox Examples
- "Create a UI action on the incident table that sets the state to resolved"
- "Show me all UI actions for the change_request table"
- "Update the 'Quick Approve' UI action to include a confirmation dialog"
- "Create a list banner button that allows bulk assignment of incidents"
- "Find all inactive UI actions across all tables"
- "Delete the UI action with sys_id abc123def456"
- "Create a form button that only appears for users with the admin role"
- "List all UI actions that contain 'approval' in their name or action text"


#### Inbound Email Action Management Examples
- "Create an email action that creates incidents from support emails"
- "Update the email processing script for the incident creation action"
- "Show me all active inbound email actions"
- "Find email actions that process emails for the incident table"
- "Delete the old email routing action"
- "Get the details of the support email processing action"

#### Table Management Examples
- "Create a custom table for tracking company assets"
- "Add a new column to the asset tracking table for serial numbers"
- "Show me all custom tables in the system"
- "List all columns in the incident table"
- "Update the asset table to make the asset type field mandatory"
- "Get the details of the custom project tracking table"
- "Create a reference field that links to the user table"
- "Add a choice field with predefined options for priority levels"

#### Application Menu Examples
- "Create a menu item for custom reports that only admins and report viewers can access"
- "Add a new menu entry for field service tools optimized for mobile devices"
- "List all active menu items in the reporting category"
- "Update the asset management menu to appear first in the navigation"
- "Show me the configuration for the executive dashboard menu item"
- "Delete the old system tools menu that's no longer needed"
- "Create a menu for help desk that appears in the service management category"
- "Add a menu item for data analytics that requires analyst role"
- "Find all menu items that are available on mobile devices"
- "Set up a menu entry for the new project tracking application"

#### Assignment Rule Management Examples
- "Create an assignment rule that assigns P1 incidents to the senior support team"
- "List all assignment rules for the incident table"
- "Update the VIP assignment rule to include new criteria"
- "Show me all inactive assignment rules that need cleanup"
- "Create a round-robin assignment rule for distributing tasks evenly"
- "Delete the old assignment rule that's no longer needed"
- "Get the details of the after-hours assignment rule"
- "Create an assignment rule that routes tickets based on location"
- "Update the assignment rule order to prioritize VIP customers first"
- "Find all assignment rules that execute synchronously"

#### Email Template Management Examples
- "Create an email template for incident resolution notifications"
- "List all email templates in the incident category"
- "Update the welcome email template with new branding"
- "Clone the change approval template for emergency changes"
- "Show me all inactive email templates that need cleanup"

#### Image Management Examples
- "Upload a company logo image to ServiceNow"
- "List all images associated with the user table"
- "Update the image name for image ID 12345"
- "Get the base64 data for an image"
- "Delete an unused image from the system"
- "Find all PNG images that contain 'logo' in the name"

#### Service Catalog Management Examples
- "Create a new service catalog for HR services"
- "List all active service catalogs"
- "Update the IT catalog to enable wish list functionality"
- "Get details for the catalog with ID 12345"
- "Delete the unused training catalog"
- "Show me all catalogs available on mobile"

#### ATF (Automated Test Framework) Examples
- "Create a new ATF test called 'User Login Validation Test'"
- "List all active ATF tests for the incident management application"
- "Show me ATF tests that contain 'login' in their name"
- "Run the ATF test with ID abc123def456"
- "Get the results of the last ATF test execution"
- "Update the ATF test description to include new validation steps"
- "Delete the obsolete ATF test for the old workflow"
- "Find all ATF tests that are currently inactive"
- "Execute all ATF tests for the customer service portal"
- "Show me the execution history for test ID xyz789"

#### Attachment Management Examples
- "Upload this screenshot to the incident record"
- "List all PDF attachments on change requests"
- "Download the attachment with ID 12345 as base64"
- "Delete the old attachment from this ticket"
- "Show me all image attachments larger than 1MB"
- "Upload this document to the knowledge article"
- "Delete the old notification template that's no longer used"
- "Get the details of the escalation email template"
- "Create a template for user account creation notifications"
- "Update the template to include mobile-friendly HTML formatting"
- "Find all email templates that contain specific variables"

#### Employee Center Quick Link Management Examples
- "Create a quick link to the employee handbook knowledge article"
- "List all active quick links in the employee center"
- "Update the IT support quick link to point to a new catalog item"
- "Delete the outdated training portal quick link"
- "Show me details for the benefits enrollment quick link"


#### Employee Center Widget Instance Management Examples
- "Create a new widget instance for the employee dashboard using the 'Quick Actions' widget"
- "Update all widget instances in the main column to use the primary color scheme"
- "List all widget instances that are currently inactive on the Employee Center"
- "Clone the 'Popular Knowledge Articles' widget instance to the sidebar column"
- "Show me the configuration details for widget instance XYZ123"
- "Delete the outdated 'Legacy Tools' widget instance from the portal"
- "Bulk update all announcement widgets to use the warning color and large size"
- "Find all widget instances that reference the 'Incident Reporter' widget"
- "Create a widget instance with custom parameters for showing only high-priority tickets"
- "Update the widget instance order to move 'Quick Links' to the top of the column"


#### Portal UI Page Configuration Management Examples

- "Create a new portal page called 'employee_dashboard' with admin role access"
- "Clone the homepage and create a development version"
- "List all public portal pages that are not in draft mode"
- "Update the CSS styling for the customer portal page"
- "Show me all portal pages in the 'custom' category"
- "Delete the old_landing_page portal page"
- "Create a public landing page with custom CSS and no role restrictions"
- "Find the portal page with ID 'service_catalog' and show its configuration"
- "Make the employee_portal page internal and add the 'employee' role"
- "Clone the customer_support page but don't copy the CSS styling"


#### Portal UI Row Management Examples

- "Create a new portal row in container ABC123 with CSS class 'hero-section'"
- "Clone the header row and move it to a different container"
- "List all rows in the homepage container ordered by their sequence"
- "Update the CSS class of row XYZ789 to 'updated-layout'"
- "Show me all portal rows that use the 'section' semantic tag"
- "Delete the old footer row that's no longer needed"
- "Reorder the rows in container ABC123 to put the navigation row first"
- "Create a new row with semantic tag 'main' and order it after the header"
- "Find the portal row with sys_id DEF456 and show its configuration"
- "Move row GHI789 from one container to another container"

#### Portal UI Column Management Examples

- "Create a new portal column in row ABC123 with Bootstrap size 6 for medium devices and size 12 for mobile"
- "Clone the sidebar column and move it to a different row with updated responsive sizes"
- "List all columns in the homepage row that are wider than 6 grid units"
- "Update the column XYZ789 to use semantic tag 'aside' and CSS class 'sidebar-widget'"
- "Show me all portal columns that use responsive breakpoints"
- "Delete the unused column that's no longer needed"
- "Reorder the columns in row ABC123 to put the main content column first"
- "Create a responsive grid with three equal columns that stack on mobile devices"
- "Find the portal column with sys_id DEF456 and show its Bootstrap size configuration"
- "Create a two-column layout with 8/4 split for desktop and stacked for mobile"

#### Portal Container Management Examples
- "Create a new main content container for the homepage with container-fluid width"
- "List all containers on the employee portal homepage"
- "Clone the header container from the main page to the help page"
- "Update the background color of the hero section container to blue"
- "Reorder the containers on the landing page so the testimonials come before the features"
- "Show me the configuration details for the footer container"
- "Delete the unused promotional banner container"
- "Create a new section container with semantic tag 'aside' for the sidebar content"

### Example Scripts

The repository includes example scripts that demonstrate how to use the tools:

- **examples/catalog_optimization_example.py**: Demonstrates how to analyze and improve the ServiceNow Service Catalog
- **examples/change_management_demo.py**: Shows how to create and manage change requests in ServiceNow

## Authentication Methods

### Basic Authentication

```
SERVICENOW_AUTH_TYPE=basic
SERVICENOW_USERNAME=your-username
SERVICENOW_PASSWORD=your-password
```

### OAuth Authentication

```
SERVICENOW_AUTH_TYPE=oauth
SERVICENOW_CLIENT_ID=your-client-id
SERVICENOW_CLIENT_SECRET=your-client-secret
SERVICENOW_TOKEN_URL=https://your-instance.service-now.com/oauth_token.do
```

### API Key Authentication

```
SERVICENOW_AUTH_TYPE=api_key
SERVICENOW_API_KEY=your-api-key
```

## Development

### Documentation

Additional documentation is available in the `docs` directory:

- [Catalog Integration](docs/catalog.md) - Detailed information about the Service Catalog integration
- [Catalog Optimization](docs/catalog_optimization_plan.md) - Detailed plan for catalog optimization features
- [Change Management](docs/change_management.md) - Detailed information about the Change Management tools
- [Workflow Management](docs/workflow_management.md) - Detailed information about the Workflow Management tools
- [Changeset Management](docs/changeset_management.md) - Detailed information about the Changeset Management tools

### Troubleshooting

#### Common Errors with Change Management Tools

1. **Error: `argument after ** must be a mapping, not CreateChangeRequestParams`**
   - This error occurs when you pass a `CreateChangeRequestParams` object instead of a dictionary to the `create_change_request` function.
   - Solution: Make sure you're passing a dictionary with the parameters, not a Pydantic model object.
   - Note: The change management tools have been updated to handle this error automatically. The functions will now attempt to unwrap parameters if they're incorrectly wrapped or passed as a Pydantic model object.

2. **Error: `Missing required parameter 'type'`**
   - This error occurs when you don't provide all required parameters for creating a change request.
   - Solution: Make sure to include all required parameters. For `create_change_request`, both `short_description` and `type` are required.

3. **Error: `Invalid value for parameter 'type'`**
   - This error occurs when you provide an invalid value for the `type` parameter.
   - Solution: Use one of the valid values: "normal", "standard", or "emergency".

4. **Error: `Cannot find get_headers method in either auth_manager or server_config`**
   - This error occurs when the parameters are passed in the wrong order or when using objects that don't have the required methods.
   - Solution: Make sure you're passing the `auth_manager` and `server_config` parameters in the correct order. The functions have been updated to handle parameter swapping automatically.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the LICENSE file for details.

