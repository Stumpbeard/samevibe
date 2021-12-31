from datetime import datetime
import json
import sqlite3

from serializers import Album, Book, Game, Movie, Vibe


def init_db():
    with open("sql/create_tables.sql") as f:
        sql = f.read()
        connection = sqlite3.connect("samevibe.db")
        cursor = connection.cursor()
        cursor.executescript(sql)


def create_vibe_connection(id, id_type, related_id, related_type, vibe):
    connection = sqlite3.connect("samevibe.db")
    vibe = (
        vibe.lower()
        .replace("http", "")
        .replace(".", "")
        .replace("/", "")
        .replace(":", "")
    )
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO relationships (primary_obj, primary_type, secondary_obj, secondary_type, vibe) VALUES (?, ?, ?, ?, ?);",
        (id, id_type, related_id, related_type, vibe),
    )
    connection.commit()


def recreate_tables():

    with open("sql/drop_tables.sql") as f:
        connection = sqlite3.connect("samevibe.db")
        cursor = connection.cursor()
        sql = f.read()
        cursor.executescript(sql)
    with open("sql/create_tables.sql") as f:
        connection = sqlite3.connect("samevibe.db")
        cursor = connection.cursor()
        sql = f.read()
        cursor.executescript(sql)


def find_vibes(id):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT vibe, count(id) FROM relationships WHERE primary_obj = ? or secondary_obj = ? GROUP BY vibe ORDER BY count(id) desc LIMIT 10",
        (id, id),
    ).fetchall()

    return [Vibe(name=result[0], count=result[1]) for result in results]


def search_vibes(q):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT vibe, count(id) FROM relationships WHERE vibe LIKE ? GROUP BY vibe",
        (f"%{q}%",),
    ).fetchall()

    return [{"vibe": result[0], "count": result[1]} for result in results]


def search_unique_ids_for_vibe(vibe):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT * FROM relationships WHERE vibe LIKE ?",
        (f"%{vibe}%",),
    ).fetchall()

    ids = set()
    for result in results:
        ids.add((result[1], result[2]))
        ids.add((result[3], result[4]))

    return list(ids)


def get_all_vibes(app, limit=10):
    app.logger.error("Time before connecting")
    app.logger.error(datetime.utcnow())
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    app.logger.error("Time after connecting, before querying")
    app.logger.error(datetime.utcnow())
    results = cursor.execute(
        "SELECT * FROM relationships ORDER BY id desc LIMIT ?;", (limit,)
    ).fetchall()
    app.logger.error("Time after querying")
    app.logger.error(datetime.utcnow())

    return results


def find_connections_by_vibe(id, vibe):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT primary_obj, primary_type, secondary_obj, secondary_type FROM relationships WHERE (primary_obj = ? OR secondary_obj = ?) AND vibe = ?",
        (id, id, vibe),
    ).fetchall()

    connections = [
        (result[0], result[1]) if result[0] != id else (result[2], result[3])
        for result in results
    ]

    return connections


def get_cursor():
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()

    return cursor


def save_album(album):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO albums (source_id, artist, title, tracklist, image_url, year, genre) VAlUES (?, ?, ?, ?, ?, ?, ?);",
        (
            album.id,
            album.artist,
            album.title,
            json.dumps(album.tracklist),
            album.image_url,
            album.year,
            album.genre,
        ),
    )

    connection.commit()


def save_game(game):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO games (source_id, developers, title, rating, image_url, year, genres) VAlUES (?, ?, ?, ?, ?, ?, ?);",
        (
            game.id,
            game.developers,
            game.title,
            game.rating,
            game.image_url,
            game.year,
            game.genres,
        ),
    )

    connection.commit()


def save_book(book: Book):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO books (source_id, author, title, pages, image_url, year, genre, publisher, description) VAlUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
        (
            book.id,
            book.author,
            book.title,
            book.pages,
            book.image_url,
            book.year,
            book.genre,
            book.publisher,
            book.description,
        ),
    )

    connection.commit()


def save_movie(movie: Movie):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO movies (source_id, director, title, rating, image_url, year, genres, writer, runtime) VAlUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
        (
            movie.id,
            movie.director,
            movie.title,
            movie.rating,
            movie.image_url,
            movie.year,
            movie.genres,
            movie.writer,
            movie.runtime,
        ),
    )

    connection.commit()


def get_game(id):
    cursor = get_cursor()
    result = cursor.execute(
        "SELECT * FROM games WHERE source_id = ? LIMIT 1;", (id,)
    ).fetchall()

    if len(result) > 0:
        return Game.from_sqlite(result[0])
    else:
        return None


def get_album(id):
    cursor = get_cursor()
    result = cursor.execute(
        "SELECT * FROM albums WHERE source_id = ? LIMIT 1;", (id,)
    ).fetchall()

    if len(result) > 0:
        return Album.from_sqlite(result[0])
    else:
        return None


def get_book(id):
    cursor = get_cursor()
    result = cursor.execute(
        "SELECT * FROM books WHERE source_id = ? LIMIT 1;", (id,)
    ).fetchall()

    if len(result) > 0:
        return Book.from_sqlite(result[0])
    else:
        return None


def get_movie(id):
    cursor = get_cursor()
    result = cursor.execute(
        "SELECT * FROM movies WHERE source_id = ? LIMIT 1;", (id,)
    ).fetchall()

    if len(result) > 0:
        return Movie.from_sqlite(result[0])
    else:
        return None
