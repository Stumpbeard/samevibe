from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    id: str
    artist: str
    title: str
    tracklist: List[dict]
    image_url: str
    year: int
    genre: str

    @classmethod
    def from_discogs(cls, results):
        return cls(
            id=results.get("id"),
            artist=results.get("artists", [None])[0].get("name"),
            title=results.get("title"),
            tracklist=results.get("tracklist", []),
            image_url=results.get("images", [None])[0].get("resource_url"),
            year=results.get("year"),
            genre=", ".join(results.get("styles")),
        )


@dataclass
class Movie:
    id: str
    director: str
    writer: str
    title: str
    year: int
    rating: str
    genres: str
    runtime: str
    image_url: str

    @classmethod
    def from_omdb(cls, result):
        return cls(
            id=result.get("imdbID"),
            director=result.get("Director"),
            writer=result.get("Writer"),
            title=result.get("Title"),
            year=result.get("Year"),
            rating=result.get("Rated"),
            genres=result.get("Genre"),
            runtime=result.get("Runtime"),
            image_url=result.get("Poster"),
        )


@dataclass
class Game:
    id: str
    title: str
    year: int
    genres: str
    developers: str
    rating: str
    image_url: str

    @classmethod
    def from_rawg(cls, result):
        resized_image = (result.get("background_image", "") or "").replace(
            "io/media/", "io/media/resize/420/-/"
        )
        return cls(
            id=result.get("id"),
            title=result.get("name"),
            year=result.get("released", "") or ""[:4],
            genres=", ".join([genre["name"] for genre in result.get("genres", [])]),
            developers=", ".join(
                [genre["name"] for genre in result.get("developers", [])]
            ),
            rating=(result.get("esrb_rating", {}) or {}).get("name"),
            image_url=resized_image,
        )


@dataclass
class Book:
    id: str
    title: str
    author: str
    publisher: str
    pages: int
    year: int
    description: str
    genre: str
    image_url: str

    @classmethod
    def from_google(cls, result):
        data = result.get("volumeInfo", {})
        return cls(
            id=result.get("id"),
            title=data.get("title"),
            author=", ".join(data.get("authors", [])),
            publisher=data.get("publisher"),
            pages=data.get("pageCount"),
            year=data.get("publishedDate", "")[:4],
            description=data.get("description"),
            genre=", ".join(data.get("categories", [])),
            image_url=data.get("imageLinks", {}).get("thumbnail"),
        )


@dataclass
class SearchResult:
    id: str
    creator: str
    title: str
    year: str
    genre: str
    image_url: str
    type: str

    @classmethod
    def from_discogs(cls, result):
        split_title = result.get("title", "").split(" - ")
        return cls(
            id=result.get("id"),
            creator=split_title[0],
            title=split_title[1],
            year=result.get("year"),
            genre=", ".join(result.get("style")),
            image_url=result.get("cover_image"),
            type="album",
        )

    @classmethod
    def from_omdb(cls, result):
        return cls(
            id=result.get("imdbID"),
            creator="",
            title=result.get("Title"),
            year=result.get("Year"),
            genre="",
            image_url=result.get("Poster"),
            type="movie",
        )

    @classmethod
    def from_googlebooks(cls, result):
        data = result.get("volumeInfo")
        return cls(
            id=result.get("id"),
            creator=", ".join(data.get("authors", [])),
            title=data.get("title"),
            year=data.get("publishedDate"),
            genre="",
            image_url=data.get("imageLinks", {}).get("thumbnail"),
            type="book",
        )

    @classmethod
    def from_rawg(cls, result):
        return cls(
            id=result.get("id"),
            creator="",
            title=result.get("name"),
            year=(result.get("released", "") or "?")[:4],
            genre=", ".join(
                [genre.get("name", "") for genre in result.get("genres", [])]
            ),
            image_url=result.get("background_image"),
            type="game",
        )

    @classmethod
    def from_serial(cls, data, type):
        if type == "movie":
            creator = data.director
        if type == "album":
            creator = data.artist
        if type == "book":
            creator = data.author
        if type == "game":
            creator = data.developers

        return cls(
            id=data.id,
            creator=creator,
            title=data.title,
            year=data.year,
            genre=data.genres if type in ["game", "movie"] else data.genre,
            image_url=data.image_url,
            type=type,
        )


@dataclass
class Vibe:
    name: str
    count: int
