#!/usr/bin/env python
"""
Simple HTTP server to show a search field and browse results
"""

# We use a gunicorn custom application if we use gunicorn (more than one worker)
# See https://docs.gunicorn.org/en/stable/custom.html

import multiprocessing
import gunicorn.app.base
import argparse
from flask import Flask, jsonify


def default_nworkers():
    return (multiprocessing.cpu_count() * 2) + 1

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


class GunicornApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, host="127.0.0.1", port=8080, workers=default_nworkers(), debug=False):
        self.application = app
        self.debug = debug
        self.host = host
        self.port = port
        self.workers = workers
        super().__init__()

    def load_config(self):
        self.cfg.set("bind", f"{self.host}:{self.port}")
        self.cfg.set("workers", self.workers)
        self.cfg.set("print_config", True)
        print("Gunicorn config: ", self.cfg)

    def load(self):
        return self.application


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Elasticsearch search server")
    parser.add_argument("--es_host", type=str, default="localhost",
                        help="Elasticsearch host (localhost)")
    parser.add_argument("--es_port", type=int, default=9901,
                        help="Elasticsearch port (9901)")
    parser.add_argument("--host", type=str, default="localhost",
                        help="Address to bind to (localhost)")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to bind to (8080)")
    parser.add_argument("--es_cfg", type=str, default=None,
                        help="ES connection config, if specified -e/p ignored. YAML or TOML format")
    parser.add_argument("--index", type=str, required=True,
                        help="Index name (required)")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of workers, if 0 determine automatically (1)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")
    args = parser.parse_args()

    if args.workers == 0:
        workers = default_nworkers()
    elif args.workers > 0:
        workers = args.workers
    else:
        raise Exception("--workers must be 0 or greater")

    if workers == 1:
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        app.debug = args.debug
        print("App config:", app.config)
        gapp = GunicornApplication(app, host=args.host, port=args.port, debug=args.debug, workers=workers)
        gapp.debug = args.debug
        gapp.run()
