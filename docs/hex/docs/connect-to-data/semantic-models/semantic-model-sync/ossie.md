On this page

# Syncing from Apache Ossie

Apache Ossie is an open, vendor-neutral specification for defining semantic models in YAML. For more information, see [the documentation](https://ossie.apache.org/).

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Requires the [Hex CLI](/docs/api-integrations/cli#installation) and a [workspace token](/docs/api-integrations/api/overview#workspace-tokens) to sync.
* **Ossie support is in Alpha.** Use the [Hex CLI](/docs/api-integrations/cli), locally or in CI, to convert and sync Ossie files with [Context Sync](/docs/agent-management/context-management/context-sync). Conversion commands, flags, and supported Ossie features are subject to change.

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

To get started, you need an Ossie semantic model document, such as `my-semantic-model.ossie.yaml`. For dbt projects, the Hex CLI can convert a semantic manifest to Hex through Ossie in one command; see [dbt conversion](#dbt). For other formats, the Ossie project maintains [reference converters](https://github.com/apache/ossie-converters) that you can use to create an Ossie document first.

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

## Convert and review locally[​](#convert-and-review-locally "Direct link to Convert and review locally")

Conversion runs locally and doesn't require a workspace token. To inspect the converted files before syncing to Hex, run `hex context semantic-project convert` with the Ossie file as the input and a local folder as the output:

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

When the conversion finishes, the CLI prints a count of errors and warnings. Files are still written when there are errors, but anything that failed to convert is left out of the output. Add `-v` to print a grouped summary of every problem. Add `-vv` to print every problem individually:

```
hex context semantic-project convert \



--from ossie \



--to hex \



--input ./my-semantic-model.ossie.yaml \



--output ./tmp \



-v
```

Common problems include:

| Message | How to resolve |
| --- | --- |
| `A datatype is required in Hex; a default was used.` | Add a `datatype` to the field or metric. Until you do, a default type is applied. |
| `Metric expression references field not in semantic model` | Define the referenced column as a field on the dataset, or update the expression to use an existing field. |
| `Temporal role markers are not supported in Hex and were dropped.` | Add a temporal `datatype`, such as `Date` or `DateTime`, to the field that sets `is_time`. |

Re-run the conversion after you update the Ossie file. Converting into the same output folder overwrites existing model files, but doesn't delete files for datasets you've removed. Delete the output folder before converting to avoid syncing stale models.

## Configure Context Sync[​](#configure-context-sync "Direct link to Configure Context Sync")

After reviewing a local conversion, follow the [Context Sync](/docs/agent-management/context-management/context-sync) instructions to create a configuration file. You'll need a semantic project in Hex to sync into: [create a semantic project](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#create-a-semantic-project) with the **Hex** type, or use an existing one. Add an entry to `semanticProjects` with the input (`path`) set to the original Ossie file and the source format to Ossie (`convert.from: ossie`):

hex\_context.config.yaml

```
semanticProjects:



- id: <semantic-project-uuid>



path: ./my-semantic-model.ossie.yaml



convert:



from: ossie
```

The CLI converts the source locally to temporary Hex model files during `hex context preview`, so the configuration can point directly at the source file.

Follow the [semantic project configuration instructions](/docs/agent-management/context-management/context-sync#semantic-projects) to find the project `id`.

## Preview and publish[​](#preview-and-publish "Direct link to Preview and publish")

Follow the [Context Sync CLI instructions](/docs/agent-management/context-management/context-sync#sync-resources-with-the-cli) to authenticate, preview, and publish using the configuration above. Conversion happens during preview.

## Sync automatically in CI[​](#sync-automatically-in-ci "Direct link to Sync automatically in CI")

Follow the [Sync automatically in CI instructions](/docs/agent-management/context-management/context-sync#sync-automatically-in-ci) to set up authentication and your workflow. Use the configuration above with `convert.from: ossie` so Context Sync handles conversion during preview.

### Sync from GitHub[​](#sync-from-github "Direct link to Sync from GitHub")

Follow the [Sync from GitHub instructions](/docs/agent-management/context-management/context-sync#sync-from-github). The action reads the configuration above and handles conversion; no separate conversion step is needed.

### Sync from other CI providers[​](#sync-from-other-ci-providers "Direct link to Sync from other CI providers")

Follow the [Sync from other CI providers instructions](/docs/agent-management/context-management/context-sync#sync-from-other-ci-providers) using the configuration above. The CLI handles conversion during preview.

## Vendor-specific conversion[​](#vendor-specific-conversion "Direct link to Vendor-specific conversion")

Hex also provides support for some vendor-specific conversion paths.

### dbt[​](#dbt "Direct link to dbt")

Use the Hex CLI to convert a dbt semantic manifest to Hex through Ossie. Your project can use either the legacy or latest dbt Semantic Layer YAML specification. The example below uses the [dbt 1.12+ syntax](https://docs.getdbt.com/docs/build/semantic-models).

The examples below assume you run commands from your dbt project root (the directory containing `dbt_project.yml`) and use the default `target/` output directory. If your dbt project is elsewhere, pass `--project-dir <path>` to `dbt parse`. If you use a different output directory, set `--target-path <path>` as needed. Adjust the converter's `--input` path and the Context Sync `path` to match the generated manifest's location; Context Sync paths are relative to `hex_context.config.yaml`.

#### Prepare the dbt project[​](#prepare-the-dbt-project "Direct link to Prepare the dbt project")

Add datatype annotations to your dbt models to preserve the types of the underlying values during conversion.

* In the latest specification (dbt 1.12+ syntax), set `entity.config.meta.ossie.datatype` or `dimension.config.meta.ossie.datatype` inside each column, and `config.meta.ossie.datatype` on each metric.
* In the legacy specification, set `config.meta.ossie.datatype` on each entity, dimension, measure, and metric.

Valid datatype values are `String`, `Integer`, `Decimal`, `Float`, `Boolean`, `Date`, `Time`, `DateTime`, `DateTimeTz`, and `Opaque`, as defined in the [Ossie specification](https://github.com/apache/ossie/blob/main/core-spec/spec.md#data-types).

Your project must also have a [configured time spine](https://docs.getdbt.com/docs/build/metricflow-time-spine). The example below assumes an existing SQL model named `opportunities` that exposes `opportunity_id`, `created_date`, and `arr`.

models/opportunities.yaml

```
version: 2



models:



- name: opportunities



description: Sales opportunities



config:



alias: DIM_OPPORTUNITIES



semantic_model:



enabled: true



agg_time_dimension: created_date



columns:



- name: opportunity_id



description: A uuid for the opportunity



entity:



name: opportunity_id



type: primary



description: A uuid for the opportunity



config:



meta:



ossie:



datatype: String



- name: created_date



description: Date the opportunity was created



dimension:



type: time



config:



meta:



ossie:



datatype: Date



granularity: day



- name: arr



description: Annual recurring revenue attributed to the opportunity



dimension:



type: categorical



config:



meta:



ossie:



datatype: Float



metrics:



- name: opportunity_count



description: Count of unique opportunities



label: Opportunity count



type: simple



config:



meta:



ossie:



datatype: Integer



agg: count_distinct



expr: opportunity_id



- name: opportunity_arr_average



description: The average opportunity ARR



label: Opportunity ARR average



type: simple



config:



meta:



ossie:



datatype: Float



agg: average



expr: arr
```

#### Convert the dbt project[​](#convert-the-dbt-project "Direct link to Convert the dbt project")

The dbt to Ossie converter expects a dbt semantic manifest as the input. Run `dbt parse` to generate the manifest. Then run `hex context semantic-project convert`, declaring the manifest as the input and a local folder as the output:

```
dbt parse



hex context semantic-project convert \



--from dbt \



--to hex \



--input ./target/semantic_manifest.json \



--output ./tmp
```

#### Convert during Context Sync[​](#convert-during-context-sync "Direct link to Convert during Context Sync")

After reviewing a local conversion, configure [Context Sync](/docs/agent-management/context-management/context-sync) to convert the dbt semantic manifest during preview. [Create a Hex semantic project](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#create-a-semantic-project), then add an entry to `semanticProjects` in `hex_context.config.yaml`. Set `path` to the manifest file and `convert.from` to `dbt`:

hex\_context.config.yaml

```
semanticProjects:



- id: <semantic-project-uuid>



path: ./target/semantic_manifest.json



convert:



from: dbt
```

An explicitly configured dbt conversion input can be ignored by Git, so you can point directly at the generated manifest in dbt's `target/` directory. The manifest must still be inside the configuration file's Git repository. For this example, place the context configuration file at your dbt project root.

Context Sync doesn't run `dbt parse`; run it to regenerate the manifest before each preview, including in CI. Follow the [preview and publish instructions](#preview-and-publish) or the [CI setup instructions](#sync-automatically-in-ci) using this configuration.

#### On this page

* [Concepts](#concepts)
* [Prepare the Ossie file for conversion](#prepare-the-ossie-file-for-conversion)
* [Convert and review locally](#convert-and-review-locally)
  + [Review conversion problems](#review-conversion-problems)
* [Configure Context Sync](#configure-context-sync)
* [Preview and publish](#preview-and-publish)
* [Sync automatically in CI](#sync-automatically-in-ci)
  + [Sync from GitHub](#sync-from-github)
  + [Sync from other CI providers](#sync-from-other-ci-providers)
* [Vendor-specific conversion](#vendor-specific-conversion)
  + [dbt](#dbt)