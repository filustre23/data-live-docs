On this page

# Threads best practices

This guide is designed to help you get the most out of Threads. Threads answers questions about your data in plain language, supports follow-up questions so you can go deeper, and helps you move from curiosity to actionable insight.

You've probably opened Threads, stared at a blank prompt box, and thought: "What do I even ask?"

It's a fair question. For years, we've been trained to ask for dashboards, not answers. We learned to speak in the language of filters and drill-downs because that's what the tools understood. But Threads works differently. It's built to handle the messy, exploratory questions you'd normally save for an analyst — the ones that start with "I need to understand..." and spiral into three follow-ups you didn't know you needed.

This guide isn't about perfect prompts. It's about building a conversation with your data that actually gets you somewhere. We'll walk through how to structure your first question, what makes a strong follow-up, and how to navigate the inevitable rabbit hole without losing track of what you're trying to learn.

Whether you're investigating churn, forecasting sales, or validating a hunch about user behavior, this is how you get Threads working for you.

## The prompt template[​](#the-prompt-template "Direct link to The prompt template")

Every strong Threads prompt has three parts: **Task + Question + Parameters**

Think of it like giving directions to someone helping you with a project. You wouldn't just say "sales stuff" — you'd tell them what you're trying to accomplish, what specifically you need to know, and any important constraints or context.

### Task[​](#task "Direct link to Task")

**What it is:** What you're asking Threads to do for you. This grounds the agent instead of forcing it to guess your intent.

**Examples:**

* "I want you to build me a forecast model"
* "I want you to help me understand customer churn"
* "I want you to help me segment users based on activity"

### Question[​](#question "Direct link to Question")

**What it is:** The specific insight you're looking to extract. This is the core of your output and should tie to an action you're planning to take based on the answer.

**Examples:**

* "Based on the last two quarters, what should we forecast sales performance to be next quarter?"
* "What is causing most of our mid-market customers to churn?"
* "What segments are driving the highest engagement with our new AI features?"

### Parameters[​](#parameters "Direct link to Parameters")

**What it is:** The filters, limitations, or conditions you want applied to the response. Every question has caveats — dates, geographies, exclusions — and the agent needs to understand yours to give you the best answer.

**Examples:**

* "I only want to forecast US sales teams"
* "Ignore objections like 'went out of business' or 'was acquired' — I want to learn specifically about churn reasons related to product performance or price, but include anything else that might be interesting"
* "We launched our AI features in Q3 of 2025, so when we look at improved engagement, use the period prior as a baseline"

**Putting it together:**

> Task: I want you to help me understand customer churn.
>
> Question: What is causing most of our mid-market customers to churn?
>
> Parameters: Ignore objections like "went out of business" or "was acquired" — I want to learn specifically about churn reasons related to product performance or price, but include anything else that might be interesting.

## When you don't know where to start[​](#when-you-dont-know-where-to-start "Direct link to When you don't know where to start")

Not every conversation begins with a clear question. Sometimes you're exploring a new area of the business, or you're not sure what data even exists to answer what you're trying to understand.

If you're starting from scratch, you can ask Threads to map out what's available before you commit to a specific question.

**Ask: "What data do you have that can help me investigate [topic]?"**

**Examples:**

* "I want to investigate assembly line performance. What kind of data do you have that can help me do that?"
* "What customer support data is available to analyze ticket resolution times?"
* "I'm trying to understand user onboarding. What data exists around new user behavior in the first 30 days?"

Threads will describe what's accessible — tables, metrics, fields — which can help you refine your actual question or discover data sources you didn't know about. Once you see what's available, you can craft a more targeted prompt using the Task + Question + Parameters structure.

## The follow-ups (where the real work happens)[​](#the-follow-ups-where-the-real-work-happens "Direct link to The follow-ups (where the real work happens)")

Your first question sets the stage. The follow-ups are where you actually learn something.

In the past, the feedback loop between question and follow-up took days — a Slack message, a ticket, waiting for someone's queue to clear. With Threads, it's instant. But knowing *what* to ask next, and how those follow-ups help you validate the agent's response, is what separates surface-level exploration from genuine insight.

Here are the follow-up patterns that work.

### "How did you calculate that?"[​](#how-did-you-calculate-that "Direct link to \"How did you calculate that?\"")

This ensures you understand exactly how the agent arrived at an answer and whether you agree with it. More importantly, it lets you share the reasoning with your data team for validation.

Asking this about one specific part of the response also helps you understand what context Threads is using. If something was calculated incorrectly or the method doesn't make sense, it's a strong signal to loop in your data team for clarification or improvement.

**Examples:**

* "How did you calculate churn? Where did you get that definition?"
* "How are you segmenting users?"
* "Where does it say that US customers are defined this way?"

### "What does this look like separated by [dimension]?"[​](#what-does-this-look-like-separated-by-dimension "Direct link to \"What does this look like separated by [dimension]?\"")

Aggregated views are easy, but they hide interesting insights. Unless you specify otherwise, Threads will often give you a rolled-up answer. Breaking results down by a dimension is the fastest way to find signal in the noise.

**Examples:**

* "Show me churn broken down by customer segment"
* "Show me AI feature engagement for new users only"

The dimensions you use will vary based on what you're investigating:

**Product:**

* Feature grouping, device type, browser, version number

**Sales & Marketing:**

* Channel, customer segment, plan tier, attribution source

**Customer Success & Support:**

* Support tier, configuration or datacenter, user age (new vs. existing), user role (admin vs. non-admin)

**Finance:**

