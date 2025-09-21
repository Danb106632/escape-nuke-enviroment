import nuke
import os

pathWindows = r"S:/public/CopyPasteData"
fileRaw = "CopyPasteData_"

def CopyData(number):
    file = fileRaw + str(number) + ".nk"
    nuke.nodeCopy(os.path.join(pathWindows, file))

def PasteData(number):
    file = fileRaw + str(number) + ".nk"
    nuke.nodePaste(os.path.join(pathWindows, file))

