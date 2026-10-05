# Frontend Hosting

The production frontend is designed for S3 + CloudFront with Origin Access Control. The S3 bucket is private and CloudFront is the only read path.

Deployment flow:

1. Build the Vite application with production API and Cognito variables.
2. Sync the generated dist directory to the private S3 bucket.
3. Invalidate CloudFront so the new assets are served.
4. Smoke-test the CloudFront URL.

Required GitHub production variables:

- AWS_REGION
- API_GATEWAY_URL
- COGNITO_DOMAIN
- COGNITO_CLIENT_ID
- FRONTEND_BUCKET_NAME
- CLOUDFRONT_DISTRIBUTION_ID
- FRONTEND_URL

Required GitHub production secret:

- AWS_ROLE_TO_ASSUME