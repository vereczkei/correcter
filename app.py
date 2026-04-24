import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. SCI-FI DIZÁJN KONFIGURÁCIÓ ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #64ffda; }
    h1, h2, h3 { color: #64ffda !important; text-shadow: 0 0 10px #64ffda77; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #112240 !important; color: #e6f1ff !important; border: 1px solid #64ffda !important; border-radius: 10px; }
    .revolut-button { 
        display: block; width: 100%; padding: 15px; background: transparent; 
        color: #64ffda !important; border: 2px solid #64ffda; border-radius: 15px; 
        text-decoration: none; text-align: center; font-weight: bold; text-transform: uppercase;
        box-shadow: 0 0 15px #64ffda44; margin-top: 20px;
    }
    .revolut-button:hover { background: #64ffda; color: #0a192f !important; box-shadow: 0 0 30px #64ffda; }
    .stButton>button { background-color: #64ffda !important; color: #020c1b !important; font-weight: bold !important; width: 100%; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA ---
if 'count' not in st.session_state:
    st.session_state.count = 0

api_key = st.secrets.get("GEMINI_API_KEY")

st.title("🧬 NEO-CORE: A Barátságos AI")

# Fizetési fal
if st.session_state.count >= 1:
    st.error("⚡ Az ingyenes energiaforrás kimerült.")
    st.markdown(f'<a href="https://revolut.me/konorp" target="_blank" class="revolut-button">Energia küldése (Revolut @konorp)</a>', unsafe_allow_html=True)
    if st.button("Visszaállítás bizonylat után"):
        st.info("Küldd el a képernyőfotót privátban!")
else:
    st.write("### Üdvözöllek, Utazó! 🌌")
    uploaded_file = st.file_uploader("Szkennelj be egy mintát...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Miben segíthetek?", placeholder="Írd le a kérdésed...")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not api_key:
            st.error("Hiba: API kulcs nem található a rendszerben!")
        elif not uploaded_file:
            st.warning("Kérlek, tölts fel egy képet!")
        else:
            try:
                with st.spinner('Neurális kapcsolat felépítése...'):
                    genai.configure(api_key=api_key)
                    
                    # LISTA AZ ÖSSZES LEHETSÉGES MODELLNÉVRŐL (Biztonsági háló)
                    possible_models = [
                        'gemini-1.5-flash',
                        'gemini-1.5-flash-latest',
                        'gemini-1.5-pro',
                        'models/gemini-1.5-flash',
                        'models/gemini-1.0-pro-vision-latest'
                    ]
                    
                    image = Image.open(uploaded_file)
                    success = False
                    
                    for model_name in possible_models:
                        try:
                            model = genai.GenerativeModel(model_name)
                            response = model.generate_content([f"Légy barátságos segítő. Kérdés: {user_query}", image])
                            
                            if response:
                                st.markdown("---")
                                st.subheader("🔮 Az elemzés eredménye:")
                                st.success(response.text)
                                st.session_state.count += 1
                                success = True
                                break # Ha sikerült, kilépünk a ciklusból
                        except Exception as e:
                            continue # Ha hiba, próbáljuk a következőt
                    
                    if success:
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("A Google szerverei jelenleg egyik protokollon sem érhetők el. Próbáld meg egy új API kulccsal az AI Studio-ból!")
                        
            except Exception as e:
                st.error(f"Váratlan rendszerhiba: {str(e)}")