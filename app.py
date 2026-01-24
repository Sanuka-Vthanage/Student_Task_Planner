import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/tasks")
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (data["title"], 0))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_db()
    conn.execute("UPDATE tasks SET completed = 1 - completed WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "updated"})

@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    conn = get_db()
    # Added 'completed' column to the table
    conn.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        completed INTEGER DEFAULT 0
      )
    """)
    conn.commit()
    conn.close()
    app.run(debug=True)