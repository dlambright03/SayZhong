# Development Environment Configuration
environment = "dev"
location    = "East US"

# Application Configuration
app_name = "sayzhong"

# Storage Configuration
storage_account_tier             = "Standard"
storage_account_replication_type = "LRS"

# Key Vault Configuration
key_vault_sku_name = "standard"

# Redis Configuration
redis_capacity = 0
redis_family   = "C"
redis_sku_name = "Basic"

# Container Registry Configuration
container_registry_sku = "Basic"

# Container App Configuration
container_app_cpu    = 0.25
container_app_memory = "0.5Gi"

# Tagging
tags = {
  Environment = "dev"
  Project     = "SayZhong"
  Owner       = "Development Team"
  CostCenter  = "R&D"
}
