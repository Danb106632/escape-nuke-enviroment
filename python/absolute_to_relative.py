"""
Absolute/Relative Path Converter for Nuke
Converts file paths in nodes between absolute and relative formats.
"""

import nuke
import os
import json


def to_relative():
    """
    Convert absolute file paths to relative paths for all configured node types.
    Reads node configuration from ../config/nodes.json.
    """
    node_configs = _load_node_config()
    
    if not node_configs:
        return
    
    converted_count = 0
    
    for node_config in node_configs:
        node_class = node_config.get('class')
        file_knob = node_config.get('file')
        
        if not node_class or not file_knob:
            continue
        
        for node in nuke.allNodes(node_class):
            if _convert_node_to_relative(node, file_knob):
                converted_count += 1
    
    if converted_count > 0:
        print(f"Converted {converted_count} path(s) to relative")


def to_absolute():
    """
    Convert relative file paths to absolute paths for all configured node types.
    Reads node configuration from ../config/nodes.json.
    """
    node_configs = _load_node_config()
    
    if not node_configs:
        return
    
    converted_count = 0
    
    for node_config in node_configs:
        node_class = node_config.get('class')
        file_knob = node_config.get('file')
        
        if not node_class or not file_knob:
            continue
        
        for node in nuke.allNodes(node_class):
            if _convert_node_to_absolute(node, file_knob):
                converted_count += 1
    
    if converted_count > 0:
        print(f"Converted {converted_count} path(s) to absolute")


def _load_node_config():
    """
    Load node configuration from JSON file.
    
    Returns:
        list or None: List of node configurations, None if error
    """
    config_path = os.path.join(
        os.path.dirname(__file__),
        '../config/nodes.json'
    )
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get('nodes', [])
    
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config file: {e}")
        return None
    
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def _convert_node_to_relative(node, file_knob):
    """
    Convert a node's file path to relative format.
    
    Args:
        node: Nuke node to process
        file_knob (str): Name of the file knob
    
    Returns:
        bool: True if converted, False otherwise
    """
    if file_knob not in node.knobs():
        return False
    
    filepath = node[file_knob].getValue()
    
    # Check if we need to convert (must be absolute and not empty)
    if not filepath or not os.path.isabs(filepath):
        return False
    
    try:
        relative_path = _get_relative_path(filepath)
        node[file_knob].setValue(relative_path)
        return True
    
    except ValueError:
        return False
    
    except Exception:
        return False


def _convert_node_to_absolute(node, file_knob):
    """
    Convert a node's file path to absolute format.
    
    Args:
        node: Nuke node to process
        file_knob (str): Name of the file knob
    
    Returns:
        bool: True if converted, False otherwise
    """
    if file_knob not in node.knobs():
        return False
    
    filepath = node[file_knob].getValue()
    
    # Check if we need to convert (must be relative and not empty)
    if not filepath or os.path.isabs(filepath):
        return False
    
    try:
        absolute_path = _get_absolute_path(filepath)
        node[file_knob].setValue(absolute_path)
        return True
    
    except ValueError:
        return False
    
    except Exception:
        return False


def _get_absolute_path(path):
    """
    Convert a relative path to an absolute path based on script directory.
    
    Args:
        path (str): Relative file path
    
    Returns:
        str: Absolute file path with forward slashes
    """
    script_dir = nuke.script_directory()
    
    if not script_dir:
        raise ValueError("Script directory not available (script not saved)")
    
    abs_path = os.path.abspath(os.path.join(script_dir, path))
    return abs_path.replace('\\', '/')


def _get_relative_path(path):
    """
    Convert an absolute path to a relative path based on script directory.
    
    Args:
        path (str): Absolute file path
    
    Returns:
        str: Relative file path with forward slashes
    """
    script_dir = nuke.script_directory()
    
    if not script_dir:
        raise ValueError("Script directory not available (script not saved)")
    
    rel_path = os.path.relpath(path, script_dir)
    return rel_path.replace('\\', '/')
