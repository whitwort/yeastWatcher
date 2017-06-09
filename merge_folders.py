# @File(label="First project directory", description="Select the root directory containing the early time points.", style="directory") firstPath
# @File(label="Second project directory", description="Select the root directory containing late time points.", style="directory") secondPath
# @boolean(label="Wells in file names", description="This should be checked if you enabled this feature in the file output configuration in Fluoview", value=TRUE) wellNames
# @boolean(label="Backup original", description="If checked a back up will be made of the first project folder before the merge is performed.", value=FALSE) backup

import re, shutil
from os      import listdir
from os.path import join

from ij      import IJ

from libyeastwatcher import scanFiles

def run(destPath, mergePath):

    if backup:
        try: copytree(destPath, destpath + ".backup")
        except shutil.Error: pass

    IJ.showStatus("Scanning first directory")
    destTracks  = scanFiles(destPath, wellNames)

    IJ.showStatus("Scanning second directory")
    mergeTracks = scanFiles(mergePath, wellNames)

    postStr = ".oif.files"
    for name, track in mergeTracks.iteritems():
        if wellNames:
            #trackPath = "{0}_Track{1}".format(track['well'], name)
            trackPath =  "%s_Track%s" % (track['well'], name)
        else:
            #trackPath = "Track{0}".format(name)
            trackPath = "Track%s" % (track['well'],)

        match    = re.search(r"Image(\d{4})", track['images'][(1, 1, 1)])
        imageStr = match.group(1)
        for timePoint in range(track['timePoints']):
            IJ.showStatus("Merging track: " + name)
            IJ.showProgress(timePoint, track['timePoints'])

            timeStr = str(timePoint + 1).rjust(2, "0")

            if wellNames:
                # imagePath = "{0}_Image{1}_{2}{3}".format( track['well'],
                #                                           imageStr,
                #                                           timeStr,
                #                                           postStr
                #                                           )
                imagePath = "%s_Image%s_%s%s" % (track['well'], imageStr, timeStr, postStr)

            else:
                # imagePath = "Image{0}_{1}{2}".format( imageStr,
                #                                       timeStr,
                #                                       postStr
                #                                       )
                imagePath = "Image%s_%s%s" % (imageStr, timeStr, postStr)

            fromPath    = join(mergePath, trackPath, imagePath)
            destTime    = destTracks[name]['timePoints'] + timePoint + 1
            toImagePath = imagePath.replace("_" + timeStr, "_" + str(destTime).rjust(2, "0"))
            toPath      = join(destPath, trackPath, toImagePath)

            # for some reason this is throwing an unknown error, even though it works
            try:
                shutil.copytree(fromPath, toPath)
            except shutil.Error:
                pass

run(str(firstPath), str(secondPath))
