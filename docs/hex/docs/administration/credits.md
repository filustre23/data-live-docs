On this page

# How Credits Work

AI features in Hex use a credit system.

## Overview[​](#overview "Direct link to Overview")

Hex accelerates data workflows to help teams move faster with trusted insights. Hex's AI features use a credit system.

To ensure everyone can use AI, Hex awards monthly credit grants to [Editors and Explorers](/docs/collaborate/sharing-and-permissions/roles). Admins can optionally purchase pooled add-on credits for additional usage.

info

* While [Hex Agents](/docs/getting-started/ai-overview) are in **Beta**, per-seat credit grants are being rolled out in phases and are not yet enforced for all customers. Per-seat credit grants will go into effect for all customers when Hex Agents move to GA later this year.
* Admins will receive advance notice before per-seat credit grants go into effect for their workspace.
* All customers will be able to track credit usage in Hex, and have the option to purchase pooled [add-on credits](#what-are-add-on-credits) to let users continue past their included per-seat credit grant.

## Credit Consumption[​](#credit-consumption "Direct link to Credit Consumption")

Core AI features in Hex consume credits based on the effort required to complete your request. Many factors influence effort-based credit consumption, including the complexity of the task, the amount of data or other context the agent needs to process, and the inference and other resources required to complete the task.

You can view how many credits a given agent task consumed after the task is complete, by clicking the three-dots menu:

Below are some illustrative examples of agent task credit consumption:

| Example Task | Example Credit Consumption\* |
| --- | --- |
| How many records do we have in `dim_customers`? | 1 credit |
| What does this retention curve look like broken out by pricing plan? | 1 credit |
| What user actions are most strongly correlated with unbounded 30-day usage retention? | 3 credits |
| Use Prophet and the financial data in `fct_arr_monthly` to build a forecast model for the next 12 months of all ARR categories. | 5 credits |

*\* These are illustrative examples based on current usage data, and are subject to change.*

Not all AI features consume credits. For example, Project Title Generation is included unlimited in the price of your plan, and other AI features may be available for free during their Beta period. The list of features that consume credits is subject to change as we evolve our product offering, and currently includes all [Hex agents](/docs/getting-started/ai-overview) (Threads, Notebook, App, Modeling, Slack Integration, and MCP Server)

### What are per-seat credit grants?[​](#what-are-per-seat-credit-grants "Direct link to What are per-seat credit grants?")

To ensure everyone can try and use Hex's AI features, users on paid seats are awarded a monthly credit grant. Per-seat credit grants are assigned to the individual user, reset each billing cycle, and can’t be transferred, shared, or rolled over. Once you've used your monthly credit grant, you can draw additional credits from the [workspace credit pool](#what-is-the-shared-workspace-credit-pool), if available.

Per-seat credit grants are currently enforced for most customers on monthly subscriptions, and will be enforced for all customers later this year. Admins will receive advance notice before per-seat credit grants are enforced for their workspace.

### What are add-on credits?[​](#what-are-add-on-credits "Direct link to What are add-on credits?")

Admins can optionally purchase add-on credits to allow users to consume past their per-seat credit grant. Add-on credits are added to the shared workspace credit pool.

There are a few ways to purchase or earn add-on credits:

* Admins can enable [auto top-ups](#what-are-auto-top-ups) to automatically purchase shared workspace credits as-needed (whenever a user’s seat grant runs out and the workspace credit pool balance is 0).
* Hex may occasionally award bonus credits, which are added to the shared workspace credit pool.

info

Later this year, we plan to offer customers on annual contracts the option to purchase committed add-on credits. Committed credits can be used in addition to, or instead of, auto top-ups.

### What is the shared workspace credit pool?[​](#what-is-the-shared-workspace-credit-pool "Direct link to What is the shared workspace credit pool?")

By default, any user who depletes their per-seat credit grant can draw from the shared workspace credit pool.

info

Later in this year, we plan to offer Admins on [**Team or Enterprise plans**](https://hex.tech/pricing/) the option to restrict which users or groups have permission to draw from the shared workspace pool.

### What are auto top-ups?[​](#what-are-auto-top-ups "Direct link to What are auto top-ups?")

Auto top-ups allow Admins to automatically purchase add-on credits when they are needed.

* Enabling auto top-ups will automatically purchase a credit pack for the workspace pool when a user depletes their per-seat credit grant and the workspace credit pool is empty.
  + Customers paying by credit card will be charged immediately for auto top-ups.
  + Customers with alternate payment methods will be charged at the end of their true-up period.
* Credits purchased via auto top-up rollover for 1 monthly billing cycle.
* Admins can set a monthly limit on auto top-up purchases to help stay within budget.

info

Later this year, we plan to give Admins on [**Team & Enterprise plans**](https://hex.tech/pricing/) an option to restrict which users or groups can draw from the shared workspace credit pool.

### Do credits rollover?[​](#do-credits-rollover "Direct link to Do credits rollover?")

* [Per-seat credit grants](#what-are-per-seat-credit-grants) do not rollover.
* Add-on credits purchased via [auto top-up](#what-are-auto-top-ups) rollover for one month.

#### On this page

* [Overview](#overview)
* [Credit Consumption](#credit-consumption)
  + [What are per-seat credit grants?](#what-are-per-seat-credit-grants)
  + [What are add-on credits?](#what-are-add-on-credits)
  + [What is the shared workspace credit pool?](#what-is-the-shared-workspace-credit-pool)
  + [What are auto top-ups?](#what-are-auto-top-ups)
  + [Do credits rollover?](#do-credits-rollover)