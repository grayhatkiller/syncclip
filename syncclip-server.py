from flask import Flask, request, jsonify, render_template_string, abort
from flask_cors import CORS
import uuid
import sqlite3
import os
import zlib
import html

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'syncclip.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS clipboards
                      (token TEXT PRIMARY KEY, content BLOB, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        db.commit()

def compress_content(content):
    return zlib.compress(content.encode('utf-8'))

def decompress_content(compressed_content):
    return zlib.decompress(compressed_content).decode('utf-8')

@app.route('/token', methods=['GET'])
def get_token():
    token = str(uuid.uuid4())
    db = get_db()
    db.execute('INSERT INTO clipboards (token, content) VALUES (?, ?)', (token, compress_content("")))
    db.commit()
    return jsonify({"token": token}), 201

@app.route('/clipboard/<token>', methods=['POST'])
def update_clipboard(token):
    db = get_db()
    cursor = db.execute('SELECT * FROM clipboards WHERE token = ?', (token,))
    if cursor.fetchone() is None:
        return jsonify({"error": "Invalid token"}), 404
    
    content = request.get_data(as_text=True)  # Get raw data as text
    compressed_content = compress_content(content)
    
    db.execute('UPDATE clipboards SET content = ?, last_updated = CURRENT_TIMESTAMP WHERE token = ?', 
               (sqlite3.Binary(compressed_content), token))
    db.commit()

    # Remove old entries, keeping only the latest 10 across all tokens
    db.execute('''DELETE FROM clipboards WHERE token NOT IN 
                  (SELECT token FROM clipboards ORDER BY last_updated DESC LIMIT 10)''')
    db.commit()

    return jsonify({"message": "Clipboard updated"}), 200

@app.route('/clipboard/<token>', methods=['GET'])
def get_clipboard(token):
    db = get_db()
    cursor = db.execute('SELECT content FROM clipboards WHERE token = ?', (token,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "Invalid token"}), 404
    
    compressed_content = row['content']
    content = decompress_content(compressed_content)
    return jsonify({"content": content}), 200

@app.route('/display/<token>')
def display_clipboard(token):
    db = get_db()
    cursor = db.execute('SELECT content FROM clipboards WHERE token = ?', (token,))
    row = cursor.fetchone()
    if row is None:
        abort(404)
    compressed_content = row['content']
    content = decompress_content(compressed_content)
    
    # Escape the content to safely display it in HTML
    safe_content = html.escape(content)
    
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SyncClip Content</title>
        <meta http-equiv="refresh" content="5">
        <style>
            #clipboard-content {
                width: 100%;
                height: 400px;
                white-space: pre-wrap;
                word-wrap: break-word;
                overflow-y: auto;
                border: 1px solid #ccc;
                padding: 10px;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <h1>SyncClip Content</h1>
        <div id="clipboard-content">%s</div>
    </body>
    </html>
    ''' % safe_content

    return render_template_string(html_content)

# Initialize the database
init_db()

# We don't need the if __name__ == '__main__': block for Gunicorn
