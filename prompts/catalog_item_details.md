# ServiceNow Catalog Item Creation Details
This file serves as a template for the ServiceNow MCP tool to get the details required to build a catalog item.

# Catalog Item General Details
1. Name: New User Request
2. Short Description: [Not specified, please generate automatically]
3. Description: [Not specified, please generate automatically]
4. Catalog: IT Service Catalog
5. Category: IT Services
6. Request method: Submit

# Catalog Item Taxonomy Topic Relationships
1. Create a connected content record such that the "Catalog Item" field is the catalog item that was just created, the "Topic" field is the "IT Support" Taxonomy Topic, and the "Content type" field is the "Catalog Item" Taxonomy Content Configuration record. Since all of the fields in the connected content record, you will need to retreive the sys id of each value provided.


# Catalog Item Variables (in order)
This is the list of variables to be created with. Please be mindful that the value of "additional claude instructions" listed here does not correspond to a field of the catalog variable. But it provides additional instructions to be completed after the variable is created.
1. {
    name: user_type, 
    question: "What type of user are you adding?",
    type: Select Box,
    mandatory: true,
    include none: true,
    choices: ["Full Time Employee", "Part-Time Employee", "Non-Employee"],
    }
2. {
    name: first_name, 
    question: "First Name",
    type: Single Line Text,
    mandatory: true
    }
3. {
    name: last_name, 
    question: Last Name,
    type: Single Line Text,
    mandatory: true
    }
4. {
    name: title, 
    question: "User’s Title (as it should appear in O365)",
    type: Single Line Text,
    mandatory: true
    }
5. {
    name: location, 
    question: "Where is the new employee located?",
    type: Select Box,
    mandatory: true,
    include none: true,
    choices: ["Canada", "Colombia", "Honduras", "USA", "Other"],
    }
6. {
    name: location_other, 
    question: "Please specify the location",
    type: Single Line Text,
    mandatory: false,
    }
7. {
    name: time_zone, 
    question: "Which time zone is the user located?",
    type: Select Box,
    mandatory: true,
    include none: true,
    choices: ["EST", "CST", "AST", "CET", "PST", "NST"]
    }
8. {
    name: personal_email, 
    question: "What is the user’s personal email address?",
    type: Single Line Text,
    mandatory: true
    }
9. {
    name: personal_cell, 
    question: "What is the user’s personal mobile/cell phone number?",
    type: Single Line Text,
    mandatory: true,
    show help: true,
    always expanded: true,
    help text: "Note: Used if someone calls in requesting an MFA (Multi-Factor Authentication) change, to confirm identity prior to processing the request."
    }
10. {
    name: start_date, 
    question: "What is the start date for the new user?",
    type: Date,
    mandatory: false,
    show help: true,
    always expanded: true,
    help text: "Note: Submissions made after 5:00 pm EST will not be processed until the next working day."
    }
11. {
    name: nextiva_required, 
    question: "Does the new user need a NexTiva phone number and extension?",
    type: Yes/No,
    mandatory: true,
    include none: true,
    }
12. {
    name: nextiva_flow, 
    question: "Which NexTiva call flow should the user be added to?",
    type: Select Box,
    mandatory: false,
    include none: true,
    choices: ["Sales", "Client/Workforce Support", "Payroll/Billing", "Corporate Finance"]
    }
13. {
    name: desktop_apps_required, 
    question: "Which of the following desktop apps should be installed on the laptop?",
    type: List Collector,
    mandatory: false,
    list table: question_choice
    reference qualifier: question=[sys_id of the current question]
    additional claude instructions: Please Create the following records in the question choice table after creating this variable ["Adobe Standard", "Adobe Signature", "NexTiva", "Other"]. Each record needs the question field to be populated with the variable that was just created.
    }
14. {
    name: desktop_apps_other, 
    question: "Please specify the desktop application",
    type: Single Line Text,
    mandatory: false,
    }
