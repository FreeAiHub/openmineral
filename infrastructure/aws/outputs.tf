output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "List of public subnets"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "List of private subnets"
  value       = module.vpc.private_subnets
}

output "ecs_cluster_id" {
  description = "The ID of the ECS cluster"
  value       = aws_ecs_cluster.openmineral.id
}

output "ecs_cluster_arn" {
  description = "The ARN of the ECS cluster"
  value       = aws_ecs_cluster.openmineral.arn
}

output "postgresql_endpoint" {
  description = "The endpoint of the PostgreSQL database"
  value       = module.postgresql.endpoint
}

output "redis_endpoint" {
  description = "The endpoint of the Redis cluster"
  value       = module.redis.endpoint
}

output "alb_dns_name" {
  description = "The DNS name of the application load balancer"
  value       = module.alb.dns_name
}

output "alb_zone_id" {
  description = "The zone ID of the application load balancer"
  value       = module.alb.zone_id
}