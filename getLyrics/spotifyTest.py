import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk


client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
scope = "user-modify-playback-state"
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager, scope=scope)


def search_song_uri(query):
    results = sp.search(q=query, type="track", limit=1)
    if results["tracks"]["items"]:
        return results["tracks"]["items"][0]["uri"]
    else:
        return None


def play_song():
    song_uri = search_song_uri(entry.get())
    if song_uri:
        sp.start_playback(uris=[song_uri])
        status_label.config(text="Song playing...")
    else:
        status_label.config(text="Song not found.")


def stop_song():
    sp.pause_playback()
    status_label.config(text="Playback stopped.")


window = tk.Tk()
window.title("Spotify Player")

search_label = tk.Label(window, text="Search Song:")
search_label.pack()
entry = tk.Entry(window)
entry.pack()

search_button = tk.Button(window, text="Search", command=play_song)
search_button.pack()

play_button = tk.Button(window, text="Play", command=play_song)
play_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_song)
stop_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()

play_button = tk.Button(window, text="Play", command=play_song)
play_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_song)
stop_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()

