"""
Question Choice Management tools for the ServiceNow MCP server.

This module provides tools for managing Question Choices that are stored in the question_choice table.
Question Choices are records used to display as options on catalog variables where a multi select or select box is used.
"""

import logging
from typing import Optional, List

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class CreateQuestionChoiceParams(BaseModel):
    """Parameters for creating a question choice."""
    
    value: str = Field(..., description="Value of the choice (stored value)")
    text: str = Field(..., description="Display text of the choice")
    question: Optional[str] = Field(None, description="Question sys_id this choice belongs to")
    order: Optional[int] = Field(100, description="Display order of the choice")
    inactive: Optional[bool] = Field(False, description="Whether the choice is inactive")
    misc: Optional[str] = Field(None, description="Price for this choice")
    rec_misc: Optional[str] = Field(None, description="Recurring price for this choice")


class UpdateQuestionChoiceParams(BaseModel):
    """Parameters for updating a question choice."""
    
    choice_id: str = Field(..., description="Question choice sys_id")
    value: Optional[str] = Field(None, description="Value of the choice (stored value)")
    text: Optional[str] = Field(None, description="Display text of the choice")
    question: Optional[str] = Field(None, description="Question sys_id this choice belongs to")
    order: Optional[int] = Field(None, description="Display order of the choice")
    inactive: Optional[bool] = Field(None, description="Whether the choice is inactive")
    misc: Optional[str] = Field(None, description="Price for this choice")
    rec_misc: Optional[str] = Field(None, description="Recurring price for this choice")


class ListQuestionChoicesParams(BaseModel):
    """Parameters for listing question choices."""
    
    question: Optional[str] = Field(None, description="Filter by question sys_id")
    inactive: Optional[bool] = Field(None, description="Filter by inactive status")
    limit: int = Field(50, description="Maximum number of choices to return")
    offset: int = Field(0, description="Offset for pagination")


class QuestionChoiceResponse(BaseModel):
    """Response from question choice operations."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    choice: Optional[dict] = Field(None, description="Question choice data")
    choices: Optional[List[dict]] = Field(None, description="List of question choices")


def create_question_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CreateQuestionChoiceParams,
) -> QuestionChoiceResponse:
    """
    Create a new question choice in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for creating the question choice.

    Returns:
        Response with question choice creation result.
    """
    api_url = f"{config.api_url}/table/question_choice"

    data = {
        "value": params.value,
        "text": params.text,
    }

    if params.question:
        data["question"] = params.question
    if params.order is not None:
        data["order"] = params.order
    if params.inactive is not None:
        data["inactive"] = params.inactive
    if params.misc:
        data["misc"] = params.misc
    if params.rec_misc:
        data["rec_misc"] = params.rec_misc

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return QuestionChoiceResponse(
            success=True,
            message="Question choice created successfully",
            choice=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to create question choice: {e}")
        return QuestionChoiceResponse(
            success=False,
            message=f"Failed to create question choice: {str(e)}",
        )


def update_question_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateQuestionChoiceParams,
) -> QuestionChoiceResponse:
    """
    Update an existing question choice in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for updating the question choice.

    Returns:
        Response with question choice update result.
    """
    api_url = f"{config.api_url}/table/question_choice/{params.choice_id}"

    data = {}

    if params.value is not None:
        data["value"] = params.value
    if params.text is not None:
        data["text"] = params.text
    if params.question is not None:
        data["question"] = params.question
    if params.order is not None:
        data["order"] = params.order
    if params.inactive is not None:
        data["inactive"] = params.inactive
    if params.misc is not None:
        data["misc"] = params.misc
    if params.rec_misc is not None:
        data["rec_misc"] = params.rec_misc

    try:
        response = requests.patch(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return QuestionChoiceResponse(
            success=True,
            message="Question choice updated successfully",
            choice=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to update question choice: {e}")
        return QuestionChoiceResponse(
            success=False,
            message=f"Failed to update question choice: {str(e)}",
        )


def list_question_choices(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListQuestionChoicesParams,
) -> QuestionChoiceResponse:
    """
    List question choices in ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        params: Parameters for listing question choices.

    Returns:
        Response with list of question choices.
    """
    api_url = f"{config.api_url}/table/question_choice"

    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": "all",
    }

    # Build query filter
    query_parts = []
    if params.question:
        query_parts.append(f"question={params.question}")
    if params.inactive is not None:
        query_parts.append(f"inactive={str(params.inactive).lower()}")

    if query_parts:
        query_params["sysparm_query"] = "^".join(query_parts)

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", [])

        return QuestionChoiceResponse(
            success=True,
            message=f"Retrieved {len(result)} question choices",
            choices=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to list question choices: {e}")
        return QuestionChoiceResponse(
            success=False,
            message=f"Failed to list question choices: {str(e)}",
        )


def get_question_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    choice_id: str,
) -> QuestionChoiceResponse:
    """
    Get a specific question choice from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        choice_id: Question choice sys_id.

    Returns:
        Response with question choice data.
    """
    api_url = f"{config.api_url}/table/question_choice/{choice_id}"

    query_params = {
        "sysparm_display_value": "all",
    }

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        result = response.json().get("result", {})

        return QuestionChoiceResponse(
            success=True,
            message="Question choice retrieved successfully",
            choice=result,
        )

    except requests.RequestException as e:
        logger.error(f"Failed to get question choice: {e}")
        return QuestionChoiceResponse(
            success=False,
            message=f"Failed to get question choice: {str(e)}",
        )


def delete_question_choice(
    config: ServerConfig,
    auth_manager: AuthManager,
    choice_id: str,
) -> QuestionChoiceResponse:
    """
    Delete a question choice from ServiceNow.

    Args:
        config: Server configuration.
        auth_manager: Authentication manager.
        choice_id: Question choice sys_id.

    Returns:
        Response with deletion result.
    """
    api_url = f"{config.api_url}/table/question_choice/{choice_id}"

    try:
        response = requests.delete(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()

        return QuestionChoiceResponse(
            success=True,
            message="Question choice deleted successfully",
        )

    except requests.RequestException as e:
        logger.error(f"Failed to delete question choice: {e}")
        return QuestionChoiceResponse(
            success=False,
            message=f"Failed to delete question choice: {str(e)}",
        )