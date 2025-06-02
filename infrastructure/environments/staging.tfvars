# Staging Environment Configuration
environment = "staging"
location    = "East US 2"

# Application Configuration
app_name = "sayzhong"

# Storage Configuration
storage_account_tier             = "Standard"
storage_account_replication_type = "GRS"

# Key Vault Configuration
key_vault_sku_name = "standard"

# Redis Configuration
redis_capacity = 1
redis_family   = "C"
redis_sku_name = "Standard"

# Container Registry Configuration
container_registry_sku = "Standard"

# Container App Configuration
container_app_cpu    = 0.5
container_app_memory = "1Gi"

# Tagging
tags = {
  Environment = "staging"
  Project     = "SayZhong"
  Owner       = "QA Team"
  CostCenter  = "QA"
}
