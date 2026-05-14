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

Workspace context is a single text file that the Hex Agent reads in every conversation.

Use it to define:

* High-level business context
* Interaction style and tone
* Response expectations that should apply broadly

Keep workspace context concise and focused on information that is relevant to most questions your users will ask. See [Best practices for workspace context](/tutorials/ai-best-practices/workspace-context-best-practices).

### How to configure workspace context[​](#how-to-configure-workspace-context "Direct link to How to configure workspace context")

Only Admins and Managers can configure workspace context.

To configure workspace context:

1. Navigate to **Context Studio**
2. Find the **Guides** tab
3. Click **Edit** to open the markdown editor
4. Add your business context, guidelines, and preferences
5. Click **Save** to apply the changes

You can also upload a markdown file directly.

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
* Copy and paste from any historical versions back into your draft.

History provides version control directly in Hex, making it easy to experiment and iterate on guides. History is available for both guides created directly in Hex and those synced from external sources like GitHub.

## Programmatically upload guides in CI[​](#programmatically-upload-guides-in-ci "Direct link to Programmatically upload guides in CI")

Alternatively, if you manage your guides in GitHub, you can use our [GitHub Action](https://github.com/hex-inc/action-context-toolkit) to automatically sync your guides from GitHub to Hex. Guides that are synced from GitHub will be read-only in Hex.

info

You can also use the CLI directly to upload and publish guides using the `hex guide preview` and `hex guide publish` locally, and in other CI providers

### Create a workspace token[​](#create-a-workspace-token "Direct link to Create a workspace token")

From **Settings** > **API keys**, a Workspace Admin will need to create a new [workspace token](/docs/api-integrations/api/overview#workspace-tokens) with your desired expiration (“No Expiry” is recommended) and the "Guides" read and write API scope.

In the GitHub UI for your repository, go to `Settings` > `Secrets and Variables` > `Actions`. [Create a new repository secret](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-a-repository) named `HEX_API_TOKEN`, and set the secret value to the workspace token you just created.

### Create a `hex_context.config.json` file[​](#create-a-hex_contextconfigjson-file "Direct link to create-a-hex_contextconfigjson-file")

In your GitHub repo where your guides live, create a `hex_context.config.json` at the root of your repository that points to where your guides are. There are 2 different ways to point to guides, paths (i.e. `guides/arr.md`) or patterns (i.e. `guides/*.md` - this will match all `.md` files in the `guides` folder). Below is a couple of examples of how you can specify which guides you want to upload.

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

### Add to CI[​](#add-to-ci "Direct link to Add to CI")

#### Using Github[​](#using-github "Direct link to Using Github")

Next, add a GitHub action by creating a file named `hex_context_toolkit.yml` inside of a directory of `.github/workflows`.

```
# .github/workflows/hex_context_toolkit.yml  
name: Publish Hex context  
  
on:  
  push:  
    branches: [ 'main', 'master' ]  
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

After this, changes to guide files detected by your hex\_context.config.json will automatically be kept in sync. You can review and debug actions by looking at the actions tab in the GitHub repository UI and clicking on the `hex_context_toolkit` workflow. When a guide change is detected on your PRs, the GitHub action will add a comment summarizing the changes and a link to test your changes using our Thread preview.

#### Other CI Providers[​](#other-ci-providers "Direct link to Other CI Providers")

Next, configure a CI job using your CI provider of choice. First, you will need to authenticate by passing in [environment variables](/docs/api-integrations/cli#authenticating-in-ci).

On pull requests / branches you can run the `hex guide preview` command which will stage your guide changes and returns a link under `previewLink`

```
export HEX_API_TOKEN='token' # set this in your secret manager  
  
hex auth login --token-from-env HEX_API_TOKEN  
  
hex guide preview --json
```

On push events to the default branch, run the `hex guide preview` command, and extract the previewId and pass it to the `hex guide publish` command

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
* [Programmatically upload guides in CI](#programmatically-upload-guides-in-ci)
  + [Create a workspace token](#create-a-workspace-token)
  + [Create a `hex_context.config.json` file](#create-a-hex_contextconfigjson-file)
  + [Add to CI](#add-to-ci)