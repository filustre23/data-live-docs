On this page

# Workspace setup

Are you just starting to consider how to set up your new Hex workspace? Follow along with this guide and we'll help you think through some of the key considerations for what your team and your company need for their data workflows. If you're looking for more detailed technical descriptions of the settings that are available to you for managing your workspace, check out our Admin 101 guide [here.](/tutorials/quickstart/admin-101)

Key Questions

1. Who are your builders and who are your stakeholders?
2. What are the most common workflows your team(s) will be building?

Take a moment to reflect on these key questions and fill out a couple examples of the workflows that Hex will facilitate. Who are the people who will build those out? Who are the people that will partner with you on project outcomes?

For example…

|  | Builders | Stakeholders |
| --- | --- | --- |
| Workflow #1: Product adoption tracking | Product Analysts | PMs, Eng Leads |
| Workflow #2: Weekly Sales forecasting | Business Analyst | AEs, SDR, Revenue Leadership |
| Workflow #3: Data delivery for clients | Data Analyst | PM, External client |
| … |  |  |

## [User Groups](https://learn.hex.tech/docs/administration/workspace_settings/overview#users--groups)[​](#user-groups "Direct link to user-groups")

Using the above, what are the natural groups of people who’ll have common data and Hex project needs? Create Hex Groups for those!

