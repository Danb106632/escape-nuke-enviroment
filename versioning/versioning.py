"""
Versioning utilities for Nuke scripts and write nodes.
Handles version number extraction, updates, and synchronization between scripts and write nodes.
"""

import nuke
import nukescripts


def get_script_version():
    """
    Get the version number from the current script filename.
    
    Returns:
        int or None: Version number if found, None otherwise
    """
    filepath = nuke.root()["name"].value()
    
    if not filepath:
        return None
    
    try:
        version_data = nukescripts.version_get(filepath, "v")
        return version_data[1]
    except (ValueError, IndexError):
        return None


def get_node_version(node):
    """
    Get the version number from a node's file path.
    
    Args:
        node: Nuke node (typically a Write or DeepWrite node)
    
    Returns:
        int or None: Version number if found, None otherwise
    """
    try:
        filepath = nuke.filename(node)
    except (AttributeError, RuntimeError):
        return None
    
    if not filepath:
        return None
    
    try:
        version_data = nukescripts.version_get(filepath, "v")
        return version_data[1]
    except (ValueError, IndexError):
        return None


def set_node_version(node, version=None):
    """
    Set the version number in a node's file path.
    
    Args:
        node: Nuke node (typically a Write or DeepWrite node)
        version (int, optional): Version number to set. If None, uses script version.
    
    Returns:
        bool: True if version was updated successfully, False otherwise
    """
    if version is None:
        version = get_script_version()
    
    if version is None:
        return False
    
    # Check if node has a 'file' knob
    if 'file' not in node.knobs():
        return False
    
    try:
        node_filepath = nuke.filename(node)
    except (AttributeError, RuntimeError):
        return False
    
    if not node_filepath:
        return False
    
    # Get the current version string format from version_get
    try:
        current_version_data = nukescripts.version_get(node_filepath, "v")
        current_version_string = current_version_data[0]  # Full version string (e.g., "v001", "v1", "v0042")
        current_version_number = current_version_data[1]  # Version number as int
    except (ValueError, IndexError):
        return False
    
    if current_version_number == version:
        return True
    
    try:
        # Determine the padding format from the current version string
        # Extract just the number part after 'v'
        padding_length = len(current_version_string) - 1  # Subtract 1 for the 'v'
        new_version_string = f"v{version:0{padding_length}d}"
        
        # Replace the version in the filepath
        new_filepath = node_filepath.replace(current_version_string, new_version_string)
        
        node["file"].setValue(new_filepath)
        return True
        
    except Exception:
        return False


def match_write_versions_to_script():
    """
    Synchronize all Write and DeepWrite node versions to match the script version.
    This is typically called on script save to keep write outputs in sync with script version.
    """
    script_ver = get_script_version()
    
    if script_ver is None:
        return
    
    write_nodes = nuke.allNodes("Write") + nuke.allNodes("DeepWrite")
    
    if not write_nodes:
        return
    
    for node in write_nodes:
        set_node_version(node, script_ver)


def version_script():
    """
    Version up the script and all write nodes using Nuke's built-in versioning.
    This is typically called after rendering.
    """
    try:
        nukescripts.script_and_write_nodes_version_up()
    except Exception:
        pass  # Silently continue if versioning fails


# Legacy function name for backwards compatibility
def script_version():
    """
    Legacy function name for get_script_version().
    Deprecated: Use get_script_version() instead.
    
    Returns:
        int or None: Version number if found, None otherwise
    """
    return get_script_version()
