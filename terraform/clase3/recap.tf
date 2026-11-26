resource "google_compute_instance" "vm_instance_debian" {
    name         = "terraform-instance-debian"
    machine_type = "e2-micro"

    boot_disk {
        initialize_params {
        image = var.os["debian"]
        size = var.size
        }
    }

    network_interface {
        # A default network is created for all GCP projects
        network = "default"
        access_config {
        }
    }
}

resource "google_compute_instance" "vm_instance_ubuntu" {
    name         = "terraform-instance-ubuntu"
    machine_type = "e2-micro"

    boot_disk {
        initialize_params {
        image = var.os["ubuntu"]
        size = var.size
        }
    }

    network_interface {
        # A default network is created for all GCP projects
        network = "default"
        access_config {
        }
    }
}