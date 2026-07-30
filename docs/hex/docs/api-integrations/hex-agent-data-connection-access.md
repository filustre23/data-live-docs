On this page

# Sensitive data connections for external integrations

Workspace Admins can mark data connections as sensitive so the Hex Agent treats them carefully in Threads started outside of the Hex app.

info

* Users require an [Admin role](/docs/collaborate/sharing-and-permissions/roles) to access this setting.
* Sensitive data connection settings apply to both the [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack) and the [Hex MCP Server](/docs/api-integrations/mcp-server).

When a user starts a Thread from an external integration — like the [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack) or the [Hex MCP Server](/docs/api-integrations/mcp-server) — the Hex Agent automatically selects from connections the user has access to. That means a casual question in Slack or an MCP chat could route analysis against data you'd rather keep off those surfaces.

Marking a connection as **Sensitive** tells Hex to treat it differently in those workflows:

* The [Hex MCP Server](/docs/api-integrations/mcp-server) never uses sensitive connections.
* The [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack#hex-agent-data-connection-permissions) follows a workspace setting that controls whether the agent can use sensitive connections, and how replies appear when it does.

Connections marked **Standard** remain available to the Hex Agent in Slack and MCP, subject to the user's ordinary connection access.

For best practices on descriptions, exclusions, and connection permissions, see [Optimizing your data connections for the Hex Agent](/tutorials/ai-best-practices/optimizing-data-connections-for-agents).

## Configuration[​](#configuration "Direct link to Configuration")

Mark connections as **Standard** or **Sensitive** in either:

1. **Settings** → **Integrations** → **Configure sensitive data connections for external integrations**

2. **Settings** → **Data sources** → select a data connection → **Access**

To choose how the Hex Agent handles sensitive connections in Slack, see [Hex Agent data connection permissions](/docs/share-insights/hex-agent-in-slack#hex-agent-data-connection-permissions).

## Related documentation[​](#related-documentation "Direct link to Related documentation")

* [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack): using the agent in Slack, permissions, and sensitive-connection reply behavior.
* [Hex MCP Server](/docs/api-integrations/mcp-server): connecting Claude, Cursor, and other MCP clients to Hex.

#### On this page

* [Configuration](#configuration)
* [Related documentation](#related-documentation)