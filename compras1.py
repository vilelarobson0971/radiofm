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

# CSS personalizado com otimizações mobile - AGORA CORRIGIDO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
    }
    </style>
    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

def main():
    # Cabeçalho com gradiente
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
    
    # Dicionário com as rádios disponíveis
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
                padding: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
        """
    ):
        # Seleção da rádio em colunas responsivas
        st.markdown("<h3 style='text-align: center;'>📻 Selecione sua rádio</h3>", unsafe_allow_html=True)
        
        # Layout responsivo (2 colunas em mobile)
        col1, col2 = st.columns(2)
        cols = [col1, col2]
        radio_selecionada = None
        
        for i, (radio_name, radio_info) in enumerate(radios.items()):
            with cols[i % 2]:  # Alterna entre as colunas
                with stylable_container(
                    key=f"radio_{i}",
                    css_styles=f"""
                        {{
                            background: linear-gradient(45deg, {radio_info['color']} 0%, #ffffff 100%);
                            border-radius: 15px;
                            padding: 12px;
                            text-align: center;
                            margin-bottom: 10px;
                        }}
                    """
                ):
                    if st.button(
                        f"{radio_info['icon']} {radio_name}",
                        key=f"btn_{i}",
                        help=f"Tocar {radio_name}"
                    ):
                        radio_selecionada = radio_name
        
        # Player de áudio
        if radio_selecionada:
            with stylable_container(
                key="now_playing",
                css_styles=f"""
                    {{
                        background: linear-gradient(45deg, {radios[radio_selecionada]['color']} 0%, #ffffff 100%);
                        border-radius: 15px;
                        padding: 20px;
                        margin-top: 15px;
                        text-align: center;
                    }}
                """
            ):
                st.markdown(
                    f"<h3 style='text-align: center; color: white;' class='now-playing'>"
                    f"▶️ TOCANDO AGORA: {radio_selecionada}</h3>", 
                    unsafe_allow_html=True
                )
                
                # Player otimizado para mobile
                st.audio(
                    radios[radio_selecionada]["url"], 
                    format='audio/aac',
                    autoplay=True
                )
                
                # Status de conexão
                st.progress(80, text=f"🔊 Conectado à {radio_selecionada}")
    
    # Rodapé com instruções para uso no carro
    with stylable_container(
        key="footer",
        css_styles="""
            {
                background: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                color: white;
            }
        """
    ):
        st.markdown("""
            <div style='font-size: 0.9rem;'>
            <p><strong>Como usar no carro:</strong></p>
            <p>1. Abra este site no seu celular<br>
            2. Conecte o celular ao rádio do carro via Bluetooth<br>
            3. Selecione sua rádio favorita e aproveite!</p>
            <p>© 2025 Dev. Robson Vilela | Atualizado em 2025</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
