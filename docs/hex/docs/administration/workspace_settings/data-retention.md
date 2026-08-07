On this page

# Data retention

Enable custom data retention policies within Hex.

info

* Available on select Enterprise [plans](https://hex.tech/pricing). Contact [[email protected]](/cdn-cgi/l/email-protection#addeccc1c8deedc5c8d583d9c8cec5) to request access.

Data retention allows Hex Admins to enable custom data retention policies of 7, 14, 30, 60, or 90 days for both cell outputs and cached warehouse data. When these data retention policies for cell outputs and cached warehouse data are enabled, data that is older than the retention policy will be permanently deleted.

note

The custom retention policy will not impact backups, which will be retained for 30 days when data retention policies are enabled regardless of the cell output and cached warehouse data timeframe.

Admins can enable and disable data retention in the **Data retention** section of settings under **Access & Security**.

warning

When a given data retention policy is enabled, all relevant data will be permanently deleted from Hex after 30 days and Hex has no liability for any deleted data thereafter.

## Cached warehouse data[​](#cached-warehouse-data "Direct link to Cached warehouse data")

Hex writes the results of all [warehouse SQL queries to the cache](/docs/explore-data/cells/sql-cells/query-caching) to optimize query runtimes and app performance. By default, cached warehouse data that has not been read in the past 30 days is deleted. When data retention for cached warehouse data is enabled, all cache results are deleted after the specified timeframe regardless of when they were last accessed. If caching is enabled on a project but the cache entry has been deleted, queries will be executed directly in your warehouse.

## Cell outputs[​](#cell-outputs "Direct link to Cell outputs")

Without data retention enabled, cell outputs are stored indefinitely. When enabled, cell outputs are automatically deleted after the specified timeframe from their creation date.

### Notebook[​](#notebook "Direct link to Notebook")

When a user opens a Notebook after cell outputs have been deleted, no output will be displayed, as displayed in the screenshot below. In order to display outputs again, the Notebook will have to be rerun.

### Published apps[​](#published-apps "Direct link to Published apps")

When a user opens an app after cell outputs have been deleted, no cell outputs will be displayed and the user will see a banner at the top of the page indicating this. In order to display output again, the app will have to be manually rerun. To update the default state of the app with new cell outputs, the app will need to be republished, updated via [scheduled run](/docs/share-insights/scheduled-runs) or [API-triggered run](/docs/api-integrations/api/overview), or run with the [Run and update published results](/docs/share-insights/apps/app-run-settings#show-results-from-a-publish-or-scheduled-run-default-update-published-results) option via the app's three-dot menu by a user with "Can edit" or "Full access" to the project.

#### On this page

* [Cached warehouse data](#cached-warehouse-data)
* [Cell outputs](#cell-outputs)
  + [Notebook](#notebook)
  + [Published apps](#published-apps)