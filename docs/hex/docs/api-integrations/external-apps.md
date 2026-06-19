On this page

# External Apps

Connect Hex's agent via MCP to external apps like Notion, Linear, or your own custom MCP-compatible tools.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Users will need the Explorer workspace [role](/docs/collaborate/sharing-and-permissions/roles) or higher to use External Apps.
* External Apps are currently in beta.

Hex agents can use tools from External Apps that your Hex Admin configures. For example, agents can search Notion docs, create Linear issues, or call tools you've built and hosted yourself.

## How External Apps work[​](#how-external-apps-work "Direct link to How External Apps work")

Admins choose which External Apps and which of their tools are available to the workspace. Users then connect the apps they want to use — with their own account, or with shared credentials provided by an Admin — and configure how much approval each tool requires before the agent can call it.

A **tool** is a discrete action the Hex agent can call on an external system — like "search Notion pages" or "create Linear issue". External Apps expose these tools to Hex over [MCP](https://modelcontextprotocol.io/docs/getting-started/intro).

## Set up an External App (Admin)[​](#set-up-an-external-app-admin "Direct link to Set up an External App (Admin)")

1. Go to **Settings > Integrations** or **Context Studio > Apps**.
2. Enable an External App:
   * For Notion or Linear, select **Enable & Connect**.
   * For a custom app, select **+ Custom MCP server** and configure the MCP-compatible endpoint.
3. Once saved, the External App becomes available for users to connect.

### Available External Apps[​](#available-external-apps "Direct link to Available External Apps")

Hex currently supports **Notion** and **Linear** as first-party External Apps. These apps have a streamlined one-click setup, and are vetted and trusted by Hex.

You can also set up a **custom External App** to any app or tool that exposes an [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) endpoint. When adding one, provide:

* **Name** — how the app appears to users and the agent.
* **Description** — what the app does. The agent uses this to decide when to call its tools, so be specific!
* **Server URL** — the MCP endpoint.

### Authentication methods for custom External Apps[​](#authentication-methods-for-custom-external-apps "Direct link to Authentication methods for custom External Apps")

Admins choose an authentication method based on what the server supports:

* **OAuth** — Users sign in to the external app through a standard OAuth pop-up. If the MCP server supports automatic registration, no extra setup is needed.

  + If the server requires you to pre-register Hex as an OAuth app with their provider first, expand **Advanced** in the dialog and use the **Redirect URI** shown in the dialog when registering the app. Once registered, enter the **Client ID**, **Client Secret**, and optional **scopes** from the registration.
* **User provided** — Each user enters their own credentials when connecting. Supported types: Bearer token, Basic auth, or API key, with optional custom headers.
* **Include credentials for users** — One shared set of credentials provided by an Admin and used for all users. Best for when access should use a shared service account or workspace-level credential instead of individual user credentials.

### Configure available tools (Admin)[​](#configure-available-tools-admin "Direct link to Configure available tools (Admin)")

Each External App exposes a set of tools to the Hex agent. Admins choose which tools are available to the workspace.

1. Open **Settings > Integrations**, click the tool count next to an enabled app (e.g., "12 allowed, 3 denied"), or use the **⋯** menu.
2. Toggle individual tools on or off, or use the section header toggle to enable/disable all available **Read-only** or **Write** tools at once. You can hover over each tool to get a description of what each tool does.
3. Set a default policy for new tools to control how Hex handles tools the server adds in the future. You can always allow them, allow only read-only ones, or always block them until an Admin reviews.
4. Click **Save**. Disabled tools are hidden from user config and the agent is aware they are disabled.

## Connect to External Apps as a user[​](#connect-to-external-apps-as-a-user "Direct link to Connect to External Apps as a user")

After an Admin sets up an External App, users need to connect to it themselves before using it in Hex.

1. Go to **Settings → Connected apps → External apps**.
2. Find the app and select **Connect**.
3. Complete the authentication flow.

Once you authenticate, the app is enabled automatically.

Connecting an External App only enables it for you — it does not expose it to other users in your workspace. Use the **⋯** menu to reconnect or disconnect without affecting other users.

### Configure tool permissions (User)[​](#configure-tool-permissions-user "Direct link to Configure tool permissions (User)")

Within the tools your Admin has enabled, each user controls how much approval each tool requires. To control tool approval:

1. Click the **⋯** next to an External App, then click **Tool Settings**.
2. For each tool, pick **Always allow**, **Always ask**, or **Block**. You can also use the section header to apply the same choice for all tools in the section.
3. You can set a default for new tools. This rule applies to any tool you haven't set explicitly.
4. Click **Save**.

## Use External Apps in agent chats[​](#use-external-apps-in-agent-chats "Direct link to Use External Apps in agent chats")

Once connected, Hex agents can call the app's tools in any conversation.

When the agent calls a tool, what happens depends on the tool's policy:

* **Always allow** — the agent runs the tool automatically without interrupting the conversation.
* **Always ask** — the agent pauses and shows an approval prompt with the tool name, arguments, and a description of what will happen. Nothing runs until you accept.
* **Block** — the agent cannot call the tool and will work around it or surface that the action is unavailable.

External Apps are not currently available from the CLI, API, or other headless entry points.

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

| Issue | What to try |
| --- | --- |
| **"Expired" badge on a connection** | Reconnect from Settings → Connected apps. For OAuth, this re-runs the authorization flow. |
| **Agent isn't using an External App you expected** | Confirm the app is toggled on in the conversation's **+** menu. Make sure the app's description clearly states what it does — the agent uses it to decide when to call its tools. |

#### On this page

* [How External Apps work](#how-external-apps-work)
* [Set up an External App (Admin)](#set-up-an-external-app-admin)
  + [Available External Apps](#available-external-apps)
  + [Authentication methods for custom External Apps](#authentication-methods-for-custom-external-apps)
  + [Configure available tools (Admin)](#configure-available-tools-admin)
* [Connect to External Apps as a user](#connect-to-external-apps-as-a-user)
  + [Configure tool permissions (User)](#configure-tool-permissions-user)
* [Use External Apps in agent chats](#use-external-apps-in-agent-chats)
* [Troubleshooting](#troubleshooting)