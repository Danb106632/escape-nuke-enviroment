import nuke

def default_settings():
    # sets the default bounding box to B
    nuke.knobDefault('Merge2.bbox', 'B')
    nuke.knobDefault('Merge2.label', 'Mix: [value mix]')

    # sets the default Remove to Keep and RGBA
    nuke.knobDefault('Remove.operation', 'keep')
    nuke.knobDefault('Remove.channels', 'rgba')

    #Set tracker4 label
    nuke.knobDefault('Tracker4.label', "Motion: [value transform]\nRef Frame: [value reference_frame]")
    nuke.addOnUserCreate(lambda:nuke.thisNode()['reference_frame'].setValue(nuke.frame()), nodeClass='Tracker4')

    #Set Blur to size to 2
    nuke.knobDefault('Blur.size', '2')
    nuke.knobDefault('Blur.label', 'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')

    #Set Roto NoClip
    nuke.knobDefault('Roto.cliptype', '0')
    nuke.knobDefault('Roto.feather', '2')
    nuke.knobDefault('Roto.label', 'Feather: [value feather]')

    #Set Grade label
    nuke.knobDefault('Grade.label', '[if {[value mix] != 1} { return "Mix: [value mix]"} else {return ""}]')

    #Set ColorCorrect label
    nuke.knobDefault('ColorCorrect.label', '[if {[value mix] != 1} { return "Mix: [value mix]"} else {return ""}]')

    #Set ScanlineRender label
    nuke.addOnUserCreate(ScanlineRenderDefault, nodeClass='ScanlineRender')
    nuke.knobDefault('ScanlineRender.label', 'GUI Samples: [value samples]\nRender Samples: [value render_samples]\n[if { [value antialiasing] != "none" } { return "Antialiasing: [value antialiasing]" } else { return ""}]\n[if { [value overscan] != "0" } { return "Overscan: [value overscan]" } else { return " "}]')

    #Set ZDefocus2 label
    nuke.knobDefault('ZDefocus2.size', '2')
    nuke.knobDefault('ZDefocus2.label', 'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')

    #Set Defocus label
    nuke.knobDefault('Defocus.size', '2')
    nuke.knobDefault('Defocus.label', 'Size: [value defocus][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')

    #Set EdgeBlur label
    nuke.knobDefault('EdgeBlur.size', '2')
    nuke.knobDefault('EdgeBlur.label', 'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')

    #Set Dilate label
    nuke.knobDefault('Dilate.size', '2')
    nuke.knobDefault('Dilate.label', 'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')

    #Set Erode label
    nuke.knobDefault('Erode.size', '2')
    nuke.knobDefault('Erode.label', 'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')

    #Set FilterErode label
    nuke.knobDefault('FilterErode.size', '2')
    nuke.knobDefault('FilterErode.label', 'Size: [value size][if {[value mix] != 1} { return " | Mix: [value mix]"} else {return ""}]')
    
    #Set Saturation label
    nuke.knobDefault('Saturation.label', '[value saturation]\nLuminance Math: [value mode]')
    
    #Set Multiply label
    nuke.knobDefault('Multiply.label', 'Value: [value value]')
    
    #Set Add label
    nuke.knobDefault('Add.label', 'Value: [value value]')
    
    #Set Write create directories
    nuke.knobDefault('Write.create_directories', '1')
    
    
def ScanlineRenderDefault():
    node = nuke.thisNode()
    node.addKnob(nuke.Int_Knob('gui_samples', 'GUI Samples'))
    node.addKnob(nuke.Int_Knob('render_samples', 'Render Samples'))
    node['gui_samples'].setValue(1)
    node['render_samples'].setValue(10)
    node['samples'].setExpression('$gui?gui_samples:render_samples')


def custom_keybinds():
    toolbar = nuke.menu("Nodes")

    toolbar.addCommand("Merge/Premult","nuke.createNode('Premult')",";", icon="Premult.png", shortcutContext = 2)
    toolbar.addCommand("Merge/Unpremult","nuke.createNode('Unpremult')","u", icon="Unpremult.png", shortcutContext = 2)
    toolbar.addCommand('Transform/Tracker', 'nuke.createNode("Tracker4")', "Ctrl+Alt+t", icon='Tracker.png', shortcutContext = 2)
