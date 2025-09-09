import os
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aski")
def aski():
    return render_template("aski.html")

@app.route("/emergency")
def Emergency():
    return render_template("Emergency.html")
@app.route("/nezam")
def nezam():
    return render_template("nezam.html")
@app.route("/learn")
def learn():
    return render_template("learn.html")
@app.route("/tarh")
def tarh():
    return render_template("tarh.html")
@app.route("/vam")
def vam():
    return render_template("vam.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

