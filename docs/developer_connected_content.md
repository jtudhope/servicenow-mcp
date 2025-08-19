# Connected Content Management in ServiceNow MCP

## Overview

The Connected Content tools provide comprehensive management of content relationships in ServiceNow. These relationships are stored in the `m2m_connected_content` table and serve as many-to-many connections between topics and various content types like knowledge articles, catalog items, and quick links. This enables structured content organization and improves content discoverability through topic-based navigation.

## Tools

### create_connected_content

Create a new connected content relationship in the m2m_connected_content table to link topics with various content types.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic | string | Yes | Topic sys_id (required) |
| content_type | string | Yes | Content type configuration sys_id (required) |
| catalog_item | string | No | Catalog item sys_id for catalog content connections |
| knowledge | string | No | Knowledge article sys_id for knowledge content connections |
| quick_link | string | No | Quick link sys_id for quick link content connections |
| order | integer | No | Display order for the connection (default: 100) |
| popularity | float | No | Popularity score for the content |
| content_display_value | string | No | Display value for the connected content |
| alphabetical_order | integer | No | Alphabetical ordering value |
| sys_domain | string | No | Domain for the connection (default: "global") |
| sys_domain_path | string | No | Domain path for the connection (default: "/") |

#### Example

```python
# Example usage of create_connected_content
result = create_connected_content({
    "topic": "a1b2c3d4e5f6000001c9dd3394009c96",
    "content_type": "knowledge_article_type_sys_id",
    "knowledge": "b2c3d4e5f6a7000001c9dd3394009c97",
    "order": 1,
    "popularity": 85.5,
    "content_display_value": "Cloud Security Best Practices"
})
```

#### Response

The tool returns a ConnectedContentResponse with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created connection data including sys_id and all fields |

### update_connected_content

Update an existing connected content relationship in the m2m_connected_content table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| connection_id | string | Yes | Connected content relationship sys_id |
| order | integer | No | Updated display order |
| popularity | float | No | Updated popularity score |
| content_display_value | string | No | Updated display value |
| alphabetical_order | integer | No | Updated alphabetical ordering |

#### Example

```python
# Example usage of update_connected_content
result = update_connected_content({
    "connection_id": "c3d4e5f6a7b8000001c9dd3394009c98",
    "order": 2,
    "popularity": 90.0,
    "content_display_value": "Enhanced Cloud Security Guide"
})
```

### list_connected_content

List connected content relationships from the m2m_connected_content table with filtering and pagination options.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of connections to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| topic | string | No | Filter by topic sys_id |
| content_type | string | No | Filter by content type sys_id |
| catalog_item | string | No | Filter by catalog item sys_id |
| knowledge | string | No | Filter by knowledge article sys_id |
| quick_link | string | No | Filter by quick link sys_id |
| sys_domain | string | No | Filter by domain |
| query | string | No | Additional query string |

#### Example

```python
# Example usage of list_connected_content
result = list_connected_content({
    "limit": 20,
    "topic": "a1b2c3d4e5f6000001c9dd3394009c96",
    "content_type": "knowledge_article_type_sys_id",
    "offset": 0
})
```

#### Response

Returns a dictionary with:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| connections | array | List of connected content objects |
| total | integer | Total number of connections returned |
| limit | integer | Limit used for the query |
| offset | integer | Offset used for the query |

### get_connected_content

Get a specific connected content relationship from the m2m_connected_content table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| connection_id | string | Yes | Connected content relationship sys_id |

#### Example

```python
# Example usage of get_connected_content
result = get_connected_content({
    "connection_id": "c3d4e5f6a7b8000001c9dd3394009c98"
})
```

### delete_connected_content

Delete a connected content relationship from the m2m_connected_content table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| connection_id | string | Yes | Connected content relationship sys_id |

#### Example

```python
# Example usage of delete_connected_content
result = delete_connected_content({
    "connection_id": "c3d4e5f6a7b8000001c9dd3394009c98"
})
```

### bulk_connect_content

Bulk connect multiple content items to a topic in the m2m_connected_content table for efficient content organization.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic | string | Yes | Topic sys_id to connect content to |
| connections | array | Yes | List of content connections to create |

