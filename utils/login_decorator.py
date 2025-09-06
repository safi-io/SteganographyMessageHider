from functools import wraps
from flask import redirect, url_for, flash, session


# === Login Required Decorator ===
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login required", "error")
            return redirect(url_for('login.handle_login'))
        return f(*args, **kwargs)

    return decorated_function
