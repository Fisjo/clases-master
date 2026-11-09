# Vibecoding: de la idea a la app

Resumen de la presentación de David Ortega (EDEM): dos sesiones de cinco horas sobre cómo construir software con un agente de programación.

## Cómo funciona el curso

- **Dos herramientas, un mismo método.** Claude Code (con suscripción de Claude) u OpenCode + Gemini (con una clave gratuita de Google AI Studio). Lo que se aprende es el método, no los botones.
- **Cada ejercicio tiene dos niveles.** *Base* para todos (que funcione y comprobarlo usándolo) y *Reto* para quien ya programa (leer el código, tests, separar frontend y backend, seguridad).
- **Al acabar cada ejercicio:** commit y una frase en voz alta sobre qué ha fallado.
- **Sesión 1, aprender a trabajar con el agente:** qué es el vibecoding, instalar y primera app, hablarle bien al agente, contexto del proyecto, planificar, pasos pequeños y git, verificar.
- **Sesión 2, construir algo de verdad:** elegir pila, datos y APIs, IA dentro de la app, extender el agente, seguridad y revisión, publicar, proyecto y demo day.

### Chuleta de comandos

| Para… | Claude Code | OpenCode + Gemini |
|---|---|---|
| Arrancar | `claude` | `opencode` |
| Elegir modelo | `/model` | `/models` |
| Instrucciones del proyecto | `/init` → CLAUDE.md | `/init` → AGENTS.md |
| Pensar sin tocar código | Shift+Tab o `/plan` | Agente Plan (Shift+Tab) |
| Deshacer | Esc Esc o `/rewind` | `/undo` y `/redo` |
| Liberar contexto | `/clear`, `/compact`, `/context` | `/new`, `/compact` |
| Revisar cambios | `/review`, `/security-review` | `/review` |
| Trabajar hasta terminar | `/goal objetivo` | `/goal objetivo` |
| Herramientas y skills | `/mcp`, `/skills` | `/mcp`, `/skills` |

## Bloque 1 · Qué es el vibecoding

- Término de Andrej Karpathy (febrero de 2025): describes lo que quieres, pruebas lo que ha hecho usándolo y corriges pegando el error.
- **Tres niveles según el riesgo** (más riesgo, más revisión):
  - *Vibecoding puro:* prototipos, demos, herramientas personales.
  - *Vibecoding con red:* plan, pasos pequeños, git y pruebas. Es lo que se hace en el curso.
  - *Ingeniería asistida:* producción, dinero real y datos de clientes. Se revisa cada cambio.
- En 2026 muchos ingenieros ya no teclean código, pero siguen decidiendo qué se construye, verificando el resultado y revisando lo que importa.
- **Cómo trabaja un agente:** lee la petición, mira el proyecto, decide, usa una herramienta, mira el resultado y repite. Tiene herramientas, un contexto limitado (su memoria de trabajo) y permisos.
- **El arnés** (especificación y plan, tests, git, permisos ajustados, entornos separados, revisión de seguridad y alguien que entienda lo que se despliega) decide cuándo es razonable usarlo. Mover dinero, guardar datos personales, decidir sobre personas o tocar autenticación y pagos solo es válido con arnés y con alguien que sepa revisarlo.

## Bloque 2 · Instalar y primera app

- Comprobar la instalación con `claude --version` o `opencode --version`. En Windows, Claude Code va nativo en PowerShell y OpenCode dentro de WSL.
- **Clave de Gemini en tres pasos:** crearla en aistudio.google.com, copiarla una sola vez (es una contraseña) y pegarla en `/connect`. El nivel gratuito puede usar lo que envíes para mejorar productos de Google, así que solo datos públicos o inventados.
- **Ejercicio 1, Hola, hipoteca:** calculadora de cuota en un único `index.html` con el sistema francés y validación de negativos. Está hecho cuando 200.000 € al 3 % a 30 años da unos 843 €/mes.

## Bloque 3 · Hablarle bien al agente

