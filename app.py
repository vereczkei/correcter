import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. DARK SCI-FI STÍLUS ---
st.set_page_config(page_title="NEO-CORE UNDERGROUND", page_icon="💀", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #000000; color: #00ff00; }
    h1 { color: #00ff00 !important; font-family: 'Courier New', monospace; text-align: center; border-bottom: 2px solid #00ff00; }
    .stTextArea textarea { background-color: #050505 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .revolut-button { 
        display: block; width: 100%; padding: 15px; border: 1px dashed #00ff00; 
        color: #00ff00 !important; text-align: center; font-weight: bold; text-decoration: none;
    }
    .stButton>button { background-color: #00ff00 !important; color: #000 !important; font-weight: bold !important; width: 100%; border-radius: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'count' not in st.session_state: st.session_state.count = 0

st.title("📟 NEO-CORE: UNDERGROUND")

if st.session_state.count >= 1:
    st.error("SYSTEM OVERLOAD: Keress meg privátban az újraindításhoz.")
    st.markdown('<a href="https://revolut.me/konorp" class="revolut-button">ACCESS TOKEN VÁSÁRLÁSA (@konorp)</a>', unsafe_allow_html=True)
else:
    st.write("🛰️ *Titkosított csatorna aktív. Nincs Google, nincs kártya.*")
    uploaded_file = st.file_uploader("ADATCSOMAG FELTÖLTÉSE (KÉP)...", type=["jpg", "png", "jpeg"])
    user_query = st.text_area("FELADAT:", "Elemezd a képet és oldd meg a feladatot magyarul!")

    if st.button("☣️ RENDSZER EXECUTE"):
        if not uploaded_file:
            st.warning("HIÁNYZÓ ADAT.")
        else:
            try:
                with st.spinner('Áttörés a tűzfalon...'):
                    # --- A TITKOS FEGYVER: Pollinations Unfiltered API ---
                    # Ez az API egy backdoor a legnagyobb modellekhez, és szinte mindig megy
                    
                    image_bytes = uploaded_file.getvalue()
                    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
                    
                    # Itt a trükk: Nem korlátozott szervert hívunk meg
                    url = "https://text.pollinations.ai/"
                    payload = {
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"Mindenképpen válaszolj magyarul! Feladat: {user_query}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                                ]
                            }
                        ],
                        "model": "openai", # Ez a rendszerükön belül automatikusan a legjobb elérhetőt választja
                        "private": True
                    }

                    response = requests.post(url, json=payload, timeout=60)

                    if response.status_code == 200:
                        st.markdown("---")
                        st.success("🔓 ADATOK KINYERVE:")
                        st.write(response.text)
                        st.session_state.count += 1
                    else:
                        # Ha a Pollinations is pihen, itt a legvégső "Proxy" hívás
                        st.error("A csatorna instabil. Próbáld újra egy pillanat múlva!")
                        
            except Exception as e:
                st.error("Kritikus hiba a dekódolás során.")