On this page

# Model picker best practices

Choose the right model and effort level for your analytical work in Hex.

When you attack a problem with the wrong tool, even if you get to the solution, you can waste time and energy. With AI, that manifests as choosing the right model for your task. More and more models are being released, each with their own strengths and cost trade-offs. We think you should be able to pick the right one for whatever you need to do in Hex.

We recently launched the ability to pick your model based on what you want to build. With this launch, it's important to understand the capabilities and estimated cost of using each model. Because agents are non-deterministic, you should treat these as guidelines on what you can expect.

Let's break them down by the tasks they are best suited for, the expected cost to use them, and the responses you'll likely get.

tip

This information was published in July 2026 and includes models available up to that date range.

## How to pick your model[​](#how-to-pick-your-model "Direct link to How to pick your model")

When starting a new agent conversation, you can select the **Auto** dropdown to choose a different model for your session.

## Auto[​](#auto "Direct link to Auto")

To optimize credits and effort, Hex defaults to **Auto**, which automatically selects the model best suited for the task based on our evals. Auto is typically the right choice for most day-to-day analytics questions. Unless you're doing a very simple or complex task, or aren't getting useful responses, we recommend starting in Auto mode.

## Choosing the right model for your task[​](#choosing-the-right-model-for-your-task "Direct link to Choosing the right model for your task")

The Hex Agent works with a range of models and efforts, each suited to different kinds of analytical work. Here's how to pick the right one for the job.

You can increase the effort on each model to improve thinking, but each estimate below is based on Medium effort across all models.

| Model | Credits | Best for | When to reach for it |
| --- | --- | --- | --- |
| **Fable 5** | $$$$ | The most ambiguous, open-ended analysis | Exploratory work where the question isn't fully defined, complex data investigations, or analyses requiring nuanced reasoning across many variables. Use when getting it right matters more than cost. |
| **Opus 4.7** | $$$ | Complex, multi-step analysis | Building involved queries, debugging tricky logic, structured deep-dives, or analyses with several moving pieces. A strong default when work is complex but doesn't quite need Fable. |
| **GPT 5.5** | $$$ | Complex analysis (alternative to Opus) | Comparable to Opus 4.7 — the right pick often comes down to the task and personal preference. Worth trying both to see which fits your workflow. |
| **Sonnet 4.6** | $$ | Everyday analysis and quick iterations | Writing SQL, summarizing results, light data wrangling, and most day-to-day asks. The best balance of capability and cost for most work. |
| **Kimi 2.7** | $ | Simple, well-defined questions | Quick syntax help, basic transformations, or straightforward lookups. Use when the ask is unambiguous and you just need a fast answer. |

**A note on Fable 5:** Because Fable 5 is part of Anthropic's Mythos class, Anthropic requires a 30-day retention window on all prompts and outputs for safety review. You must [enable data retention](/docs/trust/ai-data-privacy#model-data-retention-settings) in Hex to use Fable 5.

### How to think about effort within a model[​](#how-to-think-about-effort-within-a-model "Direct link to How to think about effort within a model")

The guidance above assumes medium effort, which is the default for most tasks. Lower effort is faster and cheaper but may miss nuance; higher effort can improve results on harder problems but increases cost meaningfully — sometimes enough to make a smaller model at high effort more expensive than a larger model at medium. When in doubt, start at medium and adjust based on the result.

Analytical questions that look simple sometimes aren't — a tidy-looking dataset can hide messy logic underneath. If an answer feels shallow or off, try increasing the effort or moving up a model tier; the question may have needed more reasoning than it appeared.

You can adjust the effort for the model you've chosen in the model picker. For guidance on how each level behaves and when to use it, review the provider's documentation: [Anthropic effort levels](https://platform.claude.com/docs/en/build-with-claude/effort#effort-levels) and [OpenAI reasoning effort](https://developers.openai.com/api/docs/guides/reasoning#reasoning-effort). Kimi 2.7 currently only allows Medium effort.

## Let's talk about Kimi[​](#lets-talk-about-kimi "Direct link to Let's talk about Kimi")

Kimi 2.7 is an open-source model, best known for its lower token costs. In our testing, we found Kimi to be, at times, 1/3rd the cost of frontier models in certain environments.

It's best suited for straightforward analytical questions, especially when they are heavily documented or semantically modeled. It excels in execution but is less capable at judgment — ambiguous problems, cross-domain analysis, nuanced interpretation of results.

When using Kimi, you'll see substantially more thinking messages; don't worry, that's a feature, not a bug. The model is designed to validate its thinking heavily and spends its tokens affirming what it's attempting to do, rather than how (judgment). You also may experience slightly longer thinking times, but not always.

A good mental model is: If a senior analyst would hand the task to a junior with clear instructions, Kimi 2.7 can probably do it cheaper. If they'd want to think through it with a peer, use Opus or GPT.

## Match the model to the ask[​](#match-the-model-to-the-ask "Direct link to Match the model to the ask")

If you're still unsure which model to reach for, think about the shape of the question — not the size of the dataset.

| Model | The kind of ask |
| --- | --- |
| **Fable 5** | "Build me a 12-month forecast from this messy data, then help me write an annual plan with targets GTM leaders should actually care about." Open-ended, high-stakes, and still half-formed. |
| **Opus 4.7** / **GPT 5.5** | "Why are customers dropping out of the conversion funnel, and where should I be paying attention?" Multi-step diagnosis with real judgment calls. Try both and see which one you prefer. |
| **Sonnet 4.6** | "Tell me more about this metric." Everyday analysis, quick iterations, and the questions you ask ten times a week. |
| **Kimi 2.7** | "How many checkouts did we have last week? What did they purchase?" Clear ask, clear answer, no ambiguity required. |

Start in Auto. Move up when the question gets fuzzy. Move down when you already know exactly what you need.

#### On this page

* [How to pick your model](#how-to-pick-your-model)
* [Auto](#auto)
* [Choosing the right model for your task](#choosing-the-right-model-for-your-task)
  + [How to think about effort within a model](#how-to-think-about-effort-within-a-model)
* [Let's talk about Kimi](#lets-talk-about-kimi)
* [Match the model to the ask](#match-the-model-to-the-ask)