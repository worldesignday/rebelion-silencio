import streamlit as st
import anthropic
import json
import os
import pandas as pd
from datetime import datetime

# 1. BASE DE DATOS DE AVATARES
AVATARES = {
    "Marie Curie": "Física y Química, pionera en radioactividad. Enfrentó discriminación académica por ser mujer y extranjera.",
    "Rosalind Franklin": "Biofísica, descubridora clave de la estructura del ADN. Su trabajo fue invisibilizado por colegas hombres.",
    "Ada Lovelace": "Matemática y primera programadora. Visionaria en un mundo de máquinas pensado por hombres.",
    "Katherine Johnson": "Matemática de la NASA. Rompió barreras raciales y de género para calcular trayectorias espaciales.",
    "Grace Hopper": "Pionera de la computación. Creó lenguajes que permitieron que humanos y máquinas hablaran inglés.",
    "Rosa Parks": "Líder civil. Su negativa a ceder el asiento demostró que un acto de dignidad puede cambiar la ley.",
    "Malala Yousafzai": "Activista por la educación. Sobrevivió a la violencia para defender el derecho de las niñas a estudiar.",
    "Margaret Thatcher": "Líder política firme. Conocida como la Dama de Hierro por su determinación inquebrantable.",
    "Benazir Bhutto": "Primera mujer en liderar un país musulmán. Luchó por la democracia frente a grandes peligros.",
    "Angela Merkel": "Científica y líder política. Gobernó con lógica, calma y una influencia global sin precedentes.",
    "Frida Kahlo": "Pintora. Usó el arte para expresar el dolor físico y la identidad, transformando el sufrimiento en belleza.",
    "Virginia Woolf": "Escritora. Exploró la mente femenina y luchó por un espacio propio para la creación de las mujeres.",
    "Coco Chanel": "Diseñadora. Liberó a la mujer de ataduras físicas (el corsé) y sociales a través del estilo.",
    "Oprah Winfrey": "Comunicadora. Superó una infancia de abusos para construir un imperio basado en la empatía y la verdad.",
    "Mary Barra": "Líder industrial. Primera mujer en dirigir General Motors, rompiendo el techo de cristal automotriz.",
    "Ana Botín": "Banquera global. Lidera una de las entidades más grandes del mundo con enfoque en educación y pymes.",
    "Amelia Earhart": "Aviadora. Cruzó el Atlántico sola, demostrando que el cielo no tiene límites para las mujeres.",
    "Serena Williams": "Atleta legendaria. Luchó por la igualdad en el deporte y demostró la fuerza de la mujer negra."
}

