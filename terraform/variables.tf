variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "repo_name" {
  description = "Artifact Registry repo name"
  type        = string
  default     = "birthdaycalc-repo"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "birthdaycalc-service"
}

variable "image_url" {
  description = "Container image URL (gcr or artifact registry)"
  type        = string
}
