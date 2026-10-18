import { ARCHITECTURE } from "../data.js";

export default function ModelPage() {
  return (
    <section className="section">
      <div className="container">
        <h1 className="page-title">Model architecture</h1>
        <p className="section-lead">
          A compact CNN: three convolution and pooling blocks extract image features, then a small
          dense network turns them into four class scores.
        </p>

        <div className="arch">
          {ARCHITECTURE.map((a, i) => (
            <div className="arch-step" key={i}>
              <div className="arch-box">
                <b>{a.layer}</b>
                {a.detail && <span>{a.detail}</span>}
              </div>
              {i < ARCHITECTURE.length - 1 && <div className="arch-arrow" aria-hidden="true">&darr;</div>}
            </div>
          ))}
        </div>

        <div className="grid three mt">
          <div className="card">
            <h3>Training setup</h3>
            <p className="small">Optimizer: Adam. Loss: sparse categorical cross-entropy. Metric: accuracy. Trained for 5 epochs in Google Colab with an 80/20 train/validation split.</p>
          </div>
          <div className="card">
            <h3>Preprocessing</h3>
            <p className="small">Images are converted to RGB and resized to 128&times;128. Pixel scaling (1/255) happens inside the model, so it is applied exactly once.</p>
          </div>
          <div className="card">
            <h3>Output</h3>
            <p className="small">Softmax gives four scores that sum to 100%. The highest score is the predicted class. They are model outputs, not medically validated probabilities.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
