On this page

# Hex's AI Features

Hex has a suite of AI features that brings the power of natural language to Hex.
Teams save time, answer questions faster, and get more done. Fully integrated
into your workspace, with assistance in any project to ask questions - or make
quick edits in every SQL, Python, Chart,
and Markdown cell.

info

* All [paid plans](https://hex.tech/pricing) include monthly per-seat [credit grants](/docs/administration/credits) that can be used towards Hex AI features. While Hex agents are in Beta, credit limits and optional add-on credits are being rolled out in phases and are not yet enforced for all customers. Admins will receive advance notice before limits go into effect for their workspace.
* Hex's AI features were formerly referred to as Hex Magic in product.

## Core capabilities[​](#core-capabilities "Direct link to Core capabilities")

### Notebook Agent[​](#notebook-agent "Direct link to Notebook Agent")

Use the Notebook Agent as a natural language assistant that generates and edits logic in your notebooks. Ask questions, get code suggestions, and iterate on analyses directly in your notebook, where the agent has full access to your project context and warehouse schema. The Notebook agent is intended to be used by technical users who can audit the SQL and code that the agent suggests.

* Generate and edit cells: The Agent is capable of creating and modifying Python, SQL, Markdown, Pivot, and Chart cells.
* Typeahead: Context-aware, inline code completions as you type. Hit `Tab` to accept, `CMD + →` for token-by-token. Learn more about Typeahead [here](/docs/explore-data/cells/code-typeahead).

[Learn more about the Notebook Agent in docs.](/docs/explore-data/notebook-view/notebook-agent)

### Threads (beta)[​](#threads-beta "Direct link to Threads (beta)")

Use Threads to self-serve data questions based on curated data in a conversational interface. The Threads agent highly prioritizes endorsed and semantically modeled data. The Threads agent is intended to be used by non-technical members outside the data team, but can be used by any users with an Explorer role or higher. [Learn more about Threads in docs.](/docs/explore-data/threads)

### Chat With App Agent (beta)[​](#chat-with-app-agent-beta "Direct link to Chat With App Agent (beta)")

On the published app view, use Chat with App to summarize information in the app, understand the project's underlying logic, update inputs and filters, and run projects! Chat with App is intended to be used by consumers of published apps, and can be used by any users with an Explorer role or higher and Can Explore project permissions. [Learn more about Chat with App in docs.](/docs/explore-data/chat-with-app)

### Modeling Agent[​](#modeling-agent "Direct link to Modeling Agent")

Use the Modeling Agent to generate and edit semantic models within Hex. Tag in warehouse tables or Hex projects to build on existing context. The Modeling Agent can be used by users who can edit semantic models in Hex (Managers and Admins). [Learn more about the Modeling Agent in docs.](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#modeling-agent)

### Context Studio[​](#context-studio "Direct link to Context Studio")

Use the Context Studio to monitor AI usage across your workspace and manage the context that influences agent behavior. Track usage patterns and review agent reasoning, then adjust settings like workspace rules, semantic models, and endorsements to improve agent accuracy and trust. Context Studio is only accessible by Admins and Managers. [Learn more about Context Studio](/docs/agent-management/context-studio).

## Enablement and controls[​](#enablement-and-controls "Direct link to Enablement and controls")

* **Workspace controls**: Admins can enable/disable all AI features for the entire workspace from **Settings > AI & Agents**. See [Enable AI & Agents](/docs/administration/workspace_settings/enable-ai-and-agents).
* **Feature toggles**:
  + Typeahead can be controlled at the workspace and per-user level. See [Typeahead](/docs/explore-data/cells/code-typeahead#enable-typeahead).
* **Plan availability**: Features may vary by plan and beta status. See in-product settings or reach out to `[email protected]` for details.

## Security, privacy, and compliance[​](#security-privacy-and-compliance "Direct link to Security, privacy, and compliance")

* **Hex has zero data retention agreements in place with our AI providers. Hex's AI providers do not train on customer data.** For more details, see [AI data privacy](/docs/trust/ai-data-privacy).
* **BYOK** (Enterprise plan only): Option to route requests via your own API keys for supported AI providers. See [AI data privacy](/docs/trust/ai-data-privacy#bring-your-own-key-byok).
* **Terms**: See the [Hex Service Agreement: Hex Magic](/docs/legal/hex-service-agreement#hex-magic-and-hex-magic-typeahead-collectively-hex-magic).

#### On this page

* [Core capabilities](#core-capabilities)
  + [Notebook Agent](#notebook-agent)
  + [Threads (beta)](#threads-beta)
  + [Chat With App Agent (beta)](#chat-with-app-agent-beta)
  + [Modeling Agent](#modeling-agent)
  + [Context Studio](#context-studio)
* [Enablement and controls](#enablement-and-controls)
* [Security, privacy, and compliance](#security-privacy-and-compliance)