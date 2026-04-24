import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SCI-FI DIZÁJN ÉS KONFIGURÁCIÓ ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")

st.markdown("""
    <style>
    /* Sötét sci-fi háttér */
    .stApp {
        background: radial-gradient(circle, #0a192f 0%, #020c1b 100%);
        color: #64ffda;
    }
    
    /* Neon zöld címek */
    h1, h2, h3 {
        color: #64ffda !important;
        text-shadow: 0 0 10px #64ffda77;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Beviteli mezők stílusa */
    .stTextArea textarea {
        background-color: #112240 !important;
        color: #e6f1ff !important;
        border: 1px solid #64ffda !important;
    }

    /* A Revolut gomb neon stílusban */
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
        transition: 0.3s;
        box-shadow: 0 0 15px #64ffda44;
    }
    .revolut-button:hover {
        background: #64ffda;
        color: #0a192f !important;
        box-shadow: 0 0 30px #64ffda;
    }

    /* Gomb stílusa */
    .stButton>button {
        background-color: #64ffda !important;
        color: #020c1b !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA ÉS SZÁMLÁLÓ ---
if 'count' not in st.session_state:
    st.session_state.count = 0

# API Kulcs behúzása a Secrets-ből
api_key = st.secrets.get("GEMINI_API_KEY")

# --- 3. FELÜLET ---
st.title("🧬 NEO-CORE: A Barátságos AI")

# Fizetési fal ellenőrzése
if st.session_state.count >= 1:
    st.markdown("---")
    st.error("⚡ Az ingyenes energiaforrás kimerült.")
    st.write("A rendszer fenntartásához küldj egy kis támogatást a Revoluton!")
    
    st.markdown(f"""
        <a href="https://revolut.me/konorp" target="_blank" class="revolut-button">
            Energia küldése (Revolut @konorp)
        </a>
    """, unsafe_allow_html=True)
    
    if st.button("Visszaállítást kérek (Bizonylat után)"):
        st.info("Küldd el a képernyőfotót a bizonylatról privátban!")
else:
    st.write("### Üdvözöllek az interfészen, Utazó! 🌌")
    st.info("Rendszerállapot: 1 szabad elemzés elérhető.")
    
    uploaded_file = st.file_uploader("Szkenneld be a képet (JPG, PNG)...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Miben segíthetek?", placeholder="Pl. Oldd meg ezt az egyenletet...")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not api_key:
            st.error("Rendszerhiba: Az API kulcs hiányzik a Secrets-ből!")
        elif not uploaded_file:
            st.warning("Kérlek, tölts fel egy képet!")
        else:
            try:
                with st.spinner('Kapcsolódás a neurális hálózathoz...'):
                    # API Konfiguráció
                    genai.configure(api_key=api_key)
                    
                    # A legstabilabb modell hívása
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Kép előkészítése
                    image = Image.open(uploaded_file)
                    
                    # Generálás
                    prompt = f"Te egy barátságos, tudományos stílusú digitális társ vagy. Válaszolj erre: {user_query}"
                    response = model.generate_content([prompt, image])
                    
                    # Eredmény megjelenítése
                    st.markdown("---")
                    st.subheader("🔮 Az elemzés eredménye:")
                    st.success(response.text)
                    
                    # Számláló növelése és frissítés
                    st.session_state.count += 1
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Hiba történt az adatfolyamban: {str(e)}")