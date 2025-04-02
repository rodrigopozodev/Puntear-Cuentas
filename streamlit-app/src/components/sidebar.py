def create_sidebar():
    import streamlit as st

    st.sidebar.title("Navegación")
    options = st.sidebar.radio("Selecciona una sección:", ("Inicio", "Otra Sección"))

    return options