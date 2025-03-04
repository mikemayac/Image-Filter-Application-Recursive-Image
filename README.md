# Filtro de Imagen Recursiva con Streamlit

### Joel Miguel Maya Castrejón │ mike.maya@ciencias.unam.mx │ 417112602

Este proyecto consiste en una aplicación web interactiva creada con **Python** y **Streamlit** que permite aplicar un filtro **recursivo** (o tipo fotomosaico fractal) a una imagen. La idea principal es **dividir** la imagen en bloques y **reemplazar** cada bloque por la propia imagen reescalada, ajustando los colores para que coincidan con el color promedio del bloque. Esto crea un efecto en el que la imagen está compuesta “infinitamente” de versiones en miniatura de sí misma (se suele realizar solo una o pocas iteraciones para no alargar el tiempo de cómputo).

## Requisitos

- Python 3.12 o superior.
- [Streamlit](https://docs.streamlit.io/) para el desarrollo de la interfaz.
- [Pillow](https://pillow.readthedocs.io/) (PIL) para leer y manipular las imágenes.

En el archivo **requirements.txt** están listadas las dependencias necesarias (Streamlit y Pillow). Asegúrate de instalarlas antes de ejecutar la aplicación.

## Instalación

1. **Clona** o **descarga** este repositorio en tu máquina local.
2. Crea un **entorno virtual** (opcional, pero recomendado) e instálalo:
   ```bash
   python -m venv venv
   source venv/bin/activate        # En Linux/Mac
   # o en Windows: venv\Scripts\activate
   ```
3. Instala los paquetes necesarios:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de la Aplicación

1. Dentro del entorno virtual y en la carpeta donde se encuentra el archivo principal (`imagen_recursiva.py`, por ejemplo), ejecuta:
   ```bash
   streamlit run imagen_recursiva.py
   ```
2. Automáticamente se abrirá tu navegador mostrando la interfaz de la aplicación. Si no se abre, puedes copiar la URL que aparece en la terminal y pegarla en tu navegador.

## Uso de la Aplicación

1. **Sube una imagen** en la barra lateral (sidebar). Acepta formatos `JPG`, `JPEG` o `PNG`. En caso de que la imagen esté en formato RGBA, se convierte a RGB.
2. **Selecciona** el tamaño de bloque en píxeles (por ejemplo, 10 px).
3. Observa cómo se muestra la **imagen original** en la columna izquierda y la **imagen resultante** (recursiva) en la columna derecha.
4. Puedes **descargar** la imagen procesada con el botón que aparece en la parte superior derecha.

### Explicación del Filtro Recursivo

- El filtro divide la imagen en bloques de tamaño fijo (por ejemplo 10×10).  
- Para cada bloque, se calcula el **color promedio** y se redimensiona la imagen original a un “tile” (o bloque) de 10×10.  
- Se **ajustan** los colores de ese tile al promedio del bloque para mantener la coherencia.  
- Finalmente, se pega ese tile “recoloreado” en el sitio del bloque.  
- Si se deseara mayor “recursividad”, se podría repetir este proceso sobre la imagen resultante, aunque aumenta mucho el tiempo de procesamiento.

## Estructura del Proyecto

```
├── imagen_recursiva.py    # Código principal de la aplicación
│── .streamlit/            # Carpeta de configuración de Streamlit
│    └── config.toml       
├── README.md              # Archivo de documentación
├── requirements.txt       # Dependencias del proyecto
└── venv/                  # Entorno virtual (opcional)
```
