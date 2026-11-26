# Terraform e IaC

Material de la clase de **Terraform e IaC** (Pedro Nieto, Máster en IA, Big Data y Cloud – EDEM, Bloque 1: Cloud Data). Cada carpeta con ficheros `.tf` es un proyecto de Terraform independiente (con su propio `terraform init` y su propio estado):

| Carpeta | Contenido |
|---|---|
| [`clase1/`](clase1/clase1.tf) | Crear un repositorio de GitHub completo con Terraform |
| [`clase2/`](clase2) | Variables, tipos y el provider `random`, generando ficheros en local |
| [`clase2/google/`](clase2/google) | Ejercicio con Google Cloud: una VM de Compute Engine con el provider `google` |
| [`clase3/recap/`](clase3/recap) | Recap en Google Cloud: dos VMs con variables, un bucket y el estado en un backend remoto (GCS) |
| [`clase3/ejercicio1/`](clase3/ejercicio1) | Servicio de Cloud Run (`hangman`) con un `output` de la URL |
| [`clase3/ejercicio2/`](clase3/ejercicio2) | Bucket y VM de Google Cloud alineados con el estado existente (sin reemplazos) |
| [`clase3/ejercicio3/`](clase3/ejercicio3) | Esqueleto vacío para el siguiente ejercicio |
| [`_shared/gcp/`](_shared/gcp) | `providers.tf` y `variables.tf` comunes a todos los proyectos de Google Cloud |

## Resumen de la presentación (`Terraform.pdf`)

1. **Introducción a IaC**: el mismo código genera siempre el mismo entorno. Terraform es de HashiCorp (junto a Vault, Consul y Nomad).
2. **IaC vs manual**: crear recursos a mano (consola), con scripts/CLI (ad-hoc) o de forma declarativa (IaC). La IaC se versiona en Git y se despliega con pipelines.
3. **State (estado deseado)**: como un termostato, Terraform compara el estado actual con el deseado y actúa solo si difieren. El estado se guarda en `terraform.tfstate`, que puede ser remoto (p. ej. Google Cloud Storage) para trabajar en equipo.
4. **Terraform y HCL**: lenguaje declarativo con bloques `resource "<tipo>" "<nombre>" { ... }`. Estructura típica: `main.tf`, `variables.tf`, `provider.tf`, `output.tf` y `*.tfvars`.
5. **Flujo de trabajo**: `init` → `validate` → `plan` → `apply` → `destroy`. Con `plan -out=tfplan` se guarda el plan para aplicarlo exactamente.
6. **Providers**: plugins que permiten hablar con APIs (AWS, GCP, Azure, GitHub, `local`, `random`...). Sin provider, Terraform no puede gestionar nada.
7. **Variables y outputs**: tipos (`string`, `number`, `bool`, `list`, `map`, `set`, `object`, `tuple`); valores por defecto, `-var`, `TF_VAR_*`, `*.tfvars` o modo interactivo; `output` para exponer valores.
8. **Dependencias**: implícitas (referenciar `recurso.atributo`) o explícitas (`depends_on`).
9. **Repetición**: `count` y `count.index`, junto con `length()`.
10. **Import y remote state**: `terraform import` para traer recursos existentes al estado; estado remoto para colaborar.

## Clase 1: `clase1/clase1.tf`

Crea con Terraform lo mismo que en la diapositiva 9 se hacía a mano (repo con ramas `main` y `develop`), añadiendo protección y secretos. Recursos, en orden lógico:

| Recurso | Qué hace |
|---|---|
| `github_repository.example` | Crea el repo público `example` con un commit inicial |
| `github_branch_default.main` | Fija `main` como rama por defecto |
| `github_branch.develop` | Crea la rama `develop` desde `main` |
| `github_repository_collaborator` | Añade un colaborador (`var.usuario`) con permiso `push` |
| `git_clone.clone` | Clona el repo en `./example` |
| `local_file.example` | Genera `example.txt` dentro del clon |
| `git_add` / `git_commit` / `git_push` | Añade, commitea y hace push del fichero (cada uno `depends_on` del anterior) |
| `github_branch_protection` (`main` y `develop`) | Exige 1 review aprobada, descarta reviews obsoletas y aplica a admins |
| `github_actions_secret.password` | Guarda un secret `password` en GitHub Actions |

