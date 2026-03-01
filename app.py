import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# Use PostgreSQL on Render (persistent), SQLite locally
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # Render Postgres uses postgres:// but psycopg2 expects postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

USE_POSTGRES = bool(DATABASE_URL)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.db")


def init_db():
    if USE_POSTGRES:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
          CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            completed INTEGER DEFAULT 0
          )
        """)
        conn.commit()
        cur.close()
        conn.close()
    else:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
          CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            completed INTEGER DEFAULT 0
          )
        """)
        conn.commit()
        conn.close()


def get_db():
    if USE_POSTGRES:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    else:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def get_cursor(conn):
    if USE_POSTGRES:
        import psycopg2.extras
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn.cursor()


def rows_to_list(cursor_or_rows):
    """Convert DB rows to list of dicts for both SQLite and Postgres."""
    if USE_POSTGRES:
        return list(cursor_or_rows)
    return [dict(r) for r in cursor_or_rows]


init_db()


@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")


@app.route("/tasks")
def get_tasks():
    conn = get_db()
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400
    title = data["title"].strip()
    conn = get_db()
    cur = get_cursor(conn)
    if USE_POSTGRES:
        cur.execute("INSERT INTO tasks (title, completed) VALUES (%s, 0)", (title,))
    else:
        cur.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (title, 0))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_db()
    cur = get_cursor(conn)
    sql = "UPDATE tasks SET completed = 1 - completed WHERE id = %s" if USE_POSTGRES else "UPDATE tasks SET completed = 1 - completed WHERE id = ?"
    cur.execute(sql, (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "updated"})


@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cur = get_cursor(conn)
    sql = "DELETE FROM tasks WHERE id = %s" if USE_POSTGRES else "DELETE FROM tasks WHERE id = ?"
    cur.execute(sql, (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
