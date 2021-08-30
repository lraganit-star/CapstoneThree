import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import cred

import spotify_class as sc
import cv2_trial

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, 
                                    client_secret= cred.client_SECRET, 
                                    redirect_uri= 'http://localhost'))

username = input("Enter username or user number: ")
playlist_id = input("Enter playlist id: ")

emo = cv2_trial
print(emo)
pl = sc.playlist(username = username, playlist_id = playlist_id, emo = emo)


# niki = get_playlist_tracks(username = '1238338842',
                           #playlist_id = 'spotify:playlist:37i9dQZF1EpkhImEQWvPYp')
