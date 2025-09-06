from flask import Blueprint, render_template, session
from utils.login_decorator import login_required
from utils.database import mycursor

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
@login_required
def view_history():
    user_id = session['user_id']
    mycursor.execute("SELECT original_filename, encoded_filename, message FROM history WHERE user_id = %s", (user_id,))
    history_data = mycursor.fetchall()
    return render_template("history.html", history=history_data)
