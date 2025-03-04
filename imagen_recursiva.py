import streamlit as st
from PIL import Image
from io import BytesIO
import math

# Configuración de la página (título y layout en modo "wide")
st.set_page_config(page_title="Imagen Recursiva", layout="wide")

def recolor_image(image, target_avg, block_avg):
    """
    Re-colorea la 'image' (que ya está escalada al tamaño del bloque)
    para que su color promedio se aproxime al del bloque en la imagen original.

    :param image: Imagen PIL escalada, en RGB.
    :param target_avg: (r, g, b) promedio de la imagen escalada.
    :param block_avg: (r, g, b) promedio del bloque en la imagen original.
    :return: Imagen re-coloreada para que su promedio sea block_avg.
    """

    # Desempaquetar colores promedio
    tr, tg, tb = target_avg
    br, bg, bb = block_avg

    # Evitar divisiones por cero si el target_avg es (0,0,0)
    # (caso muy raro, pero por seguridad)
    if tr == 0: tr = 1
    if tg == 0: tg = 1
    if tb == 0: tb = 1

    # Creamos una copia
    recolored = image.copy()
    pix = recolored.load()
    width, height = recolored.size

    # Diferencia promedio (cuánto queremos desplazar)
    # En lugar de un simple offset, hacemos un factor multiplicativo
    # para manejar mejor la re-escalada de colores.
    # Otra alternativa es un desplazamiento lineal, pero el multiplicador
    # conserva mejor la variación de tonos.
    # factor = block_avg / target_avg (en cada canal)
    factor_r = (br / tr)
    factor_g = (bg / tg)
    factor_b = (bb / tb)

    for y in range(height):
        for x in range(width):
            r, g, b = pix[x, y]
            # Re-escalamos cada canal
            nr = int(r * factor_r)
            ng = int(g * factor_g)
            nb = int(b * factor_b)
            # Limitamos a [0..255]
            nr = max(0, min(255, nr))
            ng = max(0, min(255, ng))
            nb = max(0, min(255, nb))
            pix[x, y] = (nr, ng, nb)

    return recolored


def compute_average_color(image, x0, y0, block_size):
    """
    Calcula el color promedio (RGB) de un bloque de la imagen original
    que inicia en (x0, y0) y tiene tamaño block_size x block_size.
    """
    width, height = image.size
    pix = image.load()

    sum_r = sum_g = sum_b = 0
    count = 0

    for y in range(y0, min(y0 + block_size, height)):
        for x in range(x0, min(x0 + block_size, width)):
            r, g, b = pix[x, y]
            sum_r += r
            sum_g += g
            sum_b += b
            count += 1

    if count == 0:
        return (0, 0, 0)

    return (sum_r // count, sum_g // count, sum_b // count)


def compute_image_average_color(image):
    """
    Devuelve el color promedio de *toda* la imagen.
    Útil para saber el promedio de la versión escalada (target_avg).
    """
    pix = image.load()
    width, height = image.size
    sum_r = sum_g = sum_b = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pix[x, y]
            sum_r += r
            sum_g += g
            sum_b += b

    total_pixels = width * height
    return (sum_r // total_pixels, sum_g // total_pixels, sum_b // total_pixels)


def recursive_image_filter(original_image, block_size=10):
    """
    Crea una nueva imagen donde cada bloque de tamaño (block_size x block_size)
    en la imagen original es reemplazado por la imagen completa (reducida) y
    re-coloreada para que coincida con el promedio de color de ese bloque.

    :param original_image: Imagen PIL (RGB).
    :param block_size: Tamaño del bloque en píxeles (ejemplo 10).
    :return: Imagen resultante con el efecto "recursivo".
    """

    width, height = original_image.size
    # Imagen de salida (mismo tamaño que la original)
    new_image = Image.new("RGB", (width, height))

    # Escalamos la imagen original al tamaño de bloque
    scaled_image = original_image.resize((block_size, block_size), Image.Resampling.LANCZOS)
    # Promedio de color de la imagen escalada
    target_avg_color = compute_image_average_color(scaled_image)

    # Recorremos la imagen en bloques
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Promedio de color en el bloque de la imagen original
            block_avg_color = compute_average_color(original_image, x, y, block_size)

            # Recoloreamos la versión escalada para adecuarla al color del bloque
            recolored_tile = recolor_image(scaled_image, target_avg_color, block_avg_color)

            # Pegamos el tile recoloreado en la posición (x, y) de la nueva imagen
            new_image.paste(recolored_tile, (x, y))

    return new_image


def main():
    # Título en la barra lateral
    st.sidebar.title("Imagen Recursiva")

    # Solo un filtro (Recursivo), sin selectbox
    st.sidebar.info("Este filtro crea un mosaico 'fractal' con la misma imagen.")

    # Parámetro: tamaño de bloque
    block_size = st.sidebar.slider(
        "Tamaño del bloque (px)",
        min_value=1,
        max_value=50,
        value=10
    )

    # Carga de archivo
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    # Encabezado y columna para el botón de descarga
    title_col, download_col = st.columns([0.85, 0.15])
    with title_col:
        st.title("Filtro de Imagen Recursiva")

    if uploaded_file is not None:
        # Cargar la imagen en PIL y convertirla a RGB
        original_image = Image.open(uploaded_file).convert('RGB')

        # Mostramos dos columnas: original y resultado
        col1, col2 = st.columns(2)

        with col1:
            st.image(
                original_image,
                caption="Imagen Original",
                use_container_width=True
            )

        # -- Aquí aplicamos el filtro recursivo --
        result_image = recursive_image_filter(original_image, block_size)

        with col2:
            st.image(
                result_image,
                caption="Imagen Recursiva",
                use_container_width=True
            )

            with download_col:
                st.write("")  # Espacio
                st.write("")
                buf = BytesIO()
                result_image.save(buf, format="PNG")

                st.download_button(
                    label="⬇️ Descargar imagen",
                    data=buf.getvalue(),
                    file_name="imagen_recursiva.png",
                    mime="image/png"
                )
    else:
        st.info("Por favor, sube una imagen para aplicar el filtro recursivo.")


# Punto de entrada
if __name__ == "__main__":
    main()
