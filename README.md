# LyriCatch

Cross Platform desktop application to view and download lyrics of the song that's currently being played. It supports ANY Music Player connted to Last.fm and Spotify (natively) for now.

## Requiremnts

GUI is made using python-tkinter, if building using macOS on a python3 installation via `brew`, `python-tk@3.9` also needs to be installed as brew python package doesn't come packaged with tkinter, unlike Windows.

```bash
brew install python-tk@3.9
```

Then install the requirements via pip (or pip3), after that, rename `.env.example` to `.env` and put your API keys there.

## Screenshots

![LyriCatch Screenshot macOS](https://i.imgur.com/dmsBEAf.png)
