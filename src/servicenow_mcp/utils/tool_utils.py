from typing import Any, Callable, Dict, Tuple, Type

# Import all necessary tool implementation functions and params models
# (This list needs to be kept complete and up-to-date)
from servicenow_mcp.tools.catalog_optimization import (
    OptimizationRecommendationsParams,
    UpdateCatalogItemParams,
)
from servicenow_mcp.tools.catalog_optimization import (
    get_optimization_recommendations as get_optimization_recommendations_tool,
)
from servicenow_mcp.tools.catalog_optimization import (
    update_catalog_item as update_catalog_item_tool,
)
from servicenow_mcp.tools.catalog_tools import (
    CreateCatalogCategoryParams,
    GetCatalogItemParams,
    ListCatalogCategoriesParams,
    ListCatalogItemsParams,
    MoveCatalogItemsParams,
    UpdateCatalogCategoryParams,
)
from servicenow_mcp.tools.catalog_tools import (
    create_catalog_category as create_catalog_category_tool,
)
from servicenow_mcp.tools.catalog_tools import (
    get_catalog_item as get_catalog_item_tool,
)
from servicenow_mcp.tools.catalog_tools import (
    list_catalog_categories as list_catalog_categories_tool,
)
from servicenow_mcp.tools.catalog_tools import (
    list_catalog_items as list_catalog_items_tool,
)
from servicenow_mcp.tools.catalog_tools import (
    move_catalog_items as move_catalog_items_tool,
)
from servicenow_mcp.tools.catalog_tools import (
    update_catalog_category as update_catalog_category_tool,
)

from servicenow_mcp.tools.catalog_variables import (
    CreateCatalogVariableParams,
    ListCatalogVariablesParams,
    UpdateCatalogVariableParams,
    DeleteCatalogVariableParams,
    GetCatalogVariableParams,
)
from servicenow_mcp.tools.catalog_variables import (
    create_catalog_variable as create_catalog_variable_tool,
    list_catalog_variables as list_catalog_variables_tool,
    update_catalog_variable as update_catalog_variable_tool,
    delete_catalog_variable as delete_catalog_variable_tool,
    get_catalog_variable as get_catalog_variable_tool,
)

from servicenow_mcp.tools.change_tools import (
    AddChangeTaskParams,
    ApproveChangeParams,
    CreateChangeRequestParams,
    GetChangeRequestDetailsParams,
    ListChangeRequestsParams,
    RejectChangeParams,
    SubmitChangeForApprovalParams,
    UpdateChangeRequestParams,
)
from servicenow_mcp.tools.change_tools import (
    add_change_task as add_change_task_tool,
)
from servicenow_mcp.tools.change_tools import (
    approve_change as approve_change_tool,
)
from servicenow_mcp.tools.change_tools import (
    create_change_request as create_change_request_tool,
)
from servicenow_mcp.tools.change_tools import (
    get_change_request_details as get_change_request_details_tool,
)
from servicenow_mcp.tools.change_tools import (
    list_change_requests as list_change_requests_tool,
)
from servicenow_mcp.tools.change_tools import (
    reject_change as reject_change_tool,
)
from servicenow_mcp.tools.change_tools import (
    submit_change_for_approval as submit_change_for_approval_tool,
)
from servicenow_mcp.tools.change_tools import (
    update_change_request as update_change_request_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    AddFileToChangesetParams,
    CommitChangesetParams,
    CreateChangesetParams,
    GetChangesetDetailsParams,
    ListChangesetsParams,
    PublishChangesetParams,
    UpdateChangesetParams,
)
from servicenow_mcp.tools.changeset_tools import (
    add_file_to_changeset as add_file_to_changeset_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    commit_changeset as commit_changeset_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    create_changeset as create_changeset_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    get_changeset_details as get_changeset_details_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    list_changesets as list_changesets_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    publish_changeset as publish_changeset_tool,
)
from servicenow_mcp.tools.changeset_tools import (
    update_changeset as update_changeset_tool,
)
from servicenow_mcp.tools.incident_tools import (
    AddCommentParams,
    CreateIncidentParams,
    ListIncidentsParams,
    ResolveIncidentParams,
    UpdateIncidentParams,
)
from servicenow_mcp.tools.incident_tools import (
    add_comment as add_comment_tool,
)
from servicenow_mcp.tools.incident_tools import (
    create_incident as create_incident_tool,
)
from servicenow_mcp.tools.incident_tools import (
    list_incidents as list_incidents_tool,
)
from servicenow_mcp.tools.incident_tools import (
    resolve_incident as resolve_incident_tool,
)
from servicenow_mcp.tools.incident_tools import (
    update_incident as update_incident_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    CreateArticleParams,
    CreateKnowledgeBaseParams,
    GetArticleParams,
    ListArticlesParams,
    ListKnowledgeBasesParams,
    PublishArticleParams,
    UpdateArticleParams,
)
from servicenow_mcp.tools.knowledge_base import (
    CreateCategoryParams as CreateKBCategoryParams,  # Aliased
)
from servicenow_mcp.tools.knowledge_base import (
    ListCategoriesParams as ListKBCategoriesParams,  # Aliased
)
from servicenow_mcp.tools.knowledge_base import (
    create_article as create_article_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    # create_category aliased in function call
    create_knowledge_base as create_knowledge_base_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    get_article as get_article_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    list_articles as list_articles_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    # list_categories aliased in function call
    list_knowledge_bases as list_knowledge_bases_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    publish_article as publish_article_tool,
)
from servicenow_mcp.tools.knowledge_base import (
    update_article as update_article_tool,
)
from servicenow_mcp.tools.script_include_tools import (
    CreateScriptIncludeParams,
    DeleteScriptIncludeParams,
    GetScriptIncludeParams,
    ListScriptIncludesParams,
    ScriptIncludeResponse,
    UpdateScriptIncludeParams,
)
from servicenow_mcp.tools.script_include_tools import (
    create_script_include as create_script_include_tool,
)
from servicenow_mcp.tools.script_include_tools import (
    delete_script_include as delete_script_include_tool,
)
from servicenow_mcp.tools.script_include_tools import (
    get_script_include as get_script_include_tool,
)
from servicenow_mcp.tools.script_include_tools import (
    list_script_includes as list_script_includes_tool,
)
from servicenow_mcp.tools.script_include_tools import (
    update_script_include as update_script_include_tool,
)
from servicenow_mcp.tools.user_tools import (
    AddGroupMembersParams,
    CreateGroupParams,
    CreateUserParams,
    GetUserParams,
    ListGroupsParams,
    ListUsersParams,
    RemoveGroupMembersParams,
    UpdateGroupParams,
    UpdateUserParams,
)
from servicenow_mcp.tools.user_tools import (
    add_group_members as add_group_members_tool,
)
from servicenow_mcp.tools.user_tools import (
    create_group as create_group_tool,
)
from servicenow_mcp.tools.user_tools import (
    create_user as create_user_tool,
)
from servicenow_mcp.tools.user_tools import (
    get_user as get_user_tool,
)
from servicenow_mcp.tools.user_tools import (
    list_groups as list_groups_tool,
)
from servicenow_mcp.tools.user_tools import (
    list_users as list_users_tool,
)
from servicenow_mcp.tools.user_tools import (
    remove_group_members as remove_group_members_tool,
)
from servicenow_mcp.tools.user_tools import (
    update_group as update_group_tool,
)
from servicenow_mcp.tools.user_tools import (
    update_user as update_user_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    ActivateWorkflowParams,
    AddWorkflowActivityParams,
    CreateWorkflowParams,
    DeactivateWorkflowParams,
    DeleteWorkflowActivityParams,
    GetWorkflowActivitiesParams,
    GetWorkflowDetailsParams,
    ListWorkflowsParams,
    ListWorkflowVersionsParams,
    ReorderWorkflowActivitiesParams,
    UpdateWorkflowActivityParams,
    UpdateWorkflowParams,
)
from servicenow_mcp.tools.workflow_tools import (
    activate_workflow as activate_workflow_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    add_workflow_activity as add_workflow_activity_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    create_workflow as create_workflow_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    deactivate_workflow as deactivate_workflow_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    delete_workflow_activity as delete_workflow_activity_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    get_workflow_activities as get_workflow_activities_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    get_workflow_details as get_workflow_details_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    list_workflow_versions as list_workflow_versions_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    list_workflows as list_workflows_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    reorder_workflow_activities as reorder_workflow_activities_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    update_workflow as update_workflow_tool,
)
from servicenow_mcp.tools.workflow_tools import (
    update_workflow_activity as update_workflow_activity_tool,
)
from servicenow_mcp.tools.story_tools import (
    CreateStoryParams,
    UpdateStoryParams,
    ListStoriesParams,
    ListStoryDependenciesParams,
    CreateStoryDependencyParams,
    DeleteStoryDependencyParams,
)
from servicenow_mcp.tools.story_tools import (
    create_story as create_story_tool,
    update_story as update_story_tool,
    list_stories as list_stories_tool,
    list_story_dependencies as list_story_dependencies_tool,
    create_story_dependency as create_story_dependency_tool,
    delete_story_dependency as delete_story_dependency_tool,
)
from servicenow_mcp.tools.epic_tools import (
    CreateEpicParams,
    UpdateEpicParams,
    ListEpicsParams,
)
from servicenow_mcp.tools.epic_tools import (
    create_epic as create_epic_tool,
    update_epic as update_epic_tool,
    list_epics as list_epics_tool,
)
from servicenow_mcp.tools.scrum_task_tools import (
    CreateScrumTaskParams,
    UpdateScrumTaskParams,
    ListScrumTasksParams,
)
from servicenow_mcp.tools.scrum_task_tools import (
    create_scrum_task as create_scrum_task_tool,
    update_scrum_task as update_scrum_task_tool,
    list_scrum_tasks as list_scrum_tasks_tool,
)
from servicenow_mcp.tools.project_tools import (
    CreateProjectParams,
    UpdateProjectParams,
    ListProjectsParams,
)
from servicenow_mcp.tools.project_tools import (
    create_project as create_project_tool,
    update_project as update_project_tool,
    list_projects as list_projects_tool,
)

