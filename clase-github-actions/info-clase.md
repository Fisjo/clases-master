# Clase de GitHub Actions

Resumen de todo lo trabajado en la clase: desde el primer "Hello world" hasta un pipeline completo con jobs, matrices, artefactos, secretos y servicios.

Los workflows están en `.github/workflows/`. GitHub **solo detecta los archivos que están directamente en esa carpeta**, no en subcarpetas, por eso no se agrupan. Los archivos de datos (`data.json`, `ventas.json`) sí están en una subcarpeta, `.github/workflows/data/`, porque GitHub ignora lo que no sea un `.yml` o `.yaml`.

## Índice

| Archivo | Concepto que enseña |
|---|---|
| `first.yaml` | Estructura mínima de un workflow (**con errores**) |
| `second.yaml` | Varios steps, `checkout` y leer archivos del repo |
| `third.yaml` | Inputs manuales |
| `output.yaml` | Outputs entre steps |
| `ej1.yaml` | Variables de entorno (`env`) |
| `ej3.yaml` | Matriz de estrategia (`matrix`) |
| `ej4.yaml` | Artefactos entre jobs |
| `ej5.yaml` | Filtros de rama y ruta |
| `ej6.yaml` | Acciones de la comunidad |
| `ej7.yaml` | Outputs entre jobs |
| `ej8.yaml` | Programación con cron |
| `ej9.yaml` | Contenedores de servicio |
| `ej10.yaml` | Dependencias y condicionales entre jobs |
| `20.desafio_final.yaml` | Pipeline completo que integra todo lo anterior |

---

## Parte 1: Fundamentos

### `first.yaml`: el "Hello world"

```yaml
on:
  workflow-dispatch:
jobs:
  say_hello:
    runs-on: ubuntu-latest
    steps:
      -run: echo "Hello world!"
```

Define un job (`say_hello`) que se ejecuta en una máquina Ubuntu y hace un `echo`.

**Tiene dos errores, así que no funciona:**
- `workflow-dispatch` debe escribirse `workflow_dispatch`, con guion bajo.
- `-run:` debe ser `- run:`, con un espacio tras el guion. Sin él, YAML no lo lee como un elemento de lista.

### `second.yaml`: varios steps y checkout

- **Trigger:** `workflow_dispatch`, es decir, ejecución manual desde la pestaña *Actions*.
- **`name:`** pone un nombre legible al workflow y al job.
- **Steps:**
  1. `echo "Hello world!"`.
  2. `actions/checkout@v3` descarga el código del repo en el runner. Es una *action* reutilizable y se usa con `uses:` en lugar de `run:`.
  3. `cat ./.github/workflows/list.txt` muestra el contenido de `list.txt`. Solo funciona porque el step anterior hizo el checkout.
  4. `echo "I'm step 4"`.

**Idea clave:** el runner empieza vacío. Sin `checkout`, no hay archivos del repo.

### `third.yaml`: inputs del usuario

```yaml
workflow_dispatch:
  inputs:
    thename:
      description: "What is your name?"
      required: true
```

Al lanzarlo a mano, GitHub muestra un formulario que pide el nombre. El step lo usa con `${{ inputs.thename }}`.

**Idea clave:** `inputs` hace que un workflow sea parametrizable. `${{ ... }}` es la sintaxis de expresiones de GitHub Actions.

### `output.yaml`: outputs entre steps

```yaml
- id: get-time
  run: |
    currTime=$(date)
    echo "currentTime=${currTime}" >> $GITHUB_OUTPUT
- run: echo "La hora es ${{ steps.get-time.outputs.currentTime }}"
```

1. El primer step escribe `clave=valor` en `$GITHUB_OUTPUT`.
2. Le pone un `id` para poder referenciarlo.
3. El segundo step lo lee con `steps.<id>.outputs.<clave>`.

### `list.txt`

Contiene `Hola que tal?`. Es el archivo que `second.yaml` imprime con `cat`.

---

## Parte 2: Ejercicios

### `ej1.yaml`: variables de entorno

```yaml
env:
  nombre: Nacho
jobs:
  saludo-1:
    steps:
      - run: echo "Hola $nombre desde el job 1"
  saludo-2:
    steps:
      - run: echo "Hola $nombre desde el job 2"
```

Un `env` a nivel de workflow está disponible en **todos los jobs y steps**. También se puede declarar a nivel de job o de step para limitar su alcance.

### `ej3.yaml`: matriz de estrategia

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

Un mismo job se ejecuta **en paralelo** una vez por cada valor de la matriz. Las versiones van entre comillas: sin ellas, YAML interpreta `3.10` como el número `3.1`.

### `ej4.yaml`: artefactos

- Job `generar`: crea `mensaje.txt` y lo sube con `actions/upload-artifact@v4`.
- Job `mostrar`: lo descarga con `actions/download-artifact@v4` y hace `cat`.

**Idea clave:** cada job corre en una máquina distinta, así que los archivos no se comparten solos. Los artefactos son la forma de pasar archivos entre jobs. `needs: generar` garantiza el orden.

### `ej5.yaml`: filtros de rama y ruta

```yaml
on:
  push:
    branches:
      - develop
    paths:
      - "docs/**"
```

