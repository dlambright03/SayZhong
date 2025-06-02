# Production Environment Configuration
environment = "prod"
location    = "East US"

# Application Configuration
app_name = "sayzhong"

# Storage Configuration
storage_account_tier             = "Standard"
storage_account_replication_type = "GRS"

# Key Vault Configuration
key_vault_sku_name = "premium"

# Redis Configuration
redis_sku = {
  capacity = 2
  family   = "C"
  name     = "Standard"
}

# Container Registry Configuration
container_registry_sku = "Premium"

# Container App Configuration
container_app_cpu    = 1.0
container_app_memory = "2Gi"

# Tagging
tags = {
  Environment = "production"
  Project     = "SayZhong"
  Owner       = "Operations Team"
  CostCenter  = "Production"
}
