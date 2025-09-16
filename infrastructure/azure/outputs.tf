output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.openmineral.name
}

output "virtual_network_id" {
  description = "The ID of the virtual network"
  value       = azurerm_virtual_network.openmineral.id
}

output "postgresql_fqdn" {
  description = "The FQDN of the PostgreSQL server"
  value       = azurerm_postgresql_flexible_server.openmineral.fqdn
}

output "redis_hostname" {
  description = "The hostname of the Redis cache"
  value       = azurerm_redis_cache.openmineral.hostname
}

output "redis_port" {
  description = "The port of the Redis cache"
  value       = azurerm_redis_cache.openmineral.port
}

output "container_registry_login_server" {
  description = "The login server of the container registry"
  value       = azurerm_container_registry.openmineral.login_server
}

output "application_gateway_id" {
  description = "The ID of the application gateway"
  value       = azurerm_application_gateway.openmineral.id
}

output "public_ip_address" {
  description = "The public IP address of the application gateway"
  value       = azurerm_public_ip.openmineral.ip_address
}