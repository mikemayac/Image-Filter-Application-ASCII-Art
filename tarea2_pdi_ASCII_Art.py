import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Configuración de la página en modo ancho
st.set_page_config(page_title="ASCII Art - Esqueleto", layout="wide")

# =============================================================================
# FUNCIONES PLACEHOLDER / DEFINITIVAS
# =============================================================================
def get_text_dimensions(draw, text, font):
    """
    Devuelve (ancho, alto) de la cadena 'text' usando 'font',
    intentando primero textbbox (Pillow >= 8.0) y, si no existe,
    recurre a getmask (funciona en Pillow más antiguas).
    """
    if hasattr(draw, "textbbox"):
        # pillow >= 8.0
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    else:
        # Fallback: obtener ancho y alto del "mask" (funciona en versiones antiguas)
        mask = font.getmask(text)
        return mask.size


def ascii_art_m_color(original_image, cell_size=10, character="M"):
    width, height = original_image.size
    pixels = original_image.load()

    new_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(new_image)

    try:
        # Si tienes la fuente TTF
        # font = ImageFont.truetype("arial.ttf", cell_size)
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            sum_r, sum_g, sum_b = 0, 0, 0
            count = 0

            for by in range(y, min(y + cell_size, height)):
                for bx in range(x, min(x + cell_size, width)):
                    r, g, b = pixels[bx, by]
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1

            avg_r = sum_r // count
            avg_g = sum_g // count
            avg_b = sum_b // count
            fill_color = (avg_r, avg_g, avg_b)

            # Usamos la función auxiliar para obtener el ancho/alto del caracter
            text_w, text_h = get_text_dimensions(draw, character, font)

            cx = x + (cell_size - text_w) // 2
            cy = y + (cell_size - text_h) // 2

            draw.text((cx, cy), character, font=font, fill=fill_color)

    return new_image



def ascii_art_m_grayscale(original_image, cell_size=10, character="M"):
    """
    Convierte la imagen en ASCII usando la misma letra (M/@),
    pero en tonos de gris (el gris promedio de cada bloque).
    """
    # Dimensiones de la imagen
    width, height = original_image.size
    pixels = original_image.load()

    # Nueva imagen en blanco donde dibujar el resultado
    new_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(new_image)

    # Cargar fuente
    try:
        # font = ImageFont.truetype("arial.ttf", cell_size)
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Recorremos en bloques de cell_size
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            sum_r, sum_g, sum_b = 0, 0, 0
            count = 0

            # Calcular color promedio del bloque
            for by in range(y, min(y + cell_size, height)):
                for bx in range(x, min(x + cell_size, width)):
                    r, g, b = pixels[bx, by]
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1

            avg_r = sum_r // count
            avg_g = sum_g // count
            avg_b = sum_b // count

            # Convertimos a gris (promedio)
            gray_value = (avg_r + avg_g + avg_b) // 3
            fill_color = (gray_value, gray_value, gray_value)

            # Medir el carácter y centrarlo
            text_w, text_h = get_text_dimensions(draw, character, font)
            cx = x + (cell_size - text_w) // 2
            cy = y + (cell_size - text_h) // 2

            # Dibujar la letra en tonos de gris
            draw.text((cx, cy), character, font=font, fill=fill_color)

    return new_image


def ascii_art_chars_bn(original_image, cell_size=10):
    """
    Convierte la imagen en ASCII usando un conjunto de caracteres en B/N
    (simulando distintos niveles de brillo). No hay color ni grises en el texto,
    solo texto negro sobre fondo blanco.
    """
    width, height = original_image.size
    pixels = original_image.load()

    # Escala de caracteres (desde "más oscuro" hasta "más claro")
    # Puedes ajustar o reordenar a tu gusto. El último puede ser un espacio en blanco.
    # Ejemplo: "MNH#QNAO0Y2$%+.- "
    char_scale = "MNH#QNAO0Y2$%+.- "

    # Nueva imagen en blanco (fondo) donde dibujaremos el resultado
    new_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(new_image)

    # Cargamos la fuente (prueba con load_default o con una fuente TTF)
    try:
        # font = ImageFont.truetype("arial.ttf", cell_size)
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Recorremos la imagen en bloques de cell_size
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            sum_r, sum_g, sum_b = 0, 0, 0
            count = 0

            # Calculamos el brillo promedio en el bloque
            for by in range(y, min(y + cell_size, height)):
                for bx in range(x, min(x + cell_size, width)):
                    r, g, b = pixels[bx, by]
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1

            avg_r = sum_r // count
            avg_g = sum_g // count
            avg_b = sum_b // count

            # Brillo en [0..255]
            brightness = (avg_r + avg_g + avg_b) // 3

            # Mapeamos el brillo a un índice de la escala de caracteres
            # Escala normaliza de 0..255 -> 0..(len(char_scale)-1)
            num_chars = len(char_scale)
            char_index = brightness * (num_chars - 1) // 255
            chosen_char = char_scale[char_index]

            # Medimos el tamaño del carácter
            text_w, text_h = get_text_dimensions(draw, chosen_char, font)

            # Calculamos posición para centrarlo dentro del bloque
            cx = x + (cell_size - text_w) // 2
            cy = y + (cell_size - text_h) // 2

            # Dibujamos con tinta negra (0,0,0)
            draw.text((cx, cy), chosen_char, font=font, fill=(0, 0, 0))

    return new_image