# 2. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="La Rebelión del Silencio", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #4B2C6D; color: white; }
    .report-box { background-color: #5D3A82; padding: 25px; border-radius: 15px; border: 1px solid #FF6B35; line-height: 1.6; color: white; }
    .stButton>button { background-color: #FF6B35; color: white !important; border-radius: 25px; height: 3.5em; width: 100%; font-weight: bold; border: none; }
    .stSelectbox label, .stTextArea label, .stRadio label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE PERSISTENCIA
def guardar_en_dashboard(nuevo_dato):
    archivo = "historico_reportes.json"
    historial = []
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding='utf-8') as f:
                historial = json.load(f)
        except: historial = []
    historial.append(nuevo_dato)
    with open(archivo, "w", encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

# 4. NAVEGACIÓN
menu = st.sidebar.radio("Ir a:", ["Portal Estudiante", "Dashboard Interesados"])

if menu == "Portal Estudiante":
    st.title("🦋 La Rebelión del Silencio")
    
    if 'paso' not in st.session_state: st.session_state.paso = 1

    # PASO 1: REPORTE
    if st.session_state.paso == 1:
        st.subheader("Paso 1: REPORTE")
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            u_input = st.selectbox("¿Dónde ocurrió?", ["Baños", "Pasillos", "Cafetería", "Gimnasio", "Salón de clase", "Biblioteca", "Patio", "Ruta Escolar"])
            q_input = st.selectbox("¿Quién fue?", ["Compañero/a", "Docente", "Grupo de estudiantes", "Personal administrativo", "Otro"])
        with col_b:
            c_input = st.selectbox("¿En qué curso estás?", [f"Grado {i}" for i in range(3, 12)])
            f_input = st.selectbox("¿Con qué frecuencia sucede?", ["Es la primera vez", "Ha pasado 2 o 3 veces", "Sucede constantemente"])
        
        r_input = st.text_area("Cuéntanos qué pasó (tus palabras son seguras):", placeholder="Ej: Me escondieron la maleta y se burlaron de mi curso...")
        
        if st.button("Siguiente: Elige tu Voz →"):
            if r_input:
                st.session_state.u, st.session_state.r = u_input, r_input
                st.session_state.f, st.session_state.q = f_input, q_input
                st.session_state.curso = c_input
                st.session_state.paso = 2
                st.rerun()
            else: st.warning("Por favor, cuéntanos qué pasó para poder orientarte.")
        st.markdown('</div>', unsafe_allow_html=True)

    # PASO 2: CREA TU VOZ
    elif st.session_state.paso == 2:
        st.subheader("Paso 2: CREA TU VOZ")
        st.write("Selecciona a la líder que quieres que analice tu situación:")
        avatar_elegido = st.radio("Líderes:", list(AVATARES.keys()), horizontal=True)
        
        if st.button("Generar Acción y Hoja de Ruta ✨"):
            st.session_state.avatar = avatar_elegido
            st.session_state.paso = 3
            st.rerun()

    # PASO 3: TOMA ACCIÓN
    elif st.session_state.paso == 3:
        st.subheader("Paso 3: TOMA ACCIÓN")
        client = anthropic.Anthropic(api_key="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")
        
        with st.spinner(f"{st.session_state.avatar} está analizando tu caso..."):
            contexto = AVATARES[st.session_state.avatar]
            prompt = f"""Eres {st.session_state.avatar}. Imagina que estás sentada en un sitio seguro y tranquilo con un estudiante de {st.session_state.curso} que acaba de confiarte lo siguiente:
                REPORTADO: '{st.session_state.r}' 
                LUGAR: '{st.session_state.u}'
                AGRESOR: {st.session_state.q}
                FRECUENCIA: {st.session_state.f}.

                Tu objetivo es hablarle desde el corazón, como una mentora o amiga mayor, para que no se sienta sola y se motive a actuar.

                ESTRUCTURA DE TU CONSEJO:
                1. "Querida amiga/o,": Inicia con una conexión humana. Cuéntale algo breve de tu vida que se parezca a lo que ella/él siente (dolor, miedo, injusticia) para validar su emoción.
                2. 📚 Lo que dice la ley sobre tu caso: Explica con palabras sencillas (sin dejar de ser técnica) si es Tipo I, II o III según la Ley 1620 y por qué. Menciona la Sentencia T-401 como su respaldo.
                3. ✊ Pasos que SÍ puedes dar: Dale 3 o 4 consejos prácticos y valientes que pueda hacer en el colegio, mencionando el lugar específico ({st.session_state.u}) y al agresor ({st.session_state.q}).
                4. 💛 Recuerda esto: Cierra con una reflexión poderosa sobre el silencio y la voz.

                IMPORTANTE: Mantén un lenguaje cercano para niños y jóvenes. No seas un manual; sé una voz de aliento.

                Al final, incluye estrictamente este JSON para el sistema:
                ```json
                {{
                    "fecha": "{datetime.now()}",
                    "categoria": "Tipo X",
                    "nivel_termometro": 0,
                    "ubicacion_especifica": "{st.session_state.u}",
                    "curso": "{st.session_state.curso}",
                    "agresor": "{st.session_state.q}"
                }}
                ```"""
            
            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1500,
                    system="Eres un experto en justicia restaurativa escolar en Colombia.",
                    messages=[{"role": "user", "content": prompt}]
                )
                texto_ia = response.content[0].text
                mensaje_final = texto_ia.split("```json")[0]
                
                st.markdown(f'<div class="report-box">{mensaje_final}</div>', unsafe_allow_html=True)
                
                json_raw = texto_ia.split("```json")[1].split("```")[0]
                guardar_en_dashboard(json.loads(json_raw))
                
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("Finalizar y Volver al Inicio"):
            st.session_state.paso = 1
            st.rerun()

# 5. DASHBOARD
else:
    st.title("📊 Dashboard para Interesados")
    if os.path.exists("historico_reportes.json"):
        with open("historico_reportes.json", "r", encoding='utf-8') as f:
            df = pd.DataFrame(json.load(f))
        
        c1, c2, c3 = st.columns(3)
        with c1:
            avg = pd.to_numeric(df['nivel_termometro']).mean()
            st.metric("Termómetro Institucional", f"{avg:.1f}%")
        with c2:
            st.write("Zonas Críticas")
            st.bar_chart(df['ubicacion_especifica'].value_counts())
        with c3:
            st.write("Reportes por Grado")
            st.bar_chart(df['curso'].value_counts())
            
        st.write("### Detalle de Incidentes")
        st.dataframe(df[['fecha', 'categoria', 'curso', 'agresor', 'ubicacion_especifica']])
    else:
        st.info("No hay datos aún.")