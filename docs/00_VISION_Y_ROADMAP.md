# 00 - Visión y Roadmap del Proyecto

**Fecha de Sincronización:** 16 de Julio de 2025

## 1. Visión General

El objetivo de este proyecto es construir un **asistente de IA personal, multimodal y de arquitectura "Local-First"**.

La filosofía principal es maximizar la **privacidad**, el **rendimiento** y minimizar los costos, ejecutando la mayor cantidad posible de componentes en el hardware local del usuario. Las APIs externas (como Gemini) se utilizan estratégicamente solo cuando es necesario, como una capa de razonamiento superior para tareas complejas o que requieren conocimiento del mundo real.

## 2. Principios Fundamentales

*   **Visión:** Crear un agente de IA que pueda **percibir** (escuchar, leer), **razonar** (usando LLMs locales y externos) y **actuar** (hablar, ejecutar comandos, interactuar con APIs).
*   **Arquitectura "Local-First":** Todo lo que pueda correr localmente, debe correr localmente.
*   **Modularidad:** El sistema se construye como un conjunto de microservicios independientes (TTS, STT, etc.) que se comunican entre sí, facilitando el desarrollo, la depuración y la mejora de cada componente por separado.
*   **Control de Recursos:** El sistema completo debe poder iniciarse y detenerse con comandos simples para no interferir con otras actividades que demanden la GPU (ej. gaming).
*   **Multimodalidad:** La interacción debe ser posible a través de voz y texto.

## 3. Roadmap General

El proyecto se divide en tres fases principales:

### Fase 1: Fundamentos de Voz (En Curso / Casi Completa)
-   **[✅] Objetivo 1.1: Servicio TTS.** Crear y validar un microservicio que convierta texto a audio.
-   **[✅] Objetivo 1.2: Servicio STT.** Diseñar y generar el código para un microservicio que transcriba audio a texto.
-   **[✅] Objetivo 1.3: Infraestructura.** Definir la arquitectura de `docker-compose.yml` para orquestar los servicios.
-   **[▶️] Próximo Paso:** Realizar la prueba de validación final del servicio STT.

### Fase 2: El Cerebro y los Sentidos (Futuro)
-   **Objetivo 2.1: Orquestador.** Crear el script principal que conecte STT -> Ollama -> TTS.
-   **Objetivo 2.2: Listener.** Crear el script de "wake-word" para la captura de audio por micrófono.
-   **Objetivo 2.3: Integración.** Unir todo el flujo de voz.

### Fase 3: Inteligencia y Automatización (Futuro)
-   **Objetivo 3.1: Memoria.** Implementar una base de datos vectorial (RAG) para dar contexto y memoria a largo plazo.
-   **Objetivo 3.2: Canales de Chat.** Integrar con plataformas como WhatsApp o Telegram.
-   **Objetivo 3.3: Playbooks.** Desarrollar sistemas de automatización para tareas complejas.
