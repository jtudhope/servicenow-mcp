# Topic Management in ServiceNow MCP

## Overview

The Topic tools provide comprehensive management of knowledge topics in ServiceNow. These topics are stored in the `topic` table and serve as labels or categories that can be attached to content to make it easier to find, filter, and organize. In ServiceNow, topics enable structured content organization through hierarchical classification and user-based access controls.

## Tools

### create_topic

Create a new topic in the topic table for knowledge and community content organization.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the topic (required) |
| taxonomy | string | Yes | Taxonomy sys_id that this topic belongs to (required) |
| description | string | No | Description of the topic |
| parent_topic | string | No | Parent topic sys_id for hierarchical structure |
| order | integer | No | Display order within the taxonomy |
| active | boolean | No | Whether the topic is active (default: true) |
| topic_based_navigation | boolean | No | Enable topic-based navigation (default: false) |
| icon_url | string | No | URL for the topic icon |
| banner_image_url | string | No | URL for the topic banner image |
| topic_manager | string | No | Comma-separated list of user criteria sys_ids for topic managers |
| topic_contributor | string | No | Comma-separated list of user criteria sys_ids for topic contributors |
| available_for | string | No | Comma-separated list of user criteria sys_ids for who can see this topic |
| not_available_for | string | No | Comma-separated list of user criteria sys_ids for who cannot see this topic |
| enable_user_criteria_check | boolean | No | Enable user criteria checking for visibility (default: false) |
| template | string | No | Service Portal page template sys_id |
| apply_to_child_topics | boolean | No | Apply template settings to child topics (default: false) |

#### Example

```python
# Example usage of create_topic
result = create_topic({
    "name": "Cloud Infrastructure",
    "taxonomy": "a1b2c3d4e5f6000001c9dd3394009c96",
    "description": "Topics related to cloud computing and infrastructure services",
    "active": true,
    "topic_based_navigation": true,
    "icon_url": "https://example.com/cloud-icon.png",
    "topic_manager": "cloud_managers_criteria_id"
})
```

#### Response

The tool returns a TopicResponse with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created topic data including sys_id and all fields |

### update_topic

Update an existing topic in the topic table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic_id | string | Yes | Topic sys_id |
| name | string | No | Updated name of the topic |
| description | string | No | Updated description |
| parent_topic | string | No | Updated parent topic sys_id |
| order | integer | No | Updated display order |
| active | boolean | No | Updated active status |
| topic_based_navigation | boolean | No | Updated topic-based navigation setting |
| icon_url | string | No | Updated icon URL |
| banner_image_url | string | No | Updated banner image URL |
| topic_manager | string | No | Updated topic managers |
| topic_contributor | string | No | Updated topic contributors |
| available_for | string | No | Updated available for criteria |
| not_available_for | string | No | Updated not available for criteria |
| enable_user_criteria_check | boolean | No | Updated user criteria check setting |
| template | string | No | Updated template |
| apply_to_child_topics | boolean | No | Updated apply to child topics setting |

#### Example

```python
# Example usage of update_topic
result = update_topic({
    "topic_id": "b2c3d4e5f6a7000001c9dd3394009c97",
    "description": "Enhanced cloud infrastructure topics including containers and serverless",
    "topic_based_navigation": true,
    "banner_image_url": "https://example.com/cloud-banner.jpg"
})
```

### list_topics

List topics from the topic table with filtering and pagination options.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of topics to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| taxonomy | string | No | Filter by taxonomy sys_id |
| parent_topic | string | No | Filter by parent topic sys_id |
| active | boolean | No | Filter by active status |
| name_contains | string | No | Filter by name containing text |
| topic_based_navigation | boolean | No | Filter by topic-based navigation setting |
| query | string | No | Additional query string |

#### Example

```python
# Example usage of list_topics
result = list_topics({
    "limit": 20,
    "taxonomy": "a1b2c3d4e5f6000001c9dd3394009c96",
    "active": true,
    "name_contains": "cloud",
    "offset": 0
})
```

#### Response

Returns a dictionary with:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| topics | array | List of topic objects |
| total | integer | Total number of topics returned |
| limit | integer | Limit used for the query |
| offset | integer | Offset used for the query |

### get_topic

Get a specific topic from the topic table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic_id | string | Yes | Topic sys_id or name |

#### Example

```python
# Example usage of get_topic
result = get_topic({
    "topic_id": "b2c3d4e5f6a7000001c9dd3394009c97"
})
```

