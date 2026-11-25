On this page

# Directory Sync

Set Hex user roles from your directory provider (Okta, Rippling, Google, Azure and more).

info

* Available on the Enterprise [plan](https://hex.tech/pricing). If your workspace is single tenant, please contact [support@hex.tech](mailto:support@hex.tech) for assistance configuring.
* Only workspace Admins can configure directory sync.

Teams who use a directory provider for authentication and access controls for their various tools can now sync with Hex. When using directory sync, Hex users, roles, and group membership can all be managed in a third party tool, like Okta, Azure, and others. This allows teams to quickly and easily keep a single source of truth for which users should have access and engage with Hex.

### Understanding directory sync:[​](#understanding-directory-sync "Direct link to Understanding directory sync:")

* Any users in your directory provider who have access to Hex will appear as a user in Hex. If a user in your directory provider is not included in a group specifying a certain Hex user role, that user will be assigned to Hex as a Viewer.
* Groups that are created in your directory provider can optionally be synced to Hex. Synced groups appear under **Groups** in the **Access & security** section of your workspace settings
* Groups can be used to determine the role of Hex users (e.g. Admin vs Editor vs Viewer).
* Any groups defined in your directory provider will also appear as groups in Hex. These Hex groups can be configured for access to shared workspace assets as with any Hex-created group. See more about managing shared group assets [here](/docs/administration/workspace_settings/workspace-assets).
* Alternatively, you can choose to forgo group-based role configuration and assign roles by user in Hex

info

Changes made to your directory details can take up to 5 minutes to be reflected in Hex. If your changes take longer than this time to be reflected reach out to [support@hex.tech](mailto:support@hex.tech)

### Setup steps:[​](#setup-steps "Direct link to Setup steps:")

* In your Hex workspace, go to **Settings** and select **Directory sync** under **Access & security**.
* Click on **Configure**, which will take you to a portal to select which directory provider your company uses.

#### Manage groups and user roles in directory[​](#manage-groups-and-user-roles-in-directory "Direct link to Manage groups and user roles in directory")

* Configure the users and group you want to sync to Hex in your directory sync provider. We recommend that at a minimum you create two groups: Hex Admins and Hex Editors. These are the two groups of users who you will set up to be automatically assigned the corresponding Hex user role.
* Depending on your provider, you’ll be guided through a setup flow for how to sync the details from your directory sync provider to Hex.
* Once the sync from your directory provider is complete, return to the **Users & groups** panel in Hex. From here you can now map which group of users should be assigned as Hex Admins and Hex Editors by selecting the appropriate group from the two options like **Admin assigned to <insert desired directory provider group name>**.

#### Manage groups and user roles in Hex[​](#manage-groups-and-user-roles-in-hex "Direct link to Manage groups and user roles in Hex")

* Configure the users you want to sync to Hex in your directory sync provider.
* Depending on your provider, you'll be guided through a setup flow for how to sync details from your directory sync provider to Hex. You can skip steps to push groups to Hex.
* Once the sync from your directory provider is complete, return to the **Users & groups** panel in Hex. From here, select **Disable role syncing** in the directory sync settings. You will now be able to configure and manage user roles in Hex directly.

For a full walk through of how to set up directory sync, using Okta in this case, check out this video:

### Group changes with Okta directory sync[​](#group-changes-with-okta-directory-sync "Direct link to Group changes with Okta directory sync")

If you are using Okta as your directory sync provider and make changes to the membership of an Okta Group you *must* make sure that once you have made your changes you select the "Push now" option in the Okta Group management page. Skipping this step may result in user group membership changes not propagating fully to Hex and inaccurate user roles and permissions could result.

### Require directory sync for new members[​](#require-directory-sync-for-new-members "Direct link to Require directory sync for new members")

By default, Admins can still add users to Hex directly even when directory sync is connected. If your directory provider should be the only way new members join your workspace, you can require directory sync for new members.

1. In **Settings**, select **Directory sync** under **Access & security**.
2. Under **Sync configuration**, turn on **Require directory sync for new members**.

Once this is turned on, new members can only be added through your directory provider:

* Admins can't add new members from the **Users** page or by sharing a project.
* Admins can't create groups from the **Groups** page.
* Invite links stop working until the setting is turned off.
* People at your workspace's allowed domains aren't added automatically when they log in.
* Guests can't be given a member role, such as Viewer, Editor, or Admin, unless they came from directory sync.
* Deactivated members can't be reactivated from Hex.

When you share a project with someone at an allowed domain who isn't a member yet, Hex shows **People from this domain must be added through directory sync**. You can still share projects with existing members and invite people from other domains as guests. If a deactivated member still has access to Hex in your directory provider, directory sync will reactivate them.

Existing members and guest invites aren't affected. Guests can still be invited to, and reactivated in, your workspace.

To see which users and groups came from your directory provider, check the **Directory sync** column on the **Users** and **Groups** pages. Synced rows show **Synced**.

info

Directory sync must be connected before you can turn this setting on. You can turn it off at any time.

caution

If your directory is disconnected while this setting is on, no one new can be added to your workspace. The **Require directory sync for new members** toggle is hidden when directory sync isn't active, so the **Directory sync** page shows a warning with a **Stop requiring directory sync** button instead. Select it to turn the setting off.

Turning this setting on or off is recorded in your workspace's [audit logs](/docs/administration/workspace_settings/audit-logs/audit-logs-overview).

## FAQs[​](#faqs "Direct link to FAQs")

How can I edit groups which have been configured in my directory sync provider?

* Groups synced from your directory provider can't be edited in Hex. Manage them, including their membership, in your directory provider.

If I have directory sync enabled, can I have still add additional users to Hex from Hex?

* Yes, unless you've turned on [**Require directory sync for new members**](#require-directory-sync-for-new-members). You can add users to your workspace from **Users** in **Settings**. However, users added in this manner will not be added to any of your groups as defined in your directory sync provider. For example: If you added a new Admin user from Hex, that user will not be appended to the "Hex Admins" group. Thus if you have configured that group to have access to any shared workspace assets the new user would not be included in that access.

What happens if I don't specify what Hex user role someone should have?

* If your workspace is configured to allow anyone with a specified email domain to log in to Hex, and the user joins your workspace via that method, their role will be determined by the configured default workspace role.
* If a user is added to Hex via your directory provider and they are *not* included in the Admin or Editor group, they will be Viewers.

#### On this page

* [Understanding directory sync:](#understanding-directory-sync)
* [Setup steps:](#setup-steps)
* [Group changes with Okta directory sync](#group-changes-with-okta-directory-sync)
* [Require directory sync for new members](#require-directory-sync-for-new-members)
* [FAQs](#faqs)