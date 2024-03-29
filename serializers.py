from dataclasses import dataclass
import json
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
    type: str = "album"

    @classmethod
    def from_discogs(cls, results):
        return cls(
            id=results.get("id"),
            artist=results.get("artists", [{}])[0].get("name"),
            title=results.get("title"),
            tracklist=results.get("tracklist", []),
            image_url=results.get("images", [{}])[0]
            .get("resource_url", "")
            .replace("http://", "https://"),
            year=results.get("year"),
            genre=", ".join(results.get("styles")),
        )

    @classmethod
    def from_sqlite(cls, data):
        return cls(
            id=data[1],
            artist=data[2],
            title=data[3],
            tracklist=json.loads(data[4]),
            image_url=(data[5] or "").replace("http://", "https://"),
            year=data[6],
            genre=data[7],
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
    type: str = "movie"

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
            image_url=result.get("Poster", "").replace("http://", "https://"),
        )

    @classmethod
    def from_sqlite(cls, data):
        return cls(
            id=data[1],
            director=data[2],
            title=data[3],
            rating=data[4],
            image_url=(data[5] or "").replace("http://", "https://"),
            year=data[6],
            genres=data[7],
            writer=data[8],
            runtime=data[9],
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
    type: str = "game"

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
            image_url=resized_image.replace("http://", "https://"),
        )

    @classmethod
    def from_sqlite(cls, data):
        return cls(
            id=data[1],
            developers=data[2],
            title=data[3],
            rating=data[4],
            image_url=(data[5] or "").replace("http://", "https://"),
            year=data[6],
            genres=data[7],
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
    type: str = "book"

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
            image_url=data.get("imageLinks", {})
            .get("thumbnail", "")
            .replace("http://", "https://")
            .replace("&zoom=1", "")
            .replace("&edge=curl", ""),
        )

    @classmethod
    def from_sqlite(cls, data):
        return cls(
            id=data[1],
            author=data[2],
            title=data[3],
            pages=data[4],
            image_url=(data[5] or "")
            .replace("http://", "https://")
            .replace("&zoom=1", "")
            .replace("&edge=curl", ""),
            year=data[6],
            genre=data[7],
            publisher=data[8],
            description=data[9],
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
            image_url=result.get("cover_image", "").replace("http://", "https://"),
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
            image_url=result.get("Poster", "").replace("http://", "https://"),
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
            image_url=data.get("imageLinks", {})
            .get("thumbnail", "")
            .replace("http://", "https://")
            .replace("&zoom=1", "")
            .replace("&edge=curl", ""),
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
            image_url=(result.get("background_image", "") or "").replace(
                "http://", "https://"
            ),
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
            image_url=(data.image_url or "")
            .replace("http://", "https://")
            .replace("&zoom=1", "")
            .replace("&edge=curl", ""),
            type=type,
        )


@dataclass
class Vibe:
    name: str
    count: int


@dataclass
class Email:
    id: int
    email: str
    token: str
    verified: bool

    @classmethod
    def from_sqlite(cls, result):
        return cls(
            id=result[0],
            email=result[1],
            token=result[2],
            verified=result[3],
        )
