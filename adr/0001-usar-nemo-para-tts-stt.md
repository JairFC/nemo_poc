# ADR 0001: Usar NVIDIA NeMo para los microservicios de TTS y STT

-   **Estado:** Aceptado
-   **Fecha:** 2025-07-16

## Contexto

El proyecto requiere capacidades de Texto-a-Voz (TTS) y Voz-a-Texto (STT) que sean de alto rendimiento, alta fidelidad y que puedan ejecutarse localmente en hardware de consumidor con GPU (NVIDIA RTX 3080). La arquitectura "Local-First" es un principio fundamental del proyecto.

## Decisión

Hemos decidido utilizar el framework **NVIDIA NeMo** para implementar los microservicios de TTS y STT. Los servicios se ejecutarán en contenedores Docker utilizando la imagen oficial de NeMo (`nvcr.io/nvidia/nemo`).

-   **Para TTS:** Usaremos la combinación de los modelos `FastPitch` y `HifiGan`.
-   **Para STT:** Usaremos el modelo `Parakeet-TDT-1.1b`.

## Consecuencias

### Positivas:
-   **Rendimiento:** NeMo está optimizado para GPUs NVIDIA, lo que garantiza la mejor performance posible en el hardware objetivo.
-   **Calidad:** Los modelos pre-entrenados de NeMo ofrecen una calidad de síntesis y transcripción de vanguardia.
-   **Consistencia:** Usar un solo framework para ambas tareas de voz simplifica el stack tecnológico.
-   **Facilidad de Despliegue:** La imagen oficial de Docker contiene todas las dependencias, eliminando la complejidad de la configuración del entorno.

### Negativas:
-   **Tamaño:** La imagen de Docker de NeMo y los modelos son muy grandes (decenas de GB), lo que resulta en un uso de disco considerable y tiempos de descarga iniciales largos.
-   **Acoplamiento al Hardware:** La solución está fuertemente acoplada al ecosistema de NVIDIA. No funcionará en hardware de otros fabricantes (AMD, Intel). Dado que el hardware objetivo es una RTX 3080, esta consecuencia es aceptable.
