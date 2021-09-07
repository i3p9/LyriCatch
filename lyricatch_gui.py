import tkinter as tk
from tkinter import Button, Entry, Toplevel, ttk, Tk, Text, scrolledtext, Label, filedialog, messagebox, font, Frame
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
from pathlib import Path
from getNowPlayingInfo import grabNowPlayingOSX

# Fix windows HiDPI blurry mess
def hidpiDetection():
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        windll.shcore.SetProcessDpiAwareness(1)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Draw()
    def Draw(self):
        self.title('LyriCatch')
        self.geometry('500x600+50+50')

        if(sys.platform == 'darwin'):
            iconFile = 'assets/icon_mac.icns'

        elif(sys.platform == 'win32'):
            iconFile = '/assets/icon_win.ico'

        self.iconbitmap(iconFile)

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
        self.lyric_box = scrolledtext.ScrolledText(self, height=45,font=("Helvetica", 15))
        self.lyric_box.grid(columnspan=3, row=3,sticky=tk.S)


    def drawLyrics(self):
        f = open("config.txt")

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
        self.configWindow = Toplevel(self)
        self.configWindow.title("configure")
        self.configWindow.geometry("500x200")
        self.configWindow.columnconfigure(0,weight=1)
        self.configWindow.columnconfigure(1,weight=3)


        geniusAPILabel = Label(self.configWindow, text="Enter Genius access token")
        geniusAPILabel.grid(column=0,row=0,sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)

        # LastfmUsernameLabel = Label(self.configWindow, text="Enter Last.fm username")
        # LastfmUsernameLabel.grid(column=0,row=1,sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)

        # LastfmAPILabel = Label(self.configWindow, text="Enter Last.fm access token")
        # LastfmAPILabel.grid(column=0,row=2,sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)


        self.geniusAPITextBox = Text(self.configWindow, width=30,height=1)
        # self.LastfmUsernameTextBox = Text(self.configWindow, width=30,height=1)
        # self.LastfmAPITextBox = Text(self.configWindow, width=30,height=1)

        savetokenButton = ttk.Button(self.configWindow,text="save",command=lambda: self.saveToken())
        savetokenButton.grid(column=1,row=4,sticky=tk.N, padx=3, pady=5,ipadx=0,ipady=0)

        # WIP for saving multiple options
        # with open('config.txt', 'r') as file:
        #     configdata = file.readlines()

        # #configfile = open("config.txt")
        # self.geniusAPITextBox.insert(1.0,configdata[0])
        # self.LastfmUsernameTextBox.insert(1.0,configdata[1])
        # self.LastfmAPITextBox.insert(1.0,configdata[2])
        # file.close()

        geniusAPIFromFile = Path('config.txt').read_text()
        geniusAPIFromFile = geniusAPIFromFile.replace('\n', '')
        self.geniusAPITextBox.insert(1.0,geniusAPIFromFile)


        self.geniusAPITextBox.grid(column=1,row=0,sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)
        # self.LastfmUsernameTextBox.grid(column=1,row=1,sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)
        # self.LastfmAPITextBox.grid(column=1,row=2,sticky=tk.W, padx=3, pady=5,ipadx=0,ipady=0)

    def saveToken(self):
        f = open("config.txt",'w')
        f.write(self.geniusAPITextBox.get(1.0, 'end'))
        print('should be saved.....')
        f.close()
        tk.messagebox.showinfo('FYI','Token saved to file successfully')

    # def for saving multiple files, WIP
    # def saveToken(self):
    #     self.replace_line('config.txt', 0, self.geniusAPITextBox.get(1.0, 'end'))
    #     self.replace_line('config.txt', 1, self.LastfmUsernameTextBox.get(1.0, 'end'))
    #     self.replace_line('config.txt', 2, self.LastfmAPITextBox.get(1.0, 'end'))
    #     tk.messagebox.showinfo('FYI','Token saved to file successfully')

    def replace_line(self,file_name, line_num, text):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()


class Lyrics:
    def __init__(self):
        super().__init__()
    def getSong(self):
        #Set API endpoints and get username and access_token of Last.fm from env
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
        if(sys.platform == 'darwin'):
            artist, song = grabNowPlayingOSX()
        else:
            artist, song = self.getSong()

        # get token from env
        #genius_access_token = os.environ.get("GENIUS_API")
        # get token from config.txt
        genius_access_token_txt = Path('config.txt').read_text()
        genius_access_token_txt = genius_access_token_txt.replace('\n', '')
        print(genius_access_token_txt)
        genius = lyricsgenius.Genius(genius_access_token_txt)
        req_song =genius.search_song(title=song, artist=artist, song_id=None, get_full_info=True)
        lyrics = str(req_song.lyrics)
        print(artist)
        print(song)
        return artist, song, lyrics


if __name__ == "__main__":
    hidpiDetection()
    load_dotenv()
    backend = Lyrics()
    app = App()
    app.mainloop()
