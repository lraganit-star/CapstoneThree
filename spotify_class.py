import pandas as pd
import numpy as np

import cv2
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import cred

from numpy.linalg import svd
from sklearn.metrics.pairwise import cosine_similarity
import webcam

import random

class playlist:
    
    #access the spotify api
    def __init__(self, username, playlist_id, webcam.camera.camera()):    
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, 
                                    client_secret= cred.client_SECRET, 
                                    redirect_uri= cred.redirect_uri'))            
        
        self.angry = pd.read_csv('angry.csv', index_col = 'uri')
        self.happy = pd.read_csv('happy.csv', index_col = 'uri')
        self.neutral = pd.read_csv('neutral.csv', index_col = 'uri')
        self.sad = pd.read_csv('sad.csv', index_col = 'uri')

        self.username = username
        self.playlist_id = playlist_id

        self.tracks_uri = self.get_playlist_tracks()
        self.audio_feats()
        
        
        self.emo = str(emos)

        if self.emo == 'Angry':
            self.emo = self.angry
        
        elif self.emo == 'Happy':
            self.emo = self.happy
        
        elif self.emo == 'Neutral':
            self.emo = self.neutral
        
        elif self.emo == 'Sad':
            self.emo = self.sad

        self.combo_df = self.combo()
        self.combo1_df = self.combo1()
      
        self.rec()

    def get_playlist_tracks(self):
    ###############################################################
    # from a playlist, this obtains each songs' uri from spotify api
    # inputs: spotify user id and spotify user id (obtained through spotify app)
    # outputs: list of spotify uris
    ################################################################
        
        results = self.sp.user_playlist_tracks(self.username,self.playlist_id)
        tracks = results['items']

        #allows us to have more than 100 songs if the playlist is large
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])

        self.tracks_uri = []
        for i in range(len(tracks)):
            self.tracks_uri.append(tracks[i]['track']['uri'])

        if self.username == '1213470849':
            self.tracks_uri.remove('spotify:local:Bill+Withers:The+70%27s+-+1972+-+CD+2:Lean+On+Me:259')

        return self.tracks_uri


    def audio_feats(self):    
    ##########################################################
    # Gets features from the songs
    # input: list of song apis
    # output: dictionary of song features, song api shown as index
    ##########################################################

        dict_feats = {}  
        for i in range(len(self.tracks_uri)):
            features = self.sp.audio_features(self.tracks_uri[i])[0]
            key = list(features.keys())
            
            for k in key:
                if k not in list(dict_feats.keys()):
                    dict_feats[k] = [features[k]]
                else:
                    dict_feats[k].append(features[k])
        
        self.df = pd.DataFrame.from_dict(dict_feats)
        self.df = self.df.drop(columns = ['type','id','track_href','analysis_url','duration_ms','time_signature','mode','key'])
        self.df = self.df.set_index('uri')


    def combo(self):
    ####################################################################
    # combining emotion df with user df
    # including adding labels with user:1, emotion:0
    # input: emotion of focus as a df
    # output: df of concatinated emotion and user with user:1, emotion:0
    #####################################################################
        
        dfs = [self.emo, self.df]
        self.emo['label'] = int(0)
        self.df['label'] = int(1)
        self.combo_df = pd.concat([self.emo,self.df])
        return self.combo_df


    def combo1(self):
    ################################################################################
    # This function is for running SVD, so it doesn't count the labels as a feature
    # input: emotion dataframe
    # output: emotion + user dataframe (no labels)
    #################################################################################
        return pd.concat([self.emo,self.df])


    def rec(self):
    #####################################################################################
    # inputs:
    #   df is obtained through combo1 function of concatinated emotion and user playlists
    #   combo is the df with labels indicating emo playlist(0) or user playlist(1)
    # output: list of songs that are the most similar to indicated emotion
    ######################################################################################
        
        arr = self.combo1_df.to_numpy() #need to have a numpy array for svd
        u, _, _ = svd(arr, compute_uv = True, full_matrices=True)
        
        lst = []
        for i in range(len(arr)):
            cs = self.combo1_df.index.values[cosine_similarity(u)[i].argsort()][1]
            lst.append(cs)
        
        final_lst = []
        for song in lst:
            if (self.combo_df.loc[song]['label']).tolist() == 1:
                final_lst.append(song)
        print(final_lst)