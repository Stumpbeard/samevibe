import json
import os

from flask import Flask, render_template, request, redirect
import requests

import db
from serializers import Album, Game, Movie, Book, SearchResult

USER_AGENT = "SameVibe/0.1 +https://samevi.be"
MUSIC_KEY = os.environ.get("DISCOGS_CONSUMER_KEY")
MUSIC_SECRET = os.environ.get("DISCOGS_CONSUMER_SECRET")
MOVIE_KEY = os.environ.get("OMDB_API_KEY")
GAMES_KEY = os.environ.get("RAWG_API_KEY")
BOOKS_KEY = os.environ.get("GOOGLE_API_KEY")
DISCOGS_API = "https://api.discogs.com"
OMDB_API = "http://www.omdbapi.com"
RAWG_API = "https://api.rawg.io/api"
GBOOKS_API = "https://www.googleapis.com/books/v1"
HEADERS = {
    "User-Agent": USER_AGENT,
}


app = Flask(__name__)
db.init_db()


@app.route("/")
def hello_world():
    vibes = db.get_all_vibes()
    most_recent_vibes = make_vibe_pairs(vibes)

    return render_template("hello.html", most_recent_vibes=most_recent_vibes)


@app.route("/loaderio-9f5e57e7decacfa267f90d5884bb7d0b/")
def load_test():
    return "loaderio-9f5e57e7decacfa267f90d5884bb7d0b"


@app.route("/search")
def search():
    q = request.args.get("q")
    type = request.args.get("type")
    if type == "movie":
        results = search_movies(q)
    elif type == "game":
        results = search_games(q)
    elif type == "book":
        results = search_books(q)
    else:
        results = search_music(q)
    return render_template(
        "search.html", search_value=q, results=results, search_type=type
    )


@app.route("/vibes")
def vibe_search():
    q = request.args.get("q")
    vibes = db.search_vibes(q)

    return render_template("vibe-search.html", search=q, vibes=vibes)


@app.route("/vibes/<vibe>")
def vibe_page(vibe):
    ids = db.search_unique_ids_for_vibe(vibe)
    results = []
    for id in ids:
        media = get_item_by_type(id[0], id[1])
        item = SearchResult.from_serial(media, media.type)
        results.append(item)

    return render_template("list-media-for-vibe.html", results=results, vibe=vibe)


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
    elif main_type == "game":
        data = get_game(id).__dict__
    elif main_type == "book":
        data = get_book(id).__dict__
    else:
        data = get_album(id).__dict__

    q = request.args.get("q")
    type = request.args.get("type")
    results = None
    if q:
        if type == "movie":
            results = search_movies(q)
        elif type == "game":
            results = search_games(q)
        elif type == "book":
            results = search_books(q)
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
        subsearch_text=q or "",
    )


@app.route("/<main_type>/<id>/connect/<type>/<related_id>")
def relate_items(main_type, id, type, related_id):
    if main_type == "movie":
        primary = get_movie(id)
    elif main_type == "game":
        primary = get_game(id)
    elif main_type == "book":
        primary = get_book(id)
    else:
        primary = get_album(id)

    primary_vibes = db.find_vibes(primary.id)

    if type == "movie":
        related = get_movie(related_id)
    elif type == "game":
        related = get_game(related_id)
    elif type == "book":
        related = get_book(related_id)
    else:
        related = get_album(related_id)

    related_vibes = db.find_vibes(related.id)

    return render_template(
        "relate-items.html",
        main_type=main_type,
        primary=primary,
        primary_vibes=primary_vibes,
        related=related,
        related_vibes=related_vibes,
        type=type,
    )


@app.route("/<main_type>/<id>/vibe/<vibe>")
def list_vibe_connections(main_type, id, vibe):
    if main_type == "movie":
        data = get_movie(id)
    elif main_type == "game":
        data = get_game(id)
    elif main_type == "book":
        data = get_book(id)
    else:
        data = get_album(id)

    vibes = db.find_vibes(id)

    connection_ids = db.find_connections_by_vibe(id, vibe)
    connections = []
    for connection in connection_ids:
        connection_id = connection[0]
        type = connection[1]
        if type == "movie":
            connection = get_movie(connection_id)
        elif type == "game":
            connection = get_game(connection_id)
        elif type == "book":
            connection = get_book(connection_id)
        else:
            connection = get_album(connection_id)

        connection = SearchResult.from_serial(connection, type)

        connections.append(connection)

    return render_template(
        "connections.html",
        connections=connections,
        main_id=id,
        vibe=vibe,
        main_type=main_type,
        data=data,
        vibes=vibes,
    )


def search_music(q, page=1):
    url = f"{DISCOGS_API}/database/search?q={q}&type=master&key={MUSIC_KEY}&secret={MUSIC_SECRET}&per_page=10&page={page}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("results")

    return [SearchResult.from_discogs(result) for result in results]


def search_movies(q):
    url = f"{OMDB_API}/?apikey={MOVIE_KEY}&s={q}&type=movie"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("Search")

    return [SearchResult.from_omdb(result) for result in results]


def search_books(q):
    url = f"{GBOOKS_API}/volumes?q={q}&orderBy=relevance"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("items")

    return [SearchResult.from_googlebooks(result) for result in results]


def search_games(q):
    url = f"{RAWG_API}/games?key={GAMES_KEY}&search={q}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response).get("results")

    return [SearchResult.from_rawg(result) for result in results]


def get_album(id):
    album = db.get_album(id)
    if album:
        return album

    url = f"{DISCOGS_API}/masters/{id}?key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    response = requests.get(url, headers=HEADERS).content
    results = json.loads(response)
    album = Album.from_discogs(results)
    db.save_album(album)

    return Album.from_discogs(results)


def get_movie(id):
    movie = db.get_movie(id)
    if movie:
        return movie

    url = f"{OMDB_API}/?apikey={MOVIE_KEY}&i={id}"
    response = requests.get(url, headers=HEADERS).content
    result = json.loads(response)
    movie = Movie.from_omdb(result)
    db.save_movie(movie)

    return Movie.from_omdb(result)


def get_game(id):
    game = db.get_game(id)
    if game:
        return game

    url = f"{RAWG_API}/games/{id}?key={GAMES_KEY}"
    response = requests.get(url, headers=HEADERS).content
    result = json.loads(response)
    game = Game.from_rawg(result)
    db.save_game(game)

    return game


def get_book(id):
    book = db.get_book(id)
    if book:
        return book

    url = f"{GBOOKS_API}/volumes/{id}"
    response = requests.get(url, headers=HEADERS).content
    result = json.loads(response)
    book = Book.from_google(result)
    db.save_book(book)

    return book


def make_vibe_pairs(vibes):
    vibe_pairs = []
    for vibe in vibes:
        vibe_pair = {
            "primary": get_item_by_type(vibe[1], vibe[2]),
            "related": get_item_by_type(vibe[3], vibe[4]),
            "type": vibe[5],
        }
        vibe_pairs.append(vibe_pair)

    return vibe_pairs


def get_item_by_type(id, type):
    if type == "movie":
        return get_movie(id)
    if type == "book":
        return get_book(id)
    if type == "game":
        return get_game(id)
    if type == "album":
        return get_album(id)

    return None
