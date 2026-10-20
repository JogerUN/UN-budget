<!--
HOW TO USE THIS TEMPLATE
------------------------
1. Copy this file to docs/design/01_Architectural_and_Detailed_Design.md in your team repository.
2. This is v1.0 of work you already started: your Class 11 "Architectural Hypothesis v0.1"
   and your Class 12 "Detailed Design v0.1". Extend them to your whole system. Do not restart.
3. Use YOUR project. Generic examples (e-commerce, food delivery, banking, library) are
   only reference material and cannot be submitted as project artifacts.
4. Fill in every section. If something genuinely does not apply, write "N/A: reason".
   Never invent content to fill a blank.
5. Every diagram needs the table or argument that explains it. A diagram records design
   decisions. It does not create them.
6. Diagrams: Mermaid is preferred because it renders on GitHub. PlantUML or another tool is
   accepted if the exported image is committed and embedded in this file.
   Optionally, also add a JPG of each diagram in docs/design/diagrams/ (the Markdown prevails if they differ).
7. Read Design_Deliverable_1_Example.md for the expected level of detail. Do not copy it.
-->

# [Project Name] — Architectural & Detailed Design v1.0

| | |
|---|---|
| **Team** | |
| **Members** | |
| **Status** | Draft / Ready for review |
| **Date** | |
| **Inputs** | `docs/requirements/`, Architectural Hypothesis v0.1 (Class 11), Detailed Design v0.1 (Class 12) |

---

## 1. System Overview & Design Drivers

**System purpose** (2–3 sentences, in terms of the need it satisfies)
>

**Requirements that shape the structure** *(the ones that most influence the design, not all of them)*

| Requirement / Use Case ID | Why it shapes the structure | Quality attribute, constraint or business rule involved |
|---|---|---|
| | | |

---

## 2. Architectural Design

*(Outward-facing: what are the major parts, what is each responsible for, how do they interact?)*

### 2.1 System Context & Boundary

| Outside the system | Type (actor / external system / hardware) | How the system interacts with it |
|---|---|---|
| | | |

### 2.2 Components, Responsibilities & Capabilities

Cover the principal functional scope of your whole system.

```mermaid
flowchart LR
    Actor([User or external actor])
    subgraph SYS["System name"]
        C1["Component 1"]
        C2["Component 2"]
        C3["Component 3"]
    end
    Ext[("External system")]

    Actor --> C1
    C1 -->|"capability requested"| C2
    C2 -->|"capability requested"| C3
    C3 -->|"capability requested"| Ext
```

*(Everything inside `SYS` is what you build and control. Everything outside is what you only interact with. Label each arrow with the capability being requested.)*

| Component | Main responsibility | Requirements / use cases supported | Provided capabilities | Required capabilities | Main dependencies |
|---|---|---|---|---|---|
| | | | | | |

*Checks: is every component named by responsibility, not technology ("the component that persists orders", not "the database")? Does any component exist only to make the diagram look more complex?*

---

## 3. Detailed Design

Cada componente se diseña con el propósito de cumplir los requerimientos establecidos, definiendo claramente la responsabilidad de cada clase, el proceso que ejecuta y el objetivo que persigue. Se busca mantener una alta cohesión dentro del módulo, de manera que sus clases trabajen de forma coordinada y estén relacionadas con una misma finalidad. Asimismo, la separación de responsabilidades permite mantener un código organizado, modular y fácil de comprender, modificar y escalar, facilitando la incorporación de nuevas funcionalidades sin afectar significativamente el funcionamiento de los componentes existentes.

### 3.1 Components selected (at least two)

| Component | Why it was selected (risk, complexity, centrality to the drivers) |
|---|---|
| **Gestor de Transacciones** | Es un componente central para la integridad financiera del sistema, ya que administra el registro, la modificación y la eliminación lógica de los gastos e ingresos. Debe garantizar la consistencia de los movimientos, conservar el historial de los cambios y evitar la pérdida de información financiera. Además, debe gestionar la clasificación de los gastos por categoría, facilitar el control del presupuesto, debe diferenciar entre la fecha esperada y la fecha real, permitiendo programar y actualizar los movimientos sin alterar la confiabilidad de la información financiera del usuario. |

### 3.2 Class Diagram(s)

```mermaid
classDiagram
    direction TB

    class RegistroGastos {
        + RegistrarGasto(gasto: Gasto) estado:Boolean
    }

    class ModificacionGastos {
        + modificarGasto(gasto_nuevo:Gasto) estado:Boolean
    }

    class EliminarGastos {
        + eliminarGasto(gasto:Gasto) estado:Boolean
    }

    class Gasto {
        +ID: Identificador_DB
        -montoCOP: Integer
        -fecha: Date
        -medioPago: Paymethod
        -categoria: Categoria
        -estadoRegistro: STATE
        -fechaCreacion: Date
        -fechaUltimaModificacion: Date
    }

    class Categoria {
        - categoria: Categoria
    }

    class RegistrarIngreso {
        +registrarIngreso(ingreso) Boolean
    }

    class ProgramarIngreso {
        +programarIngreso(fechaNueva) Boolean
    }

    class ModificarIngreso {
        +modificarIngreso(ingresoModificado) Boolean
    }

    class EliminarIngreso {
        +eliminarIngreso(ingreso) Boolean
    }

    class Ingreso {
        +ID: Identificador_DB
        -montoCOP: Integer
        -fuenteIngreso: String
        -fechaEsperada: Date
        -fechaReal: Date
        -estadoRegistro: STATE
        -fechaCreacion: Date
        -fechaUltimaModificacion: Date
    }

    RegistroGastos --> Gasto : registra
    ModificacionGastos --> Gasto : modifica
    EliminarGastos --> Gasto : elimina logicamente

    Gasto "*" --> "1" Categoria : pertenece a

    RegistrarIngreso --> Ingreso : registra
    ProgramarIngreso --> Ingreso : programa
    ModificarIngreso --> Ingreso : modifica
    EliminarIngreso --> Ingreso : elimina logicamente

```

