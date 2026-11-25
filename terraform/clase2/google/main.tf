resource "google_compute_instance" "vm_instance" {
    name         = "terraform-instance-nacho"
    machine_type = "e2-micro"

    boot_disk {
        initialize_params {
        image = "debian-cloud/debian-12"
        }
    }

    network_interface {
        # A default network is created for all GCP projects
        network = "default"
        access_config {
        }
    }
 }