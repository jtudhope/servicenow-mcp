"""
Tools module for the ServiceNow MCP server.
"""

# Import tools as they are implemented
from servicenow_mcp.tools.catalog_optimization import (
    get_optimization_recommendations,
    update_catalog_item,
)
from servicenow_mcp.tools.catalog_tools import (
    create_catalog_category,
    create_catalog_item,
    delete_catalog_item,
    get_catalog_item,
    list_catalog_categories,
    list_catalog_items,
    move_catalog_items,
    update_catalog_category,
    update_catalog_item,
)
from servicenow_mcp.tools.catalog_variables import (
    create_catalog_variable,
    list_catalog_variables,
    update_catalog_variable,
    delete_catalog_variable,
    get_catalog_variable,
)
from servicenow_mcp.tools.change_tools import (
    add_change_task,
    approve_change,
    create_change_request,
    get_change_request_details,
    list_change_requests,
    reject_change,
    submit_change_for_approval,
    update_change_request,
)
from servicenow_mcp.tools.changeset_tools import (
    add_file_to_changeset,
    commit_changeset,
    create_changeset,
    get_changeset_details,
    list_changesets,
    publish_changeset,
    update_changeset,
)
from servicenow_mcp.tools.incident_tools import (
    add_comment,
    create_incident,
    list_incidents,
    resolve_incident,
    update_incident,
)
from servicenow_mcp.tools.knowledge_base import (
    create_article,
    create_category,
    create_knowledge_base,
    get_article,
    list_articles,
    list_knowledge_bases,
    publish_article,
    update_article,
    list_categories,
)
from servicenow_mcp.tools.script_include_tools import (
    create_script_include,
    delete_script_include,
    get_script_include,
    list_script_includes,
    update_script_include,
)
from servicenow_mcp.tools.user_tools import (
    create_user,
    update_user,
    get_user,
    list_users,
    create_group,
    update_group,
    add_group_members,
    remove_group_members,
    list_groups,
)
from servicenow_mcp.tools.workflow_tools import (
    activate_workflow,
    add_workflow_activity,
    create_workflow,
    deactivate_workflow,
    delete_workflow_activity,
    get_workflow_activities,
    get_workflow_details,
    list_workflow_versions,
    list_workflows,
    reorder_workflow_activities,
    update_workflow,
    update_workflow_activity,
)
from servicenow_mcp.tools.story_tools import (
    create_story,
    update_story,
    list_stories,
    list_story_dependencies,
    create_story_dependency,
    delete_story_dependency,
)
from servicenow_mcp.tools.epic_tools import (
    create_epic,
    update_epic,
    list_epics,
)
from servicenow_mcp.tools.scrum_task_tools import (
    create_scrum_task,
    update_scrum_task,
    list_scrum_tasks,
)
from servicenow_mcp.tools.project_tools import (
    create_project,
    update_project,
    list_projects,
)

from servicenow_mcp.tools.developer_ui_action import (
    create_ui_action,
    update_ui_action,
    list_ui_actions,
    get_ui_action,
    delete_ui_action,
)

from servicenow_mcp.tools.developer_acl import (
    create_acl,
    update_acl,
    list_acls,
    get_acl,
    delete_acl,
)



# Add import for new inbound email action tools
from servicenow_mcp.tools.developer_inbound_email_actions import (
    create_inbound_email_action,
    update_inbound_email_action,
    list_inbound_email_actions,
    get_inbound_email_action,
    delete_inbound_email_action,
)


# Add import for new table tools
from servicenow_mcp.tools.developer_table import (
    create_table,
    create_table_column,
    update_table,
    update_table_column,
    list_tables,
    list_table_columns,
    get_table,
    get_table_column,
)

from servicenow_mcp.tools.developer_table_choice import (
    create_choice,
    update_choice,
    list_choices,
    get_choice,
    delete_choice,
    bulk_create_choices,
    reorder_choices,
)

