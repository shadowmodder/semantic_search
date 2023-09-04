# controllers/search_controller.py

from flask import request, jsonify
from services.search_service import SearchService

search_service = SearchService()

def search_endpoint(query=None):
    print('query----> ')
    print(query)
    if query is None:
        query = request.args.get('q', '')  # Get user query from query parameter
    search_results = search_service.search(query)
    return jsonify(search_results)
