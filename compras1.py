import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# Configuração da página
st.set_page_config(
    page_title="Rádio Player Online",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
    }
    
    .radio-option {
        display: inline-block;
        margin: 5px;
        padding: 10px 15px;
        border-radius: 20px;
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white !important;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .radio-option:hover {
        transform: scale(1.05);
    }
    
    .radio-option input:checked + label {
        background: linear-gradient(45deg, #11998e 0%, #38ef7d 100%) !important;
    }
    </style>
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
        st.markdown("<h1 style='text-align: center; margin: 0;'>🎧 RÁDIO PLAYER ONLINE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin: 0;'>by Robson Vilela | Escolha sua vibe musical!</p>", unsafe_allow_html=True)
    
    # Dicionário com as rádios disponíveis (agora com The Cure)
    radios = {
        "Rádio Transamérica": {
            "url": "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac",
            "color": "#FF9E7D",
            "icon": "🎶"
        },
        "Rádio KISS FM": {
            "url": "https://26593.live.streamtheworld.com/RADIO_KISSFM_ADP_SC",
            "color": "#FF6B6B",
            "icon": "💋"
        },
        "Rádio Mundo Livre": {
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
            "color": "#8A2BE2",  # Roxo vibrante
            "icon": "🦇"  # Ícone de morcego (referência ao visual da banda)
        }
    }
    
    # Container principal
    with stylable_container(
        key="main_container",
        css_styles="""
            {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
        """
    ):
        # Seleção da rádio
        st.subheader("🎚️ Selecione sua rádio preferida:")
        
        # Usando columns para melhor layout
        cols = st.columns(len(radios))
        radio_selecionada = None
        
        for i, (radio_name, radio_info) in enumerate(radios.items()):
            with cols[i]:
                with stylable_container(
                    key=f"radio_{i}",
                    css_styles=f"""
                        {{
                            background: linear-gradient(45deg, {radio_info['color']} 0%, #ffffff 100%);
                            border-radius: 15px;
                            padding: 10px;
                            text-align: center;
                            margin-bottom: 10px;
                        }}
                    """
                ):
                    if st.button(f"{radio_info['icon']} {radio_name}"):
                        radio_selecionada = radio_name
        
        # Se uma rádio foi selecionada
        if radio_selecionada:
            # Card da rádio selecionada
            with stylable_container(
                key="now_playing",
                css_styles=f"""
                    {{
                        background: linear-gradient(45deg, {radios[radio_selecionada]['color']} 0%, #ffffff 100%);
                        border-radius: 15px;
                        padding: 20px;
                        margin-top: 20px;
                        text-align: center;
                    }}
                """
            ):
                st.markdown(f"<h2 style='text-align: center; color: white;' class='now-playing'>🎧 TOCANDO AGORA: {radio_selecionada}</h2>", unsafe_allow_html=True)
                
                # Player de áudio
                st.audio(radios[radio_selecionada]["url"], format='audio/aac')
                
                # Barra de progresso simulada
                st.progress(70, text="📻 Sintonizando a melhor qualidade...")
                
                # Efeitos visuais
                st.balloons()
    
    # Rodapé
    with stylable_container(
        key="footer",
        css_styles="""
            {
                background: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%);
                border-radius: 10px;
                padding: 15px;
                margin-top: 30px;
                text-align: center;
                color: white;
            }
        """
    ):
        st.markdown("🎶 Música é vida! | © 2025 Robson Vilela | Atualizado em 2025 🎶", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
