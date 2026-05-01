On this page

# Modeling Workbench

info

* Semantic authoring is in **public beta** and available for [Team and Enterprise plans](https://hex.tech/pricing/).
* You need the **Admin** or **Manager** workspace role to create and edit semantic projects.

Semantic authoring lets you create and manage semantic resources directly in Hex — no third-party tool required. Semantic projects define a set of data models containing measures, dimensions, and relationships to provide a consistent, governed source of truth for self-serve analytics and AI across your workspace.

## Create a semantic project[​](#create-a-semantic-project "Direct link to Create a semantic project")

1. Navigate to **Settings > Data Sources > Semantic projects**.

2. Click **+ Semantic project**.
3. Enter a name, description, and select a data connection.

## Use the Modeling Workbench[​](#use-the-modeling-workbench "Direct link to Use the Modeling Workbench")

The Modeling Workbench is where you define all the data models and views in your semantic project, as well as their relationships. You can create data models based on existing tables and their columns, use inline validation and autocomplete to help build your YAML file, and use the publish preview to review changes and understand their impact before deploying.

### Create a model[​](#create-a-model "Direct link to Create a model")

1. In the Modeling Workbench, click **Create a model**.
2. Add a **Name** and **Description**.
3. Choose a table or query as the data source.
   * Use **Choose table** or the **Data Browser** on the left sidebar to explore your warehouse.
   * The default data source is a table, but you can also use a SQL query if you need to do any final filtering or transformation.

By default, Hex imports all columns from the underlying table as dimensions and imports column descriptions.

Each model is defined as a YAML configuration file, with fields specifying:

* Source table
* Dimensions
* Measures
* Relationships

When editing the YAML, the Modeling Workbench provides autocomplete suggestions for fields to help you write models and views faster and with fewer errors. Inline validation flags issues — such as missing definitions or incorrect formatting — so you can fix them before publishing.

See [YAML specification](/docs/connect-to-data/semantic-models/semantic-authoring/modeling-specification) for a detailed developer reference guide.

### Semantic Views[​](#semantic-views "Direct link to Semantic Views")

Semantic views provide curated entry points into your semantic project, making complex data models more accessible. While models define all of your measures, dimensions, and relationships, semantic views let you select and organize a subset of those fields into a focused, user-friendly interface.

Views are optional, but helpful when you want to:

* Expose only the fields relevant for a particular analysis or audience
* Provide clearer names or descriptions without altering the underlying model
* Control how users navigate relationships across entities
* Create focused, purpose-built interfaces for different business domains

Views are presentational only - they don’t affect underlying query logic, but they shape how users browse and work with the modeled data. For example, a “Sales Performance” view might expose only certain revenue metrics and customer dimensions from a broader eCommerce model. This keeps the experience streamlined for sales teams and ensures users interact with the modeled data according to the definitions established by the data team.

Once published, semantic views appear in the Data Explorer and anywhere semantic projects are used across your workspace. See [View specification](/docs/connect-to-data/semantic-models/semantic-authoring/modeling-specification#view-specification) for more details.

### Modeling Agent[​](#modeling-agent "Direct link to Modeling Agent")

info

* Modeling agent is available in **Beta** on the [Team and Enterprise plans](https://hex.tech/pricing/), which include monthly per-seat [credit grants](/docs/administration/credits) that can be used towards Hex AI features. While Hex agents are in Beta, credit limits and optional add-on credits are being rolled out in phases and are not yet enforced for all customers. Admins will receive advance notice before limits go into effect for their workspace.

The modeling agent helps you write and edit semantic resources using natural language. Instead of manually writing YAML, you can describe the model you want and let the agent generate or update it.

The agent can generate new models and views from scratch or edit existing resources with incremental changes. You can accept or undo these changes at any time.

Specific tables or Hex projects can be referenced directly with **@ mentions**.

The modeling agent can greatly speed up model creation and iteration. Always review the generated YAML to confirm that measures, dimensions, and relationships match your intended logic before publishing.

### Publish a semantic project[​](#publish-a-semantic-project "Direct link to Publish a semantic project")

When ready, click **Publish** to open the publish preview modal. The modal has three tabs:

1. **Changes** - Shows updates since your last publish, alongside validation checks for errors or missing definitions.
2. **References** - shows where the model is used in your workspace.
3. **Explore** - lets you test the model and any changes in an Explore cell before publishing.
4. **Threads** - lets you test the model and any changes in a Thread before publishing.

### History[​](#history "Direct link to History")

The History page records a complete version timeline of your semantic project, including drafts, published versions, and agent-generated checkpoints.

You can:

* View and compare previously published versions.
* Compare your draft to a past version or agent checkpoint.
* Copy and paste definitions from any historical version back into your draft.

History provides version control directly in Hex, making it easy to experiment and iterate on natively authored semantic projects.

## Sync from GitHub (Optional)[​](#sync-from-github-optional "Direct link to Sync from GitHub (Optional)")

You can keep a semantic project in Hex synchronized with YAML files stored in GitHub for version control. The sync runs in a single direction - from GitHub into Hex.

To set up the sync from GitHub:

1. Go to **Settings > Data sources > Semantic projects**.
2. Open the **three-dot menu** next to your project.
3. Select **View import instructions** to generate the steps and configuration you need.

## Next steps[​](#next-steps "Direct link to Next steps")

Continue to [Using semantic projects](/docs/connect-to-data/semantic-models/viewing-and-using-semantic-models).

#### On this page

* [Create a semantic project](#create-a-semantic-project)
* [Use the Modeling Workbench](#use-the-modeling-workbench)
  + [Create a model](#create-a-model)
  + [Semantic Views](#semantic-views)
  + [Modeling Agent](#modeling-agent)
  + [Publish a semantic project](#publish-a-semantic-project)
  + [History](#history)
* [Sync from GitHub (Optional)](#sync-from-github-optional)
* [Next steps](#next-steps)