# Proxy Auth Support Plan

## Overview

Add support for proxy-based API access (e.g., `proxypal-local`) alongside existing OAuth authentication.

**Goal**: Allow users to authenticate via `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL` without OAuth token format validation.

## Current State

- Backend requires OAuth token with `sk-ant-oat01-` prefix (from Keychain)
- `ANTHROPIC_AUTH_TOKEN` already supported but only as fallback
- `ANTHROPIC_BASE_URL` already passed to SDK
- Frontend shows "Authenticated via OAuth" only

## Target State

- Proxy mode: `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL` set → skip OAuth validation
- OAuth mode: Existing behavior unchanged
- Frontend shows "Authenticated via Proxy" when proxy config detected

## Phases

| Phase | Description | Status | Files |
|-------|-------------|--------|-------|
| [Phase 01](./phase-01-backend-auth-proxy-mode.md) | Backend auth proxy mode | ✅ Done | `core/auth.py` |
| [Phase 02](./phase-02-frontend-proxy-status.md) | Frontend proxy status display | ✅ Done | `ClaudeAuthSection.tsx` |
| [Phase 03](./phase-03-env-documentation.md) | Update .env.example docs | ✅ Done | `.env.example` |

## Key Changes Summary

### Backend (`apps/backend/core/auth.py`)
1. Add `is_proxy_mode()` function - detects `ANTHROPIC_BASE_URL` set
2. Modify `get_token_from_keychain()` - skip prefix validation in proxy mode
3. Update `get_auth_token_source()` - return "Proxy" when applicable

### Frontend (`apps/frontend/`)
1. Add proxy mode detection in auth status
2. Show "Authenticated via Proxy" instead of "Authenticated via OAuth"

### Documentation
1. Add proxy setup example to `.env.example`

## Dependencies

- No external dependencies
- No breaking changes to existing OAuth flow

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Proxy token rejected by SDK | Low | High | Test with actual proxy |
| OAuth flow broken | Low | High | Keep OAuth as primary path |

## Success Criteria

- [x] `ANTHROPIC_AUTH_TOKEN=proxypal-local` + `ANTHROPIC_BASE_URL=http://127.0.0.1:8317` works
- [x] Existing OAuth flow unchanged
- [x] Frontend shows correct auth status
