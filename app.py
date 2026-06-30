from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/v1/prd-deploy-check', methods=['GET'])
def prd_deploy_check():
    """
    Health check endpoint for production deployment verification.
    Returns a simple JSON indicating the service is operational.
    """
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    # Run the Flask development server; in production, a WSGI server would be used.
    app.run(host='0.0.0.0', port=5000)
