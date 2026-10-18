"""Flask API for Brain Tumor Classification Using Deep Learning.

Loads the CNN trained in Google Colab (brain_tumor_cnn.keras) and exposes:
    GET  /api/health   -> model status
    POST /api/predict  -> multipart form field "image" -> class + four scores

Educational prototype only - not a medical diagnostic tool.
"""

import io
import os
import threading
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request
from PIL import Image, UnidentifiedImageError

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "brain_tumor_cnn.keras"

IMG_SIZE = (128, 128)
# Same alphabetical order that image_dataset_from_directory used in the Colab notebook.
CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
DISPLAY_NAMES = {
    "glioma": "Glioma",
    "meningioma": "Meningioma",
    "notumor": "No Tumor",
    "pituitary": "Pituitary Tumor",
}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
MAX_UPLOAD_MB = 10

MISSING_MODEL_HELP = (
    f"Model file not found. Place your trained model at: {MODEL_PATH}. "
    "To export it from Google Colab run: "
    "model.save('/content/brain_tumor_cnn.keras') and then "
    "from google.colab import files; files.download('/content/brain_tumor_cnn.keras')."
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

_model = None
_model_error = None
_model_lock = threading.Lock()


@app.after_request
def add_cors_headers(response):
    # The Vite dev server proxies /api, but allow direct calls from localhost too.
    origin = request.headers.get("Origin", "")
    if origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:"):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def load_model():
    """Load the real trained model. Never substitutes a fake one.

    Returns (model, error_message). Retries on every call while the model is
    not loaded, so dropping the file in place works without restarting Flask.
    """
    global _model, _model_error
    with _model_lock:
        if _model is not None:
            return _model, None

        if not MODEL_PATH.exists():
            _model_error = MISSING_MODEL_HELP
            return None, _model_error

        try:
            import tensorflow as tf

            model = tf.keras.models.load_model(str(MODEL_PATH), compile=False)
            if tuple(model.input_shape[1:]) != (IMG_SIZE[0], IMG_SIZE[1], 3):
                raise ValueError(
                    f"Model expects input {model.input_shape}, but 128x128 RGB images are sent."
                )
            if model.output_shape[-1] != len(CLASS_NAMES):
                raise ValueError(
                    f"Model has {model.output_shape[-1]} outputs, expected {len(CLASS_NAMES)}."
                )
            _model = model
            _model_error = None
            return _model, None
        except Exception as exc:  # noqa: BLE001 - report any load problem to the UI
            _model_error = (
                f"The model file exists but could not be loaded "
                f"({type(exc).__name__}: {exc}). Try: pip install -U -r requirements.txt"
            )
            return None, _model_error


def preprocess(image: Image.Image) -> np.ndarray:
    """RGB -> 128x128 -> float32 in the 0-255 range with a batch axis.

    The model already contains Rescaling(1/255), so we do NOT divide by 255 here.
    """
    image = image.convert("RGB").resize(IMG_SIZE, Image.BILINEAR)
    return np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)


@app.get("/api/health")
def health():
    model, error = load_model()
    return jsonify(
        {
            "status": "ok",
            "model_loaded": model is not None,
            "model_path": str(MODEL_PATH),
            "classes": CLASS_NAMES,
            "error": error,
        }
    )


@app.post("/api/predict")
def predict():
    model, error = load_model()
    if model is None:
        return jsonify({"error": error}), 503

    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify({"error": "No image was uploaded. Send the file in the 'image' field."}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file type. Please upload a PNG, JPG or JPEG image."}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        image.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        return jsonify({"error": "The file could not be read as a valid image."}), 400

    try:
        with _model_lock:
            scores = model.predict(preprocess(image), verbose=0)[0]
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Prediction failed: {type(exc).__name__}: {exc}"}), 500

    scores = [float(s) for s in scores]
    top = int(np.argmax(scores))
    return jsonify(
        {
            "predicted_class": CLASS_NAMES[top],
            "display_name": DISPLAY_NAMES[CLASS_NAMES[top]],
            "confidence": scores[top],
            "scores": [
                {
                    "class": c,
                    "display_name": DISPLAY_NAMES[c],
                    "score": scores[i],
                }
                for i, c in enumerate(CLASS_NAMES)
            ],
        }
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": f"Image is too large. Maximum size is {MAX_UPLOAD_MB} MB."}), 413


if __name__ == "__main__":
    model, err = load_model()
    if model is None:
        print(f"\n[WARNING] {err}\n")
    else:
        print("\nModel loaded successfully.\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
