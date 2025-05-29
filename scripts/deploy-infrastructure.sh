#!/bin/bash

# SayZhong Infrastructure Deployment Script
# This script deploys all Azure resources for the SayZhong application

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRASTRUCTURE_DIR="$SCRIPT_DIR/../infrastructure"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if user is logged in to Azure
    if ! az account show &> /dev/null; then
        log_error "You are not logged in to Azure. Please run 'az login' first."
        exit 1
    fi
    
    # Check if Bicep is available
    if ! az bicep version &> /dev/null; then
        log_info "Installing Bicep..."
        az bicep install
    fi
    
    log_info "Prerequisites check completed."
}

# Validate environment parameter
validate_environment() {
    local env=$1
    if [[ ! "$env" =~ ^(dev|staging|prod)$ ]]; then
        log_error "Invalid environment '$env'. Must be one of: dev, staging, prod"
        exit 1
    fi
}

# Get Azure subscription information
get_subscription_info() {
    local subscription_id=$(az account show --query id -o tsv)
    local subscription_name=$(az account show --query name -o tsv)
    log_info "Using Azure subscription: $subscription_name ($subscription_id)"
}

# Deploy infrastructure
deploy_infrastructure() {
    local environment=$1
    local resource_group="sayzhong-${environment}-rg"
    local location="East US"
    local deployment_name="infrastructure-$(date +%Y%m%d-%H%M%S)"
    
    log_info "Deploying infrastructure for environment: $environment"
    
    # Create resource group if it doesn't exist
    log_info "Creating resource group: $resource_group"
    az group create \
        --name "$resource_group" \
        --location "$location" \
        --tags Environment="$environment" Application=sayzhong \
        --output none
    
    # Validate Bicep template
    log_info "Validating Bicep template..."
    az deployment group validate \
        --resource-group "$resource_group" \
        --template-file "$INFRASTRUCTURE_DIR/main.bicep" \
        --parameters "@$INFRASTRUCTURE_DIR/parameters/${environment}.parameters.json" \
        --output none
    
    if [ $? -eq 0 ]; then
        log_info "Template validation successful."
    else
        log_error "Template validation failed."
        exit 1
    fi
    
    # Deploy infrastructure
    log_info "Deploying infrastructure (this may take 10-15 minutes)..."
    az deployment group create \
        --resource-group "$resource_group" \
        --template-file "$INFRASTRUCTURE_DIR/main.bicep" \
        --parameters "@$INFRASTRUCTURE_DIR/parameters/${environment}.parameters.json" \
        --name "$deployment_name" \
        --output table
    
    if [ $? -eq 0 ]; then
        log_info "Infrastructure deployment completed successfully!"
    else
        log_error "Infrastructure deployment failed."
        exit 1
    fi
    
    # Get deployment outputs
    log_info "Retrieving deployment outputs..."
    local outputs=$(az deployment group show \
        --resource-group "$resource_group" \
        --name "$deployment_name" \
        --query properties.outputs \
        --output json)
    
    echo "$outputs" > "$SCRIPT_DIR/../deployment-outputs-${environment}.json"
    log_info "Deployment outputs saved to deployment-outputs-${environment}.json"
    
    # Display important information
    display_deployment_info "$outputs"
}

# Display deployment information
display_deployment_info() {
    local outputs=$1
    
    echo ""
    log_info "=== Deployment Information ==="
    echo ""
    
    local app_url=$(echo "$outputs" | jq -r '.containerAppUrl.value // "N/A"')
    local storage_account=$(echo "$outputs" | jq -r '.storageAccountName.value // "N/A"')
    local key_vault=$(echo "$outputs" | jq -r '.keyVaultName.value // "N/A"')
    local container_registry=$(echo "$outputs" | jq -r '.containerRegistryName.value // "N/A"')
    local managed_identity=$(echo "$outputs" | jq -r '.managedIdentityClientId.value // "N/A"')
    
    echo "Application URL: $app_url"
    echo "Storage Account: $storage_account"
    echo "Key Vault: $key_vault"
    echo "Container Registry: $container_registry"
    echo "Managed Identity Client ID: $managed_identity"
    echo ""
    
    log_info "Next steps:"
    echo "1. Update your CI/CD pipeline with the container registry name"
    echo "2. Configure Azure AD B2C application settings"
    echo "3. Deploy your application using the CI/CD pipeline"
    echo "4. Test the deployment using the application URL above"
}

# Setup Azure AD B2C (placeholder for future implementation)
setup_azure_ad_b2c() {
    log_warn "Azure AD B2C setup is not automated in this script."
    log_warn "Please configure Azure AD B2C manually in the Azure portal:"
    echo "1. Create an Azure AD B2C tenant"
    echo "2. Register the SayZhong application"
    echo "3. Configure user flows for sign-up and sign-in"
    echo "4. Update the parameter files with the correct tenant and client IDs"
}

# Clean up resources (for development/testing)
cleanup_resources() {
    local environment=$1
    local resource_group="sayzhong-${environment}-rg"
    
    log_warn "This will delete ALL resources in the resource group: $resource_group"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deleting resource group: $resource_group"
        az group delete --name "$resource_group" --yes --no-wait
        log_info "Resource group deletion initiated (running in background)"
    else
        log_info "Cleanup cancelled."
    fi
}

# Main script logic
main() {
    local command=${1:-"deploy"}
    local environment=${2:-"dev"}
    
    case $command in
        deploy)
            validate_environment "$environment"
            check_prerequisites
            get_subscription_info
            deploy_infrastructure "$environment"
            setup_azure_ad_b2c
            ;;
        cleanup)
            validate_environment "$environment"
            cleanup_resources "$environment"
            ;;
        validate)
            validate_environment "$environment"
            check_prerequisites
            log_info "Validating Bicep template for environment: $environment"
            az deployment group validate \
                --resource-group "sayzhong-${environment}-rg" \
                --template-file "$INFRASTRUCTURE_DIR/main.bicep" \
                --parameters "@$INFRASTRUCTURE_DIR/parameters/${environment}.parameters.json" \
                --output table
            ;;
        *)
            echo "Usage: $0 [deploy|cleanup|validate] [dev|staging|prod]"
            echo ""
            echo "Commands:"
            echo "  deploy    - Deploy infrastructure to specified environment (default)"
            echo "  cleanup   - Delete all resources in the specified environment"
            echo "  validate  - Validate Bicep template for specified environment"
            echo ""
            echo "Environments:"
            echo "  dev       - Development environment (default)"
            echo "  staging   - Staging environment"
            echo "  prod      - Production environment"
            echo ""
            echo "Examples:"
            echo "  $0 deploy dev"
            echo "  $0 cleanup staging"
            echo "  $0 validate prod"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
