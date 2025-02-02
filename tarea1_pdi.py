import streamlit as st
from PIL import Image

# Configuración de la página en modo ancho
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

            # Calculamos el color promedio en el bloque
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

            # Asignamos ese color promedio a todos los pixeles del bloque
            for by in range(y, min(y + block_size, height)):
                for bx in range(x, min(x + block_size, width)):
                    pixels_mosaic[bx, by] = (avg_r, avg_g, avg_b)

    return image


def grayscale_filter(original_image, method="average"):
    """
    Convierte una imagen a escala de grises de dos maneras:
    1) Promedio: (R + G + B) / 3
    2) Ponderado: (0.3*R + 0.7*G + 0.1*B)

    :param original_image: Imagen PIL original.
    :param method: "average" o "weighted".
    :return: Nueva imagen en escala de grises.
    """
    image = original_image.copy()
    pixels_original = original_image.load()
    pixels_gray = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels_original[x, y]

            if method == "average":
                # gris = (R + G + B) / 3
                gray_value = (r + g + b) // 3
            else:
                # gris = (R*0.3) + (G*0.7) + (B*0.1)
                gray_value = int(0.3 * r + 0.7 * g + 0.1 * b)

            # Ajustamos a (gray, gray, gray)
            pixels_gray[x, y] = (gray_value, gray_value, gray_value)

    return image


def high_contrast_filter(original_image, method="average", threshold=128):
    """
    Crea un filtro de alto contraste a partir de la imagen original:
      1. Se convierte a escala de grises (usando average o weighted).
      2. Se aplica un umbral para determinar si cada píxel es negro o blanco.

    :param original_image: Imagen PIL original.
    :param method: Método de gris ("average" o "weighted").
    :param threshold: Umbral de corte para el alto contraste.
    :return: Imagen en blanco y negro (alto contraste).
    """
    # 1. Convertimos a escala de grises (reutilizamos la función anterior)
    gray_image = grayscale_filter(original_image, method=method)

    # 2. Aplicamos el umbral
    width, height = gray_image.size
    pixels = gray_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]  # en gris, r = g = b
            if r < threshold:
                # Píxel negro
                pixels[x, y] = (0, 0, 0)
            else:
                # Píxel blanco
                pixels[x, y] = (255, 255, 255)

    return gray_image


def negative_filter(original_image):
    """
    Filtro inverso o negativo de la imagen.
    Para cada píxel (r, g, b), el nuevo píxel será (255-r, 255-g, 255-b).
    """
    image = original_image.copy()
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            pixels[x, y] = (255 - r, 255 - g, 255 - b)

    return image


def rgb_filter_channel_only(original_image, channel="red"):
    """
    Filtro que conserva únicamente el canal especificado (R, G o B)
    y pone a 0 los otros canales.

    channel = "red"   -> (r, 0, 0)
    channel = "green" -> (0, g, 0)
    channel = "blue"  -> (0, 0, b)
    """
    image = original_image.copy()
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if channel == "red":
                new_r, new_g, new_b = (r, 0, 0)
            elif channel == "green":
                new_r, new_g, new_b = (0, g, 0)
            elif channel == "blue":
                new_r, new_g, new_b = (0, 0, b)
            else:
                # Por si acaso hay un valor no esperado,
                # devolvemos el píxel tal cual.
                new_r, new_g, new_b = r, g, b

            pixels[x, y] = (new_r, new_g, new_b)

    return image



def main():
    st.sidebar.title("Configuraciones y Filtros")

    filter_options = [
        "Mosaico",
        "Tono de gris",
        "Alto contraste",
        "Inverso",
        "Filtro RGB",
        "Brillo (pendiente)"
    ]

    selected_filter = st.sidebar.selectbox("Selecciona un filtro:", filter_options)
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    # Parámetros
    block_size = 10
    grayscale_method = "average"
    high_contrast_threshold = 128
    rgb_choice = "red"  # Rojo por defecto

    if selected_filter == "Mosaico":
        block_size = st.sidebar.number_input(
            "Tamaño de la cuadrícula (px):",
            min_value=1,
            max_value=100,
            value=10
        )

    elif selected_filter == "Tono de gris":
        grayscale_choice = st.sidebar.radio(
            "Método de conversión a gris",
            ("(R+G+B)/3", "(0.3*R) + (0.7*G) + (0.1*B)")
        )
        if grayscale_choice == "(R+G+B)/3":
            grayscale_method = "average"
        else:
            grayscale_method = "weighted"

    elif selected_filter == "Alto contraste":
        grayscale_choice = st.sidebar.radio(
            "Método de conversión a gris",
            ("(R+G+B)/3", "(0.3*R) + (0.7*G) + (0.1*B)")
        )
        if grayscale_choice == "(R+G+B)/3":
            grayscale_method = "average"
        else:
            grayscale_method = "weighted"

        high_contrast_threshold = st.sidebar.slider(
            "Umbral para alto contraste",
            min_value=0,
            max_value=255,
            value=128
        )

    elif selected_filter == "Filtro RGB":
        # Elegimos uno de los 3 canales para saturarlo
        rgb_channel = st.sidebar.radio(
            "Elige el canal a saturar:",
            ("Rojo", "Verde", "Azul")
        )
        if rgb_channel == "Rojo":
            rgb_choice = "red"
        elif rgb_channel == "Verde":
            rgb_choice = "green"
        else:
            rgb_choice = "blue"

    st.title("Aplicación de Filtros de Imágenes")

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                original_image,
                caption="Imagen Original",
                use_container_width=True
            )

        with col2:
            if selected_filter == "Mosaico":
                result_image = mosaic_filter(original_image, block_size)
                st.image(
                    result_image,
                    caption="Imagen con Filtro Mosaico",
                    use_container_width=True
                )

            elif selected_filter == "Tono de gris":
                result_image = grayscale_filter(original_image, grayscale_method)
                st.image(
                    result_image,
                    caption="Imagen en Escala de Grises",
                    use_container_width=True
                )

            elif selected_filter == "Alto contraste":
                result_image = high_contrast_filter(
                    original_image,
                    method=grayscale_method,
                    threshold=high_contrast_threshold
                )
                st.image(
                    result_image,
                    caption="Imagen con Alto Contraste",
                    use_container_width=True
                )

            elif selected_filter == "Inverso":
                result_image = negative_filter(original_image)
                st.image(
                    result_image,
                    caption="Imagen Inversa (Negativo)",
                    use_container_width=True
                )

            elif selected_filter == "Filtro RGB":
                result_image = rgb_filter_channel_only(original_image, channel=rgb_choice)
                st.image(
                    result_image,
                    caption=f"Imagen con Filtro RGB ({rgb_choice.upper()})",
                    use_container_width=True
                )

            else:
                st.warning("Este filtro todavía no está implementado.")
    else:
        st.info("Por favor, sube una imagen para aplicar un filtro.")


if __name__ == "__main__":
    main()