from servicenow_mcp.tools.developer_ui_action import (
    CreateUIActionParams,
    UpdateUIActionParams,
    ListUIActionsParams,
    GetUIActionParams,
    DeleteUIActionParams,
)

from servicenow_mcp.tools.developer_ui_action import (
    create_ui_action as create_ui_action_tool,
    update_ui_action as update_ui_action_tool,
    list_ui_actions as list_ui_actions_tool,
    get_ui_action as get_ui_action_tool,
    delete_ui_action as delete_ui_action_tool,
)

from servicenow_mcp.tools.developer_acl import (
    CreateACLParams,
    UpdateACLParams,
    ListACLsParams,
    GetACLParams,
    DeleteACLParams,
)
from servicenow_mcp.tools.developer_acl import (
    create_acl as create_acl_tool,
    update_acl as update_acl_tool,
    list_acls as list_acls_tool,
    get_acl as get_acl_tool,
    delete_acl as delete_acl_tool,
)

from servicenow_mcp.tools.developer_elevate_permissions import (
    SecurityElevationParams,
)
from servicenow_mcp.tools.developer_elevate_permissions import (
    security_elevation as security_elevation_tool,
)

# Add imports for the inbound email action tool parameters and functions
from servicenow_mcp.tools.developer_inbound_email_actions import (
    CreateInboundEmailActionParams,
    UpdateInboundEmailActionParams,
    ListInboundEmailActionsParams,
    GetInboundEmailActionParams,
    DeleteInboundEmailActionParams,
)
from servicenow_mcp.tools.developer_inbound_email_actions import (
    create_inbound_email_action as create_inbound_email_action_tool,
    update_inbound_email_action as update_inbound_email_action_tool,
    list_inbound_email_actions as list_inbound_email_actions_tool,
    get_inbound_email_action as get_inbound_email_action_tool,
    delete_inbound_email_action as delete_inbound_email_action_tool,
)

from servicenow_mcp.tools.developer_table import (
    CreateTableParams,
    CreateTableColumnParams,
    UpdateTableParams,
    UpdateTableColumnParams,
    ListTablesParams,
    ListTableColumnsParams,
    GetTableParams,
    GetTableColumnParams,
)
from servicenow_mcp.tools.developer_table import (
    create_table as create_table_tool,
    create_table_column as create_table_column_tool,
    update_table as update_table_tool,
    update_table_column as update_table_column_tool,
    list_tables as list_tables_tool,
    list_table_columns as list_table_columns_tool,
    get_table as get_table_tool,
    get_table_column as get_table_column_tool,
)


from servicenow_mcp.tools.developer_table_choice import (
    CreateChoiceParams,
    UpdateChoiceParams,
    ListChoicesParams,
    GetChoiceParams,
    DeleteChoiceParams,
    BulkCreateChoicesParams,
    ReorderChoicesParams,
)
from servicenow_mcp.tools.developer_table_choice import (
    create_choice as create_choice_tool,
    update_choice as update_choice_tool,
    list_choices as list_choices_tool,
    get_choice as get_choice_tool,
    delete_choice as delete_choice_tool,
    bulk_create_choices as bulk_create_choices_tool,
    reorder_choices as reorder_choices_tool,
)

# Email Notification Actions
from servicenow_mcp.tools.developer_notification import (
    CreateEmailNotificationParams,
    UpdateEmailNotificationParams,
    ListEmailNotificationsParams,
    GetEmailNotificationParams,
    DeleteEmailNotificationParams,
)

from servicenow_mcp.tools.developer_notification import (
    create_email_notification as create_email_notification_tool,
    update_email_notification as update_email_notification_tool,
    list_email_notifications as list_email_notifications_tool,
    get_email_notification as get_email_notification_tool,
    delete_email_notification as delete_email_notification_tool,
)

# Application Menu Items
from servicenow_mcp.tools.menu.developer_menu_application import (
    CreateApplicationMenuParams,
    UpdateApplicationMenuParams,
    ListApplicationMenusParams,
    GetApplicationMenuParams,
    DeleteApplicationMenuParams,
)

from servicenow_mcp.tools.menu.developer_menu_application import (
    create_application_menu as create_application_menu_tool,
    update_application_menu as update_application_menu_tool,
    list_application_menus as list_application_menus_tool,
    get_application_menu as get_application_menu_tool,
    delete_application_menu as delete_application_menu_tool,
)

from servicenow_mcp.tools.menu.developer_menu_module import (
    CreateAppModuleParams,
    UpdateAppModuleParams,
    ListAppModulesParams,
)
from servicenow_mcp.tools.menu.developer_menu_module import (
    create_app_module as create_app_module_tool,
    update_app_module as update_app_module_tool,
    list_app_modules as list_app_modules_tool,
    get_app_module as get_app_module_tool,
    delete_app_module as delete_app_module_tool,
)

from servicenow_mcp.tools.developer_user_role import (
    AssignUserRoleParams,
    RemoveUserRoleParams,
    ListUserRolesParams,
    BulkAssignRolesParams,
    BulkRemoveRolesParams,
)
from servicenow_mcp.tools.developer_user_role import (
    assign_user_role as assign_user_role_tool,
    remove_user_role as remove_user_role_tool,
    list_user_roles as list_user_roles_tool,
    bulk_assign_user_roles as bulk_assign_user_roles_tool,
    bulk_remove_user_roles as bulk_remove_user_roles_tool,
)

