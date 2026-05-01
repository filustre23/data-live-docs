On this page

# Endorsements

Indicate which data assets are trusted in your workspace.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* **Admins**, **Managers**, **Editors**, and **Explorers** can view the Endorsements tab.
* Only **Admins** and **Managers** can edit context asset statuses.

Endorsements indicate which data assets are trusted in your workspace. Endorsed assets are prioritized when agents answer questions and act as a clear visual signal to end users that the data has been reviewed and approved by workspace Admins or Managers.

Endorsements can be applied to multiple asset types, including:

* Schemas and tables in data connections
* Projects in your workspace
* Semantic models

Admins and Managers can manage asset statuses directly on this page. See [Endorsed statuses](/docs/organize-content/statuses-categories#endorsed-statuses) for more details.

## Managing endorsements via API[​](#managing-endorsements-via-api "Direct link to Managing endorsements via API")

In addition to the Context Studio interface, you can programmatically manage endorsements using the [Hex API](/docs/api-integrations/api/overview). This is useful for bulk updates or integrating endorsement management into your existing workflows. The following endpoints are available:

* [`UpdateSemanticProject`](/docs/api-integrations/api/reference#operation/UpdateSemanticProject) — Update status for datasets and views in semantic models
* [`UpdateDataConnectionSchema`](/docs/api-integrations/api/reference#operation/UpdateDataConnectionSchema) — Update status for warehouse databases, schemas, and tables
* [`UpdateProject`](/docs/api-integrations/api/reference#operation/UpdateProject) — Update status for projects

#### On this page

* [Managing endorsements via API](#managing-endorsements-via-api)