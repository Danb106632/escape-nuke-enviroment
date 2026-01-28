"""
Postage Stamp Replacement Tool for Nuke
Replaces duplicate Read nodes with PostageStamp or NoOp nodes connected to a master Read.
"""

import nuke
import nukescripts


def postage_replace():
    """
    Replace duplicate Read nodes with PostageStamp or NoOp nodes.
    
    Finds all Read nodes with the same file path as the selected Read node
    and replaces them with PostageStamp or NoOp nodes connected to the original.
    """
    # Validate selection
    selected_nodes = nuke.selectedNodes()
    
    if len(selected_nodes) > 1:
        nuke.message("Select one Read node!")
        return
    
    if len(selected_nodes) == 0:
        nuke.message("No Read nodes selected!")
        return
    
    read_node = selected_nodes[0]
    
    if read_node.Class() != 'Read':
        nuke.message("Selected node is not a Read node!")
        return
    
    # Get postage stamp name from user
    postage_name = nuke.getInput("Name for PostageStamps", "Scan")
    
    if postage_name is None or postage_name == '':
        return
    
    # Ask user which node type to use
    node_class = "NoOp" if nuke.ask("Use NoOp?") else "PostageStamp"
    
    # Get the file path from the selected Read node
    source_filepath = read_node['file'].getValue()
    
    # Find and replace duplicate Read nodes
    replaced_count = _replace_duplicate_reads(read_node, source_filepath, node_class, postage_name)
    
    # Reset selection
    nukescripts.clear_selection_recursive()
    read_node['selected'].setValue(True)
    
    # Show result message
    if replaced_count == 0:
        nuke.message("No changes occurred!")
    else:
        nuke.message(f"Replaced {replaced_count} Read node(s)!")


def _replace_duplicate_reads(source_read, filepath, node_class, postage_name):
    """
    Find and replace Read nodes with matching file paths.
    
    Args:
        source_read: The original Read node to connect to
        filepath (str): File path to match
        node_class (str): Node type to create ("PostageStamp" or "NoOp")
        postage_name (str): Name for the new nodes
    
    Returns:
        int: Number of nodes replaced
    """
    # Select all Read nodes with similar properties
    nuke.selectSimilar(0)
    source_read['selected'].setValue(False)
    
    replaced_count = 0
    
    for read_node in nuke.selectedNodes('Read'):
        # Check if file paths match
        if read_node['file'].getValue() != filepath:
            continue
        
        # Clear selection and select only this Read node
        nukescripts.clear_selection_recursive()
        read_node['selected'].setValue(True)
        
        # Get position of the Read node
        xpos = int(read_node['xpos'].value())
        ypos = int(read_node['ypos'].value())
        
        # Create replacement node
        replacement_node = nuke.createNode(node_class, inpanel=False)
        replacement_node['xpos'].setValue(xpos)
        replacement_node['ypos'].setValue(ypos)
        replacement_node['hide_input'].setValue(True)
        
        # Connect to original Read node
        replacement_node.setInput(0, source_read)
        
        # Set name
        replacement_node.setName(postage_name)
        
        # Delete the duplicate Read node
        nuke.delete(read_node)
        
        replaced_count += 1
    
    return replaced_count
