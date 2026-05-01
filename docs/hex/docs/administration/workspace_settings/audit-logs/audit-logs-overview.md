On this page

# Audit logs overview

View audit logs through Hex or stream to your own SIEM provider.

Audit logs are a record of the activities that occurred in the Hex platform, intended for use by security and compliance teams. They capture actions that are pre-defined in the Hex product, including activities related to projects, collections, cells, users and more. For a complete list of events captured in audit logs, please see the [Audit log event reference page](/docs/administration/workspace_settings/audit-logs/audit-logs-reference).

info

* Available on the Enterprise [plan](https://hex.tech/pricing)
* Only workspace [Admins](/docs/collaborate/sharing-and-permissions/roles) can access audit logs

## Accessing audit logs[​](#accessing-audit-logs "Direct link to Accessing audit logs")

Audit logs are located in Settings under Access and Security. Once in the audit log page, click the button to enable audit logs for the workspace.

With audit logs enabled, you have the option to view audit logs through WorkOS or configure log stream to your Security Information and Event Management (SIEM) provider.

## View audit logs[​](#view-audit-logs "Direct link to View audit logs")

Hex uses WorkOS as the user interface for audit logs. Once they are enabled in Hex, clicking the “View audit logs” button will take you to the WorkOS page with your logs. Within the WorkOS interface, you will see each event along with the actor and date and time. Clicking into the log will provide a JSON with details about the event. You also have the option to Export the logs as a CSV.

The UI shows audit log records from the past thirty (30) days.

## Configure log stream[​](#configure-log-stream "Direct link to Configure log stream")

Audit logs can be configured to stream directly to your Security Information and Event Management (SIEM) provider for you to monitor and work with alongside events from other cloud services. This also gives you control over how much historical data you want to keep.

Hex supports streaming to Amazon S3, Datadog, Splunk, and Google Cloud Storage. Click on “Configure log stream” and follow the step by step instructions provided by WorkOS to set up the stream for your SIEM or cloud storage provider.

#### On this page

* [Accessing audit logs](#accessing-audit-logs)
* [View audit logs](#view-audit-logs)
* [Configure log stream](#configure-log-stream)