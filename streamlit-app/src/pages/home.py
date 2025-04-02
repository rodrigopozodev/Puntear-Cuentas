def show_home():
    import streamlit as st

    st.title("Bienvenido a la Página de Inicio")
    st.write("Esta es la página principal de la aplicación Streamlit.")
    st.write("Aquí puedes agregar contenido, gráficos y más.")
    
    # Puedes agregar más elementos aquí, como gráficos, tablas, etc.
    st.image("ruta/a/una/imagen.jpg", caption="Ejemplo de imagen")  # Asegúrate de tener la imagen en la ruta correcta
    st.button("Haz clic aquí")  # Ejemplo de botón
