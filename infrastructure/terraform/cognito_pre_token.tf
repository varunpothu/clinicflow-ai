data "archive_file" "pre_token_generation" {
  type        = "zip"
  source_file = "${path.module}/../../lambda/pre-token-generation/index.py"
  output_path = "${path.module}/.generated/pre-token-generation.zip"
}

resource "aws_iam_role" "pre_token_generation" {
  name = "${local.name_prefix}-cognito-pre-token"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "pre_token_generation_logs" {
  role       = aws_iam_role.pre_token_generation.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "pre_token_generation" {
  function_name    = "${local.name_prefix}-cognito-pre-token"
  role             = aws_iam_role.pre_token_generation.arn
  runtime          = "python3.12"
  handler          = "index.handler"
  filename         = data.archive_file.pre_token_generation.output_path
  source_code_hash = data.archive_file.pre_token_generation.output_base64sha256
  timeout          = 5
  memory_size      = 128
}

resource "aws_lambda_permission" "cognito_pre_token_generation" {
  statement_id  = "AllowCognitoPreTokenGeneration"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pre_token_generation.function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.clinic.arn
}