# 🕵️‍♂️ Steganography Message Hider

> 🎓 *4th Semester Information Security Project – Image Steganography Tool*

**Steganography Message Hider** is a web-based steganography tool that allows you to hide and extract secret messages within images. With a clean and responsive user interface powered by HTML, CSS, and JavaScript, and a secure backend built in Python, Steganography makes message concealment simple, private, and elegant.

---

## ✨ Features

- 🔍 **Image-Based Steganography**: Encode messages within JPEG or PNG images.
- 📥 **Encoding and Decoding**: Seamlessly hide or retrieve messages from images.
- 🎨 **Beautiful UI**: Responsive and elegant frontend built with HTML/CSS/JavaScript.
- 🔐 **Privacy-First**: Fully local processing with no external data transfers.
- 🧪 **Simple UX**: Just upload an image, type your message, and you're done!
- ⚙️ **Offline Capable**: Run locally without internet access or external APIs.

---

📷 Upload → 🔒 Encode → 📤 Download → 🧾 Decode → 📖 Read

---

## 📷 How It Works

### 🧬 Encoding
1. Upload a carrier image.
2. Enter the message you want to hide.
3. The Python backend embeds the message using **Least Significant Bit (LSB)** technique.
4. Download the new stego-image.

### 🔍 Decoding
1. Upload a previously encoded image.
2. Backend extracts and returns the hidden message.

---

## 🛠️ Tech Stack

| Layer     | Technology             |
|-----------|------------------------|
| Frontend  | HTML5, CSS3, JavaScript |
| Backend   | Python 3, Flask        |
| Image Processing | Pillow (PIL)   |

---

## 📦 Installation

### ⚙️ Prerequisites
- Python 3.8+
- pip

### 🔧 Steps
```bash
# Clone the repository
git clone https://github.com/safi-io/SteganographyMessageHider
cd steganrory

# Install dependencies
pip install flask pillow

# Run the app
python app.py

# Visit in your browser
http://127.0.0.1:5000
```
### Project Directory
``` bash
steganrory/
├── static/
│   ├── index.css
│   ├── encode.css
│   ├── decode.css
├── templates/
│   └── index.html
│   └── decode.html
│   └── encode.html
├── uploads/             # Temporary image storage
├── app.py               # Main Flask application & Encoding/decoding logic
├── README.md
```
## 🔐 Security

Steganography is built with privacy and security at its core. Here's how your data stays safe:

- 🔒 **No External Data Transfers**  
  All image and message processing is done locally on your machine. Nothing is sent to third-party servers or cloud storage.

- 🗂️ **Temporary File Handling**  
  Uploaded files are stored temporarily and removed automatically after encoding or decoding is complete.

- 🚫 **No Analytics or Tracking**  
  The application does not include cookies, trackers, or analytics scripts, ensuring a clean and private experience.

- 💾 **Offline-Ready**  
  You can run Steganrory completely offline. Just install the dependencies, start the server, and use it locally.

- 🔐 **Local-Only Execution**  
  The backend server runs on your local machine, and the frontend interacts only with it, avoiding exposure to the internet.

> ✅ Your messages stay yours. Steganrory ensures data confidentiality and local control.

## 📈 Future Enhancements

Steganrory is a solid foundation for exploring steganography, and future versions can expand its capabilities even further:

- 🔑 **Password-Protected Encoding**  
  Allow users to encrypt their hidden message with a password before embedding it into the image.

- 📱 **Mobile Optimization**  
  Enhance the frontend UI for better usability on smartphones and tablets.

- 🖼️ **Drag-and-Drop File Upload**  
  Improve UX by enabling users to drag and drop images directly into the browser.

- 🔁 **Batch Processing Support**  
  Enable users to encode or decode multiple images in one go.

- 🧠 **AI-Powered Steganalysis Detection**  
  Integrate tools to detect steganography in images for forensic or research purposes.

- 💬 **Multilingual Support**  
  Localize the interface to support multiple languages for broader accessibility.

- 📤 **Export Options**  
  Provide downloadable logs or embed reports detailing message length, encoding method, and more.

> 💡 Contributions are welcome! If you have ideas or want to work on any of these features, feel free to open an issue or pull request.


