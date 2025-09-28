from flask import Flask, request, render_template
import requests

app = Flask(__name__)

LASTFM_API_URL = 'http://ws.audioscrobbler.com/2.0'
API_KEY = '2993c6e15c91a2890c2f11fa95673067'

def get_recent_tracks(user):
    url = f"{LASTFM_API_URL}/?method=user.getrecenttracks&user={user}&api_key={API_KEY}&format=json"
    try:
        response = requests.get(url)
        resp = response.json()
    except Exception as e:
        print(f"Error fetching Last.fm data: {e}")
        return []

    raw_tracks = resp.get('recenttracks', {}).get('track', [])
    tracks = []
    for track in raw_tracks:
        imgsrc = track['image'][0]["#text"] or "http://cdn.last.fm/flatness/catalogue/noimage/2/default_artist_small.png"
        tracks.append({
            'name': track['name'],
            'artist': track['artist']['#text'],
            'url': track['url'],
            'image_url': imgsrc
        })
    return tracks

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/last', methods=['POST'])
def lastfm():
    user = request.form.get('username', '')
    tracks = get_recent_tracks(user)
    return render_template('results.html', user=user, tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)

