import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- DARK SCI-FI STÍLUS ---
st.set_page_config(page_title="NEO-CORE UNDERGROUND v2", page_icon="💀", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #000000; color: #00ff00; }
    h1 { color: #00ff00 !important; font-family: 'Courier New', monospace; text-align: center; border-bottom: 2px solid #00ff00; }
    .stTextArea textarea { background-color: #050505 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .stFileUploader { border: 1px dashed #00ff00 !important; }
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
    st.error("SYSTEM OVERLOAD: Keress meg privátban.")
    st.markdown('<a href="https://revolut.me/konorp" class="revolut-button">ACCESS TOKEN (@konorp)</a>', unsafe_allow_html=True)
else:
    st.write("🛰️ *Képérzékelés optimalizálva. Nincs kártya.*")
    uploaded_file = st.file_uploader("ADATCSOMAG (KÉP)...", type=["jpg", "png", "jpeg"])
    user_query = st.text_area("FELADAT:", "Elemezd a csatolt képen látható matek feladatot és oldd meg magyarul!")

    if st.button("☣️ RENDSZER EXECUTE"):
        if not uploaded_file:
            st.warning("HIÁNYZÓ ADAT.")
        else:
            try:
                with st.spinner('Kép injektálása a neurális hálóba...'):
                    # KÉP OPTIMALIZÁLÁSA (hogy ne legyen túl nagy)
                    img = Image.open(uploaded_file)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Átméretezés, ha túl nagy, hogy az ingyenes szerver ne dobja el
                    img.thumbnail((800, 800)) 
                    
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=85)
                    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    # Új, stabilabb Pollinations végpont
                    url = "https://text.pollinations.ai/"
                    payload = {
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"FONTOS: A képen egy matek feladat van. Oldd meg pontosan és válaszolj magyarul! Kérdés: {user_query}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                                ]
                            }
                        ],
                        "model": "openai",
                        "private": True,
                        "seed": 42
                    }

                    response = requests.post(url, json=payload, timeout=60)

                    if response.status_code == 200 and len(response.text) > 50:
                        st.markdown("---")
                        st.success("🔓 ADATOK KINYERVE:")
                        st.write(response.text)
                        st.session_state.count += 1
                    else:
                        st.error("Az AI nem látja tisztán a képet. Próbáld meg közelebbről fotózni!")
                        
            except Exception as e:
                st.error(f"Hiba: {e}")