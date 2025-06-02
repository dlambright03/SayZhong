# Main Terraform configuration for SayZhong infrastructure
# Deploys all Azure resources needed for the application

# Local values for common configurations
locals {
  resource_prefix = "${var.app_name}-${var.environment}"
  
  # Merge default tags with user-provided tags
  default_tags = {
    Environment = var.environment
    Application = var.app_name
    ManagedBy   = "Terraform"
  }
  tags = merge(local.default_tags, var.tags)
}

# Data sources
data "azurerm_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${local.resource_prefix}-rg"
  location = var.location
  tags     = local.tags
}

# Storage Account with Data Lake Gen2
resource "azurerm_storage_account" "main" {
  name                = replace("${local.resource_prefix}storage", "-", "")
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.tags

  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  access_tier              = "Hot"
  
  # Enable hierarchical namespace for Data Lake
  is_hns_enabled           = true
  https_traffic_only_enabled = true
  min_tls_version          = "TLS1_2"
  allow_nested_items_to_be_public = false

  blob_properties {
    delete_retention_policy {
      days = 7
    }
    container_delete_retention_policy {
      days = 7
    }
  }

  network_rules {
    default_action = "Allow"
    bypass         = ["AzureServices"]
  }
}

# Storage containers for different data types
resource "azurerm_storage_container" "user_data" {
  name                  = "user-data"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "learning_content" {
  name                  = "learning-content"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "usage_data" {
  name                  = "usage-data"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Key Vault for secrets management
resource "azurerm_key_vault" "main" {
  name                = "${local.resource_prefix}-vault"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags

  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  enable_rbac_authorization  = true

  network_acls {
    default_action = "Allow"
    bypass         = "AzureServices"
  }
}

# Redis Cache for session management and caching
resource "azurerm_redis_cache" "main" {
  name                = "${local.resource_prefix}-redis"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags

  capacity            = var.redis_sku.capacity
  family              = var.redis_sku.family
  sku_name           = var.redis_sku.name
  non_ssl_port_enabled = false
  minimum_tls_version = "1.2"
  public_network_access_enabled = true

  redis_configuration {
    maxmemory_policy = "allkeys-lru"
  }
}

# Container Registry for Docker images
resource "azurerm_container_registry" "main" {
  name                = replace("${local.resource_prefix}acr", "-", "")
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.tags

  sku           = "Basic"
  admin_enabled = true

  public_network_access_enabled = true
  zone_redundancy_enabled       = false
}

# Log Analytics Workspace for monitoring
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${local.resource_prefix}-logs"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags

  sku               = "PerGB2018"
  retention_in_days = var.log_retention_days
}

# Application Insights for application monitoring
resource "azurerm_application_insights" "main" {
  name                = "${local.resource_prefix}-insights"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags

  application_type                = "web"
  workspace_id                    = azurerm_log_analytics_workspace.main.id
  internet_ingestion_enabled      = true
  internet_query_enabled          = true
}

# Managed Identity for Container Apps
resource "azurerm_user_assigned_identity" "main" {
  name                = "${local.resource_prefix}-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags
}

# Role assignments for Managed Identity
resource "azurerm_role_assignment" "storage_blob_data_contributor" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

resource "azurerm_role_assignment" "key_vault_secrets_user" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

# Container Apps Environment
resource "azurerm_container_app_environment" "main" {
  name                       = "${local.resource_prefix}-env"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tags                       = local.tags
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

# Key Vault Secrets
resource "azurerm_key_vault_secret" "azure_ad_client_id" {
  name         = "azure-ad-client-id"
  value        = var.azure_ad_client_id
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "azure_ad_client_secret" {
  name         = "azure-ad-client-secret"
  value        = var.azure_ad_client_secret
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "azure_ad_tenant_id" {
  name         = "azure-ad-tenant-id"
  value        = var.azure_ad_tenant_id
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "openai_api_key" {
  name         = "openai-api-key"
  value        = var.openai_api_key
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "openai_endpoint" {
  name         = "openai-endpoint"
  value        = var.openai_endpoint
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "storage_connection_string" {
  name         = "storage-connection-string"
  value        = azurerm_storage_account.main.primary_connection_string
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "redis_connection_string" {
  name         = "redis-connection-string"
  value        = "${azurerm_redis_cache.main.hostname}:${azurerm_redis_cache.main.ssl_port},password=${azurerm_redis_cache.main.primary_access_key},ssl=True,abortConnect=False"
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

resource "azurerm_key_vault_secret" "appinsights_connection_string" {
  name         = "appinsights-connection-string"
  value        = azurerm_application_insights.main.connection_string
  key_vault_id = azurerm_key_vault.main.id
  content_type = "text/plain"

  depends_on = [azurerm_role_assignment.key_vault_secrets_user]
}

# Container App
resource "azurerm_container_app" "main" {
  name                         = "${local.resource_prefix}-app"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"
  tags                         = local.tags

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.main.id]
  }

  registry {
    server   = azurerm_container_registry.main.login_server
    identity = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "azure-ad-client-id"
    key_vault_secret_id = azurerm_key_vault_secret.azure_ad_client_id.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "azure-ad-client-secret"
    key_vault_secret_id = azurerm_key_vault_secret.azure_ad_client_secret.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "azure-ad-tenant-id"
    key_vault_secret_id = azurerm_key_vault_secret.azure_ad_tenant_id.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "openai-api-key"
    key_vault_secret_id = azurerm_key_vault_secret.openai_api_key.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "openai-endpoint"
    key_vault_secret_id = azurerm_key_vault_secret.openai_endpoint.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "storage-connection-string"
    key_vault_secret_id = azurerm_key_vault_secret.storage_connection_string.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "redis-connection-string"
    key_vault_secret_id = azurerm_key_vault_secret.redis_connection_string.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  secret {
    name                = "appinsights-connection-string"
    key_vault_secret_id = azurerm_key_vault_secret.appinsights_connection_string.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 8501

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    container {
      name   = "sayzhong-app"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest" # Placeholder
      cpu    = var.container_app_cpu
      memory = var.container_app_memory

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      env {
        name        = "AZURE_AD_CLIENT_ID"
        secret_name = "azure-ad-client-id"
      }

      env {
        name        = "AZURE_AD_CLIENT_SECRET"
        secret_name = "azure-ad-client-secret"
      }

      env {
        name        = "AZURE_AD_TENANT_ID"
        secret_name = "azure-ad-tenant-id"
      }

      env {
        name        = "OPENAI_API_KEY"
        secret_name = "openai-api-key"
      }

      env {
        name        = "OPENAI_ENDPOINT"
        secret_name = "openai-endpoint"
      }

      env {
        name        = "STORAGE_CONNECTION_STRING"
        secret_name = "storage-connection-string"
      }

      env {
        name        = "REDIS_CONNECTION_STRING"
        secret_name = "redis-connection-string"
      }

      env {
        name        = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        secret_name = "appinsights-connection-string"
      }

      env {
        name  = "AZURE_CLIENT_ID"
        value = azurerm_user_assigned_identity.main.client_id
      }
    }

    min_replicas = var.container_app_min_replicas
    max_replicas = var.container_app_max_replicas

    http_scale_rule {
      name                = "http-scaling"
      concurrent_requests = 100
    }
  }

  depends_on = [
    azurerm_role_assignment.key_vault_secrets_user,
    azurerm_key_vault_secret.azure_ad_client_id,
    azurerm_key_vault_secret.azure_ad_client_secret,
    azurerm_key_vault_secret.azure_ad_tenant_id,
    azurerm_key_vault_secret.openai_api_key,
    azurerm_key_vault_secret.openai_endpoint,
    azurerm_key_vault_secret.storage_connection_string,
    azurerm_key_vault_secret.redis_connection_string,
    azurerm_key_vault_secret.appinsights_connection_string
  ]
}