Each connection in the `connections` array should include:
- `content_type` (required): Content type configuration sys_id
- `catalog_item`, `knowledge`, or `quick_link`: Content reference
- `order`, `popularity`, `content_display_value`, `alphabetical_order`: Optional metadata

#### Example

```python
# Example usage of bulk_connect_content
result = bulk_connect_content({
    "topic": "a1b2c3d4e5f6000001c9dd3394009c96",
    "connections": [
        {
            "content_type": "knowledge_article_type_sys_id",
            "knowledge": "kb_article_1_sys_id",
            "order": 1,
            "popularity": 85.0
        },
        {
            "content_type": "catalog_item_type_sys_id", 
            "catalog_item": "catalog_item_1_sys_id",
            "order": 2,
            "popularity": 75.0
        },
        {
            "content_type": "quick_link_type_sys_id",
            "quick_link": "quick_link_1_sys_id",
            "order": 3,
            "popularity": 90.0
        }
    ]
})
```

#### Response

Returns a ConnectedContentResponse with:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the overall result |
| data | object | Bulk operation results including success/failure counts and details |

## Common Use Cases

### Knowledge Article Topic Organization

Connect knowledge articles to relevant topics for better content discovery:

```python
# Connect knowledge articles to a security topic
result = create_connected_content({
    "topic": "security_topic_sys_id",
    "content_type": "knowledge_article_type_sys_id", 
    "knowledge": "security_kb_article_sys_id",
    "order": 1,
    "popularity": 88.5,
    "content_display_value": "Multi-Factor Authentication Setup Guide"
})
```

### Service Catalog Topic Mapping

Link catalog items to topics for organized service browsing:

```python
# Connect IT services to relevant topics
result = create_connected_content({
    "topic": "it_services_topic_sys_id",
    "content_type": "catalog_item_type_sys_id",
    "catalog_item": "laptop_request_item_sys_id", 
    "order": 2,
    "popularity": 92.0,
    "content_display_value": "Business Laptop Request"
})
```

### Quick Link Topic Association

Associate quick links with topics for streamlined navigation:

```python
# Connect quick links to a training topic
result = create_connected_content({
    "topic": "training_topic_sys_id",
    "content_type": "quick_link_type_sys_id",
    "quick_link": "training_portal_link_sys_id",
    "order": 1,
    "popularity": 95.0,
    "content_display_value": "Employee Training Portal"
})
```

### Bulk Content Organization

Efficiently organize multiple content items under a topic:

```python
# Bulk connect various cloud-related content to a cloud computing topic
result = bulk_connect_content({
    "topic": "cloud_computing_topic_sys_id",
    "connections": [
        {
            "content_type": "knowledge_article_type_sys_id",
            "knowledge": "aws_guide_kb_sys_id",
            "order": 1,
            "popularity": 88.0,
            "content_display_value": "AWS Best Practices Guide"
        },
        {
            "content_type": "catalog_item_type_sys_id",
            "catalog_item": "cloud_storage_request_sys_id", 
            "order": 2,
            "popularity": 85.0,
            "content_display_value": "Cloud Storage Request"
        },
        {
            "content_type": "quick_link_type_sys_id",
            "quick_link": "cloud_dashboard_link_sys_id",
            "order": 3,
            "popularity": 92.0,
            "content_display_value": "Cloud Services Dashboard"
        }
    ]
})
```

### Topic-Based Content Curation

Create curated content collections for specific audiences:

```python
# Create executive dashboard content connections
result = bulk_connect_content({
    "topic": "executive_dashboard_topic_sys_id",
    "connections": [
        {
            "content_type": "knowledge_article_type_sys_id",
            "knowledge": "quarterly_review_kb_sys_id",
            "order": 1,
            "popularity": 95.0,
            "content_display_value": "Quarterly Business Review Template"
        },
        {
            "content_type": "quick_link_type_sys_id", 
            "quick_link": "analytics_portal_sys_id",
            "order": 2,
            "popularity": 90.0,
            "content_display_value": "Business Analytics Portal"
        }
    ]
})
```

