On this page

# Context Sync

Programmatically sync context resources into Hex from an external source of truth, such as a git repository.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Requires a [workspace token](/docs/api-integrations/api/overview#workspace-tokens).

You can author and manage context resources outside Hex and sync them to your workspace with the [Hex CLI](/docs/api-integrations/cli) from any environment. This makes it easy to integrate into your existing development and CI workflows. Resources synced this way are read-only in Hex, giving you security and control over the source of truth.

If you're using GitHub, we recommend the [Hex Context Toolkit GitHub Action](https://github.com/hex-inc/action-context-toolkit) to automate syncing and preview changes in pull requests.

Supported resources:

* [Guides](/docs/agent-management/context-management/guides#workspace-guide-library) - including the [workspace context file](/docs/agent-management/context-management/guides#workspace-context)
* [Semantic projects](/docs/connect-to-data/semantic-models/intro-to-semantic-models) sourced from [Hex](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#sync-from-github-optional), [Cube](/docs/connect-to-data/semantic-models/semantic-model-sync/cube), or [dbt MetricFlow](/docs/connect-to-data/semantic-models/semantic-model-sync/dbt-metricflow)

tip

Context Sync does not apply to [Snowflake Semantic Views](/docs/connect-to-data/semantic-models/semantic-model-sync/snowflake-semantic-views) or [Databricks Unity Catalog Metric Views](/docs/connect-to-data/semantic-models/semantic-model-sync/unity-catalog-metric-views). Those resources are stored in the warehouse and are kept up to date through the respective [Data connection](/docs/connect-to-data/data-connections/data-connections-introduction) schema refresh.

## Create a configuration file[​](#create-a-configuration-file "Direct link to Create a configuration file")

In your repository, create a `hex_context.config.json` file in the repository root that points to the resources you want to sync.

Example:

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



],



"semanticProjects": [



{



"id": "<semantic-project-uuid>",



"path": "path/to/dir"



}



]



}
```

### Guides[​](#guides "Direct link to Guides")

There are two ways to point to guides: paths or patterns.

* `path` - the path to a single file.
  + `{ "path": "guides/arr.md" }`
  + Optionally, specify `"hexFilePath"` if you want the path that appears in Hex to be different from its path in your repository.
* `pattern` - a glob that matches multiple files
  + `{ "pattern": "guides/*.md" }` matches all `.md` files directly inside a `guides` folder.
  + `{ "pattern": "guides/**/*.md" }` matches files in subdirectories.
  + Optionally, specify `"transform": { "stripFolders": true }` to rewrite the uploaded path to only include the file name, ignoring the folder path (e.g. `folder1/folder2/guide.md` becomes `guide.md`).

tip

The reserved path `hex.md` (with no preceding directories) is how Hex identifies the [workspace context file](/docs/agent-management/context-management/guides#workspace-context). Use `hexFilePath: "hex.md"` to map any file in your repository to the workspace context slot.

### Semantic projects[​](#semantic-projects "Direct link to Semantic projects")

Each entry in `semanticProjects` requires:

* `id` - the ID of the semantic project in your Hex workspace. To find it, go to **Context Studio** > **Models** > **Semantic projects**, open the semantic project's row action menu, and select **Copy ID**.
* `path` - the path to the local directory containing that project's semantic model and view files.

Before syncing a semantic project this way, make sure it's prepared correctly for import - see [Syncing Hex semantic models](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#sync-from-github-optional), [Syncing from Cube](/docs/connect-to-data/semantic-models/semantic-model-sync/cube), or [Syncing from dbt MetricFlow](/docs/connect-to-data/semantic-models/semantic-model-sync/dbt-metricflow) for details on required metadata and supported features.

## Sync resources with the CLI[​](#sync-resources-with-the-cli "Direct link to Sync resources with the CLI")

The [Hex CLI](/docs/api-integrations/cli) provides a `hex context` command group to sync context programmatically from your local development environment or any CI provider. The commands support both guides and semantic projects in a single workflow.

* `hex context preview` - stages your changes and returns a link you can use to test them against real threads before they're live
* `hex context publish` - publishes a previously staged preview to your workspace

Remember to authenticate with your workspace before using the CLI: `hex auth login`.

## Sync automatically in CI[​](#sync-automatically-in-ci "Direct link to Sync automatically in CI")

Integrate context sync into your CI/CD workflow to generate previews during review, then publish changes when they merge into your primary branch. Your workflow environment needs a workspace token to authenticate the Hex CLI.

### Create a workspace token[​](#create-a-workspace-token "Direct link to Create a workspace token")

A Workspace Admin must create a new [workspace token](/docs/api-integrations/api/overview#workspace-tokens) from **Settings** > **API keys**. Choose an expiration (**No Expiry** is recommended) and grant read and write API scopes for the resources you want to sync, such as **Guides: Read, Write** and **Semantic layer sync**.

### Sync from GitHub[​](#sync-from-github "Direct link to Sync from GitHub")

For GitHub repositories, the [Hex Context Toolkit GitHub Action](https://github.com/hex-inc/action-context-toolkit) is the recommended way to automate syncs. It installs and manages the Hex CLI, publishes changes from your default branch, and can add a context preview to pull requests.

In your repository, go to **Settings** > **Secrets and variables** > **Actions**. [Create a repository secret](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-a-repository) named `HEX_API_TOKEN`, and set it to the workspace token you created.

Create a GitHub Actions workflow by adding a file named `hex_context_toolkit.yml` to the `.github/workflows` directory.

```
name: Publish Hex context



on:



push:



branches: ["main", "master"]



pull_request:



permissions:



contents: read



pull-requests: write



jobs:



publish_hex_context:



runs-on: ubuntu-latest



steps:



- name: Checkout



uses: actions/checkout@v6



- name: Upload context resources



uses: hex-inc/action-context-toolkit@v2



env:



GITHUB_TOKEN: ${{ github.token }}



with:



token: ${{ secrets.HEX_API_TOKEN }}



comment_on_pr: true
```

After you add the workflow, changes to the guides and semantic projects defined in `hex_context.config.json` are synced automatically. You can review and debug runs from the **Actions** tab in the GitHub repository by selecting the `hex_context_toolkit` workflow. On Pull Requests, the workflow will add a comment summarizing any changed resources, along with a link to test them in a thread preview.

For in-depth documentation on workflow configuration, see the [Hex Context Toolkit GitHub Action](https://github.com/hex-inc/action-context-toolkit/blob/main/README.md).

### Sync from other CI providers[​](#sync-from-other-ci-providers "Direct link to Sync from other CI providers")

For GitLab and other CI providers, configure a job that uses the Hex CLI. Authenticate by passing in [environment variables](/docs/api-integrations/cli#authenticating-in-ci).

For pull requests and non-default branches, run `hex context preview`, which stages your changes and returns a link under `previewLink`:

```
export HEX_API_TOKEN='token' # set this in your secret manager



hex auth login --token-from-env HEX_API_TOKEN



hex context preview --json
```

On push events to the default branch, run `hex context preview`, then extract the `previewId` and pass it to `hex context publish`:

```
export HEX_API_TOKEN='token' # set this in your secret manager



hex auth login --token-from-env HEX_API_TOKEN



PREVIEW=$(hex context preview --json)



echo "$PREVIEW"



PREVIEW_ID=$(echo -E "$PREVIEW" | jq -r '.previewId')



UPSERT_COUNT=$(echo -E "$PREVIEW" | jq -r '.guides.upserted | length')



REMOVED_COUNT=$(echo -E "$PREVIEW" | jq -r '.guides.removed | length')



SEMANTIC_PROJECT_COUNT=$(echo -E "$PREVIEW" | jq -r '.semanticProjects | length')



HAS_CHANGES=$(( UPSERT_COUNT > 0 || REMOVED_COUNT > 0 || SEMANTIC_PROJECT_COUNT > 0 ))



if (( HAS_CHANGES )); then



hex context publish "$PREVIEW_ID"



fi
```

If your config file isn't at the default location (`./hex_context.config.json`), pass `--config-path <path>` to `hex context preview`.

## Migrate from the Semantic Model Sync GitHub Action[​](#migrate-from-the-semantic-model-sync-github-action "Direct link to Migrate from the Semantic Model Sync GitHub Action")

caution

The GitHub Actions workflow described in [Semantic Model Sync](/docs/connect-to-data/semantic-models/semantic-model-sync/intro) is deprecated for semantic projects. This workflow calls Hex's `IngestSemanticModel` API which publishes changes without the chance to first preview them in the app. Use the Hex Context Toolkit GitHub Action or the Hex CLI context commands described on this page instead.

To migrate to Context Sync, add the semantic project's `id` and the `path` to its model files to your `hex_context.config.json`. Replace any existing workspace token(s) with a new one that has the **Guides: Read, Write** and **Semantic layer sync** scopes. Use the Hex Context Toolkit GitHub Action or the Hex CLI to stage and publish changes.

All of the advice about preparing an external semantic layer for import into Hex still applies, since it reflects how Hex translates each spec's concepts (not how the files get uploaded):

* [Syncing from Cube](/docs/connect-to-data/semantic-models/semantic-model-sync/cube) - concept mapping and supported feature coverage
* [Syncing from dbt MetricFlow](/docs/connect-to-data/semantic-models/semantic-model-sync/dbt-metricflow) - required `config.meta.hex` metadata, schema requirements, and supported feature coverage

This deprecation doesn't apply to [Snowflake Semantic Views](/docs/connect-to-data/semantic-models/semantic-model-sync/snowflake-semantic-views) or [Databricks Unity Catalog Metric Views](/docs/connect-to-data/semantic-models/semantic-model-sync/unity-catalog-metric-views). Those semantic objects are stored in the respective database, not in a git repository, and continue to sync through their own Data connection schema refresh process.

#### On this page

* [Create a configuration file](#create-a-configuration-file)
  + [Guides](#guides)
  + [Semantic projects](#semantic-projects)
* [Sync resources with the CLI](#sync-resources-with-the-cli)
* [Sync automatically in CI](#sync-automatically-in-ci)
  + [Create a workspace token](#create-a-workspace-token)
  + [Sync from GitHub](#sync-from-github)
  + [Sync from other CI providers](#sync-from-other-ci-providers)
* [Migrate from the Semantic Model Sync GitHub Action](#migrate-from-the-semantic-model-sync-github-action)