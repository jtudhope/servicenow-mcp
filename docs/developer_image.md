# Image Management in ServiceNow MCP

## Overview

The Image Management tools provide functionality to manage images stored in the `db_image` table in ServiceNow. These tools allow developers to upload, retrieve, update, and delete images that can be used throughout the ServiceNow platform for various purposes such as logos, icons, attachments, and other visual content.

## Image Management Tools

### create_image

Create a new image in the db_image table with base64 encoded image data.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the image |
| image_data | string | Yes | Base64 encoded image data |
| content_type | string | Yes | MIME type of the image (e.g., 'image/png', 'image/jpeg') |
| table_name | string | No | Table name this image is associated with |
| table_sys_id | string | No | Sys ID of the record this image is associated with |
| image_type | string | No | Type of image (attachment, logo, icon, etc.) - defaults to "attachment" |
| size_bytes | integer | No | Size of the image in bytes |
| size_compressed | integer | No | Compressed size of the image in bytes |

#### Example

```python
result = create_image({
    "name": "company_logo.png",
    "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
    "content_type": "image/png",
    "table_name": "sys_user",
    "table_sys_id": "a1b2c3d4e5f6g7h8i9j0",
    "image_type": "logo"
})
```

#### Response

The tool returns a response with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| data | object | The created image details including sys_id, name, content_type, etc. |

### update_image

Update an existing image in the db_image table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image_id | string | Yes | Image sys_id |
| name | string | No | Name of the image |
| image_data | string | No | Base64 encoded image data |
| content_type | string | No | MIME type of the image |
| table_name | string | No | Table name this image is associated with |
| table_sys_id | string | No | Sys ID of the record this image is associated with |
| image_type | string | No | Type of image |

#### Example

```python
result = update_image({
    "image_id": "12345678901234567890123456789012",
    "name": "updated_logo.png",
    "image_type": "icon"
})
```

### list_images

List images from the db_image table with optional filtering.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of images to return (default: 10) |
| offset | integer | No | Offset for pagination (default: 0) |
| table_name | string | No | Filter by table name |
| table_sys_id | string | No | Filter by table sys_id |
| image_type | string | No | Filter by image type |
| content_type | string | No | Filter by content type |
| query | string | No | Search query for image name |

#### Example

```python
result = list_images({
    "limit": 20,
    "table_name": "sys_user",
    "image_type": "logo",
    "query": "company"
})
```

### get_image

Get a specific image from the db_image table with optional image data.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image_id | string | Yes | Image sys_id |
| include_data | boolean | No | Whether to include base64 image data in response (default: false) |

#### Example

```python
# Get image metadata only
result = get_image({
    "image_id": "12345678901234567890123456789012"
})

# Get image with base64 data
result = get_image({
    "image_id": "12345678901234567890123456789012",
    "include_data": true
})
```

### delete_image

Delete an image from the db_image table.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image_id | string | Yes | Image sys_id |

#### Example

```python
result = delete_image({
    "image_id": "12345678901234567890123456789012"
})
```

## Use Cases

### Company Logos and Branding
Upload and manage company logos, brand images, and visual assets that can be referenced throughout ServiceNow applications and portals.

### User Profile Pictures
Store and manage user profile images that can be associated with user records.

### Catalog Item Images
Upload images for service catalog items to enhance the visual presentation of offerings.

### Portal and Widget Images
Manage images used in Service Portal pages, widgets, and other UI components.

### Documentation and Knowledge Base
Store images that are referenced in knowledge articles, documentation, and help content.

## Best Practices

### Image Formats
- Use common web formats: PNG, JPEG, GIF, SVG
- PNG is recommended for logos and icons with transparency
- JPEG is suitable for photographs and complex images
- Consider file size optimization before upload

### Naming Conventions
- Use descriptive, consistent naming patterns
- Include version numbers if managing multiple versions
- Consider prefixes for different image types (logo_, icon_, photo_)

### Size Considerations
- Optimize images for web use before uploading
- Consider providing both original and compressed sizes
- Be mindful of storage quotas and performance impacts

### Security
- Validate image content and file types
- Consider virus scanning for uploaded content
- Implement appropriate access controls

## Error Handling

All image management tools return a consistent response structure with success/failure indicators and descriptive error messages. Common error scenarios include:

- Invalid image data or corrupted base64 encoding
- Unsupported image formats or MIME types
- File size limitations
- Permission restrictions
- Network or API connectivity issues

## Example Natural Language Commands for Claude

Users can interact with the image management tools using natural language prompts:

- "Upload a company logo image to ServiceNow"
- "List all images associated with the user table"
- "Update the image name for image ID 12345"
- "Get the base64 data for an image"
- "Delete an unused image from the system"
- "Find all PNG images that contain 'logo' in the name"
- "Show me all images uploaded in the last week"