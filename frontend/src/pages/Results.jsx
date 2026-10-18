import { useState } from "react";
import { Link } from "react-router-dom";
import { REPORTED } from "../data.js";

export default function Results() {
  const [hasMatrix, setHasMatrix] = useState(true);

  return (
    <section className="section">
      <div className="container">
        <h1 className="page-title">Project results</h1>
        <p className="section-lead">
          These are the reported results from the existing Google Colab evaluation on the dataset's
          Testing folder. This website did not re-run the evaluation.
        </p>

        <div className="grid two">
          <div className="card metric">
            <div className="metric-value">{REPORTED.accuracy}</div>
            <div className="metric-label">Test accuracy</div>
          </div>
          <div className="card metric">
            <div className="metric-value">{REPORTED.testImages}</div>
            <div className="metric-label">Test images</div>
          </div>
        </div>

        <h2 className="mt">Per-class F1-score</h2>
        <div className="grid four">
          {REPORTED.f1.map((c) => (
            <div className="card metric" key={c.name}>
              <div className="metric-value">{c.value.toFixed(2)}</div>
              <div className="metric-label">{c.name}</div>
              <div className="bar-track slim">
                <div className="bar-fill top" style={{ width: `${c.value * 100}%` }} />
              </div>
            </div>
          ))}
        </div>

        <h2 className="mt">Confusion matrix</h2>
        {hasMatrix ? (
          <div className="card center">
            <img
              src="/confusion_matrix.png"
              alt="Confusion matrix from the Colab evaluation"
              className="matrix-img"
              onError={() => setHasMatrix(false)}
            />
            <p className="muted small">Confusion matrix from the Colab evaluation.</p>
          </div>
        ) : (
          <div className="card">
            <p>
              No confusion matrix image has been added yet. To add the real one: in Colab,
              right-click the confusion matrix plot, save it as <code>confusion_matrix.png</code>,
              and put it in <code>frontend/public/</code>. It will show here after a refresh.
            </p>
          </div>
        )}

        <h2 className="mt">Reading these numbers</h2>
        <div className="card">
          <p>
            Pituitary and No Tumor are classified best (F1 0.91 and 0.88). Glioma and Meningioma
            are weaker (0.76 and 0.72), which means the model confuses them more often. Training
            was short (5 epochs) and used no data augmentation, so there is room to improve.
          </p>
        </div>

        <div className="cta mt">
          <Link to="/analyze" className="btn btn-primary">Try the model</Link>
        </div>
      </div>
    </section>
  );
}