Cuando `branches` y `paths` van juntos, **deben cumplirse las dos condiciones** (rama Y ruta). `docs/**` incluye las subcarpetas.

### `ej6.yaml`: acciones de la comunidad

Usa `GrantBirki/json-yaml-validate@v3` para validar `data.json`. Necesita `actions/checkout` antes para tener el archivo. Solo comprueba que el JSON sea sintácticamente válido; para exigir claves concretas haría falta un JSON Schema.

**Idea clave:** el Marketplace de GitHub tiene miles de acciones. Conviene fijar la versión (`@v3`) y revisar quién las mantiene.

### `ej7.yaml`: outputs entre jobs

```yaml
job-a:
  outputs:
    numero: ${{ steps.generar.outputs.numero }}
  steps:
    - id: generar
      run: echo "numero=$RANDOM" >> "$GITHUB_OUTPUT"
job-b:
  needs: job-a
  steps:
    - run: echo "${{ needs.job-a.outputs.numero }}"
```

Se necesitan tres piezas: el step escribe en `$GITHUB_OUTPUT`, el job lo declara en `outputs` y el job siguiente lo lee con `needs.<job>.outputs.<clave>`.

### `ej8.yaml`: programación con cron

```yaml
on:
  schedule:
    - cron: "0 9 * * 1"
jobs:
  tarea-semanal:
    if: ${{ vars.ACTIVO == 'true' }}
```

- `0 9 * * 1` son los lunes a las 9:00, **en UTC**.
- Los workflows con `schedule` solo se ejecutan desde la rama por defecto.
- Un workflow no puede declararse "desactivado" desde el YAML. Aquí se simula con una variable de repositorio (`ACTIVO`); la alternativa es desactivarlo desde la pestaña Actions o con `gh workflow disable`.

### `ej9.yaml`: contenedores de servicio

```yaml
services:
  db:
    image: postgres:16
    env:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: secreto
      POSTGRES_DB: prueba
    ports:
      - 5432:5432
    options: >-
      --health-cmd "pg_isready -U usuario -d prueba"
```

GitHub levanta un contenedor junto al job. El healthcheck hace esperar a que Postgres esté listo antes de empezar los steps. Como el job corre en el runner, se conecta por `localhost:5432`. En un proyecto real la contraseña iría en un secreto.

### `ej10.yaml`: dependencias y condicionales

```yaml
deploy:
  needs: build
  if: ${{ success() && github.event_name == 'workflow_dispatch' }}
```

`deploy` solo corre si `build` termina bien y el evento es un lanzamiento manual. Para exigir además una aprobación humana, se añade `environment:` al job y se configuran revisores obligatorios en Settings → Environments.

---

## Parte 3: Desafío final (`20.desafio_final.yaml`)

Pipeline de datos de ventas que combina casi todo lo visto.

```text
ci-seguridad  ──►  procesamiento (staging | production)  ──►  notificacion
```

1. **Activación:** `workflow_dispatch` con un input de tipo `choice` (`si` / `no`) para decidir si se ejecutan los tests de seguridad.
2. **`ci-seguridad`:** valida que `ventas.json` es JSON válido. El escaneo de claves API (`escaneo_seguridad.py`) lleva un `if` que depende del input.
3. **`procesamiento`:** depende del anterior. Usa una matriz `staging` / `production`, genera `reporte-<entorno>.txt` y lo sube como artefacto con un nombre distinto por entorno, para que el jefe de departamento pueda descargarlos.
4. **`notificacion`:** corre solo si los anteriores terminaron bien (`needs` + `success()`). Usa el secreto `DISCORD_WEBHOOK` y simula el envío con un `echo`. GitHub enmascara el valor de los secretos en los logs (`***`).

### Script de ejemplo: `escaneo_seguridad.py`

Simula un escaneo de seguridad: recorre el archivo línea a línea buscando patrones de claves expuestas (`AKIA…`, `api_key`, `secret`, `token` con un valor largo). Si encuentra alguna, sale con código 1 y el step falla.

---

## Configuración necesaria

| Elemento | Dónde | Para qué |
|---|---|---|
| Secreto `DISCORD_WEBHOOK` | Settings → Secrets and variables → Actions | Desafío final |
| Variable `ACTIVO=true` | Settings → Secrets and variables → Actions → Variables | Activar `ej8.yaml` |

## Resumen de conceptos

| Concepto | Para qué sirve |
|---|---|
| `on` | Triggers: `workflow_dispatch`, `push`, `schedule` |
| `inputs` | Parámetros del lanzamiento manual |
| `env` | Variables de entorno |
| `jobs`, `runs-on`, `steps` | Estructura y entorno de ejecución |
| `run` / `uses` | Comando de shell o acción reutilizable |
| `needs` | Orden y dependencias entre jobs |
| `if` y `success()` | Condicionales |
| `strategy.matrix` | Ejecuciones paralelas con distintos valores |
| `outputs` y `$GITHUB_OUTPUT` | Pasar datos entre steps y jobs |
| Artefactos | Pasar archivos entre jobs y descargarlos |
| `services` | Contenedores auxiliares (bases de datos, etc.) |
| `secrets` y `vars` | Datos sensibles y configuración del repo |
| Expresiones `${{ }}` | Leer contextos: `inputs`, `matrix`, `needs`, `steps`, `secrets`, `vars` |
