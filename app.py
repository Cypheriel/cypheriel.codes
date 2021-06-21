from flask import Flask, render_template, redirect, request, make_response

from embed import Embed

app = Flask(__name__)


def under_to_ws(s: str) -> str:
    return s.replace("\\_", "__UNDER__").replace("_", " ").replace("__UNDER__", "_")


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

    return render_template("embed.html", embed=embed)


@app.route("/ping_test")
def ping_test():
    return redirect("https://youtu.be/dQw4w9WgXcQ")


if __name__ == "__main__":
    app.run()
