# ATF Test: Incident Creation Form Validation

## Test Overview
This ATF test validates the complete incident creation workflow including form navigation, data entry, submission, and verification.

## Test Name
`Incident Creation Form Validation Test`

## Test Description
Validates that users can successfully create incidents through the incident creation form with proper field validation and data persistence.

## Test Configuration

### Test Type
Client Test

### Test Duration
Expected: 2-3 minutes

### Prerequisites
- User must have incident_user or itil role
- Incident table must be accessible
- Test data for caller_id must exist

## Test Steps

### Step 1: Navigate to Incident Creation Form
**Step Type:** Open URL
**Description:** Navigate to the incident creation form
**Configuration:**
- URL: `incident.do?sys_action=sysverb_new`
- Wait Condition: Form fully loaded
- Timeout: 10 seconds

**Validation:**
- Verify page title contains "New record | Incident"
- Verify form fields are visible and enabled

### Step 2: Set Up Test Data Variables
**Step Type:** Server Side Script
**Description:** Prepare test data for incident creation
**Script:**
```javascript
// Set test data variables
test_data.short_description = "ATF Test - Incident Creation Validation " + new Date().getTime();
test_data.description = "This is an automated test incident created by ATF to validate the incident creation workflow. Please ignore and close.";
test_data.category = "inquiry";
test_data.subcategory = "status";
test_data.impact = "3";
test_data.urgency = "3";

// Get a valid caller_id (system administrator for testing)
var user = new GlideRecord('sys_user');
user.addQuery('user_name', 'admin');
user.setLimit(1);
user.query();
if (user.next()) {
    test_data.caller_id = user.sys_id.toString();
    test_data.caller_name = user.name.toString();
}

gs.log("ATF Test Data Set - Short Description: " + test_data.short_description);
```

### Step 3: Fill Short Description Field
**Step Type:** Set Field Value
**Description:** Enter short description for the incident
**Configuration:**
- Field: `short_description`
- Value: `${test_data.short_description}`
- Wait for field update: Yes

**Validation:**
- Verify field contains the entered value
- Verify no validation errors are displayed

### Step 4: Fill Description Field
**Step Type:** Set Field Value
**Description:** Enter detailed description for the incident
**Configuration:**
- Field: `description`
- Value: `${test_data.description}`
- Wait for field update: Yes

**Validation:**
- Verify field contains the entered value

### Step 5: Set Caller ID
**Step Type:** Set Field Value
**Description:** Select caller for the incident
**Configuration:**
- Field: `caller_id`
- Value: `${test_data.caller_id}`
- Wait for field update: Yes

**Validation:**
- Verify caller field displays the correct user name
- Verify no validation errors for caller field

### Step 6: Set Category
**Step Type:** Set Field Value
**Description:** Select incident category
**Configuration:**
- Field: `category`
- Value: `${test_data.category}`
- Wait for field update: Yes

**Validation:**
- Verify category field shows selected value

### Step 7: Set Impact and Urgency
**Step Type:** Set Field Value
**Description:** Set impact level for the incident
**Configuration:**
- Field: `impact`
- Value: `${test_data.impact}`

**Step Type:** Set Field Value
**Description:** Set urgency level for the incident
**Configuration:**
- Field: `urgency`
- Value: `${test_data.urgency}`

**Validation:**
- Verify priority is automatically calculated
- Verify priority field shows "5 - Planning"

### Step 8: Validate Form State Before Submission
**Step Type:** Client Side Script
**Description:** Verify all required fields are populated correctly
**Script:**
```javascript
// Validate required fields are populated
var shortDesc = g_form.getValue('short_description');
var description = g_form.getValue('description');
var callerId = g_form.getValue('caller_id');
var category = g_form.getValue('category');

// Assert all required fields have values
test_result.assertEquals(shortDesc, test_data.short_description, "Short description should match test data");
test_result.assertNotEmpty(description, "Description field should not be empty");
test_result.assertNotEmpty(callerId, "Caller ID should not be empty");
test_result.assertEquals(category, test_data.category, "Category should match test data");

// Verify no form validation errors
var hasErrors = g_form.hasFieldMsgs();
test_result.assertFalse(hasErrors, "Form should not have any validation errors before submission");
```

### Step 9: Submit the Form
**Step Type:** UI Action
**Description:** Submit the incident creation form
**Configuration:**
- Action: Click Submit button
- Button: `sysverb_insert`
- Wait Condition: Form submission complete
- Timeout: 15 seconds

**Validation:**
- Verify form submission succeeds
- Verify no error messages are displayed
- Verify redirect to incident record

### Step 10: Capture Created Incident Number
**Step Type:** Server Side Script
**Description:** Get the incident number that was just created
**Script:**
```javascript
// Get the incident that was just created
var incident = new GlideRecord('incident');
incident.addQuery('short_description', test_data.short_description);
incident.addQuery('caller_id', test_data.caller_id);
incident.orderByDesc('sys_created_on');
incident.setLimit(1);
incident.query();

if (incident.next()) {
    test_data.created_incident_id = incident.sys_id.toString();
    test_data.created_incident_number = incident.number.toString();
    test_data.created_incident_state = incident.state.toString();
    gs.log("ATF Test - Created incident: " + test_data.created_incident_number);
} else {
    gs.error("ATF Test - Failed to find created incident");
    test_result.fail("Could not locate the created incident record");
}
```

