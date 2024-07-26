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
        console.log(response)
        response.text()})
    .then(data => {
        console.log(data)
        document.getElementById('transcription').innerText = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
