# routes/health.py

from flask import Blueprint, jsonify
from services.health_service import check_application_health


health_bp = Blueprint('health', __name__)


# routes/health.py


@health_bp.route('/health', methods=['GET'])
def health_check():
    health_status = check_application_health()
    return jsonify(health_status)


