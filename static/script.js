document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    var formData = new FormData();
    var file = document.getElementById('file').files[0];
    formData.append('file', file);

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';
    document.getElementById('transcription').innerText = '';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
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
    }
});
