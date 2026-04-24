import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SCI-FI DIZÁJN ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #64ffda; }
    h1, h2, h3 { color: #64ffda !important; text-shadow: 0 0 10px #64ffda77; font-family: 'Courier New', monospace; }
    .stTextArea textarea, .stFileUploader { background-color: #112240 !important; color: #e6f1ff !important; border: 1px solid #64ffda !important; border-radius: 10px; }
    .revolut-button { display: block; width: 100%; padding: 15px; background: transparent; color: #64ffda !important; border: 2px solid #64ffda; border-radius: 15px; text-decoration: none; text-align: center; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; box-shadow: 0 0 15px #64ffda44; }
    .revolut-button:hover { background: #64ffda; color: #0a192f !important; box-shadow: 0 0 30px #64ffda; }
    .stButton>button { background-color: #64ffda !important; color: #020c1b !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0

api_key = st.secrets.get("GEMINI_API_KEY")

st.title("🧬 NEO-CORE: A Barátságos AI")
st.write("### Üdvözöllek, Utazó! 🌌")

if st.session_state.count >= 1:
    st.error("⚡ Az ingyenes energiaforrás kimerült.")
    st.markdown(f'<a href="https://revolut.me/konorp" target="_blank" class="revolut-button">Energia küldése (Revolut @konorp)</a>', unsafe_allow_html=True)
else:
    uploaded_file = st.file_uploader("Szkenneld be a fájlt...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Miben segíthetek?", placeholder="Írj ide...")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not api_key:
            st.error("Rendszerhiba: Az API mag hiányzik a Secrets-ből!")
        elif not uploaded_file:
            st.warning("Kérlek, helyezz be egy vizuális mintát!")
        else:
            try:
                with st.spinner('Csatlakozás a hálózathoz...'):
                    genai.configure(api_key=api_key)
                    
                    # --- BIZTOSRA MENŐ MODELL VÁLASZTÁS ---
                    # Megpróbáljuk a legújabbat, ha nem megy, jön a stabil
                    model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro-vision']
                    
                    response = None
                    last_error = ""
                    
                    image = Image.open(uploaded_file)
                    
                    for m_name in model_names:
                        try:
                            model = genai.GenerativeModel(m_name)
                            response = model.generate_content([f"Te egy barátságos digitális társ vagy. {user_query}", image])
                            if response: break
                        except Exception as e:
                            last_error = str(e)
                            continue
                    
                    if response:
                        st.markdown("---")
                        st.subheader("🔮 Az elemzés eredménye:")
                        st.success(response.text)
                        st.session_state.count += 1
                        st.rerun()
                    else:
                        st.error(f"Sajnos egyik protokoll sem válaszolt. Hiba: {last_error}")
            except Exception as e:
                st.error(f"Váratlan hiba: {e}")