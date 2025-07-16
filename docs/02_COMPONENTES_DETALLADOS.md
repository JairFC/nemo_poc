# 02 - Componentes Detallados del Sistema

**Fecha de Sincronización:** 16 de Julio de 2025

Este documento detalla cada uno de los componentes de software que conforman el asistente.

---

### 1. Servicio de Texto a Voz (TTS)

-   **Archivo Fuente:** `api_server.py`
-   **Estado:** **Completo y Validado.**
-   **Descripción:** Un microservicio basado en Flask que convierte cadenas de texto en audio de alta fidelidad.
-   **Tecnología Clave:**
    -   **Framework:** Flask
    -   **Modelos NeMo:**
        -   `nvidia/tts_en_fastpitch`: Generador de espectrogramas.
        -   `nvidia/tts_hifigan`: Vocoder para la síntesis de audio.
-   **Endpoint API:**
    -   **Ruta:** `POST /synthesize`
    -   **Puerto (local):** `5000`
    -   **Entrada:** `Content-Type: application/json`
        ```json
        {
          "text": "Hello world! This is a test."
        }
        ```
    -   **Salida:** Un stream de datos binarios en formato `audio/wav`.

---

### 2. Servicio de Voz a Texto (STT)

-   **Archivo Fuente:** `stt_server.py`
-   **Estado:** **Diseñado y Pendiente de Prueba Final.**
-   **Descripción:** Un microservicio basado en Flask que transcribe archivos de audio a texto.
-   **Tecnología Clave:**
    -   **Framework:** Flask
    -   **Modelo NeMo:**
        -   `nvidia/parakeet-tdt-1.1b`: Modelo de reconocimiento de voz de 1.1 mil millones de parámetros.
-   **Endpoint API:**
    -   **Ruta:** `POST /transcribe`
    -   **Puerto (local):** `5001`
    -   **Entrada:** `Content-Type: multipart/form-data`
        -   Un campo llamado `audio_file` que contiene el archivo de audio (ej. `.wav`).
    -   **Salida:** `Content-Type: application/json`
        ```json
        {
          "text": "hello world this is a test"
        }
        ```

---

### 3. Orquestador / Cerebro

-   **Archivo Fuente:** (Aún no creado)
-   **Estado:** **Futuro.**
-   **Descripción:** Será el script principal de Python que unirá todos los servicios. Su responsabilidad es gestionar el flujo completo de una interacción: recibir el texto del STT, decidir a qué LLM consultar, procesar la respuesta y enviarla al TTS.

---

### 4. Razonamiento (LLM)

-   **Estado:** **Configurado (Ollama) y Planeado (Gemini).**
-   **Descripción:** El componente responsable de la "inteligencia" y la generación de respuestas.
-   **Tecnología Clave:**
    -   **Ollama:** Para ejecución de LLMs de forma local (ej. Llama 3, Mistral). Ya está instalado en el sistema (`v0.9.6`). Será la opción por defecto para mantener la privacidad.
    -   **Gemini API:** Se usará como un "escape" para consultas que requieran conocimiento del mundo real, información actualizada o un razonamiento más complejo que el que pueden ofrecer los modelos locales.

---

### 5. Infraestructura de Orquestación

-   **Archivo Fuente:** `docker-compose.yml`
-   **Estado:** **Completo y Validado.**
-   **Descripción:** Define la configuración para ejecutar los servicios de TTS y STT en contenedores Docker.
-   **Puntos Clave:**
    -   Utiliza la imagen oficial `nvcr.io/nvidia/nemo:25.04`.
    -   Asigna recursos de GPU a cada contenedor.
    -   Gestiona un volumen persistente (`nemo_model_cache`) para evitar descargar los modelos repetidamente.
