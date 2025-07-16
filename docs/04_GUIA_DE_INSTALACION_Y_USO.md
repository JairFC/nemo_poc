# 04 - Guía de Instalación y Uso

**Fecha de Sincronización:** 16 de Julio de 2025

Esta guía proporciona los pasos necesarios para levantar el entorno de desarrollo y probar los servicios.

## 1. Requisitos Previos

-   **Sistema Operativo:** Linux o Windows con WSL2.
-   **Hardware:** Una GPU NVIDIA con soporte para CUDA.
-   **Software:**
    -   Drivers de NVIDIA actualizados en el host.
    -   Docker y Docker Compose.
    -   NVIDIA Container Toolkit (para habilitar el acceso a la GPU desde los contenedores).

## 2. Levantando los Servicios

Todos los servicios están orquestados a través de Docker Compose. Para iniciarlos, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
# Levanta los contenedores en modo "detached" (en segundo plano)
# --build asegura que se reconstruyan las imágenes si hay cambios en los Dockerfiles (no aplica aquí, pero es buena práctica)
docker-compose up -d --build
```

La primera vez que se ejecute este comando, Docker descargará la imagen base de NeMo (`~88 GB`) y los modelos (`~5 GB`), lo cual puede tardar un tiempo considerable dependiendo de tu conexión a internet. En ejecuciones posteriores, el inicio será casi instantáneo.

### Comandos Útiles de Docker Compose:

-   **Verificar el estado de los servicios:**
    ```bash
    docker-compose ps
    ```
-   **Ver los logs de los servicios en tiempo real:**
    ```bash
    docker-compose logs -f
    ```
-   **Detener y eliminar los contenedores:**
    ```bash
    docker-compose down
    ```

## 3. Cómo Interactuar con los Servicios

Una vez que los servicios estén en ejecución, puedes interactuar con ellos usando `curl` o cualquier cliente de API.

### Probar el Servicio TTS (Texto a Voz)

-   **Endpoint:** `http://localhost:5000/synthesize`
-   **Método:** `POST`

```bash
# Envía una petición con texto y guarda la salida de audio en un archivo
curl -X POST \
  http://localhost:5000/synthesize \
  -H 'Content-Type: application/json' \
  -d '{"text": "This is a test of the text to speech service."}' \
  --output prueba_tts.wav
```

### Probar el Servicio STT (Voz a Texto)

-   **Endpoint:** `http://localhost:5001/transcribe`
-   **Método:** `POST`

```bash
# Envía un archivo de audio .wav y recibe la transcripción en formato JSON
# Asegúrate de reemplazar 'voz_generada.wav' con la ruta a un archivo de audio real.
curl -X POST \
  http://localhost:5001/transcribe \
  -F 'audio_file=@voz_generada.wav'
```
La salida esperada es un objeto JSON como este:
```json
{
  "text": "hello world i am alive and this time it works"
}
```
