terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC for the application
module "vpc" {
  source = "../modules/network/vpc"

  name = "openmineral-vpc"
  cidr = "10.0.0.0/16"

  azs             = var.availability_zones
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# ECS Cluster for container orchestration
resource "aws_ecs_cluster" "openmineral" {
  name = "openmineral-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# RDS PostgreSQL database
module "postgresql" {
  source = "../modules/database/postgresql"

  identifier = "openmineral-postgresql"

  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = "openmineral"
  username = "openmineral"
  password = var.db_password

  skip_final_snapshot = true

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  db_subnet_group_name   = module.vpc.database_subnet_group_name

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Elasticache Redis
module "redis" {
  source = "../modules/database/redis"

  replication_group_id       = "openmineral-redis"
  node_type                  = "cache.t3.micro"
  engine_version             = "6.2"
  port                       = 6379
  parameter_group_name       = "default.redis6.x"
  maintenance_window         = "sun:05:00-sun:06:00"
  snapshot_window            = "03:00-04:00"
  snapshot_retention_limit   = 7
  apply_immediately          = true
  auto_minor_version_upgrade = true

  num_cache_clusters = 1

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}

# Application Load Balancer
module "alb" {
  source = "../modules/network/alb"

  name = "openmineral-alb"

  vpc_id         = module.vpc.vpc_id
  subnets        = module.vpc.public_subnets
  security_groups = [module.vpc.default_security_group_id]

  target_groups = [
    {
      name             = "openmineral-frontend-tg"
      backend_protocol = "HTTP"
      backend_port     = 3000
      target_type      = "ip"
    },
    {
      name             = "openmineral-backend-tg"
      backend_protocol = "HTTP"
      backend_port     = 8000
      target_type      = "ip"
    }
  ]

  https_listeners = [
    {
      port               = 443
      protocol           = "HTTPS"
      certificate_arn    = var.certificate_arn
      target_group_index = 0
    }
  ]

  http_tcp_listeners = [
    {
      port               = 80
      protocol           = "HTTP"
      target_group_index = 0
    }
  ]

  tags = {
    Environment = var.environment
    Project     = "OpenMineral"
  }
}