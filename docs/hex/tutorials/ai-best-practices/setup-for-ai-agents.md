On this page

# Setup your workspace for AI agents

The best way to think about enabling Hex agents is similar to the way you'd think about enabling a new analyst - they have all the core fundamentals and know how to write great SQL or Python but they lack business context. The lack of context can lead to incorrect assumptions when facing an abundance of data. Great data curation is the #1 lever you can pull to return higher quality results.

This tutorial outlines steps that help provide Hex agents with a focused view on relevant information, leading to more accurate suggestions.

info

**Hex agents are meant as a way to augment, not replace, human insight and judgement.** You should **not** rely on AI-generated code to be accurate, complete, or free from bias.

## Warehouse Curation[​](#warehouse-curation "Direct link to Warehouse Curation")

### Setup the default data connection[​](#setup-the-default-data-connection "Direct link to Setup the default data connection")

Generally, the majority of users in your Hex workspace only need access to a subset of the data in your warehouse. Access to all of the tables and databases can be confusing for both humans and agents.

The default data connection in your Hex workspace should tailored to only have access to the schemas/databases that the majority of users need to use, thereby giving a focused view of the data.

You can control the data exposed in the default data connection by either:

1. Creating a new role/permissioning structure in your warehouse directly. This will prevent users from querying tables outside of the schema/databases this role has access to.
2. Use Hex's [schema filter](/docs/connect-to-data/data-connections/data-connections-introduction#schema-filtering) feature - this will only pull in schema details based on regex rules you set. This is a lightweight way to curate your data connection without any extra work in the data warehouse.

caution

Schema filtering is not a security feature and users can still query the underlying tables directly if the user has proper permissions to do so.

Once you have your default connection set up, you can set up [scheduled refreshes](/docs/connect-to-data/data-connections/data-connections-introduction#schedule-automated-refreshes-for-the-data-browser) to ensure we're regularly resyncing and making sure agents have access to up-to-date schema information and metadata.

### Endorse data the agent should use[​](#endorse-data-the-agent-should-use "Direct link to Endorse data the agent should use")

Adding an [endorsed
status](/docs/organize-content/statuses-categories#endorsed-statuses) to a
database, schema, table, or semantic model is the easiest and fastest way to
help agents (and end users!) know what data is "Approved" or "Trusted" by data
leaders. Endorsed data will be prioritized for all AI features. Child data objects will
inherit their parent's Endorsed status and also will be prioritized - so it's easy
to endorse an entire database or schema with just one click!

### Exclude data the agent shouldn't use[​](#exclude-data-the-agent-shouldnt-use "Direct link to Exclude data the agent shouldn't use")

If you want to keep certain databases, schemas, or tables visible in the Data browser for people but **not** have them surface in the agent's default discovery and SQL generation, use the **Include/Exclude for AI** setting. Excluded objects are left out of the metadata and search-style context the agent uses to choose what to query, which steers Threads and Notebook agents away from that data in normal use. This is not a hard block: if someone @mentions a table or otherwise points the agent at excluded data, the agent may still use it—so for true access control, rely on warehouse permissions and roles, not this toggle alone.

Child data objects inherit their parent's exclusion state, so if you exclude an entire database, all schemas, tables, and columns under it are excluded from AI context as well.

### Add descriptions to your data[​](#add-descriptions-to-your-data "Direct link to Add descriptions to your data")

Table and column descriptions saved in your warehouse get synced with every schema refresh. Agents can use this context to generate better results. If you use dbt, you can take advantage of our [dbt Cloud integration](/docs/connect-to-data/data-connections/dbt-integration) - once set up, Hex will sync all your descriptions which agents will automatically leverage.

#### What to include in descriptions[​](#what-to-include-in-descriptions "Direct link to What to include in descriptions")

* For a table:
  + Information about what a table should be used for and what things can be calculated with it
* For a column:
  + Add enumerated values for all low cardinality columns
  + For text values, add an example in the description and describe a pattern it might follow:
    - Example: `State: Text column following the pattern: CA , AZ , NV`

tip

Above is an excerpt from our data team's Coalesce talk on documentation best practices - [you can listen in here](https://www.youtube.com/watch?v=eo0C6Drth-Q)!

#### Test the impact of adding descriptions[​](#test-the-impact-of-adding-descriptions "Direct link to Test the impact of adding descriptions")

If you want to prototype descriptions and see how agents use them, you can directly edit the description fields in Hex within the Data browser UI. You can then ask a Hex agent your question and observe the results, updating the descriptions as needed!

If you want a Hex agent to use a specific table, you can @mention the table in the prompt.

## Semantic Models[​](#semantic-models "Direct link to Semantic Models")

A semantic model is "instructions for use" for a given set of tables. How should an agent calculate measures based on the columns? What are valid joins and aggregations? Semantic models encode this up front, so everyone knows how to use the data correctly downstream.

This is an immensely useful concept for "self-serve" analytics, where you want a broader set of users in the organization to leverage data in a consistent, standardized way. Adding semantic models to your workspaces creates a single-source of truth for metric definitions like Revenue and entities like Customers.

Semantic models can be either defined directly in Hex, using Hex's [Semantic Authoring](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview) or synced from our integrations partners, such as dbt, Cube, and Snowflake, with [Semantic Model Sync](/docs/connect-to-data/semantic-models/semantic-model-sync/intro).

Once the semantic models are configured, agents will prefer to use the definitions encoded in the models, rather than querying the warehouse directly.

## Workspace context[​](#workspace-context "Direct link to Workspace context")

The [workspace context file](/tutorials/ai-best-practices/workspace-context-best-practices) allows Admins to provide additional context to Hex's agents through a markdown file. This context is used by all AI agents in Hex when generating responses, helping them better understand your business context, data conventions, and preferred practices.

This feature is similar to Claude Projects or Cursor rules - by providing consistent, high-level context to Hex agents, you can ensure consistency across threads.

Since these rules apply to the entire workspace, only workspace Admins can modify the rules.

tip

[Learn more about workspace context best practices](/tutorials/ai-best-practices/workspace-context-best-practices)

#### On this page

* [Warehouse Curation](#warehouse-curation)
  + [Setup the default data connection](#setup-the-default-data-connection)
  + [Endorse data the agent should use](#endorse-data-the-agent-should-use)
  + [Exclude data the agent shouldn't use](#exclude-data-the-agent-shouldnt-use)
  + [Add descriptions to your data](#add-descriptions-to-your-data)
* [Semantic Models](#semantic-models)
* [Workspace context](#workspace-context)