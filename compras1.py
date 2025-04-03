import streamlit as st

# Configuração da página
st.set_page_config(page_title="Rádio Player Online", page_icon="🎵")

def main():
    st.title("🎵 Rádio Player Online by Robson Vilela")
    st.markdown("---")
    
    # Dicionário com as rádios disponíveis
    radios = {
        "Rádio Transamérica": {
            "url": "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac",
            "color": "yellow"
        },
        "Rádio KISS FM": {
            "url": "https://26593.live.streamtheworld.com/RADIO_KISSFM_ADP_SC",
            "color": "orange"
        },
        "Rádio Mundo Livre": {
            "url": "http://up-continental.webnow.com.br/cultura.aac?1743555337315",
            "color": "green"
        },
        "Antena 1": {
            "url": "https://antenaone.crossradio.com.br/stream/1;",
            "color": "blue"
        }
    }
    
    # Seleção da rádio
    st.subheader("Selecione uma rádio:")
    radio_selecionada = st.radio(
        "Opções:",
        options=list(radios.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Exibe o nome da rádio com a cor correspondente
    cor = radios[radio_selecionada]["color"]
    st.markdown(f"<h3 style='color:{cor}'>▶ {radio_selecionada}</h3>", unsafe_allow_html=True)
    
    # Player de áudio (inicia automaticamente)
    st.audio(radios[radio_selecionada]["url"], format='audio/aac')
    st.success(f"Reproduzindo: {radio_selecionada}")
    
    # Rodapé
    st.markdown("---")
    st.caption("Player desenvolvido por Robson Vilela | © 2023")

if __name__ == "__main__":
    main()
