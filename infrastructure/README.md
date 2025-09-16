# OpenMineral Infrastructure

This directory contains Terraform configurations for deploying the OpenMineral platform on AWS and Azure.

## Structure

- `aws/` - AWS Terraform modules and configurations
  - `compute/` - EC2 instances, Lambda functions
  - `storage/` - S3 buckets, RDS databases
  - `networking/` - VPCs, subnets, security groups
  - `services/` - API Gateway, EKS, CloudWatch
- `azure/` - Azure Terraform modules and configurations
  - `compute/` - Virtual machines, Azure Functions
  - `storage/` - Blob storage, SQL databases
  - `networking/` - Virtual networks, security
  - `services/` - AKS, Azure Monitor, Cognitive Services
- `modules/` - Reusable Terraform modules
  - `database/` - Database module templates
  - `network/` - Networking module templates
  - `compute/` - Compute resource templates
- `environments/` - Environment-specific configurations (dev, staging, prod)
  - `development/` - Development environment
  - `staging/` - Staging environment
  - `production/` - Production environment