On this page

# Introduction to Semantic Model Sync

info

* Semantic Model Sync is in **beta**.
* Semantic Model Sync is available on the Team and Enterprise [plans](https://hex.tech/pricing).

Semantic projects make self-service analytics easier by allowing data teams to encode business logic into reusable, drag-and-drop elements.

In Hex, semantic projects are:

* **Open:** They are imported from common external specs that can be free and used for many purposes besides just Hex.
* **Flexible:** They are designed to integrate seamlessly into notebooks and can serve as jumping-off points for deeper, frictionless, exploratory work. Hex semantic projects can be used alongside exploratory data analysis across notebooks and apps, enabling consistent measures without limiting exploration or experimentation.

Currently, Hex can import models via Semantic Model Sync from the following semantic specs:

* [dbt MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow)
* [Cube](https://cube.dev/docs/product/introduction)
* [Snowflake Semantic Views](https://docs.snowflake.com/en/user-guide/views-semantic/overview)

## Concepts[​](#concepts "Direct link to Concepts")

Semantic projects are a collection of logical tables, columns, aggregations, and join relationships that can be shared to make self-serve analytics easier and more consistent. In Hex’s semantic projects, the key semantic objects are models, measures, dimensions, and joins.

### Definitions[​](#definitions "Direct link to Definitions")

| Term | Definition |
| --- | --- |
| **Semantic Project** | A grouping of models, connected to a single data connection. A connection can have multiple semantic projects across different semantic specs. |
| **Model** | A logical table of data that often maps directly to a table in the data warehouse, but can be the result of a SQL query too (like a database view). Models contain measures and dimensions. |
| **Measure** | A pre-defined aggregation (sum, count, max, min, avg, count distinct, median) or expression of multiple aggregations. Example: a “Conversion rate” could be `SUM(CASE WHEN converted = TRUE THEN 1 ELSE 0 END) / COUNT(*)`. |
| **Dimension** | The logical columns you want to group ("slice and dice") and filter by. These can point to singular warehouse columns or can be arbitrary (non-aggregating) expressions. |
| **Join** | Also called “join relationships,” a join describes the relationship between two models, most commonly linked together using a shared common field. Note that users cannot define joins between models that belong to different projects. |

Hex imports Cube and MetricFlow semantic model files stored in GitHub, while Snowflake Semantic Views are stored in Snowflake. Hex translates the models into semantic objects (models, dimensions, measures, and joins) that represent data structures. These components can be selected from the [Data browser](/docs/explore-data/data-browser#semantic-models-in-the-data-browser), where users can access these objects through [Explore](/docs/share-insights/explore#exploring-with-semantic-models) to easily build queries by dragging and dropping the available dimensions, measures, and joins.

## Setting up Semantic Model Sync[​](#setting-up-semantic-model-sync "Direct link to Setting up Semantic Model Sync")

info

* Users will need the **Admin** workspace role in Hex to import semantic models
* For Cube and MetricFlow based semantic models, users will need **Admin** role for the repository in GitHub containing the semantic model code

tip

* Cube and MetricFlow workflows use GitHub and it is possible to enable Semantic Model Sync with any Git host (i.e. BitBucket, GitLab) as long as the workflow is able to send a `.zip` file to Hex's [IngestSemanticModel API endpoint](/docs/api-integrations/api/reference).
* The setup uses [GitHub actions](https://docs.github.com/en/actions). The equivalent functionality for Bitbucket and GitLab is [Bitbucket Pipelines](https://www.atlassian.com/software/bitbucket/features/pipelines) and [GitLab CI/CD](https://docs.gitlab.com/ci/).

Creating a semantic project establishes a layer where logic is defined and reused throughout Hex. Users can point to existing semantic projects that contain definitions for models, dimensions, measures, and joins. Through Hex Semantic Model Sync, Hex imports the semantic concepts and enables users to explore using these predefined concepts.

### Preparing for import[​](#preparing-for-import "Direct link to Preparing for import")

#### dbt MetricFlow[​](#dbt-metricflow "Direct link to dbt MetricFlow")

If you are using dbt MetricFlow, you will need to add some metadata to your YAML files before importing them into Hex. Read more [here](/docs/connect-to-data/semantic-models/semantic-model-sync/dbt-metricflow), along with Hex’s support coverage of MetricFlow features.

#### Cube[​](#cube "Direct link to Cube")

You can read about Hex’s support coverage of Cube features [here](/docs/connect-to-data/semantic-models/semantic-model-sync/cube).

#### Snowflake Semantic Views[​](#snowflake-semantic-views "Direct link to Snowflake Semantic Views")

You can read about Hex's support coverage of Snowflake Semantic Views [here](/docs/connect-to-data/semantic-models/semantic-model-sync/snowflake-semantic-views).

## Configuring a semantic project for import[​](#configuring-a-semantic-project-for-import "Direct link to Configuring a semantic project for import")

### Snowflake Semantic Views[​](#snowflake-semantic-views-1 "Direct link to Snowflake Semantic Views")

1. **Navigate to configuration settings in Hex**

* Go to **Settings** > **Data sources** > **Semantic projects**

2. **Select Model Type: Snowflake**

* Add a human-readable **Name** and **Description**
* Select your semantic project **Data connection** and **Semantic View**

3. **Sync your Semantic View**

* Allow a moment for the Semantic Views to sync, once complete, click **Finish**.

### Cube and MetricFlow[​](#cube-and-metricflow "Direct link to Cube and MetricFlow")

info

Before getting started, please make sure the following requirements are met:

* In **GitHub**, your semantic files are stored in a repository.
* In **GitHub**, you are an Admin of the repository. If you do not have Admin access, you will need to ask an Admin to add a GitHub secret before you can complete the setup process
* In **Hex**, you have an **Admin** role.

1. **Navigate to configuration settings in Hex**

* Go to **Settings** > **Data sources** > **Semantic projects**

2. **Configure your semantic project and generate API token**

* Click **Import**
* Add a human-readable **Name** and **Description**
* Select your semantic project **Type** and **Data connection**

* Provide a **Description** for your API token
* Set the **Expiration** for your API token
* **Submit** to generate API token

info

For non-GitHub Git hosts, refer to the generated GitHub Actions YAML file as a guide for setting up in your Git host.

4. **Add the API token as a secret in GitHub**

* Open your GitHub repository, then go to **Settings** > **Secrets and Variables** > **Actions** > **Repository Secrets**
* Select **New repository secret**
* Copy the token name from Hex and paste it into GitHub as the secret **Name**
* **Copy token** from Hex and paste in the **Secret** field

5. **Configure GitHub Action**

* Create a new branch in your repository
* Create a new file `.github/workflows/hex-semantic-layer-sync.yml`
* **Copy workflow file** from Hex and paste into the created file
* Open a new pull request against your `main` branch
* Merge your branch

Check the **Actions** tab of the repository after pushing to the main branch to see if there were any errors or skipped objects.

If there are no errors, check the **Semantic projects** section of **Data sources** settings in Hex to see when the last import job completed.

Click into the value in the "Latest update" column to view the import status and skipped output from the most recent import.

## Testing and importing the semantic model[​](#testing-and-importing-the-semantic-model "Direct link to Testing and importing the semantic model")

The provided GitHub Action workflow is configured to trigger differently based on the merge target:

* **Merge to dev branch:** test the contents of the branch against the importer without saving the objects to your Hex workspace
* **Merge to main branch:** run the import, materialize any found objects to your Hex workspace.

View the import results in the Actions tab in the GitHub repository. Click into your workflow run and navigate to the “Ingest Semantic Model" section.

[](/assets/medias/sm-github-actions-2d2c0dba40305ae67b2dd6d7b1dd2353.mp4)

**Running the GitHub action when semantic model files change**

Update the GitHub action to only run when specific files within a directory change. This is recommended if the semantic model files are in a larger repository that contain other unrelated files. See GitHub action [documentation](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#example-including-paths).

**Re-running an import from the GitHub Actions UI**

In order to trigger an import, go to GitHub → Actions → Rerun all jobs. An import cannot be triggered from Hex, since the model is pushed from GitHub to Hex. This flow keeps Hex in sync with the latest semantic project versions managed in GitHub.

### Git based workflow[​](#git-based-workflow "Direct link to Git based workflow")

It is possible to use any Git host (. BitBucket, GitLab) as long as the workflow is able to send a `.zip` file to Hex's [IngestSemanticModel API endpoint](/docs/api-integrations/api/reference).

An equivalent to GitHub Actions is BitBucket Pipelines and GitLab CI/CD. In order to set up a workflow similar to GitHub Actions, please refer to the GitHub Actions YAML file (the workflow file generated in Step #2 in [Configuring a semantic project for import](#configuring-a-semantic-project-for-import)) as a guide.

## Next steps[​](#next-steps "Direct link to Next steps")

Continue to [Using semantic projects](/docs/connect-to-data/semantic-models/viewing-and-using-semantic-models).

#### On this page

* [Concepts](#concepts)
  + [Definitions](#definitions)
* [Setting up Semantic Model Sync](#setting-up-semantic-model-sync)
  + [Preparing for import](#preparing-for-import)
* [Configuring a semantic project for import](#configuring-a-semantic-project-for-import)
  + [Snowflake Semantic Views](#snowflake-semantic-views-1)
  + [Cube and MetricFlow](#cube-and-metricflow)
* [Testing and importing the semantic model](#testing-and-importing-the-semantic-model)
  + [Git based workflow](#git-based-workflow)
* [Next steps](#next-steps)