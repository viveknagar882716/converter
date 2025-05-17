from flask import Flask, render_template, request
import os
from transformers import pipeline
from pydub import AudioSegment
import uuid

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Load the whisper pipeline
pipe = pipeline(model="openai/whisper-base")

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio_file" not in request.files:
        return "No file uploaded", 400

    audio_file = request.files["audio_file"]
    if audio_file.filename == "":
        return "No selected file", 400

    # Save file
    filename = str(uuid.uuid4()) + ".mp3"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    audio_file.save(filepath)

    # Transcribe using whisper
    try:
        result = pipe(filepath)
        transcript = result["text"]
    except Exception as e:
        transcript = f"Error during transcription: {str(e)}"

    return render_template("result.html", transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True)
