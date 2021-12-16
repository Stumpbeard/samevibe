import json
import os

from flask import Flask, render_template, request
import requests


USER_AGENT = "SameVibe/0.1 +https://samevi.be"
MUSIC_KEY = os.environ.get("DISCOGS_CONSUMER_KEY")
MUSIC_SECRET = os.environ.get("DISCOGS_CONSUMER_SECRET")


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("hello.html", key=MUSIC_KEY, secret=MUSIC_SECRET)


@app.route("/search")
def search():
    q = request.args.get("q")
    url = f"https://api.discogs.com/database/search?q={q}&key={MUSIC_KEY}&secret={MUSIC_SECRET}"
    headers = {
        "User-Agent": USER_AGENT,
    }
    response = requests.get(url, headers=headers).content
    results = json.loads(response).get("results")
    return render_template("search.html", search=q, results=results)
