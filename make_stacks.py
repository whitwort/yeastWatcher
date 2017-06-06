# @File(label="Project Directory", description="Select the root directory containing Fluoview output files from a MATL run.", style="directory") sourcePath
# @boolean(label="Wells in file names", description="Do track folder names include the names of the wells they are from.", value=TRUE) wellNames
# @boolean(label="Customize LUTS", description="Usable in interactive mode to customize the color look up tables in hyperstacks.", value=TRUE) showLUTS
# @boolean(label="Randomize track names", description="Scramble track names and include translation in images result table.", value=FALSE) randomizeNames

from __future__ import with_statement

import os
import os.path
from sys import path
from pprint import pprint

from ij import IJ

from java.lang.System import getProperty
path.append(getProperty('fiji.dir') + '/plugins/yeastWatcher')
from libyeastwatcher import scanFiles

def hyperstack(name, track):
    return FALSE

def run(path):
    IJ.showStatus("Scanning files")
    tracks = scanFiles(path)

    for name, track in tracks.iteritems():
        IJ.showStatus("Processing track: " + name)
        alias = hyperstack(name, track)  # TODO add name randomization here

    with open(os.path.join(path, "images.txt"), 'wt') as out:
        pprint(tracks, stream=out)

run(str(sourcePath))
