import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# Configuração da página
st.set_page_config(
    page_title="Bob Rádios Online",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado corrigido
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Corrigindo o fundo */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    /* Títulos sempre visíveis */
    h1, h2, h3, h4, h5, h6, .stMarkdown h3 {
        color: #333333 !important;
    }
    
    /* Botões centralizados e visíveis */
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }
    
    .stButton>button {
        width: 90% !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        color: white !important;
        border: none !important;
        margin: 0 auto !important;
    }
    
    /* Container das rádios */
    .radio-option {
        border-radius: 15px !important;
        padding: 12px !important;
        margin-bottom: 10px !important;
        text-align: center !important;
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Rodapé visível */
    .footer {
        text-align: center !important;
        padding: 15px !important;
        margin-top: 30px !important;
        background: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%) !important;
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
                background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
                border-radius: 10px;
                padding: 20px;
                color: white;
                text-align: center;
                margin-bottom: 30px;
            }
        """
    ):
        st.markdown("<h1 style='text-align: center; margin: 0;'>🎧 BOB RÁDIOS ONLINE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin: 0;'>Escolha sua música favorita!</p>", unsafe_allow_html=True)
    
    # Rádios disponíveis
    radios = {
        "Transamérica": {
            "url": "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac",
            "color": "#FF9E7D",
            "icon": "🎶"
        },
        "KISS FM": {
            "url": "https://26593.live.streamtheworld.com/RADIO_KISSFM_ADP_SC",
            "color": "#FF6B6B",
            "icon": "💋"
        },
        "Mundo Livre": {
            "url": "http://up-continental.webnow.com.br/cultura.aac?1743555337315",
            "color": "#4ECDC4",
            "icon": "🌍"
        },
        "Antena 1": {
            "url": "https://antenaone.crossradio.com.br/stream/1;",
            "color": "#6A8EAE",
            "icon": "📡"
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
                            background: linear-gradient(45deg, {info['color']} 0%, #ffffff 100%);
                            border-radius: 15px;
                            padding: 5px;
                            margin-bottom: 10px;
                        }}
                    """
                ):
                    if st.button(
                        f"{info['icon']} {name}",
                        key=f"btn_{i}",
                        help=f"Tocar {name}"
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
                background: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%);
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
                <p>© 2025 Bob Rádios Online</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
