import base64
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.badges import badge
from streamlit_extras.mention import mention
from streamlit_extras.keyboard_text import key
from streamlit_extras.keyboard_text import load_key_css
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def main():
    img = get_img_as_base64("images2.jpg")
    img_2 = get_img_as_base64("water.jpg")

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
    st.markdown('<div class="title-text" style="text-align: center;">Servicio de predicción de estado psicológico</div>', unsafe_allow_html=True)
    st.sidebar.header("bienvenidos")
    
     # Personaliza el estilo del botón
   # Botón para "Comenzar análisis" con estilo personalizado
    
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
  margin: 200px auto 0;
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
    
    
    
    start_analysis_button = st.button("Comenzar análisis")

    # Si se presiona el botón, mostrar el contenido del análisis
    if start_analysis_button:
        analysis_page()

    row1 = st.columns(3)
    Celia = row1[1].container()
    Celia.markdown('<div class="title-text" style="text-align:left ; font-family: calibri; font-size: 30px; color: #FFFFFF;">Celia</div>', unsafe_allow_html=True)
    with Celia:
        mention(
        label="Linkedin",
        icon= "https://cdn-icons-png.flaticon.com/512/174/174857.png",
        url="https://www.linkedin.com/in/joel-de-andrade-175663152/",
    )
    joel = row1[2].container()
    joel.markdown('<div class="title-text" style="text-align: center;">Joel</div>', unsafe_allow_html=True)
    with joel:
        mention(
        label="Linkedin",
        icon= "https://cdn-icons-png.flaticon.com/512/174/174857.png",
        url="https://www.linkedin.com/in/joel-de-andrade-175663152/",
    )
    David = row1[0].container()
    David.markdown('<div class="title-text" style="text-align: center;">David</div>', unsafe_allow_html=True)
    with David:
        mention(
        label="Linkedin",
        icon= "https://cdn-icons-png.flaticon.com/512/174/174857.png",
        url="https://www.linkedin.com/in/joel-de-andrade-175663152/",
    )
    

    
    
    
def analysis_page():
    
    switch_page("predict_twitter")
   


   
   

if __name__ == "__main__":
 
    main()