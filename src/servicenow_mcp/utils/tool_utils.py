import importlib
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, Tuple, Type

from pydantic import BaseModel

# Define ToolDefinition type
ToolDefinition = Tuple[Callable, Type[BaseModel], Type, str, str]

def _discover_tool_functions_and_params():
    """
    Automatically discover tool functions and their corresponding parameter models.
    
    Returns:
        Tuple of (functions_dict, params_dict) where:
        - functions_dict: Maps function names to their implementations
        - params_dict: Maps function names to their parameter model classes
    """
    functions = {}
    params = {}
    
    # Get the path to the tools directory
    tools_dir = Path(__file__).parent.parent / "tools"
    
    # Define the subfolders to scan
    subfolders = ['catalog', 'developer', 'foundation', 'agile', 'notifications', 'knowledge', 'menu', 'portal', 'atf']
    
    for subfolder in subfolders:
        subfolder_path = tools_dir / subfolder
        if not subfolder_path.exists():
            continue
            
        # Scan all Python files in the subfolder
        for py_file in subfolder_path.glob('*.py'):
            if py_file.name.startswith('__'):
                continue  # Skip __init__.py and other special files
                
            # Construct module path
            module_name = f"servicenow_mcp.tools.{subfolder}.{py_file.stem}"
            
            try:
                # Import the module
                module = importlib.import_module(module_name)
                
                # Get all classes and functions from the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj) and obj.__module__ == module_name and not name.startswith('_'):
                        # This is a function defined in this module
                        functions[name] = obj
                    elif inspect.isclass(obj) and obj.__module__ == module_name and issubclass(obj, BaseModel):
                        # This is a Pydantic model class defined in this module
                        params[name] = obj
                        
            except ImportError as e:
                # Log the error but continue with other modules
                print(f"Warning: Could not import {module_name}: {e}")
                continue
    
    return functions, params

def _generate_tool_descriptions():
    """Generate descriptions for tools based on their docstrings and patterns."""
    descriptions = {
        # Pattern-based descriptions for common operations
        "create_": "Create a new {} in ServiceNow",
        "update_": "Update an existing {} in ServiceNow", 
        "list_": "List {} from ServiceNow",
        "get_": "Get a specific {} from ServiceNow",
        "delete_": "Delete a {} from ServiceNow",
        "add_": "Add {} in ServiceNow",
        "remove_": "Remove {} from ServiceNow",
        "upload_": "Upload {} to ServiceNow",
        "download_": "Download {} from ServiceNow",
        "clone_": "Clone an existing {} in ServiceNow",
        "bulk_": "Perform bulk operation on {} in ServiceNow",
        "move_": "Move {} in ServiceNow",
        "reorder_": "Reorder {} in ServiceNow",
        "activate_": "Activate {} in ServiceNow",
        "deactivate_": "Deactivate {} in ServiceNow",
        "approve_": "Approve {} in ServiceNow",
        "reject_": "Reject {} in ServiceNow",
        "resolve_": "Resolve {} in ServiceNow",
        "publish_": "Publish {} in ServiceNow",
        "commit_": "Commit {} in ServiceNow",
        "assign_": "Assign {} in ServiceNow",
        "submit_": "Submit {} in ServiceNow",
    }
    return descriptions

def _infer_tool_description(func_name: str, func_obj: Callable) -> str:
    """Infer tool description from function name and docstring."""
    # Try to get description from docstring first
    if func_obj.__doc__:
        # Extract first line of docstring as description
        first_line = func_obj.__doc__.strip().split('\n')[0].strip()
        if first_line and not first_line.startswith('Args:') and not first_line.startswith('Returns:'):
            return first_line
    
    # Fall back to pattern-based description
    descriptions = _generate_tool_descriptions()
    
    for pattern, template in descriptions.items():
        if func_name.startswith(pattern):
            # Extract object name from function name
            object_name = func_name[len(pattern):].replace('_', ' ')
            return template.format(object_name)
    
    # Default description
    return f"Execute {func_name.replace('_', ' ')} operation in ServiceNow"

def _match_function_to_params(func_name: str, params_dict: Dict[str, Type[BaseModel]]) -> Type[BaseModel]:
    """Match a function name to its parameter model class."""
    # Common patterns for matching function names to parameter classes
    patterns = [
        # Direct match: create_incident -> CreateIncidentParams
        lambda fn: ''.join(word.capitalize() for word in fn.split('_')) + 'Params',
        # Alternative: create_incident -> CreateIncident  
        lambda fn: ''.join(word.capitalize() for word in fn.split('_')),
        # Handle list functions: list_incidents -> ListIncidentsParams
        lambda fn: ''.join(word.capitalize() for word in fn.split('_')) + 'Params' if fn.startswith('list_') else None,
    ]
    
    for pattern in patterns:
        if pattern is None:
            continue
        param_class_name = pattern(func_name)
        if param_class_name and param_class_name in params_dict:
            return params_dict[param_class_name]
    
    # If no match found, return a generic BaseModel
    return BaseModel

def get_tool_definitions(
    create_kb_category_tool_impl: Callable, list_kb_categories_tool_impl: Callable
) -> Dict[str, ToolDefinition]:
    """
    Returns a dictionary containing definitions for all available ServiceNow tools.
    
    This function automatically discovers tools from all submodules and generates
    their definitions dynamically.

    Args:
        create_kb_category_tool_impl: Aliased function for KB categories
        list_kb_categories_tool_impl: Aliased function for KB categories
        
    Returns:
        Dict[str, ToolDefinition]: A dictionary mapping tool names to their definitions.
    """
    # Discover all functions and parameter models
    functions_dict, params_dict = _discover_tool_functions_and_params()
    
    # Generate tool definitions
    tool_definitions: Dict[str, ToolDefinition] = {}
    
    for func_name, func_obj in functions_dict.items():
        # Find matching parameter class
        param_class = _match_function_to_params(func_name, params_dict)
        
        # Generate description
        description = _infer_tool_description(func_name, func_obj)
        
        # Determine return type and output format
        return_type = str  # Default to string
        output_format = "json"  # Default to JSON
        
        # Add to tool definitions
        tool_definitions[func_name] = (
            func_obj,
            param_class,
            return_type,
            description,
            output_format,
        )
    
    # Handle special cases for KB category functions that are passed as parameters
    if create_kb_category_tool_impl:
        tool_definitions["create_category"] = (
            create_kb_category_tool_impl,
            params_dict.get("CreateCategoryParams", BaseModel),
            str,
            "Create a new category in a knowledge base",
            "json",
        )
    
    if list_kb_categories_tool_impl:
        tool_definitions["list_categories"] = (
            list_kb_categories_tool_impl,
            params_dict.get("ListCategoriesParams", BaseModel),
            str,
            "List categories in a knowledge base",
            "json",
        )
    
    return tool_definitions
