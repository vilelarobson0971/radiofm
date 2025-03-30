import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Rádio Transamérica", page_icon="🎵")

def generate_vu_meter(level):
    """Gera uma barra VU dinâmica simulada"""
    fig, ax = plt.subplots(figsize=(10, 2))
    color = 'green' if level < 70 else 'yellow' if level < 90 else 'red'
    ax.barh(0, level, color=color, height=0.5)
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.text(50, 0, f'{level}%', ha='center', va='center', color='black', fontsize=12)
    return fig

def main():
    st.title("🎵 Rádio Transamérica - Player Online by Robson Vilela")
    
    # URL do streaming de áudio da rádio
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Player de áudio
    audio_placeholder = st.empty()
    audio_placeholder.audio(stream_url, format='audio/aac')
    
    # Barra VU dinâmica (simulada)
    vu_placeholder = st.empty()
    
    # Controles
    if st.button("▶️ Reproduzir Rádio"):
        audio_placeholder.audio(stream_url, format='audio/aac')
        st.success("Rádio em reprodução!")
        
        # Simulação da barra VU (apenas visual)
        for _ in range(100):  # Atualiza por 10 segundos (100 iterações)
            level = np.random.randint(30, 95)  # Valor aleatório para simulação
            vu_fig = generate_vu_meter(level)
            vu_placeholder.pyplot(vu_fig)
            time.sleep(0.1)
    
    # Rodapé
    st.markdown("---")
    st.caption("Player desenvolvido por Robson Vilela | © 2023")

if __name__ == "__main__":
    main()
