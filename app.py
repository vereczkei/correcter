import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. SCI-FI DIZÁJN ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #64ffda; }
    h1, h2, h3 { color: #64ffda !important; text-shadow: 0 0 10px #64ffda77; font-family: 'Courier New', monospace; }
    .stTextArea textarea, .stFileUploader { background-color: #112240 !important; color: #e6f1ff !important; border: 1px solid #64ffda !important; border-radius: 10px; }
    .revolut-button { 
        display: block; width: 100%; padding: 15px; background: transparent; 
        color: #64ffda !important; border: 2px solid #64ffda; border-radius: 15px; 
        text-decoration: none; text-align: center; font-weight: bold; text-transform: uppercase;
        letter-spacing: 2px; transition: 0.3s; box-shadow: 0 0 15px #64ffda44; margin-top: 20px;
    }
    .revolut-button:hover { background: #64ffda; color: #0a192f !important; box-shadow: 0 0 30px #64ffda; }
    .stButton>button { background-color: #64ffda !important; color: #020c1b !important; font-weight: bold !important; width: 100%; border-radius: 10px !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0

# Groq API kulcs (gsk_...)
api_key = st.secrets.get("GEMINI_API_KEY")

st.title("🧬 NEO-CORE: A Barátságos AI")

if st.session_state.count >= 1:
    st.error("⚡ Az ingyenes energiaforrás kimerült.")
    st.markdown(f'<a href="https://revolut.me/konorp" target="_blank" class="revolut-button">Energia küldése (Revolut @konorp)</a>', unsafe_allow_html=True)
else:
    st.write("### Üdvözöllek az interfészen, Utazó! 🌌")
    uploaded_file = st.file_uploader("Szkenneld be a képet...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Miben segíthetek?", placeholder="Írj ide...")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not api_key:
            st.error("Rendszerhiba: Az API kulcs hiányzik a Secrets-ből!")
        elif not uploaded_file:
            st.warning("Kérlek, tölts fel egy képet!")
        else:
            try:
                with st.spinner('Kapcsolódás az élő hálózathoz...'):
                    client = Groq(api_key=api_key)
                    image_bytes = uploaded_file.getvalue()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')

                    # A 2026-ban aktuális, stabil Groq Vision modellek
                    models_to_try = [
                        "llama-3.2-11b-vision-instant",
                        "llama-3.2-90b-vision-instant",
                        "llama-3.2-11b-vision-preview",
                        "llama-3.2-90b-vision-preview"
                    ]
                    
                    response_text = None
                    
                    for model_id in models_to_try:
                        try:
                            completion = client.chat.completions.create(
                                model=model_id,
                                messages=[{
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": f"Te egy barátságos AI vagy. Válaszolj magyarul: {user_query}"},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                    ]
                                }]
                            )
                            response_text = completion.choices[0].message.content
                            if response_text: break
                        except:
                            continue

                    if response_text:
                        st.markdown("---")
                        st.subheader("🔮 Az elemzés eredménye:")
                        st.success(response_text)
                        st.session_state.count += 1
                        st.rerun()
                    else:
                        st.error("A szolgáltató minden Vision modellt lekapcsolt az ingyenes fiókodban. Kérlek, nézz rá a Groq Console-ra!")
            except Exception as e:
                st.error(f"Rendszerhiba: {str(e)}")