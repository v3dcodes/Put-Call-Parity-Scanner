"""Put/Call Parity Scanner - Flask API.

Dev:  run this (port 5002) + `npm run dev` in ../frontend.
Prod: `npm run build` in ../frontend, then this serves it at /.
"""
import os
from flask import Flask, jsonify, send_from_directory

import marketdata
import parity

DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app = Flask(__name__, static_folder=None)


def _chain(spot):
    if os.environ.get("SCHWAB_TOKEN"):
        return marketdata.get_chain(spot=spot)
    return marketdata.synthetic_chain(spot=spot, mispricing=0.006)


@app.route("/api/parity")
def api_parity():
    spot = 5500.0
    return jsonify(parity.payload(_chain(spot), spot))


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    full = os.path.join(DIST, path)
    if path and os.path.exists(full):
        return send_from_directory(DIST, path)
    if os.path.exists(os.path.join(DIST, "index.html")):
        return send_from_directory(DIST, "index.html")
    return ("Frontend not built. Run `npm install && npm run dev` in ../frontend.", 200)


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5002)))
