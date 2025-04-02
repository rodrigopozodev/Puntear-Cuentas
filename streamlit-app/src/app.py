import streamlit as st
from components.sidebar import create_sidebar
from pages.home import show_home

def main():
    st.title("Mi Aplicación Streamlit")
    create_sidebar()
    
    # Mostrar la página de inicio
    show_home()

if __name__ == "__main__":
    main()