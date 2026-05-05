On this page

# Agent integration data connection access

Workspace **Admins** can limit which data connections the Hex Agent may use in Threads that are started outside of the Hex app.

info

* Users require an [Admin role](/docs/collaborate/sharing-and-permissions/roles) to access this setting.
* Agent integration data connection access applies to both the [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack) and the [Hex MCP Server](/docs/api-integrations/mcp-server).

When a user starts a Thread from an external integration — like the [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack) or the [Hex MCP Server](/docs/api-integrations/mcp-server) — the Hex Agent automatically selects from connections the user has access to, which means a casual question in Slack or an MCP chat could route analysis against data you'd rather keep out of those surfaces.

**Agent integration data connection access** controls which connections the Hex Agent may use for Threads started outside the Hex app. Connections you don't include are unavailable for those external workflows, regardless of the user's individual access. Many teams use this to exclude sensitive or regulated sources from external Threads while keeping day-to-day connections available.

For best practices on descriptions, exclusions, and connection permissions, see [Optimizing your data connections for the Hex Agent](/tutorials/ai-best-practices/optimizing-data-connections-for-agents).

## Configuration[​](#configuration "Direct link to Configuration")

Configure **Agent integration data connection access** in either:

1. **Settings** → **Integrations** → **Agent integration data connection access**

2. **Settings** → **Data sources** → select a data connection → **Access**

## Related documentation[​](#related-documentation "Direct link to Related documentation")

* [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack): using the agent in Slack, permissions, and setup.
* [Hex MCP Server](/docs/api-integrations/mcp-server): connecting Claude, Cursor, and other MCP clients to Hex.

#### On this page

* [Configuration](#configuration)
* [Related documentation](#related-documentation)