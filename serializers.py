from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    id: str
    artist: str
    title: str
    tracklist: List[dict]
    image_url: str

    @classmethod
    def from_discogs(cls, results):
        return cls(
            id=results.get("id"),
            artist=results.get("artists", [None])[0].get("name"),
            title=results.get("title"),
            tracklist=results.get("tracklist", []),
            image_url=results.get("images", [None])[0].get("resource_url"),
        )


@dataclass
class Movie:
    id: str
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
    image_url: str

    @classmethod
    def from_rawg(cls, result):
        resized_image = result.get("background_image", "").replace(
            "io/media/", "io/media/resize/420/-/"
        )
        return cls(
            id=result.get("id"),
            title=result.get("name"),
            year=result.get("released", "")[:4],
            genres=", ".join([genre["name"] for genre in result.get("genres", [])]),
            image_url=resized_image,
        )
