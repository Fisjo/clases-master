# Clase de Git y GitHub

Apuntes de la clase de Git. Los ficheros de esta carpeta (`app.py`, `interes-compuesto.py`, `numeros-aleatorios.py`, `fichero.txt`, `documento-main.txt`) son solo material de práctica: lo importante es el flujo de trabajo, no el código.

## Contenido

1. [Conceptos básicos](#1-conceptos-básicos)
2. [Git por línea de comandos](#2-git-por-línea-de-comandos)
3. [Ramas, merge y conflictos](#3-ramas-merge-y-conflictos)
4. [Pull requests](#4-pull-requests)
5. [Fork](#5-fork)
6. [Reglas de protección de ramas](#6-reglas-de-protección-de-ramas-branch-protection-rules)
7. [CODEOWNERS](#7-codeowners)
8. [Plantilla de pull request](#8-plantilla-de-pull-request-pull_request_template)
9. [`.gitignore`](#9-gitignore)

---

## 1. Conceptos básicos

- **Git** es el sistema de control de versiones (local). **GitHub** es la plataforma donde se aloja el repositorio remoto y se colabora.
- **Repositorio**: carpeta con el proyecto y todo su historial (`.git/`).
- **Commit**: una "foto" de los cambios, con autor, fecha y mensaje.
- **Rama (branch)**: línea de desarrollo independiente. `main` es la rama principal.
- **Remoto (`origin`)**: la copia del repositorio en GitHub.
- Las zonas de trabajo: **directorio de trabajo** → `git add` → **staging** → `git commit` → **repositorio local** → `git push` → **remoto**.

## 2. Git por línea de comandos

### Configuración inicial

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
git config --list
```

### Empezar un repositorio

```bash
git init                      # crea un repositorio nuevo en la carpeta actual
git clone <url>               # descarga un repositorio existente
git remote -v                 # ver los remotos configurados
git remote add origin <url>   # añadir un remoto
```

### Ciclo de trabajo diario

```bash
git status                    # estado de los ficheros
git add fichero.txt           # añade un fichero al staging
git add .                     # añade todos los cambios
git commit -m "mensaje"       # guarda el commit
git push                      # sube los commits al remoto
git pull                      # baja y fusiona los cambios del remoto
git fetch                     # baja los cambios del remoto sin fusionarlos
```

### Consultar el historial y los cambios

```bash
git log                       # historial completo
git log --oneline             # historial resumido
git log --oneline --graph --all   # historial con ramas
git diff                      # cambios sin añadir al staging
git diff --staged             # cambios ya en el staging
git show <commit>             # detalle de un commit
```

### Deshacer cosas

```bash
git restore fichero.txt           # descarta cambios locales de un fichero
git restore --staged fichero.txt  # saca un fichero del staging
git commit --amend                # modifica el último commit (solo si no se ha subido)
git revert <commit>               # crea un commit que deshace otro (seguro)
git reset --soft HEAD~1           # deshace el último commit conservando los cambios
```

> ⚠️ `git reset --hard` y `git push --force` destruyen trabajo y reescriben historia. En equipo **no se usan** sobre ramas compartidas (la plantilla de PR de este repo lo recuerda).

## 3. Ramas, merge y conflictos

```bash
git branch                    # lista las ramas locales
git branch -a                 # lista también las remotas
git branch nueva-rama         # crea una rama
git switch nueva-rama         # cambia de rama
git switch -c nueva-rama      # crea y cambia en un paso
git push -u origin nueva-rama # sube la rama y la enlaza con el remoto
git branch -d nueva-rama      # borra una rama ya fusionada
```

Para fusionar una rama en `main`:

```bash
git switch main
git pull
git merge nueva-rama
```

### Conflictos

Aparecen cuando dos ramas modifican la misma parte de un fichero. Git lo marca así:

```text
<<<<<<< HEAD
versión de la rama actual
=======
versión de la otra rama
>>>>>>> nueva-rama
```

Para resolverlo: editar el fichero y quedarse con la versión correcta (borrando los marcadores), y luego:

```bash
git add fichero-en-conflicto
git commit
```

## 4. Pull requests

Una **pull request (PR)** es la petición para fusionar una rama en otra (normalmente en `main`). Permite revisar el código, comentarlo y ejecutar comprobaciones antes del merge.

Flujo habitual:

1. Crear una rama a partir de `main` (`git switch -c mi-cambio`).
2. Hacer commits y subirlos (`git push -u origin mi-cambio`).
3. Abrir la PR en GitHub (de `mi-cambio` hacia `main`).
4. Revisión: comentarios, cambios solicitados y aprobación.
5. Merge de la PR y borrado de la rama.
6. En local: `git switch main && git pull`.

## 5. Fork

Un **fork** es una copia personal de un repositorio ajeno en tu cuenta de GitHub. Se usa cuando **no tienes permisos de escritura** en el repositorio original (típico en proyectos de código abierto).

Flujo:

1. Pulsar **Fork** en GitHub: se crea `tu-usuario/repositorio`.
2. Clonar tu fork: `git clone <url-de-tu-fork>`.
3. Añadir el repositorio original como remoto `upstream`:

   ```bash
   git remote add upstream <url-del-repo-original>
   git remote -v
   ```

4. Trabajar en una rama, hacer commits y `git push origin mi-rama` (a tu fork).
5. Abrir una PR desde tu fork hacia el repositorio original.
6. Mantener el fork actualizado:

   ```bash
   git fetch upstream
   git switch main
   git merge upstream/main
   git push origin main
   ```

| | Fork | Rama |
|---|---|---|
| Dónde vive | En otro repositorio (tu cuenta) | En el mismo repositorio |
| Permisos necesarios | Ninguno de escritura | Escritura en el repo |
| Uso típico | Contribuir a proyectos ajenos | Trabajo dentro de un equipo |

## 6. Reglas de protección de ramas (branch protection rules)

Configuración de GitHub para proteger ramas importantes como `main`. Se encuentran en **Settings → Branches → Add branch ruleset / protection rule** (o **Settings → Rules → Rulesets**).

Reglas más habituales:

- **Require a pull request before merging**: nadie hace `push` directo a `main`; todo cambio entra por PR.
  - **Require approvals**: número mínimo de aprobaciones.
  - **Dismiss stale approvals**: una nueva subida de commits invalida las aprobaciones anteriores.
  - **Require review from Code Owners**: exige la aprobación de los propietarios definidos en `CODEOWNERS`.
- **Require status checks to pass**: los checks (por ejemplo, workflows de GitHub Actions) deben estar en verde para poder fusionar.
- **Require conversation resolution**: todos los comentarios de la PR deben estar resueltos.
- **Require linear history**: impide commits de merge; obliga a rebase o squash.
- **Block force pushes**: prohíbe `git push --force` en la rama.
- **Restrict deletions**: impide borrar la rama.
- **Do not allow bypassing the above settings**: ni siquiera los administradores se saltan las reglas.

Resultado: `main` siempre contiene código revisado y comprobado.

## 7. CODEOWNERS

El fichero [`.github/CODEOWNERS`](../.github/CODEOWNERS) indica **quién es el responsable de cada parte del repositorio**. Cuando una PR toca esos ficheros, GitHub solicita automáticamente la revisión a sus propietarios (y, con la regla de protección *Require review from Code Owners*, su aprobación es obligatoria).

Ubicaciones válidas: `.github/CODEOWNERS`, `CODEOWNERS` (raíz) o `docs/CODEOWNERS`.

Sintaxis: un patrón de ruta (como en `.gitignore`) seguido de uno o varios usuarios o equipos.

```text
# Propietario por defecto de todo el repositorio
*                   @usuario

# Un fichero concreto
/README.md          @Fisjo

# Una carpeta
/docker/            @usuario1 @usuario2

# Un tipo de fichero
*.sql               @equipo-datos

# Un equipo de una organización
/github-actions/    @organizacion/devops
```

Si varias líneas coinciden con un fichero, **gana la última**. En este repositorio:

```text
/README.md @Fisjo
```

es decir, cualquier cambio en el `README.md` de la raíz requiere la revisión de `@Fisjo`.

## 8. Plantilla de pull request (`pull_request_template`)

El fichero [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md) define el texto que aparece **precargado en la descripción de cada nueva PR**. Sirve para que todo el equipo siga el mismo formato y recuerde las normas.

Ubicaciones válidas: `.github/PULL_REQUEST_TEMPLATE.md`, raíz del repo o `docs/`.

La plantilla de este repositorio:

```markdown
## PULL REQUEST

Before mergin the pull request please make sure of the following things:

- Don't push code you haven't checked
- Don't do --force

Please do things right :)
```

Ideas habituales para una plantilla más completa:

- Descripción del cambio y motivo.
- Tipo de cambio (corrección, funcionalidad nueva, documentación…).
- Lista de comprobación (`- [ ] He probado los cambios`, `- [ ] He actualizado la documentación`).
- Issue relacionada (`Closes #12`).

## 9. `.gitignore`

Lista de ficheros y carpetas que Git **no debe rastrear** (secretos, cachés, entornos virtuales…). En este repositorio:

```text
.password
__pycache__/
.hypothesis
.pytest_cache
.DS_Store
.venv
/data-science/clase2/data
```

Por eso `git/.password` nunca se sube: **los secretos no se commitean**. Si un fichero ya estaba rastreado, añadirlo a `.gitignore` no basta; hay que quitarlo del índice con `git rm --cached <fichero>`.

---

## Resumen rápido del flujo colaborativo

```bash
git switch main && git pull          # partir de main actualizado
git switch -c mi-cambio              # rama nueva
# ...editar ficheros...
git add . && git commit -m "mensaje" # commit
git push -u origin mi-cambio         # subir la rama
# abrir PR en GitHub → revisión (CODEOWNERS) → checks en verde → merge
git switch main && git pull          # volver a main y actualizar
git branch -d mi-cambio              # limpiar
```
