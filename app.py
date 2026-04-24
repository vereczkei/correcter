import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SCI-FI DIZÁJN ÉS KONFIGURÁCIÓ ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")

# CSS a barátságos Matrix/Sci-fi hangulathoz
st.markdown("""
    <style>
    /* Fő háttér és szöveg */
    .stApp {
        background: radial-gradient(circle, #0a192f 0%, #020c1b 100%);
        color: #64ffda;
    }
    
    /* Címek stílusa */
    h1, h2, h3 {
        color: #64ffda !important;
        text-shadow: 0 0 10px #64ffda77;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Kártyák és beviteli mezők */
    .stTextArea textarea, .stFileUploader {
        background-color: #112240 !important;
        color: #e6f1ff !important;
        border: 1px solid #64ffda !important;
        border-radius: 10px;
    }

    /* A Revolut gomb - neon stílusban */
    .revolut-button {
        display: block;
        width: 100%;
        padding: 15px;
        background: transparent;
        color: #64ffda !important;
        border: 2px solid #64ffda;
        border-radius: 15px;
        text-decoration: none;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s;
        box-shadow: 0 0 15px #64ffda44;
    }
    .revolut-button:hover {
        background: #64ffda;
        color: #0a192f !important;
        box-shadow: 0 0 30px #64ffda;
    }

    /* Egyedi gomb stílus */
    .stButton>button {
        background-color: #64ffda !important;
        color: #020c1b !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 0 10px #64ffda55;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA ---
if 'count' not in st.session_state:
    st.session_state.count = 0

api_key = st.secrets.get("GEMINI_API_KEY")

# --- FELÜLET ---
st.title("🧬 NEO-CORE: A Barátságos AI")
st.write("### Üdvözöllek az interfészen, Utazó! 🌌")
st.write("Tölts fel egy darabkát a valóságból (kép), és én segítek értelmezni azt.")

if st.session_state.count >= 1:
    st.markdown("---")
    st.markdown("### ⚡ Az ingyenes energiaforrás kimerült")
    st.write("Ahhoz, hogy a kapcsolatot fenntartsuk a mátrixszal, egy kis támogatásra van szükségem.")
    
    st.markdown(f"""
        <a href="https://revolut.me/konorp" target="_blank" class="revolut-button">
            Energia küldése (Revolut @konorp)
        </a>
    """, unsafe_allow_html=True)
    
    st.info("Miután átküldted a támogatást, küldj egy üzenetet, és feloldom a végtelen módot! 🚀")
else:
    st.markdown(f"**Rendszerállapot:** 1 szabad elemzés elérhető.")
    
    uploaded_file = st.file_uploader("Szkenneld be a fájlt...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Miben segíthetek neked?", placeholder="Írj ide bátran, figyelmesen hallgatlak...")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not api_key:
            st.error("Rendszerhiba: Az API mag hiányzik.")
        elif not uploaded_file:
            st.warning("Kérlek, helyezz be egy vizuális mintát!")
        else:
            try:
                with st.spinner('Kapcsolódás a neurális hálózathoz...'):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    image = Image.open(uploaded_file)
                    
                    # Itt adunk neki egy "barátságos" stílust a háttérben
                    prompt = f"Te egy barátságos, segítőkész digitális társ vagy. Válaszolj erre a kérésre: {user_query}"
                    response = model.generate_content([prompt, image])
                    
                    st.markdown("---")
                    st.subheader("🔮 Az elemzés eredménye:")
                    st.success(response.text)
                    
                    st.session_state.count += 1
                    st.rerun()
            except Exception as e:
                st.error(f"Hiba az adatfolyamban: {e}")