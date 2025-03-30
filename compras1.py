import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configurações da página
st.set_page_config(page_title="Rádio Transamérica", page_icon="🎵")

def generate_vu_meter(level):
    """Cria uma barra VU dinâmica colorida"""
    fig, ax = plt.subplots(figsize=(10, 1.5))
    color = 'green' if level < 70 else 'yellow' if level < 90 else 'red'
    ax.barh(0, level, color=color, height=0.8)
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.text(50, 0, f'{level}%', ha='center', va='center', color='black', fontsize=10, weight='bold')
    return fig

def main():
    st.title("🎵 Rádio Transamérica - Player Online by Robson Vilela")
    
    # URL do streaming
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac"
    
    # Inicializa o estado do player
    if 'playing' not in st.session_state:
        st.session_state.playing = False
    
    # Layout em colunas para botão e barra VU
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Botão único de reprodução
        if st.button("▶️ Reproduzir Rádio" if not st.session_state.playing else "⏹️ Parar"):
            st.session_state.playing = not st.session_state.playing
    
    # Exibe o player de áudio se estiver ativo
    if st.session_state.playing:
        st.audio(stream_url, format='audio/aac')
        
        # Barra VU dinâmica (simulada)
        vu_placeholder = st.empty()
        for _ in range(100):  # Atualiza por 15 segundos (100 iterações)
            if not st.session_state.playing:
                break
            level = np.random.randint(30, 95)  # Valor aleatório para simulação
            vu_placeholder.pyplot(generate_vu_meter(level))
            time.sleep(0.15)
    
    # Rodapé
    st.markdown("---")
    st.caption("Player desenvolvido por Robson Vilela | © 2023")

if __name__ == "__main__":
    main()
