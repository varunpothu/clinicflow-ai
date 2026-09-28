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
}

resource "aws_cognito_user_pool_group" "patient" {
  name         = "PATIENT"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 50
}

resource "aws_cognito_user_pool_group" "receptionist" {
  name         = "RECEPTIONIST"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 20
}

resource "aws_cognito_user_pool_group" "clinician" {
  name         = "CLINICIAN"
  user_pool_id = aws_cognito_user_pool.clinic.id
  precedence   = 30
}

resource "aws_cognito_user_pool_group" "admin" {
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
}
