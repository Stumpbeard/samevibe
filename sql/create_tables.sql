CREATE TABLE IF NOT EXISTS relationships
(
    id INTEGER PRIMARY KEY,
    primary_obj TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_obj TEXT NOT NULL,
    secondary_type TEXT NOT NULL,
    vibe TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS albums
(
    id INTEGER PRIMARY KEY,
    source_id TEXT NOT NULL,
    artist TEXT,
    title TEXT,
    tracklist TEXT,
    image_url TEXT,
    year INTEGER,
    genre TEXT
);