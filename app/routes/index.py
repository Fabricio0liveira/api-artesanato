from flask import Blueprint, jsonify

bp = Blueprint('health_check', __name__)

@bp.get('/health')
def health_check():
    return jsonify({"status": "UP"}), 200