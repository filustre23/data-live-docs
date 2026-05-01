On this page

# App run settings

Configure how the results in your app are updated, to balance run speed and data freshness.

info

* Available on all [pricing plans](https://hex.tech/pricing).
* Users will need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to configure app run settings.

There are a number of options available to you to determine how your app is run, and how the published results in your app are updated.

**Published results** refers to the results that an app user sees when first landing on the app. These results are always updated by:

* A new version of the app being published
* A [scheduled run](/docs/share-insights/scheduled-runs) where update published results is enabled.

You can adjust the app run settings from the **App settings** menu in the [app builder](/docs/share-insights/apps/app-builder), or when [publishing](/docs/share-insights/apps/publish-and-share-apps)

## Auto-refresh published results[​](#auto-refresh-published-results "Direct link to Auto-refresh published results")

`Default: Enabled`

When enabled, upon opening a published app, if the published results in the app are older than the allowed timeout, the app will start to refresh in the background. This background run will ignore any cached SQL results, to ensure the results are as fresh as possible, and then update the published results for all users.

Additionally:

* App users will see the below UI
* **Any** viewer of an app can choose to **Refresh** the results, which will update the results for all users.
* Non-refresh runs will leverage cached SQL results, according to the staleness timeout configured as part of this setting. [Learn more about query caching](/docs/explore-data/cells/sql-cells/query-caching).

Enabling this option is a great choice for apps where you expect results to always be up-to-date, for example, a company-wide dashboard.

When this setting is disabled:

* App users will see the below UI to refresh the results, and only users with Can Edit or higher project permissions can refresh the published results for all users.
* The run settings will show a separate setting for "Leverage cached SQL results"

Disabling this option is a good idea for any apps where you, as an editor, want finer grained control over when the app updates. Use cases include an analysis that is related to a specific point in time, or apps that should only be updated on a schedule.

As part of this setting, you must configure a staleness timeout. This timeout controls both when the published results are marked as stale (triggering a refresh), and when the results of a previous execution of a SQL query are considered stale.

By default, the staleness timeout is based on the workspace default set by an Admin. Editors can update this to a custom time period for their app. If a [scheduled run](/docs/share-insights/scheduled-runs) is configured, you can also use the timestamp of the previous scheduled run as the staleness cutoff, as shown above.

If your app uses [signed embedding](/docs/share-insights/embedding/signed-embedding), this option will not be available.

## Advanced settings[​](#advanced-settings "Direct link to Advanced settings")

There are a number of advanced settings available by selecting "Advanced".

### Run from scratch on load[​](#run-from-scratch-on-load "Direct link to Run from scratch on load")

`Default: Disabled`

When enabled, every time a user opens the app, the app will run to show fresh results.

Enabling this option will lead to slower load times as the app has to run before showing users results. However, you can [leverage cached SQL results](/docs/explore-data/cells/sql-cells/query-caching) to help improve run times.

This option is useful when your app is personalized using the `hex_user_email` [variable](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables), and published results cannot be shared between users. Similarly, for embedded apps, this option is always enabled.

Note that when enabled, you cannot use the [auto-refresh published results](#auto-refresh-published-results) feature, since there is no concept of previously populated published results for the app user to land on.

If your app uses [signed embedding](/docs/share-insights/embedding/signed-embedding), this option will be enabled, and uneditable. This is to ensure all users see distinct outputs, and no data is shared between them.

### Leverage cached SQL results[​](#leverage-cached-sql-results "Direct link to Leverage cached SQL results")

`Default: Enabled`

By default, this option does not appear in the run settings menu, as it is enabled via [Auto-refresh published results](#auto-refresh-published-results). If Auto-refresh published results is disabled, it will appear as a separate option.

When enabled, any queries that are executed against the data warehouse may leverage cached SQL results, so long as those results are within the staleness timeout. This helps speed up app runs, while also ensuring users are seeing fresh-enough results. Users can also choose to manually run the app without cached results to see the freshest-possible results.

By default, the staleness timeout is based on the workspace default set by an admin. Editors can update this to a custom time period for their app. If a [scheduled run](/docs/share-insights/scheduled-runs) is configured, you can also use the timestamp of the previous scheduled run as the staleness cutoff.

When disabled, any warehouse queries will *always* go back to the data warehouse, resulting in longer run times.

### Auto-rerun cells[​](#auto-rerun-cells "Direct link to Auto-rerun cells")

`Default: Enabled`

When enabled, when an app user interacts with a published app (for example, changes an [input parameter](/docs/explore-data/cells/input-cells/dropdown-inputs), or updates a [filter](/docs/share-insights/apps/project-filters)), cells that are downstream will automatically start running.

When disabled, a manual "Run" button will be added to the published app. When an app user interacts with the published app, cells will not be run until the **Run** button is pressed. Then, the entire project will be run.

This is useful when multiple inputs should be configured before running the app cells.

## Restoring previous results[​](#restoring-previous-results "Direct link to Restoring previous results")

By default, [Auto-refresh published results](#auto-refresh-published-results) is enabled. This can lead to cases where the results are updated unintentionally, potentially invalidating previous results.

In this case, a user with **Can edit** permissions can restore a previous run as the published results. To do this, head to the published app, select the **Scheduled runs & notifications** icon, then choose the **Run log**. From the three-dot menu, select **Restore run as published results**. You can only restore a run that is associated with the currently published version.

This will restore the run as the published results, and also disable [Auto-refresh published results](#auto-refresh-published-results) so that the results do not get updated automatically in the future.

#### On this page

* [Auto-refresh published results](#auto-refresh-published-results)
* [Advanced settings](#advanced-settings)
  + [Run from scratch on load](#run-from-scratch-on-load)
  + [Leverage cached SQL results](#leverage-cached-sql-results)
  + [Auto-rerun cells](#auto-rerun-cells)
* [Restoring previous results](#restoring-previous-results)