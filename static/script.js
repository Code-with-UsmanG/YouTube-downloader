// Wait until the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  const downloadForm = document.getElementById("downloadForm");
  const messageDiv = document.getElementById("message");

  downloadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get the URL from the input field
    const videoUrl = document.getElementById("videoUrl").value.trim();

    // Display a status message
    messageDiv.textContent = "Processing your request...";

    // Define the possible resolutions in order of preference
    const resolutions = ["1080p", "720p", "360p"];

    for (const resolution of resolutions) {
      try {
        // Send the URL and resolution to the Flask backend endpoint (/download)
        const response = await fetch("/download", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ url: videoUrl, resolution }),
        });

        const data = await response.json();

        if (data.success) {
          messageDiv.textContent = `Download initiated successfully at ${resolution}. Please check your Downloads folder.`;
          return;
        } else {
          console.log(`${resolution} failed, trying next resolution...`);
        }
      } catch (error) {
        console.error("Error:", error);
        messageDiv.textContent = "An error occurred while processing your request. Please try again.";
        return;
      }
    }

    // If none of the resolutions worked
    messageDiv.textContent = "Error: None of the requested resolutions are available.";
  });
});

// Dark Mode Toggle Function
function toggleTheme() {
  const body = document.body;
  body.classList.toggle("dark-mode");
  document.querySelector(".toggle-theme").textContent =
    body.classList.contains("dark-mode") ? "☀️" : "🌙";
}