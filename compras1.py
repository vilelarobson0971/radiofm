import streamlit as st
import vlc
import time
import os

# Caminho para o VLC (Altere conforme necessário)
VLC_PATH = r"C:\Program Files\VideoLAN\VLC"
os.environ["PATH"] = VLC_PATH + os.pathsep + os.environ["PATH"]

# Instância do player
player = None

def tocar_radio(stream_url):
    """Reproduz um streaming de áudio de uma rádio online."""
    global player
    if player is None:
        player = vlc.MediaPlayer(stream_url)
        player.play()
        st.success("Reprodução iniciada!")
    else:
        st.warning("O rádio já está tocando!")

def parar_radio():
    """Para a reprodução da rádio."""
    global player
    if player:
        player.stop()
        player = None
        st.warning("Reprodução parada!")
    else:
        st.warning("Nenhuma rádio está tocando!")

# URL do streaming de áudio da rádio
stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/RT_SPAAC.aac?1735034341263"

# Interface Streamlit
st.title("Rádio Transamérica - Streamlit Player")

if st.button("Reproduzir Rádio"):
    tocar_radio(stream_url)

if st.button("Parar Rádio"):
    parar_radio()