def ascii_art_custom_text_color(original_image, cell_size=10, user_text="Hola"):
    """
    Convierte la imagen en ASCII usando un texto/frase definido por el usuario.
    Cada bloque se dibuja con el siguiente carácter de 'user_text',
    rellenado con el color promedio de ese bloque.
    """
    width, height = original_image.size
    pixels = original_image.load()

    # Crear una nueva imagen en blanco (RGB) donde dibujar el resultado
    new_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(new_image)

    # Cargar la fuente (puede ser la por defecto o una TTF)
    try:
        # font = ImageFont.truetype("arial.ttf", cell_size)
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Asegurarnos de tener al menos 1 caracter en user_text para evitar divisiones por cero
    if len(user_text) == 0:
        user_text = " "  # Si está vacío, forzamos un espacio

    text_index = 0
    text_length = len(user_text)

    # Recorrer la imagen en bloques de cell_size
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            sum_r, sum_g, sum_b = 0, 0, 0
            count = 0

            # Calculamos el color promedio
            for by in range(y, min(y + cell_size, height)):
                for bx in range(x, min(x + cell_size, width)):
                    r, g, b = pixels[bx, by]
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1

            avg_r = sum_r // count
            avg_g = sum_g // count
            avg_b = sum_b // count

            fill_color = (avg_r, avg_g, avg_b)

            # Tomar el siguiente carácter de la frase
            current_char = user_text[text_index]
            text_index = (text_index + 1) % text_length  # avanzar y hacer wrap

            # Medir el tamaño del carácter para centrarlo
            text_w, text_h = get_text_dimensions(draw, current_char, font)
            cx = x + (cell_size - text_w) // 2
            cy = y + (cell_size - text_h) // 2

            draw.text((cx, cy), current_char, font=font, fill=fill_color)

    return new_image


def ascii_art_domino_cards_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando símbolos de dominó
    o naipes, en blanco/negro, que representen distintos niveles de brillo.
    (Pendiente de implementar)
    """
    return original_image

# =============================================================================
# FUNCIÓN PRINCIPAL DE STREAMLIT
# =============================================================================

def main():
    st.sidebar.title("Configuraciones y ASCII Art")

    filter_options = [
        "ASCII - Letra (M/@) Color",
        "ASCII - Letra (M/@) Gris",
        "ASCII - Conjunto de caracteres B/N",
        "ASCII - Texto Custom a Color",
        "ASCII - Fichas de Dominó/Naipes (B/N)"
    ]

    selected_filter = st.sidebar.selectbox("Selecciona un tipo de ASCII Art:", filter_options)
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    # Parámetros para cada filtro
    if selected_filter == "ASCII - Letra (M/@) Color":
        cell_size = st.sidebar.slider("Tamaño de celda (px)", 1, 50, 10)
        character_choice = st.sidebar.radio("Elige la letra:", ("M", "@"))

    elif selected_filter == "ASCII - Letra (M/@) Gris":
        cell_size = st.sidebar.slider("Tamaño de celda (px)", 1, 50, 10)
        character_choice = st.sidebar.radio("Elige la letra:", ("M", "@"))

    elif selected_filter == "ASCII - Conjunto de caracteres B/N":
        cell_size = st.sidebar.slider("Tamaño de celda (px)", 1, 50, 10)
        st.sidebar.info("Usa un conjunto de caracteres en B/N para simular distintos niveles de brillo.")

    elif selected_filter == "ASCII - Texto Custom a Color":
        cell_size = st.sidebar.slider("Tamaño de celda (px)", 1, 50, 10)
        user_text = st.sidebar.text_input("Texto/Frase para el ASCII Art:", value="Mi frase aquí")
        st.sidebar.info("Cada celda se dibujará con el siguiente caracter de tu frase, en el color promedio de la región.")

    # Layout principal
    title_col, download_col = st.columns([0.85, 0.15])
    with title_col:
        st.title("Aplicación ASCII Art")

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file).convert('RGB')

        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="Imagen Original", use_container_width=True)

        with col2:
            if selected_filter == "ASCII - Letra (M/@) Color":
                result_image = ascii_art_m_color(original_image, cell_size, character_choice)
                st.image(result_image, caption="ASCII con color", use_container_width=True)

            elif selected_filter == "ASCII - Letra (M/@) Gris":
                result_image = ascii_art_m_grayscale(original_image, cell_size, character_choice)
                st.image(result_image, caption="ASCII en gris", use_container_width=True)

            elif selected_filter == "ASCII - Conjunto de caracteres B/N":
                result_image = ascii_art_chars_bn(original_image, cell_size)
                st.image(result_image, caption="ASCII en B/N", use_container_width=True)

            elif selected_filter == "ASCII - Texto Custom a Color":
                # Nueva función implementada
                result_image = ascii_art_custom_text_color(original_image, cell_size, user_text)
                st.image(result_image, caption="ASCII con texto custom a color", use_container_width=True)

            elif selected_filter == "ASCII - Fichas de Dominó/Naipes (B/N)":
                result_image = ascii_art_domino_cards_placeholder(original_image)
                st.image(result_image, caption="Resultado (Placeholder)", use_container_width=True)

            # Botón de descarga
            with download_col:
                st.write("")
                st.write("")
                buf = BytesIO()
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