import os
import sqlite3
import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                media TEXT,
                timestamp TEXT
            )
        ''')

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/comment")
def comment():
    return render_template("index.html")



@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/comments", methods=["GET"])
def get_comments():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT content, media, timestamp FROM comments ORDER BY id DESC")
        rows = c.fetchall()
        comments = [{"content": r[0], "media": r[1], "timestamp": r[2]} for r in rows]
    return jsonify(comments)

@app.route("/comment", methods=["POST"])
def post_comment():
    content = request.form.get("content")
    file = request.files.get("file")
    filename = None

    if file:
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO comments (content, media, timestamp) VALUES (?, ?, ?)", (content, filename, timestamp))
        conn.commit()

    return jsonify({"status": "success"})

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5300, debug=True)

