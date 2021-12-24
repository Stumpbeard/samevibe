CREATE TABLE IF NOT EXISTS relationships
(
    id INTEGER PRIMARY KEY,
    primary_obj TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_obj TEXT NOT NULL,
    secondary_type TEXT NOT NULL,
    vibe TEXT NOT NULL
);