# @File(label="Project Directory", description="Select the root directory containing Fluoview output files from a MATL run.", style="directory") sourcePath
# @boolean(label="Wells in file names", description="This should be checked if you enabled this feature in the file output configuration in Fluoview", value=TRUE) wellNames
# @boolean(label="Customize LUTS", description="This feature is in interactive mode; it allows you to choose which look-up-tables to use to pseudo-color each of your channels.", value=TRUE) showLUTS
# @boolean(label="Scramble track names", description="This feature allows you to scramble the names of the merged track files for blind scoring; the summary table lists aliases.", value=FALSE) scrambleNames
# @boolean(label="Compress & copy", description="Compresses source files and merge files into seperate zip archives and then copies them to the location specified below.", value=TRUE) compressCopy
# @File(label="Copy compressed files to", description="Ignored if Compress and Copy isn't checked.", style="directory") destPath

from __future__ import with_statement

import os
import os.path
from sys     import path
from pprint  import pprint
from random  import shuffle
from zipfile import ZipFile

from ij         import IJ, VirtualStack, ImagePlus
from ij.plugin  import HyperStackConverter
from ij.io      import FileSaver
from ij.measure import ResultsTable
from ij.gui     import GenericDialog
from ij.plugin  import LutLoader

from java.lang.System import getProperty
path.append(getProperty('fiji.dir') + '/plugins/yeastWatcher')

from libyeastwatcher import scanFiles

def hyperstack(name, track, path, luts):

    firstImgPath = track['images'][(1, 1, 1)]
    firstImg     = IJ.openImage(firstImgPath)
    vstack       = VirtualStack(firstImg.width, firstImg.height, None, path) # this is probably broken

    cs = track['cMax']
    zs = track['zMax']
    ts = track['timePoints']

    blankPath = ""
    if len(track['images']) != cs * zs * ts:
        img = IJ.createImage("blank", "16-bit black", firstImg.width, firstImg.height, 1)
        blankPath = os.path.join(path, "blank.tif")
        IJ.saveAsTiff(img, blankPath)

    for frameN in range(1, ts + 1):
        for zN in range(1, zs + 1):
            for cN in range(1, cs + 1):

                imagePath = track['images'].get((frameN, cN, zN))
                if imagePath is None:
                    imagePath = blankPath
                vstack.addSlice(imagePath[len(path):])

    img   = ImagePlus(name, vstack)
    hsc   = HyperStackConverter()
    stack = hsc.toHyperStack(img, cs, zs, ts, "default", "color")

    for i in range(cs):
        # this feels like the wrong way to be doing this
        stack.show()
        stack.setC(i + 1)
        IJ.run(luts[i])
        stack.hide()

    IJ.saveAsTiff(stack, os.path.join(path, name + "-merged"  + ".tif"))

    if blankPath != "":
        os.remove(blankPath)

def lutsGUI(channels, luts):
    dialog = GenericDialog("Customize LUTS")
    for i in range(channels):
        dialog.addChoice("Channel " + str(i) + ":", luts, luts[1])
    dialog.showDialog()

    choices = dialog.getChoices()

    return [choice.getSelectedItem() for choice in choices]

def zipdir(source, dest, nameFilter):
    zip     = ZipFile(dest, "w")
    pathlen = len(source) + 1

    for base, dirs, files in os.walk(source):
        for file in files:
            if nameFilter(file):
                filePath = os.path.join(base, file)
                zip.write(filePath, filePath[pathlen:])

    zip.close()

def compressMerge(source, dest):
    def nameFilter(file): return "-merged.tif" in file
    zipdir(source, dest, nameFilter)

def compressSource(source, dest):
    def nameFilter(file): return not "-merged.tif" in file
    zipdir(source, dest, nameFilter)

def run(path, dest):
    IJ.showStatus("Scanning files")
    tracks = scanFiles(path, wellNames)

    luts = IJ.getLuts()
    if showLUTS:
        channels = [tracks[name]['cMax'] for name in tracks]
        luts     = lutsGUI(max(channels), luts)

    if scrambleNames:
        scrambledNames = [i + 1 for i in range(len(tracks))]
        shuffle(scrambledNames)

    table = ResultsTable()
    for i, name in enumerate(tracks):
        IJ.showStatus("Processing track: " + name)
        IJ.showProgress(i, len(tracks))

        track = tracks[name]

        table.incrementCounter()
        table.addValue("track", name)
        table.addValue("well", track['well'])
        table.addValue("channels", track['cMax'])
        table.addValue("z-stacks", track['zMax'])
        table.addValue("timepoints", track['timePoints'])
        table.addValue("images", len(track['images']))
        if scrambleNames:
            name = str(scrambledNames[i])
            table.addValue("scrambled-name", name)
        table.show("Track summary")

        hyperstack(name, track, path, luts)

    table.save(os.path.join(path, "track-summary.csv"))

    if compressCopy:
        IJ.showStatus("Compressing and copying merge files")
        zippath = os.path.join(dest, "merged-tracks.zip")
        compressMerge(path, zippath)

        zip = ZipFile(zippath, "a")
        zip.write(os.path.join(path, "track-summary.csv"), "track-summary.csv")
        zip.close()

        IJ.showStatus("Compressing and copying source files")
        compressSource(path, os.path.join(dest, "source-files.zip"))

run(str(sourcePath), str(destPath))
