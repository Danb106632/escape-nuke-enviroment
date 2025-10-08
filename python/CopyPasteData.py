import nuke
import os

pathWindowsSMCA = r"S:/public/CopyPasteData"
pathWindowsUG = r"U:/public/CopyPasteData"
fileRaw = "CopyPasteData_"

def CopyData(number):
    file = fileRaw + str(number) + ".nk"
    try:
        nuke.nodeCopy(os.path.join(pathWindowsSMCA, file))
    except RuntimeError:
        try:
            nuke.nodeCopy(os.path.join(pathWindowsUG, file))
        except RuntimeError:
            nuke.message("File Path Not Found!")


def PasteData(number):
    file = fileRaw + str(number) + ".nk"
    try:
        nuke.nodePaste(os.path.join(pathWindowsSMCA, file))
    except RuntimeError:
        try:
            nuke.nodePaste(os.path.join(pathWindowsUG, file))
        except RuntimeError:
            nuke.message("File Path Not Found!")