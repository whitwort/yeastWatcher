# yeastWatcher
A collection of ImageJ plugins that facilitate manipulation of images from live cell imaging experiments using Olympus Fluoview.

# Install

This plugin was developed and tested using Fiji (imageJ) version 1.51n (Windows, x64).  It's recommended that you use the same.

To install, either `git clone` the repository, or download a zipped version of the repository (green button above) and extract it, into the `plugins` subfolder of your `Fiji.app` directory.  When you start/restart ImageJ you should see a 'yeastWatcher' entry in the `Plugins` menu with all of the commands listed below.

Delete this folder before updating the plugin in the future.

# Usage

For all of the tools, you can mouse over options in dialog boxes to get additional information.

## make stacks

This tool scans a Fluoview multi-area time-lapse output folder and merges the images for each track into a stacked TIFF.  The merged TIFFs are saved in the root folder along side a table summarizing the tracks that were found.

Missing source images will be replaced with an all black image, with one exception:  the image for the to the first time point, with the first z-stack, on the first channel must be present.

## merge folders

This tool will merge image files from one project folder into another.  Your early time points should be used for your first folder (target of the merge) and your later time points should set to the second folder (source of the merge).  The tracks must match up exactly between the two project folders.  This tool is useful for generating a project folder that can be used with the other tools after Fluoview has crashed in the middle of a run.

# Limitations

This plugin makes hard assumptions about file and folder naming conventions, adhering to the Fluoview defaults. In particular we assume Track folders use a 4-digit number, Image folders a 4-digit number followed by an underscore and 2-digit number (the time point), and image files use a 3-digit channel and 3-digit z-stack number.  The only flexible option is whether or not well names are included.

# Version

* 0.2 added `merge folders`
* 0.1 Initial release; includes `make stacks`

# License

Copyright © 2017 Gregg Whitworth and licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).
