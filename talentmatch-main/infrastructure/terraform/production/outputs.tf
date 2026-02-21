output "vpc_id" {
  description = "ID of the production VPC"
  value       = module.vpc.vpc_id
}

output "rds_endpoint" {
  description = "RDS database endpoint"
  value       = module.rds.db_instance_endpoint
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "alb_dns_name" {
  description = "ALB DNS name for API"
  value       = aws_lb.api.dns_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.backend.name
}

output "secrets_manager_arns" {
  description = "ARNs of secrets in Secrets Manager"
  value = {
    jwt_secret          = aws_secretsmanager_secret.jwt_secret.arn
    google_client_id    = aws_secretsmanager_secret.google_client_id.arn
    google_client_secret = aws_secretsmanager_secret.google_client_secret.arn
  }
}
