# Frontend Authentication Configuration

Set VITE_APP_ENV=production for the deployed application.

Required production variables:

- VITE_API_BASE_URL
- VITE_COGNITO_DOMAIN
- VITE_COGNITO_CLIENT_ID
- VITE_COGNITO_REDIRECT_URI
- VITE_COGNITO_LOGOUT_URI

The application uses OAuth Authorization Code with PKCE. No Cognito client secret is embedded in the browser.

Terraform uses the web_url variable as the Cognito callback/logout origin. Set it to the deployed web application origin before provisioning production.