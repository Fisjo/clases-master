variable "os" {
  type = map
  default = {
    "debian" = "debian-cloud/debian-12"
    "ubuntu" = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
  }
}

variable "size" {
  type = number
  default = 50
}