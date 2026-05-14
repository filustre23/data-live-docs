On this page

# API overview

Programmatically list and run Hex projects with the API.

info

Admin APIs are available on both the **Team** and **Enterprise** [plans](https://hex.tech/pricing/); certain endpoints are exclusive to the **Enterprise** plan.

The Hex public API allows teams to programmatically interact with their Hex workspace — including listing projects, triggering runs of published projects, managing access controls, and configuring data connections.

* Core Admin APIs, such as user, group, collection, and project run management, are available to both Team and Enterprise plans.
* Observability API for advanced capabilities - such as retrieving queried tables for a given project (eg. [`GetQueriedTables`](/docs/api-integrations/api/reference#operation/GetQueriedTables)) - is available on the Enterprise plan only.

If you are looking to integrate Hex project runs into orchestration tools, check our native integrations with [Airflow](https://github.com/hex-inc/airflow-provider-hex), [Dagster](https://github.com/hex-inc/dagster-hex), and [Orchestra](https://docs.getorchestra.io/docs/integrations/hex/).

For full path parameters and request/response schemas, view the [API reference](/docs/api-integrations/api/reference).

## Authentication[​](#authentication "Direct link to Authentication")

API requests are authenticated using OAuth 2.0 Bearer Tokens in the header of the HTTP request. The token is always bound to a single Hex user's account and requests are executed as that Hex user, meaning the user can only execute requests against projects that are in line with the current permissions for that project.

### Token creation[​](#token-creation "Direct link to Token creation")

There are two types of tokens users can create: **Personal access tokens** and **Workspace tokens**. Tokens are prefixed to indicate their type: `hxtp_` for personal access tokens and `hxtw_` for workspace tokens. This prefix enables security scanning tools to detect accidentally exposed tokens.

### Personal access tokens[​](#personal-access-tokens "Direct link to Personal access tokens")

Personal access tokens mirror the same permissions that a user has within the Hex product. They can be created by anyone with an [Editor](/docs/collaborate/sharing-and-permissions/roles) or higher workspace role. Unlike [workspace tokens](#workspace-tokens) (which can have no expiration), they must be configured to expire after a fixed duration.

info

Enforcing token expiration for personal access tokens ensures that tokens are rotated frequently.

To create a Personal access token, head to the [user settings](/docs/administration/user-settings), and then the **API keys** page under the **Account** section. Then, select the **New Token** button and provide a description and an expiration time frame. An existing token can be regenerated at any time by selecting the three-dot menu to the right of the token, and selecting **Regenerate**.

warning

Regenerating a personal access token will generate a new value for the token and immediately revoke the existing token.

If a user is deactivated in a workspace, their personal access tokens will no longer work.

### Workspace tokens[​](#workspace-tokens "Direct link to Workspace tokens")

Workspace tokens are created, managed, and shared by Admins of a workspace. Unlike [personal access tokens](#personal-access-tokens), **workspace tokens can be configured to never expire**. This more permissive setting is available for workspace tokens, since any Admin can revoke this token at any time.

To create a Workspace token, head to the [user settings](/docs/administration/user-settings), and then the **API keys** page under the **Account** section. Then, select the **New Token** button and provide a description and an expiration time frame. Workspace tokens can be configured to have the following scopes:

* Read projects: The token will work with any API endpoint that only gets information (e.g. [`ListProjects`](/docs/api-integrations/api/reference#operation/ListProjects) and [`GetProjectRuns`](/docs/api-integrations/api/reference#operation/GetProjectRuns)).
* Run projects: The token will also work with the RunProjects endpoint.
* For Users, Groups, Collections, and Data connections: The token can be specified to have read-only or write access (which includes read).

tip

If you are creating a token that is used to orchestrate projects across a workspace, consider using a Workspace token so that the token is not scoped to an individual user.

### Comparison[​](#comparison "Direct link to Comparison")

| Feature | Personal access token | Workspace token |
| --- | --- | --- |
| Required workspace role | Editor or higher | Admin only |
| Maximum expiration | Follows expiration rules configured by Admins | Can be configured to never expire |
| Permissions | Mirrors an individual user's permissions | Mirrors the admin permissions for the workspace, with additional configuration for scopes |

### Token expiration[​](#token-expiration "Direct link to Token expiration")

When creating a token, users can specify an expiration period:

* **Personal access tokens**: When creating a personal access token, users can specify a time to live that is equal to, or less than, the maximum expiration time configured by an Admin (see below). Durations may include 7, 30, 60, 90, or 120 days.
* **Workspace tokens**: When creating a workspace token, admins can specify an expiration that is a fixed duration (one of 7, 30, 60, 90, or 120 days), or no expiry.

To configure the maximum expiration for a personal access token, Admins can head to the **Integrations** page, under the **Workspace** section of **Settings**.

Users will receive an email notification 72 hours before and 24 hours before any token expires, warning them that the token will be expiring soon. Tokens can be manually revoked by clicking the three-dot menu to the right of the token, and selecting **Revoke**. Once a token is revoked or expired, the token can never again be used to authenticate requests.

## Using the API[​](#using-the-api "Direct link to Using the API")

The Hex API provides programmatic access to a broad set of capabilities within the Hex platform, supporting both project execution and administrative workflows.

Initially designed to run published Hex projects with specific inputs—enabling automation of workflows, refreshing cached query results, and updating app state—the API has since expanded to include endpoints for managing:

* **Users** and their roles
* **Groups** and access controls
* **Collections** of projects
* **Data connections** and credentials (for [Tier 1](/docs/connect-to-data/data-connections/data-connections-introduction#tier-1) connectors)

This expanded API surface allows teams to automate administration, enforce governance, and integrate Hex more deeply into existing systems. You can find the full reference documentation for the Hex API [here](/docs/api-integrations/api/reference).

info

If your workspace is using [Directory Sync](/docs/administration/workspace_settings/directory-sync), users and groups will continue to be managed there and not via API.

The examples below use the [requests](https://pypi.org/project/requests/) package to run the API, though it can also be accessed using tools like running a `cURL` command, Postman, or any HTTP client of your choice.

### Setup needed for the API[​](#setup-needed-for-the-api "Direct link to Setup needed for the API")

To use the API correctly, first run some setup code. Ensure that you replace values for your specific use-case.

* **Base URL**: For most Hex users, this will be `https://app.hex.tech/api/v1`. For single tenant, EU multi tenant, and HIPAA multi tenant customers, replace `app.hex.tech` with your custom URL (e.g. `atreides.hex.tech`, `eu.hex.tech`).
* **Project ID**: The project ID can be found by visiting the project you wish to run and using the "Copy project id" option in either the help menu or 3-dot menu at top right, in the notebook and published app respectively. More on how you can retrieve a project's ID is described [here](/docs/explore-data/projects/create-and-manage-projects#extract-project-uuid). Additionally, the project ID can be found in the **[Variables](/docs/explore-data/projects/environment-configuration/environment-views#variables)** view of the sidebar.
* **Token**: See the above section on [token creation](#token-creation). Consider using a [secret](/docs/explore-data/projects/environment-configuration/environment-views) to store this more securely.

```
import requests  
  
# Single tenant, HIPAA, and EU users will need to replace this with their Hex URL  
BASE_URL = 'https://app.hex.tech/api/v1'  
  
# Replace this with the project ID  
PROJECT_ID = '5a8591dd-4039-49df-9202-96385ba3eff8'  
  
# Replace this with your token (format: hxtp_<96 hex chars> for personal, hxtw_<96 hex chars> for workspace)  
TOKEN = 'hxtp_5bbf1c8b1989d6657d5c...'
```

### Run a published project with default inputs[​](#run-a-published-project-with-default-inputs "Direct link to Run a published project with default inputs")

This API call uses the [`RunProject`](/docs/api-integrations/api/reference#operation/RunProject) endpoint to run a published project with its default inputs. It does **not** update the cache for this project.

```
response = requests.post(  
    url=f"{BASE_URL}/projects/{PROJECT_ID}/runs",  
    headers={"Authorization" : f"Bearer {TOKEN}"}  
)
```

The response from this request will contain a `runUrl` which will display the results of the project run as a [Snapshot](/docs/share-insights/apps/snapshots), viewable by any user who has at least view access to the project.

### Run a published project with custom inputs[​](#run-a-published-project-with-custom-inputs "Direct link to Run a published project with custom inputs")

The [`RunProject`](/docs/api-integrations/api/reference#operation/RunProject) endpoint contains an optional `inputParams` body parameter that allows users to specify the values for [Input parameters](/docs/explore-data/cells/input-cells/input-cells-introduction) to be used in the project run.

```
inputs = {  
  "inputParams": {  
    "user_name": "j_doe",  
    "team": "finance",  
    "id": 1234567890  
  }  
}  
  
response = requests.post(  
    url=f"{BASE_URL}/projects/{PROJECT_ID}/runs",  
    json=inputs,  
    headers={"Authorization" : f"Bearer {TOKEN}"}  
)
```

### Update the cached state and query cache of a published project[​](#update-the-cached-state-and-query-cache-of-a-published-project "Direct link to Update the cached state and query cache of a published project")

The [`RunProject`](/docs/api-integrations/api/reference#operation/RunProject) API allows control over two key caching options: `updatePublishedResults` for updating the published app's state, and `useCachedSqlResults` for controlling whether cached SQL results are used.

**updatePublishedResults**: When `updatePublishedResults` is set to false in a `RunProject` request (the default), the project run will not update the published app state. When `updatePublishedResults` is set to true, the project run will update the cached state of the published app with the latest run results⁠. This ensures that viewers see the results generated by the run when they open the app.⁠

In order to set `updatePublishedResults` to true, ["Show results from a publish, or scheduled run"](/docs/share-insights/apps/app-run-settings) must be enabled. If `inputParams` are included in the request with `updatePublishedResults` set to true, the provided parameter values will be ignored, as updating the published app’s cache state requires the default Input parameter values to be used.

**useCachedSqlResults**: When `useCachedSqlResults` is set to true in a `RunProject` request (the default), the project will use cached SQL results if available. When `useCachedSqlResults` is set to false, SQL cells will run without hitting the cache, essentially refreshing the cached SQL query results for future runs.

In order for a query to execute and update cached results using `useCachedSqlResults`, "Use SQL caching in published app" must be enabled on the project’s [Published app run settings](/docs/share-insights/apps/app-run-settings#sql-caching).

```
# Forces a fresh run of SQL queries and updates the published app with new results  
inputs = {  
  "useCachedSqlResults": "false",  
  "updatePublishedResults": "true"  
}  
  
response = requests.post(  
    url=f"{BASE_URL}/projects/{PROJECT_ID}/runs",  
    json=inputs,  
    headers={"Authorization" : f"Bearer {TOKEN}"}  
)
```

### Create a new group given a list of user emails[​](#create-a-new-group-given-a-list-of-user-emails "Direct link to Create a new group given a list of user emails")

warning

Group names are not unique - if you create a group with the same name as one that already exists, a new group with the same name will be created.

#### Step 1: Get User IDs from Emails[​](#step-1-get-user-ids-from-emails "Direct link to Step 1: Get User IDs from Emails")

```
import requests  
  
# Example: Fetch user list to get IDs  
resp = requests.get(  
    url=f"{BASE_URL}/users",  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)  
users = resp.json()["users"]  
email_to_id = {u["email"]: u["id"] for u in users}
```

tip

You’ll need to fetch all users across paginated API responses

#### Step 2: Create the Group[​](#step-2-create-the-group "Direct link to Step 2: Create the Group")

```
group_payload = {  
    "name": "Data Engineering Team",  
    "members": {  
        "users": [{"id": email_to_id["[email protected]"]}, {"id": email_to_id["[email protected]"]}]  
    }  
}  
  
resp = requests.post(  
    url=f"{BASE_URL}/groups",  
    json=group_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

### Create a new Collection with specific sharing permissions[​](#create-a-new-collection-with-specific-sharing-permissions "Direct link to Create a new Collection with specific sharing permissions")

The [`CreateCollection`](/docs/api-integrations/api/reference#operation/CreateCollection) endpoint lets you define sharing settings for users, groups, or the workspace at creation.

info

You must have admin privileges to set group and workspace-level access.

```
collection_payload = {  
    "name": "Q3 Projects",  
    "description": "All Q3 cross-functional initiatives",  
    "members": {  
        "groups": [  
            {"id": "group-analytics", "access": "MEMBER"},  
            {"id": "group-admins", "access": "MANAGER"}  
        ],  
        "workspace": {"members": "MEMBER"}  
    }  
}  
  
resp = requests.post(  
    url=f"{BASE_URL}/collections",  
    json=collection_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

### Change Collection permissions[​](#change-collection-permissions "Direct link to Change Collection permissions")

To update permissions on an existing Collection, use the [`EditCollection`](/docs/api-integrations/api/reference#operation/EditCollection) endpoint. You can upsert user/group/workspace access using the `sharing.upsert` field.

```
edit_payload = {  
    "collectionId": "COLLECTION_ID",  
    "sharing": {  
        "upsert": {  
            "groups": [  
                {"id": "group-analytics", "access": "NONE"},     # Remove access  
                {"id": "group-ops", "access": "MEMBER"}           # Add new group  
            ],  
            "workspace": {"members": "MANAGER"}  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/collections/{COLLECTION_ID}",  
    json=edit_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)  
print(resp.json())
```

### Rotate data connection credentials[​](#rotate-data-connection-credentials "Direct link to Rotate data connection credentials")

To rotate secrets (e.g., passwords, service accounts), use the [`EditDataConnection`](/docs/api-integrations/api/reference#operation/EditDataConnection) endpoint and supply a new `connectionDetails` block.

info

This is only applicable for [Tier 1](/docs/connect-to-data/data-connections/data-connections-introduction#tier-1) data connectors.

#### Step 1: Get data connection ID[​](#step-1-get-data-connection-id "Direct link to Step 1: Get data connection ID")

```
import requests  
  
resp = requests.get(  
    url=f"{BASE_URL}/data-connections",  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)  
  
# Print available connections  
for conn in resp.json()["values"]:  
    print(f"{conn['name']} → ID: {conn['id']}")
```

#### Step 2: Update the connectionDetails block[​](#step-2-update-the-connectiondetails-block "Direct link to Step 2: Update the connectionDetails block")

* Snowflake
* BigQuery
* Postgres
* Redshift
* Athena
* Databricks

```
edit_conn_payload = {  
    "connectionDetails": {  
        "snowflake": {  
            "accountName": "test123.us-east-2.com",  
            "warehouse": "FOO",  
            "database": "MY_DB",  
            "schema": "MY_SCHEMA",  
            "username": "hex_user",  
            "privateKey": "NEW_PRIVATE_KEY",  
            "passphrase": "NEW_PASSPHRASE",  
            "role": "MY_ROLE"  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/data-connections/{DATA_CONNECTION_ID}",  
    json=edit_conn_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

```
edit_conn_payload = {  
    "connectionDetails": {  
        "bigquery": {  
            "projectID": "my-test-project-123456",  
            "enableDriveAccess": true,  
            "enableStorageApi": true,  
            "serviceAccountJsonConfig": "{}",  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/data-connections/{DATA_CONNECTION_ID}",  
    json=edit_conn_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

You can rotate BigQuery service accounts by updating the `serviceAccountJsonConfig` in the `bigquery` object.

```
edit_conn_payload = {  
    "connectionDetails": {  
        "postgres": {  
            "hostname": "db.mycompany.com",  
            "port": 5432,  
            "database": "prod_data",  
            "username": "hex_user",  
            "password": "NEW_SECURE_PASSWORD"  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/data-connections/{DATA_CONNECTION_ID}",  
    json=edit_conn_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

```
edit_conn_payload = {  
    "connectionDetails": {  
        "redshift": {  
            "host": "prod.abcdef1234.us-east-2.redshift.amazonaws.com",  
            "port": 5432,  
            "database": "prod_data",  
            "username": "hex_user",  
            "password": "NEW_SECURE_PASSWORD"  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/data-connections/{DATA_CONNECTION_ID}",  
    json=edit_conn_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

```
edit_conn_payload = {  
    "connectionDetails": {  
        "athena": {  
            "hostname": "athena.us-east-2.amazonaws.com",  
            "port": 5432,  
            "s3OutputPath": "s3://hex-prod-athena",  
            "catalog": "",  
            "workgroup": "",  
            "accessKeyId": "NEW_ACCESS_KEY",  
            "secretAccessKey": "NEW_SECRET_ACCESS_KEY"  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/data-connections/{DATA_CONNECTION_ID}",  
    json=edit_conn_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

```
edit_conn_payload = {  
    "connectionDetails": {  
        "databricks": {  
            "jdbcUrl": "jdbc:jdbcType://uuid.my-databricks-host.com;httpPath=/some/http/path",  
            "accessToken": "NEW_ACCESS_TOKEN",  
        }  
    }  
}  
  
resp = requests.patch(  
    url=f"{BASE_URL}/data-connections/{DATA_CONNECTION_ID}",  
    json=edit_conn_payload,  
    headers={"Authorization": f"Bearer {YOUR_API_TOKEN}"}  
)
```

### Cancel active runs for a project[​](#cancel-active-runs-for-a-project "Direct link to Cancel active runs for a project")

Project runs can be cancelled using the [`CancelRun`](/docs/api-integrations/api/reference#operation/CancelRun) endpoint. This can be especially useful if project runs triggered by the API are contributing to database performance degradation, or your user is running into the [kernel limit](#kernel-and-rate-limits). The [`GetProjectRuns`](/docs/api-integrations/api/reference#operation/GetProjectRuns) endpoint can be used in conjunction with this in order to easily cancel all API-triggered project runs.

```
# Get all runs for project  
response = requests.get(  
    url=f"{BASE_URL}/projects/{PROJECT_ID}/runs",  
    params={"limit": 25, "statusFilter": "RUNNING"},  
    headers={"Authorization" : f"Bearer {TOKEN}"}  
)  
response = response.json()  
  
# Iterate through runs and cancel them  
for run in response["runs"]:  
    run_id = run["runId"]  
    requests.delete(  
        url=f"{BASE_URL}/projects/{PROJECT_ID}/runs/{run_id}",  
        headers={"Authorization" : f"Bearer {TOKEN}"}  
    )
```

tip

The `GetProjectRuns` endpoint will only return information on API-triggered project runs. To cancel ongoing Scheduled Runs, you'll need the relevant `runId`, which can be found as the final argument in the URL when you view a given run from the [Run Log](/docs/share-insights/scheduled-runs#accessing-past-scheduled-runs).

### Kernel and rate limits[​](#kernel-and-rate-limits "Direct link to Kernel and rate limits")

Users are limited to 60 API requests per minute. If a user exceeds 60 requests in a minute, subsequent requests will be denied and return a 429 status until the rate limit is reset, 60 seconds after the first request. Request response headers contain metadata about the remaining number of requests allowed, and when the rate limit will be reset. Some Hex API endpoints may have additional rate limits which can be found in the [API reference docs](/docs/api-integrations/api/reference).

Users are also limited to 25 concurrently running kernels between projects opened in the Hex UI and project runs triggered via the API. Each `RunProject` request will use a single kernel until the project run completes. Once 25 kernels are running, subsequent `RunProject` requests will result in a 503 status code, with no project run created. In addition to this, projects opened in the UI that do not already have a running kernel will show an error that you have reached the maximum number of running kernels. Cancelling a project run using the `CancelRun` endpoint will stop a running kernel and free it for use via the UI or API.

## The API and hextoolkit[​](#the-api-and-hextoolkit "Direct link to The API and hextoolkit")

The [hextoolkit](/tutorials/connect-to-data/using-the-hextoolkit) contains a wrapper for all of the Hex API's functionality. This section is a brief overview of the functionality and syntax. You can view all of the ApiClient methods, their arguments, and their return objects in the [API reference docs](/docs/api-integrations/api/reference).

### Create the client[​](#create-the-client "Direct link to Create the client")

To make requests using the `hextoolkit`, you will need to generate an ApiClient with your [token](#token-creation). We recommend storing this token as a [secret](/docs/explore-data/projects/environment-configuration/environment-views#variables).

```
import hextoolkit as htk  
import hex_api  
api_client = htk.get_api_client(TOKEN)
```

### Get project metadata[​](#get-project-metadata "Direct link to Get project metadata")

Metadata can be fetched for an individual project via the `get_project` endpoint or for up to 100 projects via the `list_projects` endpoint.

```
single_project = api_client.get_project(project_id=PROJECT_ID)  
many_projects = api_client.list_projects(limit=100)
```

A `ProjectApiResource` is returned from the `get_project` endpoint, which contains various pieces of metadata about the project (see the [API Reference docs](/docs/api-integrations/api/reference) for the complete object structure). The `list_projects` endpoint will return a list of these, as well as a `pagination` object containing cursor information for fetching the next page of projects. You can pass in the `pagination.after` cursor string into a subsequent `list_projects()` request in order to continue fetching new projects. When the end of pagination has been reached, the `after` value will be `None`. See below for an example of a loop to fetch metadata for all projects in a workspace:

```
first_page = client.list_projects(limit=100)  
after = first_page.pagination.after  
projects = first_page.values  
  
while after:  
    response = client.list_projects(limit = 100, after=after)  
    after = response.pagination.after  
    new_projects = response.values  
    projects = [*projects, *new_projects]
```

### Run projects[​](#run-projects "Direct link to Run projects")

Running a project with no inputs is as simple as specifying the `project_id`:

```
project_run = api_client.run_project(project_id=PROJECT_ID)
```

The `run_project` method returns a `ProjectRunResponsePayload` object containing metadata, as well as a `run_url` where you can view the results.

It is also possible to run a project with inputs or to update the cache of a project using the `run_project_request_body argument`:

```
# Run a project with inputs  
input_request_body = hex_api.RunProjectRequestBody(  
  input_params={  
    "input_parameter_name": "input_parameter_value",  
    ...  
  }  
)  
  
# Set a new cache  
update_cache_request_body = hex_api.RunProjectRequestBody(  
  update_cache=True  
)  
  
# Update the value used for run_project_request_body depending on desired behavior  
project_run = api_client.run_project(project_id=PROJECT_ID, run_project_request_body=input_request_body)
```

### Get a run status[​](#get-a-run-status "Direct link to Get a run status")

The status of a run can be viewed using the `run_status_url` as part of the returned object from the `run_project` method. The `get_run_status` method can also be used to programmatically check the status of a run:

```
project_run = api_client.run_project(project_id=PROJECT_ID)  
status = api_client.get_run_status(project_id=PROJECT_ID, run_id=project_run.run_id)
```

### Cancel a project run[​](#cancel-a-project-run "Direct link to Cancel a project run")

Project runs can be cancelled using the `cancel_run` method:

```
project_run = api_client.run_project(project_id=PROJECT_ID)  
api_client.cancel_run(project_id=PROJECT_ID, run_id=project_run.run_id)
```

### Get all project runs[​](#get-all-project-runs "Direct link to Get all project runs")

All runs of a given project can be retrieved using the `get_project_runs` method. The project runs can be filtered using the `status_filter` argument to easily identify project runs that have completed, errored, etc.

```
active_runs = api_client.get_project_runs(project_id=PROJECT_ID, status_filter='RUNNING')
```

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

### 401 Unauthorized[​](#401-unauthorized "Direct link to 401 Unauthorized")

A 401 status code indicates that Hex was unable to authenticate the request. Make sure that a token is being included in the header of your request, and that you have specified a [valid base URL](#setup-needed-for-the-api). If you are including a token in the header of the request, double-check that the token has not expired and consider regenerating the token or creating a new token.

### 404 Not found[​](#404-not-found "Direct link to 404 Not found")

A 404 status code indicates that Hex was unable to find the resource referenced. This could mean that the project ID or run ID included in the request are not accurate, or that your user does not have permission for the requested resource. Double-check that the user an access the Hex project in the UI.

### 422 Unprocessable Entity[​](#422-unprocessable-entity "Direct link to 422 Unprocessable Entity")

A 422 status code can indicate that you are attempting to interact with a project that hasn't been published, or that you have provided invalid input parameters as a part of your request. Double-check that your app has been published, and that any [input parameters](#run-a-published-project-with-custom-inputs) provided are correctly specified.

Note that some GET endpoints only return data for published projects:

* `GetQueriedTables` will return a 422 for unpublished projects.
* `GetProjectRuns` also only returns data for published projects, as unpublished projects have no run history.

You can check whether a project is published by verifying that `lastPublishedAt` is non-null in `ListProjects` or `GetProject`.

### 429 Too many requests[​](#429-too-many-requests "Direct link to 429 Too many requests")

A 429 status code indicates that you have hit the request rate limit. See the section on [rate limiting](#kernel-and-rate-limits) above for more information.

### 500 Internal server error[​](#500-internal-server-error "Direct link to 500 Internal server error")

A 500 status code indicates an error with the Hex application. Please contact [Hex support](/cdn-cgi/l/email-protection#ccbfb9bcbca3beb88ca4a9b4e2b8a9afa4) for help troubleshooting.

### 503 Service Unavailable[  ​](#503-service-unavailable "Direct link to 503 Service Unavailable")

A 503 status code indicates that the user has reached the maximum number of concurrently running kernels. See the section on [kernel limits](#kernel-and-rate-limits) above for more information.

#### On this page

* [Authentication](#authentication)
  + [Token creation](#token-creation)
  + [Personal access tokens](#personal-access-tokens)
  + [Workspace tokens](#workspace-tokens)
  + [Comparison](#comparison)
  + [Token expiration](#token-expiration)
* [Using the API](#using-the-api)
  + [Setup needed for the API](#setup-needed-for-the-api)
  + [Run a published project with default inputs](#run-a-published-project-with-default-inputs)
  + [Run a published project with custom inputs](#run-a-published-project-with-custom-inputs)
  + [Update the cached state and query cache of a published project](#update-the-cached-state-and-query-cache-of-a-published-project)
  + [Create a new group given a list of user emails](#create-a-new-group-given-a-list-of-user-emails)
  + [Create a new Collection with specific sharing permissions](#create-a-new-collection-with-specific-sharing-permissions)
  + [Change Collection permissions](#change-collection-permissions)
  + [Rotate data connection credentials](#rotate-data-connection-credentials)
  + [Cancel active runs for a project](#cancel-active-runs-for-a-project)
  + [Kernel and rate limits](#kernel-and-rate-limits)
* [The API and hextoolkit](#the-api-and-hextoolkit)
  + [Create the client](#create-the-client)
  + [Get project metadata](#get-project-metadata)
  + [Run projects](#run-projects)
  + [Get a run status](#get-a-run-status)
  + [Cancel a project run](#cancel-a-project-run)
  + [Get all project runs](#get-all-project-runs)
* [Troubleshooting](#troubleshooting)
  + [401 Unauthorized](#401-unauthorized)
  + [404 Not found](#404-not-found)
  + [422 Unprocessable Entity](#422-unprocessable-entity)
  + [429 Too many requests](#429-too-many-requests)
  + [500 Internal server error](#500-internal-server-error)
  + [503 Service Unavailable](#503-service-unavailable)