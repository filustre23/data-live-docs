On this page

# Context consultant agent skill

Brief a coding agent that already knows how to build, measure, and improve Hex context.

info

* Requires the [context consultant skill](https://github.com/hex-inc/hex-skills/tree/main/skills/context-consultant) and the [Hex CLI](/docs/api-integrations/cli) (Team and Enterprise [plans](https://hex.tech/pricing/)).
* Runs of the Hex Agent and [evals](/docs/agent-management/evals) consume [credits](/docs/administration/credits).
* **Admins** and **Managers** can publish [guides](/docs/agent-management/context-management/guides), edit [endorsements](/docs/agent-management/context-management/endorsements-in-context-studio), and review [suggestions](/docs/agent-management/suggestions). **Editors** can run the Hex Agent and evals.
* Publishing guides, semantic models, or evals from Git uses [Context Sync](/docs/agent-management/context-management/context-sync) and a [workspace token](/docs/api-integrations/api/overview#workspace-tokens).

The context consultant agent skill teaches a coding agent the practices behind [Threads](/docs/explore-data/threads), the [Notebook Agent](/docs/explore-data/notebook-view/notebook-agent), and the [Modeling Agent](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#modeling-agent). Work with it the way you would a consultant. You bring the use case, the tables you trust, and which answers have to be exact. The agent already knows where each kind of context belongs, what to do first, and how to check a change before it is published.

Ask for the outcome in plain language. The agent chooses the asset, the command, and the order of steps. It works in Cursor, Claude Code, Codex, and other agents that read Markdown skills.

When a draft has to name real tables or columns, the coding agent asks the Hex Agent to write that part, because the Hex Agent can see your warehouse. The coding agent keeps only names the Hex Agent confirmed.

## Install[​](#install "Direct link to Install")

```
npx skills add hex-inc/hex-skills --skill context-consultant
```

Claude Code:

```
/plugin marketplace add hex-inc/hex-skills



/plugin install context-consultant@hex-skills
```

Start a **new chat**, then brief it the way you would a consultant. Name one use case and the outcome you want.

tip

This is different from `hex install agent-skill`, which teaches agents how to use the Hex CLI in general. Use `-g` to install the skill globally, or `-a cursor` / `-a claude-code` / `-a codex` to target a specific agent. You'll also need the [Hex CLI](/docs/api-integrations/cli) (`hex auth login`).

## The context it manages[​](#the-context-it-manages "Direct link to The context it manages")

Hex agents use four kinds of context. Each one has a job. The skill already applies this routing, so you can describe the information and let the agent place it. This table is what it is deciding.

| Kind | Job | Where you manage it |
| --- | --- | --- |
| **Endorsements** | Which tables, schemas, and models agents should prefer, and which to leave out | [Endorsements](/docs/agent-management/context-management/endorsements-in-context-studio) in Hex |
| **Warehouse descriptions** | What a table or column contains | Your warehouse, or the [Data browser](/docs/explore-data/data-browser) |
| **Workspace context and guides** | How to use the data. Workspace context is sent with every prompt. A guide is retrieved when a question matches its domain. | [Guides](/docs/agent-management/context-management/guides), in Hex or in Git through [Context Sync](/docs/agent-management/context-management/context-sync) |
| **Semantic models** | Joins, measures, and dimensions that must be calculated the same way every time | [Semantic models](/docs/agent-management/context-management/models), in Hex or in Git |

Put a rule that applies to every question in workspace context. Put a rule for one domain in a guide. Put a metric formula in a guide or a semantic model. Mark a table the agent should ignore with an **Exclude** status in Hex. A sentence in workspace context is an unreliable way to hide a table.

On Team and Enterprise, [reference repositories](/docs/agent-management/context-management/reference-repositories) and [External Apps](/docs/api-integrations/external-apps) can come later. They follow the same rule: a clear description of when the agent should use them.

## Set up one use case[​](#set-up-one-use-case "Direct link to Set up one use case")

Tell the agent one subject and three to five questions about it. Orders and returns is one use case. All of finance is too broad to tell whether the context helped.

The agent follows the order below. Ask it to walk you through a step before it writes anything, the same way you would ask a consultant to show their recommendation first.

1. **Endorse and exclude first.** In [Context Studio](/docs/agent-management/context-studio) or the [Data browser](/docs/explore-data/data-browser), **Endorse** the tables that use case needs and **Exclude** staging, test, and deprecated objects. This step happens in Hex. For a self-serve rollout, pair it with [Governed mode](/docs/agent-management/governed-mode) using the **Endorsed data** configuration.
2. **Describe the tables you endorsed.** Add descriptions for the tables and columns those questions use. Keep descriptions in the warehouse when you can. The [dbt Cloud integration](/docs/connect-to-data/data-connections/dbt-integration) can sync them into Hex.
3. **Draft workspace context and one guide.** Ask the coding agent for `hex.md` and one domain guide. It should hand any wording that names real tables or columns to the Hex Agent. See [what goes in workspace context](/tutorials/ai-best-practices/workspace-context-best-practices#what-goes-in-your-workspace-context).
4. **Preview, then publish.** The agent forks a [context preview](/docs/agent-management/evals#test-context-changes-before-publishing), checks a question or a small eval, then publishes. Use a pull request when you want review. The [Hex Context Toolkit GitHub Action](https://github.com/hex-inc/action-context-toolkit) syncs the merge. `hex context publish` publishes from the CLI.
5. **Lock in a baseline eval.** Write a few [baseline evals](/docs/agent-management/evals#designing-useful-evals) for the use case before the next edit, so a later change can be checked for regressions.

### A 30-minute start[​](#a-30-minute-start "Direct link to A 30-minute start")

Ask for a short first version. The agent already knows this sequence: endorse a few golden tables, exclude the objects agents should ignore, describe the most-queried columns, and write a guide with 5–10 rules. It adds a semantic model when a metric has to be exact. A small first version is enough. Context compounds as people use it.

## Improve context that is live[​](#improve-context-that-is-live "Direct link to Improve context that is live")

After people start asking questions, describe the miss or point the agent at open suggestions. It already knows this loop:

1. **Read the signal.** [Suggestions](/docs/agent-management/suggestions) propose a fix from real conversations. [Evals](/docs/agent-management/evals) show whether a known question still passes.
2. **Draft the change where that asset lives.** A repo-managed guide is a pull request. A guide that lives in Hex is edited in Context Studio, or published from a preview. An endorsement or a warehouse description is always a change in Hex.
3. **Test before you publish.** Compare an eval run on published context with a run against the [preview](/docs/agent-management/evals#test-context-changes-before-publishing). Publish when the failing case improves and the baseline cases still pass.
4. **Close it out.** Merge the pull request so [Context Sync](/docs/agent-management/context-management/context-sync) updates Hex, or run `hex context publish`.

Group related edits by domain. Several revenue-guide fixes belong in one change.

## What to ask[​](#what-to-ask "Direct link to What to ask")

Start a new chat after you install the skill. Brief it the way you would a consultant. Be specific, or describe the problem and let it choose the fix:

> Set up Hex context for our orders and returns questions. Endorse the tables we need, exclude staging, and draft one guide. Show me the eval before you publish.

> Threads keeps answering revenue from the staging orders table. Fix the context and check it against our baseline evals.

> Review open Context Studio suggestions for revenue and turn the useful ones into a guide update.

## Customize the skill[​](#customize-the-skill "Direct link to Customize the skill")

Use the skill as it ships for the first few sessions. Customizing it is a later step, once you know which of its defaults you want to keep.

The installed skill is a set of Markdown files on your machine. Edit those files so the next chat already knows how your team works. Useful additions:

* The publish path you prefer, a GitHub pull request or `hex context publish`
* Metrics that have to be exact, and questions where a close answer is enough
* Schemas and tables agents should ignore
* A semantic-first rule, if agents should use semantic models before they write raw SQL
* Sections you want in every new guide

The agent also writes a short `hex_context.profile.md` the first time it learns your workspace, so later chats skip the setup questions. Editing the skill is how those preferences stay with the copy you installed. Start with [SKILL.md](https://github.com/hex-inc/hex-skills/blob/main/skills/context-consultant/SKILL.md).

## Related guides[​](#related-guides "Direct link to Related guides")

* [Set up your workspace for AI agents](/tutorials/ai-best-practices/setup-for-ai-agents)
* [Workspace context best practices](/tutorials/ai-best-practices/workspace-context-best-practices)
* [Guides](/docs/agent-management/context-management/guides)
* [Evals](/docs/agent-management/evals)
* [Context Sync](/docs/agent-management/context-management/context-sync)

#### On this page

* [Install](#install)
* [The context it manages](#the-context-it-manages)
* [Set up one use case](#set-up-one-use-case)
  + [A 30-minute start](#a-30-minute-start)
* [Improve context that is live](#improve-context-that-is-live)
* [What to ask](#what-to-ask)
* [Customize the skill](#customize-the-skill)
* [Related guides](#related-guides)