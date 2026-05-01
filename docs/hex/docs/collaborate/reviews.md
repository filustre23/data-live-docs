On this page

# Reviews

Protect business-critical projects with required reviews, or request a review whenever you want a second pair of eyes.

When publishing changes to a project, editors can request a review from another user. Reviewers can then provide feedback in comments, and approve, or request changes before a new version is published.

info

* Reviews are available on the Team and Enterprise [plans](https://hex.tech/pricing).
* Users will need **Can edit** or higher project permissions to create a review request, and to publish a project once a review has been approved.
* Users will need **Full access** project permissions to require reviews for a project.
* Users will need **Can explore** or higher project permissions to leave a review.

## Requesting a review[​](#requesting-a-review "Direct link to Requesting a review")

### Creating a review request[​](#creating-a-review-request "Direct link to Creating a review request")

After clicking **Publish** in a notebook, click **Request review** in the bottom right of the publish modal. For projects that [require reviews](#marking-a-project-as-requiring-reviews), this is a necessary step before publishing.

Include a title for the changes you are requesting a review for, and optionally a description to let your reviewer(s) know why you are requesting a review.

### Adding reviewers[​](#adding-reviewers "Direct link to Adding reviewers")

A review request can have multiple reviewers. Use the **Add +** button to search for users or groups to request a review from. Once you click **Open publish request**, each user will be notified that you have requested a review from them. A reviewer must have [Can Explore](/docs/collaborate/sharing-and-permissions/project-sharing#can-explore) access to the project in order to review it. If you request a review from a user that does not already have access to the project, they will be granted Can Explore access once you open the publish request.

After opening the review request, the review must be marked as "approved" in order to publish the proposed changes. Read more about how a project can be marked as "approved" [below](#understanding-review-request-states).

## Leaving a review[​](#leaving-a-review "Direct link to Leaving a review")

As a reviewer, you have the option to comment, approve, or request changes on the review. You can also leave comments on individual cells as part of their review for more fine-grained feedback.

**Comment** allows the reviewer to add feedback without giving explicit approval. **Approve** marks the review as "approved". **Request changes** will prevent the review from being marked as "approved" until that reviewer has changed their review determination. More on this [below](#understanding-review-request-states).

A feed of review activity can be found in the review modal.

## Addressing requested changes[​](#addressing-requested-changes "Direct link to Addressing requested changes")

To address any changes requested by a reviewer, edit the draft, then add the changes to the review request via the below button.

tip

Changes made to the draft while a review is in progress will not be added to the review request automatically, in order to prevent unreviewed changes being published.

To notify the reviewer that their feedback has been addressed and changes have been added to the review, click the circular arrows icon next to the reviewers name. This will re-request their review on the project.

## Resolving a review request[​](#resolving-a-review-request "Direct link to Resolving a review request")

### Understanding review request states[​](#understanding-review-request-states "Direct link to Understanding review request states")

The review request will be marked as either **Pending**, **Changes Requested**, or **Approved** based on each reviewer's determination. You can see the current state in the publish modal next to the **Publish** button.

* **Pending approval**: Reviewers have either not yet left a review, or have only commented on the changes.
* **Changes requested**: If any reviewer has requested changes, the review will be marked with "Changes requested". The review request will not be marked as "Request approved" until the reviewer who requested changes updates their review determination. More on addressing changes [above](#addressing-requested-changes).
* **Request approved**: At least one user has approved the request, and no users are requesting changes. It is now possible to publish the project.

### Publishing changes[​](#publishing-changes "Direct link to Publishing changes")

Once a review request is in the **Request approved** state, the **Publish** button will become enabled and it will be possible to publish the approved changes.

If the review has not yet been approved, the **Publish** button will be greyed out. If the review is not [required](#marking-a-project-as-requiring-reviews), you can override the review request and publish without approval by clicking the down arrow next to the **Publish** button.

## Required reviews[​](#required-reviews "Direct link to Required reviews")

Reviews can be required on a project via one of two mechanisms:

* **Configured per project**: Users with [Full Access](/docs/collaborate/sharing-and-permissions/project-sharing#full-access) to a project can require that changes are reviewed and approved before they can be published.
* **Statuses**: Admins and Managers can apply a [status](/docs/organize-content/statuses-categories) that enforces reviews to a project. Once applied, all subsequent changes will need to be reviewed before publishing.

The review outcomes are the same as [optional reviews](#understanding-review-request-states).

However, unlike optional reviews, where any user with **Full access** can publish without approval, only Admins can publish without approval when reviews are required.

## FAQ[​](#faq "Direct link to FAQ")

#### Who can request a review?[​](#who-can-request-a-review "Direct link to Who can request a review?")

Anyone with [Can Edit](/docs/collaborate/sharing-and-permissions/project-sharing#can-edit) access to a project can request a review as part of the publish flow.

#### Who can leave a review?[​](#who-can-leave-a-review "Direct link to Who can leave a review?")

Anyone with [Can Explore](/docs/collaborate/sharing-and-permissions/project-sharing#can-explore) access to a project can review work. This allows stakeholders to review projects as well as collaborators.

#### If I request a review from multiple users or a group, do all users need to approve?[​](#if-i-request-a-review-from-multiple-users-or-a-group-do-all-users-need-to-approve "Direct link to If I request a review from multiple users or a group, do all users need to approve?")

No, only one user needs to approve in order for the review to be marked as "approved". If any reviewers requests changes, though, that same reviewer will need to update their review decision in order for the review request to be marked as "approved".

#### How do reviews work with Git Export?[​](#how-do-reviews-work-with-git-export "Direct link to How do reviews work with Git Export?")

When reviews are used in conjunction with [Git Export](/docs/explore-data/projects/git-export), changes will be merged to your provider's publish branch upon publish.

#### On this page

* [Requesting a review](#requesting-a-review)
  + [Creating a review request](#creating-a-review-request)
  + [Adding reviewers](#adding-reviewers)
* [Leaving a review](#leaving-a-review)
* [Addressing requested changes](#addressing-requested-changes)
* [Resolving a review request](#resolving-a-review-request)
  + [Understanding review request states](#understanding-review-request-states)
  + [Publishing changes](#publishing-changes)
* [Required reviews](#required-reviews)
* [FAQ](#faq)