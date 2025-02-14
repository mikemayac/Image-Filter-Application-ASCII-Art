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



def ascii_art_m_grayscale_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando la misma letra (M/@)
    en tonos de gris.
    (Pendiente de implementar)
    """
    return original_image

def ascii_art_chars_bn_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando un conjunto de caracteres
    en blanco y negro, simulando distintos niveles de brillo.
    (Pendiente de implementar)
    """
    return original_image

def ascii_art_custom_text_placeholder(original_image):
    """
    Placeholder para convertir la imagen en ASCII usando un texto o frase
    definida por el usuario, con el color promedio real de la imagen.
    (Pendiente de implementar)
    """
    return original_image

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

    # Parámetros comunes o específicos
    if selected_filter == "ASCII - Letra (M/@) Color":
        # Tamaño de celda
        cell_size = st.sidebar.slider(
            "Tamaño de celda (px)",
            min_value=1,
            max_value=50,
            value=10
        )
        # Elección de carácter
        character_choice = st.sidebar.radio(
            "Elige la letra:",
            ("M", "@")
        )

    if selected_filter == "ASCII - Texto Custom a Color":
        user_text = st.sidebar.text_input("Texto/Frase para el ASCII Art:", value="Mi frase aquí")
        # (luego se podrá usar en la función real)

    title_col, download_col = st.columns([0.85, 0.15])
    with title_col:
        st.title("Aplicación ASCII Art")

    if uploaded_file is not None:
        # Cargar la imagen original (convertida a RGB)
        original_image = Image.open(uploaded_file).convert('RGB')

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                original_image,
                caption="Imagen Original",
                use_container_width=True
            )

        # Aplicar el filtro correspondiente
        with col2:
            if selected_filter == "ASCII - Letra (M/@) Color":
                # Llamamos a nuestra función ya implementada
                result_image = ascii_art_m_color(original_image,
                                                 cell_size=cell_size,
                                                 character=character_choice)
                st.image(
                    result_image,
                    caption=f"ASCII Art con '{character_choice}' a color",
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
                # Aquí usaríamos user_text en el futuro
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
                    label="⬇️ Descargar",
                    data=buf.getvalue(),
                    file_name=file_names.get(selected_filter, "ascii_art.png"),
                    mime="image/png"
                )

    else:
        st.info("Por favor, sube una imagen para aplicar un filtro ASCII.")


if __name__ == "__main__":
    main()
