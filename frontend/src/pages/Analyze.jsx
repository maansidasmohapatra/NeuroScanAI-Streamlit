import { useEffect, useRef, useState } from "react";
import ScoreChart from "../components/ScoreChart.jsx";
import { CLASSES } from "../data.js";

const ALLOWED = ["image/png", "image/jpeg"];
const MAX_MB = 10;

export default function Analyze() {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);
  // null = checking, otherwise { reachable, model_loaded, error }
  const [backend, setBackend] = useState(null);

  const checkBackend = async () => {
    setBackend(null);
    try {
      const res = await fetch("/api/health");
      if (!res.ok) throw new Error("bad status");
      const data = await res.json();
      setBackend({ reachable: true, model_loaded: data.model_loaded, error: data.error });
    } catch {
      setBackend({ reachable: false, model_loaded: false, error: null });
    }
  };

  useEffect(() => {
    checkBackend();
  }, []);

  useEffect(() => {
    return () => previewUrl && URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  const chooseFile = (f) => {
    setResult(null);
    setError(null);
    if (!f) return;
    if (!ALLOWED.includes(f.type)) {
      setError("Unsupported file type. Please upload a PNG, JPG or JPEG image.");
      return;
    }
    if (f.size > MAX_MB * 1024 * 1024) {
      setError(`Image is too large. Maximum size is ${MAX_MB} MB.`);
      return;
    }
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
  };

  const reset = () => {
    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const form = new FormData();
      form.append("image", file);
      const res = await fetch("/api/predict", { method: "POST", body: form });
      let data = null;
      try {
        data = await res.json();
      } catch {
        /* non-JSON response */
      }
      if (!res.ok) {
        throw new Error((data && data.error) || `Server returned an error (${res.status}).`);
      }
      setResult(data);
      checkBackend();
    } catch (e) {
      if (e instanceof TypeError) {
        setError(
          "Could not reach the backend. Make sure the Flask server is running (python app.py in the backend folder)."
        );
        setBackend({ reachable: false, model_loaded: false, error: null });
      } else {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const info = result && CLASSES.find((c) => c.key === result.predicted_class);
  const backendBlocked = backend && (!backend.reachable || !backend.model_loaded);

  return (
    <section className="section">
      <div className="container">
        <h1 className="page-title">MRI analysis</h1>
        <p className="section-lead">
          Upload a brain MRI image (PNG, JPG or JPEG). The image is sent to the Flask backend, where
          the trained CNN predicts one of four classes.
        </p>

        {backend === null && <div className="banner info">Checking backend connection...</div>}
        {backend && !backend.reachable && (
          <div className="banner error">
            <b>Backend not reachable.</b> Start the Flask server: open a terminal, go to the
            <code>backend</code> folder and run <code>python app.py</code>.
            <button className="link-btn" onClick={checkBackend}>Retry</button>
          </div>
        )}
        {backend && backend.reachable && !backend.model_loaded && (
          <div className="banner error">
            <b>Model not loaded.</b> {backend.error}
            <button className="link-btn" onClick={checkBackend}>Retry</button>
          </div>
        )}
        {backend && backend.reachable && backend.model_loaded && (
          <div className="banner ok">Backend connected. Trained model loaded.</div>
        )}

        <div className="analyze-grid">
          <div className="panel">
            <h3>1. Upload</h3>
            {!previewUrl ? (
              <div
                className={`dropzone ${dragging ? "drag" : ""}`}
                onClick={() => inputRef.current && inputRef.current.click()}
                onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                onDragLeave={() => setDragging(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragging(false);
                  chooseFile(e.dataTransfer.files[0]);
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === "Enter" && inputRef.current && inputRef.current.click()}
              >
                <div className="drop-icon" aria-hidden="true">&#8679;</div>
                <p><b>Drag and drop an MRI image here</b></p>
                <p className="muted small">or click to browse. PNG, JPG, JPEG up to {MAX_MB} MB</p>
              </div>
            ) : (
              <div className="preview">
                <img src={previewUrl} alt="Uploaded MRI preview" />
                <p className="muted small">{file.name}</p>
              </div>
            )}
            <input
              ref={inputRef}
              type="file"
              accept=".png,.jpg,.jpeg,image/png,image/jpeg"
              hidden
              onChange={(e) => chooseFile(e.target.files[0])}
            />

            <div className="btn-row">
              <button
                className="btn btn-primary"
                onClick={analyze}
                disabled={!file || loading || backendBlocked}
              >
                {loading ? "Analyzing..." : "Analyze MRI"}
              </button>
              <button className="btn btn-ghost" onClick={reset} disabled={loading || (!file && !error)}>
                Reset / upload another
              </button>
            </div>
            {error && <div className="banner error mt-sm" role="alert">{error}</div>}
          </div>

          <div className="panel">
            <h3>2. Prediction</h3>
            {loading && (
              <div className="loading">
                <div className="spinner" aria-hidden="true" />
                <p>Analyzing MRI image...</p>
              </div>
            )}
            {!loading && !result && (
              <div className="placeholder">
                <p className="muted">Results will appear here after you click <b>Analyze MRI</b>.</p>
              </div>
            )}
            {!loading && result && (
              <div className="result">
                <div className="pred-label">Predicted class</div>
                <div className="pred-class">{result.display_name}</div>
                <div className="pred-score">Model output score: {(result.confidence * 100).toFixed(1)}%</div>

                <ScoreChart scores={result.scores} topClass={result.predicted_class} />
                <p className="muted small">
                  Scores are the model's softmax outputs, not medically validated probabilities.
                </p>

                {info && (
                  <div className="explain">
                    <h4>What this means</h4>
                    <p>{info.text}</p>
                  </div>
                )}
                {result.confidence < 0.6 && (
                  <div className="banner warn">
                    The top score is below 60%, so the model is uncertain about this image. Treat
                    the prediction as low-confidence.
                  </div>
                )}
                <p className="muted small">
                  The model reached about 82% accuracy on its test set, so wrong predictions are
                  expected, especially between glioma and meningioma.
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="disclaimer-box">
          <b>Educational use only.</b> This is a student project, not a medical diagnostic tool.
        </div>
      </div>
    </section>
  );
}
