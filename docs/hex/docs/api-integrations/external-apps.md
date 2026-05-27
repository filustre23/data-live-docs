On this page

# External Apps

Connect Hex's agent to external apps like Notion, Linear, and your own custom MCP-compatible tools.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Users will need the Explorer workspace [role](/docs/collaborate/sharing-and-permissions/roles) or higher to use External Apps.
* External Apps is currently in beta.

Hex agents can use tools from external apps that your Hex Admin configures. For example, agents can search Notion docs, create Linear issues, or call tools you've built and hosted yourself.

## How External Apps work[​](#how-external-apps-work "Direct link to How External Apps work")

Admins choose which External Apps are available to the workspace. Users can then connect the apps they want to use, either with their own account or with shared credentials provided by an Admin.

Once connected, Hex agents can discover and call the app's tools in conversations. Users only see tools from apps they've connected, and each tool call requires approval in the conversation before it runs.

## Set up an External App (Admin)[​](#set-up-an-external-app-admin "Direct link to Set up an External App (Admin)")

1. Go to **Settings > Integrations** (or **Context Studio > Apps**).
2. Enable an External App:
   * **First-party app (Notion or Linear):** open the **⋯** menu next to the app and select **Enable**.
   * **Custom app:** select **+ Custom MCP server** and configure the MCP-compatible endpoint.
3. Once saved, the External App becomes available for users to connect.

### Available External Apps[​](#available-external-apps "Direct link to Available External Apps")

Hex currently supports **Notion** and **Linear** as first-party External Apps. These apps have a streamlined one-click setup, and are vetted and trusted by Hex.

You can also connect a **custom External App** — any app or tool that exposes an [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) endpoint. When adding one, provide:

* **Name** — how the app appears to users and the agent.
* **Description** — what the app does. The agent uses this to decide when to call its tools, so be specific!
* **Server URL** — the MCP endpoint.

### Authentication methods for custom External Apps[​](#authentication-methods-for-custom-external-apps "Direct link to Authentication methods for custom External Apps")

Admins choose an authentication method based on what the server supports:

* **OAuth** — Users sign in to the external app through a standard OAuth pop-up. If the MCP server supports automatic registration, no extra setup is needed.

  + If the server requires you to pre-register Hex as an OAuth app with their provider first, expand **Advanced** in the dialog and use the **Redirect URI** shown in the dialog when registering the app. Once registered, enter the **Client ID**, **Client Secret**, and optional **scopes** from the registration.
* **User provided** — Each user enters their own credentials when connecting. Supported types: Bearer token, Basic auth, or API key, with optional custom headers.
* **Include credentials for users** — One shared set of credentials provided by an Admin and used for all users. Best for when access should use a shared service account or workspace-level credential instead of individual user credentials.

## Connect as a user[​](#connect-as-a-user "Direct link to Connect as a user")

After an Admin sets up an External App, users need to connect to it themselves before using it in Hex.

1. Go to **Settings → Connected apps → External apps**.
2. Find the app and select **Connect**.
3. Complete the authentication flow.

Once you authenticate, the app is enabled automatically.

Connecting an External App only enables it for you — it does not expose it to other users in your workspace. Use the **⋯** menu to reconnect or disconnect without affecting other users.

## Use External Apps in agent chats[​](#use-external-apps-in-agent-chats "Direct link to Use External Apps in agent chats")

Once connected, Hex agents can call the app's tools in any conversation. Each tool call must be accepted in the interface before it runs.

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
* [Connect as a user](#connect-as-a-user)
* [Use External Apps in agent chats](#use-external-apps-in-agent-chats)
* [Troubleshooting](#troubleshooting)