from pathlib import Path
import streamlit as st
import numpy as np
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "backend" / "brain_tumor_cnn.keras"
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]
DISPLAY = {"glioma": "Glioma", "meningioma": "Meningioma", "notumor": "No Tumor", "pituitary": "Pituitary Tumor"}
EXPLANATIONS = {
    "glioma": "Gliomas arise from glial (supporting) cells of the brain or spinal cord. They may appear as irregular masses on MRI.",
    "meningioma": "Meningiomas grow from the membranes surrounding the brain and can appear as masses attached to the brain's outer surface.",
    "notumor": "The model found no pattern resembling the three tumor classes it was trained on in this image.",
    "pituitary": "Pituitary tumors develop in the pituitary gland at the base of the brain.",
}
ARCH = [("Input", "128 × 128 × 3 (RGB)"), ("Rescaling", "1/255 (inside the model)"), ("Conv2D + ReLU", "16 filters, 3×3"), ("MaxPooling2D", "2×2"), ("Conv2D + ReLU", "32 filters, 3×3"), ("MaxPooling2D", "2×2"), ("Conv2D + ReLU", "64 filters, 3×3"), ("MaxPooling2D", "2×2"), ("Flatten", ""), ("Dense + ReLU", "64 units"), ("Dropout", "0.4"), ("Dense + Softmax", "4 output units")]

