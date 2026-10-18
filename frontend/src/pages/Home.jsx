import { Link } from "react-router-dom";
import { CLASSES } from "../data.js";

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="container hero-inner">
          <div className="hero-text">
            <span className="pill">Machine Learning CCA-3 Project</span>
            <h1>
              Brain Tumor Classification <span className="accent">Using Deep Learning</span>
            </h1>
            <p className="lead">
              CNN-based classification of brain MRI images into four categories: glioma,
              meningioma, pituitary tumor, and no tumor.
            </p>
            <div className="hero-actions">
              <Link to="/analyze" className="btn btn-primary">Analyze an MRI</Link>
              <Link to="/model" className="btn btn-ghost">View the model</Link>
            </div>
          </div>
          <div className="hero-visual" aria-hidden="true">
            <div className="orb" />
            <div className="stat-card s1"><b>4</b><span>classes</span></div>
            <div className="stat-card s2"><b>128&times;128</b><span>input size</span></div>
            <div className="stat-card s3"><b>82.12%</b><span>test accuracy</span></div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Project introduction</h2>
          <p className="section-lead">
            Brain tumors are identified on MRI scans, and reading them takes expert training. This
            project explores whether a small convolutional neural network (CNN) can learn to tell
            tumor types apart from MRI images.
          </p>
          <div className="grid three">
            <div className="card">
              <h3>1. Data</h3>
              <p>
                The Brain Tumor MRI Dataset from Kaggle, with separate Training and Testing folders
                across four classes.
              </p>
            </div>
            <div className="card">
              <h3>2. Model</h3>
              <p>
                A three-block CNN trained in Google Colab with the Adam optimizer and sparse
                categorical cross-entropy loss.
              </p>
            </div>
            <div className="card">
              <h3>3. Website</h3>
              <p>
                A React frontend sends your image to a Flask API, which runs the real trained model
                and returns four output scores.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="section alt">
        <div className="container">
          <h2>The four classes</h2>
          <div className="grid four">
            {CLASSES.map((c) => (
              <div className="card" key={c.key}>
                <h3>{c.name}</h3>
                <p className="small">{c.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container cta">
          <h2>Try it yourself</h2>
          <p className="section-lead">Upload an MRI image from the dataset's Testing folder and see what the model predicts.</p>
          <Link to="/analyze" className="btn btn-primary">Go to MRI analysis</Link>
        </div>
      </section>
    </>
  );
}
