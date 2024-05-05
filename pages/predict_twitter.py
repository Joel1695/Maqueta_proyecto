import base64
import streamlit as st
import pandas as pd
from utils import obtener_datos_desde_api
from streamlit_extras.badges import badge
from streamlit_extras.mention import mention
from streamlit_extras.keyboard_text import key
from streamlit_extras.keyboard_text import load_key_css
from markdownlit import mdlit


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img_2 = get_img_as_base64("water.jpg")
img = get_img_as_base64("image3.jpg")

page_bg_img = f"""
    <style>
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{img}");
            background-position: center; 
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{img_2}");
            background-position: center; 
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover
}}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stToolbar"] {{
            right: 2rem;
        }}

        .stMarkdown {{
            color: white !important;
            font-size: 40px;
        }}
    </style>
    """

st.markdown(page_bg_img, unsafe_allow_html=True)
# Título de la aplicación
st.markdown('<div class="title-text" style="text-align: center;">Servicio de predicción de estado psicológico</div>', unsafe_allow_html=True)
st.image('amigas.jpeg', caption='Te ayudamos a cuidar de los tuyos ', use_column_width=True)

enlace = st.text_input("Ingrese el enlace para obtener datos")

st.markdown(
        """
    <style>
.stButton>button {
  background: #48C9B0; /* color de fondo */
  color: #1ABC9C; /* color de fuente */
  border: 2px solid #1ABC9C; /* tamaño y color de borde */
  padding: 16px 20px;
  border-radius: 10px; /* redondear bordes */
  position: relative;
  z-index: 1;
  overflow: hidden;
  display: block;
  margin:auto;
  transition: background-color 0.3s ease;
}
.stButton>button {
  background: darken(#48C9B0, 10%);
  color: #fff; /* color de fuente hover */
}
.stButton>button::after {
  content: "";
  background: #1ABC9C; /* color de fondo hover */
  position: absolute;
  z-index: -1;
  padding: 16px 20px;
  display: block;
  top: 0;
  bottom: 0;
  left: -100%;
  right: 100%;
  -webkit-transition: all 0.35s;
  transition: all 0.35s;
}
.stButton>button:hover::after {
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  -webkit-transition: all 0.35s;
  transition: all 0.35s;
}
    </style>
    """,
        unsafe_allow_html=True,
    )



if st.button("Obtener datos y hacer predicción"):
    if enlace:
        # Obtener datos desde la API
        datos = obtener_datos_desde_api(enlace)
        
        # Verificar si se obtuvieron datos
        if datos is not None:
            # Hacer la predicción con el modelo
            resultado_prediccion = datos
            st.write("Resultado de la predicción:")
            if resultado_prediccion == 1 :
                st.write(f'segun nuestro modelo esta persona tienen posibilidades de sufrir algun transtorno mental')
            elif resultado_prediccion == 0:
                st.write(f'Segun nuestro modelo esta persona no indica tener algun transtorno mental')    
            
            st.warning("ALERTA!!! sin importar el resultado de la app le recomendamos que si tienen algun duda de si una persona puede o no tener algun desorden mental visite a un profecional para un correcto diagnostico")
        else:
            st.warning("No se pudieron obtener datos de la API")
    else:
        st.warning("Por favor ingrese un enlace válido")



