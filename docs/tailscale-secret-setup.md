# Tailscale Authentication Key Storage

This document describes how to securely store the Tailscale auth key for the Legion PC remediation.

## GitHub Environments (Recommended)

Store the Tailscale auth key in GitHub Environments:

1. Go to your repository settings → Environments
2. Create environment: `legion-pc`
3. Add secret: `TAILSCALE_AUTH_KEY` = your Tailscale auth key (from https://login.tailscale.com/admin/settings/keys)
4. Configure environment protection rules as needed

## OpenClaw Secrets (Alternative)

```bash
openclaw secrets request TAILSCALE_AUTH_KEY "Tailscale auth key for Legion PC provisioning"
```

## Usage in n8n Workflow

The `deploy-tailscale.json` workflow references `$env.TAILSCALE_AUTH_KEY` which should be set in the n8n environment or passed via the MCP config.

## Security Notes

- Auth keys are reusable but should be treated as secrets
- Rotate after use (Step 18 playbook does this)
- Use ephemeral keys for one-time provisioning when possible
- Restrict key permissions: `--ephemeral --reusable --preauthorized`