On this page

# Chat with App

info

* Chat with App is available in public **Beta** on the [Team and Enterprise plans](https://hex.tech/pricing/), which include monthly per-seat [credit grants](/docs/administration/credits) that can be used towards Hex AI features. While Hex agents are in Beta, credit limits and optional add-on credits are being rolled out in phases and are not yet enforced for all customers. Admins will receive advance notice before limits go into effect for their workspace.
* Users require an **[Explorer role](/docs/collaborate/sharing-and-permissions/roles)** or higher to use Chat with App.
* Users must have **[Can explore](/docs/collaborate/sharing-and-permissions/project-sharing)** access or higher on a published app in order to chat with it.
* Users must have **[Can view results](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions)** access or higher on all data connections used in the app.

Chat with App lets you ask natural language questions and run analysis from a conversational sidebar on any published app. Each conversation is backed by the [Threads](/docs/explore-data/threads) agent with the app as context, so in addition to interacting with the app itself - viewing outputs, updating inputs, applying filters, re-running the app - the agent can write and run SQL and python, pull from semantic models, build charts, and work with uploaded files to extend its analysis beyond what is in the app.

## What the agent can do[​](#what-the-agent-can-do "Direct link to What the agent can do")

The agent can interact with the app and run analysis through a single conversational interface:

* **View and summarize project outputs:** Understand and synthesize the results and insights displayed in the app
* **View and summarize project logic:** Give explanations of how metrics used in the app are defined
* **Update input parameters and project filters:** Modify existing input parameters and add or update cell filters to refine and inspect the data in the app
* **Sort tables:** Apply sorts to table displays and pivot tables
* **Query your data warehouse:** Write and run SQL against connected data sources
* **Work with semantic models:** Query metrics and dimensions from your connected semantic layer
* **Build charts and analysis:** Create new visualizations and computed outputs within the conversation
* **Use uploads:** Bring in uploaded files for ad hoc analysis

Each Chat with App conversation kicks off a Thread that can be accessed from both the published app and the typical Threads interface. For a full description of agent capabilities, see [Threads](/docs/explore-data/threads).

## How to use[​](#how-to-use "Direct link to How to use")

[](/assets/medias/chat-with-app-5dcc4c75752fffd82b751ebf2ab2d24b.mp4)

Getting started with Chat with App is simple:

1. **Open the chat sidebar:** Click the interlocking circles icon in the lower right of your published app to open the chat interface
2. **Ask questions:** Type natural language questions or requests in the chat
3. **View responses:** The agent will respond with insights, summaries, or an extended analysis based on your request
4. **Continue in Thread:** Each Chat with App conversation starts a Thread with the app as context. You can view (and continue) the conversation in the Threads interface by clicking the down caret next to the chat title

### Open full thread[​](#open-full-thread "Direct link to Open full thread")

Since each chat with app conversation is its own Thread, you can continue every chat with app conversation in the [Threads](/docs/explore-data/threads) interface. Just click the down carat next to the chat title and select "Open full thread".

[](/assets/medias/chat-with-app-to-thread-739912399cea298f473dfc5a029f82ce.mp4)

### Sharing conversations[​](#sharing-conversations "Direct link to Sharing conversations")

You can share specific Threads that were started from Chat with App with specific users or groups by clicking the down caret next to the chat title. You can grant users **Can view thread** or **Full access** to your Thread.

info

For users to view the shared Thread, they must have **[Can view results](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions)** access or higher to any data connections used by the Thread.

## Best practices[​](#best-practices "Direct link to Best practices")

To get the best results from Chat with App:

* **Use clear, specific questions:** The more specific your question, the better the agent can help
* **Provide context when needed:** Reference specific data or outputs to provide the agent direction
* **Iterate with follow-up questions:** Build on previous responses to refine your analysis

#### On this page

* [What the agent can do](#what-the-agent-can-do)
* [How to use](#how-to-use)
  + [Open full thread](#open-full-thread)
  + [Sharing conversations](#sharing-conversations)
* [Best practices](#best-practices)