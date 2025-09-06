from flask import Blueprint, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from utils.tasks import encode_image_task
from utils.login_decorator import login_required

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

encode_bp = Blueprint('encode', __name__)

@encode_bp.route('/encode', methods=['GET', 'POST'])
@login_required
def handle_encode():
    if request.method == 'GET':
        return render_template('encode.html')

    image_files = request.files.getlist('image')
    message = request.form['message']

    task_ids = []
    output_files = []

    for image_file in image_files:
        filename = secure_filename(image_file.filename)
        base_name, ext = os.path.splitext(filename)

        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = f"{base_name}_encoded{ext}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        image_file.save(input_path)

        task = encode_image_task.delay(input_path, message, output_path)
        task_ids.append(task.id)
        output_files.append(output_filename)

    return jsonify({"task_ids": task_ids, "output_files": output_files})

@encode_bp.route('/task-status/<task_id>')
@login_required
def task_status(task_id):
    task = encode_image_task.AsyncResult(task_id)
    return jsonify({"task_id": task_id, "status": task.status})

@encode_bp.route('/download-zip', methods=['POST'])
@login_required
def download_zip():
    output_files = request.json.get("output_files", [])
    zip_filename = "encoded_images.zip"
    zip_path = os.path.join(OUTPUT_FOLDER, zip_filename)

    import zipfile
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for fname in output_files:
            fpath = os.path.join(OUTPUT_FOLDER, fname)
            if os.path.exists(fpath):
                zipf.write(fpath, fname)

    from flask import send_file
    return send_file(
        zip_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name=zip_filename
    )
