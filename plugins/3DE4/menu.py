import nuke
import os
import glob
 
plugins_menu = nuke.menu('Nodes').addMenu("Escape Studios/3DE4", icon="3de_white.png")
 
dll_pattern = os.path.join(
    os.path.dirname(__file__), 
    "{}.{}".format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR),
    "*.dll"
)
for dll_file in glob.glob(dll_pattern):
    plugin_name = os.path.splitext(os.path.basename(dll_file))[0]
    plugins_menu.addCommand(plugin_name, "nuke.createNode('{}')".format(plugin_name))