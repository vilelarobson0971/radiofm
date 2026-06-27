import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

# ============================================================
# Configuração da página
# ============================================================
st.set_page_config(
    page_title="Neuros Som",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS global — tema escuro com acentos neon e cards de vidro
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Fundo gradiente animado */
    .main, .stApp {
        background: radial-gradient(circle at 20% 20%, #2a0f4e 0%, #150a30 35%, #060314 100%) !important;
        background-attachment: fixed !important;
    }

    /* remove o respiro padrão do topo do app */
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 980px !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Título principal com brilho neon */
    .neuros-title h1 {
        color: #FFD15C !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        margin: 0 !important;
        text-shadow: 0 0 10px rgba(255, 209, 92, 0.55), 0 0 24px rgba(255, 100, 200, 0.25);
        animation: glow 2.6s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 8px rgba(255,209,92,0.5), 0 0 18px rgba(255,100,200,0.2); }
        to   { text-shadow: 0 0 16px rgba(255,209,92,0.85), 0 0 32px rgba(255,100,200,0.45); }
    }

    .neuros-subtitle {
        text-align: center;
        margin: 6px 0 0 0;
        color: rgba(255,255,255,0.78);
        font-size: 1.02rem;
        font-weight: 400;
    }

    /* Botões — visual "ouvir agora" em pílula com glow */
    .stButton { display: flex !important; justify-content: center !important; }

    .stButton > button {
        width: 100% !important;
        padding: 10px 16px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px;
        color: white !important;
        border-radius: 999px !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        cursor: pointer !important;
        background: rgba(255,255,255,0.06) !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25) !important;
    }

    .stButton > button:hover {
        background: rgba(255,255,255,0.16) !important;
        border-color: rgba(255,255,255,0.4) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.35) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
        filter: brightness(0.95) !important;
    }

    /* Cartão "vidro" genérico usado pelos stylable_containers */
    .glass-block {
        backdrop-filter: blur(14px);
    }

    /* Badge "AO VIVO" pulsante */
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(255, 70, 70, 0.18);
        border: 1px solid rgba(255, 90, 90, 0.55);
        color: #ff8a8a;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        padding: 3px 9px;
        border-radius: 20px;
        white-space: nowrap;
    }

    .live-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #ff5c5c;
        animation: pulse 1.4s ease-in-out infinite;
    }

    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(255,92,92,0.6); }
        70%  { box-shadow: 0 0 0 6px rgba(255,92,92,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,92,92,0); }
    }

    /* Equalizador animado no player */
    .equalizer {
        display: inline-flex;
        align-items: flex-end;
        gap: 3px;
        height: 18px;
        margin-right: 8px;
        vertical-align: middle;
    }
    .equalizer span {
        width: 3px;
        background: #FFD15C;
        border-radius: 2px;
        animation: eq 1s ease-in-out infinite;
    }
    .equalizer span:nth-child(1) { height: 40%; animation-delay: 0s; }
    .equalizer span:nth-child(2) { height: 100%; animation-delay: 0.2s; }
    .equalizer span:nth-child(3) { height: 60%; animation-delay: 0.4s; }
    .equalizer span:nth-child(4) { height: 80%; animation-delay: 0.1s; }
    @keyframes eq {
        0%, 100% { transform: scaleY(0.4); }
        50% { transform: scaleY(1); }
    }

    /* Player entrando com leve slide */
    .player-container { animation: slideIn 0.45s ease-out; }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #FFD15C, #FF8A65) !important;
    }

    audio {
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
        margin-top: 4px;
    }

    .autoplay-hint {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.6);
        margin-top: 8px;
    }

    hr.soft { border: none; border-top: 1px solid rgba(255,255,255,0.12); margin: 18px 0; }

    @media (max-width: 768px) {
        .neuros-title h1 { font-size: 2rem !important; }
        .stButton > button { font-size: 0.88rem !important; padding: 9px 14px !important; }
    }
    @media (max-width: 480px) {
        .neuros-title h1 { font-size: 1.6rem !important; }
    }
    </style>

    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
