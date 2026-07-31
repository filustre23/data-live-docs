On this page

# Evals

Measure how reliably the Hex agent answers questions, and track regressions and improvements over time.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Users need the Editor, Manager or Admin workspace role to create and view evals.

Evals let you programmatically run [threads](/docs/explore-data/threads) with the Hex agent and grade each response against rubrics you define. You can use evals to:

* Establish a baseline for questions the agent should answer reliably
* Test changes to guides and semantic models before you publish them
* Catch regressions in agent behavior
* Measure consistency, run time, and credit usage
* Compare performance across context or model configurations

Because eval suites are defined in YAML files, you can keep them in version control alongside your context files and include them in your development workflows.

## Terminology[​](#terminology "Direct link to Terminology")

An **eval suite** holds one or more **cases**, each graded by one or more **rubrics**. When you **run** a suite, the agent answers each case's prompt in its own thread.

* **Eval suite:** A group of cases and their rubrics, defined together in one YAML file.
* **Case:** A single test that defines a prompt given to the agent and settings for how the thread should run (attempts, Endorsed Mode, etc.).
* **Rubric:** A pass/fail check applied to a case. One case can have multiple rubrics — for example, one rubric might verify the agent used the correct guide, while another checks whether the final answer includes the expected value.
* **Run:** One execution of a suite. Review run results from the [CLI](/docs/api-integrations/cli) or in [Context Studio](/docs/agent-management/context-studio).

## Run your first eval[​](#run-your-first-eval "Direct link to Run your first eval")

Before you begin, make sure:

* The [Hex CLI](/docs/api-integrations/cli) is installed and authenticated
* You have an **Admin**, **Manager**, or **Editor** role in the workspace
* You have access to any resources referenced by the eval

