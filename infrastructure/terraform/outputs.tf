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

output "api_gateway_url" {
  value       = aws_apigatewayv2_api.http.api_endpoint
  description = "Authenticated HTTP API endpoint."
}

output "cognito_user_pool_id" {
  value       = aws_cognito_user_pool.clinic.id
  description = "Cognito user pool identifier."
}

output "cognito_client_id" {
  value       = aws_cognito_user_pool_client.web.id
  description = "Public web application client identifier."
}

output "cognito_domain" {
  value       = aws_cognito_user_pool_domain.clinic.domain
  description = "Cognito hosted login domain prefix."
}
output "frontend_bucket_name" {
  value       = aws_s3_bucket.frontend.id
  description = "Private S3 bucket containing the React build."
}

output "cloudfront_distribution_id" {
  value       = aws_cloudfront_distribution.web.id
  description = "CloudFront distribution used for the frontend."
}

output "frontend_url" {
  value       = "https://${aws_cloudfront_distribution.web.domain_name}"
  description = "CloudFront URL for the ClinicFlow web application."
}