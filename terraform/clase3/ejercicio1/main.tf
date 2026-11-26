resource "google_cloud_run_v2_service" "default" {
  name                = "hangman"
  location            = var.region
  deletion_protection = false

  template {
    max_instance_request_concurrency = 1000

    scaling {
      min_instance_count = 1
      max_instance_count = 1
    }

    containers {
      image = "docker.io/shahdev007/hangman:latest"

      ports {
        container_port = 5173
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
    }
  }
}

output "url" {
  value = google_cloud_run_v2_service.default.uri
}
