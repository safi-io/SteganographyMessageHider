from flask import Blueprint, render_template
from utils.login_decorator import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    return render_template('index.html')
