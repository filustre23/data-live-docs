On this page

# Generative apps

Generative apps are a new app type in Hex - you describe what you want, and the Hex agent creates a flexible, fully customizable app to meet your needs.

info

* Generative apps are available in **Beta** on all [plans](https://hex.tech/pricing/). Paid plans include monthly per-seat [credit grants](/docs/administration/credits) that can be used towards Hex AI features. While Hex agents are in Beta, credit limits and optional add-on credits are being rolled out in phases and are not yet enforced for all customers. Admins will receive advance notice before limits go into effect for their workspace.
* Users need [Can Edit](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) or higher permissions on a project to create a Generative app.
* To share suggestions for new features or improvements, reach out to [[email protected]](/cdn-cgi/l/email-protection#c8bbbdb8b8a7babc88a0adb0e6bcadaba0).

Generative apps give you a fully customized, code-generated app experience where the Hex agent builds your UI, visuals, and theming from a plain-language description. Unlike [Classic apps](/docs/share-insights/apps/apps-introduction), which use a fixed grid of standard components, Generative apps produce flexible, web-style interfaces with custom layout, styling, and components tailored to what you're trying to build. This gives you more expressive power when a standard dashboard layout isn't enough.

Generative apps are built from cells in the project's [Notebook view](/docs/explore-data/notebook-view/develop-your-notebook). The agent can build that notebook from scratch, or layer a Generative app on top of an existing one.

[](/assets/medias/editorial-style-gen-app-48d53551663571da97efe2a49dc48998.mp4)

## Create a Generative app[​](#create-a-generative-app "Direct link to Create a Generative app")

tip

The Hex agent is capable of building more than just dashboards! Prompt it to build you a slide deck, or an interactive quiz, or whatever you can think of. Its work will be grounded in your workspace's data and context no matter what you ask it to build.

### From a project[​](#from-a-project "Direct link to From a project")

1. Select the **App builder** tab in a project where you have **Can Edit** or higher permissions.
2. Select **Generative app** when asked for an **app type**.
3. Describe what you want to build in the prompt bar, then submit.
4. The Hex agent will kick off and create your app, and you can continue to iterate with it in the sidebar.

### From your workspace homepage[​](#from-your-workspace-homepage "Direct link to From your workspace homepage")

1. Type a prompt into the prompt bar on your workspace homepage.
2. Select the **Generate an app** intent.
3. Submit your prompt. The Hex agent will open a new project in the **App** view with agent chat so that you can follow its work and keep iterating.

## Iterate on your app[​](#iterate-on-your-app "Direct link to Iterate on your app")

Each time the agent writes or edits a file, the updated app is pushed to the **App** tab live and you'll see the result render as the agent works. You can keep iterating in the sidebar with targeted prompts like:

* "Add a filter for region above the bar chart"
* "Switch the donut to a stacked bar"
* "Match the color palette to our brand: #0F62FE for primary"

The agent can also read the rendered app and its console output, so it can fix layout issues, broken components, and runtime errors when you ask.

## Publish and share your Generative app[​](#publish-and-share-your-generative-app "Direct link to Publish and share your Generative app")

Just like with our Classic apps, the best way to share your Generative app with others is to [publish it](/docs/share-insights/apps/publish-and-share-apps). Publishing makes the latest version visible in the Published App view, while allowing you to continue to iterate in the Notebook view. Publishing on its own does not grant access to other users in your workspace — you still need to explicitly share the project with them before they can see it.

### Scheduled runs and notifications[​](#scheduled-runs-and-notifications "Direct link to Scheduled runs and notifications")

You can set up [scheduled runs](/docs/share-insights/scheduled-runs) to run your Generative app on a defined schedule. Scheduled runs can only be configured on an already published app. Use schedules to [update published results](/docs/share-insights/scheduled-runs#update-published-results) or send [app notifications](/docs/share-insights/app-notifications) - however, Generative apps do not currently support app notifications with an attached screenshot. Configure schedules from the **Scheduled runs** tab in the Notebook sidebar, or from **Scheduled runs & Notifications** menu in the published app.

## Switch between Classic and Generative apps[​](#switch-between-classic-and-generative-apps "Direct link to Switch between Classic and Generative apps")

You can switch a project between Classic and Generative app types from the **App type** menu in the App builder. Switching between app types won't affect your work in either view or the underlying cells in the Notebook. Only one version of your project can be published at a time - you cannot have a single project with both a published Classic and Generative app.

info

A project can only have one published app at a time. If you switch app types and republish, the new app replaces the previously published version - you can't have both a Classic and a Generative published app built from the same underlying Notebook.

## Security FAQ[​](#security-faq "Direct link to Security FAQ")

### How is the agent's generated code isolated?[​](#how-is-the-agents-generated-code-isolated "Direct link to How is the agent's generated code isolated?")

Every Generative app runs inside a nested iframe with a strict content security policy that blocks all javascript outbound network requests, with an exception for Google Fonts. Whatever the agent writes cannot call third-party services or exfiltrate data. The browser blocks the request before it leaves the page.

### How does the app access my data?[​](#how-does-the-app-access-my-data "Direct link to How does the app access my data?")

The iframe has no independent way to fetch data. It receives data exclusively from the backing project's Notebook through a single controlled channel, which means Generative apps automatically inherit your existing Hex permissions. [Data connection access](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions) (including OAuth), [workspace roles](/docs/collaborate/sharing-and-permissions/roles), and [project sharing](/docs/collaborate/sharing-and-permissions/project-sharing) settings all apply to Generative apps the same way they do to Classic apps.

## Limitations[​](#limitations "Direct link to Limitations")

While Generative apps are in Beta, some Hex features are not yet supported. These include:

* [Signed embedding](/docs/share-insights/embedding/signed-embedding)
* [App notifications with screenshots](/docs/share-insights/app-notifications#attaching-screenshots)
* [Saved views](/docs/share-insights/apps/saved-views)
* [Export as PDF](/docs/share-insights/apps/export-as-pdf)
* [CSV downloads](/docs/administration/workspace_settings/workspace-security#download-and-copy-csvs-from-tables)
* [Google Sheets export](/docs/administration/workspace_settings/workspace-security#send-data-to-google-sheets)
* [Published app comments](/docs/collaborate/comments#published-app-comments-vs-notebook-comments)
* [Chat with App](/docs/explore-data/chat-with-app)

#### On this page

* [Create a Generative app](#create-a-generative-app)
  + [From a project](#from-a-project)
  + [From your workspace homepage](#from-your-workspace-homepage)
* [Iterate on your app](#iterate-on-your-app)
* [Publish and share your Generative app](#publish-and-share-your-generative-app)
  + [Scheduled runs and notifications](#scheduled-runs-and-notifications)
* [Switch between Classic and Generative apps](#switch-between-classic-and-generative-apps)
* [Security FAQ](#security-faq)
  + [How is the agent's generated code isolated?](#how-is-the-agents-generated-code-isolated)
  + [How does the app access my data?](#how-does-the-app-access-my-data)
* [Limitations](#limitations)