Variables:

- `usuario`: usuario de GitHub colaborador (por defecto `AlejCervera`).
- `password`: valor del secret; marcada como `sensitive`, **sin valor por defecto**.

Conceptos de la clase que aparecen: dependencias implícitas (`github_repository.example.name`), explícitas (`depends_on`), variables, `sensitive` y varios providers (`github`, `git`, `local`).

> Nota: `clase1.tf` no declara los providers (`required_providers` / `provider`). Hay que añadirlos (p. ej. en un `provider.tf`) con la autenticación de GitHub antes de ejecutar.

### Uso (clase 1)

```bash
cd terraform/clase1
export GITHUB_TOKEN=<tu_token>      # autenticación del provider github
terraform init
terraform plan -var "password=<secreto>"
terraform apply -var "password=<secreto>"
terraform destroy -var "password=<secreto>"   # para limpiar
```

## Clase 2: `clase2/`

Ejercicio local, sin credenciales ni cuentas en la nube: usa solo los providers `local` y `random` para practicar variables y dependencias.

| Fichero | Contenido |
|---|---|
| `main.tf` | Recursos: `local_file.pet`, `random_pet.my-pet` y `local_file.pet-name` |
| `variables.tf` | Variables de varios tipos (ver abajo) |
| `terraform.tfvars` | Valores que sobrescriben los por defecto: `filename`, `content`, `prefix`, `separator` y `length` |

Recursos:

- `local_file.pet`: crea `saludo.txt` (`var.filename`) con el valor `statement2` del mapa `var.file-content`.
- `random_pet.my-pet`: genera un nombre aleatorio con prefijo `var.prefix[3]` (`Madam`), `var.length` palabras y separador `var.separator`.
- `local_file.pet-name`: crea `<nombre>.txt` con el nombre generado (p. ej. `Madam_rapid_gar.txt`). Depende de forma implícita de `random_pet.my-pet.id`.

Tipos de variable que se practican: `string`, `number` (`length`), `bool` (`password_change`), `list(string)` (`prefix`), `map` (`file-content`) y `object` (`student`). `content`, `password_change` y `student` están declaradas pero `main.tf` no las usa todavía.

### Uso (clase 2)

```bash
cd terraform/clase2
terraform init
terraform plan
terraform apply
terraform destroy      # para limpiar
```

## Clase 2 (Google Cloud): `clase2/google/`

Proyecto independiente (su propio `terraform init` y estado) que despliega una VM en Google Cloud. **Necesita una cuenta de GCP con credenciales** y crea recursos que pueden generar coste.

| Fichero | Contenido |
|---|---|
| `providers.tf`, `variables.tf` | Symlinks a `_shared/gcp/` (provider `hashicorp/google` `8.12.0`, proyecto `edem-108`, región `europe-southwest1`, zona `-a`) |
| `main.tf` | Recurso `google_compute_instance.vm_instance` |

La VM se llama `terraform-instance-nacho`, es de tipo `e2-micro`, usa la imagen `debian-cloud/debian-12` y se conecta a la red `default` con una IP externa (`access_config` vacío).

### Uso (clase 2, Google)

```bash
cd terraform/clase2/google
gcloud auth application-default login   # credenciales para el provider
terraform init
terraform plan
terraform apply
terraform destroy      # para limpiar y evitar costes
```

## Clase 3: `clase3/`

Todo en Google Cloud (**necesita credenciales de GCP** y crea recursos que pueden generar coste). Cada subcarpeta es un proyecto independiente (su propio `terraform init` y estado) y comparte `providers.tf` y `variables.tf` (proyecto `edem-108`, región `europe-southwest1`, zona `europe-southwest1-a`) mediante symlinks a [`_shared/gcp/`](_shared/gcp). Cada una solo tiene su propio código:

