import os
import numpy as np
import mysql.connector

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model

from feature_extraction import extract_mfcc
from metadata_analysis import analyze_metadata


# ==============================
# Flask Configuration
# ==============================

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# Create uploads folder automatically
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# ==============================
# Load Model (FIXED FOR RENDER)
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model", "deepfake_model.h5")

model = load_model(model_path)


# ==============================
# Database Connection
# ==============================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="audio_deepfake_db",
        charset="utf8mb4"
    )


# ==============================
# Allowed Extensions
# ==============================

ALLOWED_EXTENSIONS = {"wav", "mp3"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ==============================
# MAIN ROUTE (FILE UPLOAD)
# ==============================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        if 'audio' not in request.files:
            return "No file uploaded"

        file = request.files['audio']

        if file.filename == "":
            return "No file selected"

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename.encode("utf-8", "ignore").decode("utf-8"))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # Feature Extraction
                mfcc = extract_mfcc(file_path)
                mfcc = mfcc.reshape(1, 40, 1)

                # Model Prediction
                pred = model.predict(mfcc)[0][0]
                bio_score = float(pred) * 100
                meta_score = analyze_metadata(file_path)

                final_score = (bio_score + meta_score) / 2
                result = "REAL HUMAN VOICE" if final_score > 70 else "FAKE / SYNTHETIC AUDIO"

                # Save to MySQL
                db = get_db_connection()
                cursor = db.cursor()

                cursor.execute(
                    "INSERT INTO uploads (filename, file_path, prediction, confidence) VALUES (%s, %s, %s, %s)",
                    (filename, file_path, result, final_score)
                )

                db.commit()
                cursor.close()
                db.close()

                return render_template(
                    "result.html",
                    result=result,
                    score=round(final_score, 2)
                )

            except Exception as e:
                return f"Error processing file: {str(e)}"

        else:
            return "Invalid file format. Only WAV or MP3 allowed."

    return render_template("index.html")


# ==============================
# MICROPHONE ROUTE
# ==============================

@app.route("/record", methods=["POST"])
def record_audio():
    try:

        if 'audio' not in request.files:
            return jsonify({"error": "No audio received"})

        file = request.files['audio']
        filename = secure_filename(file.filename)

        if not allowed_file(filename):
            return jsonify({"error": "Invalid file format"})

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        mfcc = extract_mfcc(file_path)
        mfcc = mfcc.reshape(1, 40, 1)

        pred = model.predict(mfcc)[0][0]
        bio_score = float(pred) * 100
        meta_score = analyze_metadata(file_path)

        final_score = (bio_score + meta_score) / 2
        result = "REAL HUMAN VOICE" if final_score > 70 else "FAKE / SYNTHETIC AUDIO"

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO uploads (filename, file_path, prediction, confidence) VALUES (%s, %s, %s, %s)",
            (filename, file_path, result, final_score)
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "result": result,
            "score": round(final_score, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ==============================
# Run App
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)