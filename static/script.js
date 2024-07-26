document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    var file = document.getElementById('file').files[0];
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
        if (data.error) {
            document.getElementById('transcription').innerText = data.error;
        } else {
            document.getElementById('transcription').innerText = data.transcription;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('transcription').innerText = 'An error occurred while processing the file.';
    });
});
