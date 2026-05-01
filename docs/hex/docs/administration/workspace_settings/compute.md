On this page

# Compute

Manage advanced compute access, spend limits, and usage logs.

info

* Advanced compute is available on Team and Enterprise [plans](https://hex.tech/pricing).
* Only workspace Admins can configure these settings.

## What is advanced compute?[​](#what-is-advanced-compute "Direct link to What is advanced compute?")

Advanced compute refers to larger [compute profile sizes](/docs/explore-data/projects/environment-configuration/environment-views#compute-profile) that offer more memory, CPUs, and/or GPUs to power data science workflows in Hex.

## Compute usage-based billing[​](#compute-usage-based-billing "Direct link to Compute usage-based billing")

Advanced compute is billed per-minute of [kernel runtime](/docs/explore-data/projects/environment-configuration/project-kernels#kernel-status), ensuring you only pay for what you use. Admins can ensure predictable costs by configuring [spend limits](/docs/administration/workspace_settings/compute#set-a-compute-spend-limit) and [access controls](/docs/administration/workspace_settings/compute#restrict-advanced-compute-access-by-user-group).

Customers without a contract will be billed every $100 of compute spend within the monthly billing cycle, and/or at the end of the billing cycle. Customers with a contract will be billed only at the end of their billing cycle.

View [compute pricing here](https://hex.tech/pricing/?modal=compute).

## Advanced compute access[​](#advanced-compute-access "Direct link to Advanced compute access")

### Enable or disable advanced compute[​](#enable-or-disable-advanced-compute "Direct link to Enable or disable advanced compute")

Advanced compute is disabled for your workspace by default, and must be enabled by a workspace Admin in **Settings > Compute**. Note that advanced compute is not available during your free trial.

Once enabled, users with **Full Access** and **Can Edit** project permissions can choose advanced compute profiles for their projects. Compute profiles apply to all notebook, app, scheduled run, and API sessions for the project.

### Restrict advanced compute access by user group[​](#restrict-advanced-compute-access-by-user-group "Direct link to Restrict advanced compute access by user group")

From **Settings > Compute**, Admins can optionally restrict advanced compute profiles to specific [user groups](/docs/administration/workspace_settings/overview#groups). Only the specified user groups will be able to choose advanced compute profiles for their projects. Note that other users can still incur costs by running the project.

### Set a compute spend limit[​](#set-a-compute-spend-limit "Direct link to Set a compute spend limit")

From **Settings > Compute**, Admins can optionally set a compute spend limit per billing cycle. Admins will be notified by email when the workspace reaches 80% and 100% of the limit.

When the limit is reached, new project runs on advanced compute profiles will be disabled, including scheduled runs. To avoid loss of work, active project runs will be allowed to complete (until manually [stopped](/docs/explore-data/projects/environment-configuration/project-kernels#manually-stopping-active-kernels), or until [kernel timeout](/docs/explore-data/projects/environment-configuration/project-kernels#kernel-timeouts)). This means it's possible for your compute spend to slightly exceed the spend limit in a given billing cycle.

After the spend limit is reached, Admins can increase the spend limit to allow additional advanced compute usage in the billing cycle.

## Advanced compute usage logs[​](#advanced-compute-usage-logs "Direct link to Advanced compute usage logs")

Admins can view 90-day advanced compute usage logs from **Settings > Compute > Usage**, including the associated user and project details.

#### On this page

* [What is advanced compute?](#what-is-advanced-compute)
* [Compute usage-based billing](#compute-usage-based-billing)
* [Advanced compute access](#advanced-compute-access)
  + [Enable or disable advanced compute](#enable-or-disable-advanced-compute)
  + [Restrict advanced compute access by user group](#restrict-advanced-compute-access-by-user-group)
  + [Set a compute spend limit](#set-a-compute-spend-limit)
* [Advanced compute usage logs](#advanced-compute-usage-logs)