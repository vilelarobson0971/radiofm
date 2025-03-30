import streamlit as st

# Configuração da página
st.set_page_config(page_title="Rádio Transamérica", page_icon="🎵")

def main():
    st.title("🎵 Rádio Transamérica - Player Online by Robson Vilela")
    
    # URL do streaming
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Player de áudio (inicia automaticamente)
    st.audio(stream_url, format='audio/aac')
    st.success("Rádio em reprodução automática!")
    
    # Rodapé
    st.markdown("---")
    st.caption("Player desenvolvido por Robson Vilela | © 2023")

if __name__ == "__main__":
    main()
