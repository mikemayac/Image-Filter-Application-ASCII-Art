# Aplicación ASCII Art con Streamlit

### Joel Miguel Maya Castrejón │ mike.maya@ciencias.unam.mx │ 417112602

Este proyecto consiste en una aplicación web interactiva, creada con **Python** y **Streamlit**, que convierte imágenes en diferentes formas de ASCII Art. Cada píxel se analiza y se reemplaza por caracteres que simulan la imagen original. Hay cinco filtros principales:

1. **Letra (M/@) a Color**  
2. **Letra (M/@) en Gris**  
3. **Conjunto de caracteres en B/N**  
4. **Texto personalizado a Color**  
5. **Naipes (en blanco/negro)**

## Requisitos

- Python 3.12 o superior  
- [Streamlit](https://docs.streamlit.io/)  
- [Pillow (PIL)](https://pillow.readthedocs.io/)  

Están listados en el archivo **requirements.txt**.

## Instalación

1. **Clona** o **descarga** el repositorio en tu equipo.
2. Crea un **entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o en Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

1. Dentro del entorno virtual, ubícate donde esté `tarea2_pdi_ASCII_Art.py`.
2. Ejecuta:
   ```bash
   streamlit run tarea2_pdi_ASCII_Art.py
   ```
3. Se abrirá tu navegador con la aplicación. Si no se abre, copia la URL que aparece en la terminal y pégala en tu navegador.

## Uso de la Aplicación

1. **Sube una imagen** (`jpg`, `jpeg` o `png`) desde la barra lateral de Streamlit.
2. **Selecciona** uno de los cinco filtros ASCII:
   - **Letra (M/@) a Color**: Cada bloque de pixeles se convierte en la misma letra con el color promedio.
   - **Letra (M/@) en Gris**: Igual que el anterior, pero en escala de grises.
   - **Conjunto de caracteres en B/N**: Mapea diferentes símbolos a diferentes niveles de brillo (texto negro, fondo blanco).
   - **Texto personalizado a Color**: Se toma una frase del usuario, usando cada caracter en color promedio.
   - **Naipes (B/N)**: Emplea una fuente de cartas para representar distintos niveles de brillo.  
3. **Ajusta** los parámetros (tamaño de celda, letra, frase, etc.) en la barra lateral.
4. Observa el **antes** (columna izquierda) y el **resultado** (columna derecha).
5. **Descarga** la imagen procesada con el botón disponible.

## Estructura

```
├── tarea2_pdi_ASCII_Art.py    # Código principal de la aplicación
├── cards.ttf                  # Fuente local (opcional) para el filtro de naipes
├── requirements.txt           # Dependencias del proyecto
├── .streamlit/                # Configuración opcional de Streamlit
│   └── config.toml
├── README.md                  # Este archivo
└── venv/                      # Entorno virtual (opcional)
```

## Contribuir

1. Haz un **fork** del repositorio.
2. Crea una **rama** para tus cambios: `git checkout -b mi-mejora`.
3. Realiza los cambios y haz commit: `git commit -m "Mi mejora"`.
4. Haz push a tu rama: `git push origin mi-mejora`.
5. Abre un **Pull Request** en el repositorio original.

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).