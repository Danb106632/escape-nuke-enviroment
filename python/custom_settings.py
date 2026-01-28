"""
Custom Default Settings for Nuke Nodes
Configures default knob values and labels for various node types.
"""

import nuke


def default_settings():
    """
    Apply custom default settings to various Nuke node types.
    Sets default values, labels, and expressions for improved workflow.
    """
    _setup_merge_defaults()
    _setup_remove_defaults()
    _setup_tracker_defaults()
    _setup_blur_defaults()
    _setup_roto_defaults()
    _setup_grade_defaults()
    _setup_colorcorrect_defaults()
    _setup_scanlinerender_defaults()
    _setup_zdefocus_defaults()
    _setup_defocus_defaults()
    _setup_edgeblur_defaults()
    _setup_dilate_defaults()
    _setup_erode_defaults()
    _setup_filtererode_defaults()
    _setup_saturation_defaults()
    _setup_multiply_defaults()
    _setup_add_defaults()
    _setup_write_defaults()


def custom_keybinds():
    """
    Set up custom keyboard shortcuts for commonly used nodes.
    """
    toolbar = nuke.menu("Nodes")
    
    # Premult/Unpremult shortcuts
    toolbar.addCommand(
        "Merge/Premult",
        "nuke.createNode('Premult')",
        ";",
        icon="Premult.png",
        shortcutContext=2
    )
    toolbar.addCommand(
        "Merge/Unpremult",
        "nuke.createNode('Unpremult')",
        "u",
        icon="Unpremult.png",
        shortcutContext=2
    )
    
    # Tracker shortcut
    toolbar.addCommand(
        'Transform/Tracker',
        'nuke.createNode("Tracker4")',
        "Ctrl+Alt+t",
        icon='Tracker.png',
        shortcutContext=2
    )


def _setup_merge_defaults():
    """Configure Merge2 node defaults."""
    nuke.knobDefault('Merge2.bbox', 'B')
    nuke.knobDefault('Merge2.label', 'Mix: [value mix]')


def _setup_remove_defaults():
    """Configure Remove node defaults."""
    nuke.knobDefault('Remove.operation', 'keep')
    nuke.knobDefault('Remove.channels', 'rgba')


def _setup_tracker_defaults():
    """Configure Tracker4 node defaults."""
    nuke.knobDefault(
        'Tracker4.label',
        "Motion: [value transform]\nRef Frame: [value reference_frame]"
    )
    nuke.addOnUserCreate(
        lambda: nuke.thisNode()['reference_frame'].setValue(nuke.frame()),
        nodeClass='Tracker4'
    )


def _setup_blur_defaults():
    """Configure Blur node defaults."""
    nuke.knobDefault('Blur.size', '2')
    nuke.knobDefault(
        'Blur.label',
        'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_roto_defaults():
    """Configure Roto node defaults."""
    nuke.knobDefault('Roto.cliptype', '0')


def _setup_grade_defaults():
    """Configure Grade node defaults."""
    nuke.knobDefault(
        'Grade.label',
        '[if {[value mix] != 1} { return "Mix: [value mix]"} else {return ""}]'
    )


def _setup_colorcorrect_defaults():
    """Configure ColorCorrect node defaults."""
    nuke.knobDefault(
        'ColorCorrect.label',
        '[if {[value mix] != 1} { return "Mix: [value mix]"} else {return ""}]'
    )


def _setup_scanlinerender_defaults():
    """Configure ScanlineRender node defaults."""
    nuke.addOnUserCreate(_scanlinerender_oncreate, nodeClass='ScanlineRender')
    nuke.knobDefault(
        'ScanlineRender.label',
        'GUI Samples: [value samples]\n'
        'Render Samples: [value render_samples]\n'
        '[if { [value antialiasing] != "none" } { return "Antialiasing: [value antialiasing]" } else { return ""}]\n'
        '[if { [value overscan] != "0" } { return "Overscan: [value overscan]" } else { return " "}]'
    )


def _setup_zdefocus_defaults():
    """Configure ZDefocus2 node defaults."""
    nuke.knobDefault('ZDefocus2.size', '2')
    nuke.knobDefault(
        'ZDefocus2.label',
        'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_defocus_defaults():
    """Configure Defocus node defaults."""
    nuke.knobDefault('Defocus.size', '2')
    nuke.knobDefault(
        'Defocus.label',
        'Size: [value defocus][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_edgeblur_defaults():
    """Configure EdgeBlur node defaults."""
    nuke.knobDefault('EdgeBlur.size', '2')
    nuke.knobDefault(
        'EdgeBlur.label',
        'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_dilate_defaults():
    """Configure Dilate node defaults."""
    nuke.knobDefault('Dilate.size', '2')
    nuke.knobDefault(
        'Dilate.label',
        'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_erode_defaults():
    """Configure Erode node defaults."""
    nuke.knobDefault('Erode.size', '2')
    nuke.knobDefault(
        'Erode.label',
        'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_filtererode_defaults():
    """Configure FilterErode node defaults."""
    nuke.knobDefault('FilterErode.size', '2')
    nuke.knobDefault(
        'FilterErode.label',
        'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]'
    )


def _setup_saturation_defaults():
    """Configure Saturation node defaults."""
    nuke.knobDefault(
        'Saturation.label',
        '[value saturation]\nLuminance Math: [value mode]'
    )


def _setup_multiply_defaults():
    """Configure Multiply node defaults."""
    nuke.knobDefault('Multiply.label', 'Value: [value value]')


def _setup_add_defaults():
    """Configure Add node defaults."""
    nuke.knobDefault('Add.label', 'Value: [value value]')


def _setup_write_defaults():
    """Configure Write node defaults."""
    nuke.knobDefault('Write.create_directories', '1')


def _scanlinerender_oncreate():
    """
    Callback function for ScanlineRender node creation.
    Adds custom GUI and render sample knobs with dynamic expression.
    """
    node = nuke.thisNode()
    
    # Add custom knobs
    node.addKnob(nuke.Int_Knob('gui_samples', 'GUI Samples'))
    node.addKnob(nuke.Int_Knob('render_samples', 'Render Samples'))
    
    # Set default values
    node['gui_samples'].setValue(1)
    node['render_samples'].setValue(10)
    
    # Set expression to switch between GUI and render samples
    node['samples'].setExpression('$gui?gui_samples:render_samples')
