On this page

# Notebook Agent best practices

This guide is designed to help you get the most out of the [Hex Notebook Agent](https://learn.hex.tech/docs/explore-data/notebook-view/notebook-agent). The agent can generate and edit cells directly in your notebook, and it can also act as a thought partner that explains, summarizes, and guides.

[](/assets/medias/full-agent-demo-be1018e554ab587b0fdb09010ead4f6b.mp4)

## Introduction[​](#introduction "Direct link to Introduction")

The Notebook Agent isn't just another chatbot, it's specifically designed for assisting with data work. There are four key capabilities:

1. **Agentic search**: It can help you discover the right data sources without you having to remember exact table names or schemas, whether that be a semantic model or a specific table. It can also search Hex docs (like this one!), and pretty soon it's going to be able to search other elements in the Hex ecosystem: other projects, components, and more.
2. **Building a plan**: It translates your business questions into a structured analytical approach.
3. **Executing analysis**: It writes and runs code to transform, visualize, and analyze your data.
4. **Summarizing results**: It explains insights in plain language anyone can understand.

The agent acts like a seasoned data analyst sitting next to you, ready to collaborate on everything from quick exploratory analysis to complex predictive modeling.

This guide outlines patterns that have proven effective for getting the most out of the Notebook Agent. Nothing here is set in stone or universally applicable; think of these as starting points! We encourage you to experiment and adapt them to your own workflows.

## Mental models for working with the notebook agent[​](#mental-models-for-working-with-the-notebook-agent "Direct link to Mental models for working with the notebook agent")

### Structured thinking[​](#structured-thinking "Direct link to Structured thinking")

You don't need to be overly explicit in your prompts, but the more specific you are the better. One approach is using clear structures that break down context, tasks, guidelines, and constraints:

Template:

```
Context: You are analyzing [dataset description] to help [business objective].  
Task: Perform [specific analysis type] to determine [specific question].  
Guidelines: Use [techniques/methods/packages], focus on [key metrics/variables].  
Constraints: The analysis must [limitations/requirements], avoid [pitfalls/assumptions].
```

Example:

```
Context: You are analyzing customer transaction data to help improve marketing targeting.  
Task: Perform k-means clustering to segment customers based on purchasing behavior.  
Guidelines: Use Python's scikit-learn, evaluate different numbers of clusters (2-10), and visualize the results with dimensionality reduction.  
Constraints: Handle missing values appropriately, normalize features before clustering, and provide business interpretations for each identified segment.
```

### Conversational prompting[​](#conversational-prompting "Direct link to Conversational prompting")

Most of the time, though, you'll prompt the Notebook Agent kind of like how you'd send a DM to a peer. That's perfectly fine, and is how we prompt most of the time, but notice that the spirit of the structure outlined above is included in the prompt below.

```
I'm looking at our customer transaction data and want to improve our marketing targeting. Could you help me segment our customers based on their purchasing behavior? I'd like to use k-means clustering for this. Use scikit-learn to implement the clustering. Try different cluster counts (between 2-10) to find the optimal number. Make sure to handle any missing values in the dataset appropriately, and normalize the features before running the clustering algorithm.
```

### Meta prompting[​](#meta-prompting "Direct link to Meta prompting")

One of the biggest unlocks for successful prompting is using the agent to craft a concrete plan, then feeding that plan with your refinement back to the agent for execution. With complex multi-step analyses, agents are prone to getting lost in all the steps in front of it. Building a plan and executing it step-by-step helps the agent focus on the task at hand, and gives you an opportunity to critique/refine the approach as results stream in.

Building the plan:

```
I need to analyze customer churn for our subscription service. What data variables should I include, and what analytical approach would be most appropriate? Can you outline a step-by-step plan for this analysis?
```

Response from the agent:

```
1. Exploratory Data Analysis  
Churn rate trends over time, by segment, and by cohort  
Feature correlation analysis and usage pattern identification  
  
2. Feature Engineering  
Create recency/frequency metrics, usage velocity changes  
Rolling averages for engagement, days-to-churn calculations  
  
3. Predictive Modeling  
Logistic regression for interpretability, random forest for feature importance  
Time-to-churn survival analysis for more nuanced insights  
  
4. Actionable Segmentation  
Risk scoring (high/medium/low churn probability)  
Intervention timing recommendations
```

Executing the plan:

```
Great, let's proceed with the first step:  
Exploratory Data Analysis  
Churn rate trends over time, by segment, and by cohort  
Feature correlation analysis and usage pattern identification
```

### Scope context, be specific[​](#scope-context-be-specific "Direct link to Scope context, be specific")

In a vacuum, the prompt is important, but we intentionally built the Notebook Agent to be deeply integrated with Hex's environment. That means you can scope context deliberately, like which tables and dataframes to use, which cells to edit or which docs to reference. Scoping context helps the agent focus on the right stuff. When you know what data you need, @ tag the relevant table:

@ tagging data:

```
"Analyze the [@customer_transactions] table, focusing on the relationship between 'purchase_frequency' and 'customer_lifetime_value' columns."
```

@ tagging cells:

```
[@Prophet Model Components Analysis] Edit this cell where we define the parameters of the Prophet model so it prioritizes the recent explosive growth we saw in the past 6 months  
## Mindset
```

### Specify analysis methods[​](#specify-analysis-methods "Direct link to Specify analysis methods")

If you know the exact approach you want to take in an analysis, clearly state the analytical techniques, models, or packages you want to use. Remember, you don't need to know everything. If you want suggestions, just ask the model for its advice first, then narrow down the plan.

```
Build a random forest classifier to predict customer churn, using feature importance to identify the top factors contributing to churn.
```

Treat the agent as a partner, not a replacement. You are the manager of its work! The most effective way to use it is to start broad, get a first draft, and then refine. Always validate the outputs the same way you would review a teammate's SQL or Python.

### Provide context for business impact[​](#provide-context-for-business-impact "Direct link to Provide context for business impact")

The agent can help you reason about actionable next steps that your stakeholders and decision makers really want to know.

```
Analyze marketing channel ROI to determine which channels to increase investment in for our Q4 campaign planning. Consider both acquisition cost and customer lifetime value by channel.
```

### Getting advice and helping you learn[​](#getting-advice-and-helping-you-learn "Direct link to Getting advice and helping you learn")

The agent is basically an expert analyst/data scientist that knows industry standard analytical and data science techniques. Often times, you might want to start by asking the agent to suggest some approaches on a type of analysis, or explain how some technique works. Treat the agent like a knowledgeable peer; it's eager to help you learn while you're building.

```
[@Prophet Model Components Analysis] Can you describe what each of these configs/parameters in this Prophet model do?
```

## How data practitioners use the agent[​](#how-data-practitioners-use-the-agent "Direct link to How data practitioners use the agent")

There are two common patterns for working with the Notebook Agent. You can combine them fluidly depending on your needs.

**Agentic Data Work:** Have the agent generate or edit SQL, Python, and Markdown. Example: *"Write a query that calculates weekly active users, filtered to the last 30 days, and add a chart."*

**Thought Partner:** Ask the agent to explain or summarize work, or propose next steps. If you explicitly want the agent to avoid creating cells, mention that in the prompt.
Examples:

* "Explain this SQL query in plain language."
* "Can you suggest three ways to validate the results of this analysis?"
* "What features should I add into this data app in the next iteration given my stakeholders' goals of XYZ?"

## Clear and specific prompts[​](#clear-and-specific-prompts "Direct link to Clear and specific prompts")

The more specific you are, the better the agent will perform!

❌ Less effective: *"Analyze our customer data."*

✅ More effective: *"Analyze our customer data from the last 30 days using the orders and customers tables. Focus on churn by product tier and highlight anomalies."*

**💡Tip:** You can reference specific cells in your notebook with @ mentions.
For example: *"Using the results from cell\_name, calculate churn rate by week
and visualize it as a line chart."* Referencing cell names or data frames helps
the agent know exactly what to look at! If you select the cell, you can
autocomplete the reference by tabbing.

[](/assets/medias/tag-cells-bb9fbf8452aa5aa4321f835a3a760069.mp4)

## Reviewing changes[​](#reviewing-changes "Direct link to Reviewing changes")

All changes the agent makes are highlighted with a diff view that you need to keep or undo. A set of changes can be confirmed all together, or kept one cell at a time. While changes are proposed in the diff view, you can edit the contents directly and rerun the output to make tweaks before keeping the changes.

If you ask a follow-up question without confirming your changes, changes will be
stacked and left in a pending state until keeping. We recommend keeping changes
as soon as you're happy with them and not letting changes stack up too long. If
you don't want to keep the changes, you can undo them cell by cell or undo all.

[](/assets/medias/undo-changes-567a62e35d891085f4c7760025dfe075.mp4)

## Iterative refinement[​](#iterative-refinement "Direct link to Iterative refinement")

The agent works best in an iterative loop. Start with a high-level ask, check the output, then refine. Ask for alternatives before committing. Example: "Propose three approaches for analyzing retention." Then pick one: "Use option #2 and filter to users who joined in the last 90 days." Then refine: "Add comments to the SQL and create a bar chart of monthly cohorts."

## Managing query costs[​](#managing-query-costs "Direct link to Managing query costs")

The agent can run queries directly on your warehouse just like a human Hex user. We recommend scoping queries to avoid unnecessary costs. Apply time filters and row limits up front. Start with small samples until the shape looks right, then expand. Document expensive tables in the warehouse with descriptions like "always filter to the last 30 days" so the agent has guidance.

## Using metadata and rules[​](#using-metadata-and-rules "Direct link to Using metadata and rules")

The agent performs better when the environment is well documented and it has
access to data that is **clean, curated, and contextual**. Add table and column
descriptions in the [Data Browser](/docs/explore-data/data-browser) so it
knows the grain, keys, and intended use. Encode defaults in your Hex rules file,
such as standard filters, naming conventions, and details about your business
and data models. These help the agent remember your preferences across tasks!

For a full guide, see [Workspace context best practices](/tutorials/ai-best-practices/workspace-context-best-practices).

## Session management[​](#session-management "Direct link to Session management")

We recommend keeping threads focused on a single task, and for new topics [start
a new thread](/docs/explore-data/notebook-view/notebook-agent#start-a-new-thread). As threads get longer, it
can cause quality of responses to degrade, so whenever you have a new question,
start a new thread. You also have a version saved on every new thread, making it
easy to trace back in time if you don't like the output of a session.

[](/assets/medias/autosaving-versions-81fe911b741133175d9ad7481d6c44b1.mp4)

## Context window and compression[​](#context-window-and-compression "Direct link to Context window and compression")

The agent automatically summarizes the conversation when about 70% of the [context window](https://docs.anthropic.com/en/docs/build-with-claude/context-windows) is reached. While you can technically continue a very long conversation without hitting a hard stop, we recommend periodically starting a new thread when you begin a new or major analysis step. This helps preserve clarity and ensures the agent has the right context to work with.

## Reviewing and trust[​](#reviewing-and-trust "Direct link to Reviewing and trust")

Do not blindly trust outputs; always read the SQL or Python before relying on it! Reproduce results with a smaller sample or a secondary check. Ask the agent to explain assumptions or summarize risks. If something looks off, tell it exactly what and why, then re-prompt for a fix.

## FAQ[​](#faq "Direct link to FAQ")

**Can the agent run queries on my warehouse?**

* Yes!

**Who can use the notebook agent?**

* Editors+ roles in Hex have access to the notebook agent.

**Can I prevent the agent from writing code / keep it in thought partner mode?**

* Yes. Ask for a plan first: *"Outline your approach before creating cells."* or explicitly tell the agent you only want to brainstorm, not create.

**What if the agent makes a mistake?**

* Delete or undo the cell, re-prompt with specifics, and validate outputs before using them.

**How do I provide feedback on the agent?**

* After the agent generates a response, you will see a 👍👎 - providing feedback is very useful for improving performance.

#### On this page

* [Introduction](#introduction)
* [Mental models for working with the notebook agent](#mental-models-for-working-with-the-notebook-agent)
  + [Structured thinking](#structured-thinking)
  + [Conversational prompting](#conversational-prompting)
  + [Meta prompting](#meta-prompting)
  + [Scope context, be specific](#scope-context-be-specific)
  + [Specify analysis methods](#specify-analysis-methods)
  + [Provide context for business impact](#provide-context-for-business-impact)
  + [Getting advice and helping you learn](#getting-advice-and-helping-you-learn)
* [How data practitioners use the agent](#how-data-practitioners-use-the-agent)
* [Clear and specific prompts](#clear-and-specific-prompts)
* [Reviewing changes](#reviewing-changes)
* [Iterative refinement](#iterative-refinement)
* [Managing query costs](#managing-query-costs)
* [Using metadata and rules](#using-metadata-and-rules)
* [Session management](#session-management)
* [Context window and compression](#context-window-and-compression)
* [Reviewing and trust](#reviewing-and-trust)
* [FAQ](#faq)