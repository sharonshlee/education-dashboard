"""
Educational Dashboard Web Application using Flask
"""
import os
from flask import Flask, send_from_directory

from backend.db.models import db
from backend.api import api


app = Flask(__name__)

app.app_context()

app.config.from_object('backend.config.DevelopmentConfig')

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)


if __name__ == "__main__":
    app.run(port=int(os.getenv('PORT', 5002)), 
            host=os.getenv('HOST', '0.0.0.0'), 
            debug=not bool(os.getenv('PRODUCTION', False)))
