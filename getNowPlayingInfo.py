def grabNowPlayingOSX():
    from subprocess import Popen, PIPE
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


def grabNowPlayingWindows():
    import win32gui
    windows = []

    windows.append(win32gui.GetWindowText(win32gui.FindWindow("SpotifyMainWindow", None)))

    def find_spotify_uwp(hwnd, windows):
        text = win32gui.GetWindowText(hwnd)
        if win32gui.GetClassName(hwnd) == "Chrome_WidgetWin_0" and len(text) > 0:
            windows.append(text)

    win32gui.EnumWindows(find_spotify_uwp, windows)

    while windows.count != 0:
        try:
            text = windows.pop()
        except:
            return "Error", "Nothing playing"
        try:
            artist, song = text.split(" - ",1)
            return artist, song
        except:
            pass
