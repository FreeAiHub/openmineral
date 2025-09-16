variable "azure_region" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "West US 2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}