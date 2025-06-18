from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Steganography Logic ===

def stego_encode(image_path, message, output_path):
    img = Image.open(image_path)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # Null terminator
    binary_message = ''.join([format(ord(c), '08b') for c in message])
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx >= len(binary_message):
                break

            r, g, b = img.getpixel((x, y))

            if idx + 3 <= len(binary_message):
                r = (r & ~1) | int(binary_message[idx])
                g = (g & ~1) | int(binary_message[idx + 1])
                b = (b & ~1) | int(binary_message[idx + 2])
                idx += 3
            else:
                if idx < len(binary_message):
                    r = (r & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < len(binary_message):
                    g = (g & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < len(binary_message):
                    b = (b & ~1) | int(binary_message[idx])
                    idx += 1

            encoded.putpixel((x, y), (r, g, b))

    encoded.save(output_path, format='PNG')  # Always save as PNG

def stego_decode(image_path):
    img = Image.open(image_path)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    width, height = img.size
    binary_data = ''

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == chr(0):  # Null terminator
            break
        chars.append(char)

    return ''.join(chars)

# === Routes ===

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['GET'])
def encode_page():
    return render_template('encode.html')

@app.route('/encode', methods=['POST'])
def handle_encode():
    image_file = request.files['image']
    message = request.form['message']

    # Ensure filename is safe
    filename = secure_filename(image_file.filename)
    base_name, ext = os.path.splitext(filename)

    # Set input and output paths
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = f"{base_name}_encoded{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Save original image
    image_file.save(input_path)

    # Perform encoding
    stego_encode(input_path, message, output_path)

    # Send the encoded file with correct download name
    return send_file(
        output_path,
        mimetype='image/png',  # You may want to detect original type
        as_attachment=True,
        download_name=output_filename  # <-- this sets the correct name
    )

@app.route('/decode', methods=['GET'])
def decode_page():
    return render_template('decode.html')

@app.route('/decode', methods=['POST'])
def handle_decode():
    image_file = request.files['image']
    filename = os.path.splitext(image_file.filename)[0] + '.png'
    input_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, 'to_decode_' + filename))
    image_file.save(input_path)

    hidden_message = stego_decode(input_path)
    return jsonify({'message': hidden_message})

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True)
