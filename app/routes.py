from flask import Blueprint, jsonify, request

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return jsonify({
        "message": "Flask OK",
        "project": "webhook_db demo"
    })

@main_bp.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })

@main_bp.route("/webhook/items", methods=["POST"])
def webhook_items():
    data = request.get_json(silent=True) or {}

    print("Webhook recibió:", data)

    return jsonify({
        "status": "ok",
        "received": data
    }), 200