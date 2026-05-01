On this page

# Archive

Archive projects to declutter a workspace and improve search results.

The Archive provides a way to keep past content in a workspace, without having it appear on the home page.

When archived:

* Projects will not show up on the home page, and instead will appear on the **Archive** page (above)
* Projects can be easily excluded from [workspace search](/docs/organize-content/workspace-search) via the **Include archived** toggle
* Any scheduled runs on an archived project will be disabled
* The project will show a banner indicating it is archived
* The project cannot be edited further unless [unarchived](#unarchiving).

## Auto-archive[​](#auto-archive "Direct link to Auto-archive")

info

* Auto-archiving is available on the **Team** and **Enterprise** [plans](https://hex.tech/pricing/).
* Users will need the Admin role to set up auto-archive rules.

Admins can set up rules to automatically archive projects, based on when a project was last **edited**, or last **viewed**.

* **Edited** is defined as any changes made to the Notebook side of a project.
* **Viewed** is defined as:
  + any visit to the published app for ***projects that are published.***
  + any changes made to the Notebook for ***unpublished projects.***

To configure these settings, head to **Settings**, then **Organization**.

tip

Projects in a [Collection](/docs/organize-content/collections), and [components](/docs/explore-data/components) are never auto-archived.

When a project is archived due to an auto-archive rule, users with **Full access** permissions will be notified via a daily summary email.

## Manual archive[​](#manual-archive "Direct link to Manual archive")

info

* Manual archiving and unarchiving is available on all plans.
* Users will need the Admin or Manager role, or **Full access** project permissions to manually archive a project or component.

Multiple projects can be archived at once on the Projects page, by selecting projects and then choosing the **Archive** action. [Learn more](/docs/organize-content/organize-projects).

Projects can be individually archived via the dropdown menu next to the project title, or the three-dot menu on the home page.

## Unarchiving[​](#unarchiving "Direct link to Unarchiving")

info

* Manual archiving and unarchiving is available on all plans.
* Users will need the Admin or Manager role, or **Full access** project permissions to unarchive a project or component.

Projects and components can be restored from the archive by:

* Selecting projects on the **Archive** page and choosing to **Unarchive**
* Visiting the project or component directly, via the **Unarchive** button in the banner.

If a project has been manually unarchived, it will not be included in future auto-archive jobs.

## FAQs[​](#faqs "Direct link to FAQs")

### How can I prevent projects from being auto-archived?[​](#how-can-i-prevent-projects-from-being-auto-archived "Direct link to How can I prevent projects from being auto-archived?")

Projects in a Collection are never auto-archived. Further, any project that has been unarchived will not be included in future auto-archive jobs.

### What happens if both rules are configured?[​](#what-happens-if-both-rules-are-configured "Direct link to What happens if both rules are configured?")

If both rules are configured, *both* criteria must be met for a project to be archived. For unpublished projects, the criteria for both settings is the same—a project is archived based on the last update to the Notebook. Therefore, the setting with the greater value is applied.

### Do auto-archive rules apply to components?[​](#do-auto-archive-rules-apply-to-components "Direct link to Do auto-archive rules apply to components?")

Components can only be manually archived, and will not be affected by auto-archive rules.

### Can projects use an archived component?[​](#can-projects-use-an-archived-component "Direct link to Can projects use an archived component?")

When a component is archived, it will no longer appear in the list of available components when importing a component to a project.

However, any existing projects that use the archived component will continue to work as expected.

#### On this page

* [Auto-archive](#auto-archive)
* [Manual archive](#manual-archive)
* [Unarchiving](#unarchiving)
* [FAQs](#faqs)
  + [How can I prevent projects from being auto-archived?](#how-can-i-prevent-projects-from-being-auto-archived)
  + [What happens if both rules are configured?](#what-happens-if-both-rules-are-configured)
  + [Do auto-archive rules apply to components?](#do-auto-archive-rules-apply-to-components)
  + [Can projects use an archived component?](#can-projects-use-an-archived-component)