import streamlit as st
import pandas as pd
import numpy as np

#Preperation of the data 
from sklearn import cluster
from sklearn.preprocessing import StandardScaler

#Usupervised Machine Learning
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import DBSCAN

#Visualisation
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#Imporing Random Rows
import random

#Evaluation metrics
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import calinski_harabasz_score

# Spotify
import config
from config import CLIENT_ID, CLIENT_SECRET
from IPython.display import IFrame
import spotipy 
import json
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64

af_df = pd.read_csv(r"C:\Users\ramya\Downloads\audio_features_dataset (1).csv").drop(columns=["Unnamed: 0"])
af_df.drop_duplicates(inplace=True)
af_df.dropna(inplace=True)

song_details = af_df[["track_id", "artists", "album_name", "track_name"]]
af_df.drop(columns=["track_id", "artists", "album_name", "track_name"], inplace=True)

top_100 = pd.read_csv(r"C:\Users\ramya\Downloads\top_100.csv")

def get_spotify_token(client_id, client_secret):
    client_credentials = f"{client_id}:{client_secret}"
    client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()
    headers = {"Authorization": f"Basic {client_credentials_b64}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")

token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def play_song(track_id):
    song_url = f"https://open.spotify.com/embed/track/{track_id}"
    st.components.v1.iframe(song_url, width=320, height=80)




def recommend_a_genre(user_preference):
    genre_list = ["trending now"]
    if user_preference.lower() == "trending now":
        recommended_song = random.choice(top_100['song'])
        artist_of_recommended_song = top_100.loc[top_100["song"] == recommended_song, "artist"].values[0]
        st.write("We recommend you these two songs")
        st.write(f"We recommend: ({recommended_song}) by ({artist_of_recommended_song})")
        recommended_billboard_song_id = sp.search(q=recommended_song, limit=1)["tracks"]["items"][0]["id"]
        play_song(recommended_billboard_song_id)
        top_99 = top_100[top_100['song'] != recommended_song]
        recommended_song_1 = random.choice(top_99['song'])
        artist_of_recommended_song_1 = top_99.loc[top_99["song"] == recommended_song_1, "artist"].values[0]
        st.write(f"We recommend: ({recommended_song_1}) by ({artist_of_recommended_song_1})")
        recommended_billboard_song_id_1 = sp.search(q=recommended_song_1, limit=1)["tracks"]["items"][0]["id"]
        play_song(recommended_billboard_song_id_1)
    else:
        st.write("Sorry, this genre is not available.")

# Streamlit App
st.title('Song Recommender')


user_preference = st.selectbox("Pick Your Favourite Genre", ["Trending Now", "Other"])
if st.button("Recommend"):
    recommend_a_genre(user_preference)