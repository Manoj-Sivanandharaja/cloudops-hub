from datetime import datetime, timezone

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.get("/")
def home():
    return jsonify({
        "name": "CloudOps Hub API",
        "message": "Welcome to CloudOps Hub",
        "status": "running"
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "cloudops-hub-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
