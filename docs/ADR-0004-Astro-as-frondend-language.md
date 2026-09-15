# ADR-0004: Título corto de la decisión

Uso de Astro como framework de desarrollo para el frontend del sistema de finanzas personales

Autores:

- @githubusername
Fecha: AAAA-MM-DD

## Estado

Propuesto

## Contexto

El sistema de finanzas personales requiere una interfaz web (frontend) ágil y eficiente para la visualización de datos financieros, tableros (dashboards), gráficos y formularios de entrada de datos, la cual debe desacoplarse del núcleo de procesamiento lógico construido en Python.

## Decisión

Proponemos utilizar Astro como el framework de desarrollo para la interfaz web del sistema de finanzas personales. Astro actuará como una capa desacoplada que consumirá los datos financieros del backend en Python, aprovechando su renderizado ultra rápido y su capacidad de entregar cero JavaScript por defecto para garantizar una experiencia de usuario ágil y ligera.

## Alternativas consideradas

Interfaz por Consola (CLI) en Python: Es la más fácil de implementar, pero ofrece una experiencia de usuario (UX) deficiente para analizar datos financieros y gráficos complejos.

React / Next.js: Frameworks excelentes, pero envían una cantidad masiva de JavaScript al navegador que es innecesaria para esta escala, aumentando la complejidad técnica del frontend de manera innecesaria.

## Consecuencias

Positivas:

    Separación clara de responsabilidades mediante una arquitectura cliente-servidor limpia, permitiendo el trabajo en paralelo del equipo.

    Rendimiento óptimo con páginas de resumen que cargan instantáneamente (HTML puro) y uso opcional de islas de interactividad solo cuando se requieran gráficos complejos.

    Independencia tecnológica total frente al backend de Python.

Negativas / Riesgos:

    Posible complejidad o fricción en el manejo de estado global e intercambio local de datos (CORS o lectura mutua de archivos) si el entorno de desarrollo local entre Astro y Python no se documenta adecuadamente.

    Se requiere definir si se utilizará renderizado estático (SSG) con archivos locales o renderizado en servidor (SSR).
