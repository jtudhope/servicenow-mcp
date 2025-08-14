# Attachment Management in ServiceNow MCP

## Overview

The Attachment Management tools provide functionality to manage file attachments using the ServiceNow Attachment API. These tools enable developers to upload, download, list, retrieve metadata, and delete file attachments associated with ServiceNow records. This is different from the Image Management tools as it uses the dedicated ServiceNow Attachment API rather than direct database table operations.

## Attachment Management Tools

### upload_attachment

Upload a file attachment using binary data to the ServiceNow Attachment API.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table to attach the file to |
| table_sys_id | string | Yes | Sys_id of the record to attach the file to |
| file_name | string | Yes | Name to give the attachment |
| file_data | string | Yes | Base64 encoded file data |
| content_type | string | Yes | Content type of the file (e.g., image/jpeg, image/png) |
| creation_time | string | No | Creation date and time of the attachment |
| encryption_context | string | No | Sys_id of an encryption context record |

#### Example

```python
result = upload_attachment({
    "table_name": "incident",
    "table_sys_id": "d71f7935c0a8016700802b64c67c11c6",
    "file_name": "screenshot.png",
    "file_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
    "content_type": "image/png"
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The attachment metadata including sys_id, download_link, size info, etc. |

### upload_multipart_attachment

Upload a file attachment using multipart form data to the ServiceNow Attachment API.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| table_name | string | Yes | Name of the table to attach the file to |
| table_sys_id | string | Yes | Sys_id of the record to attach the file to |
| file_name | string | Yes | Name to give the attachment |
| file_data | string | Yes | Base64 encoded file data |
| content_type | string | Yes | Content type of the file (e.g., image/jpeg, image/png) |

#### Example

```python
result = upload_multipart_attachment({
    "table_name": "incident",
    "table_sys_id": "d71f7935c0a8016700802b64c67c11c6",
    "file_name": "document.pdf",
    "file_data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwo+PgplbmRvYmoKdGVzdA==",
    "content_type": "application/pdf"
})
```

### list_attachments

List attachments from the ServiceNow Attachment API with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of attachments to return (default: 1000) |
| offset | integer | No | Offset for pagination (default: 0) |
| query | string | No | Encoded query for filtering attachments |
| table_name | string | No | Filter by table name |
| table_sys_id | string | No | Filter by table sys_id |
| file_name | string | No | Filter by file name |
| content_type | string | No | Filter by content type |

#### Example

```python
result = list_attachments({
    "limit": 50,
    "table_name": "incident",
    "content_type": "image/png"
})
```

### get_attachment

Get attachment metadata from the ServiceNow Attachment API.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| attachment_id | string | Yes | Sys_id of the attachment |

#### Example

```python
result = get_attachment({
    "attachment_id": "615ea769c0a80166001cf5f2367302f5"
})
```

### download_attachment

Download attachment binary data as base64 from the ServiceNow Attachment API.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| attachment_id | string | Yes | Sys_id of the attachment |
| accept_type | string | No | Accept header for response type (default: "*/*") |

#### Example

```python
# Download any file type
result = download_attachment({
    "attachment_id": "615ea769c0a80166001cf5f2367302f5"
})

# Download only image files
result = download_attachment({
    "attachment_id": "615ea769c0a80166001cf5f2367302f5",
    "accept_type": "image/*"
})
```

### delete_attachment

Delete an attachment from the ServiceNow Attachment API.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| attachment_id | string | Yes | Sys_id of the attachment to delete |

#### Example

```python
result = delete_attachment({
    "attachment_id": "615ea769c0a80166001cf5f2367302f5"
})
```

## Key Differences from Image Management

### API Endpoint
- **Attachment Management**: Uses ServiceNow's dedicated `/api/now/attachment/*` endpoints
- **Image Management**: Uses direct Table API calls to `db_image` table

### File Handling
- **Attachment Management**: Uses ServiceNow's built-in file handling, compression, and metadata extraction
- **Image Management**: Direct database storage of base64 data

### Metadata
- **Attachment Management**: Provides rich metadata including download links, compression status, image dimensions
- **Image Management**: Basic metadata storage in database fields

### Integration
- **Attachment Management**: Fully integrated with ServiceNow's attachment system and UI
- **Image Management**: Custom database records that may require additional integration

## Use Cases

### Document Attachments
Upload documents, PDFs, spreadsheets, and other files to ServiceNow records like incidents, change requests, and knowledge articles.

### Image Attachments
Attach screenshots, diagrams, photos, and other visual content to support tickets and documentation.

### Bulk File Operations
List and manage multiple attachments across different records and tables for maintenance and organization.

### Automated File Processing
Download attachments for processing, analysis, or migration to other systems.

### Compliance and Audit
Track file attachments, their metadata, and manage retention policies.

## Best Practices

### File Size and Types
- Be mindful of ServiceNow's file size limits (default 1024MB)
- Check allowed file extensions configured in `glide.attachment.extensions`
- Use appropriate content types for proper file handling

### Performance
- Use pagination for large result sets when listing attachments
- Consider multipart upload for larger files
- Batch operations when possible to reduce API calls

### Security
- Validate file content and types before upload
- Use encryption contexts for sensitive files
- Implement proper access controls and role requirements
- Never upload executable or potentially malicious files

### Metadata Management
- Use descriptive file names that include context
- Leverage creation_time parameter for accurate timestamping
- Store additional context in the associated record's fields

## Error Handling

All attachment management tools return consistent response structures with success/failure indicators and descriptive error messages. Common error scenarios include:

- File size exceeding system limits
- Invalid base64 encoding in file_data
- Insufficient permissions for attachment operations
- Non-existent target records (table_name/table_sys_id)
- Network connectivity issues
- Invalid content types or file formats

## Role Requirements

To use attachment management tools, the authenticating user must have:

- Roles required to create/read/write/delete Attachment [sys_attachment] records
- Roles required for the target table (e.g., itil role for incident attachments)
- Consider creating specific attachment management roles for service accounts

## Integration Points

### ServiceNow UI
Attachments uploaded via these tools appear in the standard ServiceNow attachment lists and can be downloaded through the UI.

### Service Portal
Attachments integrate with Service Portal widgets and can be accessed by end users based on security rules.

### Email Integration
Attachments can be referenced in email notifications and templates using the download_link field.

### Mobile Applications
ServiceNow mobile apps can access and display attachments uploaded through these tools.

## Example Natural Language Commands for Claude

Users can interact with the attachment management tools using natural language prompts:

- "Upload this screenshot to the incident record"
- "List all PDF attachments on change requests"
- "Download the attachment with ID 12345 as base64"
- "Delete the old attachment from this ticket"
- "Show me all image attachments larger than 1MB"
- "Upload this document to the knowledge article"
- "Find all attachments created by John Smith last month"
- "Get metadata for the attachment on this problem record"