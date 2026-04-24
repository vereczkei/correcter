import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Beállítások - Itt adod meg a "szupererőt"
st.set_page_config(page_title="Univerzális Megoldó", page_icon="🧠")
st.title("🧠 Univerzális AI Megoldó")
st.write("Mutass neki bármit, és megoldja!")

# Ide kell majd a te API kulcsod
api_key = st.sidebar.text_input("Gemini API Kulcs", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Ez a leggyorsabb és "lát" is

    # 2. Bemenetek: Kép és Szöveg
    feltoltott_kep = st.file_uploader("Tölts fel egy képet (opcionális)", type=["jpg", "jpeg", "png"])
    kerdes = st.text_input("Mit kell megoldanom?", "Magyarázd el ezt nekem, mintha 5 éves lennék!")

    if st.button("Megoldás indítása 🚀"):
        with st.spinner("Gondolkodom..."):
            try:
                if feltoltott_kep:
                    # Ha van kép, azt is elküldjük
                    img = Image.open(feltoltott_kep)
                    valasz = model.generate_content([kerdes, img])
                else:
                    # Ha csak szöveg van
                    valasz = model.generate_content(kerdes)
                
                st.subheader("Az AI válasza:")
                st.write(valasz.text)
                
            except Exception as e:
                st.error(f"Hiba történt: {e}")
else:
    st.warning("Kérlek, add meg az API kulcsodat az oldalsávban a kezdéshez!")