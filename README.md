# Arquitectura de Microservicios de Voz con NeMo

Este proyecto implementa una arquitectura de microservicios para el procesamiento de voz utilizando los modelos de IA de NVIDIA NeMo. La solución está contenerizada con Docker y orquestada a través de Docker Compose para facilitar su despliegue y escalabilidad.

## Descripción General

El sistema se compone de dos microservicios principales:

1.  **Servicio de Texto a Voz (TTS):** Convierte texto plano en audio de alta calidad.
2.  **Servicio de Voz a Texto (STT):** Transcribe archivos de audio a texto.

Ambos servicios utilizan modelos pre-entrenados de la colección NeMo de NVIDIA y están diseñados para ejecutarse en hardware con aceleración por GPU.

## Componentes del Proyecto

### 1. `api_server.py` - Servicio de Texto a Voz (TTS)

Este script implementa un servidor web con Flask que expone un endpoint para la síntesis de voz.

-   **Framework:** Flask
-   **Modelos NeMo:**
    -   `nvidia/tts_en_fastpitch`: Para la generación de espectrogramas a partir de texto.
    -   `nvidia/tts_hifigan`: Vocoder para convertir los espectrogramas en audio audible.
-   **Endpoint:** `POST /synthesize`
    -   **Entrada:** Un objeto JSON con la clave `text`.
        ```json
        {
          "text": "Hello world! This is a test."
        }
        ```
    -   **Salida:** Un stream de audio en formato `audio/wav`.

### 2. `stt_server.py` - Servicio de Voz a Texto (STT)

Este script implementa un servidor web con Flask para la transcripción de audio.

-   **Framework:** Flask
-   **Modelo NeMo:**
    -   `nvidia/parakeet-tdt-1.1b`: Modelo de Reconocimiento Automático del Habla (ASR) para la transcripción.
-   **Endpoint:** `POST /transcribe`
    -   **Entrada:** Una petición `multipart/form-data` con un campo `audio_file` que contiene el archivo de audio a transcribir.
    -   **Salida:** Un objeto JSON con la clave `text` y el texto transcrito como valor.
        ```json
        {
          "text": "hello world this is a test"
        }
        ```

### 3. `docker-compose.yml` - Orquestación de Servicios

Este archivo define y configura los dos microservicios para que se ejecuten en contenedores Docker aislados.

-   **Servicios Definidos:**
    -   `tts-server`: Expone el puerto `5000`.
    -   `stt-server`: Expone el puerto `5001`.
-   **Imagen Base:** `nvcr.io/nvidia/nemo:25.04` para ambos servicios.
-   **Gestión de GPU:** Configurado para reservar un dispositivo NVIDIA GPU para cada servicio, lo cual es crucial para el rendimiento de los modelos NeMo.
-   **Volúmenes:**
    -   Monta los scripts Python (`.py`) dentro de sus respectivos contenedores.
    -   Utiliza un volumen nombrado (`nemo_model_cache`) para compartir la caché de modelos descargados entre los contenedores. Esto evita descargas duplicadas y acelera el tiempo de inicio.

### 4. `tts_test.py` - Script de Prueba

Un script de utilidad para probar la funcionalidad del modelo TTS de forma local y directa, sin necesidad de levantar el servidor. Genera un archivo `voz_generada.wav`.

## Requisitos

-   Docker
-   Docker Compose
-   NVIDIA Container Toolkit (para soporte de GPU en Docker)
-   Un host con al menos una GPU NVIDIA compatible.

## Cómo Ejecutar el Proyecto

1.  **Asegúrate de tener los drivers de NVIDIA y el NVIDIA Container Toolkit instalados** en la máquina host.

2.  **Levanta los servicios** utilizando Docker Compose:
    ```bash
    docker-compose up --build
    ```
    La primera vez que se ejecute, Docker descargará la imagen de NeMo y los modelos, lo que puede tardar varios minutos.

3.  **Verifica que los contenedores estén en ejecución:**
    ```bash
    docker-compose ps
    ```

## Cómo Usar los Servicios

### Sintetizar Texto a Voz (TTS)

Envía una petición POST al servicio TTS en el puerto `5000`:

```bash
curl -X POST \
  http://localhost:5000/synthesize \
  -H 'Content-Type: application/json' \
  -d '{"text": "This is a test of the text to speech service."}' \
  --output audio_sintetizado.wav
```
Esto guardará la respuesta de audio en un archivo llamado `audio_sintetizado.wav`.

### Transcribir Voz a Texto (STT)

Envía una petición POST con un archivo de audio al servicio STT en el puerto `5001`:

```bash
curl -X POST \
  http://localhost:5001/transcribe \
  -F 'audio_file=@/ruta/a/tu/archivo.wav'
```
La respuesta será un JSON con el texto transcrito.

```