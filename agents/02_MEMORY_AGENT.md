# Agente Experto: 02 - Memoria

**Alias:** "El Archivista", "El Historiador"

## 1. Propósito y Directiva Principal

La misión del Agente de Memoria es **proporcionar al asistente un sentido del contexto y la continuidad**, almacenando y recuperando interacciones pasadas de manera eficiente. Su objetivo es transformar una serie de preguntas y respuestas aisladas en una conversación coherente.

## 2. Responsabilidades Clave

-   **Almacenamiento de Interacciones:** Guardar las tuplas de (pregunta del usuario, respuesta del asistente) en una base de datos vectorial.
-   **Creación de Embeddings:** Convertir el texto de las interacciones en vectores numéricos (embeddings) para poder realizar búsquedas semánticas.
-   **Recuperación de Contexto (RAG):** Dada una nueva petición del usuario, buscar en la base de datos las interacciones pasadas más relevantes semánticamente.
-   **Enriquecimiento de Prompts:** Proporcionar el contexto recuperado al Orquestador para que este pueda añadirlo al prompt que se envía al LLM, mejorando así la calidad y coherencia de la respuesta.
-   **Gestión de la Base de Datos:** Manejar la inicialización y la conexión con la base de datos vectorial.

## 3. Lógica de Decisión (Borrador)

```plaintext
FUNCIÓN almacenar_memoria(peticion, respuesta):
  1. Concatenar: "Usuario dijo: [peticion]. Asistente respondió: [respuesta]".
  2. Generar el embedding del texto concatenado.
  3. Almacenar el texto y su embedding en la base de datos vectorial.

FUNCIÓN recuperar_contexto(peticion_actual, top_k=3):
  1. Generar el embedding de la [peticion_actual].
  2. Realizar una búsqueda de similitud en la base de datos vectorial usando el embedding.
  3. Obtener los `top_k` resultados más relevantes.
  4. Formatear los resultados como una cadena de texto: "Contexto de conversaciones pasadas: [resultado1], [resultado2], ...".
  5. Devolver la cadena de texto de contexto.
```

## 4. Herramientas y Colaboradores

-   **Bibliotecas Potenciales:**
    -   **Base de Datos Vectorial:** `ChromaDB`, `FAISS`, `LanceDB` (opciones locales excelentes).
    -   **Modelos de Embeddings:** `SentenceTransformers` (para generar los vectores desde el texto).
-   **Colabora con:**
    -   **Orquestador:** El Orquestador es su único cliente. Lo invoca para guardar nuevas memorias o para recuperar contexto antes de llamar a un LLM.
-   **Es invocado por:** El `Agente Orquestador`.
