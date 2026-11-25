terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "8.12.0"
    }
  }
}

provider "google" {
    project = "edem-108"
    region  = "europe-southwest1"
    zone    = "europe-southwest1-a"
}