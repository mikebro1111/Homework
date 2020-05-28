from flask import Flask
from geocreator import create_map

app = Flask(__name__)


@app.route("/")
def main():
    mp = create_map()
    return mp