from servicenow_mcp.tools.developer_notification import (
    create_email_notification,
    update_email_notification,
    list_email_notifications,
    get_email_notification,
    delete_email_notification,
)

# Application Menu Items
from servicenow_mcp.tools.menu.developer_menu_application import (
    create_application_menu,
    update_application_menu,
    list_application_menus,
    get_application_menu,
    delete_application_menu,
)

# Import for new application module tools
from servicenow_mcp.tools.menu.developer_menu_module import (
    create_app_module,
    update_app_module,
    list_app_modules,
    get_app_module,
    delete_app_module,
)


from servicenow_mcp.tools.developer_user_role import (
    assign_user_role,
    remove_user_role,
    list_user_roles,
    bulk_assign_user_roles,
    bulk_remove_user_roles,
)

from servicenow_mcp.tools.developer_esc_quicklinks import (
    create_quick_link,
    update_quick_link,
    list_quick_links,
    get_quick_link,
    delete_quick_link,
)

# Portal Configuration Management
from servicenow_mcp.tools.portal.developer_portal import (
    create_portal,
    update_portal,
    list_portals,
    get_portal,
    delete_portal,
)

from servicenow_mcp.tools.portal.developer_portal_instance import (
    create_widget_instance,
    update_widget_instance,
    list_widget_instances,
    get_widget_instance,
    delete_widget_instance,
    clone_widget_instance,
    bulk_update_widget_instances,
)

from servicenow_mcp.tools.portal.developer_portal_page import (
    create_portal_page,
    update_portal_page,
    list_portal_pages,
    get_portal_page,
    clone_portal_page,
    delete_portal_page,
)

from servicenow_mcp.tools.portal.developer_portal_row import (
    create_portal_row,
    update_portal_row,
    list_portal_rows,
    get_portal_row,
    clone_portal_row,
    delete_portal_row,
    reorder_portal_rows,
)

from servicenow_mcp.tools.portal.developer_portal_column import (
    create_portal_column,
    update_portal_column,
    list_portal_columns,
    get_portal_column,
    clone_portal_column,
    delete_portal_column,
    reorder_portal_columns,
    create_responsive_grid,
)

from servicenow_mcp.tools.portal.developer_portal_container import (
    create_portal_container,
    update_portal_container,
    list_portal_containers,
    get_portal_container,
    clone_portal_container,
    delete_portal_container,
    reorder_portal_containers,
)

from servicenow_mcp.tools.developer_assignment_rule import (
    create_assignment_rule,
    update_assignment_rule,
    list_assignment_rules,
    get_assignment_rule,
    delete_assignment_rule,
)

from servicenow_mcp.tools.developer_email_template import (
    create_email_template,
    update_email_template,
    list_email_templates,
    get_email_template,
    delete_email_template,
    clone_email_template,
)

from servicenow_mcp.tools.developer_image import (
    create_image,
    update_image,
    list_images,
    get_image,
    delete_image,
)

from servicenow_mcp.tools.developer_servicecatalog import (
    create_service_catalog,
    update_service_catalog,
    list_service_catalogs,
    get_service_catalog,
    delete_service_catalog,
)

from servicenow_mcp.tools.developer_attachment import (
    upload_attachment,
    upload_multipart_attachment,
    list_attachments,
    get_attachment,
    download_attachment,
    delete_attachment,
)

from servicenow_mcp.tools.developer_email_layouts import (
    create_email_layout,
    update_email_layout,
    list_email_layouts,
    get_email_layout,
    delete_email_layout,
    clone_email_layout,
)

from servicenow_mcp.tools.catalog.catalog_ui_policy import (
    create_catalog_ui_policy,
    update_catalog_ui_policy,
    list_catalog_ui_policies,
    get_catalog_ui_policy,
    delete_catalog_ui_policy,
    clone_catalog_ui_policy,
)

