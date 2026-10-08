package workshop.access

default allow = false

# Brownfield starter policy: too coarse; participants should add resource and purpose constraints.
allow {
  input.role == "admin"
}
allow {
  input.role == "operator"
  input.action == "read"
}
