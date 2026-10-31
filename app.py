import os
import streamlit as st
import base64
from openai import OpenAI
import openai
#from PIL import Image
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "
    
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."


# Streamlit
st.set_page_config(page_title='¿Adivinas qué dibujé?', page_icon='🎲')

# ------------------------------------------------------------------
# TEMA "¿ADIVINAS QUÉ DIBUJÉ?" (solo estilos CSS; la lógica y los inputs no cambian)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Nunito:wght@400;600;700&display=swap');

:root{
  --mesa:#f6f3ee;
  --punto:#e3ddd2;
  --violeta:#6c5ce7;
  --violeta-oscuro:#4a3db8;
  --violeta-claro:#ece9fd;
  --coral:#ffb4a2;
  --menta:#a8e6cf;
  --sol:#ffe08a;
  --tinta:#1f1d2b;
}

/* Fondo: mesa de juego con puntos suaves */
.stApp{
  background:
    radial-gradient(var(--punto) 1.5px, transparent 1.5px) 0 0 / 22px 22px,
    var(--mesa);
  background-attachment: fixed;
}
header[data-testid="stHeader"]{ background: transparent; }

/* Panel central: carta de juego */
[data-testid="stMainBlockContainer"], .block-container{
  background:#ffffff;
  border-radius:24px;
  border:3px solid var(--tinta);
  box-shadow:8px 8px 0 var(--violeta);
  margin-top:2rem;
  margin-bottom:4rem;
  padding:2rem 2.4rem 2.4rem !important;
  max-width:820px;
}
@media (max-width:640px){
  [data-testid="stMainBlockContainer"], .block-container{
    padding:1.4rem 1.1rem 1.8rem !important;
    box-shadow:5px 5px 0 var(--violeta);
  }
}

/* Encabezado */
.juego-tag{
  display:inline-block;
  font-family:'Nunito', sans-serif;
  font-weight:700; font-size:.8rem; letter-spacing:.12em; text-transform:uppercase;
  color:var(--violeta-oscuro);
  background:var(--violeta-claro);
  padding:.3rem .8rem; border-radius:999px;
}
.juego-title{
  font-family:'Fredoka', sans-serif;
  font-weight:700; font-size:2.8rem; line-height:1.05;
  color:var(--tinta);
  margin:.7rem 0 .5rem;
}
.juego-title span{ color:var(--violeta); }
.juego-sub{
  font-family:'Nunito', sans-serif;
  font-size:1.1rem; line-height:1.55;
  color:#4a4858;
}
.juego-pasos{ display:flex; flex-wrap:wrap; gap:.7rem; margin:1.2rem 0 .6rem; }
.juego-paso{
  flex:1 1 150px;
  border:2px solid var(--tinta);
  border-radius:14px;
  padding:.7rem .9rem;
  font-family:'Nunito', sans-serif; font-weight:700; font-size:.98rem;
  color:var(--tinta);
}
.juego-paso b{
  display:block;
  font-family:'Fredoka', sans-serif; font-size:1.5rem; line-height:1;
  margin-bottom:.25rem;
}
.juego-paso:nth-child(1){ background:var(--sol); }
.juego-paso:nth-child(2){ background:var(--menta); }
.juego-paso:nth-child(3){ background:var(--coral); }
@media (max-width:640px){
  .juego-title{ font-size:2.1rem; }
}

/* Títulos y textos del contenido */
h2, h3{
  font-family:'Fredoka', sans-serif !important;
  font-weight:700 !important;
  color:var(--tinta) !important;
}
h1 a, h2 a, h3 a{ display:none !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{
  font-family:'Nunito', sans-serif;
  line-height:1.6;
}

/* Barra lateral: violeta muy suave */
section[data-testid="stSidebar"]{
  background:var(--violeta-claro);
  border-right:3px solid var(--tinta);
}
section[data-testid="stSidebar"] h3{ font-size:1.1rem !important; }

/* Textos sobre fondos claros: siempre en negro (también si Streamlit usa el tema oscuro) */
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="caption"],
.stApp [data-testid="stSliderThumbValue"],
.stApp [data-testid="stSliderTickBarMin"],
.stApp [data-testid="stSliderTickBarMax"],
.stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] *{
  color:#1a1a1a !important;
}

