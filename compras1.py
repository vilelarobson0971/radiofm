import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# Configuração da página para mobile
st.set_page_config(
    page_title="Bob Rádios Online",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado com otimizações mobile - CORRIGIDO O CONTRASTE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Título "Selecione sua rádio" com cor fixa */
    h3 {
        color: #333333 !important; /* Cor escura fixa para bom contraste */
    }
    
    /* Botões maiores para touch */
    .stButton>button {
        width: 100% !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
    }
    
    .radio-card {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        background: white;
    }
    
    .radio-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    .now-playing {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .footer {
        text-align: center;
        padding: 15px;
        margin-top: 30px;
        background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        border-radius: 10px;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        /* Ajustes para telas pequenas */
        .css-1v0mbdj {
            width: 100% !important;
        }
        .stAudio {
            width: 100% !important;
        }
        
        /* Garantindo contraste no mobile */
        h3, .stMarkdown h3 {
            color: #333333 !important;
            font-weight: bold !important;
        }
    }
    </style>
    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

def main():
    # Cabeçalho com gradiente (mantido igual)
    with stylable_container(
        key="header",
        css_styles="""
            {
                background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
                border-radius: 10px;
                padding: 20px;
                color: white;
                text-align: center;
                margin-bottom: 30px;
            }
        """
    ):
        st.markdown("<h1 style='text-align: center; margin: 0; font-size: 2rem;'>🎧 BOB RÁDIOS ONLINE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin: 0; font-size: 1rem;'>Toque sua música favorita no carro ou onde estiver!</p>", unsafe_allow_html=True)
    
    # [Restante do código permanece igual...]
    # ... (o dicionário de rádios, container principal, etc.)
    
    # MODIFICAÇÃO ESPECÍFICA NO TÍTULO PROBLEMÁTICO:
    # Substitua a linha original do subtítulo por:
    st.markdown("<h3 style='text-align: center; color: #333333;'>📻 Selecione sua rádio</h3>", unsafe_allow_html=True)
    
    # [Restante do código continua igual...]

if __name__ == "__main__":
    main()
