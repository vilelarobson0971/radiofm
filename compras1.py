import streamlit as st
import time

def main():
    st.title("🎵 Rádio Transamérica - Player Online")
    
    # URL do streaming de áudio da rádio
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Player de áudio
    audio_placeholder = st.empty()
    audio_placeholder.audio(stream_url, format='audio/aac')
    
    # Controles
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Reproduzir Rádio"):
            audio_placeholder.audio(stream_url, format='audio/aac')
            
    with col2:
        if st.button("⏹️ Parar Rádio"):
            audio_placeholder.empty()  # Remove o player
    
    # Status e informações
    if audio_placeholder._is_top_level:
        st.success("Rádio carregada com sucesso!")
    else:
        st.warning("Clique em 'Reproduzir' para iniciar")
    
    # Atualização automática (opcional)
    refresh = st.checkbox("Manter conexão ativa (atualizar a cada 30s)")
    if refresh:
        time.sleep(30)
        st.rerun()  # Usando st.rerun() em vez de st.experimental_rerun()

if __name__ == "__main__":
    main()
