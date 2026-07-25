from flask import Blueprint, request, jsonify
from database import get_db_connection
from utils.helpers import generate_token, is_valid_url

routes = Blueprint("routes", __name__)

@routes.route("/generate", methods=["POST"])
def generate_link():

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    destination_url = data["url"]

    if not is_valid_url(destination_url):
        return jsonify({"error": "Invalid URL"}), 400

    token = generate_token()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO links(token, destination_url)
        VALUES(?,?)
    """, (token, destination_url))

    conn.commit()
    conn.close()

    tracking_link = f"http://127.0.0.1:5000/t/{token}"

    return jsonify({
        "message": "Tracking link created successfully",
        "tracking_link": tracking_link,
        "token": token
    })