""", unsafe_allow_html=True)


def get_radios():
    """Retorna dicionário de rádios organizadas por categoria.

    O campo 'format' é o tipo MIME real do stream (quando conhecido),
    usado para que o navegador não precise "adivinhar" o codec antes
    de iniciar a reprodução — isso é o que evitava o autoplay em
    quase todas as rádios, exceto a que já era MP3 puro.
    """
    return {
        "KISS FM": {
            "url": "https://26593.live.streamtheworld.com/RADIO_KISSFM_ADP_SC",
            "color": "#FF6B6B",
            "icon": "💋",
            "genre": "Pop/Hits",
            "format": "audio/mpeg",
        },
        "80s80s Rock": {
            "url": "https://regiocast.streamabc.net/regc-80s80srock2191507-mp3-192-4255750",
            "color": "#FF8E53",
            "icon": "🤘",
            "genre": "Rock",
            "format": "audio/mpeg",
        },
        "The Cure Radio": {
            "url": "https://2.mystreaming.net/er/thecure/icecast.audio",
            "color": "#8A2BE2",
            "icon": "🦇",
            "genre": "Alternative",
            "format": "audio/mpeg",
        },
        "I Love 80s": {
            "url": "https://live1.livemus.com.br:27400/stream",
            "color": "#FF69B4",
            "icon": "❤️",
            "genre": "80s Hits",
            "format": "audio/mpeg",
        },
        "Wonder 80s": {
            "url": "https://80.streeemer.com/listen/80s/radio.aac",
            "color": "#9370DB",
            "icon": "✨",
            "genre": "80s",
            "format": "audio/aac",
        },
        "80s Pop": {
            "url": "https://oldies.streeemer.com/listen/oldies/radio.aac",
            "color": "#FFA500",
            "icon": "🎤",
            "genre": "Pop",
            "format": "audio/aac",
        },
        "80s Alive": {
            "url": "https://stream.80sa.live/80s-alive.mp3",
            "color": "#32CD32",
            "icon": "🌟",
            "genre": "80s Classics",
            "format": "audio/mpeg",
        },
        "Rádio Anos 80": {
            "url": "https://stream.zeno.fm/3ywickpd3rkvv",
            "color": "#4ECDC4",
            "icon": "🎸",
            "genre": "BR 80s",
            "format": "audio/mpeg",
        },
        "Its 80s": {
            "url": "https://securestream.cuelightsmedia.com.au/listen/80s/low.aac",
            "color": "#6A8EAE",
            "icon": "📻",
            "genre": "80s Mix",
            "format": "audio/aac",
        },
        "80s90s Hits": {
            "url": "https://live.streamthe.world/80s90s-hits",
            "color": "#E74C3C",
            "icon": "🎵",
            "genre": "80s/90s",
            "format": "audio/mpeg",
        },
    }


def guess_format(url: str, fallback: str = "audio/mpeg") -> str:
    """Fallback de detecção de formato pela extensão da URL,
    usado caso uma rádio não tenha 'format' definido manualmente."""
    url_lower = url.lower()
    if ".aac" in url_lower or "aac" in url_lower.split("/")[-1]:
        return "audio/aac"
    if ".ogg" in url_lower:
        return "audio/ogg"
    if ".mp3" in url_lower or "-mp3-" in url_lower:
        return "audio/mpeg"
    return fallback


def render_header():
    """Renderiza o cabeçalho da aplicação."""
    with stylable_container(
        key="header",
        css_styles="""
            {
                background: linear-gradient(120deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 20px;
                padding: 28px 20px;
                text-align: center;
                margin-bottom: 24px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.35);
            }
        """
    ):
        st.markdown("""
            <div class="neuros-title">
                <h1>🔊 NEUROS SOM</h1>
            </div>
            <p class="neuros-subtitle">🎧 Escolha sua Rádio Favorita e Aproveite</p>
        """, unsafe_allow_html=True)


def _select_radio(name):
    """Callback executado ANTES do rerun do script.

    Usar on_click garante que st.session_state['current_radio'] já
    esteja atualizado quando o script reprocessa e desenha os cartões
    — por isso o badge 'NO AR' aparece já no primeiro clique, sem
    precisar de um segundo clique para 'alcançar' o estado.
    """
    st.session_state["current_radio"] = name


def render_radio_buttons(radios):
    """Renderiza as rádios como cartões."""
    st.markdown(
        "<h3 style='text-align:center; font-size:1.15rem; opacity:0.9; margin-bottom:16px;'>"
        "📻 Selecione sua rádio</h3>",
        unsafe_allow_html=True
    )

    cols = st.columns(2, gap="medium")

    for i, (name, info) in enumerate(radios.items()):
        with cols[i % 2]:
            is_playing = st.session_state.get("current_radio") == name
            border_glow = f"0 0 0 1px {info['color']}aa, 0 8px 22px rgba(0,0,0,0.35)" if is_playing else "0 6px 16px rgba(0,0,0,0.25)"

            with stylable_container(
                key=f"card_{i}",
                css_styles=f"""
                    {{
                        background: linear-gradient(155deg, {info['color']}26, rgba(255,255,255,0.03));
                        border: 1px solid {info['color']}55;
                        border-radius: 18px;
                        padding: 16px 16px 12px 16px;
                        margin-bottom: 16px;
                        box-shadow: {border_glow};
                        transition: all 0.25s ease;
                    }}
                """
            ):
                st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                        <div style="font-size:1.8rem;line-height:1;">{info['icon']}</div>
                        <div style="flex:1;">
                            <div style="font-weight:700;color:white;font-size:1rem;">{name}</div>
                            <div style="font-size:0.78rem;color:rgba(255,255,255,0.65);">{info['genre']}</div>
                        </div>
                        {'<span class="live-badge"><span class="live-dot"></span>NO AR</span>' if is_playing else ''}
                    </div>
                """, unsafe_allow_html=True)

                if is_playing:
                    # components.html garante execução real de JS (st.markdown
                    # não executa <script> e nem sempre preserva onclick de
                    # forma confiável). O botão vive num iframe, então
                    # acessamos o documento pai via window.parent.document
                    # para encontrar e dar play no <audio> real da página —
                    # isso conta como gesto de clique síncrono e válido.
                    components.html(f"""
                        <style>
                            html, body {{ margin:0; padding:0; background:transparent; }}
                            .neuros-play-btn {{
                                width:100%;
                                box-sizing:border-box;
                                padding:10px 16px;
                                font-size:0.95rem;
                                font-weight:700;
                                letter-spacing:0.3px;
                                color:white;
                                border-radius:999px;
                                border:1px solid rgba(255,255,255,0.18);
                                cursor:pointer;
                                background:rgba(255,255,255,0.06);
                                box-shadow:0 4px 14px rgba(0,0,0,0.25);
                                font-family:'Montserrat',sans-serif;
                                transition: all 0.2s ease;
                            }}
                            .neuros-play-btn:hover {{
                                background:rgba(255,255,255,0.16);
                                border-color:rgba(255,255,255,0.4);
                            }}
                            .neuros-play-btn:active {{
                                filter:brightness(0.9);
                            }}
                        </style>
                        <button id="neurosPlayBtn_{i}" class="neuros-play-btn">
                            ⏸️ Tocando agora
                        </button>
                        <script>
                            (function() {{
                                var btn = document.getElementById("neurosPlayBtn_{i}");
                                if (btn) {{
                                    btn.addEventListener("click", function() {{
                                        try {{
                                            var pdoc = window.parent.document;
                                            var audio = pdoc.querySelector("audio");
                                            if (audio) {{
                                                audio.play().catch(function(err) {{
                                                    console.log("Neuros Som: play bloqueado", err);
                                                }});
                                            }}
                                        }} catch (e) {{
                                            console.log("Neuros Som: erro ao acessar audio", e);
                                        }}
                                    }});
                                }}
                            }})();
                        </script>
                    """, height=52)
                else:
                    st.button(
                        "▶️ Ouvir agora",
                        key=f"btn_{i}",
                        use_container_width=True,
                        on_click=_select_radio,
                        args=(name,),
                    )


