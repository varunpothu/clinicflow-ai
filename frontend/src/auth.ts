const ACCESS_TOKEN_KEY = "clinicflow_access_token";
const REFRESH_TOKEN_KEY = "clinicflow_refresh_token";
const EXPIRES_AT_KEY = "clinicflow_expires_at";
const STATE_KEY = "clinicflow_oauth_state";
const VERIFIER_KEY = "clinicflow_pkce_verifier";

const configured = {
  domain: import.meta.env.VITE_COGNITO_DOMAIN ?? "",
  clientId: import.meta.env.VITE_COGNITO_CLIENT_ID ?? "",
  redirectUri: import.meta.env.VITE_COGNITO_REDIRECT_URI ?? `${window.location.origin}/auth/callback`,
  logoutUri: import.meta.env.VITE_COGNITO_LOGOUT_URI ?? window.location.origin,
};

export const productionAuthEnabled = (import.meta.env.VITE_APP_ENV ?? "local") === "production";

function base64Url(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

async function createPkce(): Promise<{ verifier: string; challenge: string }> {
  const verifier = base64Url(crypto.getRandomValues(new Uint8Array(32)));
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier));
  return { verifier, challenge: base64Url(new Uint8Array(digest)) };
}

export function isAuthenticated(): boolean {
  const token = sessionStorage.getItem(ACCESS_TOKEN_KEY);
  const expiresAt = Number(sessionStorage.getItem(EXPIRES_AT_KEY) ?? 0);
  return Boolean(token) && expiresAt > Date.now() + 30_000;
}

export async function login(): Promise<void> {
  if (!configured.domain || !configured.clientId) throw new Error("COGNITO_CONFIG_MISSING");
  const state = base64Url(crypto.getRandomValues(new Uint8Array(24)));
  const { verifier, challenge } = await createPkce();
  sessionStorage.setItem(STATE_KEY, state);
  sessionStorage.setItem(VERIFIER_KEY, verifier);
  const params = new URLSearchParams({
    response_type: "code",
    client_id: configured.clientId,
    redirect_uri: configured.redirectUri,
    scope: "openid email",
    state,
    code_challenge: challenge,
    code_challenge_method: "S256",
  });
  window.location.assign(`https://${configured.domain}/oauth2/authorize?${params.toString()}`);
}

export async function handleAuthCallback(search: string): Promise<void> {
  const params = new URLSearchParams(search);
  const code = params.get("code");
  const state = params.get("state");
  const expectedState = sessionStorage.getItem(STATE_KEY);
  const verifier = sessionStorage.getItem(VERIFIER_KEY);
  if (!code || !state || !expectedState || state !== expectedState || !verifier) {
    throw new Error("OAUTH_CALLBACK_INVALID");
  }

  const response = await fetch(`https://${configured.domain}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      client_id: configured.clientId,
      code,
      redirect_uri: configured.redirectUri,
      code_verifier: verifier,
    }),
  });
  if (!response.ok) throw new Error("OAUTH_TOKEN_EXCHANGE_FAILED");
  const token = await response.json() as { access_token: string; refresh_token?: string; expires_in: number };
  sessionStorage.setItem(ACCESS_TOKEN_KEY, token.access_token);
  if (token.refresh_token) sessionStorage.setItem(REFRESH_TOKEN_KEY, token.refresh_token);
  sessionStorage.setItem(EXPIRES_AT_KEY, String(Date.now() + token.expires_in * 1000));
  sessionStorage.removeItem(STATE_KEY);
  sessionStorage.removeItem(VERIFIER_KEY);
}

async function refresh(): Promise<string | null> {
  const refreshToken = sessionStorage.getItem(REFRESH_TOKEN_KEY);
  if (!refreshToken || !configured.domain || !configured.clientId) return null;
  const response = await fetch(`https://${configured.domain}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      client_id: configured.clientId,
      refresh_token: refreshToken,
    }),
  });
  if (!response.ok) return null;
  const token = await response.json() as { access_token: string; expires_in: number };
  sessionStorage.setItem(ACCESS_TOKEN_KEY, token.access_token);
  sessionStorage.setItem(EXPIRES_AT_KEY, String(Date.now() + token.expires_in * 1000));
  return token.access_token;
}

export async function getAccessToken(): Promise<string | null> {
  if (!productionAuthEnabled) return null;
  if (isAuthenticated()) return sessionStorage.getItem(ACCESS_TOKEN_KEY);
  return refresh();
}

export async function getAuthHeaders(): Promise<Record<string, string>> {
  if (!productionAuthEnabled) {
    return {
      "X-Demo-Role": "PATIENT",
      "X-Demo-Subject": "00000000-0000-4000-8000-000000000001",
    };
  }
  const token = await getAccessToken();
  if (!token) throw new Error("AUTH_REQUIRED");
  return { Authorization: `Bearer ${token}` };
}

export function logout(): void {
  sessionStorage.clear();
  if (productionAuthEnabled && configured.domain && configured.clientId) {
    const params = new URLSearchParams({
      client_id: configured.clientId,
      logout_uri: configured.logoutUri,
    });
    window.location.assign(`https://${configured.domain}/logout?${params.toString()}`);
    return;
  }
  window.location.assign("/");
}