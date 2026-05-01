On this page

# Public and private embedding

Embed entire apps or specific cells in an iframe on your website, or in a Notion page using Hex's Notion integration.

info

* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to implement public or private embedding.

## Public embedding[​](#public-embedding "Direct link to Public embedding")

Public embedding refers to embedding a Hex app that is publicly shared. Anyone viewing the Hex app from the embed or from the project URL will be able see the content without authenticating, so this type of embedding is recommended only for public audience use cases where the data is safe to share.

To enable public embedding, open the **Share** dialogue and select the **Anyone with the link** option. Then follow the steps to [embed in an iframe](/docs/share-insights/embedding/public-and-private-embedding#embed-in-an-iframe) or [embed in a Notion page](/docs/share-insights/embedding/public-and-private-embedding#embed-in-a-notion-page).

## Private embedding[​](#private-embedding "Direct link to Private embedding")

Private embedding refers to embedding a Hex app that is invite-only. Anyone viewing the embed will be required to log in to Hex before they can see the content, just as they would if they were to follow the project or app URL. This type of embedding is most suitable for private internal audience use cases.

To enable private embedding, open the **Share** dialogue, invite the appropriate users or groups to the project, and select the **Invite only** option. Then follow the steps to [embed in an iframe](/docs/share-insights/embedding/public-and-private-embedding#embed-in-an-iframe) or [embed in a Notion page](/docs/share-insights/embedding/public-and-private-embedding#embed-in-a-notion-page).

## Embed in an iframe[​](#embed-in-an-iframe "Direct link to Embed in an iframe")

To embed an app in an iframe in your website, first share the project with the desired audience. Then from **Share > Embedding**, copy the embed code to your clipboard. You can paste the embed code into your website code.

To embed a single cell rather than the entire app, navigate to the cell in the Notebook, and click the three dots, then click Embed.

tip

You can specify input parameter selections in the embedded app URL by following the formatting outlined [here](/docs/share-insights/apps/publish-and-share-apps#current-inputs-link). When setting a parameter inside of an embed `src` string, you'll need to UTF-8 encode the parameter value. For example, you'll need to use the UTF-8 character for double quotes, `%22`, in place of `"`.

## Embed in a Notion page[​](#embed-in-a-notion-page "Direct link to Embed in a Notion page")

To embed an app into Notion, simply copy and paste the link to the published app into Notion and choose "Paste as preview" or "Paste as mention" when prompted. The first time you generate a preview in a given Notion workspace, you'll be prompted to connect to your Hex workspace by setting up the Hex Notion integration.

[](/assets/medias/notion-preview-8e3964155e9b9edc55c1e51e9d291006.mp4)

### How do permissions work for Notion link previews?[​](#how-do-permissions-work-for-notion-link-previews "Direct link to How do permissions work for Notion link previews?")

When you past a Hex app URL into a Notion page and choose "Paste as preview", Notion generates a preview of the Hex content. That preview will be viewable by anyone with access to the Notion page, no matter their permissions on the Hex project.

While this makes it convenient to share Hex projects with other users in your Notion workspace, it also effectively gives all Notion users the **Can View App** permission on your Hex project. As a result, only users with **Full Access** or **Can Edit** project permissions can generate a preview in Notion – users with **Can Explore** or **Can View App** permissions will not be able to generate a preview. This is in line with how permissions work within Hex: users with **Can Edit** project permissions and above are able to share projects with additional users, but users with **Can Explore** and **Can View App** permissions cannot.

The exception is projects that are shared with [**Anyone with the link**](/docs/collaborate/sharing-and-permissions/project-sharing#share-to-web), in which case anyone with a Hex login can generate a preview for these projects.

### Can I prevent users from embedding projects in Notion?[​](#can-i-prevent-users-from-embedding-projects-in-notion "Direct link to Can I prevent users from embedding projects in Notion?")

**Admins** can turn off the ability for users in their workspace to embed projects in Notion by heading to the **Admin panel**, then **Security** and disabling the **Allow Notion Link Previews** toggle.

### Does Notion embedding work in the Notion app?[​](#does-notion-embedding-work-in-the-notion-app "Direct link to Does Notion embedding work in the Notion app?")

For multi-tenant customers, Notion link previews work in both the browser and the Notion app. For single-tenant customers, Notion embedding only works in the browser. Due to Notion's connected app architecture, Notion embeds for single-tenant customers use iframe embedding, which relies on authorizing through your browser.

#### On this page

* [Public embedding](#public-embedding)
* [Private embedding](#private-embedding)
* [Embed in an iframe](#embed-in-an-iframe)
* [Embed in a Notion page](#embed-in-a-notion-page)
  + [How do permissions work for Notion link previews?](#how-do-permissions-work-for-notion-link-previews)
  + [Can I prevent users from embedding projects in Notion?](#can-i-prevent-users-from-embedding-projects-in-notion)
  + [Does Notion embedding work in the Notion app?](#does-notion-embedding-work-in-the-notion-app)