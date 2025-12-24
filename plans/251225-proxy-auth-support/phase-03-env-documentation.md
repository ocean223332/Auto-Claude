# Phase 03: Update .env.example Documentation

## Context

- **Parent Plan**: [plan.md](./plan.md)
- **Dependencies**: [Phase 01](./phase-01-backend-auth-proxy-mode.md), [Phase 02](./phase-02-frontend-proxy-status.md)
- **Docs**: `.env.example` files

## Overview

| Field | Value |
|-------|-------|
| Priority | Low |
| Status | 🔲 Pending |
| Description | Document proxy authentication setup in .env.example |

## Related Code Files

| File | Action | Description |
|------|--------|-------------|
| `apps/backend/.env.example` | Modify | Add proxy auth example |

## Implementation Steps

### Step 1: Update AUTHENTICATION section

Update `apps/backend/.env.example` authentication section:

```bash
# =============================================================================
# AUTHENTICATION (REQUIRED - Choose ONE method)
# =============================================================================
#
# METHOD 1: Claude Code OAuth (recommended for personal use)
# ----------------------------------------------------------
# Run `claude setup-token` to save token to macOS Keychain (recommended)
# Or set the token explicitly:
# CLAUDE_CODE_OAUTH_TOKEN=your-oauth-token-here
#
# METHOD 2: Proxy/Gateway Authentication
# ---------------------------------------
# For local proxies (proxypal, ccr, litellm) or API gateways.
# Set BOTH variables together:
#
ANTHROPIC_AUTH_TOKEN=proxypal-local
ANTHROPIC_BASE_URL=http://127.0.0.1:8317
#
# Common proxy setups:
#   - ProxyPal: ANTHROPIC_AUTH_TOKEN=proxypal-local, ANTHROPIC_BASE_URL=http://127.0.0.1:8317
#   - CCR: ANTHROPIC_AUTH_TOKEN=sk-zcf-x-ccr, ANTHROPIC_BASE_URL=http://localhost:3456
#   - LiteLLM: ANTHROPIC_AUTH_TOKEN=your-key, ANTHROPIC_BASE_URL=http://localhost:4000
#
# Related settings (usually set together with proxy):
# NO_PROXY=127.0.0.1
# DISABLE_TELEMETRY=true
# DISABLE_COST_WARNINGS=true
# API_TIMEOUT_MS=600000
```

## Todo List

- [ ] Update .env.example with proxy auth examples
- [ ] Add common proxy setup examples

## Success Criteria

- [ ] Clear documentation for proxy setup
- [ ] Examples for common proxies (ProxyPal, CCR, LiteLLM)
- [ ] Both auth methods documented

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Users confused about methods | Clear METHOD 1/METHOD 2 sections |

## Security Considerations

- Example tokens are placeholders only
- Remind users not to commit real tokens

## Next Steps

After completion → Plan complete, ready for implementation
