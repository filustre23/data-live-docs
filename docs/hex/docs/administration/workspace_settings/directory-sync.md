On this page

# Directory Sync

Set Hex user roles from your directory provider (Okta, Rippling, Google, Azure and more).

info

* Available on the Enterprise [plan](https://hex.tech/pricing). If your workspace is single tenant, please contact [[email protected]](/cdn-cgi/l/email-protection#ef9c9a9f9f809d9baf878a97c19b8a8c87) for assistance configuring.
* Only workspace Admins can configure directory sync.

Teams who use a directory provider for authentication and access controls for their various tools can now sync with Hex. When using directory sync, Hex users, roles, and group membership can all be managed in a third party tool, like Okta, Azure, and others. This allows teams to quickly and easily keep a single source of truth for which users should have access and engage with Hex.

### Understanding directory sync:[​](#understanding-directory-sync "Direct link to Understanding directory sync:")

* Any users in your directory provider who have access to Hex will appear as a user in Hex. If a user in your directory provider is not included in a group specifying a certain Hex user role, that user will be assigned to Hex as a Viewer.
* Groups that are created in your directory provider can optionally be synced to Hex, appearing as groups in the **Users & Groups** section of your Hex **Administration** panel.
* Groups can be used to determine the role of Hex users (e.g. Admin vs Editor vs Viewer).
* Any groups defined in your directory provider will also appear as groups in Hex. These Hex groups can be configured for access to shared workspace assets as with any Hex-created group. See more about managing shared group assets [here](/docs/administration/workspace_settings/workspace-assets).
* Alternatively, you can choose to forgo group-based role configuration and assign roles by user in Hex

info

Changes made to your directory details can take up to 5 minutes to be reflected in Hex. If your changes take longer than this time to be reflected reach out to [[email protected]](/cdn-cgi/l/email-protection#0774727777687573476f627f297362646f)

### Setup steps:[​](#setup-steps "Direct link to Setup steps:")

* In the Hex Administration panel, go to the **Users & groups** panel and scroll down to **Directory sync** — if you don’t see this option then Directory Sync is not currently available for your workspace. Get in touch with us at [`[email protected]`](/cdn-cgi/l/email-protection#69010c05050629010c11471d0c0a01) to change that!
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

## FAQs[​](#faqs "Direct link to FAQs")

How can I edit groups which have been configured in my directory sync provider?

* Any group synced from your directory provider cannot be edited in Hex. e.g. membership for groups which have been set up via your directory sync must be managed in your directory provider directly.

If I have directory sync enabled, can I have still add additional users to Hex from Hex?

* Yes. You can add users to your workspace from the **Administration** panel. However, users added in this manner will *not* be added to any of your groups as defined in your directory sync provider. For example: If you added a new Admin user from Hex, that user will not be appended to the "Hex Admins" group. Thus if you have configured that group to have access to any shared workspace assets the new user would *not* be included in that access.

What happens if I don't specify what Hex user role someone should have?

* If your workspace is configured to allow anyone with a specified email domain to log in to Hex, and the user joins your workspace via that method, their role will be determined by the configured default workspace role.
* If a user is added to Hex via your directory provider and they are *not* included in the Admin or Editor group, they will be Viewers.

#### On this page

* [Understanding directory sync:](#understanding-directory-sync)
* [Setup steps:](#setup-steps)
* [Group changes with Okta directory sync](#group-changes-with-okta-directory-sync)
* [FAQs](#faqs)