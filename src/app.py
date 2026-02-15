import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()


# Spotify API credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")


auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

alejandro_sanz_id='5sUrlPAHlS9NEirDB8SEbF'

try:
    # Get artist info first (this usually works even in Dev Mode)
    artist = spotify.artist(alejandro_sanz_id)
    print(f"✓ Successfully got artist: {artist['name']}")
    exit
    results = spotify.artist_top_tracks(alejandro_sanz_id, country='ES')
    tracks = results['tracks']

except Exception as e:
    print(f"Problems to access to the Spotify API: {str(e)[:80]}")


# Create lists to store the data
songs_data = []

for track in tracks:
    song_name = track['name']
    popularity = track['popularity']
    duration_ms = track['duration_ms']
    duration_minutes = duration_ms / 60000  # Convert milliseconds to minutes
    
    songs_data.append({
        'Song Name': song_name,
        'Popularity': popularity,
        'Duration (minutes)': round(duration_minutes, 2)
    })
    
    print(f"Song: {song_name}")
    print(f"Popularity: {popularity}")
    print(f"Duration: {round(duration_minutes, 2)} minutes")
    print("-" * 50)

# Create a DataFrame 
df_tracks = pd.DataFrame(songs_data)
print(f"\nTop {len(df_tracks)} tracks:")

# Relationship between Popular song and Duration
# Scatter plot: Popularity vs Duration
plt.figure(figsize=(10, 6))
plt.scatter(df_tracks['Duration (minutes)'], df_tracks['Popularity'], 
            alpha=0.7, s=100)


plt.xlabel('Duration (minutes)', fontsize=12)
plt.ylabel('Popularity', fontsize=12)
plt.title('Relationship between Song Duration and Popularity', fontsize=14, fontweight='bold')


plt.grid(True, alpha=0.3)


for i, row in df_tracks.iterrows():
    plt.annotate(row['Song Name'][:20], 
                 (row['Duration (minutes)'], row['Popularity']),
                 fontsize=8, alpha=0.6, rotation=15)

plt.tight_layout()
plt.show()

correlation = df_tracks['Duration (minutes)'].corr(df_tracks['Popularity'])
print(f"\nCorrelation coefficient: {correlation:.3f}")

if abs(correlation) < 0.3:
    print("→ Weak correlation: Duration doesn't seem to significantly affect popularity.")
elif abs(correlation) < 0.7:
    print("→ Moderate correlation: There's some relationship between duration and popularity.")
else:
    print("→ Strong correlation: Duration has a significant impact on popularity.")