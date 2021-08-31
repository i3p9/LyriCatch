import tkinter as tk
from tkinter import ttk, Tk, Text, scrolledtext, Label, filedialog, font, Frame
from tkinter.messagebox import showinfo
import tkinter.scrolledtext as scrolledtext
from time import sleep
from dotenv import load_dotenv
import os
import requests
import json
from pprint import pprint
import sys
import codecs
import lyricsgenius
from getNowPlayingInfo import grabNowPlayingOSX

# Fix windows HiDPI blurry mess
def hidpiDetection():
    import os
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        windll.shcore.SetProcessDpiAwareness(1)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Draw()
    def Draw(self):
        self.title('Spotify Lyrics')
        self.geometry('500x600+50+50')
        self.iconbitmap('./icon.ico')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)

        #download_icon = tk.PhotoImage(file='./download.png')
        # Initating buttons
        refreshButton = ttk.Button(self, text='Refresh',compound=tk.LEFT,command=self.drawLyrics)
        refreshButton.grid(column=0, row=0, sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)

        saveButton = ttk.Button(self, text='Save Lyrics to File',command=self.saveLyricsToFile)
        saveButton.grid(column=0, row=1, sticky=tk.W, padx=3, pady=5)

        configButton = ttk.Button(self, text='Configuration',command=lambda: self.configApp())
        configButton.grid(column=1, row=1, sticky=tk.W, padx=3, pady=5)

        exitButton = ttk.Button(self, text='Exit',command=lambda: self.quit())
        exitButton.grid(column=1, row=0, sticky=tk.W, padx=3, pady=5)

        self.label = Label(self, text='Press Refresh to Look Up Lyrics')
        self.label.grid(columnspan=3, row=2, sticky=tk.EW, padx=3, pady=5)

        # Separator between buttons and lyrics text box
        # separator = ttk.Separator(self, orient='horizontal')
        # separator.pack(fill='x')

        #Initiate lyrics text box
        self.lyric_box = scrolledtext.ScrolledText(self, height=45,font=("Helvetica", 10))
        self.lyric_box.grid(columnspan=3, row=3,sticky=tk.S)


    def drawLyrics(self):
        #Gets lyrics, artist and title info to show
        artist, song, lyric_text = backend.getLyrics()
        self.lyrics_file = lyric_text
        song_info = "Now Playing: "+str(artist)+"- "+str(song)
        # Update lyrics and NowPlaying text automatically
        self.lyric_box.delete('1.0', 'end')
        self.lyric_box.insert('end',lyric_text)
        self.label.configure(text=song_info)

    def saveLyricsToFile(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.write(self.lyrics_file)
        f.close()
        successfulDialog = ttk.Button(self,text='Show an information message',command=lambda: showinfo(
            title='Information',message='This is an information message.'))
        successfulDialog.pack(fill='both', padx=10, pady=10, ipadx=5)

    def configApp(self):
        echo ("Under construction")


class Lyrics:
    def __init__(self):
        super().__init__()
    def getSong(self):
        #Set API endpoints and hardcode username and access_token from Last.fm
        base_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
        user = os.environ.get("LASTFM_USER")
        key = os.environ.get("LASTFM_API")
        r = requests.get(base_url+user+'&api_key='+key+'&format=json')
        data = json.loads(r.text)
        latest_track = data['recenttracks']['track'][0]
        try:
            if latest_track['@attr']['nowplaying'] == 'true':
                artist = latest_track['artist']['#text']
                song = latest_track['name']
                album = latest_track['album']['#text']
                print ("\nNow Playing: {0} - {1}".format(artist, song))
                return artist,song
        except KeyError:
            print ('Nothing playing...')
            return ('Nothing playing...')

    def getLyrics(self):
        #artist, song = self.getSong()
        artist, song = grabNowPlayingOSX()
        genius_access_token = os.environ.get("GENIUS_API")
        genius = lyricsgenius.Genius(genius_access_token)
        req_song =genius.search_song(title=song, artist=artist, song_id=None, get_full_info=True)
        lyrics = str(req_song.lyrics)
        print(artist)
        print(song)
        return artist, song, lyrics

    def saveLyrics(self,lyrics):
        text_file = open("out.txt", "w")
        text_file.write(lyrics)
        text_file.close()


if __name__ == "__main__":
    hidpiDetection()
    load_dotenv()
    backend = Lyrics()
    app = App()
    app.mainloop()





## TO DO ACCESS TOKEN
# access_token = tk.StringVar()

# get_token = ttk.Frame(root)
# get_token.pack(padx=10, pady=10, fill='x', expand=True)

# token_label = ttk.Label(get_token, text="Access Token:")
# token_label.pack(fill='x', expand=True)

# token_entry = ttk.Entry(get_token, textvariable=access_token)
# token_entry.pack(fill='x', expand=True)
# token_entry.focus()

# token_submit_button = ttk.Button(get_token, text="Submit", command=access_token_clicked)
# token_submit_button.pack(fill='x', expand=True, pady=10)
