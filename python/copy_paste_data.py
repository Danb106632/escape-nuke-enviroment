"""
Copy/Paste Data Utility for Nuke
Allows saving and loading node selections to/from shared network locations.
"""

import platform
import nuke
import os


# Configuration
FILE_PREFIX = "CopyPasteData_"
SYSTEM = platform.system()

PATHS = {
    "Windows": {
        "SMCA": r"S:/public/CopyPasteData",
        "UG": r"U:/public/CopyPasteData",
    },
    "Linux": {
        "SMCA": r"/escape/shares/SMCA/public/CopyPasteData",
        "UG": r"/escape/shares/UG/public/CopyPasteData",
    }
}


def get_platform_path(course="UG"):
    """
    Get the platform-specific path for a given course.
    
    Args:
        course (str): Course name ("UG" or "SMCA")
    
    Returns:
        str or None: Path if found, None otherwise
    """
    return PATHS.get(SYSTEM, {}).get(course)


def copy_data(number):
    """
    Copy selected nodes to a numbered file on the network.
    
    Args:
        number (int or str): Slot number to save to
    """
    filename = f"{FILE_PREFIX}{number}.nk"
    _try_nuke_operation(nuke.nodeCopy, filename)


def paste_data(number):
    """
    Paste nodes from a numbered file on the network.
    
    Args:
        number (int or str): Slot number to load from
    """
    filename = f"{FILE_PREFIX}{number}.nk"
    _try_nuke_operation(nuke.nodePaste, filename)


def _try_nuke_operation(operation, filename):
    """
    Try to perform a Nuke operation (copy/paste) across multiple network paths.
    
    Args:
        operation (callable): Nuke function to call (nodeCopy or nodePaste)
        filename (str): Name of the file to operate on
    """
    # Try each course location
    for course in ("SMCA", "UG"):
        base_path = get_platform_path(course)
        
        if not base_path:
            continue
        
        filepath = os.path.join(base_path, filename)
        
        try:
            operation(filepath)
            return
        except RuntimeError:
            continue
    
    # If we get here, all paths failed
    nuke.message("File Path Not Found!")
