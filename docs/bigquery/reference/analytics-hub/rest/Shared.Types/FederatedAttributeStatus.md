* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# FederatedAttributeStatus Stay organized with collections Save and categorize content based on your preferences.

Explicit indication of why a particular federated attribute is not included in a request. This is necessary because the server needs to behave differently if an attribute is federated and known to be empty than if the caller is expecting IAM to read it from central storage. It also allows the server to identify requests where the caller failed to populate a particular attribute due to a bug. If the resource doesn't exist, then use FEDERATED\_AND\_EMPTY.

| Enums | |
| --- | --- |
| `FEDERATION_STATUS_UNSET` |  |
| `NOT_FEDERATED` | This attribute is not provided in the request and instead should be read from IAM central storage. |
| `FEDERATED_AND_EMPTY` | This attribute is stored by the calling service, but is empty or unset for this particular resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]