resource "aws_security_group" "vpc_link" {
  name        = "${local.name_prefix}-vpc-link"
  description = "Egress-only security group for API Gateway VPC Link."
  vpc_id      = aws_vpc.main.id

  egress {
    description = "Reach internal ALB"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }
}

resource "aws_apigatewayv2_vpc_link" "app" {
  name               = "${local.name_prefix}-vpc-link"
  subnet_ids         = aws_subnet.private[*].id
  security_group_ids = [aws_security_group.vpc_link.id]
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name_prefix}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_authorizer" "jwt" {
  api_id           = aws_apigatewayv2_api.http.id
  authorizer_type  = "JWT"
  authorizer_uri   = null
  identity_sources = ["$request.header.Authorization"]
  name             = "${local.name_prefix}-jwt"

  jwt_configuration {
    audience = [aws_cognito_user_pool_client.web.id]
    issuer   = "https://cognito-idp.${var.aws_region}.amazonaws.com/${aws_cognito_user_pool.clinic.id}"
  }
}

resource "aws_apigatewayv2_integration" "alb" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "HTTP_PROXY"
  integration_uri        = aws_lb_listener.http.arn
  integration_method     = "ANY"
  connection_type        = "VPC_LINK"
  connection_id          = aws_apigatewayv2_vpc_link.app.id
  payload_format_version = "1.0"

  request_parameters = {
    "overwrite:header.X-Principal-Subject" = "$context.authorizer.claims.sub"
    "overwrite:header.X-Principal-Clinic"  = "$context.authorizer.claims.custom:clinic_id"
    "overwrite:header.X-Principal-Groups"  = "$context.authorizer.claims.cognito:groups"
    "overwrite:header.X-Correlation-ID"    = "$context.requestId"
  }
}

resource "aws_apigatewayv2_route" "default" {
  api_id             = aws_apigatewayv2_api.http.id
  route_key          = "ANY /{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.alb.id}"
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_security_group_rule" "alb_from_vpc_link" {
  type                     = "ingress"
  security_group_id        = aws_security_group.alb.id
  source_security_group_id = aws_security_group.vpc_link.id
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
}
