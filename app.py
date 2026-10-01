import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar el diseño
st.markdown("""
    <style>
    /* Estilo para las tarjetas de métricas */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 10px;
    }
    
    /* Personalización del área de texto */
    .stTextArea textarea {
        border-radius: 10px;
    }

    /* Estilo de los contenedores de frases */
    .phrase-box-pos {
        border-left: 5px solid #28a745;
        background-color: rgba(40, 167, 69, 0.05);
        padding: 12px 15px;
        border-radius: 4px 8px 8px 4px;
        margin-bottom: 12px;
    }
    .phrase-box-neg {
        border-left: 5px solid #dc3545;
        background-color: rgba(220, 53, 69, 0.05);
        padding: 12px 15px;
        border-radius: 4px 8px 8px 4px;
        margin-bottom: 12px;
    }
    .phrase-box-neu {
        border-left: 5px solid #6c757d;
        background-color: rgba(108, 117, 125, 0.05);
        padding: 12px 15px;
        border-radius: 4px 8px 8px 4px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal estilizado
st.title("✨ Analizador de Texto Inteligente")
st.caption("Procesamiento de Lenguaje Natural simplificado con TextBlob & Streamlit")
st.divider()

# Barra lateral
st.sidebar.image("https://img.icons8.com/isometric/512/text.png", width=80)
st.sidebar.title("Panel de Control")
modo = st.sidebar.radio(
    "Selecciona el modo de entrada:",
    ["✍️ Texto directo", "📁 Archivo de texto"]
)

st.sidebar.divider()
st.sidebar.info("💡 **Tip:** El análisis de sentimiento traduce el texto internamente al inglés para obtener mayor precisión.")

# Función para contar palabras
def contar_palabras(texto):
    stop_words = set([
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
        "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
        "ellas", "ellos", "en", "entre", "era", "eras", "es", "esa", "esas", "ese",
        "eso", "esos", "esta", "estas", "este", "esto", "estos", "ha", "había", "han",
        "has", "hasta", "he", "la", "las", "le", "les", "lo", "los", "me", "mi", "mía",
        "mías", "mío", "míos", "mis", "mucho", "muchos", "muy", "nada", "ni", "no", "nos",
        "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os", 
        "otra", "otras", "otro", "otros", "para", "pero", "poco", "por", "porque", "que", 
        "quien", "quienes", "qué", "se", "sea", "sean", "según", "si", "sido", "sin", 
        "sobre", "sois", "somos", "son", "soy", "su", "sus", "suya", "suyas", "suyo", 
        "suyos", "también", "tanto", "te", "tenéis", "tenemos", "tener", "tengo", "ti", 
        "tiene", "tienen", "todo", "todos", "tu", "tus", "tuya", "tuyas", "tuyo", "tuyos", 
        "tú", "un", "una", "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras", 
        "vuestro", "vuestros", "y", "ya", "yo",
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", 
        "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", 
        "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", 
        "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", 
        "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", 
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", 
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's", 
        "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", 
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", 
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", 
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])
    
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words and len(palabra) > 2]
    
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    return contador_ordenado, palabras_filtradas

translator = Translator()

def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]
    
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })
    
    contador_palabras, palabras = contar_palabras(texto_ingles)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# Función visual mejorada para mostrar resultados
def crear_visualizaciones(resultados):
    st.markdown("### 📊 Métrica Global")
    
    # Tarjetas Métricas
    m1, m2, m3 = st.columns(3)
    
    sent = resultados["sentimiento"]
    if sent > 0.05:
        estado_sent = "Positivo 😊"
    elif sent < -0.05:
        estado_sent = "Negativo 😟"
    else:
        estado_sent = "Neutral 😐"

    subj = resultados["subjetividad"]
    estado_subj = "Subjetivo 💭" if subj > 0.5 else "Objetivo 📋"

    m1.metric("Sentimiento", f"{sent:.2f}", delta=estado_sent)
    m2.metric("Subjetividad", f"{subj:.2f}", delta=estado_subj, delta_color="off")
    m3.metric("Total Palabras Analizadas", len(resultados["palabras"]))

    st.divider()

    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.container(border=True):
            st.subheader("🎯 Desglose de Polaridad")
            
            sentimiento_norm = (resultados["sentimiento"] + 1) / 2
            st.write("**Sentimiento General**")
            st.progress(sentimiento_norm)
            
            st.write("**Subjetividad General**")
            st.progress(resultados["subjetividad"])

    with col2:
        with st.container(border=True):
            st.subheader("🔝 Palabras Más Frecuentes")
            if resultados["contador_palabras"]:
                palabras_top = dict(list(resultados["contador_palabras"].items())[:8])
                st.bar_chart(palabras_top, height=200)
            else:
                st.info("No hay suficiente texto para mostrar palabras frecuentes.")

    # Texto traducido con acordeón mejorado
    st.subheader("📄 Comparativa de Traducción")
    with st.expander("Ver vista paralela (Español / Inglés)"):
        col_orig, col_trad = st.columns(2)
        with col_orig:
            st.markdown("**Original (ES):**")
            st.info(resultados["texto_original"])
        with col_trad:
            st.markdown("**Traducción (EN):**")
            st.success(resultados["texto_traducido"])

    # Análisis de frases por tarjetas ordenadas
    st.subheader("🔍 Análisis Detallado por Frase")
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            
            try:
                blob_frase = TextBlob(frase_traducida)
                sent_f = blob_frase.sentiment.polarity
                
                if sent_f > 0.05:
                    css_class = "phrase-box-pos"
                    tag = "😊 Positivo"
                elif sent_f < -0.05:
                    css_class = "phrase-box-neg"
                    tag = "😟 Negativo"
                else:
                    css_class = "phrase-box-neu"
                    tag = "😐 Neutral"
                
                st.markdown(f"""
                <div class="{css_class}">
                    <small><b>Frase {i}</b> — {tag} (Polaridad: {sent_f:.2f})</small><br>
                    <b>Original:</b> "{frase_original}"<br>
                    <span style="color: #6c757d;"><b>Traducción:</b> "{frase_traducida}"</span>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.write(f"**{i}.** {frase_original}")
    else:
        st.info("No se detectaron frases estructuradas.")

# Selección del modo de entrada
if modo == "✍️ Texto directo":
    st.subheader("Ingresa el texto a procesar")
    texto = st.text_area("", height=180, placeholder="Escribe o pega tu texto aquí para comenzar el análisis...")
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        btn_analizar = st.button("🚀 Analizar Texto", use_container_width=True, type="primary")

    if btn_analizar:
        if texto.strip():
            with st.spinner("Procesando y calculando métricas..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("⚠️ El campo de texto está vacío. Por favor escribe algo.")

elif modo == "📁 Archivo de texto":
    st.subheader("Carga un documento")
    archivo = st.file_uploader("Formatos permitidos: .txt, .csv, .md", type=["txt", "csv", "md"])
    
    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("👁️ Previsualización del archivo"):
                st.code(contenido[:1000] + ("..." if len(contenido) > 1000 else ""), language="text")
            
            if st.button("🚀 Analizar Archivo", type="primary"):
                with st.spinner("Procesando archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

# Pie de página
st.divider()
st.caption("Desarrollado con ❤️ usando Streamlit & TextBlob")
