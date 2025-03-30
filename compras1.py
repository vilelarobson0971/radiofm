import streamlit as st
import requests
from io import BytesIO
import time

def main():
    st.title("Rádio Transamérica - Streamlit Player")
    
    # URL do streaming de áudio da rádio
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Usando o player de áudio nativo do Streamlit
    st.audio(stream_url, format='audio/aac')
    
    # Controles adicionais
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reproduzir Rádio"):
            st.experimental_rerun()  # Recarrega o player
            
    with col2:
        if st.button("Parar Rádio"):
            st.experimental_rerun()  # Recarrega a página para "parar"

    st.write("O player pode levar alguns segundos para começar a reprodução.")
    
    # Atualização automática para manter o stream ativo
    st_autorefresh = st.empty()
    st_autorefresh.info("Atualizando a cada 30 segundos...")
    time.sleep(30)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
