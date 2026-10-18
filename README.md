# Brain Tumor Classification Using Deep Learning (Website)

A website for the Machine Learning CCA-3 project. Upload a brain MRI image and your trained CNN predicts one of four classes: **glioma, meningioma, no tumor, pituitary tumor**.

- **Frontend:** React + Vite (pages: Home, Model, Analyze MRI, Results)
- **Backend:** Python Flask API that loads your real `brain_tumor_cnn.keras` model

> Educational prototype only. This is **not** a medical diagnostic tool. It runs on your own computer and is not deployed online.

## Project structure

```
brain-tumor-website/
├── backend/
│   ├── app.py                  # Flask API
│   ├── requirements.txt
│   └── brain_tumor_cnn.keras   # <-- your trained model goes HERE
├── frontend/
│   ├── package.json
│   ├── vite.config.js          # forwards /api to Flask
│   ├── public/                 # optional: confusion_matrix.png
│   └── src/                    # React pages, components, styles
└── README.md
```

## Before you start: install these (Windows)

1. **Python 3.10 to 3.13** (64-bit), from python.org. Tick "Add Python to PATH" in the installer. Check with `python --version`.
2. **Node.js LTS**, from nodejs.org. Check with `node --version` and `npm --version`.

## Step 1: Put the model in the right place

Copy your trained model file to exactly:

```
backend/brain_tumor_cnn.keras
```

To export it from Google Colab after training:

```python
model.save("/content/brain_tumor_cnn.keras")

from google.colab import files
files.download("/content/brain_tumor_cnn.keras")
```

If the file is missing, the website shows a clear message and refuses to predict. It never uses a fake model.

## Step 2: Start the backend (Terminal 1)

Open the project folder in Cursor / VS Code (File > Open Folder). Open a terminal (Terminal > New Terminal).

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The TensorFlow install is large, so `pip install` takes a few minutes the first time. When it works you will see `Model loaded successfully.` and the server runs at http://127.0.0.1:5000. **Leave this terminal open.**

If PowerShell blocks `activate`, run this once and retry: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Step 3: Start the frontend (Terminal 2)

Open a **second** terminal with the `+` button in the terminal panel (the first must keep running).

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

## Step 4: Test it

1. Go to **Analyze MRI**. The green banner should say "Backend connected. Trained model loaded."
2. Upload an image from the dataset's `Testing/glioma`, `Testing/meningioma`, `Testing/notumor` or `Testing/pituitary` folder.
3. Click **Analyze MRI**. The predicted class and the four output scores appear.

Use Testing images, since the model never trained on them. The model is about 82% accurate, so some wrong predictions are normal, mostly glioma vs. meningioma.

## How prediction works

1. The browser sends the image to `POST /api/predict`.
2. Flask converts it to RGB, resizes it to 128 x 128 and adds a batch dimension.
3. Pixels stay in the 0-255 range, because the model already contains `Rescaling(1/255)`. Dividing in the backend too would normalize twice.
4. The model returns four softmax scores in this class order: `glioma, meningioma, notumor, pituitary`.
5. The highest score is the predicted class. Scores are model outputs, not medically validated probabilities.

## Adding the confusion matrix

No confusion matrix is invented. To add your real one, save the plot from Colab as `confusion_matrix.png` and place it in `frontend/public/`. It appears on the Results page after a refresh.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Backend not reachable" on the Analyze page | Terminal 1 must be running `python app.py` in the `backend` folder. Click Retry. |
| "Model not loaded" / "Model file not found" | Put `brain_tumor_cnn.keras` in `backend/` (no restart needed, click Retry). |
| "Model could not be loaded" | Run `pip install -U -r requirements.txt` in the backend venv. |
| `npm` is not recognized | Install Node.js LTS and reopen the terminal. |
| `python app.py` says port 5000 is in use | Close the other program using port 5000, or restart your terminal. |
| `pip install tensorflow` fails | Check Python is 3.10 to 3.13 (64-bit). |

## Production build (optional)

`cd frontend` then `npm run build` creates a `dist/` folder. The site still needs the Flask backend running, and it is not deployed anywhere unless you host it yourself.

## Streamlit version

A Streamlit implementation of the same Home, Model, Analyze MRI, and Results sections is included in `streamlit_app.py`. The original React/Vite frontend and Flask backend remain unchanged. The Streamlit version loads the existing model from `backend/brain_tumor_cnn.keras`.

### Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

### Deploy on Streamlit Community Cloud

Select this repository, branch `main`, and main file path `streamlit_app.py`. Keep `requirements.txt` in the repository root. The model is expected at `backend/brain_tumor_cnn.keras`.
