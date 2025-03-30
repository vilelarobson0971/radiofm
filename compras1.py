import streamlit as st

# Configuração da página
st.set_page_config(page_title="Rádio Transamérica", page_icon="🎵")

def main():
    st.title("🎵 Rádio Transamérica - Player Online by Robson Vilela")
    
    # URL do streaming
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Inicializa o estado do player
    if 'playing' not in st.session_state:
        st.session_state.playing = False
    
    # Player de áudio (sempre visível)
    audio_placeholder = st.empty()
    
    # Único botão de controle
    if st.button("▶️ Reproduzir Rádio" if not st.session_state.playing else "⏹️ Parar"):
        st.session_state.playing = not st.session_state.playing
        if st.session_state.playing:
            audio_placeholder.audio(stream_url, format='audio/aac')
            st.success("Rádio em reprodução!")
        else:
            audio_placeholder.empty()
            st.warning("Reprodução parada")
    
    # Rodapé
    st.markdown("---")
    st.caption("Player desenvolvido por Robson Vilela | © 2023")

if __name__ == "__main__":
    main()
