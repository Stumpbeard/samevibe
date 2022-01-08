CREATE TABLE IF NOT EXISTS relationships
(
    id INTEGER PRIMARY KEY,
    primary_obj TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_obj TEXT NOT NULL,
    secondary_type TEXT NOT NULL,
    vibe TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS emails
(
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    token TEXT NOT NULl,
    verified INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS subscriptions
(
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    type_id TEXT NOT NULL,
    email_id INTEGER NOT NULL,
    subscribed INTEGER
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

CREATE TABLE IF NOT EXISTS games
(
    id INTEGER PRIMARY KEY,
    source_id TEXT NOT NULL,
    developers TEXT,
    title TEXT,
    rating TEXT,
    image_url TEXT,
    year TEXT,
    genres TEXT
);

CREATE TABLE IF NOT EXISTS books
(
    id INTEGER PRIMARY KEY,
    source_id TEXT NOT NULL,
    author TEXT,
    title TEXT,
    pages INTEGER,
    image_url TEXT,
    year INTEGER,
    genre TEXT,
    publisher TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS movies
(
    id INTEGER PRIMARY KEY,
    source_id TEXT NOT NULL,
    director TEXT,
    title TEXT,
    rating INTEGER,
    image_url TEXT,
    year INTEGER,
    genres TEXT,
    writer TEXT,
    runtime TEXT
);

PRAGMA journal_mode=WAL;
