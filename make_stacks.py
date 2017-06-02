# @File(label="Project Directory", description="Select the root directory containing Fluoview output files from a MATL run.", style="directory") sourcePath
# @boolean(label="Wells in file names", description="Do track folder names include the names of the wells they are from.", value=TRUE) wellNames

from __future__ import with_statement
import os
import os.path
from pprint import pprint

from ij import IJ

# (timePoint, channel, Z-stack)

def scanFiles(path):

    tracks = {}

    for dirpath, dirnames, filenames in os.walk(path):

        if "Track" in dirpath and not "Image" in dirpath:
            if wellNames:
                well = os.path.basename(dirpath)[:3]
            else:
                well = ""

            trackName = os.path.basename(dirpath)[-4:]

            track = { 'track':      trackName,
                      'well':       well,
                      'images':     dict(),
                      'timePoints': [],
                      'zs':         [],
                      'cs':         []
                    }
            tracks[trackName] = track

        if "Image" in dirpath:
            timePoint = int(os.path.basename(dirpath)[-12:-10])
            track['timePoints'].append(timePoint)

        for name in filenames:
            if name.endswith(".tif"):
                z = int(name[-7:-4])
                c = int(name[-11:-8])

                track['zs'].append(z)
                track['cs'].append(c)
                track['images'][(timePoint, c, z)] = os.path.join(dirpath, name)

    for key, track in tracks.iteritems():
        track['timePoints'] = len(track['timePoints'])
        track['zMax']       = max(track['zs'])
        track['cMax']       = max(track['cs'])

        track.pop('zs')
        track.pop('cs')

    return tracks

def run(path):
    IJ.showStatus("Scanning files")
    tracks = scanFiles(path)

    with open(os.path.join(path, "images.txt"), 'wt') as out:
        pprint(tracks, stream=out)

run(str(sourcePath))
