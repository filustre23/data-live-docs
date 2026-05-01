On this page

# Hex Agent in Slack

Ask questions in Slack and get back answers from the Hex Agent.

info

* Hex Agent in Slack is available on our [Team](https://hex.tech/pricing/) plan and above.
* Hex Agent in Slack contributes towards monthly agent usage limits. Later this year we plan to allow you to purchase additional AI usage for power users. Until then, limits will be enforced only as-needed.
* Hex Agent in Slack is currently available on our US Multi-tenant and EU Multi-tenant stacks. Hex Agent is not yet supported on HIPAA Multi-tenant and Single-tenant stacks.
* Users need the **Admin**, **Manager**, **Editor**, or **Explorer¹** workspace role to access the Hex Slack Agent.

¹ Explorers can access Hex Agent in Slack if they have access to Threads. Threads is off by default for Explorers, but can be enabled by a Workspace Admin.

Hex’s Slack integration enables you to interact with Hex [Threads](/docs/explore-data/threads) directly in your Slack workspace. You can ask questions, analyze data, and get AI-powered insights without leaving Slack, making it easier to integrate data analysis into your team's conversations.

## Set up Hex Agent[​](#set-up-hex-agent "Direct link to Set up Hex Agent")

In order to leverage the Hex Agent, Slack must be enabled in your organization's Workspace settings. A Workspace Admin can enable the Slack integration in **Integrations** settings as described [here](/docs/api-integrations/slack).

The Slack integration requires read and write access to your Slack workspace. This allows Hex to read messages when @Hex is tagged and respond to them. We only read messages when Hex is explicitly invoked, so there's no general access to your Slack workspace.

Once Slack is enabled on the Workspace level, **Hex Agent in Slack** must be toggled on.

Users must also individually authenticate into Slack via **Connected apps** Settings in order to access the Hex Agent.

## Hex Agent data connection permissions[​](#hex-agent-data-connection-permissions "Direct link to Hex Agent data connection permissions")

Because the Hex Agent uses [Threads](/docs/explore-data/threads) as its underlying engine, the Hex Agent's permissions will be inherited from Threads.

To answer a user's question, the agent searches across all connections, databases, schemas, and tables that are [included for AI](/docs/explore-data/data-browser#exclusion-and-endorsement) and that the user has access to. If your workspace has a [default data connection](/tutorials/ai-best-practices/setup-for-ai-agents#setup-the-default-data-connection), the agent searches that connection first.

Admins can restrict which data connections the Hex Agent may use when Threads are started from external integrations, including Slack and the [Hex MCP Server](/docs/api-integrations/mcp-server), under **Settings** → **Integrations** → **External integration data connection access**, or on each connection’s **Access** tab under **Settings** → **Data sources**. For more information, see [Hex Agent data connection access](/docs/api-integrations/hex-agent-data-connection-access).

For best practices on descriptions, exclusions, and permissions, see [Optimizing your data connections for the Hex Agent](/tutorials/ai-best-practices/optimizing-data-connections-for-agents).

tip

Threads leveraging an OAuth [data connection](/docs/connect-to-data/data-connections/oauth-data-connections) will send results to public channels, and will leverage the OAuth credentials of the user asking the question.

## Add Hex Agent to Slack[​](#add-hex-agent-to-slack "Direct link to Add Hex Agent to Slack")

Once the Hex Agent has been connected to your Workspace and authenticated by the individual user, the Agent must be added to each Slack channel where it will work. Tagging **@Hex** in a public or private channel will prompt you to add the Hex Agent to the Slack channel if the Hex Agent isn't already a member.

## Ask questions in Slack[​](#ask-questions-in-slack "Direct link to Ask questions in Slack")

You can ask a question to the Hex Agent by tagging **@Hex** in a new Slack message or existing Slack thread, or by directly messaging the Hex Slack app. The Hex Agent works in public and private Slack channels.

Once your question is asked, you will see a "..." emoji automatically applied to your Slack message to indicate that the Hex Agent is formulating a response."

Once the response is formulated, the Agent will apply a checkmark emoji.

## View underlying Threads[​](#view-underlying-threads "Direct link to View underlying Threads")

As part of its response in public and private Slack channels, the Hex Agent will return a Threads link that is Shared with the workspace by default. If you message the Hex Agent directly, the Threads link will be private to you by default.

Anyone who sees the thread in Slack can click and view the Thread's analysis, but only the Thread creator can ask follow up questions to the Hex Agent; other users cannot ask follow-up questions in on another user's Slack thread.

tip

To ask a follow-up question, just reply in the same Slack thread! If the message is in a channel, make sure you @-mention the Hex Agent again in your reply so that it's sent it to the Agent.

## Best practices on Slack setup in Threads[​](#best-practices-on-slack-setup-in-threads "Direct link to Best practices on Slack setup in Threads")

* **Create dedicated Slack channels**: Separate channels for different data domains (e.g., #revenue-insights, #product-analytics, #marketing-metrics) with appropriate permissions and pinned context about available data.
* **Question effectively**: Be specific with time ranges, segments, and metrics ("show Q4 Enterprise ARR by Region" not "show revenue"). Follow up by replying with **@Hex** in the same Slack thread to maintain context.
* **Set clear boundaries**: Hex Agent shines when used for quick insights and explorations. Complex analysis or sensitive customer-specific queries should move to full Hex projects.
* **Brief teams on data visibility**: Ensure users understand that data queried through Slack (and, by extension, public Threads) will appear in Slack channels. Use private channels for sensitive data.
* **Monitor for patterns**: Review common questions often to identify patterns that should become [Semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models) or [Workspace rules](/docs/agent-management/context-management/guides).

#### On this page

* [Set up Hex Agent](#set-up-hex-agent)
* [Hex Agent data connection permissions](#hex-agent-data-connection-permissions)
* [Add Hex Agent to Slack](#add-hex-agent-to-slack)
* [Ask questions in Slack](#ask-questions-in-slack)
* [View underlying Threads](#view-underlying-threads)
* [Best practices on Slack setup in Threads](#best-practices-on-slack-setup-in-threads)