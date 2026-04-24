import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- DIZÁJN (Matrix stílus marad) ---
st.set_page_config(page_title="NEO-CORE AI", page_icon="🧬", layout="centered")
st.markdown("""<style>.stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #64ffda; } h1, h2, h3 { color: #64ffda !important; text-shadow: 0 0 10px #64ffda77; font-family: 'Courier New', monospace; } .stTextArea textarea { background-color: #112240 !important; color: #e6f1ff !important; border: 1px solid #64ffda !important; } .revolut-button { display: block; width: 100%; padding: 15px; border: 2px solid #64ffda; border-radius: 15px; color: #64ffda !important; text-decoration: none; text-align: center; font-weight: bold; } .stButton>button { background-color: #64ffda !important; color: #020c1b !important; font-weight: bold !important; width: 100%; }</style>""", unsafe_allow_html=True)

if 'count' not in st.session_state: st.session_state.count = 0

# Itt a Secrets-ben a nevet hagyd GEMINI_API_KEY-nek, csak a tartalmat cseréld a gsk_... kulcsra!
api_key = st.secrets.get("GEMINI_API_KEY")

st.title("🧬 NEO-CORE: Groq Edition")

if st.session_state.count >= 1:
    st.error("⚡ Energia kimerült.")
    st.markdown(f'<a href="https://revolut.me/konorp" target="_blank" class="revolut-button">Energia küldése (Revolut @konorp)</a>', unsafe_allow_html=True)
else:
    uploaded_file = st.file_uploader("Kép feltöltése...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Kérdésed:", placeholder="Pl. Mi van a képen?")

    if st.button("👁️ ANALÍZIS INDÍTÁSA"):
        if not api_key: st.error("Hiányzik a Groq API kulcs!")
        elif not uploaded_file: st.warning("Tölts fel egy képet!")
        else:
            try:
                with st.spinner('Neurális kapcsolat a Groq hálózattal...'):
                    client = Groq(api_key=api_key)
                    
                    # Kép kódolása Base64-be
                    image_bytes = uploaded_file.getvalue()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')

                    # Llama 3.2 Vision hívása (ez ingyenes és tud képet!)
                    completion = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Légy barátságos digitális társ. Válaszolj magyarul: {user_query}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }]
                    )
                    
                    st.success(completion.choices[0].message.content)
                    st.session_state.count += 1
                    st.rerun()
            except Exception as e:
                st.error(f"Hiba történt: {str(e)}")