/* Botones: conservan los colores originales de Streamlit (contraste) */
.stApp button [data-testid="stMarkdownContainer"],
.stApp button [data-testid="stMarkdownContainer"] *,
.stApp button [data-testid="stMarkdownContainer"] p{
  color:inherit !important;
  font-family:inherit !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<span class="juego-tag">🎲 Juego de dibujo con IA</span>
<div class="juego-title">¿Adivinas qué <span>dibujé</span>?</div>
<div class="juego-sub">Dibuja lo que quieras y reta a la inteligencia artificial: ¿será capaz de descubrir qué es?</div>
<div class="juego-pasos">
  <div class="juego-paso"><b>1</b>Dibuja algo en el tablero</div>
  <div class="juego-paso"><b>2</b>Pulsa «¡Adivina!»</div>
  <div class="juego-paso"><b>3</b>¿Acertó la IA?</div>
</div>
""", unsafe_allow_html=True)
with st.sidebar:
    st.subheader("🎲 Cómo se juega")
    st.subheader("Dibuja algo en el tablero y la IA intentará adivinar qué es. ¡Pon a prueba sus ojos!")
st.subheader("✏️ Tu turno: dibuja algo")

# Add canvas component
#bg_image = st.sidebar.file_uploader("Cargar Imagen:", type=["png", "jpg"])
# Specify canvas parameters in application
with st.sidebar:
    st.subheader("🎨 Tu tablero")

    # Canvas dimensions (moved to the top)
    st.subheader("📏 Tamaño")
    canvas_width = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero", 200, 600, 300, 50)

    # Drawing mode selector
    drawing_mode = st.selectbox(
        "✏️ Herramienta de dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    # Stroke width slider
    stroke_width = st.slider('Grosor del trazo', 1, 30, 15)

    # Stroke color picker
    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")

    # Background color
    bg_color = st.color_picker("Color de fondo", "#000000")


# Create a canvas component with dynamic key
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    #background_image= None #Image.open(bg_image) if bg_image else None,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",  # Dynamic key based on dimensions
)

ke = st.text_input('🔑 Ingresa tu clave de OpenAI')
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = ke


# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

analyze_button = st.button("🎲 ¡Adivina!", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("🤔 La IA está pensando qué dibujaste..."):
        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')
        
      # Codificar la imagen en base64
 
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = (f"Describe the image in spanish")
    
      # Create the payload for the completion request
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url":f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]
    
        # Make the request to the OpenAI API
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model= "gpt-4o-mini",  #o1-preview ,gpt-4o-mini
              messages=[
                {
                   "role": "user",
                   "content": [
                     {"type": "text", "text": prompt_text},
                     {
                       "type": "image_url",
                       "image_url": {
                         "url": f"data:image/png;base64,{base64_image}",
                       },
                     },
                   ],
                  }
                ],
              max_tokens=500,
              )
            #response.choices[0].message.content
            if response.choices[0].message.content is not None:
                    full_response += response.choices[0].message.content
                    message_placeholder.markdown(full_response + "▌")
            # Final update to placeholder after the stream ends
            message_placeholder.markdown(full_response)
            if Expert== profile_imgenh:
               st.session_state.mi_respuesta= response.choices[0].message.content #full_response 
    
            # Display the response in the app
            #st.write(response.choices[0])
        except Exception as e:
            st.error(f"Ups, la IA no pudo adivinar esta vez: {e}")
else:
    # Warnings for user action required

    if not api_key:
        st.warning("🔑 Ingresa tu clave de OpenAI para empezar a jugar.")
