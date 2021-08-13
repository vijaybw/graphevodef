from flask import Flask
from config import Config
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from graph.schema import graph
    from main.main import main

    app.register_blueprint(graph)
    app.register_blueprint(main)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    return app
