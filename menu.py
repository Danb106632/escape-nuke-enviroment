"""
Escape Nuke Pipeline
Developed by Daniel Beeching
updated: 16/09/2025
"""
################################

# Default imports

import nuke
import nukescripts

################################

# Add Escape to the Nodes Toolbar

Escape = nuke.toolbar("Nodes").addMenu('Escape Studios', icon='escape.png')

################################

for i in range(1,6):
    Escape.addCommand("Share Nodes/Copy/" + str(i), "import CopyPasteData\nCopyPasteData.CopyData({})".format(str(i)))
    Escape.addCommand("Share Nodes/Paste/" + str(i), "import CopyPasteData\nCopyPasteData.PasteData({})".format(str(i)))

################################

Escape.addCommand("Python Commands/Relative Paths/Aboslute2Relative", "import Absolute2Relative\nAbsolute2Relative.toRelative()")
Escape.addCommand("Python Commands/Relative Paths/Relative2Absolute", "import Absolute2Relative\nAbsolute2Relative.toAbsolute()")

Escape.addCommand("Python Commands/Roto to Trackers", "import RotoToTrackers\nRotoToTrackers.RotoShape_to_Trackers()")
Escape.addCommand("Python Commands/Silhouette Exporter", "import SilhouetteExporter\nSilhouetteExporter.silhouetteFxsExporter()")

################################