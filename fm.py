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

# CSS personalizado otimizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Fundo gradiente fixo */
    .main, .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    }
    
    /* Melhor contraste para títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Título principal destacado */
    .neuros-title h1 {
        color: #FFD700 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 3px 3px 6px rgba(0,0,0,0.5), 0 0 10px #FFD700; }
        to { text-shadow: 3px 3px 6px rgba(0,0,0,0.5), 0 0 20px #FFD700, 0 0 30px #FFD700; }
    }
    
    /* Botões 3D otimizados */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }
    
    .stButton > button {
        width: 100% !important;
        padding: 18px 20px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        cursor: pointer !important;
        position: relative !important;
        transition: all 0.2s ease !important;
        box-shadow: 
            0 8px 0 rgba(0,0,0,0.3), 
            0 6px 15px rgba(0,0,0,0.2),
            inset 0 2px 2px rgba(255,255,255,0.3) !important;
        text-shadow: 0 2px 3px rgba(0,0,0,0.3) !important;
        transform: translateY(0) !important;
        overflow: hidden;
    }
    
    /* Efeito de brilho ao passar o mouse */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255,255,255,0.3) 50%,
            transparent 70%
        );
        transform: rotate(45deg);
        transition: all 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        filter: brightness(1.1) !important;
        transform: translateY(-2px) !important;
        box-shadow: 
            0 10px 0 rgba(0,0,0,0.3), 
            0 8px 20px rgba(0,0,0,0.3),
            inset 0 2px 2px rgba(255,255,255,0.3) !important;
    }
    
    .stButton > button:active {
        box-shadow: 
            0 2px 0 rgba(0,0,0,0.3), 
            0 2px 5px rgba(0,0,0,0.2),
            inset 0 2px 2px rgba(255,255,255,0.3) !important;
        transform: translateY(6px) !important;
    }
    
    /* Cores das rádios com gradientes vibrantes */
    button[key*="btn_0"] { background: linear-gradient(145deg, #FF6B6B, #EE5A6F) !important; }
    button[key*="btn_1"] { background: linear-gradient(145deg, #FF8E53, #FFA07A) !important; }
    button[key*="btn_2"] { background: linear-gradient(145deg, #8A2BE2, #9370DB) !important; }
    button[key*="btn_3"] { background: linear-gradient(145deg, #FF69B4, #FF1493) !important; }
    button[key*="btn_4"] { background: linear-gradient(145deg, #9370DB, #8A2BE2) !important; }
    button[key*="btn_5"] { background: linear-gradient(145deg, #FFA500, #FF8C00) !important; }
    button[key*="btn_6"] { background: linear-gradient(145deg, #32CD32, #00FA9A) !important; }
    button[key*="btn_7"] { background: linear-gradient(145deg, #4ECDC4, #45B7D1) !important; }
    button[key*="btn_8"] { background: linear-gradient(145deg, #6A8EAE, #4A90E2) !important; }
    button[key*="btn_9"] { background: linear-gradient(145deg, #E74C3C, #C0392B) !important; }
    
    /* Player com animação */
    .player-container {
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Barra de progresso personalizada */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
    }
    
    /* Melhorias no áudio player */
    audio {
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Responsividade aprimorada */
    @media (max-width: 768px) {
        .neuros-title h1 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            font-size: 1rem !important;
            padding: 15px !important;
        }
    }
    
    @media (max-width: 480px) {
        .neuros-title h1 {
            font-size: 1.6rem !important;
        }
        
        .stButton > button {
            font-size: 0.95rem !important;
            padding: 12px !important;
        }
    }
    
    /* Tooltip personalizado */
    .stButton > button[title]:hover::after {
        content: attr(title);
        position: absolute;
        bottom: 110%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.85rem;
        white-space: nowrap;
        z-index: 1000;
    }
    </style>
    
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
""", unsafe_allow_html=True)

def get_radios():
    """Retorna dicionário de rádios organizadas por categoria"""
    return {
        "KISS FM": {
            "url": "https://26593.live.streamtheworld.com/RADIO_KISSFM_ADP_SC",
            "color": "#FF6B6B",
            "icon": "💋",
            "genre": "Pop/Hits"
        },
        "80s80s Rock": {
            "url": "https://regiocast.streamabc.net/regc-80s80srock2191507-mp3-192-4255750",
            "color": "#FF8E53",
            "icon": "🤘",
            "genre": "Rock"
        },
        "The Cure Radio": {
            "url": "https://2.mystreaming.net/er/thecure/icecast.audio",
            "color": "#8A2BE2",
            "icon": "🦇",
            "genre": "Alternative"
        },
        "I Love 80s": {
            "url": "https://live1.livemus.com.br:27400/stream",
            "color": "#FF69B4",
            "icon": "❤️",
            "genre": "80s Hits"
        },
        "Wonder 80s": {
            "url": "https://80.streeemer.com/listen/80s/radio.aac",
            "color": "#9370DB",
            "icon": "✨",
            "genre": "80s"
        },
        "80s Pop": {
            "url": "https://oldies.streeemer.com/listen/oldies/radio.aac",
            "color": "#FFA500",
            "icon": "🎤",
            "genre": "Pop"
        },
        "80s Alive": {
            "url": "https://stream.80sa.live/80s-alive.mp3",
            "color": "#32CD32",
            "icon": "🌟",
            "genre": "80s Classics"
        },
        "Rádio Anos 80": {
            "url": "https://stream.zeno.fm/3ywickpd3rkvv",
            "color": "#4ECDC4",
            "icon": "🎸",
            "genre": "BR 80s"
        },
        "Its 80s": {
            "url": "https://securestream.cuelightsmedia.com.au/listen/80s/low.aac",
            "color": "#6A8EAE",
            "icon": "📻",
            "genre": "80s Mix"
        },
        "80s90s Hits": {
            "url": "https://live.streamthe.world/80s90s-hits",
            "color": "#E74C3C",
            "icon": "🎵",
            "genre": "80s/90s"
        }
    }

def render_header():
    """Renderiza o cabeçalho da aplicação"""
    with stylable_container(
        key="header",
        css_styles="""
            {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            }
        """
    ):
        st.markdown("""
            <div class="neuros-title">
                <h1>🔊 NEUROS SOM</h1>
            </div>
            <p style='text-align: center; margin: 0; color: white; font-size: 1.1rem;'>
                🎧 Escolha sua música favorita e aproveite!
            </p>
        """, unsafe_allow_html=True)

def render_radio_buttons(radios):
    """Renderiza os botões das rádios e retorna a selecionada"""
    st.markdown("<h3 style='text-align: center; color: white;'>📻 Selecione sua rádio</h3>", unsafe_allow_html=True)
    
    # Criar 2 colunas para layout responsivo
    cols = st.columns(2, gap="medium")
    radio_selecionada = None
    
    for i, (name, info) in enumerate(radios.items()):
        with cols[i % 2]:
            if st.button(
                f"{info['icon']} {name}",
                key=f"btn_{i}",
                help=f"🎵 {info['genre']} - Clique para tocar",
                type="secondary",
                use_container_width=True
            ):
                radio_selecionada = name
                st.session_state['current_radio'] = name
    
    return radio_selecionada

def render_player(radio_name, radio_info):
    """Renderiza o player de áudio"""
    with stylable_container(
        key="player",
        css_styles=f"""
            {{
                background: linear-gradient(135deg, {radio_info['color']} 0%, rgba(255,255,255,0.1) 100%);
                border-radius: 20px;
                padding: 25px;
                margin-top: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
            }}
        """
    ):
        st.markdown(f"""
            <div class="player-container">
                <h2 style="color: white; margin-bottom: 15px;">
                    ▶️ {radio_info['icon']} {radio_name}
                </h2>
                <p style="color: white; font-size: 1.1rem; margin-bottom: 20px;">
                    🎵 Gênero: {radio_info['genre']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.audio(radio_info["url"], format='audio/mp3', autoplay=True)
        st.progress(100, text=f"🔊 Conectado à {radio_name}")

def render_footer():
    """Renderiza o rodapé com instruções"""
    with stylable_container(
        key="footer",
        css_styles="""
            {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                color: white;
                margin-top: 30px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            }
        """
    ):
        st.markdown("""
            <div>
                <h4 style="color: #FFD700; margin-bottom: 15px;">🚗 Como usar no carro</h4>
                <p style="line-height: 1.8;">
                    <strong>1.</strong> Abra este site no navegador do celular<br>
                    <strong>2.</strong> Conecte via Bluetooth ao rádio do carro<br>
                    <strong>3.</strong> Selecione sua rádio favorita<br>
                    <strong>4.</strong> Aproveite sua música!
                </p>
                <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 20px 0;">
                <p style="font-size: 0.9rem; opacity: 0.9;">
                    💡 <strong>Dica:</strong> Adicione à tela inicial para acesso rápido!
                </p>
                <p style="margin-top: 15px; font-size: 0.85rem;">
                    © 2025 Desenvolvido com ❤️ por <strong>Robson Vilela</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

def main():
    # Inicializar session state
    if 'current_radio' not in st.session_state:
        st.session_state['current_radio'] = None
    
    # Renderizar componentes
    render_header()
    
    radios = get_radios()
    
    # Container principal
    with stylable_container(
        key="main_container",
        css_styles="""
            {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
            }
        """
    ):
        radio_selecionada = render_radio_buttons(radios)
        
        # Manter player visível se já houver uma rádio selecionada
        radio_atual = radio_selecionada or st.session_state.get('current_radio')
        
        if radio_atual and radio_atual in radios:
            render_player(radio_atual, radios[radio_atual])
    
    render_footer()

if __name__ == "__main__":
    main()
