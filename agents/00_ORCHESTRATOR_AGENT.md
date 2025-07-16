# Agente Experto: 00 - Orquestador

**Alias:** "El Cerebro", "El Director del Proyecto"

## 1. Propósito y Directiva Principal

El Orquestador es el agente de más alto nivel. Su única y más importante misión es **recibir una petición del usuario y delegarla al agente experto adecuado**. No debe realizar el trabajo por sí mismo; su habilidad es saber quién es el mejor para cada tarea.

## 2. Responsabilidades Clave

-   **Punto de Entrada:** Es el primer agente en recibir el texto limpio y la intención del usuario.
-   **Análisis de Tareas:** Analiza la petición para determinar la naturaleza de la tarea (ej: ¿es una pregunta?, ¿es un comando?, ¿requiere memoria?, ¿es una comunicación?).
-   **Delegación Inteligente:** Basado en el análisis, invoca a uno o más agentes expertos en la secuencia correcta.
-   **Composición de Respuestas:** Recibe los resultados de los agentes expertos y compone la respuesta final que se enviará al usuario (generalmente a través del servicio TTS).
-   **Gestión de Estado:** Mantiene el estado de la conversación a corto plazo.

## 3. Lógica de Decisión (Borrador)

```plaintext
CUANDO recibo una petición:
  1. ¿La petición requiere información de conversaciones pasadas?
     SI -> Invocar al **Agente de Memoria** para enriquecer la petición con contexto.

  2. ¿La petición es un comando para actuar en el sistema o en el mundo exterior (ej: "busca en la web", "pon música")?
     SI -> Invocar al **Agente de Acción** con los parámetros necesarios.

  3. ¿La petición es una interacción a través de un canal de chat (Telegram, etc.)?
     SI -> Invocar al **Agente de Comunicación** para manejar el formato.

  4. ¿La petición es una pregunta o una conversación general?
     SI -> (Por defecto) Enviar la petición (con contexto, si se obtuvo) al **LLM (Ollama/Gemini)** para generar una respuesta conversacional.

  5. ¿La respuesta final debe ser almacenada para el futuro?
     SI -> Invocar al **Agente de Memoria** para guardar la interacción.

  6. Componer la respuesta final y enviarla al servicio TTS.
```

## 4. Herramientas y Colaboradores

-   **Invoca a:**
    -   `Agente de Memoria`
    -   `Agente de Acción`
    -   `Agente de Comunicación`
    -   Servicios de LLM (Ollama, Gemini)
    -   Servicio TTS (para la respuesta final)
-   **Es invocado por:** El bucle principal de la aplicación, después de que el `Agente Listener` y el servicio STT hayan hecho su trabajo.
