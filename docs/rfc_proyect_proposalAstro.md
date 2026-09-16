# Astro as frontend framework

Autores:

- @desainea

## 1 TL;DR

Proponemos utilizar Astro como el framework de desarrollo para la interfaz web (frontend) del sistema de finanzas personales. Astro actuará como una capa desacoplada que consumirá los datos financieros del backend en Python, aprovechando su renderizado ultra rápido y su capacidad de entregar cero JavaScript por defecto para garantizar una experiencia de usuario ágil y ligera

## 2 Motivación

La motivación principal es aplicar el principio de separación de responsabilidades mediante una arquitectura cliente-servidor limpia.En un sistema de finanzas, el usuario interactúa constantemente con tableros, gráficos y formularios de entrada de datos. Al elegir Astro, resolvemos tres problemas críticos:Rendimiento óptimo: Las páginas estáticas de resumen cargan instantáneamente (HTML puro) y solo se añade interactividad donde se necesita.Independencia tecnológica: El frontend queda completamente aislado del backend de Python. Esto simula un entorno real de desarrollo de software donde el equipo de frontend puede avanzar sin depender de la infraestructura del backend y Astro permite usar HTML/CSS estándar o integrar componentes reactivos (como React o Vue) solo si los gráficos financieros interactivos lo requieren.

## 3 Propuesta de implementación

Astro se estructurará como una aplicación web independiente que se comunicará con el backend de Python a través de una interfaz de comunicación clara (archivos JSON locales en la fase inicial, o peticiones HTTP/Fetch en una fase posterior).

 Astro Web App ──► (Peticiones de Datos / JSON) ──► [ Backend: Python Core ]
          │                                                            │
          ▼                                                            ▼
(Renderiza HTML estático +                                    (Procesa reglas de negocio
 Islas de interactividad para gráficos)                        y cálculos financieros)

## 4 Métricas

Monitorearemos el impacto de Astro a través de las siguientes métricas de software:

Métricas de Core Web Vitals (Performance): Mantener un puntaje de Lighthouse > 95% en rendimiento y accesibilidad, gracias al renderizado estático de Astro.

Tamaño del Bundle de JavaScript: Vigilar que las páginas que no requieran interactividad (como los reportes históricos o términos de uso) tengan un peso de 0 KB de JavaScript enviado al cliente.

Tiempo de Compilación (Build Time): Medir cuánto tarda Astro en generar el sitio estático completo a medida que agregamos más páginas a la interfaz.

## 5 Riesgos e inconvenientes

Complejidad en el manejo de estado global: Fricción en la comunicación local: Si el backend de Python y el frontend de Astro corren localmente en la computadora del evaluador de la materia, configurar el intercambio de datos (CORS o lectura mutua de archivos) puede generar problemas de entorno de desarrollo si no se documenta bien el despliegue.

## 6 Alternativas

Interfaz por Consola (CLI) en Python: Es la más fácil de hacer, pero ofrece una experiencia de usuario (UX) deficiente para analizar datos financieros y gráficos complejos.React

Next.js: Frameworks excelentes, pero envían una cantidad masiva de JavaScript al navegador que es innecesaria para un proyecto de esta escala, aumentando la complejidad técnica del frontend innecesariamente.

## 7 Impacto potencial y dependencias

Dado que las finanzas son datos sensibles, el frontend de Astro no debe almacenar credenciales ni datos financieros crudos de forma permanente en el código cliente. Las páginas dinámicas deben renderizarse del lado del servidor (SSR) o protegerse mediante validación estricta de rutas. Impacto en el equipo: Al dividir el proyecto en Frontend (Astro) y Backend (Python), dos integrantes del grupo pueden trabajar de forma 100% paralela definiendo previamente un contrato de datos (API/JSON), reduciendo los conflictos en Git.

## 8 Preguntas sin resolver

¿Adoptaremos el modo estático de Astro (SSG) leyendo datos mediante archivos locales en tiempo de compilación, o usaremos el modo de renderizado en el servidor (SSR) para consultar al backend en tiempo real por cada clic del usuario?

¿Qué librería visual ligera (ej. Tailwind CSS o Vanilla CSS) utilizaremos para garantizar que la interfaz sea responsiva y limpia?

## 9 Conclusión

Adoptar Astro para el frontend dota al proyecto de un estándar de arquitectura profesional. Demuestra que el equipo no se limitó a la terminal de comandos, sino que diseñó una solución con un desacoplamiento claro, enfocada en la velocidad de carga y en una experiencia visual óptima para que el usuario controle sus finanzas personales de manera eficiente.

<!--

## 10 El proceso (elimina esta sección)

Al escribir un RFC, estas incluyendo al equipo en la dirección que estas tomando. En muchos casos puede haber multiples soluciones, y tambien opiniones diferentes sobre como atacar un problema. Es posible que en el futuro esta propuesta no sea la mejor solución posible, pero aprenderemos de ella.

Como proponente, estas tomando responsabilidad sobre la dirección que quieres tomar y con este documento buscas que tus otros miembros de nuestro equipo contribuyan con sus comentarios acerca de tu idea, pero ultimamente esta decision es tuya y te apoyamos.

En resumen, este documento es:
 - un ejercicio de pensamiento, prototipamos con palabras
 - un record historico, y su valor puede disminuir con el tiempo
 - un mecanismo para
 - una forma de transmitir información
 - un mecanismo para construir confianza
 - una herramienta de empoderamiento
 - un canal de comunicación

Este documento no es
 - una solucitud de permiso
 - un documento que requiere aprobación
 - la representación actual de nuestros sistemas o procesos
 -

-->
<!--

- [ ] Copia este template
- [ ] Bosqueja el documento, piensa que es un wireframe en prosa
- [ ] Compartelo con personas de tu equipo para retroalimentación inicial
- [ ] Envíalo como un pull request
- [ ] Etiquétalo para que sea facil categorizarlo
- [ ] Compartelo con todas las personas a quien les pueda interesar
- [ ] Comunica un limite de tiempo razonable dependiendo de la complejidad de la decisión
- [ ] Pidele a dos personas que entiendan el probelma que lo revisen por tí, o pidele ayuda a tu manager
- [ ] Hazle merge con dos +1

### Recomendaciones

- Utiliza la etiqueta [WIP] si aún estas refinando detalles
- Utiliza la etiqueta [newbie] si tienes una propuesta en la que tienes poca confianza por tu conocimiento actual
- Si hay areas específicas en las que quieres atencion, etiqueta a personas que consideras que saben algo al respecto y preguntales directamente. "María, impacto crees que va a tener este API sobre tu base de datos?"
- Si tienes dudas, pídele ayuda a tu manager o lider de tecnología
- Es tu decisión
- Ten en cuenta la prioridad de las propuestas que estas haciendo, los RFC no son documentos para proponer rearquitecturas o proyectos "cool" que no se alinean con los objetivos a corto plazo de la empresa

-->