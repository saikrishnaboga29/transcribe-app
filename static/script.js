document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    console.log("Form submission started.");

    var formData = new FormData();
    var file = document.getElementById('file').files[0];
    formData.append('file', file);
    console.log("File appended to FormData.");

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';
    document.getElementById('transcription').innerText = '';

    try {
        console.log("Sending POST request to /upload.");
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log("Response received from /upload.");

        const data = await response.json();
        console.log("Response JSON parsed:", data);
        if (data.error) {
            document.getElementById('transcription').innerText = data.error;
        } else {
            document.getElementById('transcription').innerText = data.transcription;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('transcription').innerText = 'An error occurred while processing the file.';
    } finally {
        // Hide loading indicator
        document.getElementById('loading').style.display = 'none';
        console.log("Form submission process ended.");
    }
});
