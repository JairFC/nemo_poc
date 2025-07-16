# Agente Experto: 01 - Listener

**Alias:** "El Oído", "El Vigilante"

## 1. Propósito y Directiva Principal

La misión del Listener es **escuchar de forma pasiva, eficiente y privada por una palabra clave (wake-word)** y, solo al detectarla, capturar el audio de la petición del usuario de manera clara y concisa.

## 2. Responsabilidades Clave

-   **Escucha Pasiva:** Monitorear el stream de audio del micrófono por defecto de forma continua y con un consumo de recursos mínimo.
-   **Detección de Wake-Word:** Utilizar una librería eficiente (ej. `openwakeword`, `picovoice`) para identificar la palabra clave específica.
-   **Grabación de Audio:** Una vez detectada la wake-word, comenzar a grabar el audio del usuario.
-   **Detección de Silencio:** Detectar el final de la locución del usuario (ej. tras 1-2 segundos de silencio) para detener la grabación.
-   **Envío a STT:** Tomar el audio grabado, guardarlo en un formato estándar (ej. `.wav`) y enviarlo al endpoint `/transcribe` del microservicio STT.

## 3. Lógica de Decisión (Borrador)

```plaintext
INICIAR:
  1. Abrir el stream de audio del micrófono por defecto.
  2. Cargar el modelo de wake-word.

BUCLE INFINITO:
  1. Leer un fragmento del stream de audio.
  2. Pasarlo al modelo de wake-word.
  3. ¿Se ha detectado la palabra clave en el fragmento?
     SI:
       a. Reproducir un sonido de activación (opcional).
       b. Iniciar un buffer de grabación.
       c. Entrar en modo "Grabando Petición":
          i. Continuar grabando audio en el buffer.
          ii. Monitorear el nivel de sonido para detectar silencio.
          iii. ¿Se ha detectado silencio prolongado?
              SI:
                - Detener la grabación.
                - Guardar el buffer como un archivo `peticion.wav`.
                - Enviar `peticion.wav` al servicio STT.
                - Salir del modo "Grabando Petición" y volver al bucle principal.
     NO:
       - Descartar el fragmento y continuar el bucle.
```

## 4. Herramientas y Colaboradores

-   **Bibliotecas Potenciales:**
    -   `openwakeword`
    -   `Picovoice Porcupine`
    -   `PyAudio` (para la interacción con el micrófono)
-   **Colabora con:**
    -   **Servicio STT:** Es el cliente principal de este servicio. Le proporciona el audio grabado.
-   **Es invocado por:** El inicio de la aplicación principal. Es uno de los primeros procesos en lanzarse.