## Best Practices

1. **Content Type Consistency** - Use appropriate content type configurations for each connection type
2. **Meaningful Ordering** - Set order values to create logical content sequences within topics
3. **Popularity Tracking** - Use popularity scores to highlight the most useful content
4. **Display Values** - Provide clear, descriptive display values for better user experience
5. **Domain Management** - Use proper domain settings for multi-domain environments
6. **Bulk Operations** - Use bulk_connect_content for efficient mass content organization
7. **Regular Maintenance** - Periodically review and update connections to maintain relevance

## Content Type Management

The content_type parameter refers to configuration records that define:
- What type of content can be connected (knowledge, catalog items, quick links)
- Display properties and behavior
- Access controls and visibility rules
- Integration with portal navigation

Common content types include:
- Knowledge article content types
- Catalog item content types  
- Quick link content types
- Custom content type configurations

## Integration with ServiceNow Features

Connected content integrates with various ServiceNow modules:

- **Knowledge Management** - Topic-based knowledge article organization
- **Service Catalog** - Topic-driven catalog browsing and discovery
- **Service Portal** - Topic navigation and content recommendations
- **Search** - Enhanced content findability through topic associations
- **Analytics** - Content usage tracking and popularity metrics
- **Workflow** - Automated content connections based on rules

## Topic Hierarchy and Content

Connected content works with topic hierarchies to provide:
- Inherited content from parent topics
- Scoped content visibility based on topic access controls
- Cascading content recommendations
- Hierarchical content organization

## Performance Considerations

For optimal performance:
- Use bulk operations for multiple connections
- Index on frequently queried fields (topic, content_type)
- Consider pagination for large result sets
- Cache popular content connections
- Monitor connection counts per topic

## Error Handling

All connected content tools return structured responses with success indicators:

```python
if result["success"]:
    print(f"Operation successful: {result['message']}")
    # Process result data
    connection_data = result.get("data", {})
    print(f"Connection ID: {connection_data.get('sys_id')}")
else:
    print(f"Operation failed: {result['message']}")
    # Handle error appropriately
```

## Troubleshooting

Common issues and solutions:

1. **Invalid content references** - Verify that knowledge, catalog_item, or quick_link sys_ids exist
2. **Content type mismatches** - Ensure content_type configuration matches the content being connected
3. **Domain access issues** - Check domain permissions and sys_domain settings
4. **Duplicate connections** - The system may prevent duplicate topic-content combinations
5. **Order conflicts** - Use unique order values or allow system auto-ordering
6. **Popularity validation** - Ensure popularity scores are within acceptable ranges

## Example Natural Language Commands for Claude

- "Connect this knowledge article about password policies to the security topic"
- "List all content connected to the IT services topic"
- "Bulk connect these three catalog items to the employee onboarding topic"
- "Update the popularity score for the cloud storage connection to 95"
- "Show me all quick links connected to the training topic"
- "Remove the connection between the outdated guide and the best practices topic"
- "Create connections between the new product documentation and relevant topics"

## Advanced Usage

### Content Recommendation Engine

```python
# Get popular content for a topic to build recommendations
result = list_connected_content({
    "topic": "target_topic_sys_id",
    "limit": 10,
    "query": "popularity>80^ORDERBYDESCpopularity"
})

# Use results to display top recommended content
```

### Content Migration Between Topics

```python
# Move content connections from one topic to another
old_connections = list_connected_content({
    "topic": "old_topic_sys_id"
})

new_connections = []
for conn in old_connections["connections"]:
    new_connections.append({
        "content_type": conn["content_type"],
        "knowledge": conn.get("knowledge"),
        "catalog_item": conn.get("catalog_item"), 
        "quick_link": conn.get("quick_link"),
        "order": conn["order"],
        "popularity": conn["popularity"]
    })

# Bulk create connections for new topic
bulk_result = bulk_connect_content({
    "topic": "new_topic_sys_id",
    "connections": new_connections
})
```

The connected content tools provide a powerful foundation for organizing and managing content relationships in ServiceNow, enabling sophisticated content discovery and topic-based navigation experiences.