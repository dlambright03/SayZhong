# Input variables for SayZhong infrastructure

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "East US"
}

variable "app_name" {
  description = "Application name prefix"
  type        = string
  default     = "sayzhong"
}

variable "azure_ad_tenant_id" {
  description = "Azure AD B2C tenant ID"
  type        = string
  sensitive   = true
}

variable "azure_ad_client_id" {
  description = "Azure AD B2C client ID"
  type        = string
  sensitive   = true
}

variable "azure_ad_client_secret" {
  description = "Azure AD B2C client secret"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "openai_endpoint" {
  description = "OpenAI endpoint URL"
  type        = string
}

variable "redis_sku" {
  description = "Redis cache SKU configuration"
  type = object({
    name     = string
    family   = string
    capacity = number
  })
  default = {
    name     = "Basic"
    family   = "C"
    capacity = 0  # C0 for development
  }
}

variable "container_app_cpu" {
  description = "CPU allocation for container app"
  type        = number
  default     = 0.25
}

variable "container_app_memory" {
  description = "Memory allocation for container app"
  type        = string
  default     = "0.5Gi"
}

variable "container_app_min_replicas" {
  description = "Minimum number of container app replicas"
  type        = number
  default     = 1
}

variable "container_app_max_replicas" {
  description = "Maximum number of container app replicas"
  type        = number
  default     = 10
}

variable "log_retention_days" {
  description = "Log Analytics workspace retention in days"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
