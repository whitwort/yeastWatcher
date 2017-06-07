# yeastWatcher
A collection of ImageJ plugins that facilitate manipulation of images from live cell imaging experiments using Olympus Fluoview.

# Install

This plugin was developed and tested using Fiji (imageJ) version 1.51n.  It's recommended that you use the same.

To install, either `git clone` the repository, or download a zipped version of the repository (green button above) and extract it, into the `plugins` subfolder of your `Fiji.app` directory.  When you start/restart ImageJ you should see a 'yeastWatcher' entry in the `Plugins` menu with all of the commands listed below.

Delete this folder before updating the plugin in the future.

# Usage

For all of the tools, you can mouse over options in dialog boxes to get additional information.

## make stacks

This tool scans a Fluoview multi-area time-lapse output folder and merges the images for each track into a stacked TIFF.  The merged TIFFs are saved in the root folder along side a table summarizing the tracks that were found.

Missing source images will be replaced with an all black image, with one exception:  the image for the to the first time point, with the first z-stack, on the first channel must be present.

## merge

# Version

* 0.1 Initial release

# License

Copyright © 2017 Gregg Whitworth and licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).
