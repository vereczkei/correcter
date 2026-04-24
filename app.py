import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- SCI-FI DIZÁJN ---
st.set_page_config(page_title="NEO-CORE FREE", page_icon="🧬", layout="centered")
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #64ffda; }
    h1, h2 { color: #64ffda !important; text-shadow: 0 0 10px #64ffda77; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #112240 !important; color: #e6f1ff !important; border: 1px solid #64ffda !important; }
    .revolut-button { display: block; width: 100%; padding: 15px; border: 2px solid #64ffda; border-radius: 15px; color: #64ffda !important; text-align: center; font-weight: bold; text-decoration: none; }
    .stButton>button { background-color: #64ffda !important; color: #020c1b !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

if 'count' not in st.session_state: st.session_state.count = 0

st.title("🧬 NEO-CORE: GERILLA AI")

if st.session_state.count >= 1:
    st.error("⚡ Energia kimerült. Támogasd a rendszert, ha tetszett!")
    st.markdown(f'<a href="https://revolut.me/konorp" target="_blank" class="revolut-button">Támogatás (Revolut @konorp)</a>', unsafe_allow_html=True)
else:
    st.write("### Kártya nélkül, szabadon. 🌌")
    uploaded_file = st.file_uploader("Kép feltöltése...", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Kérdés:", "Oldd meg a képen látható feladatot!")

    if st.button("👁️ ELEMZÉS INDÍTÁSA"):
        if not uploaded_file:
            st.warning("Kép nélkül nem megy!")
        else:
            try:
                with st.spinner('Csatlakozás a közösségi szerverekhez...'):
                    # Ez egy ingyenes, kulcs nélküli API (vagy egy demo hívás)
                    # Itt a Moondream modellt használjuk, ami kicsi és ingyenes
                    
                    img = Image.open(uploaded_file)
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    # Ingyenes API hívás (Moondream API demo)
                    response = requests.post(
                        "https://moondream-ai-moondream2.hf.space/run/predict",
                        json={
                            "data": [
                                f"data:image/jpeg;base64,{img_str}",
                                user_query
                            ]
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        res = response.json()
                        st.markdown("---")
                        st.subheader("🔮 Megoldás:")
                        st.success(res["data"][0])
                        st.session_state.count += 1
                        st.rerun()
                    else:
                        st.error("A szabad szerver épp túlterhelt. Próbáld meg 1 perc múlva!")
                        
            except Exception as e:
                st.info("A szerver épp pihen. De legalább nem kért kártyát! Próbáld meg később.")