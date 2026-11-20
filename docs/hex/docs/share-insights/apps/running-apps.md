On this page

# Running apps

Learn about the different ways to run apps to update results.

info

* Available on all [pricing plans](https://hex.tech/pricing).
* Users will need **Can View** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to run an app.

When viewing an app, there are a number of different ways to run the app to get new results. Some of these options vary depending on how the editor has configured the app's [run settings](/docs/share-insights/apps/app-run-settings).

## Age of results[​](#age-of-results "Direct link to Age of results")

In the top right hand corner of an app, users will see a relative timestamp, indicating the age of the oldest data referenced in the results currently displayed.

Generally, you can think of this as the timestamp of the run that produced the outputs you're viewing. These results may have been updated by a recent publish, a scheduled run, or an automatic or manual refresh of results.

## When do apps refresh?[​](#when-do-apps-refresh "Direct link to When do apps refresh?")

By default, apps in your workspace are set to **auto-refresh**. This means that if you visit an app, if the results are older than the staleness timeout, the results will start refreshing in the background.The [staleness timeout](/docs/share-insights/apps/app-run-settings#auto-refresh-published-results) is set by a user with Can Edit or higher access to the project.

Once the app has refreshed in the background, a **New results available** notification will appear in place of the result age indicator.

Note that this UI won't appear if you have already started interacting with the app, since visiting the new results will undo any changes to inputs you've made.

Apps are also refreshed by:

* A new version of the app being published
* A [scheduled run](/docs/share-insights/scheduled-runs) where update published results is enabled.

## Manually refreshing an app[​](#manually-refreshing-an-app "Direct link to Manually refreshing an app")

If the app has results that are not fresh enough, you can choose to refresh the results manually, by selecting the age of results, and then the **Refresh data**\* button, as pictured [above](#age-of-results).

These refresh runs will ignore any previous outputs, even if they are within the configured staleness timeout, leading to longer run times, but fresher results.

Typically, this refresh action will kick off two runs:

1. A run in front of the user, which ignores any previous results, and respects the current values for any inputs and filters.
2. A run in the background, which ignores any previous results, but uses the default values for inputs and filters. This run refreshes the results for all users of the app.

A user with **Can edit** or higher project permissions may have turned off auto-refresh. A common reason for this is to have have finer-grained control over when the results are updated.

If the app is not set to auto-refresh:

* The refresh UI will look slightly different (see below)
* All users can refresh the results in their current session, which only updates the results for themselves. Similar to above, this refresh run will ignore any previous outputs.
* Users with **Can edit** or higher project permissions can choose to refresh the results for all users.

## Interacting with an app[​](#interacting-with-an-app "Direct link to Interacting with an app")

By default, interacting with the app will cause the app to run. Interactions include changing an input value, and adding a filter to a chart or table.

However it's also worth noting that whenever an app runs Hex may leverage previous outputs to speed up execution, if the age of those outputs are within the [staleness timeout](/docs/share-insights/apps/app-run-settings#auto-refresh-published-results) set by a user with Can Edit or higher access to the project. In these cases you may have just run the app, but the age of results will continue to reflect the oldest data.

An Editor may have turned off the auto-rerun behavior. This is typically done if multiple inputs should be configured before the app is run. If this is the case:

1. An additional **Run** button will appear in the top-right hand corner (below)
2. An Editor may have added a Run input to the app, clicking on this button will also run the whole app. Run inputs appears as one of the UI elements within the dashboard, rather than a separate button in the top right hand corner of the app.

## Troubleshooting & FAQ[​](#troubleshooting--faq "Direct link to Troubleshooting & FAQ")

### Why didn't the age of results change after running the app?[​](#why-didnt-the-age-of-results-change-after-running-the-app "Direct link to Why didn't the age of results change after running the app?")

Runs triggered by interactions with the app, or by clicking the **Run** button will leverage previous results if they are within the staleness policy set by a project editor. This means that even after running the app, the age of results may still be older than "Just now". Consider [refreshing the app](#refreshing-an-app) for newer results.

### Why can't I refresh results for all users?[​](#cant-refresh "Direct link to Why can't I refresh results for all users?")

If an app has [auto-refresh](/docs/share-insights/apps/app-run-settings#auto-refresh-published-results) disabled, only users with **Can edit** or higher project permissions can refresh the results for all users. This setting may have been disabled by an editor so they can have finer-grained control over when results are updated.

If you have **Can view** or **Can explore** access to the app, this option will be disabled.

See [above](#refreshing-an-app-manually) for more details.

### What does it take longer than I expect for results to update?[​](#what-does-it-take-longer-than-i-expect-for-results-to-update "Direct link to What does it take longer than I expect for results to update?")

When you interact with an app (e.g. by changing an input or filter), Hex's DAG-based model means that more cells than are visually shown in the app may have to run to update cells downstream of your interaction. This can result in the run taking longer than expected, especially if these upstream cells are slow to execute.

If you have **Can explore** or higher project permissions, you can use the [Run stats](/docs/explore-data/projects/project-execution/run-stats) feature to see which cells ran, and diagnose performance issues. After completing the run, from the three-dot menu in the top right hand corner, choose **Advanced** > **Enter debug mode**. Then, from the bottom left hand corner, choose the **Help** menu, and then **View run stats**.

### How do I change inputs and filters without affecting other browser tabs?[​](#how-do-i-change-inputs-and-filters-without-affecting-other-browser-tabs "Direct link to How do I change inputs and filters without affecting other browser tabs?")

If you open an app within 30 minutes of the last time you visited the app, Hex will return you to your existing app session.

This means that any inputs you changed will still reflect the changed values, and you'll see the results from your most recent run. If you have the app open in two browser tabs, these tabs will stay in sync.

If you would like to change inputs or filters in one browser tab without affecting other browser tabs where you have opened the app, from the three-dot menu, select **Start a new session**. This will open the app in a new tab, in an isolated session, indicated by the unique app session ID in the URL.

#### On this page

* [Age of results](#age-of-results)
* [When do apps refresh?](#when-do-apps-refresh)
* [Manually refreshing an app](#manually-refreshing-an-app)
* [Interacting with an app](#interacting-with-an-app)
* [Troubleshooting & FAQ](#troubleshooting--faq)
  + [Why didn't the age of results change after running the app?](#why-didnt-the-age-of-results-change-after-running-the-app)
  + [Why can't I refresh results for all users?](#cant-refresh)
  + [What does it take longer than I expect for results to update?](#what-does-it-take-longer-than-i-expect-for-results-to-update)
  + [How do I change inputs and filters without affecting other browser tabs?](#how-do-i-change-inputs-and-filters-without-affecting-other-browser-tabs)