from servicenow_mcp.tools.catalog.catalog_ui_policy_action import (
    create_catalog_ui_policy_action,
    update_catalog_ui_policy_action,
    list_catalog_ui_policy_actions,
    get_catalog_ui_policy_action,
    delete_catalog_ui_policy_action,
    clone_catalog_ui_policy_action,
)

from servicenow_mcp.tools.catalog.catalog_client_scripts import (
    create_catalog_client_script,
    update_catalog_client_script,
    list_catalog_client_scripts,
    get_catalog_client_script,
    delete_catalog_client_script,
    clone_catalog_client_script,
)

from servicenow_mcp.tools.catalog.catalog_item_available_for import (
    add_available_for,
    remove_available_for,
    add_not_available_for,
    remove_not_available_for,
    list_available_for,
    bulk_update_available_for,
)

from servicenow_mcp.tools.knowledge.taxonomy import (
    create_taxonomy,
    update_taxonomy,
    list_taxonomies,
    get_taxonomy,
    delete_taxonomy,
    clone_taxonomy,
)

from servicenow_mcp.tools.knowledge.topic import (
    create_topic,
    update_topic,
    list_topics,
    get_topic,
    delete_topic,
    clone_topic,
)

from servicenow_mcp.tools.knowledge.connected_content import (
    create_connected_content,
    update_connected_content,
    list_connected_content,
    get_connected_content,
    delete_connected_content,
    bulk_connect_content,
)

from servicenow_mcp.tools.catalog.question_choice import (
    create_question_choice,
    update_question_choice,
    list_question_choices,
    get_question_choice,
    delete_question_choice,
)

from servicenow_mcp.tools.catalog.variable_sets import (
    create_variable_set,
    update_variable_set,
    list_variable_sets,
    get_variable_set,
    delete_variable_set,
)

from servicenow_mcp.tools.portal.portal_catalog_associations import (
    create_portal_catalog_association,
    update_portal_catalog_association,
    list_portal_catalog_associations,
    delete_portal_catalog_association,
    get_portal_catalog_association,
    bulk_create_portal_catalog_associations,
)

from servicenow_mcp.tools.portal.portal_taxonomy_associations import (
    create_portal_taxonomy_association,
    update_portal_taxonomy_association,
    list_portal_taxonomy_associations,
    delete_portal_taxonomy_association,
    get_portal_taxonomy_association,
    bulk_create_portal_taxonomy_associations,
)

from servicenow_mcp.tools.portal.taxonomy_content_configuration import (
    create_taxonomy_content_configuration,
    update_taxonomy_content_configuration,
    list_taxonomy_content_configurations,
    get_taxonomy_content_configuration,
    delete_taxonomy_content_configuration,
)

# from servicenow_mcp.tools.request_tools import create_request, update_request