### 3.3 Class Responsibilities

| Class | Component it belongs to | Responsibility | Key collaborators |
|---|---|---|---|
| RegistroGastos | Gestión de gastos | Validar y coordinar el registro de un nuevo gasto. | Gasto, Categoria |
| ModificacionGastos | Gestión de gastos | Coordinar la modificación de los datos de un gasto existente. | Gasto, Categoria |
| EliminarGastos | Gestión de gastos | Realizar la eliminación lógica de un gasto y conservar su historial. | Gasto |
| Gasto | Gestión de gastos | Mantener la información del gasto, su estado y sus fechas de auditoría. | Categoria, clases de operaciones de gastos |
| Categoria | Gestión de gastos | Representar la categoría utilizada para clasificar los gastos. | Gasto |
| RegistrarIngreso | Gestión de ingresos | Validar y coordinar el registro de un nuevo ingreso. | Ingreso |	
| ProgramarIngreso |	Gestión de ingresos | Establecer la fecha esperada de un ingreso sin confundirla con su fecha real. | Ingreso |
| ModificarIngreso |	Gestión de ingresos | Coordinar la modificación de la información de un ingreso existente. | Ingreso |
| EliminarIngreso	 | Gestión de ingresos	| Realizar la eliminación lógica de un ingreso y conservar su historial. | Ingreso |
| Ingreso | Gestión de ingresos | Mantener los datos del ingreso, su fuente, las fechas esperada y real, su estado y las fechas de auditoría. | Clases de operaciones de ingresos |

### 3.4 Behavior of one key operation



```text
Operation: RegistrarGasto(gasto:Gasto): Boolean -> Esta operación es importante porque el registro correcto de los gastos contribuye
directamente a la integridad financiera del sistema.

Flujo de comportamiento:
1. Recibir el objeto Gasto con la información proporcionada por el usuario.
2. Verificar que los datos obligatorios estén presentes y que el monto sea válido.
3. Comprobar que la categoría asociada exista y sea válida.
4. Si la información no cumple las validaciones, rechazar el registro y devolver false.
5. Asignar el estado inicial correspondiente al gasto.
6. Establecer la fecha de creación y la fecha de última modificación.
7. Guardar el gasto mediante el mecanismo de persistencia del sistema.
8. Si el guardado falla, informar que la operación no se completó y devolver false.
9. Si el gasto supera el presupuesto de su categoría, generar una alerta visual sin bloquear el registro.
10. Si el registro se completa correctamente, devolver true.

Happy-path: el sistema registra el gasto cuando los datos son válidos, conserva su información y permite alertar sobre un posible
exceso del presupuesto sin impedir la transacción.

Non-happy-path: si el monto es inválido, la categoría no existe o el almacenamiento falla, el gasto no debe registrarse como una
operación exitosa. El sistema debe informar el error y evitar que quede un movimiento duplicado o parcialmente registrado.
```

---

## 4. Design Quality — Cohesion, Coupling, Information Hiding

| Question | Your answer, with evidence from your design |
|---|---|
| **Cohesion:** do the responsibilities inside each class or component belong together? | |
| **Coupling:** how far does a change in one element spread? Where are the strongest dependencies? | |
| **Information hiding:** what did you keep private or internal, and why? | |

**At least one real finding** (a problem you found in your own design) **and what you changed or would change:**
>

---

## 5. Design Decisions & Decision Record

Two decisions are required: one architectural (Class 11 level) and one detailed-design (Class 12 level). Avoid "it is best practice", "it scales" or "it is cleaner" without project evidence.

### Decision A — Architectural

| | |
|---|---|
| **Context** (requirement, constraint or problem that motivated it) | |
| **Decision** | |
| **Rationale** (why it is reasonable here) | |
| **Trade-off accepted** | |

### Decision B — Detailed design

| | |
|---|---|
| **Context** | |
| **Decision** | |
| **Rationale** | |
| **Trade-off accepted** | |

### ADR

At least one of the two decisions above must also be recorded as an ADR (use `Plantilla_ADR_Nygard`) in `docs/decisions/`.

**ADR file:** `docs/decisions/ADR-XXX-title.md` — records Decision [A / B].

---

## 6. Traceability

| Requirement ID | Use Case | Component(s) | Class(es) |
|---|---|---|---|
| | | | |

*(Every requirement in Section 1 must appear. Every component and class should appear at least once. If an element traces to nothing, ask why it exists.)*

---

## 7. Optional — AI-Assisted Design Reflection

> One design recommendation generated by AI that the team accepted, modified or rejected, and why.

---

## 8. Consistency Checklist

- [ ] Every component in the diagram appears in the responsibilities table, and the other way around.
- [ ] Every class belongs to an identifiable component.
- [ ] Components are named by responsibility, not technology.
- [ ] Nothing inside the system boundary is something you do not control.
- [ ] Provided and required capabilities match across components (what one requires, another provides).
- [ ] Both decisions name a real cost or limitation, and at least one has an ADR.
- [ ] The traceability table has no empty rows and no orphan components or classes.
- [ ] Diagrams render correctly on GitHub (or the exported images are embedded).
