from flask import Flask
from . import helpers, routes

def create_app():
    app = Flask(__name__)
    routes.init_routes(app)
    return app

def run_server():
    ip = helpers.get_local_ip()
    app = create_app()
    print(f"Server started → http://{ip}:5000/")
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)
