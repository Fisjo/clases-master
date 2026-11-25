variable "filename" {
    default = "pets.txt"
}

variable "content" {
    default = "We love pets!"
}

variable "separator" {
    default = "-"
}

variable "length" {
    default = "1"
    type = number
    description = "Length of the pets name"
}

variable "prefix" {
    default = ["Mr", "Mrs", "Sir", "Madam"]
    type = list(string)
}

variable "password_change" {
    default = "true"
    type = bool
}

variable file-content {
    type = map
    default = {
        "statement1" = "We love pets"
        "statement2" = "We hate pets"
    }
}

variable "student" {
    type = object({
      name = string
      age = number
      is_enrrolled = bool
      subjects = set(string)
    })

    default = {
      name = "Nacho"
      age = 22
      is_enrrolled = true
      subjects = ["FSO", "IPC", "BDA"]
    }

}