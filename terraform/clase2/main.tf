resource "local_file" "pet" {
  filename = var.filename
  content = var.file-content["statement2"]
}


resource "random_pet" "my-pet" {
  prefix = var.prefix[3]
  length = var.length
  separator = var.separator
}

resource "local_file" "pet-name" {
  filename = "${random_pet.my-pet.id}.txt"
  content = "Pets name: ${random_pet.my-pet.id}"
}