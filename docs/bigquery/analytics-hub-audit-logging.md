Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 共用稽核記錄

BigQuery sharing 的 Cloud 稽核記錄可讓您追蹤資源的管理和資料存取作業，協助您監控存取權和設定變更。您可以在 Logs Explorer 中查詢這些記錄，並查看哪些 BigQuery sharing API 方法會產生 Cloud 稽核記錄。

如要進一步瞭解 Cloud 稽核記錄，請參閱下列文件：

* [稽核記錄類型](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#types)
* [稽核記錄項目結構](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#audit_log_entry_structure)
* [儲存及轉送稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#storing_and_routing_audit_logs)
* [Cloud Logging 定價摘要](https://docs.cloud.google.com/stackdriver/pricing?hl=zh-tw#logs-pricing-summary)
* [啟用資料存取稽核記錄](https://docs.cloud.google.com/logging/docs/audit/configure-data-access?hl=zh-tw)

## 服務名稱

如要查看 BigQuery sharing 稽核記錄，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面：

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 複製下列查詢並貼到 Logs Explorer 的「Query」(查詢) 欄位，然後按一下「Run query」(執行查詢)。

   ```
       protoPayload.serviceName="analyticshub.googleapis.com"
   ```

## 依權限類型區分的方法

每個 IAM 權限都具有 `type` 屬性，其值為以下四個列舉值之一：`ADMIN_READ`、`ADMIN_WRITE`、`DATA_READ` 或 `DATA_WRITE`。呼叫方法時，BigQuery sharing 會產生一筆稽核記錄，類別取決於執行該方法所需權限的 `type` 屬性。若方法需要的 IAM 權限，`type` 屬性值為 `DATA_READ`、`DATA_WRITE` 或 `ADMIN_READ`，就會產生[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)稽核記錄；若所需 IAM 權限的 `type` 屬性值為 `ADMIN_WRITE`，則會產生[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)稽核記錄。

下表列出的 API 方法中，如標有 (LRO) 字樣，表示為長時間執行的作業。這類方法通常會產生兩個稽核記錄項目，作業開始和結束時各一個。詳情請參閱「[長時間執行的作業稽核記錄](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)」。

| 權限類型 | 方法 |
| --- | --- |
| `ADMIN_READ` | `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetDataExchange` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetIamPolicy` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetListing` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetSubscription` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListDataExchanges` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListListings` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListOrgDataExchanges` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListSharedResourceSubscriptions` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListSubscriptions` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetDataExchange` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetIamPolicy` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetListing` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListDataExchanges` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListListings` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListOrgDataExchanges` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.SubscribeListing` |
| `ADMIN_WRITE` | `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.CreateDataExchange` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.CreateListing` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteDataExchange` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteListing` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteSubscription` (LRO) `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.RefreshSubscription` (LRO) `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.RevokeSubscription` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SetIamPolicy` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SubscribeDataExchange` (LRO) `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SubscribeListing` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.UpdateDataExchange` `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.UpdateListing` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.CreateDataExchange` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.CreateListing` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.DeleteDataExchange` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.DeleteListing` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.SetIamPolicy` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.UpdateDataExchange` `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.UpdateListing` |

## API 介面稽核記錄

如要瞭解各方法所需的權限及評估方式，請參閱 BigQuery 共用功能的 Identity and Access Management 說明文件。

### `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService`

屬於 `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService` 的方法會產生以下稽核記錄。

#### `CreateDataExchange`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.CreateDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.CreateDataExchange"`

#### `CreateListing`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.CreateListing`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.CreateListing"`

#### `DeleteDataExchange`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteDataExchange"`

#### `DeleteListing`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteListing`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteListing"`

#### `DeleteSubscription`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteSubscription`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.subscribe - ADMIN_WRITE`
  + `analyticshub.subscriptions.delete - ADMIN_WRITE`
* **方法的作業種類**：
  [**長時間執行的作業**](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.DeleteSubscription"`

#### `GetDataExchange`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetDataExchange`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetDataExchange"`

#### `GetIamPolicy`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetIamPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.getIamPolicy - ADMIN_READ`
  + `analyticshub.listings.getIamPolicy - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetIamPolicy"`

#### `GetListing`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetListing`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetListing"`

#### `GetSubscription`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetSubscription`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.subscriptions.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.GetSubscription"`

#### `ListDataExchanges`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListDataExchanges`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListDataExchanges"`

#### `ListListings`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListListings`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListListings"`

#### `ListOrgDataExchanges`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListOrgDataExchanges`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListOrgDataExchanges"`

#### `ListSharedResourceSubscriptions`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListSharedResourceSubscriptions`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.viewSubscriptions - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListSharedResourceSubscriptions"`

#### `ListSubscriptions`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListSubscriptions`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.subscriptions.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.ListSubscriptions"`

#### `RefreshSubscription`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.RefreshSubscription`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.subscriptions.update - ADMIN_WRITE`
* **方法的作業種類**：
  [**長時間執行的作業**](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.RefreshSubscription"`

#### `RevokeSubscription`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.RevokeSubscription`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.update - ADMIN_WRITE`
  + `analyticshub.listings.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.RevokeSubscription"`

#### `SetIamPolicy`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SetIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SetIamPolicy"`

#### `SubscribeDataExchange`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SubscribeDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.subscriptions.create - ADMIN_WRITE`
* **方法的作業種類**：
  [**長時間執行的作業**](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SubscribeDataExchange"`

#### `SubscribeListing`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SubscribeListing`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.subscribe - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.SubscribeListing"`

#### `UpdateDataExchange`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.UpdateDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.UpdateDataExchange"`

#### `UpdateListing`

* **方法**：`google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.UpdateListing`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.UpdateListing"`

### `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService`

屬於 `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService` 的方法會產生以下稽核記錄。

#### `CreateDataExchange`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.CreateDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.CreateDataExchange"`

#### `CreateListing`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.CreateListing`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.CreateListing"`

#### `DeleteDataExchange`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.DeleteDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.DeleteDataExchange"`

#### `DeleteListing`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.DeleteListing`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.DeleteListing"`

#### `GetDataExchange`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetDataExchange`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetDataExchange"`

#### `GetIamPolicy`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetIamPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.getIamPolicy - ADMIN_READ`
  + `analyticshub.listings.getIamPolicy - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetIamPolicy"`

#### `GetListing`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetListing`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.GetListing"`

#### `ListDataExchanges`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListDataExchanges`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListDataExchanges"`

#### `ListListings`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListListings`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListListings"`

#### `ListOrgDataExchanges`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListOrgDataExchanges`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.dataExchanges.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.ListOrgDataExchanges"`

#### `SetIamPolicy`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.SetIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.SetIamPolicy"`

#### `SubscribeListing`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.SubscribeListing`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `analyticshub.listings.subscribe - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.SubscribeListing"`

#### `UpdateDataExchange`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.UpdateDataExchange`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.dataExchanges.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.UpdateDataExchange"`

#### `UpdateListing`

* **方法**：`google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.UpdateListing`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `analyticshub.listings.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.UpdateListing"`

## 不會產生稽核記錄的方法

某些方法可能不會產生稽核記錄，原因包括以下一或多項：

* 該方法的流量使用量高，若產生稽核記錄，會導致記錄與儲存成本過高。
* 稽核價值低。
* 其他稽核記錄或平台記錄已涵蓋該方法的活動。

下列方法不會產生稽核記錄：

* `google.cloud.bigquery.analyticshub.v1.AnalyticsHubService.TestIamPermissions`
* `google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService.TestIamPermissions`




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]