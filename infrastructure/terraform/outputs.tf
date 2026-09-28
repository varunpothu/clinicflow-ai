output "ecr_repository_url" {
  value       = aws_ecr_repository.app.repository_url
  description = "Container repository used by the application deployment."
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.app.name
  description = "ECS cluster for the application."
}

output "booking_queue_url" {
  value       = aws_sqs_queue.booking_events.url
  description = "Booking event queue."
}
