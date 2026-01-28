from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            url TEXT,
            page INTEGER,
            position INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_ad', methods=['POST'])
def add_ad():
    url = request.form['url']
    image = request.files['image']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('SELECT MAX(page) FROM ads')
    page = c.fetchone()[0]
    page = 1 if page is None else page

    c.execute('SELECT COUNT(*) FROM ads WHERE page=?', (page,))
    count = c.fetchone()[0]

    if count >= 100:
        page += 1
        position = 0
    else:
        position = count

    filename = secure_filename(image.filename)
    filename = f"{page}_{position}_{filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path)

    c.execute(
        'INSERT INTO ads(image, url, page, position) VALUES (?, ?, ?, ?)',
        (path, url, page, position)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route('/get_ads/<int:page>')
def get_ads(page):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT image, url, position FROM ads WHERE page=?', (page,))
    ads = c.fetchall()
    conn.close()

    return jsonify(ads)

if __name__ == '__main__':
    app.run(debug=True)
