import json
import os
import sqlite3

from flask import Flask, render_template, request, redirect
import requests

import db


USER_AGENT = "SameVibe/0.1 +https://samevi.be"
MUSIC_KEY = os.environ.get("DISCOGS_CONSUMER_KEY")
MUSIC_SECRET = os.environ.get("DISCOGS_CONSUMER_SECRET")
DISCOGS_API = "https://api.discogs.com"
HEADERS = {
    "User-Agent": USER_AGENT,
}


app = Flask(__name__)
db.init_db()


@app.route("/")
def hello_world():
    return render_template("hello.html")


@app.route("/search")
def search():
    q = request.args.get("q")
    results = search_music(q)
    return render_template("search.html", search=q, results=results[:10])


@app.route("/release/<id>", methods=["GET", "POST"])
def music_release(id):
    if request.method == "POST":
        vibe = request.form.get("vibe")
        related_id = request.form.get("related_id")
        if vibe and related_id:
            db.create_vibe_connection(id, related_id, vibe)
        return redirect(f"/release/{id}")

    url = f"{DISCOGS_API}/releases/{id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)
    artist = results.get("artists", [None])[0].get("name")
    title = results.get("title")
    tracklist = results.get("tracklist", [])
    image_url = results.get("images", [None])[0].get("resource_url")

    q = request.args.get("q")
    results = None
    if q:
        results = search_music(q)

    vibes = db.find_vibes(id)

    return render_template(
        "artist-release.html",
        id=id,
        artist=artist,
        title=title,
        tracklist=tracklist,
        image_url=image_url,
        results=results,
        vibes=vibes,
    )


@app.route("/release/<id>/connect/<related_id>")
def music_release_related(id, related_id):
    url = f"{DISCOGS_API}/releases/{id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)
    artist = results.get("artists", [None])[0].get("name")
    title = results.get("title")
    tracklist = results.get("tracklist", [])
    image_url = results.get("images", [None])[0].get("resource_url")

    url = f"{DISCOGS_API}/releases/{related_id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)
    artist_2 = results.get("artists", [None])[0].get("name")
    title_2 = results.get("title")
    tracklist_2 = results.get("tracklist", [])
    image_url_2 = results.get("images", [None])[0].get("resource_url")

    return render_template(
        "artist-release-related.html",
        id=id,
        related_id=related_id,
        artist=artist,
        title=title,
        tracklist=tracklist,
        image_url=image_url,
        artist_2=artist_2,
        title_2=title_2,
        tracklist_2=tracklist_2,
        image_url_2=image_url_2,
    )


@app.route("/release/<id>/vibe/<vibe>")
def list_vibe_connections(id, vibe):
    connection_ids = db.find_connections_by_vibe(id, vibe)
    connections = []
    for connection_id in connection_ids:
        url = f"{DISCOGS_API}/releases/{connection_id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
        response = requests.get(url, headers=HEADERS).content
        results = json.loads(response)
        connection = {
            "id": results.get("id"),
            "artist": results.get("artists", [None])[0].get("name"),
            "title": results.get("title"),
        }
        connections.append(connection)

    return render_template(
        "connections.html", connections=connections, main_id=id, vibe=vibe
    )


def search_music(q):
    url = f"{DISCOGS_API}/database/search?q={q}&type=release&key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("results")

    return results
