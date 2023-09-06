# routes/routes.py

from flask import Blueprint, render_template, request
from controllers.search_controller import search_endpoint
from services.search_service import SearchService


search_bp = Blueprint('search', __name__)
# Define URL routes
search_bp.add_url_rule('/search/<query>', 'search', search_endpoint)


# @search_bp.route('/search', methods=['GET'])
# def search_page():
#     return render_template('search.html')
@search_bp.route('/search', methods=['GET'])
@search_bp.route('/search/', methods=['GET'])
def search_page():
    query = request.args.get('q', '')
    if(query):
        search_service = SearchService()
        search_results = search_service.search(query)  # Call your search function to get results
        return render_template('search.html', search_results=search_results)
    return render_template('search.html')