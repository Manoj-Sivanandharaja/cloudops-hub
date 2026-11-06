import os
import time
from datetime import datetime, timezone

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "5432")),
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "connect_timeout": 5,
    "row_factory": dict_row,
}

ALLOWED_STATUSES = {"pending", "in_progress", "completed"}


def get_db():
    return psycopg.connect(**DB_CONFIG)


def init_db():
    """Create the task table if it does not exist."""
    for attempt in range(10):
        try:
            with get_db() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        description TEXT NOT NULL DEFAULT '',
                        status VARCHAR(20) NOT NULL DEFAULT 'pending'
                            CHECK (
                                status IN (
                                    'pending',
                                    'in_progress',
                                    'completed'
                                )
                            ),
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                """)
            return
        except psycopg.OperationalError:
            if attempt == 9:
                raise
            time.sleep(2)


def task_json(task):
    return {
        **task,
        "created_at": task["created_at"].isoformat(),
        "updated_at": task["updated_at"].isoformat(),
    }


@app.get("/")
def home():
    return jsonify({
        "name": "CloudOps Hub API",
        "message": "Welcome to CloudOps Hub",
        "status": "running",
        "version": "1.0.0",
    })


@app.get("/api/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return jsonify({
            "status": "healthy",
            "service": "cloudops-hub-api",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    except psycopg.Error:
        app.logger.exception("Database health check failed")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
        }), 503


@app.get("/api/tasks")
def list_tasks():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return jsonify([task_json(row) for row in rows])


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "pending")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400
    if len(title.strip()) > 200:
        return jsonify({"error": "Title must be 200 characters or fewer"}), 400
    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400
    if not isinstance(status, str) or status not in ALLOWED_STATUSES:
        return jsonify({
            "error": "Status must be pending, in_progress, or completed"
        }), 400

    with get_db() as conn:
        task = conn.execute(
            """
            INSERT INTO tasks (title, description, status)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (title.strip(), description, status),
        ).fetchone()

    return jsonify(task_json(task)), 201

@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    with get_db() as conn:
        task = conn.execute(
            "SELECT * FROM tasks WHERE id = %s",
            (task_id,)
        ).fetchone()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task_json(task))

@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    allowed_fields = {"title", "description", "status"}
    if not data or not set(data).issubset(allowed_fields):
        return jsonify({"error": "Provide valid task fields to update"}), 400

    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM tasks WHERE id = %s", (task_id,)
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Task not found"}), 404

        title = data.get("title", existing["title"])
        description = data.get("description", existing["description"])
        status = data.get("status", existing["status"])

        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "A non-empty title is required"}), 400
        if len(title.strip()) > 200:
            return jsonify({"error": "Title must be 200 characters or fewer"}), 400
        if not isinstance(description, str):
            return jsonify({"error": "Description must be a string"}), 400
        if not isinstance(status, str) or status not in ALLOWED_STATUSES:
            return jsonify({
                "error": "Status must be pending, in_progress, or completed"
            }), 400

        task = conn.execute(
            """
            UPDATE tasks
            SET title = %s, description = %s, status = %s,
                updated_at = NOW()
            WHERE id = %s
            RETURNING *
            """,
            (title.strip(), description, status, task_id),
        ).fetchone()

    return jsonify(task_json(task))


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    with get_db() as conn:
        deleted = conn.execute(
            "DELETE FROM tasks WHERE id = %s RETURNING id",
            (task_id,),
        ).fetchone()

    if deleted is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task deleted successfully",
        "id": deleted["id"],
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
