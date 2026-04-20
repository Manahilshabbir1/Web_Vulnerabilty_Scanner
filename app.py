from flask import Flask, render_template, request
from scanner import scan_website
from db import init_db, save_scan

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    url = request.form["url"]

    results = scan_website(url)

    save_scan(url, results)

    return render_template("index.html", url=url, results=results)

if __name__ == "__main__":
    app.run(debug=True)
