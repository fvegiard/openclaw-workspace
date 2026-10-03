# Gateway n8n Plugin Configuration

Added to `/home/fvegiard/.openclaw/openclaw.json`:

```json
"n8n": {
  "enabled": true,
  "config": {
    "baseUrl": "http://n8n:5678",
    "apiKeyEnv": "N8N_API_KEY",
    "enableEdit": true,
    "enableCredentialsWrite": true,
    "backupDir": "~/.n8n-backups"
  }
}
```

**Status:** ✅ Plugin enabled in gateway (verified via `openclaw plugins list`)

**Note:** This config file lives outside the workspace repo at `/home/fvegiard/.openclaw/openclaw.json`. The change is documented here for reproducibility.
