# GitHub Actions to AWS

The deployment workflow uses GitHub Actions OIDC so the workflow can receive short-lived AWS credentials rather than storing long-lived access keys.

## Required GitHub configuration

- repository/environment variable: AWS_REGION
- repository/environment secret: AWS_ROLE_TO_ASSUME

The AWS IAM role must trust GitHub's OIDC provider and scope its trust policy to this repository and deployment environment.

GitHub's current documentation recommends OIDC for AWS authentication and requires id-token: write in the workflow. The role should use restrictive claim conditions so unrelated repositories cannot request credentials. citeturn740826search0turn740826search1

## Why this is better than static keys

No long-lived AWS access key is committed to the repository or stored as a reusable CI credential. The role is assumed for the workflow run and should be granted least-privilege permissions.

## Deployment gate

The workflow is manual by design. This repository does not assume that an AWS account or production role already exists.
