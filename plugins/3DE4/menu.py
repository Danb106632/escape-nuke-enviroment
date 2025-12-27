import nuke
import os
import glob
import platform

plugins_menu = nuke.menu('Nodes').addMenu('Escape Studios/3DE4', icon = "3de_white.png")

system_os = platform.system().lower()

plugin_folder = ""

plugin_pattern = ""

if system_os == "windows":
    plugin_folder = os.path.join(
        os.path.dirname(__file__),
        system_os,
        "Nuke{}.{}".format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)
    )
    plugin_pattern = os.path.join(
        plugin_folder,
        "*.dll"
    )
elif system_os == "linux":
    plugin_folder = os.path.join(
        os.path.dirname(__file__),
        system_os,
        "Nuke{}.{}".format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)
    )
    plugin_pattern = os.path.join(
        plugin_folder,
        "*.so"
    )
elif system_os == "darwin":
    plugin_folder = os.path.join(
        os.path.dirname(__file__),
        "osx",
        "Nuke{}.{}".format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)
    )
    plugin_pattern = os.path.join(
        plugin_folder,
        "*.dylib"
    )

nuke.pluginAddPath(plugin_folder)

for plugin_file in glob.glob(plugin_pattern):
    plugin_name = os.path.splitext(os.path.basename(plugin_file))[0]
    plugins_menu.addCommand(plugin_name, "nuke.createNode('{}')".format(plugin_name))
