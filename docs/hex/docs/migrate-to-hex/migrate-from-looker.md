On this page

# Migrate Looker dashboards

Rebuild Looker dashboards and Looks in Hex, and check the numbers against Looker's own results.

info

* Requires the [Looker migration skill](https://github.com/hex-inc/hex-skills/tree/main/skills/looker-migration) and the [Hex CLI](/docs/api-integrations/cli) (Team and Enterprise [plans](https://hex.tech/pricing/)).
* The default path uses the [Hex Agent](/docs/explore-data/notebook-view/notebook-agent) and consumes [credits](/docs/administration/credits).
* **Admins**, **Managers**, and **Editors** can use the Hex Agent. Only **Admins** and **Managers** can create or publish Hex [guides](/docs/agent-management/context-management/guides) or [semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models).
* Most production dashboards are built in the Looker UI (user-defined dashboards). Those are only reachable through the Looker API — a LookML git checkout isn't enough on its own.

Looker already has the SQL and the numbers. The skill uses both: it reads LookML and Looker's generated queries, then the Hex Agent rebuilds the dashboard as a [generative app](/docs/share-insights/apps/generative-apps). Before you sign off, Hex's cell output is compared to Looker's own results.

## Install[​](#install "Direct link to Install")

```
npx skills add hex-inc/hex-skills --skill looker-migration
```

Claude Code:

```
/plugin marketplace add hex-inc/hex-skills



/plugin install looker-migration@hex-skills
```

Start a **new chat**, then try asking to migrate your Looker dashboards to Hex.

tip

This is different from `hex install agent-skill`, which teaches agents how to use the Hex CLI in general. Use `-g` to install the skill globally, or `-a cursor` / `-a claude-code` / `-a codex` to target a specific agent. You'll also need the [Hex CLI](/docs/api-integrations/cli) (`hex auth login`). Keep filled-in credential files gitignored.

## What you need[​](#what-you-need "Direct link to What you need")

1. In the installed skill folder, copy `credentials/looker.env.example` to `credentials/looker.env`. Fill in your Looker **base URL** plus an **API3 client ID and secret**. You can also use `~/.looker/looker.ini`. Don't commit the filled-in file.
2. Install and log in to the [Hex CLI](/docs/api-integrations/cli).
3. Know which Hex [data connection](/docs/connect-to-data/data-connections/data-connections-introduction) the migrated SQL should use. The skill matches the LookML model's `connection:` by dialect and database, not by name.
4. **Optional:** Install Playwright for screenshot QA (`pip install playwright && playwright install chromium`). The first Hex screenshot run asks you to sign in once; Looker source images render over the API and don't need a browser. Skip this if you'd rather review the app yourself.
5. Smoke-test access with `python3 scripts/looker_fetch.py whoami`.

A LookML git checkout is enough for LookML dashboards. You still need the API for user-defined dashboards, generated SQL, and the result rows used to check numbers.

## How it works[​](#how-it-works "Direct link to How it works")

Looker has a semantic layer and a presentation layer. The skill converts them separately:

| In Looker | Becomes in Hex |
| --- | --- |
| LookML views, models, and explores | Shared SQL cells plus a Hex [guide](/docs/agent-management/context-management/guides). Optionally a governed [semantic model](/docs/connect-to-data/semantic-models/intro-to-semantic-models). |
| Dashboards (user-defined and LookML) | A Hex project: SQL cells and a generative app |
| Looks | The same path, as a one-tile app |

Most real dashboards are **user-defined** — built in the Looker UI, not sitting in a `.lkml` file — so discovery goes through the API.

1. **It finds the right Hex connection** from the LookML model's `connection:`.
2. **It fetches the dashboard, Looker's SQL, and a source image.** Looker's SQL is already in your warehouse dialect, so the skill adapts it to Hex rather than reverse-engineering every measure. It also pulls the actual result rows, which is how it checks Hex's numbers later.
3. **It groups tiles that belong together** — same explore, join graph, and shared filters — into shared SQL. Explore-level filters and dashboard filters that tiles listen to go on the shared query; a tile's own filters stay on the chart. Fields are resolved by `view.field` id, not the label people see.
4. **Hex builds a generative app.** The Hex Agent reads the brief (including colors and number formats from Looker) and creates the app on those SQL dataframes. You'll get a live thread URL so you can watch the build.
5. **The numbers get checked against Looker, then the look.** Hex cell output is compared to Looker's results. If you installed Playwright, the skill can also compare screenshots and iterate.
6. **It ships a semantic layer once per explore.** The default is a Hex guide. If your team wants an enforced metrics layer, the skill can also author a Hex semantic model — after you create an empty semantic project in the UI. Both require the **Admin** or **Manager** workspace role. **Editors** can finish the app without this step, or ask an **Admin** or **Manager** to publish the guide or semantic model.

If you prefer to build a classic Hex app, the skill can fall back to native [chart](/docs/explore-data/cells/visualization-cells/chart-cells) and [single value](/docs/explore-data/cells/visualization-cells/single-value-cells) cells.

## Run a migration[​](#run-a-migration "Direct link to Run a migration")

### Choose what to migrate[​](#choose-what-to-migrate "Direct link to Choose what to migrate")

You don't need to bring the whole Looker instance with you. List dashboards, Looks, and models with `looker_fetch.py`, then pull usage from Looker's **System Activity** model if the API user has `see_system_activity`. Per dashboard, capture title, owner, last run, 90-day run count, and the decision it drives.

|  | Bring over | Leave behind |
| --- | --- | --- |
| **Usage** | People run it regularly | Almost no runs in 90 days |
| **Value** | Drives a recurring decision | One-off or "nice to have" |
| **Ownership** | Someone still maintains it | Stale or orphaned |

Have the owners confirm the buckets, and collapse near-duplicates. Put a wave of dashboard ids in one folder so the skill can batch them.

### Start with a pilot[​](#start-with-a-pilot "Direct link to Start with a pilot")

Migrate **one or two** dashboards all the way through before the rest of the list. Pick something representative and reasonably simple. If you run a second, choose one with a pivot, table calc, or derived table.

Then ask something like:

> Migrate this Looker dashboard into Hex. Use Looker's generated SQL as the reference, and check the numbers against Looker's own results before worrying about the look. Finish this one dashboard before the rest of the list.

If a dashboard in a batch fails, the skill records it and keeps going.

### What you'll be asked for[​](#what-youll-be-asked-for "Direct link to What you'll be asked for")

* Looker API3 credentials (required for user-defined dashboards) and, optionally, a LookML git checkout
* The target Hex data connection, when names don't uniquely match
* A one-time Hex sign-in, if you're using screenshot QA
* A look at the pilot (and each later batch) before you call it done
* For an optional semantic model: an empty semantic project created in the Hex UI, so the CLI can populate it

The default path spends Hex credits. As soon as the Hex Agent starts building, the coding agent should share the thread URL so you can follow along.

## Things that don't map 1:1[​](#things-that-dont-map-11 "Direct link to Things that don't map 1:1")

Worth flagging before a pilot, so nobody expects a pixel-perfect copy:

* **Maps** rebuild as Python cells.
* **Custom or marketplace visualizations** are approximated or called out.
* **Merged results** become a join or a companion query.
* **User-attribute row-level security** can map to Hex RBAC with Jinja, but test it on purpose — don't assume it came along for the ride.
* **Derived tables / PDTs** become CTEs or subqueries, with similar cost.
* **Table calcs** run after SQL in Looker, so they aren't in Looker's generated SQL. The skill translates them to window functions and checks the final numbers against Looker's results.

Two things you don't have to special-case: Hex supports cross-filtering, and Hex refreshes cells individually.

## After you migrate[​](#after-you-migrate "Direct link to After you migrate")

Leave the Looker contract cell in the notebook — just don't put it on the app. The SQL stays in cells so analysts can see what changed. Dashboards that shared a Looker explore should share one Hex [guide](/docs/agent-management/context-management/guides). Refresh it rather than duplicating it per dashboard.

Full instructions are in the skill's `[SKILL.md](https://github.com/hex-inc/hex-skills/blob/main/skills/looker-migration/SKILL.md)`.

#### On this page

* [Install](#install)
* [What you need](#what-you-need)
* [How it works](#how-it-works)
* [Run a migration](#run-a-migration)
  + [Choose what to migrate](#choose-what-to-migrate)
  + [Start with a pilot](#start-with-a-pilot)
  + [What you'll be asked for](#what-youll-be-asked-for)
* [Things that don't map 1:1](#things-that-dont-map-11)
* [After you migrate](#after-you-migrate)