# Agente Experto: 03 - Acción

**Alias:** "Las Manos", "El Ejecutor"

## 1. Propósito y Directiva Principal

La misión del Agente de Acción es **interactuar con sistemas fuera del propio cerebro del asistente**. Es el puente entre la decisión de "hacer algo" y la ejecución real de esa tarea. Su objetivo es traducir una intención en un resultado tangible.

## 2. Responsabilidades Clave

-   **Catálogo de Herramientas:** Mantener un registro de las "herramientas" disponibles (ej. `buscar_en_web`, `ejecutar_comando_terminal`, `controlar_luz_inteligente`).
-   **Parseo de Comandos:** Recibir una petición del Orquestador (ej. `{ "herramienta": "buscar_en_web", "parametros": { "query": "NVIDIA" } }`) y entender qué herramienta invocar y con qué argumentos.
-   **Ejecución Segura:** Ejecutar la herramienta solicitada. Esto es especialmente crítico para herramientas como `ejecutar_comando_terminal`, que deben tener mecanismos de seguridad (sandboxing, comandos permitidos, etc.).
-   **Formateo de Resultados:** Tomar la salida cruda de la herramienta (ej. el texto de una página web, la salida de un comando) y formatearla en un resumen o una estructura clara que el Orquestador pueda entender y usar.

## 3. Lógica de Decisión (Borrador)

```plaintext
FUNCIÓN ejecutar_accion(peticion_accion):
  1. Parsear la [peticion_accion] para obtener `nombre_herramienta` y `parametros`.
  2. ¿Existe `nombre_herramienta` en mi catálogo de herramientas?
     SI:
       a. Llamar a la función interna correspondiente a la herramienta (ej. `self._buscar_en_web(parametros)`).
       b. Recibir el resultado crudo de la función.
       c. Formatear el resultado en una cadena de texto limpia.
       d. Devolver el resultado formateado.
     NO:
       - Devolver un mensaje de error: "Error: Herramienta desconocida."

# Ejemplo de una función de herramienta interna
FUNCIÓN _buscar_en_web(parametros):
  - Usar una API de búsqueda (ej. Brave, DuckDuckGo) con `parametros['query']`.
  - Obtener los resultados.
  - Devolver los fragmentos de texto más relevantes.
```

## 4. Herramientas y Colaboradores

-   **Bibliotecas Potenciales:**
    -   `requests` (para APIs REST).
    -   `subprocess` (para ejecutar comandos de terminal de forma segura).
    -   APIs específicas de servicios (ej. `spotipy` para Spotify, `pytube` para YouTube).
    -   Herramientas de web scraping como `BeautifulSoup`.
-   **Colabora con:**
    -   **Orquestador:** Es invocado por el Orquestador cuando una petición del usuario requiere una acción en el mundo real.
    -   **LLM (indirectamente):** A menudo, el LLM es el que decide que se necesita una herramienta y formatea la `peticion_accion` que el Orquestador luego pasa a este agente.
-   **Es invocado por:** El `Agente Orquestador`.
