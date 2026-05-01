* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# AuditConfig Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [AuditLogConfig](#AuditLogConfig)
  + [JSON representation](#AuditLogConfig.SCHEMA_REPRESENTATION)

Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs.

If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log\_types specified in each AuditConfig are enabled, and the exemptedMembers in each AuditLogConfig are exempted.

Example Policy with multiple AuditConfigs:

```
{
  "auditConfigs": [
    {
      "service": "allServices",
      "auditLogConfigs": [
        {
          "logType": "DATA_READ",
          "exemptedMembers": [
            "user:jose@example.com"
          ]
        },
        {
          "logType": "DATA_WRITE"
        },
        {
          "logType": "ADMIN_READ"
        }
      ]
    },
    {
      "service": "sampleservice.googleapis.com",
      "auditLogConfigs": [
        {
          "logType": "DATA_READ"
        },
        {
          "logType": "DATA_WRITE",
          "exemptedMembers": [
            "user:aliya@example.com"
          ]
        }
      ]
    }
  ]
}
```

For sampleservice, this policy enables DATA\_READ, DATA\_WRITE and ADMIN\_READ logging. It also exempts `jose@example.com` from DATA\_READ logging, and `aliya@example.com` from DATA\_WRITE logging.

| JSON representation |
| --- |
| ``` {   "service": string,   "auditLogConfigs": [     {       object (AuditLogConfig)     }   ] } ``` |

| Fields | |
| --- | --- |
| `service` | `string`  Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services. |
| `auditLogConfigs[]` | `object (AuditLogConfig)`  The configuration for logging of each type of permission. |

## AuditLogConfig

Provides the configuration for logging a type of permissions. Example:

```
{
  "auditLogConfigs": [
    {
      "logType": "DATA_READ",
      "exemptedMembers": [
        "user:jose@example.com"
      ]
    },
    {
      "logType": "DATA_WRITE"
    }
  ]
}
```

This enables 'DATA\_READ' and 'DATA\_WRITE' logging, while exempting [jose@example.com](mailto:jose@example.com) from DATA\_READ logging.

| JSON representation |
| --- |
| ``` {   "logType": enum (LogType),   "exemptedMembers": [     string   ] } ``` |

| Fields | |
| --- | --- |
| `logType` | `enum (LogType)`  The log type that this config enables. |
| `exemptedMembers[]` | `string`  Specifies the identities that do not cause logging for this type of permission. Follows the same format of `Binding.members`. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]