On this page

# Syncing from Apache Ossie

Apache Ossie is an open, vendor-neutral specification for defining semantic models in YAML. For more information, see [the documentation](https://ossie.apache.org/).

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Requires the [Hex CLI](/docs/api-integrations/cli#installation) and a [workspace token](/docs/api-integrations/api/overview#workspace-tokens) to sync.
* **Ossie support is in Alpha.** Syncing an Ossie file currently requires a conversion step: use the [Hex CLI](/docs/api-integrations/cli) to convert the file to the Hex semantic model format, then sync it with [Context Sync](/docs/agent-management/context-management/context-sync). Direct import of Ossie files is in active development. Conversion commands, flags, and supported Ossie features are subject to change.

## Concepts[​](#concepts "Direct link to Concepts")

To effectively leverage your Ossie models within Hex, check how key concepts translate between the two platforms.

| Ossie | Hex |
| --- | --- |
| semantic model | semantic project |
| dataset | model |
| field | dimension |
| metric | measure |
| relationship | join |

## Prepare the Ossie file for conversion[​](#prepare-the-ossie-file-for-conversion "Direct link to Prepare the Ossie file for conversion")

To get started, you need an Ossie semantic model document, such as `my-semantic-model.ossie.yaml`. If your semantic layer uses another format, such as dbt or Cube, convert it to Ossie first. The Ossie project maintains [reference converters](https://github.com/apache/ossie-converters) between Ossie and other semantic formats. Hex doesn't provide conversion from other formats into Ossie.

The converter expects a single Ossie document that follows the [`0.2.0.dev0` specification](https://github.com/apache/ossie/blob/main/core-spec/spec.md).

my-semantic-model.ossie.yaml

```
version: 0.2.0.dev0



name: my_semantic_model



datasets:



- name: opportunities



source: b2b_demo_data.prod.dim_opportunities



primary_key:



- opportunity_id



fields:



- name: opportunity_id



datatype: String



expression:



dialects:



- dialect: ANSI_SQL



expression: opportunity_id



- name: account_id



datatype: String



expression:



dialects:



- dialect: ANSI_SQL



expression: account_id



- name: created_date



datatype: Date



dimension:



is_time: true



expression:



dialects:



- dialect: ANSI_SQL



expression: created_date



- name: accounts



source: b2b_demo_data.prod.dim_accounts



primary_key:



- account_id



fields:



- name: account_id



datatype: String



expression:



dialects:



- dialect: ANSI_SQL



expression: account_id



- name: account_name



datatype: String



expression:



dialects:



- dialect: ANSI_SQL



expression: account_name



relationships:



- name: opportunities__accounts



from: opportunities



to: accounts



from_columns:



- account_id



to_columns:



- account_id



metrics:



- name: opportunity_count



datatype: Integer



expression:



dialects:



- dialect: ANSI_SQL



expression: COUNT(DISTINCT opportunities.opportunity_id)
```

Before converting, check that:

* **The document uses `version: 0.2.0.dev0`.** Earlier Ossie snapshots wrap models in a top-level `semantic_model:` list and declare a top-level `dialects:` key. Both cause an `Invalid Ossie document` error. See [Migrating earlier document shapes](https://github.com/apache/ossie/blob/main/core-spec/spec.md#migrating-earlier-document-shapes) to update older files.
* **Every field and metric has a `datatype`.** Supported values are `String`, `Integer`, `Decimal`, `Float`, `Boolean`, `Date`, `Time`, `DateTime`, `DateTimeTz`, and `Opaque`. Without datatype annotations, the conversion succeeds with warnings and falls back to default types.
* **Metric expressions reference fields defined on a dataset, not raw warehouse columns.** References to undefined fields are reported as errors and the affected measures are skipped.

## Step 1: Convert the Ossie file[​](#step-1-convert-the-ossie-file "Direct link to Step 1: Convert the Ossie file")

Run `hex context semantic-project convert` with the Ossie file as the input and a local folder as the output:

```
hex context semantic-project convert \



--from ossie \



--to hex \



--input ./my-semantic-model.ossie.yaml \



--output ./tmp
```

The converter writes one Hex model file per Ossie dataset into a subfolder named after the Ossie model's `name`:

```
tmp/



└── my_semantic_model/



├── accounts.yml



└── opportunities.yml
```

The first time you run the command, the CLI downloads the conversion tooling and prompts you to confirm. In CI environments, the download happens automatically.

| Flag | Description |
| --- | --- |
| `--from <format>` | Source format. Use `ossie`. |
| `--to <format>` | Destination format. Use `hex`. |
| `-i`, `--input <path>` | Path to the Ossie file. |
| `-o`, `--output <path>` | Folder to write the converted Hex semantic model files to. |
| `--dialect <dialect>` | Ossie expression dialect to convert. Defaults to `ansi_sql`. |

### Review conversion problems[​](#review-conversion-problems "Direct link to Review conversion problems")

When the conversion finishes, the CLI prints a count of errors and warnings. Files are still written when there are errors, but anything that failed to convert is left out of the output. Add `-v` to print a grouped summary of every problem:

```
hex -v context semantic-project convert \



--from ossie \



--to hex \



--input ./my-semantic-model.ossie.yaml \



--output ./tmp
```

Common problems include:

| Message | How to resolve |
| --- | --- |
| `A datatype is required in Hex; a default was used.` | Add a `datatype` to the field or metric. Until you do, a default type is applied. |
| `Metric expression references field not in semantic model` | Define the referenced column as a field on the dataset, or update the expression to use an existing field. |
| `Temporal role markers are not supported in Hex and were dropped.` | Add a temporal `datatype`, such as `Date` or `DateTime`, to the field that sets `is_time`. |

Re-run the conversion after you update the Ossie file. Converting into the same output folder overwrites existing model files, but doesn't delete files for datasets you've removed. Delete the output folder before converting to avoid syncing stale models.

## Step 2: Point Context Sync at the converted output[​](#step-2-point-context-sync-at-the-converted-output "Direct link to Step 2: Point Context Sync at the converted output")

Context Sync needs a semantic project in Hex to sync the converted files into. [Create a semantic project](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#create-a-semantic-project) with the **Hex** type, or use an existing one.

In your `hex_context.config.yaml`, add an entry to `semanticProjects`. Set `path` to the converted model folder, which is the subfolder inside your `--output` folder, not the Ossie file:

hex\_context.config.yaml

```
semanticProjects:



- id: <semantic-project-uuid>



path: ./tmp/my_semantic_model
```

To find the semantic project `id`, go to **Context Studio** > **Semantic models**. In the **Semantic projects** table, open the semantic project's **⋯** menu and select **Copy ID**. See [Create a configuration file](/docs/agent-management/context-management/context-sync#create-a-configuration-file) for all configuration options.

## Step 3: Preview and publish[​](#step-3-preview-and-publish "Direct link to Step 3: Preview and publish")

Authenticate with your workspace, then stage the converted files as a preview:

```
hex auth login



hex context preview --title "Import Ossie semantic model"
```

The command returns a preview link you can use to test the semantic project in threads before it's live. When you're ready, publish the most recent preview:

```
hex context publish -
```

If your config file isn't in the repository root, pass `--config-path <path>` to `hex context preview`.

## Sync automatically in CI[​](#sync-automatically-in-ci "Direct link to Sync automatically in CI")

To keep Hex in sync with an Ossie file stored in a repository, run the conversion in your CI workflow before syncing. The conversion runs locally and doesn't need a workspace token. See [Sync automatically in CI](/docs/agent-management/context-management/context-sync#sync-automatically-in-ci) for how to set up the workspace token used to sync.

### Sync from GitHub[​](#sync-from-github "Direct link to Sync from GitHub")

For GitHub repositories, add the Hex CLI install and conversion steps before the upload step in your [Hex Context Toolkit GitHub Action](/docs/agent-management/context-management/context-sync#sync-from-github) workflow:

.github/workflows/hex\_context\_toolkit.yml

```
# ...



jobs:



publish_hex_context:



runs-on: ubuntu-latest



steps:



- name: Checkout



uses: actions/checkout@v6



- name: Install Hex CLI



run: curl -fsSL https://hex.tech/install.sh | bash



- name: Convert semantic model



run: |



hex context semantic-project convert \



--from ossie \



--to hex \



--input ./my-semantic-model.ossie.yaml \



--output ./tmp



- name: Upload context resources



uses: hex-inc/action-context-toolkit@v2



env:



GITHUB_TOKEN: ${{ github.token }}



with:



token: ${{ secrets.HEX_API_TOKEN }}



comment_on_pr: true
```

### Sync from other CI providers[​](#sync-from-other-ci-providers "Direct link to Sync from other CI providers")

For GitLab and other CI providers, install the Hex CLI and run the same conversion command before `hex context preview`. See [Sync from other CI providers](/docs/agent-management/context-management/context-sync#sync-from-other-ci-providers) for the preview and publish steps.

#### On this page

* [Concepts](#concepts)
* [Prepare the Ossie file for conversion](#prepare-the-ossie-file-for-conversion)
* [Step 1: Convert the Ossie file](#step-1-convert-the-ossie-file)
  + [Review conversion problems](#review-conversion-problems)
* [Step 2: Point Context Sync at the converted output](#step-2-point-context-sync-at-the-converted-output)
* [Step 3: Preview and publish](#step-3-preview-and-publish)
* [Sync automatically in CI](#sync-automatically-in-ci)
  + [Sync from GitHub](#sync-from-github)
  + [Sync from other CI providers](#sync-from-other-ci-providers)