import streamlit as st

# Configuração da página
st.set_page_config(page_title="Rádio Transamérica", page_icon="🎵")

def main():
    st.title("🎵 Rádio Transamérica - Player Online by Robson Vilela")
    
    # URL do streaming de áudio da rádio
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Inicializa o estado do player
    if 'player' not in st.session_state:
        st.session_state.player = None
    
    # Layout do player
    audio_placeholder = st.empty()
    
    # Botão único de controle
    if st.button("▶️ Reproduzir Rádio" if st.session_state.player is None else "⏹️ Parar"):
        if st.session_state.player is None:
            st.session_state.player = audio_placeholder.audio(stream_url, format='audio/aac')
            st.success("Rádio em reprodução!")
        else:
            audio_placeholder.empty()
            st.session_state.player = None
            st.warning("Reprodução parada")
    
    # Rodapé
    st.markdown("---")
    st.caption("Player desenvolvido por Robson Vilela | © 2023")

if __name__ == "__main__":
    main()
