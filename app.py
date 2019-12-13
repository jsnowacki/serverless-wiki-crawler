from flask import Flask, request, jsonify
from wiki import parse_main

app = Flask(__name__)


@app.route("/crawl", methods=['POST'])
def crawl():
    lang = request.json['lang']

    res = parse_main(lang)
    if res is None:
        res = {"message": f"Error! Unsupported language {lang}"}

    return jsonify(res)


@app.route("/")
def healthcheck():
    return "OK"
