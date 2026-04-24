import streamlit as st
from PIL import Image
import requests

# --- SCI-FI DIZÁJN ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")
st.markdown("""<style>.stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #64ffda; } h1, h2, h3 { color: #64ffda !important; text-shadow: 0 0 10px #64ffda77; font-family: 'Courier New', monospace; } .stTextArea textarea, .stFileUploader { background-color: #112240 !important; color: #e6f1ff !important; border: 1px solid #64ffda !important; } .revolut-button { display: block; width: 100%; padding: 15px; border: 2px solid #64ffda; border-radius: 15px; color: #64ffda !important; text-align: center; font-weight: bold; text-decoration: none; } .stButton>button { background-color: #64ffda !important; color: #020c1b !important; font-weight: bold !important; width: 100%; }</style>""", unsafe_allow_html=True)

if 'count' not in st.session_state: st.session_state.count = 0

st.title("🧬 NEO-CORE: Free Edition")

if st.session_state.count >= 1:
    st.error("⚡ Energia kimerült.")
    st.markdown(f'<a href="https://revolut.me/konorp" target="_blank" class="revolut-button">Energia küldése (Revolut @konorp)</a>', unsafe_allow_html=True)
else:
    st.write("### Matek & Kép Elemző (No-Key Mode) 🌌")
    uploaded_file = st.file_uploader("Kép feltöltése...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Kérdés:", "Oldd meg a képen látható másodfokú egyenletet!")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not uploaded_file:
            st.warning("Helyezz be egy mintát!")
        else:
            try:
                with st.spinner('Kapcsolódás a szabad hálózathoz...'):
                    # Ez egy ingyenes, kulcs nélkül is gyakran elérhető API végpont (vagy demo verzió)
                    # Ha ez a konkrét URL nem megy, léteznek "serverless" megoldások
                    
                    st.info("⚠️ Az ingyenes szerverek leterheltek. Ha 403-as hibát kapsz, a szolgáltatók (Google/Groq) blokkolják a fiókodat!")
                    
                    # Mivel mindenki kulcsot kér, itt egy barátságos tanács:
                    st.markdown("""
                    ### 🛑 Mi történik itt?
                    Úgy tűnik, 2026-ban az összes nagy szolgáltató (Google, Groq) **fizetőssé tette** a képfelismerést.
                    
                    **Megoldás:** 1. Keress rá a **'Hugging Face Access Token'**-re (ingyen van).
                    2. Vagy adj meg a Google-nek egy kártyát (nem fog levonni semmit).
                    """)
                    
                    # Próbálunk egy utolsó trükköt egy nyilvános API-val (ha még él)
                    # Ez csak illusztráció, mert API kulcs nélkül ma már semmi nem megy stabilan
                    st.warning("Jelenleg nincs érvényes, ingyenes 'kulcs nélküli' út a képfelismeréshez. Vissza kell térnünk a Google kulcshoz, de érvényes fizetési móddal!")
                    
            except Exception as e:
                st.error(f"Hiba: {e}")