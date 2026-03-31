import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import os

st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f5f3ef;
    color: #1a1a2e;
}
.stApp {
    background: linear-gradient(135deg, #faf8f4 0%, #f0ece4 50%, #faf7f2 100%);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8f5f0 100%);
    border-right: 1px solid #e8e0d4;
}
section[data-testid="stSidebar"] * { color: #4a4540 !important; }

.hero-banner {
    background: linear-gradient(135deg, #ffffff 0%, #fdf8f2 60%, #fff5eb 100%);
    border: 1px solid #e8ddd0;
    border-radius: 20px;
    padding: 48px 56px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(234,88,12,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 200px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(234,88,12,0.10);
    border: 1px solid rgba(234,88,12,0.25);
    color: #ea580c !important;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 900;
    color: #1a1208 !important;
    line-height: 1.1;
    margin: 0 0 14px 0;
    letter-spacing: -1px;
}
.hero-title span { color: #ea580c; }
.hero-subtitle {
    font-size: 16px;
    color: #7a6e62 !important;
    font-weight: 300;
    max-width: 480px;
    line-height: 1.6;
}

.stats-row {
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
}
.stat-card {
    flex: 1;
    background: #ffffff;
    border: 1px solid #e8ddd0;
    border-radius: 14px;
    padding: 22px 24px;
    text-align: center;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.stat-card:hover {
    border-color: #ea580c;
    box-shadow: 0 4px 16px rgba(234,88,12,0.10);
    transform: translateY(-2px);
}
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    color: #ea580c !important;
    display: block;
}
.stat-label {
    font-size: 12px;
    color: #a89e94 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
}

.section-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #a89e94 !important;
    margin-bottom: 16px;
}

.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid #ddd4c8 !important;
    border-radius: 10px !important;
    color: #1a1208 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    padding: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.stTextArea textarea:focus {
    border-color: #ea580c !important;
    box-shadow: 0 0 0 3px rgba(234,88,12,0.10) !important;
}
.stTextArea textarea::placeholder { color: #c8beb4 !important; }

.stButton > button {
    background: linear-gradient(135deg, #ea580c 0%, #dc4e08 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    padding: 14px 28px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(234,88,12,0.20) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(234,88,12,0.28) !important;
}

.result-real {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border: 1px solid #bbf7d0;
    border-left: 4px solid #16a34a;
    border-radius: 14px;
    padding: 28px 32px;
    margin: 16px 0;
    box-shadow: 0 2px 12px rgba(22,163,74,0.08);
}
.result-fake {
    background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
    border: 1px solid #fecdd3;
    border-left: 4px solid #dc2626;
    border-radius: 14px;
    padding: 28px 32px;
    margin: 16px 0;
    box-shadow: 0 2px 12px rgba(220,38,38,0.08);
}
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 8px 0;
}
.result-real .result-title { color: #16a34a !important; }
.result-fake .result-title { color: #dc2626 !important; }
.result-desc { font-size: 14px; color: #6b7280 !important; line-height: 1.5; }

.sidebar-stat {
    background: #faf8f4;
    border: 1px solid #e8ddd0;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.sidebar-stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    color: #ea580c !important;
    font-weight: 700;
}
.sidebar-stat-lbl {
    font-size: 11px;
    color: #a89e94 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}
hr { border-color: #e8ddd0 !important; }
</style>
""", unsafe_allow_html=True)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return re.sub(r'\s+', ' ', text).strip()


@st.cache_resource(show_spinner="🔄 Training model on dataset...")
def load_and_train():
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import PassiveAggressiveClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix

    paths = [("True.csv","Fake.csv"), ("dataset/True.csv","dataset/Fake.csv")]
    true_df = fake_df = None
    for tp, fp in paths:
        if os.path.exists(tp) and os.path.exists(fp):
            true_df, fake_df = pd.read_csv(tp), pd.read_csv(fp)
            break
    if true_df is None:
        return None, None, None, None, 0, 0

    true_df['label'] = 1
    fake_df['label'] = 0
    df = pd.concat([true_df, fake_df], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    df['content'] = (df['title'] + ' ' + df['text']).apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(df['content'], df['label'], test_size=0.2, random_state=42)
    tfidf = TfidfVectorizer(max_features=10000, stop_words='english')
    Xtr = tfidf.fit_transform(X_train)
    Xte = tfidf.transform(X_test)
    model = PassiveAggressiveClassifier(max_iter=50, random_state=42)
    model.fit(Xtr, y_train)
    preds = model.predict(Xte)
    return model, tfidf, accuracy_score(y_test, preds), confusion_matrix(y_test, preds), len(true_df), len(fake_df)


model, tfidf, accuracy, cm, real_count, fake_count = load_and_train()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 📋 Model Info")
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-stat"><div class="sidebar-stat-num">PAC</div><div class="sidebar-stat-lbl">Algorithm</div></div>
    <div class="sidebar-stat"><div class="sidebar-stat-num">TF-IDF</div><div class="sidebar-stat-lbl">Vectorizer</div></div>
    <div class="sidebar-stat"><div class="sidebar-stat-num">10K</div><div class="sidebar-stat-lbl">Max Features</div></div>
    """, unsafe_allow_html=True)
    if accuracy:
        st.markdown(f'<div class="sidebar-stat"><div class="sidebar-stat-num">{accuracy*100:.1f}%</div><div class="sidebar-stat-lbl">Accuracy</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Dataset: Kaggle Fake News Detection")
    st.caption("🎓 Made by Pratham")

# ── HERO ──
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">🤖 ML Project · NLP · Text Classification</div>
    <h1 class="hero-title">Fake News<br><span>Detector</span></h1>
    <p class="hero-subtitle">Paste any news headline or article below — the model will instantly classify it as Real or Fake using NLP.</p>
</div>
""", unsafe_allow_html=True)

# ── STATS ──
if model:
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card"><span class="stat-number">{real_count:,}</span><div class="stat-label">Real Articles</div></div>
        <div class="stat-card"><span class="stat-number">{fake_count:,}</span><div class="stat-label">Fake Articles</div></div>
        <div class="stat-card"><span class="stat-number">{accuracy*100:.1f}%</span><div class="stat-label">Accuracy</div></div>
        <div class="stat-card"><span class="stat-number">TF-IDF</span><div class="stat-label">Method</div></div>
    </div>
    """, unsafe_allow_html=True)

# ── DATASET NOT FOUND ──
if model is None:
    st.markdown("""
    <div style="background:#fff7ed;border:1px solid #fed7aa;border-left:4px solid #ea580c;border-radius:14px;padding:28px 32px;margin-bottom:24px;box-shadow:0 2px 12px rgba(234,88,12,0.08);">
        <h3 style="color:#ea580c;margin:0 0 12px 0;font-family:'Playfair Display',serif;">⚠️ Dataset Not Found</h3>
        <p style="color:#92400e;margin:0 0 16px 0;font-size:15px;">
            Place <code style="background:#fde68a;padding:2px 8px;border-radius:4px;color:#92400e;">True.csv</code> and 
            <code style="background:#fde68a;padding:2px 8px;border-radius:4px;color:#92400e;">Fake.csv</code> 
            in the <strong>same folder</strong> as <code style="background:#fde68a;padding:2px 8px;border-radius:4px;color:#92400e;">app.py</code>
        </p>
        <p style="color:#a16207;font-size:13px;margin:0 0 16px 0;">
            📥 Download: <a href="https://www.kaggle.com/datasets/emineyetm/fake-news-detection-datasets" style="color:#ea580c;" target="_blank">kaggle.com → Fake News Detection Dataset</a>
        </p>
        <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;font-family:monospace;font-size:13px;color:#92400e;">
            📂 ML/<br>
            &nbsp;&nbsp;&nbsp;├── app.py<br>
            &nbsp;&nbsp;&nbsp;├── True.csv<br>
            &nbsp;&nbsp;&nbsp;└── Fake.csv
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── INPUT ──
st.markdown('<p class="section-label">🔍 Analyse Article</p>', unsafe_allow_html=True)
news_input = st.text_area("", placeholder="Paste your news headline or full article here...\n\nExample: Scientists confirm new evidence of water beneath Mars polar ice caps...", height=180, label_visibility="collapsed")

col1, col2, _ = st.columns([2, 1, 2])
with col1:
    analyse_btn = st.button("🚀 Analyse Now", use_container_width=True)
with col2:
    st.button("🗑️ Clear", use_container_width=True)

if analyse_btn:
    if not news_input.strip():
        st.markdown('<div style="background:#fdf2f8;border:1px solid #f9a8d4;border-left:4px solid #ec4899;border-radius:12px;padding:16px 24px;margin:16px 0;"><p style="color:#be185d;margin:0;">⚡ Please enter some news text first.</p></div>', unsafe_allow_html=True)
    else:
        with st.spinner("Analysing..."):
            pred = model.predict(tfidf.transform([clean_text(news_input)]))[0]
        if pred == 1:
            st.markdown('<div class="result-real"><div class="result-title">✅ Real News</div><p class="result-desc">The model classified this as <strong style="color:#16a34a">REAL</strong>. Language patterns match credible news sources in the training data.</p></div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown('<div class="result-fake"><div class="result-title">❌ Fake News</div><p class="result-desc">The model classified this as <strong style="color:#dc2626">FAKE</strong>. Language patterns suggest misinformation. Always verify with trusted sources.</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── EXAMPLES ──
st.markdown('<p class="section-label">💡 Try Sample Examples</p>', unsafe_allow_html=True)
ex1, ex2 = st.columns(2)

with ex1:
    st.markdown('<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:16px 20px;margin-bottom:10px;"><div style="font-size:11px;letter-spacing:1.5px;color:#16a34a;text-transform:uppercase;margin-bottom:6px;">Real News Sample</div><p style="color:#374151;font-size:13px;line-height:1.5;margin:0;">"NASA confirms new findings about water ice on the lunar south pole surface."</p></div>', unsafe_allow_html=True)
    if st.button("▶ Test Real Example", use_container_width=True, key="r1"):
        p = model.predict(tfidf.transform([clean_text("NASA confirms new findings about water ice on the lunar south pole surface")]))[0]
        st.success("✅ REAL News") if p == 1 else st.error("❌ FAKE News")

with ex2:
    st.markdown('<div style="background:#fff1f2;border:1px solid #fecdd3;border-radius:12px;padding:16px 20px;margin-bottom:10px;"><div style="font-size:11px;letter-spacing:1.5px;color:#dc2626;text-transform:uppercase;margin-bottom:6px;">Fake News Sample</div><p style="color:#374151;font-size:13px;line-height:1.5;margin:0;">"Government secretly putting microchips in vaccines to track the population."</p></div>', unsafe_allow_html=True)
    if st.button("▶ Test Fake Example", use_container_width=True, key="f1"):
        p = model.predict(tfidf.transform([clean_text("Government secretly putting microchips in vaccines to track the population")]))[0]
        st.error("❌ FAKE News") if p == 0 else st.success("✅ REAL News")

st.markdown("<br>", unsafe_allow_html=True)

# ── CONFUSION MATRIX ──
with st.expander("📊 Model Performance & Confusion Matrix"):
    import matplotlib.pyplot as plt
    import seaborn as sns

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#faf8f4')
        sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges',
                    xticklabels=['Fake','Real'], yticklabels=['Fake','Real'],
                    ax=ax, linewidths=0.5, linecolor='#e8ddd0',
                    annot_kws={"size":16, "color":"#1a1208"})
        ax.set_title('Confusion Matrix', color='#1a1208', fontsize=14, pad=14)
        ax.set_ylabel('Actual', color='#6b7280')
        ax.set_xlabel('Predicted', color='#6b7280')
        ax.tick_params(colors='#6b7280')
        for spine in ax.spines.values():
            spine.set_edgecolor('#e8ddd0')
        plt.tight_layout()
        st.pyplot(fig)

    with c2:
        st.markdown(f"""
        <div style="padding:10px 0;">
            <div style="margin-bottom:20px;">
                <div style="font-size:11px;letter-spacing:2px;color:#a89e94;text-transform:uppercase;margin-bottom:6px;">Overall Accuracy</div>
                <div style="font-family:'Playfair Display',serif;font-size:48px;color:#ea580c;font-weight:700;">{accuracy*100:.2f}%</div>
            </div>
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:14px 18px;margin-bottom:10px;">
                <div style="font-size:11px;color:#a89e94;margin-bottom:4px;">TRUE POSITIVES</div>
                <div style="font-size:22px;color:#16a34a;font-weight:600;">{cm[1][1]:,}</div>
            </div>
            <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:14px 18px;margin-bottom:10px;">
                <div style="font-size:11px;color:#a89e94;margin-bottom:4px;">TRUE NEGATIVES</div>
                <div style="font-size:22px;color:#2563eb;font-weight:600;">{cm[0][0]:,}</div>
            </div>
            <div style="background:#fff1f2;border:1px solid #fecdd3;border-radius:10px;padding:14px 18px;">
                <div style="font-size:11px;color:#a89e94;margin-bottom:4px;">MISCLASSIFIED</div>
                <div style="font-size:22px;color:#dc2626;font-weight:600;">{cm[0][1]+cm[1][0]:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)