* Department, geography, budget category

### "Why did we see a spike in [metric] in [time period]?"[​](#why-did-we-see-a-spike-in-metric-in-time-period "Direct link to \"Why did we see a spike in [metric] in [time period]?\"")

The first question triggers a response. The natural next question is "why?" — so ask it. If you've noticed something interesting, or the agent called out an anomaly or outlier, now you have the opportunity to dig into it in real time.

**Example:**

If your first prompt was:

> I want you to help me prepare for a quarterly roadmap review for AI features. What AI features are driving the highest adoption in our product over the past quarter? I want to look specifically at new users vs. existing, and adoption should be measured by daily retention.

And Threads responds indicating that engagement for new users is 10% lower than existing users, you can dig into why with a follow-up like:

> Why are new users engaging less often with AI features? Is this happening over a specific period or with certain types of new users?

## Navigating the rabbit hole[​](#navigating-the-rabbit-hole "Direct link to Navigating the rabbit hole")

Welcome to the rabbit hole — where analysts spend most of their time.

You've asked a first question, then a strong follow-up, and another, and another. Now you've forgotten where you started, what you're even doing here, and possibly your own name. It's fine. We've all been there, and coming up for air is something Threads can actually help with.

**When you've gone 2–3 follow-ups deep, pause and ask Threads to summarize your conversation.** Remind you where you started and what the original goal was. Then reassess: Has your initial question been answered? Do you have an actionable insight?

Ask yourself: "I've learned X, Y, Z from this Thread. Do I know what action I can take?"

If yes — great. Ask Threads to:

> Summarize these insights with the intent to [take specific action], and use this conversation as the evidence or context to support my recommendation.

If you're still unsure — that's also fine. You've explored the data, tested hypotheses, iterated through responses. You can either:

1. **Keep exploring:** Continue with more follow-ups, noting to Threads that you're stuck or uncertain. That might look like: "I'm a bit stuck — what other questions would help me understand the impact of our new feature on new user adoption?"
2. **Engage your data team:** Share your Thread with them in Slack or a direct message. What we love about this approach is that the data team now has full context into what you were investigating and can deliver a more targeted recommendation, shortening your time to insight.

## A real example[​](#a-real-example "Direct link to A real example")

A member of our Marketing team recently used Threads to quantify the impact of a campaign promoting a new Hex feature. Standard stuff.

In the past, this workflow would have started with bouncing between dashboards, then a quick Slack to our data team for help. But honestly? They probably wouldn't have asked. They needed to move fast on this campaign, and taking action felt more urgent than deep investigation.

They knew anecdotally that the feature was well-liked, and adoption dashboards showed positive trends. The team member wanted to validate that the value she *believed* was there — and to what degree.

**The original prompt:**

> I want to understand the impact of an organization adopting [feature]. I want to see it across expansion, user growth, retention specifically for new users, and avg messages per user sent to [feature]. Ignore system responses for now.

The agent responded with statistics on strong net expansion and new-user adoption — nearly 30% higher than for users who didn't engage with the feature. It used a calculation for "net expansion" but didn't clearly explain how it was calculated. Anything to do with expansion should be vetted, so they wanted to clarify the logic.

**The follow up prompt:**

> For number 1, explain how you calculated net expansion.

Threads gave its logic and cited our semantic model as the source. Now that it was trusted as a quality insight, they wanted to see if this trend held across customer segments.

**The next follow up prompt:**

> Do we see this consistent across customer segments?

Threads responded with a resounding yes. In fact, some segments that *didn't* engage with the feature saw negative expansion. This meant the feature was especially valuable — maybe even worth a larger marketing strategy to drive adoption and awareness.

**The final prompt:**

> I want to craft a marketing strategy positioning Hex as the AI analytics platform, and these findings help me demonstrate that [feature] adoption is a net positive across the board. Can you summarize these insights into 3–5 executive bullet points I can include in my report and research? Also flag anything else from these findings that would help me.

Now they have a polished value proposition for the marketing campaign and a strong case to make it bigger than initially planned. Super Bowl ad? Maybe not. But certainly high ROI.

## Final thoughts[​](#final-thoughts "Direct link to Final thoughts")

Threads won't replace your judgment or your data team. It won't know your business context better than you do. But it will give you the ability to ask follow-up questions in real time, validate your hunches faster, and spend less time waiting for someone else to translate your curiosity into SQL.

The prompts in this guide aren't rules — they're patterns. Use them as starting points, adjust them to fit how you think, and don't be afraid to get messy with your questions. The goal isn't perfection. It's momentum.

Start with a clear task, ask a specific question, add your parameters, and then follow the thread wherever it leads. You'll know you're done when you have something you can act on — or when you realize you need to bring someone else in to help.

Either way, you'll get there faster than you used to.

#### On this page

* [The prompt template](#the-prompt-template)
  + [Task](#task)
  + [Question](#question)
  + [Parameters](#parameters)
* [When you don't know where to start](#when-you-dont-know-where-to-start)
* [The follow-ups (where the real work happens)](#the-follow-ups-where-the-real-work-happens)
  + ["How did you calculate that?"](#how-did-you-calculate-that)
  + ["What does this look like separated by [dimension]?"](#what-does-this-look-like-separated-by-dimension)
  + ["Why did we see a spike in [metric] in [time period]?"](#why-did-we-see-a-spike-in-metric-in-time-period)
* [Navigating the rabbit hole](#navigating-the-rabbit-hole)
* [A real example](#a-real-example)
* [Final thoughts](#final-thoughts)