### delete_topic

Delete a topic from the topic table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic_id | string | Yes | Topic sys_id |

#### Example

```python
# Example usage of delete_topic
result = delete_topic({
    "topic_id": "b2c3d4e5f6a7000001c9dd3394009c97"
})
```

### clone_topic

Clone an existing topic to create a duplicate with a new name.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic_id | string | Yes | Source topic sys_id |
| new_name | string | Yes | Name for the cloned topic |
| new_description | string | No | Description for the cloned topic |
| new_taxonomy | string | No | Taxonomy for the cloned topic (defaults to source taxonomy) |

#### Example

```python
# Example usage of clone_topic
result = clone_topic({
    "topic_id": "b2c3d4e5f6a7000001c9dd3394009c97",
    "new_name": "Cloud Infrastructure - Development",
    "new_description": "Development environment version of cloud infrastructure topics",
    "new_taxonomy": "dev_taxonomy_sys_id"
})
```

## Common Use Cases

### Knowledge Article Categorization

Create topics for organizing knowledge articles by technology area:

```python
# Create technology-focused topics
result = create_topic({
    "name": "Artificial Intelligence",
    "taxonomy": "tech_taxonomy_id",
    "description": "Topics related to AI, machine learning, and automation",
    "active": true,
    "topic_based_navigation": true,
    "icon_url": "https://example.com/ai-icon.png"
})
```

### Community Forum Organization

Structure community discussions with hierarchical topics:

```python
# Create main category topic
result = create_topic({
    "name": "IT Support",
    "taxonomy": "forum_taxonomy_id",
    "description": "General IT support discussions and solutions",
    "topic_based_navigation": true
})

# Create subtopic under main category
result = create_topic({
    "name": "Network Issues",
    "taxonomy": "forum_taxonomy_id",
    "parent_topic": "it_support_topic_sys_id",
    "description": "Network connectivity and configuration problems",
    "order": 1
})
```

### Department-Specific Content Organization

Create access-controlled topics for department-specific content:

```python
# Create HR-specific topic with access controls
result = create_topic({
    "name": "HR Policies",
    "taxonomy": "dept_taxonomy_id",
    "description": "Human resources policies and procedures",
    "available_for": "hr_department_criteria_id",
    "not_available_for": "contractor_criteria_id",
    "enable_user_criteria_check": true,
    "topic_manager": "hr_managers_criteria_id"
})
```

### Product Documentation Structure

Organize product documentation with templates:

```python
# Create product topic with custom template
result = create_topic({
    "name": "Product API Documentation",
    "taxonomy": "product_taxonomy_id",
    "description": "API documentation and developer resources",
    "template": "api_docs_template_id",
    "apply_to_child_topics": true,
    "topic_contributor": "developer_team_criteria_id"
})
```

### Event and Training Topics

Structure learning and event content:

```python
# Create training topic with navigation
result = create_topic({
    "name": "Security Training",
    "taxonomy": "training_taxonomy_id",
    "description": "Cybersecurity awareness and training materials",
    "topic_based_navigation": true,
    "banner_image_url": "https://example.com/security-banner.jpg",
    "available_for": "all_employees_criteria_id",
    "topic_manager": "security_team_criteria_id"
})
```

## Best Practices

1. **Use descriptive names** that clearly indicate the topic's content and scope
2. **Plan hierarchy carefully** - design parent-child relationships before creating topics
3. **Set appropriate access controls** using user criteria for sensitive topics
4. **Consistent taxonomy usage** - associate topics with appropriate taxonomies
5. **Regular maintenance** - review and update topic structures as content evolves
6. **Visual consistency** - use consistent icon and banner image styles
7. **Navigation optimization** - enable topic-based navigation for user-facing topics
8. **Template management** - use templates for consistent topic presentation
9. **Order management** - set meaningful order values for logical topic sequencing

## Topic Hierarchy Best Practices

When designing topic hierarchies:

1. **Logical grouping** - Group related content under parent topics
2. **Balanced depth** - Generally 2-4 levels maximum for usability
3. **Clear relationships** - Parent topics should logically contain child topics
4. **Avoid circular references** - Ensure no topic becomes its own ancestor
5. **Consistent naming** - Use consistent naming conventions across hierarchies
6. **Scalable structure** - Design with future growth in mind

## Access Control and User Criteria

Managing topic visibility:

