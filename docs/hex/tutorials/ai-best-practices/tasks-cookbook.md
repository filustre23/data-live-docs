On this page

# Tasks cookbook

A practical guide to building automated, recurring analyses with Tasks — including prompt templates and worked examples for the most common use cases.

This is a practical guide to building automated, recurring analyses with [Tasks](/docs/explore-data/tasks). Tasks let you schedule the Hex Agent to answer a question automatically, on whatever cadence makes sense, and deliver the results to [Slack or email](/docs/explore-data/tasks#notifications).

Every data team has a list of questions they answer on repeat. You describe what you want once, set a schedule, and the results land in your inbox or Slack.

## General best practices[​](#general-best-practices "Direct link to General best practices")

**Run it as a Thread before you schedule it**

The best way to build a reliable task is to get the prompt right before you commit to a recurring run. Run the analysis as a [Thread](/docs/explore-data/threads), look at what comes back, and adjust until the output is actually useful. It's much easier to iterate in a Thread than to fix a week's worth of bad deliveries after the fact.

**Create the task from the Thread**

You can create a Task directly from any [Thread](/docs/explore-data/threads). The agent carries over the context from your conversation, and you pick the [cadence and delivery destination](/docs/explore-data/tasks#configuring-a-task) from there. The prompt stays editable after you schedule it, so if something changes, you can change it before the next run.

**Start with one**

More tasks isn't always better. A task that delivers something useful every week is more valuable than five that generate noise no one reads. Start with the one recurring analysis that takes the most time to produce manually, get that running well, and go from there.

## Use case: Dashboard digests[​](#use-case-dashboard-digests "Direct link to Use case: Dashboard digests")

Most dashboards require someone to interpret them before they're useful. You open it, read the numbers, figure out what's up or down, and decide what's worth surfacing to the team. That's usually 15 minutes of work that happens before a business review, Monday standup, or ahead of the close of the month. Tasks can do that read-through for you.

If your team has a dashboard someone checks every week before they know what to say in a meeting, that's a good candidate.

### Prompt template[​](#prompt-template "Direct link to Prompt template")

```
I want you to summarize [dashboard/project name] and surface what's most important.



What changed most significantly compared to [last week / last month / same period last year],



and what should I pay attention to going into [next week / next quarter]?



Focus on [specific metrics or sections]. Flag anything that moved more than [X]%



from the prior period. Don't describe metrics that are tracking as expected. Only surface



things that warrant attention or action.
```

### Worked examples[​](#worked-examples "Direct link to Worked examples")

**Weekly GTM digest**

> I want you to summarize last week's GTM performance from our @GTMDashboard using our revenue and pipeline data. What changed most significantly compared to the prior week, and what should leadership pay attention to going into this week?
>
> Focus on new ARR, pipeline created, pipeline velocity, and win rate by segment. Flag any metric that moved more than 15% from the prior week. Only surface things that warrant attention — skip metrics that are tracking as expected. Run every Monday at 7am.

**Monthly product engagement digest**

> I want you to summarize how our top product features performed from our @FeaturePerformanceApp last month. Which features saw the biggest changes in adoption compared to the prior month, and are any showing early signs of drop-off?
>
> Look at daily active usage in @DAUMetrics, feature retention at day seven and day 30, and new-user adoption. Highlight any features launched in the last 30 days. Exclude internal users.

**Executive board prep**

> I want you to prepare a summary of this quarter's business performance from @CompanyMetricsDashboard for a board-level audience. What are the three to five most important things that happened this quarter, and how do they compare to our plan?
>
> Pull from our finance and GTM data in their respective tabs on the @CompanyMetricsDashboard. Focus on revenue, new logos, NRR, and headcount efficiency. Flag anything that came in more than 10% above or below target. Frame each point as a signal, not just a number.

### Getting good results[​](#getting-good-results "Direct link to Getting good results")

Tell the agent you want the narrative first, with supporting numbers behind it. "Summarize findings in three to five bullets. Each bullet should lead with the insight, then support it with the number" gets you something you can actually share, not a table you still have to read.

## Use case: Anomaly detection[​](#use-case-anomaly-detection "Direct link to Use case: Anomaly detection")

Not every recurring question needs a full summary — sometimes you just want to know if anything looks off.

Anomaly detection tasks run on a schedule, just like any other task. The difference is what you're asking the agent to do: instead of summarizing what happened, you're asking it to scan for anything outside the expected range and report back.

* A pipeline metric that dropped overnight
* An account that went dark
* A support category spiking before it turns into a broader customer complaint

Most runs, the answer is "everything looks normal," and that's the point.

You describe what "normal" looks like, tell the agent where to look, and it either flags something or confirms things are fine. Always include "if everything looks normal, say so" — otherwise silence is ambiguous, and you won't know whether the task ran clean or didn't run at all.

### Prompt template[​](#prompt-template-1 "Direct link to Prompt template")

```
I want you to scan [data source / metric area] for anything that looks unusual.



Did any [metrics / segments / accounts] move significantly from [yesterday / last 7 days /



same day last week]?



- Flag anything that changed by more than [X]% or crossed [specific threshold].



- Ignore [known noise sources, expected fluctuations, test accounts].



- If everything looks normal, say so. I'd rather get a "nothing to flag" than silence.
```

### Worked examples[​](#worked-examples-1 "Direct link to Worked examples")

**Daily metric anomaly scan**

> I want you to scan our key product and business metrics for anything that looks unusual. Did any metric move more than 20% from yesterday or from the same day last week?
>
> Check daily active users, new signups, sessions, and support ticket open rate. Ignore weekends when comparing to same-day-last-week. If everything looks normal, confirm that explicitly. Run every morning at 7am.

**Weekly customer health check**

> I want you to check the health of my top 100 accounts by ARR. Which accounts showed a significant drop in product usage or engagement over the past seven days?
>
> Flag any account where DAU dropped more than 25% week-over-week, or where there have been zero logins in the past five days. Exclude accounts in their first 30 days. Group flagged accounts by tier and include the account owner if that data is available.

**Data pipeline status check**

> I want you to check whether our data pipelines ran successfully overnight. Are there any tables or models that failed to update, ran significantly longer than usual, or are showing row count anomalies?
>
> Compare last run time and row counts against the rolling seven-day average. Flag anything more than two standard deviations from the norm. If everything ran clean, confirm it. Run every morning at 6am.

**Support volume spike detection**

> I want you to monitor our incoming support ticket volume for unusual spikes. Did ticket volume or a specific ticket category spike significantly in the last 24 hours compared to the prior seven-day average?
>
> Look at overall ticket count and break it down by category. Flag any category that's more than 40% above its seven-day rolling average. Include the top three most common ticket subjects for any flagged category. Run daily at 9am.

### Getting good results[​](#getting-good-results-1 "Direct link to Getting good results")

Anomaly detection works best when you're specific about what you want flagged. Vague instructions like "flag anything unusual" give the agent too much discretion. Specific ones like "flag any metric that moved more than 20% from the same day last week" give it a clear standard to work against.

A daily "nothing to flag" confirmation is actually useful. It tells you the task ran, the data looks healthy, and you don't need to dig in.

## Use case: Synthesizing across multiple data sources[​](#use-case-synthesizing-across-multiple-data-sources "Direct link to Use case: Synthesizing across multiple data sources")

Some of the most time-consuming recurring work isn't analysis — it's assembly. Pulling together what happened across GTM, product, and finance — each living in different tables, semantic models, or Hex projects — and turning it into something a person can actually act on.

The Hex Agent can pull from multiple sources in a single query: **[data connections](/docs/connect-to-data/data-connections/data-connections-introduction)** (the raw tables in your warehouse), **[semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models)** (curated business metrics your data team has defined), and **existing Hex projects** (analyses or apps already built in Hex). Attach them via `@`-mentions when you [configure the Task](/docs/explore-data/tasks#configuring-a-task). The more precise you are about where to look, the more coherent the output will be.

Ask for the same format every time. Consistent structure means the output is easy to scan and compare across runs. "Format as a short brief with one section per area" or "five bullets max, one per topic" gives you something predictable to come back to.

### Prompt template[​](#prompt-template-2 "Direct link to Prompt template")

```
I want you to pull together a summary across [list @-mentioned sources — mix of



semantic models, data connections, or existing Hex projects as needed]



and synthesize it into a single update.



What are the most important things that happened in [time period] across [areas / teams / topics],



and what requires attention or action?



Weight toward [outcomes / signals / decisions] over activity.



Exclude [noise, routine updates, test accounts].



Format as [bullet points / a short brief / an exec summary].



Run every [cadence].
```

### Worked examples[​](#worked-examples-2 "Direct link to Worked examples")

**Weekly business performance summary**

> Pull together a weekly summary of business performance using our `@Revenue semantic model`, `@Pipeline semantic model`, and `@Product Usage semantic model`.
>
> What changed most significantly across revenue, pipeline health, and product engagement last week? Flag anything that moved more than 15% from the prior week or that came in meaningfully above or below plan. Format as a short brief with one section per area. Run every Monday at 8am.

**End-of-quarter GTM and finance rollup**

> Summarize how we performed against our targets this quarter using our `@Finance semantic model` and our `@Q3 GTM Review Hex project`.
>
> Cover new ARR, pipeline coverage, win rate, and headcount efficiency. Compare actual performance to plan and flag anything that came in more than 10% above or below target. Format as an executive summary suitable for a board-level audience. Send to me on the last Friday of every quarter.

**Weekly product and data health check**

> Pull together a weekly health summary using our `@Product Usage semantic model` and the `pipeline_run_log` table from `@Snowflake`.
>
> For product: which features saw the biggest changes in adoption last week? For data: did all pipelines run successfully, and are there any models with row count anomalies or delayed refreshes? Separate findings by area. Run every Monday at 9am.

**Monthly cross-functional KPI digest**

> Summarize last month's performance using our `@Company KPIs semantic model`, our `@Feature Adoption Hex project`, and the `revenue_recognition` table from `@Snowflake`.
>
> For each area, surface the two or three most important developments and flag anything that warrants a decision. Focus on signals, not routine updates. Format as a monthly brief with one section per function. Run on the first Monday of every month.

### Getting good results[​](#getting-good-results-2 "Direct link to Getting good results")

The most useful thing you can do for cross-source summaries is @-mention your sources explicitly in the prompt — don't rely on the agent to find data it hasn't been pointed to. The more specific you are, the more coherent the output will be.

Ask for outcomes and decisions, not activity. "What happened" generates a list. "What needs attention or action" generates something you can do something with.

#### On this page

* [General best practices](#general-best-practices)
* [Use case: Dashboard digests](#use-case-dashboard-digests)
  + [Prompt template](#prompt-template)
  + [Worked examples](#worked-examples)
  + [Getting good results](#getting-good-results)
* [Use case: Anomaly detection](#use-case-anomaly-detection)
  + [Prompt template](#prompt-template-1)
  + [Worked examples](#worked-examples-1)
  + [Getting good results](#getting-good-results-1)
* [Use case: Synthesizing across multiple data sources](#use-case-synthesizing-across-multiple-data-sources)
  + [Prompt template](#prompt-template-2)
  + [Worked examples](#worked-examples-2)
  + [Getting good results](#getting-good-results-2)