from servicenow_mcp.tools.developer_esc_quicklinks import (
    CreateQuickLinkParams,
    UpdateQuickLinkParams,
    ListQuickLinksParams,
    GetQuickLinkParams,
    DeleteQuickLinkParams,
)
from servicenow_mcp.tools.developer_esc_quicklinks import (
    create_quick_link as create_quick_link_tool,
    update_quick_link as update_quick_link_tool,
    list_quick_links as list_quick_links_tool,
    get_quick_link as get_quick_link_tool,
    delete_quick_link as delete_quick_link_tool,
)

from servicenow_mcp.tools.developer_assignment_rule import (
    CreateAssignmentRuleParams,
    UpdateAssignmentRuleParams,
    ListAssignmentRulesParams,
    GetAssignmentRuleParams,
    DeleteAssignmentRuleParams,
)
from servicenow_mcp.tools.developer_assignment_rule import (
    create_assignment_rule as create_assignment_rule_tool,
    update_assignment_rule as update_assignment_rule_tool,
    list_assignment_rules as list_assignment_rules_tool,
    get_assignment_rule as get_assignment_rule_tool,
    delete_assignment_rule as delete_assignment_rule_tool,
)

from servicenow_mcp.tools.developer_email_template import (
    CreateEmailTemplateParams,
    UpdateEmailTemplateParams,
    ListEmailTemplatesParams,
    GetEmailTemplateParams,
    DeleteEmailTemplateParams,
    CloneEmailTemplateParams,
)
from servicenow_mcp.tools.developer_email_template import (
    create_email_template as create_email_template_tool,
    update_email_template as update_email_template_tool,
    list_email_templates as list_email_templates_tool,
    get_email_template as get_email_template_tool,
    delete_email_template as delete_email_template_tool,
    clone_email_template as clone_email_template_tool,
)

from servicenow_mcp.tools.portal.developer_portal import (
    CreatePortalParams,
    UpdatePortalParams,
    ListPortalsParams,
    GetPortalParams,
    DeletePortalParams,
)
from servicenow_mcp.tools.portal.developer_portal import (
    create_portal as create_portal_tool,
    update_portal as update_portal_tool,
    list_portals as list_portals_tool,
    get_portal as get_portal_tool,
    delete_portal as delete_portal_tool,
)

from servicenow_mcp.tools.portal.developer_portal_instance import (
    CreateWidgetInstanceParams,
    UpdateWidgetInstanceParams,
    ListWidgetInstancesParams,
    GetWidgetInstanceParams,
    DeleteWidgetInstanceParams,
    CloneWidgetInstanceParams,
    BulkUpdateWidgetInstancesParams,
)

from servicenow_mcp.tools.portal.developer_portal_instance import (
    create_widget_instance as create_widget_instance_tool,
    update_widget_instance as update_widget_instance_tool,
    list_widget_instances as list_widget_instances_tool,
    get_widget_instance as get_widget_instance_tool,
    delete_widget_instance as delete_widget_instance_tool,
    clone_widget_instance as clone_widget_instance_tool,
    bulk_update_widget_instances as bulk_update_widget_instances_tool,
)

from servicenow_mcp.tools.portal.developer_portal_page import (
    CreatePortalPageParams,
    UpdatePortalPageParams,
    ListPortalPagesParams,
    GetPortalPageParams,
    ClonePortalPageParams,
    DeletePortalPageParams,
)
from servicenow_mcp.tools.portal.developer_portal_page import (
    create_portal_page as create_portal_page_tool,
    update_portal_page as update_portal_page_tool,
    list_portal_pages as list_portal_pages_tool,
    get_portal_page as get_portal_page_tool,
    clone_portal_page as clone_portal_page_tool,
    delete_portal_page as delete_portal_page_tool,
)

from servicenow_mcp.tools.portal.developer_portal_row import (
    CreatePortalRowParams,
    UpdatePortalRowParams,
    ListPortalRowsParams,
    GetPortalRowParams,
    ClonePortalRowParams,
    DeletePortalRowParams,
    ReorderPortalRowsParams,
)
from servicenow_mcp.tools.portal.developer_portal_row import (
    create_portal_row as create_portal_row_tool,
    update_portal_row as update_portal_row_tool,
    list_portal_rows as list_portal_rows_tool,
    get_portal_row as get_portal_row_tool,
    clone_portal_row as clone_portal_row_tool,
    delete_portal_row as delete_portal_row_tool,
    reorder_portal_rows as reorder_portal_rows_tool,
)

from servicenow_mcp.tools.portal.developer_portal_column import (
    CreatePortalColumnParams,
    UpdatePortalColumnParams,
    ListPortalColumnsParams,
    GetPortalColumnParams,
    ClonePortalColumnParams,
    DeletePortalColumnParams,
    ReorderPortalColumnsParams,
    CreateResponsiveGridParams,
)
from servicenow_mcp.tools.portal.developer_portal_column import (
    create_portal_column as create_portal_column_tool,
    update_portal_column as update_portal_column_tool,
    list_portal_columns as list_portal_columns_tool,
    get_portal_column as get_portal_column_tool,
    clone_portal_column as clone_portal_column_tool,
    delete_portal_column as delete_portal_column_tool,
    reorder_portal_columns as reorder_portal_columns_tool,
    create_responsive_grid as create_responsive_grid_tool,
)

from servicenow_mcp.tools.portal.developer_portal_container import (
    CreatePortalContainerParams,
    UpdatePortalContainerParams,
    ListPortalContainersParams,
    GetPortalContainerParams,
    ClonePortalContainerParams,
    DeletePortalContainerParams,
    ReorderPortalContainersParams,
)

from servicenow_mcp.tools.portal.developer_portal_container import (
    create_portal_container as create_portal_container_tool,
    update_portal_container as update_portal_container_tool,
    list_portal_containers as list_portal_containers_tool,
    get_portal_container as get_portal_container_tool,
    clone_portal_container as clone_portal_container_tool,
    delete_portal_container as delete_portal_container_tool,
    reorder_portal_containers as reorder_portal_containers_tool,
)

from servicenow_mcp.tools.service_catalog_management import (
    CreateServiceCatalogParams,
    UpdateServiceCatalogParams,
    ListServiceCatalogsParams,
    GetServiceCatalogParams,
    DeleteServiceCatalogParams,
)
from servicenow_mcp.tools.service_catalog_management import (
    create_service_catalog as create_service_catalog_tool,
    update_service_catalog as update_service_catalog_tool,
    list_service_catalogs as list_service_catalogs_tool,
    get_service_catalog as get_service_catalog_tool,
    delete_service_catalog as delete_service_catalog_tool,
)

# Define a type alias for the Pydantic models or dataclasses used for params
ParamsModel = Type[Any]  # Use Type[Any] for broader compatibility initially

# Define the structure of the tool definition tuple
ToolDefinition = Tuple[
    Callable,  # Implementation function
    ParamsModel,  # Pydantic model for parameters
    Type,  # Return type annotation (used for hints, not strictly enforced by low-level server)
    str,  # Description
    str,  # Serialization method ('str', 'json', 'dict', 'model_dump', etc.)
]


