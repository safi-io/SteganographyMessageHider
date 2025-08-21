from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
import mysql.connector
from functools import wraps

from helper import stego_encode, stego_decode

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.secret_key = 'your_secret_key_here'  # This is for debugging phase.

# === Database Connection ===
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hellosafi",
        database="steganographyFlaskProject"
    )
    print("Connection established successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")

mycursor = mydb.cursor()


# === Login Required Decorator ===
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login required", "error")
            return redirect(url_for('handle_login'))
        return f(*args, **kwargs)

    return decorated_function


# === Routes ===

@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/encode', methods=['GET', 'POST'])
@login_required
def handle_encode():
    if request.method == 'GET':
        return render_template('encode.html')

    image_file = request.files['image']
    message = request.form['message']

    filename = secure_filename(image_file.filename)
    base_name, ext = os.path.splitext(filename)

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = f"{base_name}_encoded{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    image_file.save(input_path)
    stego_encode(input_path, message, output_path)

    # Save history
    sql = "INSERT INTO history (user_id, original_filename, encoded_filename, message) VALUES (%s, %s, %s, %s)"
    val = (session['user_id'], filename, output_filename, message)
    mycursor.execute(sql, val)
    mydb.commit()

    return send_file(
        output_path,
        mimetype='image/png',
        as_attachment=True,
        download_name=output_filename
    )


@app.route('/decode', methods=['GET', 'POST'])
@login_required
def handle_decode():
    if request.method == 'GET':
        return render_template('decode.html')

    image_file = request.files['image']
    filename = os.path.splitext(image_file.filename)[0] + '.png'
    input_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, 'to_decode_' + filename))
    image_file.save(input_path)

    hidden_message = stego_decode(input_path)
    return jsonify({'message': hidden_message})


@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    mycursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = mycursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['email'] = user[1]
        flash("Login successful", "success")
        return redirect(url_for('home'))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('handle_login'))


@app.route('/register', methods=['GET', 'POST'])
def handle_register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for('handle_register'))

    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    mycursor.execute(sql, val)
    mydb.commit()

    flash("Registration successful. Please login.", "success")
    return redirect(url_for('handle_login'))


@app.route('/logout')
@login_required
def handle_logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('handle_login'))


@app.route('/history')
@login_required
def view_history():
    user_id = session['user_id']
    mycursor.execute("SELECT original_filename, encoded_filename, message FROM history WHERE user_id = %s", (user_id,))
    history_data = mycursor.fetchall()
    return render_template("history.html", history=history_data)


if __name__ == '__main__':
    app.run(debug=True)
