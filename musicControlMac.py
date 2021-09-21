def TogglePlayPauseMac():
    from subprocess import Popen, PIPE
    app = "Terminal"

    toggleplaypause = '''
    tell application "Spotify" to playpause
    ''' % {'app': app}

    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    npinfo, error = proc.communicate(toggleplaypause)

def NextTrackMac():
    from subprocess import Popen, PIPE
    app = "Terminal"

    nexttrack = '''
    tell application "Spotify" to next track
    ''' % {'app': app}

    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    npinfo, error = proc.communicate(nexttrack)

def PrevTrackMac():
    from subprocess import Popen, PIPE
    app = "Terminal"

    prevtrack = '''
    tell application "Spotify" to previous track
    ''' % {'app': app}

    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    npinfo, error = proc.communicate(prevtrack)
