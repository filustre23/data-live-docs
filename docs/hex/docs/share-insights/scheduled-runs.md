On this page

# Scheduled runs

Set up your Hex apps to automatically run on a schedule. Scheduled runs can also be used to update published results, and trigger [app notifications](/docs/share-insights/app-notifications).

info

* Scheduled runs are available on the Team and Enterprise [plans](https://hex.tech/pricing).
* The Professional plan is limited to one scheduled run per project and does not include Slack notifications or custom schedules.
* Users with **Can edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) can manage all scheduled runs on a project.
* Users with **Can explore** project permissions can create a maximum of one scheduled run per project.

Hex apps can be configured to be run on a schedule that suits your use case, with a maximum frequency of hourly.

When a scheduled run is triggered, the cells [required by the app](/docs/explore-data/projects/project-execution/execution-model) are run, providing a way to automate code execution. Scheduled runs can also be used to [update the published results](#update-published-results), and to trigger [app notifications](/docs/share-insights/app-notifications).

tip

Your app needs to be published before a scheduled run can be setup. Scheduled runs will always run the currently published version, rather than the draft version.

The scheduled runs for a project can be accessed in two different UI locations:

* **Published app:** Via the **Scheduled runs & Notifications** button in the top right-hand corner of the app.
* **Notebook view:** The **Scheduled runs** tab in the left sidebar

This sidebar contains details of the currently configured scheduled runs, your notifications tied to the scheduled run, and a log of past scheduled runs.

## Create a scheduled run[​](#create-a-scheduled-run "Direct link to Create a scheduled run")

To create a scheduled run, visit the Scheduled runs sidebar in either the published app or the notebook, and select **+ Add**. You can schedule apps to run on hourly, daily, weekly or monthly intervals.

Users on the Team and Enterprise plan also have the option of using a cron expression to define a schedule.

If [saved views](/docs/share-insights/apps/saved-views) are available on the app, users have the option to configure which saved views will run as part of the scheduled run. A maximum of three views can be attached to a scheduled run.

Users with **Can edit** permissions can create multiple scheduled runs per project. A maximum of 12 hourly scheduled runs can be added to a project.

Users with **Can explore** permissions can create up to one scheduled run per project, with a maximum frequency of **daily**.

Note: scheduled runs may be delayed up to ten minutes. This is done for reliability at times when many jobs may be scheduled to run simultaneously.

## Cancel a scheduled run[​](#cancel-a-scheduled-run "Direct link to Cancel a scheduled run")

Users with **Can edit** permission can cancel in-progress scheduled runs from the **Run log**, accessible via the **Published app** or the **Notebook view**. Hovering over the run will give you the option to stop the run. Canceled runs will be marked as failed in the **Run log**, and will not update the published results of the app.

## Update published results[​](#update-published-results "Direct link to Update published results")

If your app is set to [show results from a previous run](/docs/share-insights/apps/app-run-settings#when-an-app-user-opens-the-published-app), users with **Can edit** permission can leverage scheduled runs to update the results a user sees when they open the app.

Runs that update the published results are marked in the scheduled runs list with a refresh icon.

By default, scheduled runs created by users with **Can edit** permission will update the published results.

To change whether a scheduled run updates published results, a user with **Can edit** permission should:

1. Select the scheduled run from the sidebar
2. Click the pencil icon to edit the schedule
3. Toggle the **Update published results** setting

In contrast, scheduled runs created by users with **Can explore** permissions will never update the published results. Users with **Can explore** permission cannot change this setting.

## Scheduled runs & SQL caching[​](#scheduled-runs--sql-caching "Direct link to Scheduled runs & SQL caching")

By default, scheduled runs created by users with **Can edit** permission will **not** use [cached SQL results](/docs/explore-data/cells/sql-cells/query-caching), and instead run the queries from scratch, **writing the latest query results to the SQL cache**.

To change whether a scheduled run uses cached SQL results, a user with **Can edit** permission should:

1. Select the scheduled run from the sidebar
2. Click the pencil icon to edit the schedule
3. Toggle the **Use cached SQL results** setting

Scheduled runs created by users with **Can view** permissions will always use cached SQL results to reduce warehouse loads. Users with **Can explore** permission cannot change this setting.

## Send notifications[​](#send-notifications "Direct link to Send notifications")

Scheduled runs can be used as triggers for two types of notifications:

* **Subscriptions**: Deliver a link to an app when a scheduled run completes, or be notified if the scheduled run errors.
* **Conditional notifications**: Get notified after a scheduled run, only if a condition is met.

[Learn more](/docs/share-insights/app-notifications) about configuring app notifications.

## Scheduled runs & input values[​](#scheduled-runs--input-values "Direct link to Scheduled runs & input values")

By default, scheduled runs execute with the default values for inputs. If you need to execute a project with the non-default values for inputs, first create a [saved view](/docs/share-insights/apps/saved-views) and then configure the scheduled run to execute the saved view.

## Detecting scheduled runs in code[​](#detecting-scheduled-runs-in-code "Direct link to Detecting scheduled runs in code")

Hex provides two [built-in variables](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables) that can be used to determine if a run is happening as part of a scheduled run:

* `hex_scheduled` (boolean): returns `True` when the project is being executed as part of a scheduled run.
* `hex_run_context` (enum): returns `'scheduled'` when the project is being executed as part of a scheduled run. Other values are: `'logic', 'app', 'api-triggered'`.

Detecting when code is being executed as part of a scheduled run can be useful when certain operations should happen during scheduled runs **only**. For example, this could be used so that a write to an external service is only triggered on a scheduled run, and not as part of an ad hoc usage of an app.

```
if hex_scheduled:  
    ## expensive query step  
    ## write results out to a file or database  
else:  
    ## read from written file or database  
  
if hex_run_context == "scheduled":  
    ## something that only needs to happen during a scheduled run  
else:  
    ## something else
```

## Accessing past scheduled runs[​](#accessing-past-scheduled-runs "Direct link to Accessing past scheduled runs")

Past scheduled runs (and API-triggered runs) can be accessed for up to **90 days** after they were executed.

To access these runs, head to the App. Click the **Scheduled runs & notifications** button in the top-right corner, then select **Run log**. You can also filter to just scheduled, or API-triggered runs in this interface.

## Files created in scheduled runs[​](#files-created-in-scheduled-runs "Direct link to Files created in scheduled runs")

Files created and written to a project's file directory during scheduled jobs or published app sessions are not persisted between scheduled runs. This means that any files written out by a scheduled job cannot be accessed in the Notebook view, App builder, or in future scheduled runs of the project. For example, a file saved using `to_csv` in a Python cell can only be read back in during the same scheduled run.

If you need to persist files between scheduled runs, we recommend writing the data to an external source, such as your [database](/tutorials/connect-to-data/use-writeback-cells), [S3](/tutorials/connect-to-data/connect-to-s3), or [Google Drive](/tutorials/connect-to-data/connect-to-google-sheets). Then, you can read this data back in during future runs of the project, including scheduled runs and published app runs.

## Manage scheduled runs in a workspace[​](#manage-scheduled-runs-in-a-workspace "Direct link to Manage scheduled runs in a workspace")

Workspace admins can view all scheduled runs in a workspace from the Admin panel. [Learn more about managing scheduled runs](/docs/administration/workspace_settings/workspace-scheduled-runs).

tip

Consider setting up [auto-archive](/docs/organize-content/archive) rules to help manage scheduled runs. Scheduled runs are disabled on archived projects.

#### On this page

* [Create a scheduled run](#create-a-scheduled-run)
* [Cancel a scheduled run](#cancel-a-scheduled-run)
* [Update published results](#update-published-results)
* [Scheduled runs & SQL caching](#scheduled-runs--sql-caching)
* [Send notifications](#send-notifications)
* [Scheduled runs & input values](#scheduled-runs--input-values)
* [Detecting scheduled runs in code](#detecting-scheduled-runs-in-code)
* [Accessing past scheduled runs](#accessing-past-scheduled-runs)
* [Files created in scheduled runs](#files-created-in-scheduled-runs)
* [Manage scheduled runs in a workspace](#manage-scheduled-runs-in-a-workspace)