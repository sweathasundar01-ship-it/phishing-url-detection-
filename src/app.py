
from pathlib import Path
import sys

import joblib
import pandas as pd
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "url_only_model.joblib"
DATASET_PATH = ROOT / "dataset" / "phishingdata_clean.csv"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from url_analyzer import extract_url_features


st.set_page_config(
    page_title="THREATVISION | URL Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stSidebar"],
[data-testid="stToolbar"] {display:none !important;}

.stApp {
    background:
        radial-gradient(ellipse at 15% 5%, #102b20 0%, transparent 38%),
        radial-gradient(ellipse at 90% 30%, #071b22 0%, transparent 35%),
        #050807;
    color: #e5fff0;
}
.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}
h1, h2, h3 {color:#eafff1 !important;}
.brand {
    color:#00ff99; font-size:20px; font-weight:800;
    letter-spacing:3px;
}
.status {
    color:#00ff99; border:1px solid #176b49;
    border-radius:30px; padding:8px 14px;
    font-size:12px; text-align:center;
}
.hero {
    padding:45px 20px; text-align:center;
    border:1px solid #173e2c; border-radius:22px;
    background:linear-gradient(140deg,#0c1b12,#07100d 65%,#07151a);
    box-shadow:0 0 45px #00ff9910;
}
.eyebrow {
    color:#00ff99; font-size:12px;
    letter-spacing:4px; font-weight:bold;
}
.hero-title {
    font-size:clamp(34px,6vw,64px);
    font-weight:900; letter-spacing:2px; margin:15px 0;
}
.hero-title span {color:#00ff99;}
.section-label {
    color:#00ff99; font-size:12px;
    letter-spacing:3px; font-weight:bold;
}
div[data-testid="stMetric"] {
    background:linear-gradient(145deg,#0d1c13,#08100c);
    border:1px solid #1c4931; border-radius:14px;
    padding:18px;
}
div[data-testid="stMetricLabel"] {color:#9fbdac;}
div[data-testid="stMetricValue"] {color:#00ff99;}
div.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    background:#00ff99; color:#031108;
    border:0; border-radius:10px;
    font-weight:800; min-height:48px;
}
div[data-baseweb="input"] input {
    background:#07100b; color:#eafff1;
}
.footer {
    text-align:center; color:#799987;
    font-size:12px; padding:25px 0;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "URL-only model missing. Run src/train_url_model.py first."
        )
    return joblib.load(MODEL_PATH)


@st.cache_data
def calculate_metrics():
    """Evaluate the saved model on the same reproducible held-out split."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError("Cleaned dataset not found.")

    df = pd.read_csv(DATASET_PATH)
    df.columns = df.columns.str.strip()

    model = load_model()
    features = list(model.feature_names_in_)

    X = df[features]
    y = df["Result"]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    predictions = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test, predictions, pos_label=1, zero_division=0
        ),
        "recall": recall_score(
            y_test, predictions, pos_label=1, zero_division=0
        ),
        "f1": f1_score(
            y_test, predictions, pos_label=1, zero_division=0
        ),
    }


# Header
left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<div class="brand">🛡 THREATVISION</div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        '<div class="status">● ML ENGINE READY</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

st.markdown("""
<div class="hero">
    <div class="eyebrow">URL SECURITY ANALYSIS</div>
    <div class="hero-title">DETECT THREATS.<br>
    <span>STAY SECURE.</span></div>
    <p style="color:#a7c5b4">
        Enter a URL to inspect its features and obtain an
        experimental machine-learning classification.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.markdown(
    '<div class="section-label">01 / URL ANALYSIS</div>',
    unsafe_allow_html=True,
)
st.subheader("Scan a website")

with st.form("url_scan_form"):
    url = st.text_input(
        "Target URL",
        placeholder="https://example.com",
    )
    submitted = st.form_submit_button(
        "⚡ ANALYSE URL",
        use_container_width=True,
    )

if submitted:
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        try:
            model = load_model()
            features = extract_url_features(url)

            # Ensure the analyzer and model have matching feature names.
            expected = list(model.feature_names_in_)
            missing = [name for name in expected if name not in features]

            if missing:
                raise ValueError(
                    f"URL analyzer is missing model features: {missing}"
                )

            X = pd.DataFrame(
                [[features[name] for name in expected]],
                columns=expected,
            )

            prediction = int(model.predict(X)[0])

            st.markdown("---")
            st.markdown(
                '<div class="section-label">02 / SCAN REPORT</div>',
                unsafe_allow_html=True,
            )

            if prediction == -1:
                st.error("⚠️ MODEL CLASSIFICATION: PHISHING")
            elif prediction == 1:
                st.success("🛡️ MODEL CLASSIFICATION: LEGITIMATE")
            else:
                st.warning(f"Unknown model class: {prediction}")

            st.write("**URL analysed:**", url)

            st.warning(
                "Experimental prediction only. This model uses a limited "
                "set of URL features and may misclassify real websites. "
                "A LEGITIMATE result does not prove a website is safe."
            )

            with st.expander("View extracted URL features"):
                st.json(features)

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")


# Model metrics
st.write("")
st.markdown("---")
st.markdown(
    '<div class="section-label">03 / MODEL PERFORMANCE</div>',
    unsafe_allow_html=True,
)
st.subheader("Held-out dataset evaluation")

try:
    metrics = calculate_metrics()
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Test Accuracy", f"{metrics['accuracy']:.2%}")
    m2.metric("Precision", f"{metrics['precision']:.2%}")
    m3.metric("Recall", f"{metrics['recall']:.2%}")
    m4.metric("F1 Score", f"{metrics['f1']:.2%}")

    st.caption(
        "These metrics describe performance on a held-out dataset split, "
        "not the correctness of the URL currently entered."
    )
except Exception as exc:
    st.error(f"Could not calculate model metrics: {exc}")


# Workflow
st.markdown("---")
st.markdown(
    '<div class="section-label">04 / HOW IT WORKS</div>',
    unsafe_allow_html=True,
)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 01 · Input")
    st.write("Enter the URL you want to analyse.")

with c2:
    st.markdown("### 02 · Analyse")
    st.write("Extract URL features and run the Random Forest model.")

with c3:
    st.markdown("### 03 · Review")
    st.write("Review the classification and extracted features.")

st.markdown("---")
st.markdown("""
<div class="footer">
    THREATVISION · PHISHING URL DETECTION<br>
    Built with Python · Streamlit · Random Forest
</div>
""", unsafe_allow_html=True)