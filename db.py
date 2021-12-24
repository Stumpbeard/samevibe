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
        "SELECT vibe, count(id) FROM relationships WHERE primary_obj = ? or secondary_obj = ? GROUP BY vibe ORDER BY count(id) desc",
        (id, id),
    ).fetchall()

    return results


def find_connections_by_vibe(id, vibe):
    connection = sqlite3.connect("samevibe.db")
    cursor = connection.cursor()
    results = cursor.execute(
        "SELECT primary_obj, secondary_obj FROM relationships WHERE primary_obj = ? OR secondary_obj = ? AND vibe = ?",
        (id, id, vibe),
    ).fetchall()

    connections = [result[0] if result[0] != id else result[1] for result in results]

    return connections
