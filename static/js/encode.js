const imageUpload = document.getElementById("image-upload");
const fileNameDisplay = document.getElementById("file-name");
const messageInput = document.getElementById("message-input");
const encodeBtn = document.getElementById("encode-btn");
const messageBox = document.getElementById("message-box");
const encodedImageContainer = document.getElementById(
  "encoded-image-container"
);
const encodedImage = document.getElementById("encoded-image");
const imagePlaceholder = document.getElementById("image-placeholder");
const loadingIndicator = document.getElementById("loading-indicator");

let selectedFiles = [];

imageUpload.addEventListener("change", (event) => {
  selectedFiles = Array.from(event.target.files);
  if (selectedFiles.length > 0) {
    const fileNames = selectedFiles.map((f) => f.name).join(", ");
    fileNameDisplay.textContent = fileNames;
    showMessage(`${selectedFiles.length} image(s) selected.`, "success");
    imagePlaceholder.style.display = "block";
    encodedImageContainer.style.display = "none";
  } else {
    fileNameDisplay.textContent = "No file chosen";
    showMessage("No image selected.", "error");
  }
});

encodeBtn.addEventListener("click", async () => {
  const messageText = messageInput.value.trim();

  if (selectedFiles.length === 0) {
    showMessage("Please select at least one image to encode.", "error");
    return;
  }

  if (!messageText) {
    showMessage("Please enter a message to hide.", "error");
    return;
  }

  if (loadingIndicator) loadingIndicator.style.display = "block";
  if (encodedImageContainer) encodedImageContainer.style.display = "none";
  if (imagePlaceholder) imagePlaceholder.style.display = "none";
  showMessage("Encoding message...", "info");
  if (encodeBtn) encodeBtn.disabled = true;

  const formData = new FormData();
  selectedFiles.forEach((file) => {
    formData.append("image", file);
  });
  formData.append("message", messageText);

  try {
    // Step 1: enqueue tasks
    const response = await fetch("/encode", { method: "POST", body: formData });
    const { task_ids, output_files } = await response.json();

    // Step 2: poll every 2s until all are done
    const checkTasks = async () => {
      const results = await Promise.all(
        task_ids.map((id) => fetch(`/task-status/${id}`).then((r) => r.json()))
      );
      const allDone = results.every((r) => r.status === "SUCCESS");
      if (allDone) {
        // Step 3: request ZIP once all are complete
        const zipResp = await fetch("/download-zip", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ output_files }),
        });
        const blob = await zipResp.blob();
        const zipUrl = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = zipUrl;
        link.download = "encoded_images.zip";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

  showMessage("All images encoded and downloaded!", "success");
  if (loadingIndicator) loadingIndicator.style.display = "none";
  if (encodeBtn) encodeBtn.disabled = false;
      } else {
        setTimeout(checkTasks, 2000); // keep polling
      }
    };

    checkTasks();
  } catch (error) {
    console.error("Encoding error:", error);
    showMessage(
      "An error occurred during encoding. Please try again.",
      "error"
    );
  if (loadingIndicator) loadingIndicator.style.display = "none";
  if (encodeBtn) encodeBtn.disabled = false;
  }
});

function showMessage(message, type) {
  messageBox.textContent = message;
  messageBox.className = "message-box show";
  if (type) {
    messageBox.classList.add(type);
  }
  if (messageTimeout) {
    clearTimeout(messageTimeout);
  }
}

let messageTimeout;
