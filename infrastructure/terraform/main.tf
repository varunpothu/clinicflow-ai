locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

resource "aws_sqs_queue" "booking_dlq" {
  name = "${local.name_prefix}-booking-dlq"
}

resource "aws_sqs_queue" "booking_events" {
  name = "${local.name_prefix}-booking-events"

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.booking_dlq.arn
    maxReceiveCount     = 5
  })
}

resource "aws_s3_bucket" "analytics" {
  bucket_prefix = "${local.name_prefix}-analytics-"
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${local.name_prefix}"
  retention_in_days = 14
}