def get_tool_definitions(
    create_kb_category_tool_impl: Callable, list_kb_categories_tool_impl: Callable
) -> Dict[str, ToolDefinition]:
    """
    Returns a dictionary containing definitions for all available ServiceNow tools.

    This centralizes the tool definitions for use in the server implementation.
    Pass aliased functions for KB categories directly.

    Returns:
        Dict[str, ToolDefinition]: A dictionary mapping tool names to their definitions.
    """
    tool_definitions: Dict[str, ToolDefinition] = {
        # Incident Tools
        "create_incident": (
            create_incident_tool,
            CreateIncidentParams,
            str,
            "Create a new incident in ServiceNow",
            "str",
        ),
        "update_incident": (
            update_incident_tool,
            UpdateIncidentParams,
            str,
            "Update an existing incident in ServiceNow",
            "str",
        ),
        "add_comment": (
            add_comment_tool,
            AddCommentParams,
            str,
            "Add a comment to an incident in ServiceNow",
            "str",
        ),
        "resolve_incident": (
            resolve_incident_tool,
            ResolveIncidentParams,
            str,
            "Resolve an incident in ServiceNow",
            "str",
        ),
        "list_incidents": (
            list_incidents_tool,
            ListIncidentsParams,
            str,  # Expects JSON string
            "List incidents from ServiceNow",
            "json",  # Tool returns list/dict, needs JSON dump
        ),
        # Catalog Tools
        "list_catalog_items": (
            list_catalog_items_tool,
            ListCatalogItemsParams,
            str,  # Expects JSON string
            "List service catalog items.",
            "json",  # Tool returns list/dict
        ),
        "get_catalog_item": (
            get_catalog_item_tool,
            GetCatalogItemParams,
            str,  # Expects JSON string
            "Get a specific service catalog item.",
            "json_dict",  # Tool returns Pydantic model
        ),
        "list_catalog_categories": (
            list_catalog_categories_tool,
            ListCatalogCategoriesParams,
            str,  # Expects JSON string
            "List service catalog categories.",
            "json",  # Tool returns list/dict
        ),
        "create_catalog_category": (
            create_catalog_category_tool,
            CreateCatalogCategoryParams,
            str,  # Expects JSON string
            "Create a new service catalog category.",
            "json_dict",  # Tool returns Pydantic model
        ),
        "update_catalog_category": (
            update_catalog_category_tool,
            UpdateCatalogCategoryParams,
            str,  # Expects JSON string
            "Update an existing service catalog category.",
            "json_dict",  # Tool returns Pydantic model
        ),
        "move_catalog_items": (
            move_catalog_items_tool,
            MoveCatalogItemsParams,
            str,  # Expects JSON string
            "Move catalog items to a different category.",
            "json_dict",  # Tool returns Pydantic model
        ),
        "get_optimization_recommendations": (
            get_optimization_recommendations_tool,
            OptimizationRecommendationsParams,
            str,  # Expects JSON string
            "Get optimization recommendations for the service catalog.",
            "json",  # Tool returns list/dict
        ),
        "update_catalog_item": (
            update_catalog_item_tool,
            UpdateCatalogItemParams,
            str,  # Expects JSON string
            "Update a service catalog item.",
            "json",  # Tool returns Pydantic model
        ),
 
        # Change Management Tools
        "create_change_request": (
            create_change_request_tool,
            CreateChangeRequestParams,
            str,
            "Create a new change request in ServiceNow",
            "str",
        ),
        "update_change_request": (
            update_change_request_tool,
            UpdateChangeRequestParams,
            str,
            "Update an existing change request in ServiceNow",
            "str",
        ),
        "list_change_requests": (
            list_change_requests_tool,
            ListChangeRequestsParams,
            str,  # Expects JSON string
            "List change requests from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "get_change_request_details": (
            get_change_request_details_tool,
            GetChangeRequestDetailsParams,
            str,  # Expects JSON string
            "Get detailed information about a specific change request",
            "json",  # Tool returns list/dict
        ),
        "add_change_task": (
            add_change_task_tool,
            AddChangeTaskParams,
            str,  # Expects JSON string
            "Add a task to a change request",
            "json_dict",  # Tool returns Pydantic model
        ),
        "submit_change_for_approval": (
            submit_change_for_approval_tool,
            SubmitChangeForApprovalParams,
            str,
            "Submit a change request for approval",
            "str",  # Tool returns simple message
        ),
        "approve_change": (
            approve_change_tool,
            ApproveChangeParams,
            str,
            "Approve a change request",
            "str",  # Tool returns simple message
        ),
        "reject_change": (
            reject_change_tool,
            RejectChangeParams,
            str,
            "Reject a change request",
            "str",  # Tool returns simple message
        ),
        # Workflow Management Tools
        "list_workflows": (
            list_workflows_tool,
            ListWorkflowsParams,
            str,  # Expects JSON string
            "List workflows from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "get_workflow_details": (
            get_workflow_details_tool,
            GetWorkflowDetailsParams,
            str,  # Expects JSON string
            "Get detailed information about a specific workflow",
            "json",  # Tool returns list/dict
        ),
        "list_workflow_versions": (
            list_workflow_versions_tool,
            ListWorkflowVersionsParams,
            str,  # Expects JSON string
            "List workflow versions from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "get_workflow_activities": (
            get_workflow_activities_tool,
            GetWorkflowActivitiesParams,
            str,  # Expects JSON string
            "Get activities for a specific workflow",
            "json",  # Tool returns list/dict
        ),
        "create_workflow": (
            create_workflow_tool,
            CreateWorkflowParams,
            str,  # Expects JSON string
            "Create a new workflow in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "update_workflow": (
            update_workflow_tool,
            UpdateWorkflowParams,
            str,  # Expects JSON string
            "Update an existing workflow in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "activate_workflow": (
            activate_workflow_tool,
            ActivateWorkflowParams,
            str,
            "Activate a workflow in ServiceNow",
            "str",  # Tool returns simple message
        ),
        "deactivate_workflow": (
            deactivate_workflow_tool,
            DeactivateWorkflowParams,
            str,
            "Deactivate a workflow in ServiceNow",
            "str",  # Tool returns simple message
        ),
        "add_workflow_activity": (
            add_workflow_activity_tool,
            AddWorkflowActivityParams,
            str,  # Expects JSON string
            "Add a new activity to a workflow in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "update_workflow_activity": (
            update_workflow_activity_tool,
            UpdateWorkflowActivityParams,
            str,  # Expects JSON string
            "Update an existing activity in a workflow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "delete_workflow_activity": (
            delete_workflow_activity_tool,
            DeleteWorkflowActivityParams,
            str,
            "Delete an activity from a workflow",
            "str",  # Tool returns simple message
        ),
        "reorder_workflow_activities": (
            reorder_workflow_activities_tool,
            ReorderWorkflowActivitiesParams,
            str,
            "Reorder activities in a workflow",
            "str",  # Tool returns simple message
        ),
        # Changeset Management Tools
        "list_changesets": (
            list_changesets_tool,
            ListChangesetsParams,
            str,  # Expects JSON string
            "List changesets from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "get_changeset_details": (
            get_changeset_details_tool,
            GetChangesetDetailsParams,
            str,  # Expects JSON string
            "Get detailed information about a specific changeset",
            "json",  # Tool returns list/dict
        ),
        "create_changeset": (
            create_changeset_tool,
            CreateChangesetParams,
            str,  # Expects JSON string
            "Create a new changeset in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "update_changeset": (
            update_changeset_tool,
            UpdateChangesetParams,
            str,  # Expects JSON string
            "Update an existing changeset in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "commit_changeset": (
            commit_changeset_tool,
            CommitChangesetParams,
            str,
            "Commit a changeset in ServiceNow",
            "str",  # Tool returns simple message
        ),
        "publish_changeset": (
            publish_changeset_tool,
            PublishChangesetParams,
            str,
            "Publish a changeset in ServiceNow",
            "str",  # Tool returns simple message
        ),
        "add_file_to_changeset": (
            add_file_to_changeset_tool,
            AddFileToChangesetParams,
            str,
            "Add a file to a changeset in ServiceNow",
            "str",  # Tool returns simple message
        ),
        # Script Include Tools
        "list_script_includes": (
            list_script_includes_tool,
            ListScriptIncludesParams,
            Dict[str, Any],  # Expects dict
            "List script includes from ServiceNow",
            "raw_dict",  # Tool returns raw dict
        ),
        "get_script_include": (
            get_script_include_tool,
            GetScriptIncludeParams,
            Dict[str, Any],  # Expects dict
            "Get a specific script include from ServiceNow",
            "raw_dict",  # Tool returns raw dict
        ),
        "create_script_include": (
            create_script_include_tool,
            CreateScriptIncludeParams,
            ScriptIncludeResponse,  # Expects Pydantic model
            "Create a new script include in ServiceNow",
            "raw_pydantic",  # Tool returns Pydantic model
        ),
        "update_script_include": (
            update_script_include_tool,
            UpdateScriptIncludeParams,
            ScriptIncludeResponse,  # Expects Pydantic model
            "Update an existing script include in ServiceNow",
            "raw_pydantic",  # Tool returns Pydantic model
        ),
        "delete_script_include": (
            delete_script_include_tool,
            DeleteScriptIncludeParams,
            str,  # Expects JSON string
            "Delete a script include in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        # Knowledge Base Tools
        "create_knowledge_base": (
            create_knowledge_base_tool,
            CreateKnowledgeBaseParams,
            str,  # Expects JSON string
            "Create a new knowledge base in ServiceNow",
            "json_dict",  # Tool returns Pydantic model
        ),
        "list_knowledge_bases": (
            list_knowledge_bases_tool,
            ListKnowledgeBasesParams,
            Dict[str, Any],  # Expects dict
            "List knowledge bases from ServiceNow",
            "raw_dict",  # Tool returns raw dict
        ),
        # Use the passed-in implementations for aliased KB category tools
        "create_category": (
            create_kb_category_tool_impl,  # Use passed function
            CreateKBCategoryParams,
            str,  # Expects JSON string
            "Create a new category in a knowledge base",
            "json_dict",  # Tool returns Pydantic model
        ),
        "create_article": (
            create_article_tool,
            CreateArticleParams,
            str,  # Expects JSON string
            "Create a new knowledge article",
            "json_dict",  # Tool returns Pydantic model
        ),
        "update_article": (
            update_article_tool,
            UpdateArticleParams,
            str,  # Expects JSON string
            "Update an existing knowledge article",
            "json_dict",  # Tool returns Pydantic model
        ),
        "publish_article": (
            publish_article_tool,
            PublishArticleParams,
            str,  # Expects JSON string
            "Publish a knowledge article",
            "json_dict",  # Tool returns Pydantic model
        ),
        "list_articles": (
            list_articles_tool,
            ListArticlesParams,
            Dict[str, Any],  # Expects dict
            "List knowledge articles",
            "raw_dict",  # Tool returns raw dict
        ),
        "get_article": (
            get_article_tool,
            GetArticleParams,
            Dict[str, Any],  # Expects dict
            "Get a specific knowledge article by ID",
            "raw_dict",  # Tool returns raw dict
        ),
        # Use the passed-in implementations for aliased KB category tools
        "list_categories": (
            list_kb_categories_tool_impl,  # Use passed function
            ListKBCategoriesParams,
            Dict[str, Any],  # Expects dict
            "List categories in a knowledge base",
            "raw_dict",  # Tool returns raw dict
        ),
        # User Management Tools
        "create_user": (
            create_user_tool,
            CreateUserParams,
            Dict[str, Any],  # Expects dict
            "Create a new user in ServiceNow",
            "raw_dict",  # Tool returns raw dict
        ),
        "update_user": (
            update_user_tool,
            UpdateUserParams,
            Dict[str, Any],  # Expects dict
            "Update an existing user in ServiceNow",
            "raw_dict",
        ),
        "get_user": (
            get_user_tool,
            GetUserParams,
            Dict[str, Any],  # Expects dict
            "Get a specific user in ServiceNow",
            "raw_dict",
        ),
        "list_users": (
            list_users_tool,
            ListUsersParams,
            Dict[str, Any],  # Expects dict
            "List users in ServiceNow",
            "raw_dict",
        ),
        "create_group": (
            create_group_tool,
            CreateGroupParams,
            Dict[str, Any],  # Expects dict
            "Create a new group in ServiceNow",
            "raw_dict",
        ),
        "update_group": (
            update_group_tool,
            UpdateGroupParams,
            Dict[str, Any],  # Expects dict
            "Update an existing group in ServiceNow",
            "raw_dict",
        ),
        "add_group_members": (
            add_group_members_tool,
            AddGroupMembersParams,
            Dict[str, Any],  # Expects dict
            "Add members to an existing group in ServiceNow",
            "raw_dict",
        ),
        "remove_group_members": (
            remove_group_members_tool,
            RemoveGroupMembersParams,
            Dict[str, Any],  # Expects dict
            "Remove members from an existing group in ServiceNow",
            "raw_dict",
        ),
        "list_groups": (
            list_groups_tool,
            ListGroupsParams,
            Dict[str, Any],  # Expects dict
            "List groups from ServiceNow with optional filtering",
            "raw_dict",
        ),
        # Story Management Tools
        "create_story": (
            create_story_tool,
            CreateStoryParams,
            str,
            "Create a new story in ServiceNow",
            "str",
        ),
        "update_story": (
            update_story_tool,
            UpdateStoryParams,
            str,
            "Update an existing story in ServiceNow",
            "str",
        ),
        "list_stories": (
            list_stories_tool,
            ListStoriesParams,
            str,  # Expects JSON string
            "List stories from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "list_story_dependencies": (
            list_story_dependencies_tool,
            ListStoryDependenciesParams,
            str,  # Expects JSON string
            "List story dependencies from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "create_story_dependency": (
            create_story_dependency_tool,
            CreateStoryDependencyParams,
            str,
            "Create a dependency between two stories in ServiceNow",
            "str",
        ),
        "delete_story_dependency": (
            delete_story_dependency_tool,
            DeleteStoryDependencyParams,
            str,
            "Delete a story dependency in ServiceNow",
            "str",
        ),
        # Epic Management Tools
        "create_epic": (
            create_epic_tool,
            CreateEpicParams,
            str,
            "Create a new epic in ServiceNow",
            "str",
        ),
        "update_epic": (
            update_epic_tool,
            UpdateEpicParams,
            str,
            "Update an existing epic in ServiceNow",
            "str",
        ),
        "list_epics": (
            list_epics_tool,
            ListEpicsParams,
            str,  # Expects JSON string
            "List epics from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        # Scrum Task Management Tools
        "create_scrum_task": (
            create_scrum_task_tool,
            CreateScrumTaskParams,
            str,
            "Create a new scrum task in ServiceNow",
            "str",
        ),
        "update_scrum_task": (
            update_scrum_task_tool,
            UpdateScrumTaskParams,
            str,
            "Update an existing scrum task in ServiceNow",
            "str",
        ),
        "list_scrum_tasks": (
            list_scrum_tasks_tool,
            ListScrumTasksParams,
            str,  # Expects JSON string
            "List scrum tasks from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        # Project Management Tools
        "create_project": (
            create_project_tool,
            CreateProjectParams,
            str,
            "Create a new project in ServiceNow",
            "str",
        ),
        "update_project": (
            update_project_tool,
            UpdateProjectParams,
            str,
            "Update an existing project in ServiceNow",
            "str",
        ),
        "list_projects": (
            list_projects_tool,
            ListProjectsParams,
            str,  # Expects JSON string
            "List projects from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "create_ui_action": (
            create_ui_action_tool,
            CreateUIActionParams,
            str,  # Expects JSON string
            "Create a new UI action in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "update_ui_action": (
            update_ui_action_tool,
            UpdateUIActionParams,
            str,  # Expects JSON string
            "Update an existing UI action in ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "list_ui_actions": (
            list_ui_actions_tool,
            ListUIActionsParams,
            str,  # Expects JSON string
            "List UI actions from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "get_ui_action": (
            get_ui_action_tool,
            GetUIActionParams,
            str,  # Expects JSON string
            "Get a specific UI action from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "delete_ui_action": (
            delete_ui_action_tool,
            DeleteUIActionParams,
            str,  # Expects JSON string
            "Delete a UI action from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "create_acl": (
            create_acl_tool,
            CreateACLParams,
            str,  # Expects JSON string
            "Create a new ACL in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "update_acl": (
            update_acl_tool,
            UpdateACLParams,
            str,  # Expects JSON string
            "Update an existing ACL in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "list_acls": (
            list_acls_tool,
            ListACLsParams,
            str,  # Expects JSON string
            "List ACLs from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "get_acl": (
            get_acl_tool,
            GetACLParams,
            str,  # Expects JSON string
            "Get a specific ACL from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "delete_acl": (
            delete_acl_tool,
            DeleteACLParams,
            str,  # Expects JSON string
            "Delete an ACL from ServiceNow",
            "json",  # Tool returns list/dict
        ),
        "security_elevation": (
            security_elevation_tool,
            SecurityElevationParams,
            str,  # Expects JSON string
            "Elevate login session with specified roles",
            "json",  # Tool returns list/dict
        ),
        "create_inbound_email_action": (
            create_inbound_email_action_tool,
            CreateInboundEmailActionParams,
            str,  # Expects JSON string
            "Create a new inbound email action in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "update_inbound_email_action": (
            update_inbound_email_action_tool,
            UpdateInboundEmailActionParams,
            str,  # Expects JSON string
            "Update an existing inbound email action in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "list_inbound_email_actions": (
            list_inbound_email_actions_tool,
            ListInboundEmailActionsParams,
            str,  # Expects JSON string
            "List inbound email actions from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "get_inbound_email_action": (
            get_inbound_email_action_tool,
            GetInboundEmailActionParams,
            str,  # Expects JSON string
            "Get a specific inbound email action from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "delete_inbound_email_action": (
            delete_inbound_email_action_tool,
            DeleteInboundEmailActionParams,
            str,  # Expects JSON string
            "Delete an inbound email action from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "create_table": (
            create_table_tool,
            CreateTableParams,
            str,  # Expects JSON string
            "Create a new custom table in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "create_table_column": (
            create_table_column_tool,
            CreateTableColumnParams,
            str,  # Expects JSON string
            "Create a new column in a table.",
            "json",  # Tool returns list/dict
        ),
        "update_table": (
            update_table_tool,
            UpdateTableParams,
            str,  # Expects JSON string
            "Update an existing table in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "update_table_column": (
            update_table_column_tool,
            UpdateTableColumnParams,
            str,  # Expects JSON string
            "Update an existing table column in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "list_tables": (
            list_tables_tool,
            ListTablesParams,
            str,  # Expects JSON string
            "List tables from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "list_table_columns": (
            list_table_columns_tool,
            ListTableColumnsParams,
            str,  # Expects JSON string
            "List columns from a specific table in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "get_table": (
            get_table_tool,
            GetTableParams,
            str,  # Expects JSON string
            "Get details of a specific table from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "get_table_column": (
            get_table_column_tool,
            GetTableColumnParams,
            str,  # Expects JSON string
            "Get details of a specific table column from ServiceNow.",
            "json",  # Tool returns list/dict
        ),



        "create_choice": (
            create_choice_tool,
            CreateChoiceParams,
            str,  # Expects JSON string
            "Create a new choice for a choice field in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "update_choice": (
            update_choice_tool,
            UpdateChoiceParams,
            str,  # Expects JSON string
            "Update an existing choice in ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "list_choices": (
            list_choices_tool,
            ListChoicesParams,
            str,  # Expects JSON string
            "List choices for a specific field from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "get_choice": (
            get_choice_tool,
            GetChoiceParams,
            str,  # Expects JSON string
            "Get a specific choice from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "delete_choice": (
            delete_choice_tool,
            DeleteChoiceParams,
            str,  # Expects JSON string
            "Delete a choice from ServiceNow.",
            "json",  # Tool returns list/dict
        ),
        "bulk_create_choices": (
            bulk_create_choices_tool,
            BulkCreateChoicesParams,
            str,  # Expects JSON string
            "Create multiple choices at once for a choice field.",
            "json",  # Tool returns list/dict
        ),
        "reorder_choices": (
            reorder_choices_tool,
            ReorderChoicesParams,
            str,  # Expects JSON string
            "Reorder choices by updating their sequence values.",
            "json",  # Tool returns list/dict
        ),

        "create_email_notification": (
            create_email_notification_tool,
            CreateEmailNotificationParams,
            str,
            "Create a new email notification action in ServiceNow. This tool allows developers to set up outbound email notifications that trigger when specified events occur on a table, enabling automated system notifications for various business processes.",
            "json",
        ),
        "update_email_notification": (
            update_email_notification_tool,
            UpdateEmailNotificationParams,
            str,
            "Update an existing email notification action in ServiceNow. Modify notification settings, recipients, message content, triggers, and other configuration options for existing email notifications.",
            "json",
        ),
        "list_email_notifications": (
            list_email_notifications_tool,
            ListEmailNotificationsParams,
            str,
            "List email notification actions from ServiceNow. Filter by table, event name, active status, category, or other criteria to find specific notifications.",
            "json",
        ),
        "get_email_notification": (
            get_email_notification_tool,
            GetEmailNotificationParams,
            str,
            "Get detailed information about a specific email notification action from ServiceNow using its sys_id.",
            "json",
        ),
        "delete_email_notification": (
            delete_email_notification_tool,
            DeleteEmailNotificationParams,
            str,
            "Delete an email notification action from ServiceNow. This permanently removes the notification configuration.",
            "json",
        ),

        "create_application_menu": (
            create_application_menu_tool,
            CreateApplicationMenuParams,
            str,
            "Create a new application menu item in ServiceNow. This tool allows developers to add custom menu entries to the All menu and other navigation areas, providing access to tables, modules, or other functionality.",
            "json",
        ),
        "update_application_menu": (
            update_application_menu_tool,
            UpdateApplicationMenuParams,
            str,
            "Update an existing application menu item in ServiceNow. Modify menu properties including title, description, roles, order, category, and other display settings.",
            "json",
        ),
        "list_application_menus": (
            list_application_menus_tool,
            ListApplicationMenusParams,
            str,
            "List application menu items from ServiceNow. Filter by active status, category, device type, title, or other criteria to find specific menu items.",
            "json",
        ),
        "get_application_menu": (
            get_application_menu_tool,
            GetApplicationMenuParams,
            str,
            "Get detailed information about a specific application menu item from ServiceNow using its sys_id.",
            "json",
        ),
        "delete_application_menu": (
            delete_application_menu_tool,
            DeleteApplicationMenuParams,
            str,
            "Delete an application menu item from ServiceNow. This permanently removes the menu entry from the navigation interface.",
            "json",
        ),

        "create_app_module": (
            create_app_module_tool,
            CreateAppModuleParams,
            str,
            "Create a new application module menu item. Application modules are children of application menus and appear in the All menu navigation.",
            "json",
        ),
        "update_app_module": (
            update_app_module_tool,
            UpdateAppModuleParams,
            str,
            "Update an existing application module menu item. Modify properties like title, roles, filters, or display settings.",
            "json",
        ),
        "list_app_modules": (
            list_app_modules_tool,
            ListAppModulesParams,
            str,
            "List application module menu items with optional filtering by application, status, table, or roles.",
            "json",
        ),
        "get_app_module": (
            get_app_module_tool,
            str,
            str,
            "Get details of a specific application module menu item by its sys_id.",
            "json",
        ),
        "delete_app_module": (
            delete_app_module_tool,
            str,
            str,
            "Delete an application module menu item by its sys_id.",
            "json",
        ),

        "assign_user_role": (
            assign_user_role_tool,
            AssignUserRoleParams,
            str,
            "Assign a role to a user by creating a record in sys_user_has_role table",
            "json",
        ),
        "remove_user_role": (
            remove_user_role_tool,
            RemoveUserRoleParams,
            str,
            "Remove a role from a user by deleting the record from sys_user_has_role table",
            "json",
        ),
        "list_user_roles": (
            list_user_roles_tool,
            ListUserRolesParams,
            str,
            "List user role assignments from sys_user_has_role table",
            "json",
        ),
        "bulk_assign_user_roles": (
            bulk_assign_user_roles_tool,
            BulkAssignRolesParams,
            str,
            "Bulk assign roles to users by creating multiple records in sys_user_has_role table",
            "json",
        ),
        "bulk_remove_user_roles": (
            bulk_remove_user_roles_tool,
            BulkRemoveRolesParams,
            str,
            "Bulk remove roles from users by deleting multiple records from sys_user_has_role table",
            "json",
        ),

        "create_quick_link": (
            create_quick_link_tool,
            CreateQuickLinkParams,
            str,
            "Create a new employee center quick link for the Service Portal with customizable content types including pages, external links, knowledge articles, and catalog items.",
            "json",
        ),
        "update_quick_link": (
            update_quick_link_tool,
            UpdateQuickLinkParams,
            str,
            "Update an existing employee center quick link including its name, content type, display properties, and associated content references.",
            "json",
        ),
        "list_quick_links": (
            list_quick_links_tool,
            ListQuickLinksParams,
            str,
            "List employee center quick links with optional filtering by active status, content type, and other criteria to manage portal navigation.",
            "json",
        ),
        "get_quick_link": (
            get_quick_link_tool,
            GetQuickLinkParams,
            str,
            "Get detailed information about a specific employee center quick link including all configuration and content references.",
            "json",
        ),
        "delete_quick_link": (
            delete_quick_link_tool,
            DeleteQuickLinkParams,
            str,
            "Delete an employee center quick link from the Service Portal navigation to remove outdated or unused links.",
            "json",
        ),

        # Portal Configuration Management
        "create_portal": (
            create_portal_tool,
            CreatePortalParams,
            str,
            "Create a new portal configuration in ServiceNow with customizable settings including title, URL suffix, themes, pages, and various portal features",
            "json",
        ),
        "update_portal": (
            update_portal_tool,
            UpdatePortalParams,
            str,
            "Update an existing portal configuration in ServiceNow, modifying settings like title, theme, pages, and portal features",
            "json",
        ),
        "list_portals": (
            list_portals_tool,
            ListPortalsParams,
            str,
            "List portal configurations from ServiceNow with optional filtering by active status, default portal, and other criteria",
            "json",
        ),
        "get_portal": (
            get_portal_tool,
            GetPortalParams,
            str,
            "Get detailed information about a specific portal configuration by sys_id or URL suffix",
            "json",
        ),
        "delete_portal": (
            delete_portal_tool,
            DeletePortalParams,
            str,
            "Delete a portal configuration from ServiceNow by sys_id",
            "json",
        ),

        # Employee Center Widget Instance Management
        "create_widget_instance": (
            create_widget_instance_tool,
            CreateWidgetInstanceParams,
            str,
            "Create a new widget instance in ServiceNow Employee Center with specified configuration, styling, and placement parameters",
            "json",
        ),
        "update_widget_instance": (
            update_widget_instance_tool,
            UpdateWidgetInstanceParams,
            str,
            "Update an existing widget instance in ServiceNow Employee Center including configuration, styling, and placement properties",
            "json",
        ),
        "list_widget_instances": (
            list_widget_instances_tool,
            ListWidgetInstancesParams,
            str,
            "List widget instances from ServiceNow Employee Center with optional filtering by widget, column, or active status",
            "json",
        ),
        "get_widget_instance": (
            get_widget_instance_tool,
            GetWidgetInstanceParams,
            str,
            "Get detailed information about a specific widget instance from ServiceNow Employee Center",
            "json",
        ),
        "delete_widget_instance": (
            delete_widget_instance_tool,
            DeleteWidgetInstanceParams,
            str,
            "Delete a widget instance from ServiceNow Employee Center to remove it from portal pages",
            "json",
        ),
        "clone_widget_instance": (
            clone_widget_instance_tool,
            CloneWidgetInstanceParams,
            str,
            "Clone an existing widget instance to create a duplicate with optional modifications to configuration and placement",
            "json",
        ),
        "bulk_update_widget_instances": (
            bulk_update_widget_instances_tool,
            BulkUpdateWidgetInstancesParams,
            str,
            "Bulk update multiple widget instances simultaneously with the same property changes for efficient portal management",
            "json",
        ),

            # Portal Page tools
        "create_portal_page": (
            create_portal_page_tool,
            CreatePortalPageParams,
            str,
            "Create a new portal page in the sp_page table with configurable properties including title, CSS, roles, and visibility settings",
            "json",
        ),
        "update_portal_page": (
            update_portal_page_tool,
            UpdatePortalPageParams,
            str,
            "Update an existing portal page in the sp_page table by ID or sys_id, modifying properties like title, CSS, roles, and other configuration options",
            "json",
        ),
        "list_portal_pages": (
            list_portal_pages_tool,
            ListPortalPagesParams,
            str,
            "List portal pages from the sp_page table with optional filtering by category, public status, draft status, and other criteria",
            "json",
        ),
        "get_portal_page": (
            get_portal_page_tool,
            GetPortalPageParams,
            str,
            "Get detailed information about a specific portal page by ID or sys_id from the sp_page table",
            "json",
        ),
        "clone_portal_page": (
            clone_portal_page_tool,
            ClonePortalPageParams,
            str,
            "Clone an existing portal page to create a duplicate with optional modifications to title, description, CSS, and roles",
            "json",
        ),
        "delete_portal_page": (
            delete_portal_page_tool,
            DeletePortalPageParams,
            str,
            "Delete a portal page from the sp_page table by ID or sys_id",
            "json",
        ),

        # Portal Row tools
        "create_portal_row": (
            create_portal_row_tool,
            CreatePortalRowParams,
            str,
            "Create a new portal row in the sp_row table with configurable container, column, CSS class, order, and semantic tag properties",
            "json",
        ),
        "update_portal_row": (
            update_portal_row_tool,
            UpdatePortalRowParams,
            str,
            "Update an existing portal row in the sp_row table by sys_id, modifying properties like container, column, CSS class, order, and semantic tag",
            "json",
        ),
        "list_portal_rows": (
            list_portal_rows_tool,
            ListPortalRowsParams,
            str,
            "List portal rows from the sp_row table with optional filtering by container, column, semantic tag, and other criteria",
            "json",
        ),
        "get_portal_row": (
            get_portal_row_tool,
            GetPortalRowParams,
            str,
            "Get detailed information about a specific portal row by sys_id from the sp_row table",
            "json",
        ),
        "clone_portal_row": (
            clone_portal_row_tool,
            ClonePortalRowParams,
            str,
            "Clone an existing portal row to create a duplicate with optional modifications to container, column, CSS class, and semantic tag",
            "json",
        ),
        "delete_portal_row": (
            delete_portal_row_tool,
            DeletePortalRowParams,
            str,
            "Delete a portal row from the sp_row table by sys_id",
            "json",
        ),
        "reorder_portal_rows": (
            reorder_portal_rows_tool,
            ReorderPortalRowsParams,
            str,
            "Reorder portal rows within a container or column by updating their order values according to a specified sequence",
            "json",
        ),
        # Portal Column tools
        "create_portal_column": (
            create_portal_column_tool,
            CreatePortalColumnParams,
            str,
            "Create a new portal column in the sp_column table with configurable row, CSS class, responsive Bootstrap sizes, order, and semantic tag properties",
            "json",
        ),
        "update_portal_column": (
            update_portal_column_tool,
            UpdatePortalColumnParams,
            str,
            "Update an existing portal column in the sp_column table by sys_id, modifying properties like row, CSS class, responsive sizes, order, and semantic tag",
            "json",
        ),
        "list_portal_columns": (
            list_portal_columns_tool,
            ListPortalColumnsParams,
            str,
            "List portal columns from the sp_column table with optional filtering by row, semantic tag, size ranges, and other criteria",
            "json",
        ),
        "get_portal_column": (
            get_portal_column_tool,
            GetPortalColumnParams,
            str,
            "Get detailed information about a specific portal column by sys_id from the sp_column table including responsive size configurations",
            "json",
        ),
        "clone_portal_column": (
            clone_portal_column_tool,
            ClonePortalColumnParams,
            str,
            "Clone an existing portal column to create a duplicate with optional modifications to row, CSS class, responsive sizes, and semantic tag",
            "json",
        ),
        "delete_portal_column": (
            delete_portal_column_tool,
            DeletePortalColumnParams,
            str,
            "Delete a portal column from the sp_column table by sys_id",
            "json",
        ),
        "reorder_portal_columns": (
            reorder_portal_columns_tool,
            ReorderPortalColumnsParams,
            str,
            "Reorder portal columns within a row by updating their order values according to a specified sequence",
            "json",
        ),
        "create_responsive_grid": (
            create_responsive_grid_tool,
            CreateResponsiveGridParams,
            str,
            "Create a responsive grid layout by generating multiple columns with specified Bootstrap responsive configurations in a single operation",
            "json",
        ),

        "create_portal_container": (
            create_portal_container_tool,
            CreatePortalContainerParams,
            str,
            "Create a new portal container in the sp_container table with configurable page, styling, background, and layout properties",
            "json",
        ),
        "update_portal_container": (
            update_portal_container_tool,
            UpdatePortalContainerParams,
            str,
            "Update an existing portal container in the sp_container table by sys_id, modifying properties like page, styling, background, and layout settings",
            "json",
        ),
        "list_portal_containers": (
            list_portal_containers_tool,
            ListPortalContainersParams,
            str,
            "List portal containers from the sp_container table with optional filtering by page, semantic tag, width, and other criteria",
            "json",
        ),
        "get_portal_container": (
            get_portal_container_tool,
            GetPortalContainerParams,
            str,
            "Get detailed information about a specific portal container by sys_id or name from the sp_container table",
            "json",
        ),
        "clone_portal_container": (
            clone_portal_container_tool,
            ClonePortalContainerParams,
            str,
            "Clone an existing portal container to create a duplicate with optional modifications to styling, background, and target page",
            "json",
        ),
        "delete_portal_container": (
            delete_portal_container_tool,
            DeletePortalContainerParams,
            str,
            "Delete a portal container from the sp_container table by sys_id",
            "json",
        ),
        "reorder_portal_containers": (
            reorder_portal_containers_tool,
            ReorderPortalContainersParams,
            str,
            "Reorder portal containers within a page by updating their order values according to a specified sequence",
            "json",
        ),

        # Catalog Variables
        "create_catalog_variable": (
            create_catalog_variable_tool,
            CreateCatalogVariableParams,
            str,
            "Create a new catalog variable in the item_option_new table with configurable properties including type, label, mandatory status, field mappings, and choice configurations",
            "json",
        ),
        "list_catalog_variables": (
            list_catalog_variables_tool,
            ListCatalogVariablesParams,
            str,
            "List catalog variables for a specific catalog item from the item_option_new table with optional detailed information and pagination",
            "json",
        ),
        "update_catalog_variable": (
            update_catalog_variable_tool,
            UpdateCatalogVariableParams,
            str,
            "Update an existing catalog variable in the item_option_new table by sys_id, modifying properties like type, label, field mappings, and choice configurations",
            "json",
        ),
        "delete_catalog_variable": (
            delete_catalog_variable_tool,
            DeleteCatalogVariableParams,
            str,
            "Delete a catalog variable from the item_option_new table by sys_id to remove it from the catalog item",
            "json",
        ),
        "get_catalog_variable": (
            get_catalog_variable_tool,
            GetCatalogVariableParams,
            str,
            "Get detailed information about a specific catalog variable by sys_id from the item_option_new table",
            "json",
        ),

        # Assignment Rule Management Tools
        "create_assignment_rule": (
            create_assignment_rule_tool,
            CreateAssignmentRuleParams,
            str,
            "Create a new assignment rule in ServiceNow",
            "json",
        ),
        "update_assignment_rule": (
            update_assignment_rule_tool,
            UpdateAssignmentRuleParams,
            str,
            "Update an existing assignment rule in ServiceNow",
            "json",
        ),
        "list_assignment_rules": (
            list_assignment_rules_tool,
            ListAssignmentRulesParams,
            str,
            "List assignment rules from ServiceNow with optional filtering",
            "json",
        ),
        "get_assignment_rule": (
            get_assignment_rule_tool,
            GetAssignmentRuleParams,
            str,
            "Get a specific assignment rule from ServiceNow",
            "json",
        ),
        "delete_assignment_rule": (
            delete_assignment_rule_tool,
            DeleteAssignmentRuleParams,
            str,
            "Delete an assignment rule from ServiceNow",
            "json",
        ),

        # Email Template Management Tools
        "create_email_template": (
            create_email_template_tool,
            CreateEmailTemplateParams,
            str,
            "Create a new email template in ServiceNow",
            "json",
        ),
        "update_email_template": (
            update_email_template_tool,
            UpdateEmailTemplateParams,
            str,
            "Update an existing email template in ServiceNow",
            "json",
        ),
        "list_email_templates": (
            list_email_templates_tool,
            ListEmailTemplatesParams,
            str,
            "List email templates from ServiceNow with optional filtering",
            "json",
        ),
        "get_email_template": (
            get_email_template_tool,
            GetEmailTemplateParams,
            str,
            "Get a specific email template from ServiceNow",
            "json",
        ),
        "delete_email_template": (
            delete_email_template_tool,
            DeleteEmailTemplateParams,
            str,
            "Delete an email template from ServiceNow",
            "json",
        ),
        "clone_email_template": (
            clone_email_template_tool,
            CloneEmailTemplateParams,
            str,
            "Clone an existing email template in ServiceNow",
            "json",
        ),

        # Service Catalog Management Tools
        "create_service_catalog": (
            create_service_catalog_tool,
            CreateServiceCatalogParams,
            str,
            "Create a new service catalog in ServiceNow",
            "json",
        ),
        "update_service_catalog": (
            update_service_catalog_tool,
            UpdateServiceCatalogParams,
            str,
            "Update an existing service catalog in ServiceNow",
            "json",
        ),
        "list_service_catalogs": (
            list_service_catalogs_tool,
            ListServiceCatalogsParams,
            str,
            "List service catalogs from ServiceNow",
            "json",
        ),
        "get_service_catalog": (
            get_service_catalog_tool,
            GetServiceCatalogParams,
            str,
            "Get a specific service catalog from ServiceNow",
            "json",
        ),
        "delete_service_catalog": (
            delete_service_catalog_tool,
            DeleteServiceCatalogParams,
            str,
            "Delete a service catalog from ServiceNow",
            "json",
        ),

    }
    return tool_definitions