- **Las cuatro piezas de un buen encargo:** objetivo, contexto, restricciones y cuándo está hecho. La cuarta es la que más se olvida y evita que el agente diga «hecho» sin estarlo.
- «Hazme la calculadora más bonita y añade más cosas» obliga al agente a adivinar. Un buen encargo es concreto: *añade una tabla de amortización anual, no cambies la fórmula de la cuota, está hecho cuando la suma del capital amortizado sea igual al préstamo*.
- **Trucos:** señalar archivos con `@`, pegar el error entero, enseñar capturas, pedirle que pregunte antes de empezar, una cosa cada vez e interrumpir pronto con Esc.
- **Ejercicio 2:** tres mejoras una a una (tabla de amortización, gráfico de barras sin librerías, guardar los últimos valores).

## Bloque 4 · El contexto del proyecto

- **Dos archivos:**
  - `docs/project-info.md`: qué es la app (problema, usuario, funciones, datos, tecnología, cómo se arranca y se prueba).
  - `AGENTS.md` / `CLAUDE.md`: cómo se trabaja. Es igual en todos los proyectos. Claude Code lee CLAUDE.md y OpenCode lee AGENTS.md; en grupos mixtos, CLAUDE.md puede contener solo `@AGENTS.md`.
- **Secciones del AGENTS.md:** antes de empezar, convenciones, código, pruebas, git, producción, nunca, y «si te corrijo dos veces, propón una línea».
- **Reglas principales:**
  - Leer `project-info.md` y `PLAN.md`, una fase cada vez y planificar antes de construir.
  - Sin dependencias hasta que hagan falta (los modelos a veces inventan paquetes).
  - Claves en `.env`, que nunca va a git.
  - Máximo 500 líneas por archivo y lógica separada de la interfaz.
  - Todo va probado, con una prueba que falle antes de arreglar un bug.
  - Commit por fase, `merge` y nunca `rebase`, nunca push y permiso explícito para cualquier acción sobre producción.
- **Gestionar el contexto:** una tarea, una sesión (`/clear` o `/new`), `/compact` para resumir y `/context` para ver qué ocupa. Síntomas de «mesa llena»: repite errores ya corregidos, olvida normas, mezcla tareas.
- **Plantilla del curso:** github.com/ObsidyVB/vibecoding-edem.
- **Ejercicio 3:** crear el repositorio desde la plantilla y rellenar `project-info.md` sin escribir código.

## Bloque 5 · Planificar antes de construir

- Modo plan (Claude Code) o agente Plan (OpenCode): el agente lee, pregunta y propone sin editar nada hasta que lo apruebes.
- Se le pide un plan en fases en el que cada fase se pueda probar, quepa en una sesión y diga cómo comprobarla. La fase 1 debe ser lo más pequeña posible.
- **Qué revisar:** que cada fase sea comprobable, que la fase 1 sea pequeña, que no haya añadido cosas que no pediste y que no use tecnologías que no entiendes.
- **Segunda opinión:** una sesión nueva (o el otro agente) revisa el plan como «desarrollador senior escéptico». El plan final se guarda en `PLAN.md`.
- **Ejercicio 4:** plan de 3 a 6 fases, revisado por otra sesión y guardado en `PLAN.md`.

## Bloque 6 · Pasos pequeños y git

- **Git en cinco palabras:** `init`, `commit`, `log`, `diff`, `revert`. No hace falta saberlos de memoria porque se le piden al agente. Con `gh` el agente también crea repositorios y pull requests.
- **Ritmo de trabajo:** pedir una fase, probarla tú, commit si funciona y pasar a la siguiente.
- Si no funciona, pegar el error. Si en dos intentos no lo arregla, volver al último commit y pedir una fase más pequeña. Para deshacer sin git: Esc Esc o `/rewind` en Claude Code, `/undo` y `/redo` en OpenCode.
- **Ejercicio 5:** construir la fase 1 con al menos dos commits y volver atrás una vez.

## Bloque 7 · Verificar

