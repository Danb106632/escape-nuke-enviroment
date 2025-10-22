import nuke

def ReadFromWrite():

    selected = nuke.selectedNode()
    if selected.Class() == "Write":
        if selected["use_limit"].value() == True:
            firstFrame = selected["first"].value()
            lastFrame = selected["last"].value()
        else:
            firstFrame = nuke.Root()["first_frame"].value()
            lastFrame = nuke.Root()["last_frame"].value()

        colorspace = selected["colorspace"].value()
        colorspace = colorspace.replace("default (", "")
        colorspace = colorspace.replace(")", "")

        read = nuke.nodes.Read(
            file=selected["file"].value(),
            colorspace=colorspace,
            first=firstFrame,
            last=lastFrame,
            origfirst=nuke.Root()["first_frame"].value(),
            origlast=nuke.Root()["last_frame"].value())
        read.setXpos(selected.xpos())
        read.setYpos(selected.ypos()-100)
        read['reload'].execute()
    else:
        nuke.message("No Write node selected")
    return
