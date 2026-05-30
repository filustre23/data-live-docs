On this page

# How Credits Work

AI features in Hex use a credit system.

## Overview[​](#overview "Direct link to Overview")

Hex accelerates data workflows to help teams move faster with trusted insights. Hex's AI features use a credit system.

To ensure everyone can use AI, Hex awards monthly credit grants to Editor and Explorer seats. Admins can optionally purchase pooled add-on credits for additional usage.

info

* Credits will go into effect for legacy customers with advance notice to Admins.
* Customers with annual contracts who wish to purchase add-on credits can contact [[email protected]](/cdn-cgi/l/email-protection#1f6c7e737a6c5f777a67316b7a7c77) to update their contract.

## Credit Consumption[​](#credit-consumption "Direct link to Credit Consumption")

Core AI features in Hex consume credits based on the effort required to complete your request. Many factors influence effort-based credit consumption, including the complexity of the task, the amount of data or other context the agent needs to process, and the inference and other resources required to complete the task.

You can view how many credits a given agent task consumed after the task is complete, by clicking the three-dots menu:

Below are some illustrative examples:

| Example Prompt | Example Credit Consumption\* |
| --- | --- |
| How many customers do we have? | ~1 credit |
| Build me a subscription retention line chart broken out by pricing plan | ~2 credits |
| What user actions correlate most strongly with 30-day retention? | ~3 credits |
| Build me a 12-month ARR forecast. | ~5 credits |
| Build a data app that visualizes sales by product category, and lets users generate sales forecasts by customizing timeframe and subcategory inputs. | ~10 credits |

*\* Actual credit consumption will vary based on your particular data, context, and prompt history.*

Not all AI features consume credits. For example, title generation is included in paid plans and Context Studio topic generation is included in Team+ plans. Other AI features may be exempt from credit consumption temporarily during their Preview or Beta period. The list of features that consume credits is subject to change as we evolve our product offering, and currently includes all [Hex agents](/docs/getting-started/ai-overview), including agent runs triggered from external integrations such as Slack, MCP, or CLI.

### What are monthly credit grants?[​](#what-are-monthly-credit-grants "Direct link to What are monthly credit grants?")

To ensure everyone can try and use Hex’s AI features, users on paid seats are awarded a monthly credit grant. Monthly per-seat credit grants are assigned to the individual user, reset each billing cycle, and can’t be transferred, shared, or rolled over.

You can view the current balance of your monthly credit grant by clicking into the workspace dropdown, located in top left corner your Hex workspace's homepage.

Credit grants vary by plan and seat type:

| Plan | Seat Type | Credit Grant |
| --- | --- | --- |
| Professional | Editor | 30 credits/mo |
| Team | Editor | 40 credits/mo |
| Enterprise | Editor | 60 credits/mo |
| Enterprise | Explorer | 10 credits/mo |

Once you’ve used your monthly credit grant, you can draw additional credits from the [workspace credit pool](#what-is-the-shared-workspace-credit-pool), if available.

info

* Monthly per-seat credit grants are currently enforced for most customers. Legacy customers will receive advance notice before enforcement.
* Monthly per-seat credit grants apply to standard seat-based subscriptions, and do not necessarily apply to custom Enterprise contract structures.

Admins can manage credits and view usage in **Settings > Billing & Credits**.

### What are add-on credits?[​](#what-are-add-on-credits "Direct link to What are add-on credits?")

Admins can opt to purchase pooled add-on credits for additional usage. There are a few ways to purchase or earn add-on credits:

* Admins can enable [auto top-ups](#what-are-auto-top-ups) to automatically refill their workspace credit pool when needed.
* Customers with annual contracts can purchase committed add-on credits upfront at contract start or renewal.
* Hex may occasionally award bonus add-on credits.

Add-on credits go to the shared workspace credit pool, which Admins can view in **Settings > Billing & credits**.

### What is the shared workspace credit pool?[​](#what-is-the-shared-workspace-credit-pool "Direct link to What is the shared workspace credit pool?")

The shared workspace credit pool is your balance of add-on credits. By default, any user who depletes their monthly per-seat credit grant can draw from the shared workspace credit pool.

### What are auto top-ups?[​](#what-are-auto-top-ups "Direct link to What are auto top-ups?")

You can think of auto top-ups as "pay-as-you-go" credits. When auto top-ups are enabled, your workspace credit pool will automatically refill when needed.

#### Auto top-up mechanics[​](#auto-top-up-mechanics "Direct link to Auto top-up mechanics")

* Enabling auto top-ups will automatically purchase a 50-credit pack ($25) for the workspace pool when the balance falls below 25 credits.
  + Customers paying by credit card will be charged immediately for auto top-ups.
  + Customers with alternate payment methods will be charged at the end of their true-up period.
* Credits purchased via auto top-up rollover to the next monthly billing cycle.

#### Auto top-up spend limits[​](#auto-top-up-spend-limits "Direct link to Auto top-up spend limits")

Admins can set a monthly limit on auto top-up purchases to help stay within budget.

* From **Settings > Billing & credits > Credits**, click "Enable auto top-ups" (or "Edit" if auto top-ups are already enabled).
* Set a custom spend limit, or choose from a preset option.
* Click "Save".

Auto top-up spend limits are anchored to your monthly billing cycle and will go into effect immediately once saved.

info

Legacy customers can safely enable auto top-ups before credits go into effect for their workspace. Auto top-ups will begin once credits go into effect.

### Do credits roll over?[​](#do-credits-roll-over "Direct link to Do credits roll over?")

* [Per-seat credit grants](#what-are-per-seat-credit-grants) do not rollover.
* Add-on credits purchased via [auto top-up](#what-are-auto-top-ups) rollover to the next monthly billing cycle.
* Committed add-on credits purchased for annual contracts expire at the end of the contract cycle.

#### On this page

* [Overview](#overview)
* [Credit Consumption](#credit-consumption)
  + [What are monthly credit grants?](#what-are-monthly-credit-grants)
  + [What are add-on credits?](#what-are-add-on-credits)
  + [What is the shared workspace credit pool?](#what-is-the-shared-workspace-credit-pool)
  + [What are auto top-ups?](#what-are-auto-top-ups)
  + [Do credits roll over?](#do-credits-roll-over)