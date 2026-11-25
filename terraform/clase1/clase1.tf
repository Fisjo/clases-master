
resource "github_repository" "example" {
  name        = "example"
  description = "My awesome codebase"
  visibility  = "public"
  auto_init   = true
}

resource "github_branch_default" "main" {
  repository = github_repository.example.name
  branch     = "main"
}

resource "github_branch" "develop" {
  repository    = github_repository.example.name
  branch        = "develop"
  source_branch = "main"
}

resource "github_repository_collaborator" "a_repo_collaborator" {
  repository = github_repository.example.name
  username   = var.usuario
  permission = "push"
}

resource "git_clone" "clone" {
  directory      = "${path.module}/example"
  url            = github_repository.example.http_clone_url
  reference_name = "main"
}

resource "local_file" "example" {
  content  = "This is Nacho's repo. This was entirely created with Terraform"
  filename = "${git_clone.clone.directory}/example.txt"
}

resource "git_add" "single_file" {
  directory  = git_clone.clone.directory
  add_paths  = ["example.txt"]
  depends_on = [local_file.example]
}

# commit changes and supply message
resource "git_commit" "commit" {
  directory  = git_clone.clone.directory
  message    = "first terraform commit"
  depends_on = [git_add.single_file]
}

# force push
resource "git_push" "remote" {
  directory  = git_clone.clone.directory
  refspecs   = ["refs/heads/main:refs/heads/main"]
  force      = true
  depends_on = [git_commit.commit]
}

########

resource "github_branch_protection" "main" {
  repository_id  = github_repository.example.node_id
  pattern        = "main"
  enforce_admins = true
  depends_on     = [git_push.remote]

  required_pull_request_reviews {
    dismiss_stale_reviews = true
    restrict_dismissals   = true    
    required_approving_review_count = 1
  }

  required_status_checks {
    strict   = true
    contexts = []
  }
}

resource "github_branch_protection" "develop" {
  repository_id  = github_repository.example.node_id
  pattern        = github_branch.develop.branch
  enforce_admins = true
  depends_on     = [git_push.remote]

  required_pull_request_reviews {
    dismiss_stale_reviews = true
    restrict_dismissals   = true
    required_approving_review_count = 1
  }

  required_status_checks {
    strict   = true
    contexts = []
  }
}

variable "password" {
  type        = string
  description = "Valor de la secret password"
  sensitive   = true
}

resource "github_actions_secret" "password" {
  repository      = github_repository.example.name
  secret_name     = "password"
  plaintext_value = var.password
}

variable "usuario" {
  type        = string
  description = "Usuario de GitHub que se añade como colaborador"
  default     = "AlejCervera"
}
