# LyriCatch

Cross Platform application to view and download lyrics of the song that's currently being played. It supports ANY Music Player connted to Last.fm and Spotify (natively) for now.

## Requiremnts

GUI is made using python-tkinter, if building using macOS on a python3 installation via `brew`, `python-tk@3.9` also needs to be installed as brew python package doesn't come packaged with tkinter, unlike Windows.

```bash
brew install python-tk@3.9
```

Other than that, installing `requirements.txt` via pip would suffice, as for `.env` file in local machine, use this format:

```bash
LASTFM_API = "API_KEY_HERE"
LASTFM_USER = "USERNAME_HERE"
GENIUS_API = "ACCESS_TOKEN_HERE"
```
