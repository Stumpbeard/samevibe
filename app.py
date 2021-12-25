from dataclasses import dataclass
import json
import os
from typing import List

from flask import Flask, render_template, request, redirect
import requests

import db
from serializers import Album, Movie

USER_AGENT = "SameVibe/0.1 +https://samevi.be"
MUSIC_KEY = os.environ.get("DISCOGS_CONSUMER_KEY")
MUSIC_SECRET = os.environ.get("DISCOGS_CONSUMER_SECRET")
MOVIE_KEY = os.environ.get("OMDB_API_KEY")
GAMES_KEY = os.environ.get("RAWG_API_KEY")
DISCOGS_API = "https://api.discogs.com"
OMDB_API = "http://www.omdbapi.com"
RAWG_API = "https://api.rawg.io/api"
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
    type = request.args.get("type")
    if type == "movie":
        results = search_movies(q)
    else:
        results = search_music(q)
    return render_template("search.html", search=q, results=results, type=type)


@app.route("/<main_type>/<id>", methods=["GET", "POST"])
def details(main_type, id):
    if request.method == "POST":
        vibe = request.form.get("vibe")
        related_id = request.form.get("related_id")
        type = request.form.get("type")
        if vibe and related_id:
            db.create_vibe_connection(id, main_type, related_id, type, vibe)
        return redirect(f"/{main_type}/{id}")

    if main_type == "movie":
        data = get_movie(id).__dict__
    else:
        data = get_album(id).__dict__

    q = request.args.get("q")
    type = request.args.get("type")
    results = None
    if q:
        if type == "movie":
            results = search_movies(q)
        else:
            results = search_music(q)

    vibes = db.find_vibes(id)

    return render_template(
        "details.html",
        id=id,
        vibes=vibes,
        results=results,
        type=type,
        data=data,
        main_type=main_type,
    )


@app.route("/<main_type>/<id>/connect/<type>/<related_id>")
def relate_items(main_type, id, type, related_id):
    if main_type == "movie":
        primary = get_movie(id)
    else:
        primary = get_album(id)

    if type == "movie":
        related = get_movie(related_id)
    else:
        related = get_album(related_id)

    return render_template(
        "relate-items.html",
        main_type=main_type,
        primary=primary.__dict__,
        related=related.__dict__,
        type=type,
    )


@app.route("/<main_type>/<id>/vibe/<vibe>")
def list_vibe_connections(main_type, id, vibe):
    connection_ids = db.find_connections_by_vibe(id, vibe)
    connections = []
    for connection in connection_ids:
        connection_id = connection[0]
        type = connection[1]
        if type == "movie":
            connection = get_movie(connection_id).__dict__
        else:
            connection = get_album(connection_id).__dict__
        connection["id"] = connection_id
        connection["type"] = type

        connections.append(connection)

    return render_template(
        "connections.html",
        connections=connections,
        main_id=id,
        vibe=vibe,
        main_type=main_type,
    )


def search_music(q):
    url = f"{DISCOGS_API}/database/search?q={q}&type=master&key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("results")

    return results


def search_movies(q):
    url = f"{OMDB_API}/?apikey={MOVIE_KEY}&s={q}&type=movie"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("Search")

    return results


def search_games(q):
    url = f"{RAWG_API}/games?key={GAMES_KEY}&search={q}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)

    return results


def get_album(id):
    url = f"{DISCOGS_API}/masters/{id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)

    return Album.from_discogs(results)


def get_movie(id):
    url = f"{OMDB_API}/?apikey={MOVIE_KEY}&i={id}"
    response = requests.get(url, headers=HEADERS).content
    result = json.loads(response)

    return Movie.from_omdb(result)
