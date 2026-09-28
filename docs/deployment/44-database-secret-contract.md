# Database Secret Contract

The application accepts two configuration modes.

## Local

DATABASE_URL can be set directly, for example:

postgresql+psycopg://user:password@host:5432/database

When DATABASE_URL is absent and component variables are absent, the app uses SQLite for zero-dependency local development.

## ECS

ECS injects:

- DATABASE_HOST
- DATABASE_PORT
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD

The password is URL-encoded before the SQLAlchemy URL is built.

This keeps secret material out of the image and avoids embedding credentials in Terraform task environment variables.
