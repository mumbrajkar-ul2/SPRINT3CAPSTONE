# Intentionally incomplete IaC baseline for workshop modernization.
resource "local_file" "workshop_env" {
  filename = "generated-env.txt"
  content  = "shared_user=app_shared"
}
