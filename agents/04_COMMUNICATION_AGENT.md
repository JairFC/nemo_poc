# Agente Experto: 04 - Comunicación

**Alias:** "El Mensajero", "El Diplomático"

## 1. Propósito y Directiva Principal

La misión del Agente de Comunicación es **gestionar la interacción a través de diferentes canales de texto**, como Telegram, WhatsApp o una terminal de chat. Su objetivo es abstraer la complejidad de cada plataforma, permitiendo que el Orquestador se comunique de manera agnóstica al canal.

## 2. Responsabilidades Clave

-   **Conexión de Canales:** Establecer y mantener la conexión con las APIs de los diferentes servicios de mensajería.
-   **Recepción y Normalización:** Escuchar por mensajes entrantes en todos los canales configurados. Al recibir un mensaje, lo transforma a un formato interno estándar (ej. `{ "id_canal": "telegram", "id_usuario": "12345", "texto": "Hola mundo" }`) antes de pasarlo al Orquestador.
-   **Envío y Formateo:** Recibir una respuesta en formato estándar del Orquestador y traducirla al formato específico requerido por el canal de origen para enviarla de vuelta al usuario correcto.
-   **Manejo de Medios:** Gestionar la descarga de archivos (ej. notas de voz de WhatsApp) y la subida de respuestas que no son de texto (ej. imágenes generadas).

## 3. Lógica de Decisión (Borrador)

```plaintext
# Lógica para un bot de Telegram
FUNCIÓN iniciar_bot_telegram():
  1. Conectar a la API de Telegram con el token.
  2. Establecer un manejador para mensajes nuevos (`on_message`).

FUNCIÓN on_message(mensaje):
  1. Extraer `chat_id`, `user_id`, `texto` del objeto `mensaje` de Telegram.
  2. Crear un objeto de petición normalizado:
     `peticion = { "id_canal": "telegram", "id_usuario": user_id, "chat_id": chat_id, "texto": texto }`
  3. Invocar al **Orquestador** con `peticion`.
  4. Recibir `respuesta_texto` del Orquestador.
  5. Usar la API de Telegram para enviar `respuesta_texto` al `chat_id` original.

# Lógica genérica de envío
FUNCIÓN enviar_respuesta(respuesta_obj):
  - `canal = respuesta_obj['id_canal']`
  - SI `canal` es "telegram":
      - llamar a la función de envío de Telegram.
  - SI `canal` es "whatsapp":
      - llamar a la función de envío de WhatsApp.
```

## 4. Herramientas y Colaboradores

-   **Bibliotecas Potenciales:**
    -   `python-telegram-bot`
    -   `twilio` (para WhatsApp)
    -   `discord.py`
-   **Colabora con:**
    -   **Orquestador:** Es la puerta de entrada y salida para todas las interacciones que no provienen del `Agente Listener` (voz). Le pasa las peticiones normalizadas y recibe las respuestas para enviarlas.
-   **Es invocado por:** Las APIs de las plataformas de mensajería (a través de webhooks o polling). Actúa como un servidor independiente para estas comunicaciones.
