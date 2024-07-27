from flask import Flask, request, render_template, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received file upload request.")
    if 'file' not in request.files:
        print("No file part in request.")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        print("No file selected for uploading.")
        return jsonify({"error": "No selected file"}), 400

    # Read the file in memory
    file_data = io.BytesIO(file.read())
    print(f"File {file.filename} read into memory.")
    transcription = transcribe_audio(file_data)

    return jsonify({"transcription": transcription})

def transcribe_audio(file_data):
    print("Starting transcription process.")
    try:
        # Convert the uploaded file to an audio segment
        audio = AudioSegment.from_file(file_data)
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)
        print("Audio file converted to WAV format.")

        # Use SpeechRecognition to transcribe the audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_data) as source:
            audio_data = recognizer.record(source)
            print("Audio data recorded for transcription.")
            text = recognizer.recognize_google(audio_data)
            print("Transcription completed successfully.")
        
        return text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
