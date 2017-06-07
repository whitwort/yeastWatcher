import os.path

# (timePoint, channel, Z-stack)
def scanFiles(path, wellNames):

    tracks = {}

    for dirpath, dirnames, filenames in os.walk(path):

        if "Track" in dirpath and not "Image" in dirpath:
            if wellNames:
                well = os.path.basename(dirpath)[:2]
            else:
                well = ""

            trackName = os.path.basename(dirpath)[-4:]

            track = { 'track'     : trackName,
                      'well'      : well,
                      'images'    : dict(),
                      'timePoints': [],
                      'zs'        : [],
                      'cs'        : []
                    }
            tracks[trackName] = track

        if "Image" in dirpath:
            timePoint = int(os.path.basename(dirpath)[-12:-10])
            track['timePoints'].append(timePoint)

        for name in filenames:
            if name.endswith(".tif") and not name.endswith("-merged.tif"):
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
