On this page

# Import data via API

Use secrets and Python to import data to your Hex project with an API

info

* Users will need **Can Edit** or higher [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

Any data accessible via API can be pulled into your Hex project. For example, you can pull in data from [Spotify](https://developer.spotify.com/documentation/web-api), [the US Census](https://www.census.gov/data/developers/data-sets.html), [Google Sheets](https://console.cloud.google.com/apis/library), or any other service with an API.

## Store your API key as a secret[​](#store-your-api-key-as-a-secret "Direct link to Store your API key as a secret")

Depending on the API you're using, there may be different requirements for setting up an account and acquiring API credentials.

Once you have your API key you can store it as a [secret](/docs/explore-data/projects/environment-configuration/environment-views#secrets) in your Hex project. From the **Variables** sidebar in your Hex project, locate the **Secrets** section and click **+Add** to create a new secret.

## Connect to your data source[​](#connect-to-your-data-source "Direct link to Connect to your data source")

You can then add a [Python cell](/docs/explore-data/cells/python-cells) to your project where you can import any required packages, create your connection using your API key stored in your secret, and defining an API scope as needed.

tip

Check out our [tutorial](/tutorials/connect-to-data/connect-to-google-sheets) on connecting Hex to Google Sheets via API to see an example in practice.

#### On this page

* [Store your API key as a secret](#store-your-api-key-as-a-secret)
* [Connect to your data source](#connect-to-your-data-source)