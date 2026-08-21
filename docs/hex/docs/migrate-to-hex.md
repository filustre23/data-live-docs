On this page

# Hex migration skills

Move Tableau and Looker dashboards into Hex with a coding agent — all from the Hex CLI.

info

* These skills run in your coding agent, such as Cursor, Claude Code, or Codex.
* The [Hex CLI](/docs/api-integrations/cli) is available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* The default path uses the [Hex Agent](/docs/explore-data/notebook-view/notebook-agent) and consumes [credits](/docs/administration/credits).
* **Admins**, **Managers**, and **Editors** can use the Hex Agent. Only **Admins** and **Managers** can create or publish Hex [guides](/docs/agent-management/context-management/guides).

You don't have to rebuild every chart by hand. [Migration skills](https://github.com/hex-inc/hex-skills) teach your coding agent how Tableau and Looker work, then the Hex Agent rebuilds each dashboard as a [generative app](/docs/share-insights/apps/generative-apps) on SQL cells you can inspect.

Ask in plain language — "migrate this Tableau workbook to Hex" — and the coding agent handles the rest.

## Skills[​](#skills "Direct link to Skills")

* [Migrate Tableau dashboards](/docs/migrate-to-hex/migrate-from-tableau)
* [Migrate Looker dashboards](/docs/migrate-to-hex/migrate-from-looker)

## How they work[​](#how-they-work "Direct link to How they work")

Your coding agent reads the source workbook or LookML and writes a brief into a Hex project. The Hex Agent builds the [generative app](/docs/share-insights/apps/generative-apps), because it can see your warehouse, workspace context, and the rendered result. The skill then checks the SQL — and, if you want, the look — before you sign off. It also writes a Hex [guide](/docs/agent-management/context-management/guides) so the rest of your team can self-serve in Threads.

Start with one or two dashboards, then batch the rest. Accuracy first, similar look and feel second.

tip

Most BI sites are full of dashboards nobody opens. Inventory usage first, and only migrate what people actually use.

#### On this page

* [Skills](#skills)
* [How they work](#how-they-work)