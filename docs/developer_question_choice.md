# Question Choice Management in ServiceNow MCP

## Overview

The Question Choice Management tools provide comprehensive functionality for managing question choices in ServiceNow. Question choices are records stored in the `question_choice` table that are used to display as options on catalog variables where a multi-select or select box is used.

## Available Tools

### create_question_choice

Creates a new question choice in ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| value | string | Yes | Value of the choice (stored value) |
| text | string | Yes | Display text of the choice |
| question | string | No | Question sys_id this choice belongs to |
| order | integer | No | Display order of the choice (default: 100) |
| inactive | boolean | No | Whether the choice is inactive (default: false) |
| misc | string | No | Price for this choice |
| rec_misc | string | No | Recurring price for this choice |

**Example:**
```json
{
  "value": "option1",
  "text": "Option One",
  "question": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "order": 100,
  "inactive": false,
  "misc": "10.00",
  "rec_misc": "5.00"
}
```

### update_question_choice

Updates an existing question choice in ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| choice_id | string | Yes | Question choice sys_id |
| value | string | No | Updated value of the choice |
| text | string | No | Updated display text of the choice |
| question | string | No | Updated question sys_id this choice belongs to |
| order | integer | No | Updated display order of the choice |
| inactive | boolean | No | Updated inactive status |
| misc | string | No | Updated price for this choice |
| rec_misc | string | No | Updated recurring price for this choice |

**Example:**
```json
{
  "choice_id": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7",
  "text": "Updated Option One",
  "order": 150,
  "inactive": true
}
```

### list_question_choices

Lists question choices with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| question | string | No | Filter by question sys_id |
| inactive | boolean | No | Filter by inactive status |
| limit | integer | No | Maximum number of choices to return (default: 50) |
| offset | integer | No | Offset for pagination (default: 0) |

**Example:**
```json
{
  "question": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "inactive": false,
  "limit": 25,
  "offset": 0
}
```

### get_question_choice

Retrieves a specific question choice by sys_id.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| choice_id | string | Yes | Question choice sys_id |

**Example:**
```json
{
  "choice_id": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7"
}
```

### delete_question_choice

Deletes a question choice from ServiceNow.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| choice_id | string | Yes | Question choice sys_id |

**Example:**
```json
{
  "choice_id": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7"
}
```

## Response Format

All question choice tools return a response with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation was successful |
| message | string | A message describing the result |
| choice | object | Single choice data (for create, update, get operations) |
| choices | array | List of choices (for list operation) |

## Common Use Cases

### Creating Choices for a Catalog Variable

When building catalog items with select box or multi-select variables, you need to create question choices that define the available options:

```json
{
  "value": "laptop_standard",
  "text": "Standard Laptop",
  "question": "hardware_type_question_id",
  "order": 100,
  "misc": "999.00"
}
```

### Managing Choice Order

Control the display order of choices by setting the `order` field. Lower numbers appear first:

```json
{
  "choice_id": "existing_choice_id",
  "order": 50
}
```

### Pricing Choices

Add pricing information to choices for cost calculations:

```json
{
  "value": "premium_support",
  "text": "Premium Support Package",
  "misc": "500.00",
  "rec_misc": "50.00"
}
```

## Natural Language Examples

These are example prompts that users can give to Claude that would trigger the question choice tools:

- "Create a new question choice with value 'laptop' and text 'Laptop Computer'"
- "List all question choices for the hardware selection question"
- "Update the display text for the laptop choice to 'Premium Laptop'"
- "Delete the outdated printer choice option"
- "Show me the details of the question choice with ID xyz123"
- "Create multiple question choices for a software selection dropdown"
- "Set the price for the premium software option to $199"