def render_player(radio_name, radio_info):
    """Renderiza o player de áudio."""
    with stylable_container(
        key="player",
        css_styles=f"""
            {{
                background: linear-gradient(135deg, {radio_info['color']}33 0%, rgba(255,255,255,0.05) 100%);
                border: 1px solid {radio_info['color']}66;
                border-radius: 20px;
                padding: 24px;
                margin-top: 16px;
                text-align: center;
                box-shadow: 0 12px 30px rgba(0,0,0,0.4);
            }}
        """
    ):
        fmt = radio_info.get("format") or guess_format(radio_info["url"])

        st.markdown(f"""
            <div class="player-container">
                <h2 style="font-size:1.5rem; margin-bottom:8px;">
                    <span class="equalizer"><span></span><span></span><span></span><span></span></span>
                    {radio_info['icon']} {radio_name}
                </h2>
                <p style="color:rgba(255,255,255,0.75); font-size:1rem; margin-bottom:14px;">
                    🎵 {radio_info['genre']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.audio(radio_info["url"], format=fmt, autoplay=True)
        st.progress(100, text=f"🔊 Conectado à {radio_name}")
        st.markdown(
            "<p class='autoplay-hint'>Se o som não iniciar automaticamente "
            "(alguns navegadores bloqueiam autoplay), toque no cartão desta rádio "
            "em \"Tocando agora\" acima para retomar.</p>",
            unsafe_allow_html=True
        )


def render_footer():
    """Renderiza o rodapé com instruções."""
    with stylable_container(
        key="footer",
        css_styles="""
            {
                background: linear-gradient(120deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 18px;
                padding: 22px;
                text-align: center;
                color: white;
                margin-top: 26px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            }
        """
    ):
        st.markdown("""
            <div>
                <h4 style="color:#FFD15C; font-size:1.05rem; margin-bottom:14px;">🚗 Como usar no carro</h4>
                <p style="line-height:1.8; color:rgba(255,255,255,0.85); font-size:0.92rem;">
                    <strong>1.</strong> Abra este site no navegador do celular<br>
                    <strong>2.</strong> Conecte via Bluetooth ao rádio do carro<br>
                    <strong>3.</strong> Selecione sua rádio favorita<br>
                    <strong>4.</strong> Aproveite sua música!
                </p>
                <hr class="soft">
                <p style="font-size:0.85rem; opacity:0.75;">
                    💡 <strong>Dica:</strong> Adicione à tela inicial para acesso rápido!
                </p>
                <p style="margin-top:14px; font-size:0.78rem; opacity:0.6;">
                    © 2025 Desenvolvido com ❤️ por <strong>Robson Vilela</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)


def main():
    if "current_radio" not in st.session_state:
        st.session_state["current_radio"] = None

    render_header()
    radios = get_radios()

    with stylable_container(
        key="main_container",
        css_styles="""
            {
                background: rgba(255, 255, 255, 0.035);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 22px;
                padding: 26px;
                box-shadow: 0 12px 40px rgba(0,0,0,0.3);
                margin-bottom: 20px;
            }
        """
    ):
        render_radio_buttons(radios)
        radio_atual = st.session_state.get("current_radio")

        if radio_atual and radio_atual in radios:
            render_player(radio_atual, radios[radio_atual])

    render_footer()


if __name__ == "__main__":
    main()
    
