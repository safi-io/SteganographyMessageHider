from flask import Blueprint, request, render_template, jsonify
import os
from utils.helper import stego_decode
from utils.login_decorator import login_required

UPLOAD_FOLDER = 'uploads'

decode_bp = Blueprint('decode', __name__)

@decode_bp.route('/decode', methods=['GET', 'POST'])
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
