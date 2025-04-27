import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# Configuração da página
st.set_page_config(
    page_title="Neuros Som",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado com botões 3D
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Corrigindo o fundo */
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    }
    
    /* Forçar cor amarela no título principal */
    .neuros-title h1 {
        color: #FFFF00 !important;
        text-align: center;
        margin: 0;
    }
    
    /* Sobrescrever especificamente o título do Streamlit */
    h1[data-testid="stMarkdownContainer"] {
        color: #FFFF00 !important;
    }
    
    /* Sobrescrever qualquer estilo do Streamlit */
    .stMarkdown h1 {
        color: #FFFF00 !important;
    }
    
    /* Container das rádios */
    .radio-option {
        border-radius: 15px !important;
        padding: 12px !important;
        margin-bottom: 10px !important;
        text-align: center !important;
        color: white !important;
        font-weight: bold !important;
        perspective: 500px;
    }
    
    /* Botões 3D - Estilo Base */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        transform-style: preserve-3d;
    }
    
    .stButton>button {
        width: 90% !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        color: white !important;
        margin: 0 auto !important;
        border-radius: 12px !important;
        border: none !important;
        cursor: pointer !important;
        position: relative !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 0 rgba(0,0,0,0.2), 
                    0 5px 10px rgba(0,0,0,0.1),
                    inset 0 1px 1px rgba(255,255,255,0.3) !important;
        text-shadow: 0 1px 1px rgba(0,0,0,0.3) !important;
        transform: translateY(0) !important;
        font-weight: bold !important;
    }
    
    /* Efeito quando o botão é pressionado */
    .stButton>button:active {
        box-shadow: 0 2px 0 rgba(0,0,0,0.2), 
                    0 1px 2px rgba(0,0,0,0.1),
                    inset 0 1px 1px rgba(255,255,255,0.3) !important;
        transform: translateY(4px) !important;
    }
    
    /* Efeito de hover suave */
    .stButton>button:hover {
        filter: brightness(1.05) !important;
    }
    
    /* Cores específicas para cada rádio com gradiente 3D */
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_0"] {
        background: linear-gradient(145deg, #FF9E7D, #ffb696) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_1"] {
        background: linear-gradient(145deg, #FF6B6B, #ff8e8e) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_2"] {
        background: linear-gradient(145deg, #4ECDC4, #88d8d0) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_3"] {
        background: linear-gradient(145deg, #6A8EAE, #8fa8c5) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_4"] {
        background: linear-gradient(145deg, #FF8E53, #ffa877) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_5"] {
        background: linear-gradient(145deg, #8A2BE2, #a155f0) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_6"] {
        background: linear-gradient(145deg, #FF69B4, #ff8ac5) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_7"] {
        background: linear-gradient(145deg, #9370DB, #ab8ce6) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_8"] {
        background: linear-gradient(145deg, #FFA500, #ffb732) !important;
    }
    
    .stButton>button[data-testid="baseButton-secondary"][class*="btn_9"] {
        background: linear-gradient(145deg, #32CD32, #5ce05c) !important;
    }
    
    /* Rodapé visível */
    .footer {
        text-align: center !important;
        padding: 15px !important;
        margin-top: 30px !important;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
    }
    
    /* Centralizando colunas */
    .stColumns {
        align-items: center !important;
    }
    
    /* Ajustes para mobile */
    @media (max-width: 768px) {
        .stButton>button {
            font-size: 1rem !important;
            padding: 12px !important;
            width: 95% !important;
        }
        
        .radio-option {
            padding: 10px !important;
        }
    }
    </style>
    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

def main():
    # Cabeçalho
    with stylable_container(
        key="header",
        css_styles="""
            {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 10px;
                padding: 20px;
                color: white;
                text-align: center;
                margin-bottom: 30px;
            }
        """
    ):
        # Usando div com classe personalizada e estilo inline
        st.markdown("""
            <div class="neuros-title">
                <h1 style="color: #FFFF00 !important;">🔊 NEUROS SOM</h1>
            </div>
            <p style='text-align: center; margin: 0;'>Escolha sua música favorita!</p>
        """, unsafe_allow_html=True)
    
    # Restante do código permanece igual...
    # [O restante do seu código original continua aqui...]

if __name__ == "__main__":
    main()
