On this page

# Manage users and groups with Hex Admin API endpoints

Programmatically manage the users and groups in your Hex workspace.

This tutorial demonstrates how to interact with Hex API endpoints for managing users and groups within your Hex workspace. You'll learn how to fetch users, create and manage groups, and perform various administrative tasks. Read through the steps below for a step-by-step description; or use the “Download template project” at the bottom of the page to get a Hex project file to upload to your own Hex workspace to start trying it out yourself!

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* A Hex workspace on the Team or Enterprise plan with Admin access
* An Admin API token - you can create a token on the “API keys” tab of your Settings panel. See more about token creation [here](/docs/api-integrations/api/overview#authentication).

### Resources[​](#resources "Direct link to Resources")

* Check out the full API reference in our docs [here](/docs/api-integrations/api/reference)

## 1. Helper functions[​](#1-helper-functions "Direct link to 1. Helper functions")

First, let's go through some helper functions that facilitate some API interactions:

### The basic request function[​](#the-basic-request-function "Direct link to The basic request function")

```
import requests  
import json  
from types import SimpleNamespace  
  
def make_request(url_path, params, method, body=None):  
    headers = {  
        'Authorization': 'Bearer ' + admin_api_personal_token,  
    }  
    try:  
        domain = 'app.hex.tech'  
        response = requests.request(method, f"https://{domain}/api/{url_path}",  
                                  headers=headers,  
                                  params=params,  
                                  json=body,  
                                  timeout=10)  
        if response.status_code > 299:  
            print(f"ERR:{response.json()}")  
            return(response.status_code)  
        response.raise_for_status()  
        if response.content:  
            return (response.json())  
    except requests.exceptions.RequestException as e:  
        print(f"HTTP Request failed: {e}")
```

This function handles the HTTP requests to the Hex API. It takes a URL path, parameters, HTTP method, and an optional request body. It returns the JSON response from the API or an error code if the request fails.

You’ll need to specify the domain specific to where your Hex workspace is hosted (e.g. ‘app.hex.tech’ for workspaces on our main multi-tenant deployment or your unique identifier if you’re on a single-tenant stack. Check your workspace url to figure this out!).

### Pagination helper[​](#pagination-helper "Direct link to Pagination helper")

This helper function, `helper_w_pagination`, handles paginated API responses. It makes requests and combines the results from all pages into a single list of contents.

```
def helper_w_pagination(params = None, url = None, method = None):  
    first_page = make_request(url, params, method)  
    obj = json.loads(json.dumps(first_page), object_hook=lambda d: SimpleNamespace(**d))  
    after = obj.pagination.after  
    contents = obj.values  
    while after:  
        params['after'] = after  
        new_page = make_request(url, params, method)  
        response = json.loads(json.dumps(new_page), object_hook=lambda d: SimpleNamespace(**d))  
        try:  
            after = response.pagination.after  
            new_contents = response.values  
            contents = [*contents, *new_contents]  
        except:  
            break  
    return contents
```

The output of the `helper_w_pagination` function is then used with a another function, `make_df`, to create a well-formatted dataframe (see below). Creating a dataframe to hold the API response results makes for easier downstream data manipulation and visualization.

```
def make_df(input_obj):  
    for i, item in enumerate(input_obj):  
        if i == 0:  
            df = pd.DataFrame(columns = list(item.__dict__.keys()))  
        for col in list(item.__dict__.keys()):  
            df.loc[i, col] = eval('item.' + col)  
    return df
```

## 2. Work with users[​](#2-work-with-users "Direct link to 2. Work with users")

### To get a list of all users in your Hex workspace:[​](#to-get-a-list-of-all-users-in-your-hex-workspace "Direct link to To get a list of all users in your Hex workspace:")

The code below fetches all users from the Hex API, handling pagination to ensure all users are retrieved. The result is stored in a dataframe called `users_df`.

You can then explore this dataframe to see user details like email, ID, name, and role.

```
method = 'GET'  
url = 'v1/users'  
params = {  
    'limit': 100  
}  
users = helper_w_pagination(url = url, params = params, method = method)  
users_df = make_df(users)
```

## 3. Work with groups[​](#3-work-with-groups "Direct link to 3. Work with groups")

### To get a list of all groups in your Hex workspace:[​](#to-get-a-list-of-all-groups-in-your-hex-workspace "Direct link to To get a list of all groups in your Hex workspace:")

The code below retrieves all groups from the Hex API and stores them in a dataframe called `groups_df`.

```
method = 'GET'  
url = 'v1/groups'  
params = {  
    'limit': 100  
}  
groups = helper_w_pagination(url = url, params = params, method = method)  
groups_df = make_df(groups)
```

### Create a new group[​](#create-a-new-group "Direct link to Create a new group")

warning

Group names are not unique! If you create a group with the same name as one that already exists, a new group with the same name but different id will be created.

In this example, we’re assuming that you have a csv with a list of user emails and IDs that you want to add to a group. That csv has been uploaded and saved as a dataframe named `user_emails_csv` , which has two columns `email` and `id` . Download the full project below to see a working example.

To create a new group with a specific set of users:

```
# Assuming user_emails_csv is a dataframe with an 'email' column containing user emails  
# and new_group_name is a string with the desired group name  
  
# Retrieve the user ids associated with the given user emails  
# NOTE: A MAXIMUM OF 100 USER EMAILS CAN BE PASSED IN AT A TIME  
new_group_user_ids = get_user_ids_by_emails(user_emails_csv["email"].tolist())  
params = {}  
group_details = {  
    "name": new_group_name,  
    "members": {"users": [{"id": u_id} for u_id in new_group_user_ids]},  
}  
new_group_response = make_request(f"v1/groups", params, "POST", body=group_details)  
new_group_id = new_group_response["id"]  
print(f"Created a new group, '{new_group_name}', with id: {new_group_id}")
```

info

There is a limit of 100 user emails that can be passed in at a time. If you need to add more than 100 users to a group, you'll need to split them into multiple batches and use the edit group endpoint (shown below) after creating the first batch.

### Edit an existing group[​](#edit-an-existing-group "Direct link to Edit an existing group")

Similar to adding users to a new group, this examples assumes that changes to group membership are captured in two different dataframes that contain user emails & ids for those users you want to add or remove from the specified group.

```
# Assuming:  
# - users_to_add_csv is a dataframe with an 'email' column for users to add  
# - users_to_remove_csv is a dataframe with an 'email' column for users to remove  
# - group_id is the ID of the group to edit  
  
# Prepare the request body  
group_details_edit = {  
    "members": {  
        "remove": {},  
        "add": {}  
    }  
}  
  
# Add users if provided  
if users_to_add_csv is not None:  
    user_ids_to_add = get_user_ids_by_emails(users_to_add_csv["email"].tolist())  
    group_details_edit["members"]["add"]["users"] = [{"id": u_id} for u_id in user_ids_to_add]  
  
# Remove users if provided  
if users_to_remove_csv is not None:  
    user_ids_to_remove = get_user_ids_by_emails(users_to_remove_csv["email"].tolist())  
    group_details_edit["members"]["remove"]["users"] = [{"id": u_id} for u_id in user_ids_to_remove]  
  
# Make the API request  
params = {}  
edit_group_response = make_request(f"v1/groups/{group_id}", params, "PATCH", body=group_details_edit)  
print(f'Updated group with id {group_id}.')
```

### Delete a Group[​](#delete-a-group "Direct link to Delete a Group")

To delete a group:

```
# Assuming group_id_to_delete is the ID of the group to delete  
  
delete_group_response = make_request(f"v1/groups/{group_id_to_delete}", {}, "DELETE")  
if isinstance(delete_group_response, int):  
    print(f'Failed to delete group with id {group_id_to_delete}.')  
else:  
    print(f'Deleted group with id {group_id_to_delete}')
```

info

If you get an error message like "you are not authorized to perform this action", it is likely that the group ID you provided is not accurate or does not exist.

### Return the list of users who belong to a given group[​](#return-the-list-of-users-who-belong-to-a-given-group "Direct link to Return the list of users who belong to a given group")

The code below will return the list of users who belong to a given group id, `check_group_id`. This uses the `users` endpoint and passing in the desired membership information via the `params` argument.

```
method = 'GET'  
url = 'v1/users'  
params = {  
    'limit': 100  
    , 'groupId': check_group_id  
}  
  
check_users_in_group = helper_w_pagination(url = url, params = params, method = method)  
check_users_in_group_df = make_df(check_users_in_group)
```

## 4. Summary[​](#4-summary "Direct link to 4. Summary")

We’ve gone through some basic examples for how to use these Admin endpoints to manage the users and groups in your Hex workspace. You can download a full Hex project file below to get a functioning version of these examples and [upload](/docs/explore-data/projects/import-export) that to your own Hex workspace. While this project demonstrates some fairly straightforward methods for using these features, the details of how/what/when/why you might want to programmatically manage your Hex user base will vary!

[Download template project](/files/Admin_API_Endpoint_Example-Users_Groups.yaml)

#### On this page

* [Prerequisites](#prerequisites)
* [Resources](#resources)
* [1. Helper functions](#1-helper-functions)
  + [The basic request function](#the-basic-request-function)
  + [Pagination helper](#pagination-helper)
* [2. Work with users](#2-work-with-users)
  + [To get a list of all users in your Hex workspace:](#to-get-a-list-of-all-users-in-your-hex-workspace)
* [3. Work with groups](#3-work-with-groups)
  + [To get a list of all groups in your Hex workspace:](#to-get-a-list-of-all-groups-in-your-hex-workspace)
  + [Create a new group](#create-a-new-group)
  + [Edit an existing group](#edit-an-existing-group)
  + [Delete a Group](#delete-a-group)
  + [Return the list of users who belong to a given group](#return-the-list-of-users-who-belong-to-a-given-group)
* [4. Summary](#4-summary)