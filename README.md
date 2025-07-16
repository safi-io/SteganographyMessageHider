# 🕵️‍♂️ Steganography Message Hider

> 🎓 *CS50 Final Project – Image Steganography Tool*

**Steganography Message Hider** is a web-based steganography tool that allows you to hide and extract secret messages within images. With a clean and responsive user interface powered by HTML, CSS, and JavaScript, and a secure backend built in Python, Steganography makes message concealment simple, private, and elegant.

---

## ✨ Features

- 🔍 **Image-Based Steganography**: Encode messages within JPEG or PNG images.
- 📥 **Encoding and Decoding**: Seamlessly hide or retrieve messages from images.
- 🗃️ **User Authentication & Session Management**: Secure login and registration with isolated user sessions.
- 🛢️ **MySQL Database Integration**: All user accounts and history logs are stored in a structured and scalable relational database.
- 🧾 **Encoding/Decoding History**: Track and view past steganography actions per user.
- ⚙️ **Offline Capable**: Run locally without internet access or external APIs.
- 🎨 **Beautiful UI**: Responsive and elegant frontend built with HTML/CSS/JavaScript.
- 🔐 **Privacy-First**: Fully local processing with no external data transfers.
- 🧪 **Simple UX**: Just upload an image, type your message, and you're done!

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

### LSB Technique Explanation
The Least Significant Bit (LSB) technique is a simple but powerful method for hiding data in images. Every pixel in an image is made up of RGB values, each of these values is stored as an 8-bit binary number.
LSB works by modifying the last bit (the least significant one) of these binary values. Since the change in the last bit causes almost no visible difference in the image, it allows data to be hidden invisibly.

For example:
Original Red value = 11100110 (230)
After encoding = 11100111 (231) — The difference is visually unnoticeable, but now contains part of your message.

This is repeated across many pixels to embed the full message bit by bit.

---

## 🛠️ Tech Stack
| Layer           | Technology                   |
|------------------|------------------------------|
| Frontend         | HTML5, CSS3, JavaScript       |
| Backend          | Python 3, Flask (with Sessions) |
| Database         | MySQL (via Flask-MySQL or pymysql) |
| Authentication   | Flask-Login, Flask Sessions   |
| Image Processing | Pillow (PIL)                  |


---

## 🖼️ Interface Previews

### 🏠 Home Page
This is the page that welcomes you when you start the application(Steganography Studio).
![Home Page](screenshots/homepage.png)

### ✏️ Encoding Page
On this page, You can upload the picture, and write the text you want to hide in the image.
#### For Example
- Image: Pakistan Flag
- Text: Pakistan is my Country.
![Encoding Page](screenshots/encoding.png)

### 📖 Decoding Page
This page gives you the ability to decode the message by uploading the image.
#### Decoded Text:
- Pakistan is my Country.
![Decoding Page](screenshots/decoding.png)

### 🔑 Login Interface
This is the page where you can log in.
![Login Page](screenshots/login.png)

### 🆕 Registration Interface
This is the page where you can register.
![Registration Page](screenshots/register.png)

---

## 📦 Installation

### ⚙️ Prerequisites
- Python 3.8+
- pip

### 🔧 Steps
```bash
# Clone the repository
git clone https://github.com/safi-io/SteganographyMessageHider
cd SteganographyMessageHider

# Install dependencies
pip install flask pillow

# Install additional dependencies for MySQL support
pip install flask-mysqldb

# Run the app
python app.py

# Visit in your browser
http://127.0.0.1:5000
```
### Project Directory
``` bash
SteganographyMessageHider/
├── static/
│   ├── index.css
│   ├── encode.css
│   ├── decode.css
├── templates/
│   └── index.html
│   └── decode.html
│   └── encode.html
│   └── login.html
│   └── register.html
│   └── histoory.html
├── uploads/                   # Temporary image storage
├── app.py                     # Main Flask application
├── app.py                     # Encoding/decoding logic
├── ProjectDocumentation.pdf   # It was previously a basic semester project, now I enhanced it as my CS50 Project.
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
  You can run SteganographyMessageHider completely offline. Just install the dependencies, start the server, and use it locally.

- 🔐 **Local-Only Execution**  
  The backend server runs on your local machine, and the frontend interacts only with it, avoiding exposure to the internet.

> ✅ Your messages stay yours. SteganographyMessageHider ensures data confidentiality and local control.

## 📈 Future Enhancements

SteganographyMessageHider is a solid foundation for exploring steganography, and future versions can expand its capabilities even further:

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

---

## License

This project is intended solely for **educational purposes** and is not licensed for commercial use.

---

## Contact

For any queries, please feel free to reach out:

**Email:** [m.safi.ullah@outlook.com](mailto:m.safi.ullah@outlook.com)

---

Thank you for exploring!
