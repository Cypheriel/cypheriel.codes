import random

from flask import Flask, render_template, redirect, request, json, make_response

from embed import Embed

app = Flask(__name__)


def under_to_ws(s: str) -> str:
    return s.replace("\\_", "%%UNDER%%").replace("/_", "%%UNDER%%").replace("_", " ").replace("%%UNDER%%", "_")


@app.errorhandler(404)
def handle_404(_e):
    messages = [
        "What? Not the kind of code you were looking for?",
        "Oopsie.",
        "[insert funny text]",
        "TODO: don't",
        "Eventually you'll get there."
    ]

    embed = Embed(
        title="404 — Not Found",
        description=f"""The resources you tried to access was not found.\n\n"""
                    f"""* {random.choice(messages)}"""
    )

    return render_template("404.html", title="404 | Not Found - cypheriel.codes", embed=embed)


@app.route("/index.html")
def index_html():
    return redirect("/")


@app.route("/")
def index():
    embed = Embed(title="Welcome to cypheriel.codes!", description="An extremely empty Flask-powered website.")
    return render_template("index.html", title="Index - cypheriel.codes", embed=embed)


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
    response = make_response(json.dumps(dict(request.args.items())))
    response.content_type = "application/json"
    return response


@app.route("/oembed")
def oembed_generator():
    oembed = dict(("description" if k == "desc" else k, v for k, v in request.args.items()))

    embed = Embed(
        title=oembed.get("title", ""),
        description=oembed.get("description", ""),
        color=oembed.get("color", "2d4268")
    )

    query = '&'.join([f'{k}={v}' for k, v in oembed.items()])

    return render_template(
        "embed.html",
        link=f"https://cypheriel.codes/oembed.json?{query}",
        embed=embed
    )


@app.route("/ping_test")
def ping_test():
    return redirect("https://youtu.be/dQw4w9WgXcQ")


if __name__ == "__main__":
    app.run()
