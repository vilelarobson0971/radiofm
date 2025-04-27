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
    
    /* Títulos sempre visíveis */
    h1, h2, h3, h4, h5, h6, .stMarkdown h3 {
        color: #333333 !important;
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
    
    /* Estilo específico para o título principal */
    .css-10trblm {
        color: #FFFF00 !important;
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
        st.markdown("<h1 style='text-align: center; margin: 0; color: #FFFF00 !important;'>🔊 NEUROS SOM</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin: 0;'>Escolha sua música favorita!</p>", unsafe_allow_html=True)
    
    # Rádios disponíveis
    radios = {
        "KISS FM": {
            "url": "https://26593.live.streamtheworld.com/RADIO_KISSFM_ADP_SC",
            "color": "#FF6B6B",
            "icon": "💋"
        },
        "80s80s Rock": {
            "url": "https://regiocast.streamabc.net/regc-80s80srock2191507-mp3-192-4255750?sABC=67rr72r0%230%23291on65n9s0149050p2r0013s22q9260%23enqvbqr&aw_0_1st.playerid=radiode&amsparams=playerid:radiode;skey:1743680224",
            "color": "#FF8E53",
            "icon": "🤘"
        },
        "The Cure": {
            "url": "https://2.mystreaming.net/er/thecure/icecast.audio",
            "color": "#8A2BE2",
            "icon": "🦇"
        },
        "I Love 80s": {
            "url": "https://live1.livemus.com.br:27400/stream",
            "color": "#FF69B4",
            "icon": "❤️"
        },
        "Wonder 80s": {
            "url": "https://80.streeemer.com/listen/80s/radio.aac",
            "color": "#9370DB",
            "icon": "✨"
        },
        "80s Pop": {
            "url": "https://oldies.streeemer.com/listen/oldies/radio.aac",
            "color": "#FFA500",
            "icon": "🎤"
        },
        "80s Alive": {
            "url": "https://stream.80sa.live/80s-alive.mp3",
            "color": "#32CD32",
            "icon": "🌟"
        },
        "The Big 80s Station": {
            "url": "https://ssl.nexuscast.com:9044/",
            "color": "#4ECDC4",
            "icon": "🎸"
        },
        "Its 80s": {
            "url": "https://securestream.cuelightsmedia.com.au/listen/80s/low.aac",
            "color": "#6A8EAE",
            "icon": "📻"
        },
        "80s90s Hits": {
            "url": "https://live.streamthe.world/80s90s-hits",
            "color": "#8A2BE2",
            "icon": "🎵"
        }
    }
    
    # Container principal
    with stylable_container(
        key="main_container",
        css_styles="""
            {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
        """
    ):
        st.markdown("<h3 style='text-align: center;'>📻 Selecione sua rádio</h3>", unsafe_allow_html=True)
        
        # Criando 2 colunas centralizadas
        cols = st.columns(2)
        radio_selecionada = None
        
        for i, (name, info) in enumerate(radios.items()):
            with cols[i % 2]:
                # Container estilizado para cada botão
                with stylable_container(
                    key=f"btn_container_{i}",
                    css_styles=f"""
                        {{
                            display: flex !important;
                            justify-content: center !important;
                            background: transparent !important;
                            border-radius: 15px;
                            padding: 5px;
                            margin-bottom: 10px;
                        }}
                    """
                ):
                    if st.button(
                        f"{info['icon']} {name}",
                        key=f"btn_{i}",
                        help=f"Tocar {name}",
                        type="secondary"
                    ):
                        radio_selecionada = name
        
        if radio_selecionada:
            with stylable_container(
                key="player",
                css_styles=f"""
                    {{
                        background: linear-gradient(45deg, {radios[radio_selecionada]['color']} 0%, #ffffff 100%);
                        border-radius: 15px;
                        padding: 20px;
                        margin-top: 20px;
                        text-align: center;
                        color: white;
                    }}
                """
            ):
                st.markdown(f"<h3>▶️ TOCANDO AGORA: {radio_selecionada}</h3>", unsafe_allow_html=True)
                st.audio(radios[radio_selecionada]["url"], format='audio/aac', autoplay=True)
                st.progress(80, text=f"🔊 Conectado à {radio_selecionada}")
    
    # Rodapé
    with stylable_container(
        key="footer",
        css_styles="""
            {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                color: white;
                margin-top: 20px;
            }
        """
    ):
        st.markdown("""
            <div>
                <p><strong>Como usar no carro:</strong></p>
                <p>1. Abra no navegador do celular<br>
                2. Conecte via Bluetooth ao rádio do carro<br>
                3. Aproveite sua música!</p>
                <p>© 2025 Desenvolvido por Robson Vilela</p>
            </div>
        """, unsafe_allow_html=True)

    # Efeito 3D avançado com JavaScript
    st.markdown("""
        <script>
        // Efeito 3D avançado com inclinação ao passar o mouse
        document.addEventListener('DOMContentLoaded', function() {
            const buttons = document.querySelectorAll('.stButton > button');
            
            buttons.forEach(button => {
                button.addEventListener('mousemove', function(e) {
                    const x = e.offsetX;
                    const y = e.offsetY;
                    const w = this.offsetWidth;
                    const h = this.offsetHeight;
                    
                    const tiltX = (y / h * 10) - 5;
                    const tiltY = (x / w * -10) + 5;
                    
                    this.style.transform = `translateY(0) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
                });
                
                button.addEventListener('mouseout', function() {
                    this.style.transform = 'translateY(0) rotateX(0) rotateY(0)';
                });
            });
        });
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
