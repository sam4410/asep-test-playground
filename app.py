"""
Simple backend service exposing a /countries endpoint.
The endpoint returns a JSON array of country objects.
Each country object contains at least an `id` and a `name`.
"""

from flask import Flask, jsonify

app = Flask(__name__)

# In a real application this data would come from a database or external service.
# For the purpose of this task we define a static list.
COUNTRIES = [
    {"id": 1, "name": "United States"},
    {"id": 2, "name": "Canada"},
    {"id": 3, "name": "Mexico"},
    {"id": 4, "name": "United Kingdom"},
    {"id": 5, "name": "Germany"},
    {"id": 6, "name": "France"},
    {"id": 7, "name": "Japan"},
    {"id": 8, "name": "Australia"},
    {"id": 9, "name": "India"},
    {"id": 10, "name": "Brazil"},
]


@app.route("/countries", methods=["GET"])
def get_countries():
    """
    Return the list of countries as JSON.
    """
    return jsonify(COUNTRIES)


if __name__ == "__main__":
    # Run the Flask development server.
    # In production, a WSGI server like gunicorn would be used.
    app.run(host="0.0.0.0", port=5000, debug=True)