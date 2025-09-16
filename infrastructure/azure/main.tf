terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource group for all resources
resource "azurerm_resource_group" "openmineral" {
  name     = "openmineral-${var.environment}-rg"
  location = var.azure_region

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Virtual network
resource "azurerm_virtual_network" "openmineral" {
  name                = "openmineral-${var.environment}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.openmineral.location
  resource_group_name = azurerm_resource_group.openmineral.name

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Subnets
resource "azurerm_subnet" "frontend" {
  name                 = "frontend-subnet"
  resource_group_name  = azurerm_resource_group.openmineral.name
  virtual_network_name = azurerm_virtual_network.openmineral.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "backend" {
  name                 = "backend-subnet"
  resource_group_name  = azurerm_resource_group.openmineral.name
  virtual_network_name = azurerm_virtual_network.openmineral.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_subnet" "database" {
  name                 = "database-subnet"
  resource_group_name  = azurerm_resource_group.openmineral.name
  virtual_network_name = azurerm_virtual_network.openmineral.name
  address_prefixes     = ["10.0.3.0/24"]
}

# PostgreSQL database
resource "azurerm_postgresql_flexible_server" "openmineral" {
  name                = "openmineral-${var.environment}-postgresql"
  resource_group_name = azurerm_resource_group.openmineral.name
  location            = azurerm_resource_group.openmineral.location

  version    = "15"
  delegated_subnet_id = azurerm_subnet.database.id
  private_dns_zone_id = azurerm_private_dns_zone.postgresql.id

  administrator_login    = "openmineral"
  administrator_password = var.db_password

  storage_mb = 32768

  sku_name = "B_Standard_B1ms"

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Private DNS zone for PostgreSQL
resource "azurerm_private_dns_zone" "postgresql" {
  name                = "postgresql-${var.environment}.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.openmineral.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgresql" {
  name                  = "postgresql-vnet-link"
  private_dns_zone_name = azurerm_private_dns_zone.postgresql.name
  virtual_network_id    = azurerm_virtual_network.openmineral.id
  resource_group_name   = azurerm_resource_group.openmineral.name
}

# Redis Cache
resource "azurerm_redis_cache" "openmineral" {
  name                = "openmineral-${var.environment}-redis"
  resource_group_name = azurerm_resource_group.openmineral.name
  location            = azurerm_resource_group.openmineral.location
  capacity            = 1
  family              = "C"
  sku_name            = "Basic"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"

  redis_configuration {
  }

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Container registry for Docker images
resource "azurerm_container_registry" "openmineral" {
  name                = "openmineral${var.environment}acr"
  resource_group_name = azurerm_resource_group.openmineral.name
  location            = azurerm_resource_group.openmineral.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Application gateway (load balancer)
resource "azurerm_application_gateway" "openmineral" {
  name                = "openmineral-${var.environment}-agw"
  resource_group_name = azurerm_resource_group.openmineral.name
  location            = azurerm_resource_group.openmineral.location

  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "openmineral-gateway-ip-configuration"
    subnet_id = azurerm_subnet.frontend.id
  }

  frontend_port {
    name = "frontend-port"
    port = 80
  }

  frontend_ip_configuration {
    name                 = "frontend-ip-configuration"
    public_ip_address_id = azurerm_public_ip.openmineral.id
  }

  backend_address_pool {
    name = "backend-pool"
  }

  backend_http_settings {
    name                  = "backend-http-settings"
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 20
  }

  http_listener {
    name                           = "frontend-listener"
    frontend_ip_configuration_name = "frontend-ip-configuration"
    frontend_port_name             = "frontend-port"
    protocol                       = "Http"
  }

  request_routing_rule {
    name                       = "frontend-routing-rule"
    rule_type                  = "Basic"
    http_listener_name         = "frontend-listener"
    backend_address_pool_name  = "backend-pool"
    backend_http_settings_name = "backend-http-settings"
  }

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Public IP for application gateway
resource "azurerm_public_ip" "openmineral" {
  name                = "openmineral-${var.environment}-pip"
  resource_group_name = azurerm_resource_group.openmineral.name
  location            = azurerm_resource_group.openmineral.location
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}