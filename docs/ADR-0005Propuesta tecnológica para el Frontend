# ADR-0005: Selección del framework CSS para el frontend

## Uso de Bootstrap como framework CSS para el frontend del sistema de finanzas personales

**Autores:**

* @mguativa

**Fecha:** 2026-09-28

## Estado

Propuesto

## Contexto

El sistema de finanzas personales requiere una interfaz web clara, organizada y adaptable a diferentes tamaños de pantalla. El frontend será desarrollado utilizando Astro, decisión establecida en el ADR-0004, y deberá proporcionar las interfaces necesarias para el registro y consulta de ingresos y gastos, gestión de categorías y cuentas, visualización de balances, generación de reportes y presentación de información mediante un dashboard.

Para el desarrollo de la interfaz se requiere una solución que facilite la implementación de elementos visuales comunes, como botones, formularios, tablas, tarjetas, menús de navegación y estructuras responsivas, de tal forma que se pueda
reducir el tiempo dedicado a la implementación de estilos básicos

Por lo tanto, se debe seleccionar un framework CSS que pueda integrarse con Astro.

## Decisión

Se propone utilizar **Bootstrap como framework CSS para el desarrollo de la interfaz del sistema**, integrado con Astro.

Astro continuará siendo el framework encargado de estructurar y desarrollar las páginas y componentes del frontend, mientras que Bootstrap proporcionará estilos, componentes visuales y herramientas para facilitar el diseño responsivo de la aplicación.

Bootstrap será utilizado para elementos como:

* Botones.
* Formularios.
* Tablas.
* Tarjetas.
* Menús de navegación.
* Alertas.
* Contenedores y sistemas de distribución.
* Elementos adaptables a diferentes tamaños de pantalla.

Cuando los componentes proporcionados por Bootstrap no sean suficientes para las necesidades específicas del proyecto, se podrá utilizar CSS personalizado de manera complementaria.

Esta decisión no modifica la elección de Astro establecida en el ADR-0004. Ambas tecnologías tendrán responsabilidades diferentes dentro del frontend.

## Alternativas consideradas

### Tailwind CSS

Tailwind CSS fue considerado como alternativa debido a que proporciona clases utilitarias que permiten construir interfaces con un alto nivel de personalización.

Sin embargo, su enfoque requiere definir una mayor cantidad de clases directamente en los elementos de la interfaz y puede implicar un mayor trabajo inicial para establecer los estilos y componentes visuales del sistema, lo cual sería innecesario para nuestro proyecto teniendo en cuenta que bootstrap también permite realizar diseños personalizados.

### CSS sin framework

También se consideró utilizar únicamente CSS desarrollado por el equipo.

Esta alternativa permitiría un control completo sobre los estilos y evitaría depender de un framework externo. Sin embargo, requeriría implementar manualmente componentes y comportamientos visuales comunes, además de establecer desde cero elementos relacionados con el diseño responsivo.


## Consecuencias

### Positivas

* Facilita la creación de una interfaz consistente.
* Proporciona componentes y estilos previamente desarrollados.
* Reduce el tiempo necesario para implementar elementos visuales comunes.
* Facilita la creación de interfaces adaptables a diferentes tamaños de pantalla.
* Permite desarrollar rápidamente formularios, tablas, tarjetas y elementos de navegación.
* Se integra como una capa de presentación complementaria a Astro.
* Permite que el equipo concentre mayor esfuerzo en las funcionalidades principales del sistema.
* Se puede complementar con CSS personalizado cuando sea necesario.

### Negativas / Riesgos

* La interfaz puede presentar una apariencia similar a otras aplicaciones que utilizan Bootstrap si no se realizan personalizaciones.
* El equipo deberá familiarizarse con las clases, componentes y sistema de diseño proporcionados por Bootstrap.
* Algunas necesidades específicas del proyecto pueden requerir CSS adicional.
* Se incorpora una dependencia externa que deberá mantenerse durante el desarrollo del proyecto.