Remember, if you’re using [Directory Sync](https://learn.hex.tech/docs/administration/workspace_settings/directory-sync), you can use your IdP as your single source of truth for all user role and group membership definitions. We highly recommend this approach for managing your workspace!

**Good to keep in mind:** Groups will govern access to data connections, external file integrations, git repos and packages, and workspace secrets in addition to projects, components, and folders.

For example:

| Group | Who’s included? |
| --- | --- |
| Hex Editors\* | All Hex Editor seats |
| Hex Admins\* | All Hex Admin seats |
| Product Analytics Team | Slice of Editors who are on the Product Analytics team |
| User Funnel Project | Slice of all folks involved in the User Funnel project. Could be Data folks, PMs, Marketing, etc |
| … |  |

\*required groups if you use Directory Sync to make user permissions and group membership!

## The Devil’s in the Data[​](#the-devils-in-the-data "Direct link to The Devil’s in the Data")

Data work depends on having… data.

info

For your most important workflows, where is your data coming from?

Who should have access to it?

Do you have some data sources whose access needs to be highly restricted?

For example: At Hex, our data team has an unfettered connection to our Snowflake warehouse. However, the vast majority of our team only uses a more-curated Snowflake connection that contains “production-ready” data only. These two data connections have different permissions configured at the Snowflake level as well as different Hex User and Group membership.

Use this example table to work through your key data sources and identify which groups of folks should have which levels of access. [Here](https://learn.hex.tech/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions)’s a primer on what these access levels mean!

|  | Can Query | Can View |
| --- | --- | --- |
| Data Source 1: Snowflake Dev | Data Team | Company |
| Data Source 2: Snowflake Prod | Company | Company |
| Data Source 3: Snowflake w/ HR data | Data Team w/ PII permission (via Hex Group) | HR (via Hex Group) |
| … |  |  |

You can move on from data permissions at this point. Or if you’re laser focused on how data can be curated for different types of Hex users come on a **Data Curation** side quest with me…

### Data Curation[​](#data-curation "Direct link to Data Curation")

Those who live in glass houses shouldn’t cast stones… it’s not uncommon for the schema and tables in your data connection to get a little bloated. You don’t necessarily need to burn it all to the ground and start over, but you can add annotations and indicate within Hex which schemas/tables are heavily used/most reliable/etc by endorsing those assets in the [Data browser](https://learn.hex.tech/docs/explore-data/data-browser).

This has *huge* benefits to help less-technical users find and use the best data, but perhaps more importantly, it also makes a world of difference for the quality of experience you can expect when working with [AI agents](/tutorials/ai-best-practices/setup-for-ai-agents).

info

Check out this blog post on the various ways you can curate your data for different use cases:

<https://hex.tech/blog/curate-workspace-for-explore/>

# Asset Curation

So you’ve set up your user Groups, defined what data they can use, and now your creators are building Hex projects left and right! But how does everything stay organized?!

Individual creators need an easy way to write one-off projects and do their EDA or scratchpad work. But how do you mix that flexibility with more structure for data work that needs to be circulated more widely?

At Hex we orient around **Teams and Themes** as the scaffolding to guide workspace organization.

**Teams** - Groups of folks within the same Team that have common mandates and goals (e.g. Data Team, Sales Team)

**Themes** - Represent an area of focus or a cross functional initiative (e.g. user activation or feature usage).

info

Refer back to your chart for the most common workflows in Hex and the builders/stakeholders of those. Can you use that to zoom out and identify the Teams and Themes most relevant to your company?

## [Folders](/docs/organize-content/folders)[​](#folders "Direct link to folders")

Folders group related projects and components and share them with one permission. A project lives in one folder. Everyone with access to the folder gets that folder's permission on every project and component inside it.

At Hex we use folders for both Teams and Themes:

* Team folders: These hold high-level dashboards, reports that track key metrics, and apps that support the everyday operational needs of the team. We use Hex [groups](https://learn.hex.tech/docs/administration/workspace_settings/overview#groups) to ensure the right people have access to their team folder. A team folder acts as a home in Hex for a particular team.
* Theme folders: These hold projects with more cross-functional stakeholders. Access can be open to the entire workspace, or restricted to specific groups depending on the sensitivity of the data.

A project can only live in one folder. When a project belongs to both a team and a theme, put it in the team folder and use [categories](https://learn.hex.tech/docs/organize-content/statuses-categories) for the theme.

## Categories[​](#categories "Direct link to Categories")

[Categories](https://learn.hex.tech/docs/organize-content/statuses-categories) are labels that can be applied at the project-level. A project can have more than one category!

We see the most success when categories match the teams and themes you organize around. This makes discovery easier with [Workspace Search](https://learn.hex.tech/docs/organize-content/workspace-search) and when navigating through projects in the bulk Project view.

Additionally, you can include categories that denote things like:

* the type of analysis in the project/component (e.g., "Model Development," "Static Dashboard," "Deep Dive," "A/B Test")
* data classifications (e.g., 'Internal Only', 'Experimental', 'Confidential', "PII")

# Project lifecycle

The last piece of this puzzle is planning for how things change!

A common pattern is starting data work in “development”. Work in this stage should be shared only with the immediate team of analysts. Once the work is deemed “good” it then gets promoted to “production”. Use [Statuses](https://learn.hex.tech/docs/organize-content/statuses-categories) to label projects accordingly.

### Endorsed Statuses + Reviews[​](#endorsed-statuses--reviews "Direct link to Endorsed Statuses + Reviews")

So how can you manage the natural evolution from dev to prod? Hex has the concept of an “[Endorsed status](/docs/organize-content/statuses-categories#endorsed-statuses)” to indicate which projects have reached the lofty goal of being ‘trusted’. Our [Review](/docs/collaborate/reviews) process can also be used in this process (either optionally or by [requirement](/docs/collaborate/reviews#required-reviews)) to make sure the right eyes are reviewing work before it goes out to the whole company!

For example:

* Specify that a piece of content-- projects, components, data connections-- can be trusted with an Endorsed status (e.g., "Trusted," "Reviewed," "Approved," "Prioritized")
* If desired, for content that's mission critical (e.g., a project that's company-wide) or to which changes would have big impacts (e.g., a component imported into many projects), require a review to apply an Endorsed status.

info

What are the phases of your data projects and their circulation that you can mirror as Hex statuses? Which should be considered Endorsed? Which might you want to gate behind a required Review?

You can also move projects between folders to mirror these different phases of the data lifecycle. Projects might start in a Dev folder and move into a Prod folder once approved.

Required reviews can be used as gates to ensure that the content of the Hex project is accurate and reliable, and that projects follow your team's lifecycle. For example, you could require that a project is in the appropriate folder, and without that, the review is not approved.

For example...

|  |  | Endorsed? | Require reviews? |
| --- | --- | --- | --- |
| WIP | Projects that are not yet ready for prime time. |  |  |
| Ad hoc | One-off analyses that might never see the “stamp of approval” to become production apps. |  |  |
| Trusted | Analyses based on trusted data that other users can rely on to be accurate. | ✅ |  |
| Production | Trusted, verified, and approved data insights that the entire team can count on. | ✅ | ✅ |

### [Archiving](https://learn.hex.tech/docs/organize-content/archive)[​](#archiving "Direct link to archiving")

Clean up cruft in your workspace by turning on Auto Archiving! Individual scratchpads are a critical piece of how developers work with data. But let’s not leave those lying about once they’re not needed! You can configure thresholds for how recently a project has been viewed or edited and automatically archive those so that they don’t clutter up your workspace.

### Birds eye view[​](#birds-eye-view "Direct link to Birds eye view")

But how can you, an Admin in your workspace, see if the processes you’ve painstakingly outlined are being followed?

Hex has a swiss-army-knife view of all of your workspace projects in the “Projects” tab of your homepage. From here you can filter projects by a ton of different attributes an also make [bulk changes](https://learn.hex.tech/docs/organize-content/organize-projects).

If you want to build more data-driven ways to curate your projects, check out the `ListProjects` [API endpoint](/docs/api-integrations/api/overview). With this endpoint you can filter through and identify projects that aren’t adhering to your internal best practices (e.g. published projects with a certain status/category that aren’t included in a category) so that you can audit adherence and touch base with folks as needed.

#### On this page

* [User Groups](#user-groups)
* [The Devil’s in the Data](#the-devils-in-the-data)
  + [Data Curation](#data-curation)
* [Folders](#folders)
* [Categories](#categories)
  + [Endorsed Statuses + Reviews](#endorsed-statuses--reviews)
  + [Archiving](#archiving)
  + [Birds eye view](#birds-eye-view)