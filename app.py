import random
from httpx import Client

from flask import Flask, render_template, redirect, request, json, make_response

from embed import Embed, OEmbed

app = Flask(__name__)
client = Client()

def under_to_ws(s: str) -> str:
    return s.replace("\\_", "%%UNDER%%").replace("/_", "%%UNDER%%").replace("_", " ").replace("%%UNDER%%", "_")


@app.errorhandler(404)
def handle_404(_e):
    messages = [
        "What? Not the kind of code you were looking for?",
        "Oopsie.",
        "[insert funny text]",
        "TODO: don't",
        "Eventually you'll get there.",
        "The mouse did it!",
        "Loading... NOT!",
        "You could've stopped it."
    ]

    oembed = OEmbed()
    oembed.title = "404 — Not Found"
    oembed.description = f"The resource you tried to access was not found.\n\n* {random.choice(messages)}"
    oembed.provider_name = "cypheriel.codes"
    oembed.provider_url = "https://cpyheriel.codes/"

    return render_template("404.html", title="404 | Not Found - cypheriel.codes", **oembed.render())


@app.route("/index.html")
def index_html():
    return redirect("/")


@app.route("/")
def index():
    oembed = OEmbed()
    oembed.title = "Welcome to cypheriel.codes!"
    oembed.description = "A fairly empty Flask-powered website by Cypheriel."
    oembed.provider_name = "cypheriel.codes"
    oembed.provider_url = "https://cpyheriel.codes/"

    return render_template("index.html", title="Index - cypheriel.codes", **oembed.render())


@app.route("/embed")
def embed_generator():
    args = request.args
    embed = Embed()
    for k, v in args.items():
        if k == "desc":
            k = "description"
        embed.__setattr__(under_to_ws(k), under_to_ws(v))

    return render_template("embed.html", embed=embed, debug=json.dumps(embed.__dict__, indent=4))


@app.route("/oembed.json")
def oembed_json():
    response = make_response(json.dumps(dict(request.args.items()), indent=4))
    response.content_type = "application/json"
    return response


@app.route("/paste")
def paste():
    response = make_response()

    link = request.args.get("link")
    if not link:
        response.status_code = 501
        return response

    res = client.get(link)

    oembed = OEmbed()
    oembed.title = "Paste Front-end — cypheriel.codes"
    oembed.description = "Paste front-end viewer."

    response.data = render_template("paste.html", paste=res.text, **oembed.render())
    return response


@app.route("/login")
def login():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


if __name__ == "__main__":
    app.run()