- **Fallos típicos del agente:**
  - Dice que ha probado algo que no ha probado.
  - Arregla el síntoma y no la causa.
  - Cambia los tests para que pasen.
  - Inventa librerías o funciones.
- La regla es pedir la prueba y no la promesa: «enséñame el resultado de ejecutarlo».
- **Tres formas de verificar:**
  - Usarlo tú, con una lista de comprobación de casos normales, raros y absurdos.
  - Tests automáticos, escritos antes que el código.
  - Un MCP de navegador (Chrome DevTools o Playwright; en Claude, también `claude --chrome`) para que el agente abra la app y la compruebe.
- **Un buen informe de error** incluye qué hiciste, qué esperabas, qué pasó, el error completo (F12 abre la consola), «explícame la causa antes de cambiar nada» y «el arreglo más pequeño posible».
- **Ejercicio 6:** caza de bugs en parejas. Cada uno crea una app con 5 errores ocultos y el agente de su pareja intenta encontrarlos.

## Bloque 8 · Elige tu pila

Lo más simple que sirva para tu proyecto:

| Ruta | Qué es | Para qué |
|---|---|---|
| A | HTML + JavaScript en un archivo, sin servidor | Calculadoras, simuladores, paneles con datos públicos |
| B | Streamlit (Python con interfaz incluida) | Apps con IA para quien no programa |
| C | React + FastAPI, separados | Quien ya programa y proyectos que crecerán |

Si la app usa una clave de IA no puede ser la ruta A, porque la clave quedaría a la vista de cualquiera.

## Bloque 9 · Datos y APIs

- Una API es una ventanilla: la app pregunta, la API responde y la app lo enseña. Para practicar hay APIs públicas sin clave, como Frankfurter (tipos de cambio del BCE) y el portal de datos del BCE.
- Hay que pedirle al agente que lea la documentación de la API antes de usarla, no que la recuerde.
- **Las claves van en `.env`:**
  - `.env` va en `.gitignore` y se crea antes del primer commit.
  - Se comparte un `.env.example` sin valores.
  - Si una clave llega a GitHub, hay que borrarla y crear otra, porque borrar el commit no basta.
  - El nombre del modelo también va en `.env`, porque cambia cada pocos meses.
- **Ejercicio 7:** conectar la app a datos reales. Si falla la red debe avisar y no romperse, y `git status` no debe mostrar el `.env`.

## Bloque 10 · IA dentro de tu app

- **Patrón:** navegador → tu servidor (donde viven la clave y el prompt) → Gemini. La clave nunca sale del servidor. Se usa Streamlit con `secrets.toml` (ruta B) o React llamando a un endpoint de FastAPI (ruta C).
- Se usa el SDK oficial `google-genai`, salida en JSON, el modelo desde `.env` y una gestión definida de fallos.
- **El prompt de tu app también es código:**
  - Guardarlo en un archivo (`prompts/`) con su historial en git.
  - Darle ejemplos.
  - Validar la respuesta.
  - Preparar el error 429 del nivel gratuito.
  - Medir con casos de prueba.
  - No enviar más datos de los necesarios, y menos datos personales.
- **Ejercicio 8:** añadir una función con Gemini. Debe avisar si falta la clave y acertar al menos 4 de 5 casos de prueba.

## Bloque 11 · Extender el agente

- **MCP:** estándar para darle herramientas nuevas al agente (GitHub, bases de datos, documentación, navegador). Se añade con `claude mcp add` o en `opencode.json`. Cada MCP es software de terceros con acceso a tu ordenador, así que solo de fuentes de confianza.
- **Del recorrido al test e2e:** el agente prueba en el navegador y luego convierte ese recorrido en un test de Playwright, que se repite siempre igual, gratis y sin modelo.
- **Comandos y skills:**
  - *Comando:* un prompt que lanzas tú con `/nombre`.
  - *Skill:* instrucciones que el agente usa solo cuando tocan.
  - Una skill en `.claude/skills/` la usan los dos agentes.
