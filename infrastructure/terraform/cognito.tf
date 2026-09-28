resource "random_string" "cognito_domain" {
  length  = 6
  lower   = true
  upper   = false
  numeric = true
  special = false
}

resource "aws_cognito_user_pool_domain" "clinic" {
  domain       = "${local.name_prefix}-${random_string.cognito_domain.result}"
  user_pool_id = aws_cognito_user_pool.clinic.id
}
resource "aws_cognito_user_pool" "clinic" {
  name = "${local.name_prefix}-users"

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length                   = 12
    require_lowercase                = true
    require_uppercase                = true
    require_numbers                  = true
    require_symbols                  = true
    temporary_password_validity_days = 7
  }

  username_attributes = ["email"]
  user_pool_tier      = "ESSENTIALS"

  schema {
    name                     = "clinic_id"
    attribute_data_type      = "String"
    developer_only_attribute = false
    mutable                  = false
    required                 = false
    string_attribute_constraints {
      min_length = 2
      max_length = 100
    }
  }

  lambda_config {
    pre_token_generation_config {
      lambda_arn     = aws_lambda_function.pre_token_generation.arn
      lambda_version = "V2_0"
    }
  }
}

resource "aws_cognito_user_group" "patient" {
  name         = "PATIENT"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 50
}

resource "aws_cognito_user_group" "receptionist" {
  name         = "RECEPTIONIST"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 20
}

resource "aws_cognito_user_group" "clinician" {
  name         = "CLINICIAN"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 30
}

resource "aws_cognito_user_group" "admin" {
  name         = "ADMIN"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 10
}

resource "aws_cognito_user_pool_client" "web" {
  name         = "${local.name_prefix}-web"
  user_pool_id = aws_cognito_user_pool.clinic.id

  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["openid", "email"]
  supported_identity_providers         = ["COGNITO"]
  callback_urls                        = [var.web_url]
  logout_urls                          = [var.web_url]
}
