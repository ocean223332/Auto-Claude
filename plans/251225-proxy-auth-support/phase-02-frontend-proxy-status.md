# Phase 02: Frontend Proxy Status Display

## Context

- **Parent Plan**: [plan.md](./plan.md)
- **Dependencies**: [Phase 01](./phase-01-backend-auth-proxy-mode.md)
- **Docs**: Frontend components

## Overview

| Field | Value |
|-------|-------|
| Priority | Medium |
| Status | 🔲 Pending |
| Description | Show "Authenticated via Proxy" in UI when proxy config detected |

## Key Insights

1. `ClaudeAuthSection.tsx` shows "Authenticated via OAuth" hardcoded
2. Auth status comes from `useClaudeAuth.ts` hook
3. Need to pass proxy mode info from backend or detect from env

## Requirements

### Functional
- Display "Authenticated via Proxy" when proxy mode detected
- Show proxy URL in status (optional, for user clarity)

### Non-Functional
- Minimal UI changes
- Backward compatible

## Related Code Files

| File | Action | Description |
|------|--------|-------------|
| `apps/frontend/src/renderer/components/project-settings/ClaudeAuthSection.tsx` | Modify | Update status text |
| `apps/frontend/src/shared/types/index.ts` | Modify | Add proxy mode to env config type |

## Implementation Steps

### Step 1: Update ProjectEnvConfig type

Add to `apps/frontend/src/shared/types/index.ts` (or appropriate types file):

```typescript
export interface ProjectEnvConfig {
  // ... existing fields
  claudeOAuthToken?: string;
  claudeTokenIsGlobal?: boolean;
  // New fields for proxy mode
  anthropicBaseUrl?: string;
  anthropicAuthToken?: string;
  isProxyMode?: boolean;
}
```

### Step 2: Update ClaudeAuthSection.tsx

Modify the status display logic:

```tsx
// Around line 60, update the status text:
<p className="text-xs text-muted-foreground">
  {isCheckingAuth ? 'Checking...' :
    authStatus === 'authenticated' ? (
      envConfig?.isProxyMode 
        ? `Authenticated via Proxy${envConfig?.anthropicBaseUrl ? ` (${envConfig.anthropicBaseUrl})` : ''}`
        : 'Authenticated via OAuth'
    ) :
    authStatus === 'not_authenticated' ? 'Not authenticated' :
    'Status unknown'}
</p>
```

### Step 3: Update auth check IPC handler

In `apps/frontend/src/main/ipc-handlers/env-handlers.ts`, detect proxy mode:

```typescript
// When loading env config, detect proxy mode:
const isProxyMode = !!(process.env.ANTHROPIC_BASE_URL && process.env.ANTHROPIC_AUTH_TOKEN);
const anthropicBaseUrl = process.env.ANTHROPIC_BASE_URL;

return {
  ...existingConfig,
  isProxyMode,
  anthropicBaseUrl,
};
```

## Todo List

- [ ] Add proxy fields to ProjectEnvConfig type
- [ ] Update ClaudeAuthSection status text
- [ ] Update env-handlers to detect proxy mode
- [ ] Test UI displays correctly

## Success Criteria

- [ ] "Authenticated via Proxy" shown when `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` set
- [ ] "Authenticated via OAuth" still shown for OAuth users
- [ ] Proxy URL displayed in status

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Type breaking change | Add optional fields only |
| UI regression | Minimal changes, use existing patterns |

## Security Considerations

- Don't display full auth token
- Only show base URL (non-sensitive)

## Next Steps

After completion → [Phase 03: Env Documentation](./phase-03-env-documentation.md)
