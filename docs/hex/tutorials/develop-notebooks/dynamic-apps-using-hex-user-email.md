On this page

# Dynamic apps using hex\_user\_email

A dive into the `hex_user_email` built-in variable and how to leverage it to create dynamic apps.

tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/6784c649-06ac-4ba4-8fa4-14d1025c49ce/latest)!

This tutorial will go into detail on the `hex_user_email` [built-in variable](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables), and cover some examples for creating dynamic app experiences based on the its value. By the end, you'll be ready to create a single app that renders differently depending on who's viewing the published app!

### What is `hex_user_email`?[​](#what-is-hex_user_email "Direct link to what-is-hex_user_email")

Hex has a few [built-in variables](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables) that can be leveraged in the logic of your projects. One of these built-in variables is `hex_user_email`.

In published apps, the logged in user's email address will be stored as the `hex_user_email` variable. This makes this variable perfect for customizing what a given user sees in the app!

### Some example use cases[​](#some-example-use-cases "Direct link to Some example use cases")

* Make a SQL query dynamic depending on the user's email, using [Jinja to parameterize the query](/tutorials/connect-to-data/parameterize-sql#finally-parameterize-the-sql-query-with-the-input-value):

```
SELECT account, sum(revenue)  
FROM sales_table  
WHERE account_owner_email == {{hex_user_email}}
```

* Execute dynamic Python code:

```
if hex_user_email in ('[email protected]', '[email protected]', '[email protected]'):  
    department = 'engineering'  
else:  
    department = 'other'
```

* Display customized Markdown text, using a [Jinja if statement](https://jinja.palletsprojects.com/en/3.1.x/templates/#if):

```
{% if hex_user_email == '[email protected]' %}  
Hi Jaylin!  
{% elif hex_user_email == '[email protected]' %}  
Hi Imani!  
{% else %}  
Hi there!  
{% endif %}
```

### `hex_user_email` and published app run settings[​](#hex_user_email-and-published-app-run-settings "Direct link to hex_user_email-and-published-app-run-settings")

When opening an app that is set to **[show results from a previous run](/docs/share-insights/apps/app-run-settings#update-published-results)**, the initial app load will not use the `hex_user_email` variable as expected.

Why? Apps set to **show results from a previous run** automatically load using the cached results from the most recent app publish or scheduled run. Therefore, if you want `hex_user_email` to be set to the viewer's email address upon the app's initial load, you'll need change this setting to **[run the app from scratch](/docs/share-insights/apps/app-run-settings#run-the-app-from-scratch)**.

### `hex_user_email` in different run contexts[​](#hex_user_email-in-different-run-contexts "Direct link to hex_user_email-in-different-run-contexts")

**Note: `hex_user_email` will only evaluate to the user's email address *in the published app***.

When viewing the project's Notebook view + App builder, the variable will always equal `[email protected]`.

If an anonymous user (i.e., someone without a Hex account) views the published App, `hex_user_email` will be a random hash. An app will only ever have anonymous viewers if it's [been made available publicly](/docs/collaborate/sharing-and-permissions/sharing-permissions#public-share-permissions).

tip

Check out this tutorial's [companion app](https://app.hex.tech/hex-public/app/6784c649-06ac-4ba4-8fa4-14d1025c49ce/latest) to see how the `hex_user_email` value changes when viewing the logic vs. the published app.

### Video example[​](#video-example "Direct link to Video example")

To drive this home, here's a quick video demo of what a published app that uses `hex_user_email` looks like from the perspectives of two different users!

#### On this page

* [What is `hex_user_email`?](#what-is-hex_user_email)
* [Some example use cases](#some-example-use-cases)
* [`hex_user_email` and published app run settings](#hex_user_email-and-published-app-run-settings)
* [`hex_user_email` in different run contexts](#hex_user_email-in-different-run-contexts)
* [Video example](#video-example)