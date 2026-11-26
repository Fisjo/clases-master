resource "google_storage_bucket" "bucket-nacho-gcp" {
    name = "bucket-nacho-gcp"
    location = "US"
}

resource "google_compute_instance" "gci-nacho" {
    name         = "instance-nacho-gcp"
    machine_type = "e2-micro"
    zone         = "europe-southwest1-b"

    key_revocation_action_type = "NONE"

    metadata = {
        enable-osconfig = "TRUE"
    }

    boot_disk {
        initialize_params {
        image = "debian-cloud/debian-13"
        }
    }

    network_interface {
        # A default network is created for all GCP projects
        network = "default"
        access_config {
        }
    }

    service_account {
        email  = "118059907082-compute@developer.gserviceaccount.com"
        scopes = [
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring.write",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/trace.append",
        ]
    }
 }