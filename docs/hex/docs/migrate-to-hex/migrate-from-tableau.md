On this page

# Migrate Tableau dashboards

Turn Tableau Cloud, Server, or Desktop workbooks into Hex apps — without rebuilding every chart from scratch.

info

* Requires the [Tableau migration skill](https://github.com/hex-inc/hex-skills/tree/main/skills/tableau-migration) and the [Hex CLI](/docs/api-integrations/cli) (Team and Enterprise [plans](https://hex.tech/pricing/)).
* The default path uses the [Hex Agent](/docs/explore-data/notebook-view/notebook-agent) and consumes [credits](/docs/administration/credits).
* **Admins**, **Managers**, and **Editors** can use the Hex Agent. Only **Admins** and **Managers** can create or publish Hex [guides](/docs/agent-management/context-management/guides).
* You need a Tableau Personal Access Token that can download workbooks, or exported `.twb` / `.twbx` files.

Ask your coding agent to migrate a Tableau workbook, and it will read the `.twb`, write a brief for Hex, and hand the build to the Hex Agent. You get a [generative app](/docs/share-insights/apps/generative-apps) sitting on SQL cells you can inspect, plus a check against the original dashboard.

## Install[​](#install "Direct link to Install")

```
npx skills add hex-inc/hex-skills --skill tableau-migration
```

Claude Code:

```
/plugin marketplace add hex-inc/hex-skills



/plugin install tableau-migration@hex-skills
```

Start a **new chat**, then try asking to migrate your Tableau dashboards to Hex.

tip

This is different from `hex install agent-skill`, which teaches agents how to use the Hex CLI in general. Use `-g` to install the skill globally, or `-a cursor` / `-a claude-code` / `-a codex` to target a specific agent. You'll also need the [Hex CLI](/docs/api-integrations/cli) (`hex auth login`). Keep filled-in credential files gitignored.

## What you need[​](#what-you-need "Direct link to What you need")

1. In the installed skill folder, copy `credentials/tableau.env.example` to `credentials/tableau.env`. Fill in your Tableau **pod URL**, **site**, and **Personal Access Token**, and don't commit the filled-in file.
2. Install and log in to the [Hex CLI](/docs/api-integrations/cli).
3. Know which Hex [data connection](/docs/connect-to-data/data-connections/data-connections-introduction) the migrated SQL should use. The skill matches on warehouse type and database, not on connection names.
4. **Optional:** Install Playwright for screenshot QA (`pip install playwright && playwright install chromium`). The first run asks you to sign in to Hex once; later captures are headless. Skip this if you'd rather review the app yourself.

No PAT? In Tableau Desktop, select **File → Export Packaged Workbook** and put the files in one folder. The skill can also pull from Tableau Cloud or Server with `scripts/tableau_fetch.py`.

## How it works[​](#how-it-works "Direct link to How it works")

The workbook XML is what the skill trusts. Screenshots are just for checking the result.

1. **It finds the right Hex connection.** Published Tableau datasources and extracts need an explicit Hex target. Extracts are snapshots, so a live warehouse query can legitimately differ.
2. **It reads the workbook.** Worksheets that share a table, join, and grain get grouped into shared SQL. Calculations, LOD expressions, table calcs, filters, and parameters land in a brief the Hex Agent can follow. Filters that apply to the whole workbook go into the shared query; sheet-level filters stay on the chart.
3. **Hex builds a generative app.** The Hex Agent reads that brief — including titles, colors from the XML, and number formats — and creates the app on those SQL dataframes. You'll get a live thread URL so you can watch (and redirect) the build.
4. **The SQL and the look both get checked.** The skill re-derives the intended queries from the `.twb` and compares them to the cells under the app. If you installed Playwright, it can also screenshot the Hex app next to Tableau and iterate.
5. **It writes a guide.** Once per Tableau data source, the skill writes a Hex [guide](/docs/agent-management/context-management/guides) so the rest of your team can self-serve in Threads. This step requires the **Admin** or **Manager** workspace role. **Editors** can finish the app without it, or ask an **Admin** or **Manager** to publish the guide.

If you prefer to build a classic Hex app, the skill can fall back to native [chart](/docs/explore-data/cells/visualization-cells/chart-cells) and [single value](/docs/explore-data/cells/visualization-cells/single-value-cells) cells.

## Run a migration[​](#run-a-migration "Direct link to Run a migration")

### Choose what to migrate[​](#choose-what-to-migrate "Direct link to Choose what to migrate")

You don't need to bring the whole Tableau site with you. Capture name, owner, last viewed, 90-day view count, and the decision each dashboard drives, then sort:

|  | Bring over | Leave behind |
| --- | --- | --- |
| **Usage** | People open it regularly | Almost no views in 90 days |
| **Value** | Drives a recurring decision | One-off or "nice to have" |
| **Ownership** | Someone still maintains it | Stale or orphaned |

Have the owners confirm the buckets, and collapse near-duplicates into one version. Put the "bring over" set in one folder of `.twb` files (or one Tableau project) so the skill can batch them.

### Start with a pilot[​](#start-with-a-pilot "Direct link to Start with a pilot")

Migrate **one or two** dashboards all the way through before you point the skill at a folder. Pick something representative and reasonably simple. If you run a second, choose one with filters, LOD, or a table calc — not the single hardest dashboard you have.

Then ask something like:

> Migrate this Tableau workbook into Hex. Get the SQL right first, then match the look as closely as you can. Finish this one dashboard, including a visual check, before touching the rest of the folder.

If a workbook in a batch fails, the skill records it and keeps going.

### What you'll be asked for[​](#what-youll-be-asked-for "Direct link to What you'll be asked for")

* Tableau access (a PAT) or exported `.twb` / `.twbx` files
* The target Hex data connection, when names don't uniquely match
* A one-time Hex sign-in, if you're using screenshot QA
* A look at the pilot (and each later batch) before you call it done

The default path spends Hex credits. As soon as the Hex Agent starts building, the coding agent should share the thread URL so you can follow along.

## Things that don't map 1:1[​](#things-that-dont-map-11 "Direct link to Things that don't map 1:1")

Worth flagging before a pilot, so nobody expects a pixel-perfect copy:

* **Maps** rebuild as Python cells, not native Hex charts.
* **Extract-backed datasources** (`.hyper`) can differ from a live query. Ask which warehouse connection the extract was built on.
* **Excel / CSV lookups** aren't stored in the `.twb`. You'll need to provide the source file.
* **Web page / iframe objects** are not scoped in the migration skill and should be added afterwards.

Where the XML doesn't specify styling, Hex defaults win. Get the layout and the numbers close; don't chase every pixel.

## After you migrate[​](#after-you-migrate "Direct link to After you migrate")

Leave the `.twb` reference cell in the notebook — it won't appear on the app. The SQL stays in cells so analysts can see what changed. Reuse the per-data-source [guide](/docs/agent-management/context-management/guides) across every dashboard that sat on that Tableau data source.

Full instructions are in the skill's `[SKILL.md](https://github.com/hex-inc/hex-skills/blob/main/skills/tableau-migration/SKILL.md)`.

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