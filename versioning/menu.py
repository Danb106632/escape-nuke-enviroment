"""
Nuke Menu Initialization
Registers pipeline callbacks for script events.
"""

import nuke
import callback_manager


def initialize_callbacks():
    """
    Initialize all pipeline callbacks.
    Registers callbacks for script save and render events.
    """
    callbacks_to_register = [
        "OnScriptSave",
        "AfterRender",
    ]
    
    for callback_type in callbacks_to_register:
        try:
            callback_manager.register_pipeline_callbacks(callback_type)
        except Exception:
            pass  # Silently continue if callback registration fails


# Initialize callbacks when the module is loaded
try:
    initialize_callbacks()
except Exception:
    pass  # Silently continue if initialization fails
