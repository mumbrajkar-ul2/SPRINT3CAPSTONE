# Local settings file for the telecom incident ops repo.
#
# Stage S04-05 Half B. PROPOSED. Owner: Team-Force.
# This file builds no cloud resource. It writes one local text file.
# The text file holds non-secret settings only.
# It holds no user name, no password, no key, and no token.
# Secret names live in .env.example and are set in the process environment (docs/04-secrets/).

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

variable "output_file" {
  description = "Path of the settings file Terraform writes."
  type        = string
  default     = "generated-env.txt"
}

variable "log_level" {
  description = "Log level written to the settings file. Matches the LOG_LEVEL line in .env.example."
  type        = string
  default     = "DEBUG"

  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR"], var.log_level)
    error_message = "log_level must be DEBUG, INFO, WARNING, or ERROR."
  }
}

variable "api_port" {
  description = "Port written to the settings file. uvicorn and api-examples/http-requests.http use 8000."
  type        = number
  default     = 8000

  validation {
    condition     = var.api_port >= 1024 && var.api_port <= 65535
    error_message = "api_port must be between 1024 and 65535."
  }
}

resource "local_file" "workshop_env" {
  filename             = var.output_file
  content              = "LOG_LEVEL=${var.log_level}\nAPI_PORT=${var.api_port}\n"
  file_permission      = "0644"
  directory_permission = "0755"
}

output "settings_file" {
  description = "Where the settings file was written."
  value       = local_file.workshop_env.filename
}
