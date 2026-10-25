Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料政策稽核記錄

本文列出 BigQuery 資料政策的稽核方法。 Google Cloud 服務會產生稽核記錄，用來記錄 Google Cloud 資源中的管理和存取活動。如要進一步瞭解 Cloud 稽核記錄，請參閱以下內容：

* [稽核記錄類型](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#types)
* [稽核記錄項目結構](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#audit_log_entry_structure)
* [儲存及轉送稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#storing_and_routing_audit_logs)
* [Cloud Logging 定價摘要](https://docs.cloud.google.com/stackdriver/pricing?hl=zh-tw#logs-pricing-summary)
* [啟用資料存取稽核記錄](https://docs.cloud.google.com/logging/docs/audit/configure-data-access?hl=zh-tw)

## 服務名稱

如要查看 BigQuery 資料政策稽核記錄，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面：

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 複製下列查詢並貼到「Logs Explorer」的「Query」欄位，然後點選「Run query」。

   ```
       protoPayload.serviceName="bigquerydatapolicy.googleapis.com"
   ```

## 依權限類型區分的方法

每個 IAM 權限都具有 `type` 屬性，其值為以下四個列舉值之一：`ADMIN_READ`、`ADMIN_WRITE`、`DATA_READ` 或 `DATA_WRITE`。呼叫方法時，BigQuery Data Policy 會產生一筆稽核記錄，記錄類別依執行該方法所需權限的 `type` 屬性而定。若方法需要的 IAM 權限，`type` 屬性值為 `DATA_READ`、`DATA_WRITE` 或 `ADMIN_READ`，就會產生[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)稽核記錄；若所需 IAM 權限的 `type` 屬性值為 `ADMIN_WRITE`，則會產生[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)稽核記錄。

下表列出的 API 方法中，如標有 (LRO) 字樣，表示為長時間執行的作業。這類方法通常會產生兩個稽核記錄項目，作業開始和結束時各一個。詳情請參閱「[長時間執行的作業稽核記錄](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)」。

| 權限類型 | 方法 |
| --- | --- |
| `ADMIN_READ` | `google.cloud.bigquery.datapolicies.v1.DataPolicyService.GetDataPolicy` `google.cloud.bigquery.datapolicies.v1.DataPolicyService.GetIamPolicy` `google.cloud.bigquery.datapolicies.v1.DataPolicyService.ListDataPolicies` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.GetDataPolicy` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.GetIamPolicy` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.ListDataPolicies` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.GetDataPolicy` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.GetIamPolicy` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.ListDataPolicies` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.GetDataPolicy` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.GetIamPolicy` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.ListDataPolicies` |
| `ADMIN_WRITE` | `google.cloud.bigquery.datapolicies.v1.DataPolicyService.CreateDataPolicy` `google.cloud.bigquery.datapolicies.v1.DataPolicyService.DeleteDataPolicy` `google.cloud.bigquery.datapolicies.v1.DataPolicyService.RenameDataPolicy` `google.cloud.bigquery.datapolicies.v1.DataPolicyService.SetIamPolicy` `google.cloud.bigquery.datapolicies.v1.DataPolicyService.UpdateDataPolicy` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.CreateDataPolicy` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.DeleteDataPolicy` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.SetIamPolicy` `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.UpdateDataPolicy` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.AddGrantees` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.CreateDataPolicy` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.DeleteDataPolicy` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.RemoveGrantees` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.SetIamPolicy` `google.cloud.bigquery.datapolicies.v2.DataPolicyService.UpdateDataPolicy` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.AddGrantees` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.CreateDataPolicy` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.DeleteDataPolicy` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.RemoveGrantees` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.SetIamPolicy` `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.UpdateDataPolicy` |

## API 介面稽核記錄

如要瞭解各方法所需的權限及評估方式，請參閱 BigQuery Data Policy 的 Identity and Access Management 說明文件。

### `google.cloud.bigquery.datapolicies.v1.DataPolicyService`

屬於 `google.cloud.bigquery.datapolicies.v1.DataPolicyService` 的方法會產生以下稽核記錄。

#### `CreateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.CreateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.create - ADMIN_WRITE`
  + `datacatalog.taxonomies.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.CreateDataPolicy"`

#### `DeleteDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.DeleteDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.DeleteDataPolicy"`

#### `GetDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.GetDataPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.GetDataPolicy"`

#### `GetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.GetIamPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.getIamPolicy - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.GetIamPolicy"`

#### `ListDataPolicies`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.ListDataPolicies`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.ListDataPolicies"`

#### `RenameDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.RenameDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.RenameDataPolicy"`

#### `SetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.SetIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.SetIamPolicy"`

#### `UpdateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1.DataPolicyService.UpdateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1.DataPolicyService.UpdateDataPolicy"`

### `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService`

屬於 `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService` 的方法會產生以下稽核記錄。

#### `CreateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.CreateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.create - ADMIN_WRITE`
  + `datacatalog.taxonomies.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.CreateDataPolicy"`

#### `DeleteDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.DeleteDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.DeleteDataPolicy"`

#### `GetDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.GetDataPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.GetDataPolicy"`

#### `GetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.GetIamPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.getIamPolicy - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.GetIamPolicy"`

#### `ListDataPolicies`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.ListDataPolicies`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.ListDataPolicies"`

#### `SetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.SetIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.SetIamPolicy"`

#### `UpdateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.UpdateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.UpdateDataPolicy"`

### `google.cloud.bigquery.datapolicies.v2.DataPolicyService`

屬於 `google.cloud.bigquery.datapolicies.v2.DataPolicyService` 的方法會產生以下稽核記錄。

#### `AddGrantees`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.AddGrantees`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.AddGrantees"`

#### `CreateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.CreateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.CreateDataPolicy"`

#### `DeleteDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.DeleteDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.DeleteDataPolicy"`

#### `GetDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.GetDataPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.GetDataPolicy"`

#### `GetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.GetIamPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.getIamPolicy - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.GetIamPolicy"`

#### `ListDataPolicies`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.ListDataPolicies`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.ListDataPolicies"`

#### `RemoveGrantees`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.RemoveGrantees`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.RemoveGrantees"`

#### `SetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.SetIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.SetIamPolicy"`

#### `UpdateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2.DataPolicyService.UpdateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2.DataPolicyService.UpdateDataPolicy"`

### `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService`

屬於 `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService` 的方法會產生以下稽核記錄。

#### `AddGrantees`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.AddGrantees`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.AddGrantees"`

#### `CreateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.CreateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.CreateDataPolicy"`

#### `DeleteDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.DeleteDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.DeleteDataPolicy"`

#### `GetDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.GetDataPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.GetDataPolicy"`

#### `GetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.GetIamPolicy`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.getIamPolicy - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.GetIamPolicy"`

#### `ListDataPolicies`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.ListDataPolicies`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.dataPolicies.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.ListDataPolicies"`

#### `RemoveGrantees`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.RemoveGrantees`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.RemoveGrantees"`

#### `SetIamPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.SetIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.SetIamPolicy"`

#### `UpdateDataPolicy`

* **方法**：`google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.UpdateDataPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.dataPolicies.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.UpdateDataPolicy"`

## 不會產生稽核記錄的方法

某些方法可能不會產生稽核記錄，原因包括以下一或多項：

* 該方法的流量使用量高，若產生稽核記錄，會導致記錄與儲存成本過高。
* 稽核價值低。
* 其他稽核記錄或平台記錄已涵蓋該方法的活動。

下列方法不會產生稽核記錄：

* `google.cloud.bigquery.datapolicies.v1.DataPolicyService.TestIamPermissions`
* `google.cloud.bigquery.datapolicies.v1beta1.DataPolicyService.TestIamPermissions`
* `google.cloud.bigquery.datapolicies.v2.DataPolicyService.TestIamPermissions`
* `google.cloud.bigquery.datapolicies.v2beta1.DataPolicyService.TestIamPermissions`




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]