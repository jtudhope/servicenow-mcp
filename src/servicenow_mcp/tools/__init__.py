"""
Tools module for the ServiceNow MCP server.

This module automatically discovers and imports all tool functions from submodules.
"""

import importlib
import inspect
import os
from pathlib import Path
from typing import Any, Dict, List

def _discover_tools() -> Dict[str, Any]:
    """
    Automatically discover and import all tool functions from submodules.
    
    Returns:
        Dictionary mapping function names to their implementations
    """
    tools = {}
    all_exports = []
    
    # Get the path to the tools directory
    tools_dir = Path(__file__).parent
    
    # Define the subfolders to scan
    subfolders = ['catalog', 'developer', 'foundation', 'agile', 'notifications', 'knowledge', 'menu', 'portal']
    
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
                
                # Get all functions from the module
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    # Only include functions defined in this module (not imported ones)
                    if obj.__module__ == module_name and not name.startswith('_'):
                        tools[name] = obj
                        all_exports.append(name)
                        
            except ImportError as e:
                # Log the error but continue with other modules
                print(f"Warning: Could not import {module_name}: {e}")
                continue
    
    return tools, all_exports

# Discover and import all tools
_tools, _all_exports = _discover_tools()

# Add all discovered functions to the global namespace
globals().update(_tools)

# Set __all__ to all discovered function names
__all__ = sorted(_all_exports)