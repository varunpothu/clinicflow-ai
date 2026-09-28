variable "aws_region" {
  description = "AWS region for the environment."
  type        = string
  default     = "eu-west-2"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "clinicflow-ai"
}

variable "web_url" {
  description = "Browser application URL used by the Cognito OAuth client."
  type        = string
  default     = "http://localhost:5173"
}