| Carpeta | Fichero | Contenido |
|---|---|---|
| `recap/` | `recap.tf`, `variables-recap.tf` | Backend `gcs`, dos VMs y un bucket; variables `os` y `size` |
| `ejercicio1/` | `main.tf` | `google_cloud_run_v2_service.default` (imagen `hangman`, 1 instancia, puerto 5173) y `output "url"` |
| `ejercicio2/` | `main.tf` | `google_storage_bucket.bucket-nacho-gcp` (ubicación `US`) y `google_compute_instance.gci-nacho` (`instance-nacho-gcp`, `e2-micro`, Debian 13, zona `-b`, con `service_account`) |
| `ejercicio3/` | `main.tf` | Vacío por ahora |

### `recap/`

- `google_compute_instance.vm_instance_debian`: VM `terraform-instance-debian` (`e2-micro`) con la imagen `var.os["debian"]` y un disco de `var.size` GB.
- `google_compute_instance.vm_instance_ubuntu`: VM `terraform-instance-ubuntu` (`e2-micro`) con la imagen `var.os["ubuntu"]` y el mismo disco.
- `google_storage_bucket.bucket-nacho`: bucket `bucket-nacho` en `EU` con `force_destroy = true`.
- Variables: `os` (mapa con las imágenes `debian` y `ubuntu`, se usa como `var.os["debian"]`) y `size` (disco en GB, por defecto `50`).

**Estado remoto:** el bloque `backend "gcs"` guarda el estado en el bucket `bucket-nacho-2` (prefijo `terraform/state/edem-108`). Ese bucket **no lo crea este proyecto**: tiene que existir antes del `terraform init` (si no, falla con `bucket doesn't exist`). Si ya habías hecho `init` con estado local, `terraform init -migrate-state` ofrece migrarlo.

### `ejercicio2/`

Ejercicio para **alinear el código con un estado existente**: se leyó el `terraform plan`, que marcaba reemplazos (`# forces replacement`), y se ajustaron `name`, `image`, `key_revocation_action_type`, `zone`, `metadata`, `service_account` y la `location` del bucket hasta que el plan no destruía nada.

### Uso (clase 3)

```bash
cd terraform/clase3/<recap|ejercicio1|ejercicio2|ejercicio3>
gcloud auth application-default login   # credenciales para el provider y el backend
terraform init
terraform plan
terraform apply
terraform destroy      # para limpiar y evitar costes
```

## Organización y ahorro de espacio

- **`_shared/gcp/`**: `providers.tf` y `variables.tf` (proyecto, región y zona) comunes a todos los proyectos de Google Cloud. Cada proyecto los enlaza con un *symlink* (`providers.tf -> ../../_shared/gcp/providers.tf`), así no se repiten y cada carpeta conserva su propio `terraform init` y estado. Si un ejercicio necesita otra zona, la define en el recurso o en un `terraform.tfvars`.
- **Caché de providers**: `~/.terraformrc` define `plugin_cache_dir = "$HOME/.terraform.d/plugin-cache"`. El provider `google` (~125 MB) se descarga una sola vez y cada `.terraform/` solo guarda un enlace (0 B en vez de 125 MB por carpeta). En otra máquina: `mkdir -p ~/.terraform.d/plugin-cache` y crea ese `~/.terraformrc`.
- Los `.terraform/` se pueden borrar sin miedo: `terraform init` los regenera.

## Buenas prácticas

No subas al repo `terraform.tfstate`, `.terraform/` ni ficheros con secretos (`*.tfvars` con contraseñas). El `.gitignore` ya ignora `.terraform`, `.terraform.lock.hcl`, `terraform.lock.hcl` y `*.tfstate*` en cualquier carpeta, y los `tfstate` que estaban versionados en `clase2/` y `clase2/google/` se han sacado del índice con `git rm --cached`. El estado puede contener datos sensibles; para trabajar en equipo usa un estado remoto (p. ej. Google Cloud Storage, como en la clase 3).
