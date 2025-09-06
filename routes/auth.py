from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from utils.database import mycursor, mydb

login_bp = Blueprint("login", __name__)

# === LOGIN ===
@login_bp.route("/login", methods=["GET", "POST"])
def handle_login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    mycursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s",
        (email, password)
    )
    user = mycursor.fetchone()

    if user:
        session["user_id"] = user[0]
        session["email"] = user[2]
        flash("Login successful.", "success")
        return redirect(url_for("main.home"))
    else:
        flash("Invalid email or password.", "error")
        return redirect(url_for("login.handle_login"))


# === REGISTER ===
@login_bp.route("/register", methods=["GET", "POST"])
def handle_register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for("login.handle_register"))

    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    mycursor.execute(sql, val)
    mydb.commit()

    flash("Registration successful. Please login.", "success")
    return redirect(url_for("login.handle_login"))


# === LOGOUT ===
@login_bp.route("/logout")
def handle_logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login.handle_login"))