The example below defines a single case with one rubric — enough to create and run your first suite. See [Write an eval suite](#write-an-eval-suite) for the full schema.

Create a file named `first-eval.yaml`:

```
name: My first eval suite



cases:



- id: math-check



prompt: What is 2 + 2?



attempts: 1



rubrics:



- id: says-four



type: judge_final_answer



criterion: Does the final answer say the result is 4?
```

Start the run:

```
hex eval run ./first-eval.yaml
```

The command returns a suite run ID and a link to the run in Context Studio.

### Billing[​](#billing "Direct link to Billing")

Running a suite consumes [credits](/docs/administration/credits), similar to any other agent activity in Hex. Each case runs a real agent thread, and the result is graded by an LLM judge. Credit usage includes both the underlying agent thread and the judge.

Credits are attributed to the user who starts the suite run. Hex uses that user’s available credits first, then draws from the workspace’s shared credit pool if needed.

## Review results[​](#review-results "Direct link to Review results")

Evals can only be defined and run from the CLI, but you can review results in either the CLI or the Evals page in Context Studio.

### Review results in the CLI[​](#review-results-in-the-cli "Direct link to Review results in the CLI")

To find a run, use `hex eval list`. It returns the most recent runs in your workspace along with their run IDs, suite IDs, status, pass and fail counts, etc.

Use `hex eval get <suite_run_id>` to see a suite-level summary and results for each case.

Use `hex eval case get <case_run_id>` to dig into a single case. This shows each rubric's verdict and the judge's reasoning, and a link to the agent thread so you can see exactly what the agent did.

Append `--json` to any command for machine-readable output.

### Review results in Context Studio[​](#review-results-in-context-studio "Direct link to Review results in Context Studio")

The Evals page is where you can see all eval suites run in your workspace. This page shows an overview of each suite, including the number of cases passed, who ran each suite, run time, and more.

You can also select multiple runs to compare them side by side — for example, to compare the same suite using published context versus a Context Preview.

Open a run to see its cases, then expand a case for the full detail: the prompt, each rubric's verdict, and the judge's reasoning for why it passed or failed. Each case also shows its attempts, run time, credit usage, and model. You can open the underlying thread to see how the agent reached its answer.

### Cancel a run[​](#cancel-a-run "Direct link to Cancel a run")

A run that's still in progress can be canceled, either from its run page in Context Studio or from the CLI:

```
hex eval cancel <run_id>
```

Canceling stops any cases that haven't finished. Cases that already completed keep their grades, and the run keeps a partial summary of those results. Cases that were still running are marked Canceled.

### Understand case results[​](#understand-case-results "Direct link to Understand case results")

* **Pass** — all rubrics passed.
* **Fail** — at least one rubric failed.
* **Error** — the case could not run or be graded, for example because a required resource was unavailable or the workspace is out of credits.
* **Cancelled** — the case was still running when the suite run was cancelled.
* **Skipped** — the case was excluded from a partial run.

#### Multiple attempts[​](#multiple-attempts "Direct link to Multiple attempts")

Each case can run 1-3 attempts. Every attempt is graded independently against the case’s rubrics.

For cases with 2 or 3 attempts, the case passes as long as no more than one attempt fails.

* 1 attempt: it must pass
* 2 attempts: at least 1 must pass
* 3 attempts: at least 2 must pass

The Hex agent is non-deterministic, so the same prompt can produce different responses across runs. Multiple attempts help distinguish a one-off failure, which is tolerated, from a repeated failure that causes the case to fail.

## Designing useful evals[​](#designing-useful-evals "Direct link to Designing useful evals")

Good evals reflect real questions your team expects the Hex agent to answer. A strong suite usually includes two kinds: baseline evals that guard what already works, and hill-climbing evals that test harder questions the agent can't reliably answer yet.

**Baseline evals** are questions you expect to pass consistently — the canonical facts and definitions your business depends on. Use them to test context changes before publishing and to monitor the ongoing health of the agent in production. This can catch changes caused by dependencies that evolve separately from your published context, such as referenced projects or MCP servers. A few examples:

* Core metric values — a known value for an important business metric: “What was our ARR in March 2024?”
* Canonical definitions — a shared definition the agent should always apply: "How do we define an active customer?"
* Methodology and rules — questions whose correct answer depends on applying the right filters and fields: "How many active customers do we have today?"

Because these usually have a knowable answer, they pair well with a `numeric_value` or `judge_final_answer` [rubric type](#rubric-types). Run them before publishing context changes, and periodically against published context to catch regressions.

**Hill-climbing evals** are harder, aspirational questions the agent isn't expected to answer reliably yet. Use them to track improvement as you build out your context.

They’re especially useful in a test-driven workflow: write the eval first, then iterate on your guides and semantic models until the agent can pass it consistently. The eval defines the target, and the pass rate shows whether your changes are moving the agent toward it.

The goal is to improve these cases over time without regressing your baseline cases.

## Test context changes before publishing[​](#test-context-changes-before-publishing "Direct link to Test context changes before publishing")

Evals are especially useful when you run them against a **Context Preview** — a sandboxed fork of your context — before a change reaches production. This mirrors a normal software workflow: fork, change, test, then publish. It assumes you keep your guides and semantic models in a Git-backed context repository.

### The editing loop[​](#the-editing-loop "Direct link to The editing loop")

1. Edit your guides or semantic models locally.
2. Run `hex context preview` from a git repository that has a `hex_context.config.json` at its root. This uploads the current working tree to an ephemeral context branch and prints a Preview ID and link.
3. Run `hex eval run <file> --preview-id <preview_id>` to run your suite against that preview instead of currently published context.
4. Compare to a baseline run (the same suite with no `--preview-id`) to see whether the change caused any regressions, or improved your hill-climbing evals.
5. When you’re ready to publish, run `hex context publish <preview_id>`. Replace `<preview_id>` with `-` to use the last preview created in this session.

## Write an eval suite[​](#write-an-eval-suite "Direct link to Write an eval suite")

An eval suite is defined in a YAML file and requires a `name` and at least one case. Each case requires an `id`, a `prompt`, an `attempts` count, and at least one rubric.

The example below shows the available suite and case settings, along with all three [rubric types](#rubric-types).

```
name: "March MAU checks"



id: march-mau-checks



cases:



- id: mau-detailed



prompt: "How many monthly active users did we have in March 2024?"



attempts: 1   # 1-3; re-runs the case to show variance



attachments:  # optional



dataConnectionId: "dc_123"



tableIds:



- "dst_123"



- "dst_456"



projectIds:



- "prj_123"



threadOptions:



endorsedMode: true



rubrics:



# judge_thread: LLM judge over the whole conversation



- id: counted_distinct_users



type: judge_thread



criterion: "Did the agent count distinct users rather than sessions?"



# judge_final_answer: LLM judge over the final answer only.



- id: states_the_number



type: judge_final_answer



criterion: "Does the final answer give a single MAU number?"



expected: "18432" # optional ground truth



# numeric_value (literal target): compare a number within tolerance



- id: mau_matches



type: numeric_value



target: 18432



tolerancePercentage: 1



# numeric_value (SQL ground truth): target computed from a query



- id: mau_matches_sql



type: numeric_value



target:



sql: "SELECT count(distinct user_id) FROM events WHERE date_trunc('month', ts) = '2024-03-01'"



dataConnectionId: "dc_..."



timeoutSeconds: 30      # optional, max 60
```

### Suite-level fields[​](#suite-level-fields "Direct link to Suite-level fields")

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `name` | Yes | string | Suite name. Used to derive `id` when `id` is omitted. |
| `cases` | Yes | array | The suite's cases. At least one is required. |
| `id` | No | string | Stable identifier used to group runs of the same suite. Derived from `name` when omitted. |
| `modelSelection` | No | object | Pins the agent `model` and `effortLevel` for the suite. |
| `caseRunSelection` | No | object | Runs only certain cases or excludes them. Set either `only` or `except` to a non-empty array of case IDs, not both. |

Eval suite limits:

* A suite can contain up to 100 cases
* Each case can run 1-3 attempts
* Each case can have up to 15 rubrics
* A workspace can have up to 3 runs in progress at once

Suite IDs

Runs with the same suite ID are grouped together, allowing you to track a suite’s results over time and filter them with `hex eval list --suite-id`.

If you don’t set an `id`, Hex derives one from the suite `name`. Renaming a suite without an explicit `id` creates a new suite grouping and separates it from earlier runs.

Use `hex eval suite ids --search <string>` to find existing suite IDs in your workspace.

### Case-level fields[​](#case-level-fields "Direct link to Case-level fields")

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `id` | Yes | string | Unique identifier for the case within the suite. |
| `prompt` | Yes | string | The question given to the agent. |
| `attempts` | Yes | number | How many times to run the case, 1-3. No default. See [Multiple attempts](#multiple-attempts). |
| `rubrics` | Yes | array | One or more rubrics to grade the case. See [Rubric types](#rubric-types). |
| `attachments` | No | object | Resources to expose to the agent up front. See [Attach context to a case](#attach-context-to-a-case). |
| `threadOptions` | No | object | Per-case thread settings, such as `endorsedMode`. |

### Rubric types[​](#rubric-types "Direct link to Rubric types")

Choose a rubric type based on what you want to check.

* `judge_thread` — grades the agent's outcome against the criterion using the full thread, including messages, tool activity, and the final answer. Use this to check how the agent arrived at its answer, such as whether it used the expected table or business definition.
* `judge_final_answer` — the same judge, but it sees only the agent's final answer. Use this to check the delivered result itself.
* `numeric_value` — checks whether the number from the agent's answer matches a target value or SQL ground truth, within the configured tolerance.

#### Fields for `judge_thread` and `judge_final_answer`[​](#fields-for-judge_thread-and-judge_final_answer "Direct link to fields-for-judge_thread-and-judge_final_answer")

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `id` | Yes | string | Unique identifier. |
| `type` | Yes | `judge_thread` or `judge_final_answer` | `judge_thread` evaluates evidence from the full thread. `judge_final_answer` evaluates only the final answer. |
| `criterion` | Yes | string | What the judge checks for, written as a clear pass/fail question or statement. |
| `expected` | No | string | An optional description of the correct answer to grade against. |
| `expectedSql` | No | SQL target | An optional query whose result is the correct answer to grade against. |

`expected` and `expectedSql` can be used together. When both are set, the judge sees your description alongside the query result.

#### Fields for `numeric_value`[​](#fields-for-numeric_value "Direct link to fields-for-numeric_value")

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `id` | Yes | string | Unique identifier. |
| `type` | Yes | `numeric_value` | — |
| `target` | Yes | number or SQL target | Fixed number, or `{ sql, dataConnectionId }` run at grade time. Optionally add `timeoutSeconds` (max 60s). |
| `tolerancePercentage` | No | number | Allowed difference as a percent of `target`. Default 1. Applies even when `absoluteTolerance` is set. |
| `absoluteTolerance` | No | number | Allowed difference as a fixed amount, in the target’s units. Checked in addition to `tolerancePercentage`, not instead of it — a value passes if it's within either. For an exact match, set both `absoluteTolerance: 0` and `tolerancePercentage: 0`. |
| `outputFormat` | No | `int` or `float` | Default `float`. |
| `strictHeadline` | No | boolean | Default `true`. Grades the number identified as the answer’s primary result, and fails the rubric if no primary result can be identified. Set to `false` to pass when any number in the response matches the target. |
| `extractionGuidance` | No | string | Hint for which number to grade when the answer has several, e.g. "the enterprise ARR, not total ARR". |

### Attach context to a case[​](#attach-context-to-a-case "Direct link to Attach context to a case")

Use `attachments` to point a case to specific resources — a data connection, tables, semantic datasets or views, or projects. This gives the agent that context up front, the same way @-mentioning a resource does in a normal thread.

You must have access to whatever you reference, or the run errors with UNAUTHORIZED.

| Field | Type | Notes |
| --- | --- | --- |
| `dataConnectionId` | string | Data connection to expose to the agent |
| `tableIds` | string[] | Specific data-source tables |
| `semanticDatasetIds` | string[] | Semantic datasets |
| `semanticViewIds` | string[] | Semantic views |
| `projectIds` | string[] | Hex projects |

To restrict the agent to endorsed resources for a case, set `threadOptions: { endorsedMode: true }`.

## Compare models[​](#compare-models "Direct link to Compare models")

You can pin a model and effort level for a single run:

```
hex eval run ./my-suite.yaml --model <model_name> --effort medium
```

`--model` and `--effort` must be provided together. Valid effort levels are low, medium, high, xhigh, and max.

You can also set a default model and effort level in the suite definition:

```
name: "March MAU checks"



id: march-mau-checks



modelSelection:



model: <model_name>



effortLevel: medium



cases:



# ...
```

If both are provided, the CLI flags override the suite’s modelSelection. If neither is provided, the run uses your workspace default.

The selected model must be available in your workspace.

#### On this page

* [Terminology](#terminology)
* [Run your first eval](#run-your-first-eval)
  + [Billing](#billing)
* [Review results](#review-results)
  + [Review results in the CLI](#review-results-in-the-cli)
  + [Review results in Context Studio](#review-results-in-context-studio)
  + [Cancel a run](#cancel-a-run)
  + [Understand case results](#understand-case-results)
* [Designing useful evals](#designing-useful-evals)
* [Test context changes before publishing](#test-context-changes-before-publishing)
  + [The editing loop](#the-editing-loop)
* [Write an eval suite](#write-an-eval-suite)
  + [Suite-level fields](#suite-level-fields)
  + [Case-level fields](#case-level-fields)
  + [Rubric types](#rubric-types)
  + [Attach context to a case](#attach-context-to-a-case)
* [Compare models](#compare-models)