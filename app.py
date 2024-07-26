from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

# Hard-coded directories for temporary storage
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['TRANSCRIPTION_FOLDER'] = '/tmp/transcriptions'

# Ensure the upload and transcription folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TRANSCRIPTION_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    transcription = transcribe_audio(file_path)
    transcription_filename = f"{os.path.splitext(filename)[0]}.txt"
    transcription_path = os.path.join(app.config['TRANSCRIPTION_FOLDER'], transcription_filename)

    with open(transcription_path, 'w') as f:
        f.write(transcription)

    # Clean up the uploaded file
    os.remove(file_path)

    return send_file(transcription_path, as_attachment=True, download_name=transcription_filename)

def transcribe_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path.replace(os.path.splitext(file_path)[1], '.wav')
    audio.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    # Clean up the intermediate WAV file
    os.remove(wav_path)

    return text

if __name__ == '__main__':
    app.run(debug=True)