### Step 11: Validate Incident Creation
**Step Type:** Server Side Script
**Description:** Verify the incident was created with correct data
**Script:**
```javascript
// Verify incident exists and has correct data
var incident = new GlideRecord('incident');
if (incident.get(test_data.created_incident_id)) {
    // Validate field values
    test_result.assertEquals(incident.short_description.toString(), test_data.short_description, 
        "Short description should match input");
    test_result.assertEquals(incident.description.toString(), test_data.description, 
        "Description should match input");
    test_result.assertEquals(incident.caller_id.toString(), test_data.caller_id, 
        "Caller ID should match input");
    test_result.assertEquals(incident.category.toString(), test_data.category, 
        "Category should match input");
    
    // Validate default values
    test_result.assertEquals(incident.state.toString(), "1", "New incident should have state = New");
    test_result.assertNotEmpty(incident.number.toString(), "Incident should have a number assigned");
    test_result.assertNotEmpty(incident.sys_created_on.toString(), "Incident should have creation timestamp");
    
    gs.log("ATF Test - Incident validation successful for: " + incident.number);
} else {
    test_result.fail("Created incident record not found with ID: " + test_data.created_incident_id);
}
```

### Step 12: Navigate to Incident List
**Step Type:** Open URL
**Description:** Navigate to incident list to verify incident appears
**Configuration:**
- URL: `incident_list.do`
- Wait Condition: List fully loaded
- Timeout: 10 seconds

### Step 13: Search for Created Incident
**Step Type:** Set Field Value
**Description:** Search for the created incident in the list
**Configuration:**
- Field: Search box
- Value: `${test_data.created_incident_number}`
- Submit search: Yes

**Validation:**
- Verify incident appears in search results
- Verify incident details match created data

### Step 14: Validate Incident in List View
**Step Type:** Client Side Script
**Description:** Verify the incident appears correctly in the list
**Script:**
```javascript
// Check if the incident appears in the list
var incidentRows = document.querySelectorAll('tr[data-list_id*="' + test_data.created_incident_id + '"]');

if (incidentRows.length > 0) {
    test_result.assertTrue(true, "Incident found in list view");
    
    // Validate key fields in list view
    var row = incidentRows[0];
    var numberCell = row.querySelector('[data-field="number"]');
    var shortDescCell = row.querySelector('[data-field="short_description"]');
    var stateCell = row.querySelector('[data-field="state"]');
    
    if (numberCell) {
        test_result.assertEquals(numberCell.textContent.trim(), test_data.created_incident_number, 
            "Incident number should match in list view");
    }
    
    if (shortDescCell) {
        test_result.assertTrue(shortDescCell.textContent.includes(test_data.short_description.substring(0, 50)), 
            "Short description should be visible in list view");
    }
    
} else {
    test_result.fail("Created incident not found in list view");
}
```

### Step 15: Cleanup - Delete Test Incident
**Step Type:** Server Side Script
**Description:** Clean up the test incident after validation
**Script:**
```javascript
// Clean up test data
var incident = new GlideRecord('incident');
if (incident.get(test_data.created_incident_id)) {
    var incidentNumber = incident.number.toString();
    incident.deleteRecord();
    gs.log("ATF Test - Cleaned up test incident: " + incidentNumber);
    test_result.assertTrue(true, "Test incident successfully cleaned up");
} else {
    gs.log("ATF Test - Test incident not found for cleanup: " + test_data.created_incident_id);
}
```

## Expected Results

### Success Criteria
1. ✅ Form loads successfully without errors
2. ✅ All required fields accept valid input
3. ✅ Form validation works correctly
4. ✅ Incident is created successfully upon submission
5. ✅ Created incident has correct field values
6. ✅ Incident appears in the incident list
7. ✅ All test data is properly cleaned up

### Failure Scenarios
- Form fails to load or displays errors
- Required field validation fails
- Form submission errors occur
- Incident is not created or has incorrect data
- Incident does not appear in list view

## Test Data Requirements

### Static Data
- Category: "inquiry"
- Subcategory: "status"
- Impact: "3 - Low"
- Urgency: "3 - Low"
- Expected Priority: "5 - Planning"

### Dynamic Data
- Short Description: Generated with timestamp
- Description: Standard test description
- Caller ID: System administrator user
- Incident Number: Auto-generated by system

## Error Handling

### Validation Checks
1. Form field accessibility
2. Required field validation
3. Data persistence verification
4. List view display validation

### Timeout Management
- Form loading: 10 seconds
- Field updates: 5 seconds
- Form submission: 15 seconds
- Page navigation: 10 seconds

## Maintenance Notes

### Regular Updates Needed
- Verify caller_id user still exists and is active
- Update category values if picklist changes
- Adjust timeouts based on system performance
- Review field names if incident form is customized

### Dependencies
- Incident table access (incident_user or itil role)
- System administrator user account
- Standard incident form configuration
- Incident list view accessibility

This test provides comprehensive coverage of the incident creation workflow with proper validation, error handling, and cleanup procedures.