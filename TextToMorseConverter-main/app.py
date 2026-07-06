from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
from flask_bcrypt import Bcrypt

from utils.encrypt import encyptToMorse
from utils.decrypt import decryptFromMorse

app = Flask(__name__)

app.secret_key = "supersecretkey"

bcrypt = Bcrypt(app)


# DATABASE SETUP
def init_db():

    conn = sqlite3.connect("morse_app.db")

    cursor = conn.cursor()

    # History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            original_text TEXT NOT NULL,
            result_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()


# SAVE HISTORY
def save_history(operation, original, result):

    conn = sqlite3.connect("morse_app.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (
            operation,
            original_text,
            result_text,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        operation,
        original,
        result,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()


# HOME PAGE
@app.route('/')
def index():

    return render_template('index.html')


# ABOUT PAGE
@app.route('/about')
def about():

    return render_template('about.html')


# ENCRYPT
@app.route('/encrypt', methods=['POST'])
def encrypt():

    if 'user' not in session:

        return redirect('/login')

    input_text = request.form.get('inputdata')

    if not input_text:

        return redirect('/')

    encrypted_text = encyptToMorse(input_text)

    save_history(
        "Encrypted",
        input_text,
        encrypted_text
    )

    data = {
        "operation": "Encrypted",
        "original": input_text,
        "result": encrypted_text
    }

    return render_template(
        'result.html',
        data=data
    )


# DECRYPT
@app.route('/decrypt', methods=['POST'])
def decrypt():

    if 'user' not in session:

        return redirect('/login')

    input_text = request.form.get('inputdata')

    if not input_text:

        return redirect('/')

    decrypted_text = decryptFromMorse(input_text)

    save_history(
        "Decrypted",
        input_text,
        decrypted_text
    )

    data = {
        "operation": "Decrypted",
        "original": input_text,
        "result": decrypted_text
    }

    return render_template(
        'result.html',
        data=data
    )


# HISTORY PAGE
@app.route('/history')
def history():

    if 'user' not in session:

        return redirect('/login')

    conn = sqlite3.connect("morse_app.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history ORDER BY id DESC"
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        'history.html',
        records=records
    )


# SIGNUP PAGE
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form.get('username')

        email = request.form.get('email')

        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

        conn = sqlite3.connect("morse_app.db")

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (
                username,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            username,
            email,
            hashed_password
        ))

        conn.commit()

        conn.close()

        return redirect('/login')

    return render_template('signup.html')


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')

        password = request.form.get('password')

        conn = sqlite3.connect("morse_app.db")

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(
            user[3],
            password
        ):

            session['user'] = user[1]

            return redirect('/')

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')


# RUN APP
if __name__ == '__main__':

    init_db()

    app.run(debug=True)
    # Test update
    