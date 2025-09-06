// Generate random particles for the background
const particlesContainer = document.querySelector(".particles");
const numParticles = 30; // Adjust number of particles

for (let i = 0; i < numParticles; i++) {
  const particle = document.createElement("div");
  particle.classList.add("particle");
  // Random positions
  particle.style.left = Math.random() * 100 + "vw";
  particle.style.top = Math.random() * 100 + "vh";
  // Random size variation
  const size = Math.random() * 4 + 2; // Size between 2px and 6px
  particle.style.width = size + "px";
  particle.style.height = size + "px";
  // Random animation delay and duration
  particle.style.animationDelay = Math.random() * 5 + "s";
  particle.style.animationDuration = Math.random() * 8 + 6 + "s"; // Duration between 6s and 14s
  particlesContainer.appendChild(particle);
}

// Get DOM elements
const imageUpload = document.getElementById("image-upload");
const fileNameDisplay = document.getElementById("file-name");
const decodeBtn = document.getElementById("decode-btn");
const messageBox = document.getElementById("message-box");
const decodedMessageOutput = document.getElementById("decoded-message-output");
const decodedTextPlaceholder = document.getElementById(
  "decoded-text-placeholder"
);
const loadingIndicator = document.getElementById("loading-indicator");

let selectedFile = null; // To store the selected image file

// Event listener for image file selection
imageUpload.addEventListener("change", (event) => {
  selectedFile = event.target.files[0];
  if (selectedFile) {
    fileNameDisplay.textContent = selectedFile.name;
    showMessage(`Image selected: ${selectedFile.name}`, "success");
    // Reset decoded message display
    decodedMessageOutput.style.display = "flex"; // Ensure it's flex for centering content
    decodedTextPlaceholder.style.display = "block"; // Show placeholder
    decodedTextPlaceholder.innerHTML =
      "Upload an encoded image and click decode to reveal the hidden message.";
    decodedMessageOutput.innerHTML = ""; // Clear previous message
    decodedMessageOutput.appendChild(decodedTextPlaceholder); // Re-add placeholder
  } else {
    fileNameDisplay.textContent = "No file chosen";
    showMessage("No image selected.", "error");
  }
});

// Event listener for the Decode button
decodeBtn.addEventListener("click", async (e) => {
  e.preventDefault(); // Prevent default form submission

  if (!selectedFile) {
    showMessage("Please select an image to decode.", "error");
    return;
  }

  // Show loading indicator and hide previous results/messages
  loadingIndicator.style.display = "block";
  decodedTextPlaceholder.style.display = "none"; // Hide placeholder during loading
  decodedMessageOutput.innerHTML = ""; // Clear previous message content
  decodedMessageOutput.appendChild(loadingIndicator); // Add loading indicator to the output area
  showMessage("Decoding message...", "info");
  decodeBtn.disabled = true; // Disable button during processing

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    // In a real application, you would fetch from your backend /decode endpoint
    const response = await fetch("/decode", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.message && data.message.trim() !== "") {
      decodedTextPlaceholder.style.display = "block"; // Show placeholder to put the message in
      decodedTextPlaceholder.innerHTML = `${data.message}`;
      decodedMessageOutput.innerHTML = ""; // Clear the loading indicator
      decodedMessageOutput.appendChild(decodedTextPlaceholder); // Add the message
      showMessage("Message decoded successfully!", "success");
    } else {
      decodedTextPlaceholder.style.display = "block";
      decodedTextPlaceholder.innerHTML =
        "No hidden message found in the image.";
      decodedMessageOutput.innerHTML = "";
      decodedMessageOutput.appendChild(decodedTextPlaceholder);
      showMessage("No hidden message found in the image.", "error");
    }
  } catch (error) {
    console.error("Decoding error:", error);
    decodedTextPlaceholder.style.display = "block";
    decodedTextPlaceholder.innerHTML =
      "An error occurred during decoding. Please try again.";
    decodedMessageOutput.innerHTML = "";
    decodedMessageOutput.appendChild(decodedTextPlaceholder);
    showMessage(
      "An error occurred during decoding. Please try again.",
      "error"
    );
  } finally {
    loadingIndicator.style.display = "none"; // Ensure loading indicator is hidden
    decodeBtn.disabled = false; // Re-enable the button
  }
});

/**
 * Displays a message in the message box.
 * @param {string} message The message to display.
 * @param {'success' | 'error' | 'info'} type The type of message (for styling).
 */
function showMessage(message, type) {
  messageBox.textContent = message;
  messageBox.className = "message-box show"; // Reset classes
  if (type) {
    messageBox.classList.add(type);
  }
  // Optional: Hide message after a few seconds
  if (messageTimeout) {
    clearTimeout(messageTimeout);
  }
  messageTimeout = setTimeout(() => {
    messageBox.classList.remove("show");
  }, 5000); // Hide after 5 seconds
}
let messageTimeout; // To store the timeout for message hiding
