import sqlite3


def init_db():
    with open("sql/create_tables.sql") as f:
        sql = f.read()
        connection = sqlite3.connect("samevibe.db")
        cursor = connection.cursor()
        cursor.executescript(sql)


def create_vibe_connection(id, related_id, vibe):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO relationships (primary_obj, primary_type, secondary_obj, secondary_type, vibe) VALUES (?, 'album', ?, 'album', ?);",
        (id, related_id, vibe),
    )
    connection.commit()


def drop_tables():
    with open("sql/drop_tables.sql") as f:
        sql = f.read()
        connection = sqlite3.connect("samevibe.db")
        cursor = connection.cursor()
        cursor.executescript(sql)


def find_vibes(id):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT vibe, count(id) FROM relationships WHERE primary_obj = ? GROUP BY vibe ORDER BY count(id) desc",
        (id,),
    ).fetchall()

    return results


def find_connections_by_vibe(id, vibe):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT secondary_obj FROM relationships WHERE primary_obj = ? AND vibe = ?",
        (id, vibe),
    ).fetchall()

    return [result[0] for result in results]
