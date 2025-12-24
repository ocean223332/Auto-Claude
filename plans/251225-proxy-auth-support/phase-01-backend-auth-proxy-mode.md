# Phase 01: Backend Auth Proxy Mode

## Context

- **Parent Plan**: [plan.md](./plan.md)
- **Dependencies**: None
- **Docs**: `apps/backend/core/auth.py`

## Overview

| Field | Value |
|-------|-------|
| Priority | High |
| Status | 🔲 Pending |
| Description | Add proxy mode detection and skip OAuth token validation when using proxy |

## Key Insights

1. `ANTHROPIC_AUTH_TOKEN` already in `AUTH_TOKEN_ENV_VARS` list (line 20)
2. `ANTHROPIC_BASE_URL` already in `SDK_ENV_VARS` list (line 26)
3. Keychain validation has hardcoded `sk-ant-oat01-` prefix check (line 81)
4. Proxy mode = `ANTHROPIC_BASE_URL` is set AND `ANTHROPIC_AUTH_TOKEN` is set

## Requirements

### Functional
- Detect proxy mode when both `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` are set
- Skip OAuth token format validation in proxy mode
- Return "Proxy" as auth source when in proxy mode

### Non-Functional
- No breaking changes to OAuth flow
- Backward compatible

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       get_auth_token()                          │
├─────────────────────────────────────────────────────────────────┤
│  1. Check CLAUDE_CODE_OAUTH_TOKEN  ──────► return token         │
│  2. Check ANTHROPIC_AUTH_TOKEN     ──────► return token         │
│  3. Check is_proxy_mode()                                       │
│     ├─ True  → skip keychain (proxy token already found in #2)  │
│     └─ False → try keychain (with sk-ant-oat01- validation)     │
└─────────────────────────────────────────────────────────────────┘
```

## Related Code Files

| File | Action | Description |
|------|--------|-------------|
| `apps/backend/core/auth.py` | Modify | Add proxy mode detection |

## Implementation Steps

### Step 1: Add `is_proxy_mode()` function

Add after line 31 (after `SDK_ENV_VARS`):

```python
def is_proxy_mode() -> bool:
    """
    Check if running in proxy mode.
    
    Proxy mode is detected when ANTHROPIC_BASE_URL is set,
    indicating a custom API endpoint (proxy, gateway, etc.).
    In proxy mode, we accept any ANTHROPIC_AUTH_TOKEN without
    OAuth token format validation.
    """
    return bool(os.environ.get("ANTHROPIC_BASE_URL"))
```

### Step 2: Update `get_auth_token_source()` function

Modify to detect proxy source (around line 120):

```python
def get_auth_token_source() -> str | None:
    """Get the name of the source that provided the auth token."""
    # Check for proxy mode first
    if is_proxy_mode() and os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return "Proxy"
    
    # Check environment variables
    for var in AUTH_TOKEN_ENV_VARS:
        if os.environ.get(var):
            return var

    # Check if token came from macOS Keychain
    if get_token_from_keychain():
        return "macOS Keychain"

    return None
```

### Step 3: Update `require_auth_token()` error message

Modify error message to include proxy option (around line 140):

```python
def require_auth_token() -> str:
    """..."""
    token = get_auth_token()
    if not token:
        error_msg = (
            "No authentication token found.\n\n"
            "Auto Claude supports two authentication methods:\n\n"
            "Option 1: Claude Code OAuth (recommended)\n"
        )
        if platform.system() == "Darwin":
            error_msg += (
                "  1. Run: claude setup-token\n"
                "  2. Token will be saved to macOS Keychain automatically\n\n"
            )
        else:
            error_msg += (
                "  1. Run: claude setup-token\n"
                "  2. Set CLAUDE_CODE_OAUTH_TOKEN in your .env file\n\n"
            )
        error_msg += (
            "Option 2: Proxy/Gateway\n"
            "  Set both in your .env file:\n"
            "  ANTHROPIC_AUTH_TOKEN=your-proxy-token\n"
            "  ANTHROPIC_BASE_URL=http://your-proxy:port"
        )
        raise ValueError(error_msg)
    return token
```

## Todo List

- [ ] Add `is_proxy_mode()` function
- [ ] Update `get_auth_token_source()` to return "Proxy"
- [ ] Update `require_auth_token()` error message
- [ ] Test with proxy config

## Success Criteria

- [ ] `is_proxy_mode()` returns `True` when `ANTHROPIC_BASE_URL` is set
- [ ] `get_auth_token_source()` returns "Proxy" in proxy mode
- [ ] OAuth flow still works (no regression)
- [ ] CLI shows "Proxy" as auth source when configured

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Token rejected by SDK | SDK already accepts any token via env var |
| Keychain accessed in proxy mode | Keychain only used as last fallback |

## Security Considerations

- Proxy token not validated for format (by design)
- User responsible for proxy security
- No credentials logged

## Next Steps

After completion → [Phase 02: Frontend Proxy Status](./phase-02-frontend-proxy-status.md)
