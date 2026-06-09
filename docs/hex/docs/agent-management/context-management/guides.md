On this page

# Guides

Provide unstructured context that helps agents interpret questions and respond appropriately.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* **Admins**, **Managers**, **Editors**, and **Explorers** can view the guides tab.
* Only **Admins** and **Managers** can create, edit, and publish guides.

The guides tab is where you can add context about your data and business to help agents interpret questions and respond appropriately across your workspace.

You can provide context in two ways:

* **Workspace context** - always included in every conversation
* **Guide library** - retrieved dynamically when relevant

Use workspace context for broad rules and behavior. Use guides for detailed, task-specific information.

## Workspace context[​](#workspace-context "Direct link to Workspace context")

info

**Recently migrated:** The workspace context file is now part of the same versioning and editing system as your guide library. Existing content has been preserved as a Hex-managed file with the reserved path `hex.md`.

To manage this file outside of Hex, you can delete the Hex-managed guide in the Workbench, and follow the directions below to sync it with your guide library.

Workspace context is a single text file that the Hex Agent reads in every conversation.

Use it to define:

* High-level business context
* Interaction style and tone
* Response expectations that should apply broadly

Keep workspace context concise and focused on information that is relevant to most questions your users will ask. See [Best practices for workspace context](/tutorials/ai-best-practices/workspace-context-best-practices).

### How to configure workspace context[​](#how-to-configure-workspace-context "Direct link to How to configure workspace context")

Only Admins and Managers can configure workspace context.

The workspace context file uses the reserved path `hex.md` and is edited directly in the Context Workbench alongside your other guides. To configure workspace context:

1. Navigate to **Context Studio**
2. Find the **Guides** tab
3. Locate the file with path `hex.md`
4. Edit the file in the Workbench
5. Click **Test and Publish** to preview your changes and publish them live

tip