1. **Available For** - Specify who can see and access the topic
2. **Not Available For** - Explicitly deny access to specific user groups
3. **Topic Managers** - Users who can manage topic content and settings
4. **Topic Contributors** - Users who can contribute content to the topic
5. **User Criteria Checking** - Enable to enforce access controls

```python
# Example of comprehensive access control
result = create_topic({
    "name": "Executive Communications",
    "taxonomy": "corp_taxonomy_id",
    "description": "Executive-level communications and announcements",
    "available_for": "executives_criteria_id,senior_managers_criteria_id",
    "not_available_for": "contractors_criteria_id,interns_criteria_id",
    "enable_user_criteria_check": true,
    "topic_manager": "executives_criteria_id",
    "topic_contributor": "communications_team_criteria_id"
})
```

## Integration with Other ServiceNow Features

Topics integrate with various ServiceNow modules:

- **Knowledge Management** - Categorize knowledge articles and content
- **Community Forums** - Organize discussion topics and threads
- **Service Portal** - Enable topic-based navigation and content discovery
- **Search** - Improve content searchability and filtering
- **Content Management** - Structure documents and media
- **Analytics** - Track content usage by topic
- **Workflow** - Trigger processes based on topic assignments

## Template Integration

Using templates with topics:

```python
# Create topic with template that applies to children
result = create_topic({
    "name": "API Documentation",
    "taxonomy": "dev_docs_taxonomy_id",
    "description": "API reference and developer guides",
    "template": "api_docs_template_id",
    "apply_to_child_topics": true,
    "topic_based_navigation": true
})
```

## Example Natural Language Commands for Claude

- "Create a topic for cloud security best practices in the IT taxonomy"
- "List all active topics under the training taxonomy with navigation enabled"
- "Update the AI/ML topic to include new machine learning subtopics"
- "Clone the production API documentation topic for the development environment"
- "Show me details of the customer support topic including its access controls"
- "Create a hierarchical topic structure for product documentation with proper templates"
- "Set up access-controlled topics for HR policies that only HR staff can see"

## Error Handling

All topic tools return structured responses with success indicators:

```python
if result["success"]:
    print(f"Operation successful: {result['message']}")
    # Process result data
    topic_data = result.get("data", {})
    print(f"Topic ID: {topic_data.get('sys_id')}")
    print(f"Topic Path: {topic_data.get('topic_path')}")
else:
    print(f"Operation failed: {result['message']}")
    # Handle error appropriately
```

## Troubleshooting

Common issues and solutions:

1. **Hierarchy errors** - Check parent topic exists and isn't creating circular references
2. **Access control issues** - Verify user criteria references are valid and active
3. **Template problems** - Ensure template sys_id exists and is compatible
4. **Taxonomy references** - Verify taxonomy sys_id is correct and accessible
5. **Navigation issues** - Check topic_based_navigation setting and portal configuration
6. **Order conflicts** - Ensure order values don't conflict with existing topics
7. **User criteria validation** - Test access controls with actual user accounts

## Advanced Usage

### Bulk Topic Creation

```python
# Create multiple related topics in a hierarchy
topics = [
    {
        "name": "DevOps",
        "taxonomy": "tech_taxonomy_id",
        "description": "DevOps practices and tools",
        "topic_based_navigation": true
    },
    {
        "name": "CI/CD",
        "taxonomy": "tech_taxonomy_id", 
        "parent_topic": "devops_topic_id",  # Set after creating parent
        "description": "Continuous integration and deployment",
        "order": 1
    },
    {
        "name": "Infrastructure as Code",
        "taxonomy": "tech_taxonomy_id",
        "parent_topic": "devops_topic_id",
        "description": "IaC tools and practices",
        "order": 2
    }
]

# Create parent first, then children
parent_result = create_topic(topics[0])
if parent_result["success"]:
    parent_id = parent_result["data"]["sys_id"]
    for child_topic in topics[1:]:
        child_topic["parent_topic"] = parent_id
        child_result = create_topic(child_topic)
```

### Topic Migration Strategy

```python
# Clone topic for environment migration
result = clone_topic({
    "topic_id": "prod_topic_id",
    "new_name": "Production Topic - Staging",
    "new_description": "Staging environment version",
    "new_taxonomy": "staging_taxonomy_id"
})
```

The topic tools provide a comprehensive foundation for organizing and managing knowledge content in ServiceNow, enabling structured information architecture and user-focused content discovery.