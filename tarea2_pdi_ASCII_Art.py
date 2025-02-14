import streamlit as st
from PIL import Image
from io import BytesIO

# Configuración de la página en modo ancho
st.set_page_config(page_title="ASCII Art - Esqueleto", layout="wide")

# =============================================================================
# FUNCIONES PLACEHOLDER PARA CADA FILTRO (sin lógica, solo definidas)
# =============================================================================

def ascii_art_m_color_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando la misma letra (M/@)
    con el color promedio.
    (Funcionalidad pendiente de implementar)
    """
    # Aquí irá la lógica en el futuro.
    # De momento, solo devolvemos la original.
    return original_image

def ascii_art_m_grayscale_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando la misma letra (M/@)
    en tonos de gris.
    (Funcionalidad pendiente de implementar)
    """
    return original_image

def ascii_art_chars_bn_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando un conjunto de caracteres
    en blanco y negro, simulando distintos niveles de brillo.
    (Funcionalidad pendiente de implementar)
    """
    return original_image

def ascii_art_custom_text_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando un texto o frase
    definida por el usuario, con el color promedio real de la imagen.
    (Funcionalidad pendiente de implementar)
    """
    return original_image

def ascii_art_domino_cards_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando símbolos de dominó
    o naipes, en blanco/negro, que representen distintos niveles de brillo.
    (Funcionalidad pendiente de implementar)
    """
    return original_image

# =============================================================================
# FUNCIÓN PRINCIPAL DE STREAMLIT
# =============================================================================

def main():
    st.sidebar.title("Configuraciones y ASCII Art")

    # Menú lateral con los 5 filtros nuevos
    filter_options = [
        "ASCII - Letra (M/@) Color",
        "ASCII - Letra (M/@) Gris",
        "ASCII - Conjunto de caracteres B/N",
        "ASCII - Texto Custom a Color",
        "ASCII - Fichas de Dominó/Naipes (B/N)"
    ]

    selected_filter = st.sidebar.selectbox("Selecciona un tipo de ASCII Art:", filter_options)
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    # ------------------------------------
    # Parámetros placeholder (ejemplo)
    # ------------------------------------
    # Dependiendo del tipo de ASCII Art, podrías agregar más controles en el futuro.
    # Por ejemplo:
    if selected_filter == "ASCII - Texto Custom a Color":
        user_text = st.sidebar.text_input("Texto/Frase para el ASCII Art:", value="Mi frase aquí")
        # Este 'user_text' se usará luego para generar el arte con texto personalizado

    # ------------------------------------
    # Layout principal
    # ------------------------------------
    title_col, download_col = st.columns([0.85, 0.15])
    with title_col:
        st.title("Aplicación ASCII Art (Esqueleto)")

    if uploaded_file is not None:
        # Cargamos la imagen original (convertida a RGB por seguridad)
        original_image = Image.open(uploaded_file).convert('RGB')

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                original_image,
                caption="Imagen Original",
                use_container_width=True
            )

        # Aplicamos el "filtro" (realmente es placeholder)
        with col2:
            if selected_filter == "ASCII - Letra (M/@) Color":
                result_image = ascii_art_m_color_placeholder(original_image)
                st.image(
                    result_image,
                    caption="Resultado (Placeholder)",
                    use_container_width=True
                )

            elif selected_filter == "ASCII - Letra (M/@) Gris":
                result_image = ascii_art_m_grayscale_placeholder(original_image)
                st.image(
                    result_image,
                    caption="Resultado (Placeholder)",
                    use_container_width=True
                )

            elif selected_filter == "ASCII - Conjunto de caracteres B/N":
                result_image = ascii_art_chars_bn_placeholder(original_image)
                st.image(
                    result_image,
                    caption="Resultado (Placeholder)",
                    use_container_width=True
                )

            elif selected_filter == "ASCII - Texto Custom a Color":
                # Aquí usaríamos user_text si fuera necesario
                result_image = ascii_art_custom_text_placeholder(original_image)
                st.image(
                    result_image,
                    caption="Resultado (Placeholder)",
                    use_container_width=True
                )

            elif selected_filter == "ASCII - Fichas de Dominó/Naipes (B/N)":
                result_image = ascii_art_domino_cards_placeholder(original_image)
                st.image(
                    result_image,
                    caption="Resultado (Placeholder)",
                    use_container_width=True
                )

            # ----------------------------
            # Botón de descarga (Placeholder)
            # ----------------------------
            with download_col:
                st.write("")
                st.write("")
                buf = BytesIO()
                # Guardamos la imagen resultante en memoria
                result_image.save(buf, format="PNG")

                file_names = {
                    "ASCII - Letra (M/@) Color": "ascii_m_color.png",
                    "ASCII - Letra (M/@) Gris": "ascii_m_gris.png",
                    "ASCII - Conjunto de caracteres B/N": "ascii_chars_bn.png",
                    "ASCII - Texto Custom a Color": "ascii_texto_color.png",
                    "ASCII - Fichas de Dominó/Naipes (B/N)": "ascii_domino.png"
                }

                st.download_button(
                    label="⬇️ Descargar resultado",
                    data=buf.getvalue(),
                    file_name=file_names.get(selected_filter, "ascii_art.png"),
                    mime="image/png"
                )

    else:
        st.info("Por favor, sube una imagen para aplicar un filtro ASCII.")


if __name__ == "__main__":
    main()