You can also sync the workspace context file externally using the same CI workflow as the guide library. Ensure that the final path of the file is `hex.md`. If the file lives in a subdirectory in your external source, transform the path with a custom mapping in your [Hex context configuration file](#create-a-hex_contextconfigjson-file).

In the Workbench, the context file is denoted with a special icon and description to indicate its special nature. The context file also does not need frontmatter since the agent will always read it.

## Workspace guide library[​](#workspace-guide-library "Direct link to Workspace guide library")

The workspace guide library is a collection of text files that the Hex Agent dynamically retrieves when they are relevant to the conversation or task. These files can expose detailed business context that the agent can use to perform specific analyses.

### When to use the guide library[​](#when-to-use-the-guide-library "Direct link to When to use the guide library")

Use the workspace guide library for:

* Detailed documentation about specific business processes
* Domain-specific terminology and definitions
* Step-by-step procedures for common analyses
* Context that's only relevant to certain types of questions

Unlike workspace context (which is always included), guide library files are selectively retrieved based on relevance, allowing you to provide more detailed context without overwhelming every conversation.

### Writing guides[​](#writing-guides "Direct link to Writing guides")

To make the most of guides, we recommend adding frontmatter to your guide files, which is used by the Hex Agent to determine when a guide is relevant to the conversation or task. Frontmatter is defined at the start of a guide file by `---` delimiters, and can include a name and description.

```
---



name: Customers



description: Understanding Hex's types of customers



---



...
```

### Project mentions in guides[​](#project-mentions-in-guides "Direct link to Project mentions in guides")

You can @-mention projects in guides. When a guide is retrieved, the agent can use mentioned projects as context. This is useful when describing a workflow or analysis that depends on a specific project.

## Context Workbench[​](#context-workbench "Direct link to Context Workbench")

The Context Workbench provides tools to manage your library of workspace guides. Admins and Managers can edit existing files and add new ones. The workbench supports multi-player workflows, allowing multiple team members to collaborate on context improvements at the same time.

Once you've made your edits, click **Test and Publish**. In the Changes view, you can double-check a diff of every edit that has been made. Use the Threads tab to test specific questions and validate how your changes will affect agent responses before publishing them live. This allows you to iterate and immediately verify that agent behavior improves with each edit. Once you're satisfied with the preview, you can publish your changes to your workspace.

### History[​](#history "Direct link to History")

The History page records a complete version timeline of your guides.

You can:

* View and compare previously published versions.
* Copy and paste from any historical version back into your draft.

History provides version control directly in Hex, making it easy to experiment and iterate on guides. History is available for both guides created directly in Hex and those synced from external sources like GitHub.

## Programmatically upload guides to Hex[​](#programmatically-upload-guides-to-hex "Direct link to Programmatically upload guides to Hex")

Alternatively, you can manage your guides externally. Hex supports uploading guides via the Hex CLI or third-party CI like GitHub Actions.

Guides uploaded from external sources will be read-only in Hex.

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before uploading guides programmatically, you’ll need:

* A [workspace token](/docs/api-integrations/api/overview#workspace-tokens) with the Guides read and write API scope
* A `hex_context.config.json` file that tells Hex which guide files to upload

#### Create a workspace token[​](#create-a-workspace-token "Direct link to Create a workspace token")

From Settings > API keys, a Workspace Admin must create a new [workspace token](/docs/api-integrations/api/overview#workspace-tokens) with the Guides read and write API scope.

“No Expiry” is recommended if the token will be used in CI.

#### Create a configuration file[​](#create-a-configuration-file "Direct link to Create a configuration file")

In the repository where your guides live, create a `hex_context.config.json` file at the root of your repository.

This file tells Hex which guide files to upload. You can reference guides by exact path or by pattern, which matches all Markdown files in the guides folder.

Below are a few examples of how to specify which guides to upload.

```
{



"guides": [



{



"path": "path/to/my/guide.md"



},



{



"path": "path_i_want_to_change.md",



"hexFilePath": "path/that/will/show/up/in/hex.md"



},



{



"pattern": "guides/*.md",



"transform": {



"stripFolders": true



}



},



{



"pattern": "guides/**/*.md"



}



]



}
```

tip

The reserved path `hex.md` (with no preceding directories) is how Hex identifies the [workspace context file](#workspace-context). Use `hexFilePath: "hex.md"` to map any file to the workspace context file.

### Uploading guides via the Hex CLI[​](#uploading-guides-via-the-hex-cli "Direct link to Uploading guides via the Hex CLI")

You can use the [Hex CLI](/docs/api-integrations/cli) to preview and publish guides directly. This is useful for testing guide changes locally before wiring up automated CI, or for publishing guides without a CI provider.

#### Repository setup[​](#repository-setup "Direct link to Repository setup")

Create a `hex_context.config.json` file. More details [here](#create-a-configuration-file).

#### Authenticate[​](#authenticate "Direct link to Authenticate")

For local use, log in with your Hex account:

```
hex auth login
```

Your own permissions apply, so you must be an **Admin** or **Manager** to publish guides.

To test these commands before connecting to a CI provider instead, authenticate with the workspace token you created above. See [other CI providers](#other-ci-providers).

#### Preview changes[​](#preview-changes "Direct link to Preview changes")

Run `hex guide preview` to stage your local guide changes against your workspace without publishing them. The command returns a `previewLink` you can use to test how the agent responds to your changes before they go live.

```
hex guide preview --json
```

#### Publish changes[​](#publish-changes "Direct link to Publish changes")

Once you're satisfied with the preview, publish it by passing the preview's `previewId` to `hex guide publish`:

```
PREVIEW=$(hex guide preview --json)



PREVIEW_ID=$(echo -E "$PREVIEW" | jq -r '.previewId')



hex guide publish "$PREVIEW_ID"
```

### Uploading guides from GitHub[​](#uploading-guides-from-github "Direct link to Uploading guides from GitHub")

If you manage your guides in GitHub, you can use our [GitHub Action](https://github.com/hex-inc/action-context-toolkit) to automatically sync your guides from GitHub to Hex. Follow the steps below to set up automatic uploads of guides from your repository.

#### Add workspace token to your repository[​](#add-workspace-token-to-your-repository "Direct link to Add workspace token to your repository")

In the GitHub UI for your repository, go to `Settings` > `Secrets and Variables` > `Actions`. [Create a new repository secret](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-a-repository) named `HEX_API_TOKEN`, and set the secret value to the workspace token you created.

#### Create the config file[​](#create-the-config-file "Direct link to Create the config file")

Create a `hex_context.config.json`. More details [here](#create-a-configuration-file).

#### Add to CI[​](#add-to-ci "Direct link to Add to CI")

Next, add a GitHub action by creating a file named `hex_context_toolkit.yml` inside of a directory of `.github/workflows`.

```
# .github/workflows/hex_context_toolkit.yml



name: Publish Hex context



on:



push:



branches: ["main", "master"]



pull_request:



permissions:



contents: read



pull-requests: write # Used to comment on pull_requests



jobs:



publish_hex_context:



runs-on: ubuntu-latest



steps:



- name: Checkout



uses: actions/checkout@v6



- name: Upload guide files



uses: hex-inc/action-context-toolkit@v1



env:



GITHUB_TOKEN: ${{ github.token }} # Used to comment on pull_requests



with:



config_file: hex_context.config.json



token: ${{ secrets.HEX_API_TOKEN }} # Create a workspace token with the Guides write scope and set this in your repository settings



# optional configuration



publish_guides: true # publish guides automatically (default true)



delete_untracked_guides: true # removes guides from hex that were also deleted in your repository (default true)



hex_url: https://app.hex.tech # For most Hex users, this will be https://app.hex.tech. For single tenant, EU multi tenant, and HIPAA multi tenant customers, replace app.hex.tech with your custom URL (e.g. atreides.hex.tech, eu.hex.tech).



comment_on_pr: true # To configure this, you must include a `GITHUB_TOKEN` in the env and ensure it has the pull-requests: write permission (see above)
```

After this, changes to guide files detected by your `hex_context.config.json` will automatically be kept in sync. You can review and debug actions by looking at the actions tab in the GitHub repository UI and clicking on the `hex_context_toolkit` workflow. When a guide change is detected on your PRs, the GitHub action will add a comment summarizing the changes and a link to test your changes.

### Other CI Providers[​](#other-ci-providers "Direct link to Other CI Providers")

You can configure a CI job using your provider of choice using Hex CLI commands. First, authenticate by passing in [environment variables](/docs/api-integrations/cli#authenticating-in-ci).

On pull requests/branches, run the `hex guide preview` command to stage your guide changes and return a link under `previewLink`.

```
export HEX_API_TOKEN='token' # set this in your secret manager



hex auth login --token-from-env HEX_API_TOKEN



hex guide preview --json
```

On push events to the default branch, run the `hex guide preview` command, and extract the `previewId` and pass it to the `hex guide publish` command.

```
export HEX_API_TOKEN='token' # set this in your secret manager



hex auth login --token-from-env HEX_API_TOKEN



PREVIEW=$(hex guide preview --json)



echo "$PREVIEW"



PREVIEW_ID=$(echo -E "$PREVIEW" | jq -r '.previewId')



UPSERT_COUNT=$(echo -E "$PREVIEW" | jq -r '.upsertedGuides | length')



REMOVED_COUNT=$(echo -E "$PREVIEW" | jq -r '.removedGuides | length')



HAS_UPSERTS_OR_REMOVALS=$(( UPSERT_COUNT > 0 || REMOVED_COUNT > 0 ))



if (( HAS_UPSERTS_OR_REMOVALS )); then



hex guide publish "$PREVIEW_ID"



fi
```

#### On this page

* [Workspace context](#workspace-context)
  + [How to configure workspace context](#how-to-configure-workspace-context)
* [Workspace guide library](#workspace-guide-library)
  + [When to use the guide library](#when-to-use-the-guide-library)
  + [Writing guides](#writing-guides)
  + [Project mentions in guides](#project-mentions-in-guides)
* [Context Workbench](#context-workbench)
  + [History](#history)
* [Programmatically upload guides to Hex](#programmatically-upload-guides-to-hex)
  + [Prerequisites](#prerequisites)
  + [Uploading guides via the Hex CLI](#uploading-guides-via-the-hex-cli)
  + [Uploading guides from GitHub](#uploading-guides-from-github)
  + [Other CI Providers](#other-ci-providers)