import nuke

import os
import json


def toRelative():
    with open(os.path.dirname(__file__) + '/../config/nodes.json', 'r') as f:
        data = json.load(f)

        for node in data['nodes']:
            for n in nuke.allNodes(node['class']):
                filePath = n[node['file']].getValue()

                #check if we need to change it, make sure it isn't already relative 
                if os.path.isabs(filePath) and filePath != '':
                    try:
                        n[node['file']].setValue(_getRelativePath(filePath))
                    except ValueError:
                        continue
                    

def toAbsolute():
    with open(os.path.dirname(__file__) + '/../config/nodes.json', 'r') as f:
        data = json.load(f)

        for node in data['nodes']:
            for n in nuke.allNodes(node['class']):
                filePath = n[node['file']].getValue()

                #check if we need to change it, make sure it isn't already absolute 
                if not os.path.isabs(filePath) and filePath != '':
                    try:
                        n[node['file']].setValue(_getAbsolutePath(filePath))
                    except ValueError:
                        continue


def _getAbsolutePath(path):
    absPath = os.path.abspath(os.path.join(nuke.script_directory(), path))
    return absPath.replace('\\', '/')


def _getRelativePath(path):
    absPath = os.path.relpath(path, nuke.script_directory())
    return absPath.replace('\\', '/')
    


