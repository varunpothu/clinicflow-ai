resource "aws_db_subnet_group" "postgres" {
  name       = "${local.name_prefix}-postgres"
  subnet_ids = aws_subnet.private[*].id
}

resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "database" {
  name_prefix = "${local.name_prefix}-database-"
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id

  secret_string = jsonencode({
    username = "clinicflow"
    password = random_password.db.result
  })
}

resource "aws_db_instance" "postgres" {
  identifier             = "${local.name_prefix}-postgres"
  engine                 = "postgres"
  engine_version         = "17"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  max_allocated_storage  = 100
  db_name                = "clinicflow"
  username               = "clinicflow"
  password               = random_password.db.result
  port                   = 5432
  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  storage_encrypted      = true
  skip_final_snapshot    = true

  backup_retention_period = 7
  deletion_protection     = false
}
