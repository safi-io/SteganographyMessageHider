from flask import Flask
import os
from utils.database import connect_db

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_ENV", "safidevelopedthis")

# Directories for Uploading and Storing Images
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# DB connection
mydb, mycursor = connect_db()

# Blueprints
from routes.main import main_bp
from routes.encode import encode_bp
from routes.decode import decode_bp
from routes.auth import login_bp
from routes.history import history_bp

app.register_blueprint(main_bp)
app.register_blueprint(encode_bp)
app.register_blueprint(decode_bp)
app.register_blueprint(login_bp)
app.register_blueprint(history_bp)

app.run(host="0.0.0.0", port=5000, debug=True)