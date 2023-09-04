# search_app.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.search import search_bp  # Import the Blueprint for routes
from routes.health import health_bp  # Import BP for health


app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

app = Flask(__name__, template_folder='views/templates')

# Register the search blueprint with the app for new routes
app.register_blueprint(search_bp, url_prefix='/')
app.register_blueprint(health_bp, url_prefix='/')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