15. {
    name: department, 
    question: "Which MBP department is the user associated with?",
    type: Reference,
    mandatory: false,
    reference: cmn_department
    }
16. {
    name: manager, 
    question: "Please list the user’s report to manager",
    type: Reference,
    mandatory: false,
    reference: sys_user
    }
17. {
    name: nextiva_flow, 
    question: "Which NexTiva call flow should the user be added to?",
    type: Select Box,
    mandatory: false,
    include none: true,
    choices: ["Sales", "Client/Workforce Support", "Payroll/Billing", "Corporate Finance"]
    }
18. {
    name: teams_hubs, 
    question: "All new users will automatically receive access to OneTeam, Operations, Members, Digital Innovation and Revenue. What other MBP Teams Hubs are required?",
    type: List Collector,
    mandatory: false,
    list table: question_choice
    reference qualifier: question=[sys_id of the current question]
    additional claude instructions: Please Create the following records in the question choice table after creating this variable ["Contracts & Compliance", "Corp Finance", "Corp HR", "CTM", "Implementation", "IT Governance", "Leadership", "Pay Bill", "Team Experience", "Other"]. Each record needs the question field to be populated with the variable that was just created.
    }
20. {
    name: teams_hubs_other, 
    question: "Please specify the MBP Teams Hub",
    type: Single Line Text,
    mandatory: false,
    }
21. {
    name: shared_inboxes, 
    question: "Which shared inbox(es) and/or distribution lists will user need to access?",
    type: List Collector,
    mandatory: false,
    list table: question_choice
    reference qualifier: question=[sys_id of the current question]
    additional claude instructions: Please Create the following records in the question choice table after creating this variable ["billing@mybasepay.com", "payrolltodo@mybasepay.com", "corpap@mybasepay.com", "implementations@mybasepay.com", "sales@mybasepay.com", "BusDev@mybasepay.com", "partnerships@mybasepay.com", "CorpHR@mybasepay.com", "HROnboarding@mybasepay.com", "marketing@mybasepay.com", "techsupport@mybasepay.com", "Ops@mybasepay.com", "Other"]. Each record needs the question field to be populated with the variable that was just created.
    }
22. {
    name: shared_inboxes_other, 
    question: "Please specify the Shared Inbox / Distribution List",
    type: Single Line Text,
    mandatory: false,
    }
23. {
    name: equipment, 
    question: "Equipment Requirements",
    type: List Collector,
    mandatory: false,
    list table: question_choice
    reference qualifier: question=[sys_id of the current question]
    additional claude instructions: Please Create the following records in the question choice table after creating this variable ["Laptop", "Monitor (1x)", "Monitor (2x) - includes docking station", "Wireless keyboard & mouse"]. Each record needs the question field to be populated with the variable that was just created.
    }
24. {
    name: laptop_requirement, 
    question: "Pleace specify the laptop requirment",
    type: Select Box,
    mandatory: false,
    choices: ["Basic User", "Power User"]
    }
25. {
    name: shipping_instructions,
    question: "Shipping & Equipment Details/Instructions",
    type: Single Line Text,
    mandatory: false
}
26. {
    name: work_email_specification,
    question: "New user email address to be created, if it should deviate from firstname@mybasepay.com",
    type: Single Line Text,
    mandatory: false
}
27. {
    name: additional_details,
    question: "Additional Details Section (Internal MBP & External Vendor Instructions)",
    type: Multi Line Text,
    mandatory: false
}

# Catalog Item UI Policies
1. Develop a UI policy such that the variable "location_other" is only visible and mandatory when the "location" variable has a value of "Other"
2. Develop a UI policy such that the variable "desktop_apps_other" is only visible and mandatory when the "desktop_apps_required" variable has a value of "Other"
3. Develop a UI policy such that the variable "teams_hubs_other" is only visible and mandatory when the "teams_hubs" variable has a display value of "Other"
4. Develop a UI policy such that the variable "shared_inboxes_other" is only visible and mandatory when the "shared_inboxes" variable has a display value of "Other"