st.set_page_config(page_title="NeuroScanAI", page_icon="🧠", layout="wide")
st.markdown("""<style>
:root{--navy:#0a1628;--navy2:#0f1f38;--navy3:#162a4a;--cyan:#22d3ee;--muted:#8fa3bf}
.stApp{background:#0a1628;color:#f1f5f9}.block-container{max-width:1120px;padding-top:1.5rem;padding-bottom:2rem}
[data-testid="stHeader"]{background:rgba(10,22,40,.92)} h1,h2,h3,h4{color:#f1f5f9} .stMarkdown p{color:#cbd5e1}
.stButton>button{border-radius:10px;font-weight:700;border:1px solid rgba(34,211,238,.35)}
.stButton>button[kind="primary"]{background:#22d3ee;color:#0a1628;border:0}
[data-testid="stFileUploader"]{background:rgba(34,211,238,.04);border:1px dashed #22d3ee;border-radius:14px;padding:1rem}
[data-testid="stMetric"]{background:#0f1f38;border:1px solid rgba(34,211,238,.2);padding:1.1rem;border-radius:14px}
[data-testid="stMetricValue"]{color:#22d3ee} hr{border-color:rgba(34,211,238,.2)}
.ns-nav{display:flex;justify-content:space-between;align-items:center;padding:.8rem 0 1rem;border-bottom:1px solid rgba(34,211,238,.2);margin-bottom:1.3rem}
.ns-brand{font-size:1.35rem;font-weight:800;color:#f1f5f9}.ns-brand span{color:#22d3ee}.ns-muted{color:#8fa3bf;font-size:.9rem}
.ns-pill{display:inline-block;color:#22d3ee;border:1px solid rgba(34,211,238,.25);background:rgba(34,211,238,.08);border-radius:999px;padding:.3rem .85rem;font-size:.85rem;font-weight:600;margin-bottom:1rem}
.ns-hero{background:radial-gradient(850px 400px at 85% 0%,rgba(34,211,238,.16),transparent 60%),radial-gradient(700px 400px at 0% 100%,rgba(14,90,140,.35),transparent 60%);border-radius:18px;padding:2.2rem;border:1px solid rgba(34,211,238,.12)}
.ns-card{background:#0f1f38;border:1px solid rgba(34,211,238,.2);border-radius:14px;padding:1.2rem 1.3rem;min-height:120px;margin-bottom:.5rem}.ns-card h3{color:#22d3ee;margin-top:0}
.ns-arch{background:#0f1f38;border:1px solid rgba(34,211,238,.2);border-left:4px solid #22d3ee;border-radius:10px;padding:.8rem 1rem;margin:.35rem auto;max-width:650px;display:flex;justify-content:space-between;gap:1rem}.ns-arch span{color:#8fa3bf}
.ns-result{background:#0f1f38;border:1px solid rgba(34,211,238,.2);border-radius:14px;padding:1.2rem}.ns-pred{color:#22d3ee;font-size:2rem;font-weight:800}
footer{color:#8fa3bf;font-size:.9rem;text-align:center;padding:1.5rem 0 .5rem;border-top:1px solid rgba(143,163,191,.2);margin-top:2rem}
</style>""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading the trained CNN model...")
def load_model():
    import tensorflow as tf
    return tf.keras.models.load_model(str(MODEL_PATH), compile=False)

st.markdown('<div class="ns-nav"><div class="ns-brand">● NeuroScan<span>AI</span></div><div class="ns-muted">Brain Tumor Classification Using Deep Learning</div></div>', unsafe_allow_html=True)
page = st.radio("Navigation", ["Home", "Model", "Analyze MRI", "Results"], horizontal=True, label_visibility="collapsed", key="nav_page")
st.markdown("<hr>", unsafe_allow_html=True)

if page == "Home":
    st.markdown('<div class="ns-hero"><div class="ns-pill">Machine Learning CCA-3 Project</div><h1>Brain Tumor Classification<br><span style="color:#22d3ee">Using Deep Learning</span></h1><p style="font-size:1.15rem;color:#cbd5e1;max-width:720px">CNN-based classification of brain MRI images into four categories: glioma, meningioma, pituitary tumor, and no tumor.</p></div>', unsafe_allow_html=True)
    st.write("")
    cols = st.columns(3)
    cards = [("1. Data", "The Brain Tumor MRI Dataset from Kaggle, with separate Training and Testing folders across four classes."), ("2. Model", "A three-block CNN trained in Google Colab with Adam and sparse categorical cross-entropy loss."), ("3. Website", "An interactive interface runs the real trained model and returns four output scores for an uploaded MRI image.")]
    for col,(title,desc) in zip(cols,cards):
        with col: st.markdown(f'<div class="ns-card"><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.subheader("The four classes")
    cols=st.columns(4)
    for col,key in zip(cols,CLASSES):
        with col: st.markdown(f'<div class="ns-card"><h3>{DISPLAY[key]}</h3><p>{EXPLANATIONS[key]}</p></div>',unsafe_allow_html=True)
    st.info("Use the navigation above to analyze an MRI, explore the CNN architecture, or view the existing evaluation results.")

elif page == "Model":
    st.title("Model architecture")
    st.markdown('<p style="color:#b6c4d8">A compact CNN: three convolution and pooling blocks extract image features, then a small dense network turns them into four class scores.</p>',unsafe_allow_html=True)
    for i,(layer,detail) in enumerate(ARCH):
        st.markdown(f'<div class="ns-arch"><b>{layer}</b><span>{detail}</span></div>',unsafe_allow_html=True)
        if i < len(ARCH)-1: st.markdown('<div style="text-align:center;color:#22d3ee">↓</div>',unsafe_allow_html=True)
    st.write("")
    cols=st.columns(3)
    texts=[("Training setup","Optimizer: Adam. Loss: sparse categorical cross-entropy. Trained for 5 epochs in Google Colab with an 80/20 train/validation split."),("Preprocessing","Images are converted to RGB and resized to 128×128. Scaling (1/255) happens inside the model, so it is applied exactly once."),("Output","Softmax gives four output scores. The highest score is the predicted class. Scores are not medically validated probabilities.")]
    for col,(title,desc) in zip(cols,texts):
        with col: st.markdown(f'<div class="ns-card"><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

elif page == "Analyze MRI":
    st.title("MRI analysis")
    st.markdown('<p style="color:#b6c4d8">Upload a brain MRI image (PNG, JPG or JPEG). The trained CNN predicts one of four classes.</p>',unsafe_allow_html=True)
    if not MODEL_PATH.exists():
        st.error(f"Model file not found at {MODEL_PATH}. Keep brain_tumor_cnn.keras inside the backend folder.")
        st.stop()
    try: model=load_model()
    except Exception as e:
        st.error(f"The trained model could not be loaded: {type(e).__name__}: {e}")
        st.info("Check that the model file is the original trained model and that the deployed Python/TensorFlow versions are compatible.")
        st.stop()
    st.success("Backend connected. Trained model loaded.")
    left,right=st.columns(2,gap="large")
    with left:
        st.markdown('<div class="ns-card"><h3>1. Upload</h3><p>PNG, JPG or JPEG · up to 10 MB</p></div>',unsafe_allow_html=True)
        uploaded=st.file_uploader("Drag and drop an MRI image here or browse",type=["png","jpg","jpeg"],key="mri_upload")
        image=None
        if uploaded:
            if uploaded.size>10*1024*1024: st.error("Image is too large. Maximum size is 10 MB.")
            else:
                try:
                    image=Image.open(uploaded).convert("RGB")
                    st.image(image,caption=uploaded.name,use_container_width=True)
                except (UnidentifiedImageError,OSError): st.error("The file could not be read as a valid image.")
        analyze=st.button("Analyze MRI",type="primary",disabled=image is None,use_container_width=True)
        if st.button("Reset / upload another",use_container_width=True):
            st.session_state.pop("mri_result",None); st.session_state.pop("mri_upload",None); st.rerun()
    with right:
        st.markdown('<div class="ns-card"><h3>2. Prediction</h3><p>Results appear here after you click Analyze MRI.</p></div>',unsafe_allow_html=True)
        if analyze and image is not None:
            with st.spinner("Analyzing MRI image..."):
                arr=np.asarray(image.resize((128,128),Image.Resampling.BILINEAR),dtype=np.float32)
                scores=np.asarray(model.predict(np.expand_dims(arr,axis=0),verbose=0)[0],dtype=float)
            if len(scores)!=4: st.error(f"Expected four model outputs, received {len(scores)}.")
            else: st.session_state.mri_result={"scores":scores.tolist(),"predicted":CLASSES[int(np.argmax(scores))]}
        result=st.session_state.get("mri_result")
        if result:
            predicted=result["predicted"]
            st.markdown(f'<div class="ns-result"><div class="ns-muted">PREDICTED CLASS</div><div class="ns-pred">{DISPLAY[predicted]}</div><p>Model output score: {max(result["scores"])*100:.1f}%</p></div>',unsafe_allow_html=True)
            fig,ax=plt.subplots(figsize=(7,3.2)); fig.patch.set_facecolor('#0f1f38'); ax.set_facecolor('#0f1f38')
            labels=[DISPLAY[k] for k in CLASSES]; vals=np.array(result["scores"])*100
            bars=ax.barh(labels,vals,color=['#22d3ee' if k==predicted else '#3b5b80' for k in CLASSES])
            ax.invert_yaxis(); ax.set_xlim(0,100); ax.set_xlabel('Model output score (%)',color='#cbd5e1'); ax.tick_params(colors='#cbd5e1')
            for spine in ax.spines.values(): spine.set_color('#162a4a')
            ax.grid(axis='x',alpha=.15)
            for bar,val in zip(bars,vals): ax.text(min(val+1,91),bar.get_y()+bar.get_height()/2,f'{val:.1f}%',va='center',color='#f1f5f9',fontsize=9)
            fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)
            st.caption("Scores are the model's softmax outputs, not medically validated probabilities.")
            st.markdown(f'<div class="ns-card"><h3>What this means</h3><p>{EXPLANATIONS[predicted]}</p></div>',unsafe_allow_html=True)
            if max(result["scores"])<0.6: st.warning("The top score is below 60%, so the model is uncertain about this image.")
            st.caption("The model reached about 82% accuracy on its test set, so incorrect predictions are possible.")
    st.markdown('<div class="ns-card" style="text-align:center;margin-top:1.5rem"><b>Educational use only.</b> This is a student project, not a medical diagnostic tool.</div>',unsafe_allow_html=True)

elif page == "Results":
    st.title("Project results")
    st.markdown('<p style="color:#b6c4d8">Reported results from the existing Google Colab evaluation on the dataset Testing folder. This website did not re-run the evaluation.</p>',unsafe_allow_html=True)
    c1,c2=st.columns(2); c1.metric("Test accuracy","82.12%"); c2.metric("Test images","1,600")
    st.subheader("Per-class F1-score")
    cols=st.columns(4)
    for col,(name,val) in zip(cols,[("Glioma",.76),("Meningioma",.72),("No Tumor",.88),("Pituitary Tumor",.91)]):
        with col: st.metric(name,f"{val:.2f}"); st.progress(val)
    st.subheader("Confusion matrix")
    matrix=ROOT/"frontend"/"public"/"confusion_matrix.png"
    if matrix.exists(): st.image(str(matrix),caption="Confusion matrix from the Colab evaluation",width=560)
    else: st.info("No confusion matrix image has been added. Add your real Colab plot as frontend/public/confusion_matrix.png to display it here.")
    st.subheader("Reading these numbers")
    st.markdown('<div class="ns-card"><p>Pituitary and No Tumor have the strongest reported F1-scores (0.91 and 0.88). Glioma and Meningioma are weaker (0.76 and 0.72), so these classes may be confused more often. Training lasted 5 epochs without data augmentation.</p></div>',unsafe_allow_html=True)

st.markdown('<footer><b>NeuroScanAI</b> · Brain Tumor Classification Using Deep Learning<br>Educational use only. This student prototype is not a medical device and must not be used for diagnosis or clinical decisions.</footer>',unsafe_allow_html=True)
