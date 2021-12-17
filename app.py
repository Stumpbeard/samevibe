import json
import os

from flask import Flask, render_template, request
import requests


USER_AGENT = "SameVibe/0.1 +https://samevi.be"
MUSIC_KEY = os.environ.get("DISCOGS_CONSUMER_KEY")
MUSIC_SECRET = os.environ.get("DISCOGS_CONSUMER_SECRET")
DISCOGS_API = "https://api.discogs.com"
HEADERS = {
    "User-Agent": USER_AGENT,
}


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("hello.html", key=MUSIC_KEY, secret=MUSIC_SECRET)


@app.route("/search")
def search():
    q = request.args.get("q")
    url = f"{DISCOGS_API}/database/search?q={q}&type=release&key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("results")
    return render_template("search.html", search=q, results=results[:10])


@app.route("/release/<id>")
def music_release(id):
    url = f"{DISCOGS_API}/releases/{id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)
    print(results)
    artist = results.get("artists", [None])[0].get("name")
    title = results.get("title")
    tracklist = results.get("tracklist", [])
    image_url = results.get("images", [None])[0].get("resource_url")
    print("image_url", image_url)
    return render_template(
        "artist-release.html",
        artist=artist,
        title=title,
        tracklist=tracklist,
        image_url=image_url,
    )
