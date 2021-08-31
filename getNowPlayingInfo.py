from subprocess import Popen, PIPE


def grabNowPlayingOSX():
    app = "Terminal"

    getNowPlayingMac = '''
    tell application "Spotify"
        set npartist to artist of the current track
        set nptrack to name of the current track
    end tell

    set np to npartist & "*" & nptrack
    ''' % {'app': app}

    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    npinfo, error = proc.communicate(getNowPlayingMac)

    artist = npinfo.partition('*')[0].strip()
    song = npinfo.partition('*')[2].strip()

    print(artist)
    print(song)

    return artist,song


grabNowPlayingOSX()
