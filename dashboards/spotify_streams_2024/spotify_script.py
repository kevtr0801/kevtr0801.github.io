import pandas as pd
import requests
import time

# STEP 1: Set your credentials
client_id = 'XXX'
client_secret = 'XXX'

# STEP 2: Authenticate with Spotify (Client Credentials Flow)
def get_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    return response.json()['access_token']

token = get_token(client_id, client_secret)
headers = {'Authorization': f'Bearer {token}'}

# STEP 3: Load your CSV
df = pd.read_csv('spotify_streams_2024.csv', encoding='ISO-8859-1')

# STEP 4: Function to search for track and get album image
def get_album_cover(track, artist):
    query = f"{track} {artist}"
    url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    results = r.json()
    try:
        return results['tracks']['items'][0]['album']['images'][0]['url']
    except (IndexError, KeyError):
        return None

# STEP 5: Add a new column with album cover URLs
album_covers = []
for index, row in df.iterrows():
    cover_url = get_album_cover(row['Track'], row['Artist'])
    album_covers.append(cover_url)

df['Album Cover URL'] = album_covers

# STEP 6: Save new CSV
df.to_csv('spotify_streams_2024_updated.csv', index=False)
print("Done")
