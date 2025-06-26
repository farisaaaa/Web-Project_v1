# --- app.py (utama)
import streamlit as st

st.set_page_config(page_title="Optimasi Rute", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1976d2;
        letter-spacing: 1px;
        margin-bottom: 0.2em;
    }
    .subtitle-box {
        background: linear-gradient(90deg, #e3f2fd 60%, #bbdefb 100%);
        border-radius: 12px;
        padding: 24px 32px 18px 32px;
        margin-bottom: 1.5em;
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.07);
    }
    .subtitle-box h4 {
        color: #1565c0;
        margin-bottom: 0.7em;
    }
    .subtitle-box ul {
        font-size: 1.1rem;
        color: #333;
        margin-left: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🚚 Dashboard Optimasi Rute Logistik</div>', unsafe_allow_html=True)
st.markdown("---")

st.markdown(
    """
    <div class="subtitle-box">
        <h4>Selamat datang di dashboard optimasi rute logistik berbasis Streamlit!</h4>
        <ul>
            <li><b>Input Pengiriman & Rekomendasi:</b> Tambahkan data pengiriman dan dapatkan rute optimal.</li>
            <li><b>Visualisasi Data:</b> Lihat insight distribusi dan performa logistik secara interaktif.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("Gunakan menu di sidebar untuk navigasi halaman.", icon="🧭")
