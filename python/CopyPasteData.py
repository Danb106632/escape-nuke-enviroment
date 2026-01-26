import platform
import nuke
import os

FILE_RAW = "CopyPasteData_"
SYSTEM = platform.system()

PATHS = {
    "Windows": {
        "SMCA": r"S:/public/CopyPasteData",
        "UG":   r"U:/public/CopyPasteData",
    },
    "Linux": {
        "SMCA": r"/escape/shares/SMCA/public/CopyPasteData",
        "UG":   r"/escape/shares/UG/public/CopyPasteData",
    }
}


def platformPath(course="UG"):
    return PATHS.get(SYSTEM, {}).get(course)


def _try_nuke_op(op, file):
    for course in ("SMCA", "UG"):
        base = platformPath(course)
        if not base:
            continue
        try:
            op(os.path.join(base, file))
            return
        except RuntimeError:
            pass
    nuke.message("File Path Not Found!")


def CopyData(number):
    file = f"{FILE_RAW}{number}.nk"
    _try_nuke_op(nuke.nodeCopy, file)


def PasteData(number):
    file = f"{FILE_RAW}{number}.nk"
    _try_nuke_op(nuke.nodePaste, file)