- **Ejercicio 9:** crear el comando `/revisar-fase`, que lee `PLAN.md`, ejecuta las comprobaciones de la fase, busca claves y datos personales, y da un informe de 5 líneas sin modificar nada.

## Bloque 12 · Seguridad y revisión

- **Cinco riesgos:**
  1. Claves a la vista.
  2. Inyección de prompt (instrucciones escondidas en webs o archivos que lee el agente).
  3. Paquetes inventados (en un estudio de 2025, cerca de 1 de cada 5 no existía y hay quien los registra con malware).
  4. Permisos demasiado amplios.
  5. Datos personales sin proteger.
- **Permisos:** leer y editar dentro del proyecto sí; borrar, publicar o tocar fuera de la carpeta, siempre preguntando. Evitar `--dangerously-skip-permissions` fuera de una máquina desechable.
- **Revisión adversarial:** `/review` y `/security-review`, o un prompt de «auditor de seguridad escéptico» que da archivo, riesgo, gravedad y arreglo sin cambiar nada.
- **Ejercicio 10:** otra sesión o el agente de tu compañero audita el proyecto, se arreglan los problemas de gravedad alta y se hace commit.

## Bloque 13 · Publicar

| Ruta | Dónde | Claves |
|---|---|---|
| A | Netlify Drop o GitHub Pages | No hay |
| B | Streamlit Community Cloud | En la sección Secrets |
| C | Cloud Run (`gcloud run deploy --source .`) | Variables de entorno o Secret Manager |

**Antes de publicar:** `git status` limpio y `.env` fuera, revisión de seguridad hecha, sin datos reales de nadie, límite de gasto o alerta de presupuesto y un aviso en la app («Prototipo educativo. No es asesoramiento financiero»). Publicar es una acción que conviene aprobar a mano, paso a paso.

## Bloque 14 · Tu proyecto y demo day

- **`/goal`:** el agente trabaja turno a turno hasta que un revisor independiente decide que el objetivo está cumplido. Un buen objetivo es comprobable (tests, lista, commits), indica lo que no se puede tocar y tiene un límite de turnos. Antes hacen falta plan, tests y git. Con permisos automáticos, solo en una carpeta con git y sin claves reales.
- **Dos horas de proyecto:** fase del plan → prueba → `/revisar-fase` → commit → siguiente. Cada 30 minutos se hace una parada para detectar atascos. Si se lía, sesión nueva, porque el contexto está en `AGENTS.md`, `project-info.md` y `PLAN.md`. Mejor una fase menos y funcionando que todas a medias.
- **Demo day (3 minutos):**
  1. El problema.
  2. La demo en vivo con el enlace publicado.
  3. Qué hace la IA y qué hace el código, y cómo se midió el acierto.
  4. Lo que más ha fallado y cómo se resolvió.
  5. Lo siguiente y los riesgos que quedan.

> Usar la IA para programar es fácil. Hacerlo bien es un método: plan, pasos pequeños, git, verificar y revisar con ojos nuevos.

## Anexos

- **Anexo A · Gemini con Vertex AI:** alternativa a AI Studio con proyecto de Google Cloud, facturación y alerta de presupuesto, elección de región (por ejemplo, UE), y datos que no se usan para entrenar. Es de pago por uso y recomendable para datos de empresa o producción.
  - Pasos: habilitar `aiplatform.googleapis.com`, `gcloud init`, `gcloud auth application-default login` y `set-quota-project`.
  - OpenCode se conecta con `GOOGLE_CLOUD_PROJECT` y `VERTEX_LOCATION`. En la app, `google-genai` pasa a Vertex con tres variables de entorno.
  - Hay una tabla con los errores habituales (403, credenciales, 404, 429, facturación).
  - Claude Code también puede usar Google Cloud.
- **Anexo B · Prompts del curso:** prompts para copiar y pegar (empezar, plan, error, tests, revisar un plan, auditar el código) y el `AGENTS.md` completo del curso.
