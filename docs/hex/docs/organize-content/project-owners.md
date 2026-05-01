# Project owners

The owner of a project indicates who currently maintains a project, and can be transferred over time.

The current owner of a project can be found via the **Share** dialog in the top right hand corner, or on the **Projects** page.

By default, the project creator is designated as the project owner. Users with **Full Access** [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions), or the **Admin** or **Manager** [role](/docs/collaborate/sharing-and-permissions/roles) can transfer ownership of a project through one of three ways:

* Individual projects can be transferred via the menu in the top-left hand corner of the logic view.
* Multiple projects can be transferred via [bulk actions](/docs/organize-content/organize-projects) on the **Projects** page.
* When a user is deactivated from a workspace, Admins can choose to transfer ownership of their projects to a new user.

Transferring ownership of a project updates the user associated with this project throughout the UI. The new owner will be granted **Full Access** [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions) to the project. No changes will be made to the previous owner's project permission¹.

Further, teams using [OAuth data connections](/docs/connect-to-data/data-connections/oauth-data-connections) can use the **Transfer owner** functionality to update the user whose warehouse credentials are used when editing. [Learn more about OAuth](/docs/connect-to-data/data-connections/oauth-data-connections).

*¹For teams using Snowflake OAuth without token sharing, the previous owner will be downgraded to **Can Explore** permission, since they can not share the new owner's token.*