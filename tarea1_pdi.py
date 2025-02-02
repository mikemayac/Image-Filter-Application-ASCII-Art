import streamlit as st
from PIL import Image

# 1. Configuramos la página para que sea de ancho completo
st.set_page_config(page_title="Aplicación de Filtros", layout="wide")


def mosaic_filter(original_image, block_size=10):
    """
    Aplica un filtro de mosaico a la imagen original.
    :param original_image: Imagen PIL original.
    :param block_size: Tamaño de cada bloque (cuadrícula) en pixeles.
    :return: Nueva imagen con efecto de mosaico.
    """
    image = original_image.copy()
    width, height = image.size
    pixels_original = original_image.load()
    pixels_mosaic = image.load()

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            sum_r, sum_g, sum_b = 0, 0, 0
            count = 0

            for by in range(y, min(y + block_size, height)):
                for bx in range(x, min(x + block_size, width)):
                    r, g, b = pixels_original[bx, by]
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1

            avg_r = sum_r // count
            avg_g = sum_g // count
            avg_b = sum_b // count

            for by in range(y, min(y + block_size, height)):
                for bx in range(x, min(x + block_size, width)):
                    pixels_mosaic[bx, by] = (avg_r, avg_g, avg_b)

    return image


def main():
    # 2. Usamos la barra lateral para opciones
    st.sidebar.title("Configuraciones y Filtros")

    # Opciones de filtros (solo implementaremos el de Mosaico por ahora)
    filter_options = [
        "Mosaico",
        "Tono de gris (pendiente)",
        "Alto contraste (pendiente)",
        "Inverso (pendiente)",
        "Filtro RGB (pendiente)",
        "Brillo (pendiente)"
    ]

    selected_filter = st.sidebar.selectbox("Selecciona un filtro:", filter_options)

    # Cargamos la imagen
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    # Parámetro para el filtro de mosaico
    block_size = 10  # Valor por defecto
    if selected_filter == "Mosaico":
        block_size = st.sidebar.number_input("Tamaño de la cuadrícula (px):",
                                             min_value=1,
                                             max_value=100,
                                             value=10)

    # 3. Encabezado principal
    st.title("Aplicación de Filtros de Imágenes")

    # 4. Mostrar resultados en el área principal
    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)

        # Creamos columnas para mostrar imágenes en paralelo
        col1, col2 = st.columns(2)

        with col1:
            st.image(original_image,
                     caption="Imagen Original",
                     use_container_width=True)

        with col2:
            if selected_filter == "Mosaico":
                mosaic_result = mosaic_filter(original_image, block_size)
                st.image(mosaic_result,
                         caption="Imagen con Filtro Mosaico",
                         use_container_width=True)
            else:
                st.warning("Este filtro todavía no está implementado.")
    else:
        st.info("Por favor, sube una imagen para aplicar un filtro.")


if __name__ == "__main__":
    main()
