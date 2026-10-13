# Resumen de `.github/workflows`

La carpeta tiene **4 workflows de GitHub Actions** y **1 archivo auxiliar**. Cada workflow añade un concepto nuevo.

| Archivo | Concepto que enseña | Estado |
|---|---|---|
| `first.yaml` | Estructura mínima de un workflow | **Tiene errores** |
| `second.yaml` | Varios steps, `checkout` y leer archivos del repo | Correcto |
| `third.yaml` | Inputs manuales (`inputs`) | Correcto |
| `output.yaml` | Pasar datos entre steps (`GITHUB_OUTPUT`) | Correcto |
| `list.txt` | Archivo de texto que lee `second.yaml` | Auxiliar |

---

## 1. `first.yaml`: el "Hello world"

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

---

## 2. `second.yaml`: varios steps y checkout

- **Trigger:** `workflow_dispatch`, es decir, ejecución manual desde la pestaña *Actions*.
- **`name:`** pone un nombre legible al workflow y al job.
- **Steps:**
  1. `echo "Hello world!"`.
  2. `actions/checkout@v3` descarga el código del repo en el runner. Es una *action* reutilizable, y se usa con `uses:` en lugar de `run:`.
  3. `cat ./.github/workflows/list.txt` muestra el contenido de `list.txt`. Solo funciona porque el step anterior hizo el checkout. Tiene un `name:` propio para que se vea claro en los logs.
  4. `echo "I'm step 4"`.

**Idea clave:** el runner empieza vacío. Sin `checkout`, no hay archivos del repo.

---

## 3. `third.yaml`: inputs del usuario

```yaml
workflow_dispatch:
  inputs:
    thename:
      description: "What is your name?"
      required: true
```

Al lanzarlo a mano, GitHub muestra un formulario que pide el nombre. El step lo usa con `${{ inputs.thename }}`:

```yaml
- run: echo "Hello there ${{inputs.thename}}!"
```

**Idea clave:** `inputs` hace que un workflow sea parametrizable. `${{ ... }}` es la sintaxis de expresiones de GitHub Actions.

---

## 4. `output.yaml`: outputs entre steps

```yaml
- id: get-time
  name: "Get the current time"
  run: |
    currTime=$(date)
    echo "currentTime=${currTime}" >> $GITHUB_OUTPUT
- run: echo "The time for the early step is ${{ steps.get-time.outputs.currentTime }}"
```

1. El primer step guarda la fecha en una variable de shell.
2. Escribe `clave=valor` en `$GITHUB_OUTPUT`, que es el mecanismo para **exponer un output**.
3. Le pone un `id` (`get-time`) para poder referenciarlo.
4. El segundo step lo lee con `steps.get-time.outputs.currentTime`.

**Idea clave:** `id` + `$GITHUB_OUTPUT` + `steps.<id>.outputs.<clave>` es la forma de pasar datos entre steps.

---

## 5. `list.txt`

Contiene `Hola que tal?`. Es el archivo que `second.yaml` imprime con `cat`.

---

## Resumen de conceptos

`on` (triggers) → `jobs` → `runs-on` → `steps` → `run` / `uses` → `name` / `id` → `inputs` → `outputs` → expresiones `${{ }}`