__all__ = [
    # Incident tools
    "create_incident",
    "update_incident",
    "add_comment",
    "resolve_incident",
    "list_incidents",
    
    # Catalog tools
    "list_catalog_items",
    "get_catalog_item",
    "create_catalog_item",
    "update_catalog_item",
    "delete_catalog_item",
    "list_catalog_categories",
    "create_catalog_category",
    "update_catalog_category",
    "move_catalog_items",
    "get_optimization_recommendations",

    
    # Change management tools
    "create_change_request",
    "update_change_request",
    "list_change_requests",
    "get_change_request_details",
    "add_change_task",
    "submit_change_for_approval",
    "approve_change",
    "reject_change",
    
    # Workflow management tools
    "list_workflows",
    "get_workflow_details",
    "list_workflow_versions",
    "get_workflow_activities",
    "create_workflow",
    "update_workflow",
    "activate_workflow",
    "deactivate_workflow",
    "add_workflow_activity",
    "update_workflow_activity",
    "delete_workflow_activity",
    "reorder_workflow_activities",
    
    # Changeset tools
    "list_changesets",
    "get_changeset_details",
    "create_changeset",
    "update_changeset",
    "commit_changeset",
    "publish_changeset",
    "add_file_to_changeset",
    
    # Script Include tools
    "list_script_includes",
    "get_script_include",
    "create_script_include",
    "update_script_include",
    "delete_script_include",
    
    # Knowledge Base tools
    "create_knowledge_base",
    "list_knowledge_bases",
    "create_category",
    "list_categories",
    "create_article",
    "update_article",
    "publish_article",
    "list_articles",
    "get_article",
    
    # User management tools
    "create_user",
    "update_user",
    "get_user",
    "list_users",
    "create_group",
    "update_group",
    "add_group_members",
    "remove_group_members",
    "list_groups",

    # Story tools
    "create_story",
    "update_story",
    "list_stories",
    "list_story_dependencies",
    "create_story_dependency",
    "delete_story_dependency",
    
    # Epic tools
    "create_epic",
    "update_epic",
    "list_epics",

    # Scrum Task tools
    "create_scrum_task",
    "update_scrum_task",
    "list_scrum_tasks",

    # Project tools
    "create_project",
    "update_project",
    "list_projects",

    # Developer Toolbox - UI Actions
    "create_ui_action",
    "update_ui_action", 
    "list_ui_actions",
    "get_ui_action",
    "delete_ui_action",

    # ACL Management tools
    "create_acl",
    "update_acl", 
    "list_acls",
    "get_acl",
    "delete_acl",

    # Security Elevation tools
    "security_elevation",
    
    # Inbound Email Action tools
    "create_inbound_email_action",
    "update_inbound_email_action", 
    "list_inbound_email_actions",
    "get_inbound_email_action",
    "delete_inbound_email_action",

    # Table Management tools
    "create_table",
    "create_table_column",
    "update_table",
    "update_table_column",
    "list_tables",
    "list_table_columns",
    "get_table",
    "get_table_column",

    # Choice Management tools
    "create_choice",
    "update_choice",
    "list_choices",
    "get_choice",
    "delete_choice",
    "bulk_create_choices",
    "reorder_choices",
    
    # Email Notification Actions
    "create_email_notification",
    "update_email_notification",
    "list_email_notifications",
    "get_email_notification",
    "delete_email_notification",


    # Application Menu Items
    "create_application_menu",
    "update_application_menu",
    "list_application_menus",
    "get_application_menu",
    "delete_application_menu",

    # Application Module Menu Tools
    "create_app_module",
    "update_app_module", 
    "list_app_modules",
    "get_app_module",
    "delete_app_module",

    # User Role Management tools
    "assign_user_role",
    "remove_user_role", 
    "list_user_roles",
    "bulk_assign_user_roles",
    "bulk_remove_user_roles",

    # Employee Center Quick Link Management
    "create_quick_link",
    "update_quick_link", 
    "list_quick_links",
    "get_quick_link",
    "delete_quick_link",

    # Portal Configuration Management
    "create_portal",
    "update_portal", 
    "list_portals",
    "get_portal",
    "delete_portal",

    # Employee Center Widget Instance Management
    "create_widget_instance",
    "update_widget_instance", 
    "list_widget_instances",
    "get_widget_instance",
    "delete_widget_instance",
    "clone_widget_instance",
    "bulk_update_widget_instances",

    # Portal Page tools
    "create_portal_page",
    "update_portal_page", 
    "list_portal_pages",
    "get_portal_page",
    "clone_portal_page",
    "delete_portal_page",

    # Portal Row tools
    "create_portal_row",
    "update_portal_row", 
    "list_portal_rows",
    "get_portal_row",
    "clone_portal_row",
    "delete_portal_row",
    "reorder_portal_rows",

    # Portal Column tools
    "create_portal_column",
    "update_portal_column", 
    "list_portal_columns",
    "get_portal_column",
    "clone_portal_column",
    "delete_portal_column",
    "reorder_portal_columns",
    "create_responsive_grid",

        # Portal Container tools
    "create_portal_container",
    "update_portal_container", 
    "list_portal_containers",
    "get_portal_container",
    "clone_portal_container",
    "delete_portal_container",
    "reorder_portal_containers",

    "create_catalog_variable",
    "list_catalog_variables", 
    "update_catalog_variable",
    "delete_catalog_variable",
    "get_catalog_variable",

    # Assignment Rule Management tools
    "create_assignment_rule",
    "update_assignment_rule", 
    "list_assignment_rules",
    "get_assignment_rule",
    "delete_assignment_rule",

    # Email Template Management tools
    "create_email_template",
    "update_email_template", 
    "list_email_templates",
    "get_email_template",
    "delete_email_template",
    "clone_email_template",

    # Image Management tools
    "create_image",
    "update_image",
    "list_images",
    "get_image",
    "delete_image",

    # Service Catalog Management tools
    "create_service_catalog",
    "update_service_catalog",
    "list_service_catalogs",
    "get_service_catalog",
    "delete_service_catalog",

    # Attachment Management tools
    "upload_attachment",
    "upload_multipart_attachment",
    "list_attachments",
    "get_attachment",
    "download_attachment",
    "delete_attachment",

    # Email Layout Management tools
    "create_email_layout",
    "update_email_layout",
    "list_email_layouts",
    "get_email_layout",
    "delete_email_layout",
    "clone_email_layout",

    # Catalog UI Policy Management tools
    "create_catalog_ui_policy",
    "update_catalog_ui_policy",
    "list_catalog_ui_policies",
    "get_catalog_ui_policy",
    "delete_catalog_ui_policy",
    "clone_catalog_ui_policy",

    # Catalog UI Policy Action Management tools
    "create_catalog_ui_policy_action",
    "update_catalog_ui_policy_action",
    "list_catalog_ui_policy_actions",
    "get_catalog_ui_policy_action",
    "delete_catalog_ui_policy_action",
    "clone_catalog_ui_policy_action",

    # Catalog Client Scripts Management tools
    "create_catalog_client_script",
    "update_catalog_client_script",
    "list_catalog_client_scripts",
    "get_catalog_client_script",
    "delete_catalog_client_script",
    "clone_catalog_client_script",

    # Catalog Item Available For Management tools
    "add_available_for",
    "remove_available_for",
    "add_not_available_for",
    "remove_not_available_for",
    "list_available_for",
    "bulk_update_available_for",

    # Taxonomy Management tools
    "create_taxonomy",
    "update_taxonomy",
    "list_taxonomies",
    "get_taxonomy",
    "delete_taxonomy",
    "clone_taxonomy",
    
    # Topic Management tools
    "create_topic",
    "update_topic",
    "list_topics",
    "get_topic",
    "delete_topic",
    "clone_topic",
    
    # Connected Content Management tools
    "create_connected_content",
    "update_connected_content",
    "list_connected_content",
    "get_connected_content",
    "delete_connected_content",
    "bulk_connect_content",

    # Question Choice Management tools
    "create_question_choice",
    "update_question_choice",
    "list_question_choices",
    "get_question_choice",
    "delete_question_choice",

    # Variable Sets Management tools
    "create_variable_set",
    "update_variable_set",
    "list_variable_sets",
    "get_variable_set",
    "delete_variable_set",

    # Portal Catalog Association Management tools
    "create_portal_catalog_association",
    "update_portal_catalog_association",
    "list_portal_catalog_associations",
    "delete_portal_catalog_association",
    "get_portal_catalog_association",
    "bulk_create_portal_catalog_associations",

    # Portal Taxonomy Association Management tools
    "create_portal_taxonomy_association",
    "update_portal_taxonomy_association",
    "list_portal_taxonomy_associations",
    "delete_portal_taxonomy_association",
    "get_portal_taxonomy_association",
    "bulk_create_portal_taxonomy_associations",

    # Taxonomy Content Configuration Management tools
    "create_taxonomy_content_configuration",
    "update_taxonomy_content_configuration",
    "list_taxonomy_content_configurations",
    "get_taxonomy_content_configuration",
    "delete_taxonomy_content_configuration",
    
] 