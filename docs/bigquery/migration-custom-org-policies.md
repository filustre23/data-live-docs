* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Guides](https://docs.cloud.google.com/bigquery/docs/introduction)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Custom Org Policies for BigQuery Migration Service

This page shows you how to use Organization Policy Service custom constraints to restrict
specific operations on the following Google Cloud resources:

* `bigquerymigration.googleapis.com/MigrationWorkflow`

To learn more about Organization Policy, see
[Custom organization policies](/organization-policy/overview#custom-organization-policies).

## About organization policies and constraints

The Google Cloud Organization Policy Service gives you centralized, programmatic
control over your organization's resources. As the
[organization policy administrator](/iam/docs/roles-permissions/orgpolicy#orgpolicy.policyAdmin), you can define an organization
policy, which is a set of restrictions called *constraints* that apply to
Google Cloud resources and descendants of those resources in the
[Google Cloud resource hierarchy](/resource-manager/docs/cloud-platform-resource-hierarchy). You can enforce organization
policies at the organization, folder, or project level.

Organization Policy provides built-in [managed constraints](/organization-policy/reference/org-policy-constraints)
for various Google Cloud services. However, if you want more granular,
customizable control over the specific fields that are restricted in your
organization policies, you can also create *custom constraints* and use those
custom constraints in an organization policy.

### Policy inheritance

By default, organization policies are inherited by the descendants of the
resources on which you enforce the policy. For example, if you enforce a policy
on a folder, Google Cloud enforces the policy on all projects in the
folder. To learn more about this behavior and how to change it, refer to
[Hierarchy evaluation rules](/organization-policy/hierarchy-evaluation#disallow_inheritance).

## Before you begin

- Sign in to your Google Cloud account. If you're new to
  Google Cloud, [create an account](https://console.cloud.google.com/freetrial) to evaluate how our products perform in
  real-world scenarios. New customers also get $300 in free credits to
  run, test, and deploy workloads.
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](/iam/docs/granting-changing-revoking-access).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- [Install](/sdk/docs/install) the Google Cloud CLI.
- If you're using an external identity provider (IdP), you must first
  [sign in to the gcloud CLI with your federated identity](/iam/docs/workforce-log-in-gcloud).
- To [initialize](/sdk/docs/initializing) the gcloud CLI, run the following command:

  ```
  gcloud init
  ```

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](/iam/docs/granting-changing-revoking-access).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- [Install](/sdk/docs/install) the Google Cloud CLI.
- If you're using an external identity provider (IdP), you must first
  [sign in to the gcloud CLI with your federated identity](/iam/docs/workforce-log-in-gcloud).
- To [initialize](/sdk/docs/initializing) the gcloud CLI, run the following command:

  ```
  gcloud init
  ```

1. Ensure that you know your
   [organization ID](/resource-manager/docs/creating-managing-organization#retrieving_your_organization_id).

### Required roles

To get the permissions that
you need to manage custom organization policies,
ask your administrator to grant you the
[Organization Policy Administrator](/iam/docs/roles-permissions/orgpolicy#orgpolicy.policyAdmin)  (`roles/orgpolicy.policyAdmin`)
IAM role on the organization resource.
For more information about granting roles, see [Manage access to projects, folders, and organizations](/iam/docs/granting-changing-revoking-access).

You might also be able to get
the required permissions through [custom
roles](/iam/docs/creating-custom-roles) or other [predefined
roles](/iam/docs/roles-overview#predefined).

## BigQuery supported resources

The following table lists the BigQuery resources that you can reference
in custom constraints.

| Resource | Field |
| --- | --- |
| bigquerymigration.googleapis.com/MigrationWorkflow | `resource.displayName` |
| `resource.tasks[*].assessmentTaskDetails.dataSource` |
| `resource.tasks[*].assessmentTaskDetails.featureHandle.addShareableDataset` |
| `resource.tasks[*].assessmentTaskDetails.inputPath` |
| `resource.tasks[*].assessmentTaskDetails.outputDataset` |
| `resource.tasks[*].assessmentTaskDetails.querylogsPath` |
| `resource.tasks[*].translationConfigDetails.gcsSourcePath` |
| `resource.tasks[*].translationConfigDetails.gcsTargetPath` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.source.attribute` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.source.database` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.source.relation` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.source.schema` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.source.type` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.target.attribute` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.target.database` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.target.relation` |
| `resource.tasks[*].translationConfigDetails.nameMappingList.nameMap.target.schema` |
| `resource.tasks[*].translationConfigDetails.requestSource` |
| `resource.tasks[*].translationConfigDetails.sourceDialect.teradataDialect.mode` |
| `resource.tasks[*].translationConfigDetails.sourceEnv.defaultDatabase` |
| `resource.tasks[*].translationConfigDetails.sourceEnv.metadataStoreDataset` |
| `resource.tasks[*].translationConfigDetails.sourceEnv.schemaSearchPath` |
| `resource.tasks[*].translationConfigDetails.targetDialect.teradataDialect.mode` |
| `resource.tasks[*].translationConfigDetails.targetTypes` |
| `resource.tasks[*].translationDetails.sourceEnvironment.defaultDatabase` |
| `resource.tasks[*].translationDetails.sourceEnvironment.metadataStoreDataset` |
| `resource.tasks[*].translationDetails.sourceEnvironment.schemaSearchPath` |
| `resource.tasks[*].translationDetails.sourceTargetMapping.sourceSpec.baseUri` |
| `resource.tasks[*].translationDetails.sourceTargetMapping.sourceSpec.encoding` |
| `resource.tasks[*].translationDetails.sourceTargetMapping.sourceSpec.literal.relativePath` |
| `resource.tasks[*].translationDetails.sourceTargetMapping.targetSpec.relativePath` |
| `resource.tasks[*].translationDetails.suggestionConfig.skipSuggestionSteps.rewriteTarget` |
| `resource.tasks[*].translationDetails.suggestionConfig.skipSuggestionSteps.suggestionType` |
| `resource.tasks[*].translationDetails.targetBaseUri` |
| `resource.tasks[*].translationDetails.targetReturnLiterals` |
| `resource.tasks[*].translationDetails.targetTypes` |
| `resource.tasks[*].type` |

## Set up a custom constraint

A custom constraint is defined in a YAML file by the resources, methods,
conditions, and actions that are supported by the service on which you are
enforcing the organization policy. Conditions for your custom constraints are
defined using
[Common Expression Language (CEL)](https://github.com/google/cel-spec/blob/master/doc/intro.md). For more information about how to build
conditions in custom constraints using CEL, see the CEL section of
[Creating and managing custom constraints](/organization-policy/create-custom-constraints#common_expression_language).

### Console

To create a custom constraint, do the following:

1. In the Google Cloud console, go to the **Organization policies** page.

   [Go to Organization policies](https://console.cloud.google.com/iam-admin/orgpolicies)
2. From the project picker, select the project that you want to set the organization
   policy for.
3. Click add **Custom constraint**.
4. In the **Display name** box, enter a human-readable name for the constraint. This name is
   used in error messages and can be used for identification and debugging. Don't use
   personally identifiable information (PII) or sensitive data in display names because this
   name could be exposed in error messages. This field can contain up to 200 characters.
5. In the **Constraint ID** box, enter the ID that you want for your new custom
   constraint. A custom constraint can only contain letters (including upper and lowercase) or
   numbers, for example `custom.requireAssessmentTask`. This field can contain up to
   70 characters, not counting the prefix (`custom.`), for example,
   `organizations/123456789/customConstraints/custom`. Don't include PII or
   sensitive data in your constraint ID, because it could be exposed in error messages.
6. In the **Description** box, enter a human-readable description of the constraint. This
   description is used as an error message when the policy is violated. Include details about
   why the policy violation occurred and how to resolve the policy violation. Don't include
   PII or sensitive data in your description, because it could be exposed in error messages.
   This field can contain up to 2000 characters.
7. In the **Resource type** box, select the name of the Google Cloud REST resource
   containing the object and field that you want to restrict—for example,
   `container.googleapis.com/NodePool`. Most resource types support up to 20 custom
   constraints. If you attempt to create more custom constraints, the operation fails.
8. Under **Enforcement method**, select whether to enforce the
   constraint on a REST `CREATE` method or both `CREATE` and
   `UPDATE` methods. If you enforce the constraint with the `UPDATE`
   method on a resource that violates the constraint, changes to that resource are blocked by
   the organization policy unless the change resolves the violation.

To see supported methods for each service, find the service in
[Services that support custom constraints](/organization-policy/reference/custom-constraint-supported-services).

9. To define a condition, click edit **Edit condition**.

1. In the **Add condition** panel, create a CEL condition that refers to a supported
   service resource, for example, `resource.management.autoUpgrade == false`. This
   field can contain up to 1000 characters. For details about CEL usage, see
   [Common Expression Language](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language).
   For more information about the service resources you can use in your custom constraints,
   see [Custom constraint supported services](/resource-manager/docs/organization-policy/custom-constraint-supported-services).
2. Click **Save**.

10. Under **Action**, select whether to allow or deny the evaluated method if the condition
    is met.

The deny action means that the operation to create or update the resource is blocked if the
condition evaluates to true.

The allow action means that the operation to create or update the resource is permitted only
if the condition evaluates to true. Every other case except those explicitly listed in the
condition is blocked.

11. Click **Create constraint**.

When you have entered a value into each field, the equivalent YAML configuration for this
custom constraint appears on the right.

### gcloud

1. To create a custom constraint, create a YAML file using the following format:

```
name: organizations/ORGANIZATION_ID/customConstraints/CONSTRAINT_NAME
resourceTypes: RESOURCE_NAME
methodTypes:
  - CREATE  
  - UPDATE 
condition: "CONDITION"
actionType: ACTION
displayName: DISPLAY_NAME
description: DESCRIPTION
```

Replace the following:

* `ORGANIZATION_ID`: your organization ID, such as
  `123456789`.
* `CONSTRAINT_NAME`: the name that you want for your new custom
  constraint. A custom constraint can only contain letters (including upper and lowercase)
  or numbers, for example, `custom.requireAssessmentTask`. This field can contain up to 70
  characters, not counting the prefix (`custom.`)— for example,
  `organizations/123456789/customConstraints/custom`. Don't include PII or
  sensitive data in your constraint ID, because it could be exposed in error messages.
* `RESOURCE_NAME`: the fully qualified name of the Google Cloud
  resource containing the object and field that you want to restrict. For example,
  `bigquerymigration.googleapis.com/MigrationWorkflow`. Most resource types support up to 20 custom
  constraints. If you attempt to create more custom constraints, the operation fails.
* `methodTypes`: the REST methods that the constraint is enforced on.
  Can be `CREATE` or both `CREATE` and
  `UPDATE`. If you enforce the constraint with the `UPDATE` method on
  a resource that violates the constraint, changes to that resource are blocked by the
  organization policy unless the change resolves the violation.

To see the supported methods for each service, find the service in
[Services that support custom constraints](/organization-policy/reference/custom-constraint-supported-services).

* `CONDITION`: a [CEL condition](/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language) that is written against a representation of a supported service
  resource. This field can contain up to 1000 characters. For example,
  `resource.tasks.all(k, resource.tasks[k].type.startsWith('Assessment'))`.

For more information about the resources available to write conditions against, see
[Supported resources](#supported_resources).

* `ACTION`: the action to take if the `condition` is met.
  Possible values are `ALLOW` and
  `DENY`.

The allow action means that if the condition evaluates to true, the operation to create or
update the resource is permitted. This also means that every other case except the one
explicitly listed in the condition is blocked.

The deny action means that if the condition evaluates to true, the operation to create or
update the resource is blocked.

* `DISPLAY_NAME`: a human-readable name for the constraint. This name
  is used in error messages and can be used for identification and debugging. Don't use PII
  or sensitive data in display names because this name could be exposed in error messages.
  This field can contain up to 200 characters.
* `DESCRIPTION`: a human-friendly description of the constraint to
  display as an error message when the policy is violated. This field can contain up to
  2000 characters.

2. After you have created the YAML file for a new custom constraint, you must set it up to make
   it available for organization policies in your organization. To set up a custom constraint,
   use the
   [`gcloud org-policies set-custom-constraint`](/sdk/gcloud/reference/org-policies/set-custom-constraint) command:

```
gcloud org-policies set-custom-constraint CONSTRAINT_PATH
```

Replace `CONSTRAINT_PATH` with the full path to your custom constraint
file. For example, `/home/user/customconstraint.yaml`.

After this operation is complete, your custom constraints are available as organization
policies in your list of Google Cloud organization policies.

3. To verify that the custom constraint exists, use the
   [`gcloud org-policies list-custom-constraints`](/sdk/gcloud/reference/org-policies/list-custom-constraints) command:

```
gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
```

Replace `ORGANIZATION_ID` with the ID of your organization resource.

For more information, see
[Viewing organization policies](/resource-manager/docs/organization-policy/creating-managing-policies#viewing_organization_policies).

## Enforce a custom organization policy

You can enforce a constraint by creating an organization policy that references it, and then
applying that organization policy to a Google Cloud resource.

### Console

1. In the Google Cloud console, go to the **Organization policies** page.

   [Go to Organization policies](https://console.cloud.google.com/iam-admin/orgpolicies)
2. From the project picker, select the project that you want to set the
   organization policy for.
3. From the list on the **Organization policies** page, select your constraint to view
   the **Policy details** page for that constraint.
4. To configure the organization policy for this resource, click **Manage policy**.
5. On the **Edit policy** page, select **Override parent's policy**.
6. Click **Add a rule**.
7. In the **Enforcement** section, select whether this organization policy is enforced or
   not.
8. Optional: To make the organization policy conditional on a tag, click
   **Add condition**. Note that if you add a conditional rule to an organization
   policy, you must add at least one unconditional rule or the policy cannot be saved. For more
   information, see
   [Scope organization policies with tags](/organization-policy/scope-policies).
9. Click **Test changes** to simulate the effect of the organization policy. For more
   information, see [Test organization policy changes with Policy Simulator](/policy-intelligence/docs/test-organization-policies).
10. To enforce the organization policy in dry-run mode, click **Set dry run policy**. For
    more information, see [Test organization policies](/organization-policy/test-policies).
11. After you verify that the organization policy in dry-run mode works as intended, set the
    live policy by clicking **Set policy**.

### gcloud

1. To create an organization policy with boolean rules, create a policy YAML file that
   references the constraint:

```
name: projects/PROJECT_ID/policies/CONSTRAINT_NAME
spec:
  rules:
  - enforce: true

dryRunSpec:
  rules:
  - enforce: true
```

Replace the following:

* `PROJECT_ID`: the project that you want to enforce your constraint
  on.
* `CONSTRAINT_NAME`: the name you defined for your custom constraint. For
  example, `custom.requireAssessmentTask`.

2. To enforce the organization policy in
   [dry-run mode](/organization-policy/test-policies), run
   the following command with the `dryRunSpec` flag:

```
gcloud org-policies set-policy POLICY_PATH --update-mask=dryRunSpec
```

Replace `POLICY_PATH` with the full path to your organization policy
YAML file. The policy requires up to 15 minutes to take effect.

3. After you verify that the organization policy in dry-run mode works as intended, set the
   live policy with the `org-policies set-policy` command and the `spec`
   flag:

```
gcloud org-policies set-policy POLICY_PATH --update-mask=spec
```

Replace `POLICY_PATH` with the full path to your organization policy
YAML file. The policy requires up to 15 minutes to take effect.

## Test the custom organization policy

The following example creates a custom constraint and policy that require all
new migration workflows in a specific project to have a task type starting
with `Assessment`. Use this custom organization policy if you want to specify
that a project should only be used for migration assessments.

Before you begin, have the following information:

* Your organization ID
* The project ID this custom organization policy is applied to

### Create the constraint

1. Save the following file as `constraint-assessment-tasks.yaml`:

   ```
   name: organizations/ORGANIZATION_ID/customConstraints/custom.requireAssessmentTask
   resourceTypes:
   - bigquerymigration.googleapis.com/MigrationWorkflow
   methodTypes:
   - CREATE
   condition: resource.tasks.all(k, resource.tasks[k].type.startsWith('Assessment'))
   condition: resource.tasks.all(k, resource.tasks[k].type.startsWith('Assessment'))
   actionType: ALLOW
   displayName: Only assessment tasks are allowed
   description: Workflows must not contain a task of type 'Assessment'.
   ```
2. Apply the constraint:

   ```
   gcloud org-policies set-custom-constraint ~/constraint-assessment-tasks.yaml
   ```
3. Verify that the constraint exists:

   ```
   gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
   ```

   The output is similar to the following:

   ```
   CUSTOM_CONSTRAINT                       ACTION_TYPE  METHOD_TYPES   RESOURCE_TYPES                                       DISPLAY_NAME
   custom.requireAssessmentTask            DENY         CREATE         bigquerymigration.googleapis.com/MigrationWorkflow   Only assessment tasks are allowed
   ...
   ```

### Create the policy

1. Save the following file as `policy-assessment-tasks.yaml`:

   ```
   name: projects/PROJECT_ID/policies/custom.requireAssessmentTask
   spec:
     rules:
     - enforce: true
   ```

   Replace `PROJECT_ID` with your project ID.
2. Apply the policy:

   ```
   gcloud org-policies set-policy ~/policy-enable-autopilot.yaml
   ```
3. Verify that the policy exists:

   ```
   gcloud org-policies list --project=PROJECT_ID
   ```

   The output is similar to the following:

   ```
   CONSTRAINT                   LIST_POLICY    BOOLEAN_POLICY    ETAG
   custom.requireAssessmentTask -              SET               CNPA+sYGEOC88P8C-
   ```

After you apply the policy, wait about two minutes for Google Cloud to
start enforcing the policy.

### Test the policy

To test the custom organization policy, you can try to create a non-assessment
workflow. To do this, first create a `workflow.json` file`, similar to the
following example:

```
{
  "tasks": {
      "my_task": {
        "type": "Teradata2BigQuery_Translation",
        "translation_details": {
          "target_base_uri": "gs://some_bucket/target",
          "source_target_mapping": {
            "source_spec": {
              "base_uri": "gs://some_bucket/dataset/"
            }
          },
          "source_target_mapping": {
            "source_spec": {
              "literal": {
                "relative_path": ".",
                "literal_string": "SELECT * FROM my_table;"
              }
            }
          },
          "target_return_literals": "sql/."
        }
      }  },
  "display_name": "Translation request"
}
```

Once you have created a `workflow.json` file, try to create the workflow with
the following command:

```
bq mk --migration_workflow --location=us --config_file=workflow.json --project_id="PROJECT_ID"
```

Replace `PROJECT_ID` with your project ID.

If you see a permission denied error, then your policy is successfully applied.

## What's next

* Learn more about
  [Organization Policy Service](/organization-policy/overview).
* Learn more about how to
  [create and manage organization policies](/organization-policy/create-organization-policies).
* See the full list of managed
  [organization policy constraints](/organization-policy/reference/org-policy-constraints).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]