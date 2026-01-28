"""
Callback Manager for Nuke Pipeline
Handles registration and execution of callback actions for various Nuke events.
"""

import nuke
import versioning


# Registry of callback actions mapped to Nuke events
CALLBACK_ACTIONS = {
    "OnScriptSave": [versioning.match_write_versions_to_script],
    "AfterRender": [versioning.version_script],
}


def register_write_callback(callback_type):
    """
    Register a write callback for the specified event type.
    
    Args:
        callback_type (str): The type of callback to register (e.g., "OnScriptSave", "AfterRender")
    
    Raises:
        ValueError: If callback_type is not recognized
    """
    if callback_type not in CALLBACK_ACTIONS:
        raise ValueError(f"Unknown callback type: {callback_type}. Valid types: {list(CALLBACK_ACTIONS.keys())}")
    
    _execute_callback("add", callback_type)


def unregister_write_callback(callback_type):
    """
    Unregister a write callback for the specified event type.
    
    Args:
        callback_type (str): The type of callback to unregister (e.g., "OnScriptSave", "AfterRender")
    
    Raises:
        ValueError: If callback_type is not recognized
    """
    if callback_type not in CALLBACK_ACTIONS:
        raise ValueError(f"Unknown callback type: {callback_type}. Valid types: {list(CALLBACK_ACTIONS.keys())}")
    
    _execute_callback("remove", callback_type)


def register_pipeline_callbacks(callback_type):
    """
    Alias for register_write_callback to match the function name used in menu.py.
    
    Args:
        callback_type (str): The type of callback to register
    """
    register_write_callback(callback_type)


def _execute_callback(action_type, callback_type):
    """
    Internal method to add or remove callbacks from Nuke.
    
    Args:
        action_type (str): Either "add" or "remove"
        callback_type (str): The type of callback (e.g., "OnScriptSave", "AfterRender")
    """
    actions = CALLBACK_ACTIONS.get(callback_type, [])
    
    for action in actions:
        # Construct the Nuke callback function name (e.g., "addOnScriptSave", "removeAfterRender")
        callback_function_name = f"{action_type}{callback_type}"
        callback_function = getattr(nuke, callback_function_name, None)
        
        if callback_function:
            try:
                callback_function(action)
            except Exception:
                pass  # Silently continue if callback registration fails


def get_registered_callbacks():
    """
    Get a dictionary of all registered callback types and their actions.
    
    Returns:
        dict: Copy of CALLBACK_ACTIONS registry
    """
    return CALLBACK_ACTIONS.copy()
