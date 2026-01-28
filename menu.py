"""
Escape Nuke Pipeline
Developed by Daniel Beeching
updated: 16/09/2025
"""
################################

# Default imports

import nuke
import nukescripts

# Custom Imports

import python.custom_settings

################################

python.custom_settings.default_settings()
python.custom_settings.custom_keybinds()

################################

# Add Escape to the Nodes Toolbar

Escape = nuke.toolbar("Nodes").addMenu('Escape Studios', icon='escape.png')

################################

for i in range(1,6):
    Escape.addCommand("Share Nodes/Copy/" + str(i), "import copy_paste_data\ncopy_paste_data.copy_data({})".format(str(i)))
    Escape.addCommand("Share Nodes/Paste/" + str(i), "import copy_paste_data\ncopy_paste_data.paste_data({})".format(str(i)))

################################

Escape.addCommand("Postage Replace", "import postage_replace\npostage_replace.postage_replace()", "Ctrl+Alt+R")

################################

Escape.addCommand("Python Commands/Relative Paths/To Relative", "import absolute_to_relative\nabsolute_to_relative.to_relative()")
Escape.addCommand("Python Commands/Relative Paths/To Absolute", "import absolute_to_relative\nabsolute_to_relative.to_absolute()")

Escape.addCommand("Python Commands/Roto to Trackers", "import RotoToTrackers\nRotoToTrackers.RotoShape_to_Trackers()")
Escape.addCommand("Python Commands/Silhouette Exporter", "import SilhouetteExporter\nSilhouetteExporter.silhouetteFxsExporter()")

################################