// Azure Bicep template for SayZhong infrastructure
// This template deploys all Azure resources needed for the application

@description('Environment name (dev, staging, prod)')
param environment string

@description('Location for all resources')
param location string = resourceGroup().location

@description('Application name prefix')
param appName string = 'sayzhong'

@description('Azure AD B2C tenant ID')
param azureAdTenantId string

@description('Azure AD B2C client ID')
@secure()
param azureAdClientId string

@description('Azure AD B2C client secret')
@secure()
param azureAdClientSecret string

@description('OpenAI API key')
@secure()
param openAiApiKey string

@description('OpenAI endpoint URL')
param openAiEndpoint string

// Variables
var resourcePrefix = '${appName}-${environment}'
var tags = {
  Environment: environment
  Application: appName
  ManagedBy: 'Bicep'
}

// Storage Account for Data Lake
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${replace(resourcePrefix, '-', '')}storage'
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    isHnsEnabled: true // Enable hierarchical namespace for Data Lake
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    encryption: {
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Blob containers for different data types
resource userDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/user-data'
  properties: {
    publicAccess: 'None'
  }
}

resource learningContentContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/learning-content'
  properties: {
    publicAccess: 'None'
  }
}

resource usageDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/usage-data'
  properties: {
    publicAccess: 'None'
  }
}

// Key Vault for secrets management
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${resourcePrefix}-vault'
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: []
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enableRbacAuthorization: true
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Redis Cache for session management and caching
resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: '${resourcePrefix}-redis'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0 // C0 for development, scale up for production
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    redisConfiguration: {
      'maxmemory-policy': 'allkeys-lru'
    }
  }
}

// Container Registry for Docker images
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: '${replace(resourcePrefix, '-', '')}acr'
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
    zoneRedundancy: 'Disabled'
  }
}

// Log Analytics Workspace for monitoring
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourcePrefix}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      searchVersion: 1
      legacy: 0
    }
  }
}

// Application Insights for application monitoring
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-insights'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Container Apps Environment
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: '${resourcePrefix}-env'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

// Managed Identity for Container Apps
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${resourcePrefix}-identity'
  location: location
  tags: tags
}

// Role assignments for Managed Identity
resource storageDataContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, managedIdentity.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource keyVaultSecretsUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, managedIdentity.id, 'KeyVaultSecretsUser')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6') // Key Vault Secrets User
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Store secrets in Key Vault
resource azureAdClientIdSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-ad-client-id'
  properties: {
    value: azureAdClientId
    contentType: 'text/plain'
  }
}

resource azureAdClientSecretSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-ad-client-secret'
  properties: {
    value: azureAdClientSecret
    contentType: 'text/plain'
  }
}

resource azureAdTenantIdSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-ad-tenant-id'
  properties: {
    value: azureAdTenantId
    contentType: 'text/plain'
  }
}

resource openAiApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'openai-api-key'
  properties: {
    value: openAiApiKey
    contentType: 'text/plain'
  }
}

resource openAiEndpointSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'openai-endpoint'
  properties: {
    value: openAiEndpoint
    contentType: 'text/plain'
  }
}

resource storageConnectionStringSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'storage-connection-string'
  properties: {
    value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=${az.environment().suffixes.storage}'
    contentType: 'text/plain'
  }
}

resource redisConnectionStringSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'redis-connection-string'
  properties: {
    value: '${redisCache.name}.redis.cache.windows.net:6380,password=${redisCache.listKeys().primaryKey},ssl=True,abortConnect=False'
    contentType: 'text/plain'
  }
}

resource applicationInsightsConnectionStringSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'appinsights-connection-string'
  properties: {
    value: applicationInsights.properties.ConnectionString
    contentType: 'text/plain'
  }
}

// Container App
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${resourcePrefix}-app'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8501
        allowInsecure: false
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
      secrets: [
        {
          name: 'azure-ad-client-id'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/azure-ad-client-id'
          identity: managedIdentity.id
        }
        {
          name: 'azure-ad-client-secret'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/azure-ad-client-secret'
          identity: managedIdentity.id
        }
        {
          name: 'azure-ad-tenant-id'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/azure-ad-tenant-id'
          identity: managedIdentity.id
        }
        {
          name: 'openai-api-key'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/openai-api-key'
          identity: managedIdentity.id
        }
        {
          name: 'openai-endpoint'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/openai-endpoint'
          identity: managedIdentity.id
        }
        {
          name: 'storage-connection-string'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/storage-connection-string'
          identity: managedIdentity.id
        }
        {
          name: 'redis-connection-string'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/redis-connection-string'
          identity: managedIdentity.id
        }
        {
          name: 'appinsights-connection-string'
          keyVaultUrl: '${keyVault.properties.vaultUri}secrets/appinsights-connection-string'
          identity: managedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest' // Placeholder, will be updated by CI/CD
          name: 'sayzhong-app'
          env: [
            {
              name: 'ENVIRONMENT'
              value: environment
            }
            {
              name: 'AZURE_AD_CLIENT_ID'
              secretRef: 'azure-ad-client-id'
            }
            {
              name: 'AZURE_AD_CLIENT_SECRET'
              secretRef: 'azure-ad-client-secret'
            }
            {
              name: 'AZURE_AD_TENANT_ID'
              secretRef: 'azure-ad-tenant-id'
            }
            {
              name: 'OPENAI_API_KEY'
              secretRef: 'openai-api-key'
            }
            {
              name: 'OPENAI_ENDPOINT'
              secretRef: 'openai-endpoint'
            }
            {
              name: 'STORAGE_CONNECTION_STRING'
              secretRef: 'storage-connection-string'
            }
            {
              name: 'REDIS_CONNECTION_STRING'
              secretRef: 'redis-connection-string'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'appinsights-connection-string'
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: managedIdentity.properties.clientId
            }
          ]
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
}

// Outputs
output storageAccountName string = storageAccount.name
output keyVaultName string = keyVault.name
output containerRegistryName string = containerRegistry.name
output containerAppName string = containerApp.name
output containerAppUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output managedIdentityId string = managedIdentity.id
output managedIdentityClientId string = managedIdentity.properties.clientId
output applicationInsightsInstrumentationKey string = applicationInsights.properties.InstrumentationKey
output applicationInsightsConnectionString string = applicationInsights.properties.ConnectionString
