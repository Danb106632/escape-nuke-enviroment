import nuke
import nukescripts

def PostageReplace():
    #Verify if read node is selected
    if len(nuke.selectedNodes()) > 1:
        nuke.message("Select one Read node!")
        return
    
    #Verify Node is selected
    ReadNode = nuke.selectedNode()
    if ReadNode.Class() != 'Read':
        nuke.message("No Read nodes selected!")
        return 

    postageName = nuke.getInput("Name for PostageStamps", "Scan")
    #If operation is cancelled or input is empty
    if postageName is None or postageName == '':
        return
    
    nodename = "NoOp" if nuke.ask("Use NoOp?") else "PostageStamp"

    #Select By Class
    nuke.selectSimilar(0)
    ReadNode['selected'].setValue(False)

    executed = False

    for n in nuke.selectedNodes('Read'):
        #If filepath are the same, rest of the values should be
        if n['file'].getValue() == ReadNode['file'].getValue():
            executed = True

            #set selection to Read node
            nukescripts.clear_selection_recursive()
            n['selected'].setValue(True)
            
            #Copy pos and set knobs
            xpos = int(n['xpos'].value())
            ypos = int(n['ypos'].value())
            PS = nuke.createNode(nodename, inpanel=False)
            PS['xpos'].setValue(xpos)
            PS['ypos'].setValue(ypos)
            PS['hide_input'].setValue(True)
   
            #connect to Orignal read
            PS.setInput(0, ReadNode)

            # Creates name
            PS.setName(postageName)

            #Delete Read
            nuke.delete(n)

    #Reset Selection after changes
    nukescripts.clear_selection_recursive()
    ReadNode['selected'].setValue(True)

    if not executed:
        nuke.message("No Changes occured!")
    else:
        nuke.message("Changed!")
