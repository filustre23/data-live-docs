* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigLake 稽核記錄

本文說明 BigLake 的稽核記錄功能。 Google Cloud 服務會產生稽核記錄，用以記錄 Google Cloud 資源中的管理和存取活動。如要進一步瞭解 Cloud 稽核記錄，請參閱以下內容：

* [稽核記錄類型](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#types)
* [稽核記錄項目結構](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#audit_log_entry_structure)
* [儲存及轉送稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#storing_and_routing_audit_logs)
* [Cloud Logging 定價摘要](https://docs.cloud.google.com/stackdriver/pricing?hl=zh-tw#logs-pricing-summary)
* [啟用資料存取稽核記錄](https://docs.cloud.google.com/logging/docs/audit/configure-data-access?hl=zh-tw)

## 服務名稱

BigLake 稽核記錄會使用服務名稱 `biglake.googleapis.com`。如要篩選此服務，請使用：

```
    protoPayload.serviceName="biglake.googleapis.com"
```

## 按權限類型劃分的方法

每個 IAM 權限都具有 `type` 屬性，其值為以下四個列舉值之一：`ADMIN_READ`、`ADMIN_WRITE`、`DATA_READ` 或 `DATA_WRITE`。呼叫方法時，BigLake 會產生一筆稽核記錄，記錄類別依執行該方法所需權限的 `type` 屬性而定。若方法需要的 IAM 權限，`type` 屬性值為 `DATA_READ`、`DATA_WRITE` 或 `ADMIN_READ`，就會產生[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)稽核記錄；若所需 IAM 權限的 `type` 屬性值為 `ADMIN_WRITE`，則會產生[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)稽核記錄。

下表列出的 API 方法中，如標有 (LRO) 字樣，表示為長時間執行的作業。這類方法通常會產生兩個稽核記錄項目，作業開始和結束時各一個。詳情請參閱「[長時間執行的作業稽核記錄](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)」。

| 權限類型 | 方法 |
| --- | --- |
| `ADMIN_READ` | `google.cloud.bigquery.biglake.v1.MetastoreService.GetCatalog` `google.cloud.bigquery.biglake.v1.MetastoreService.GetDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.GetTable` `google.cloud.bigquery.biglake.v1.MetastoreService.ListCatalogs` `google.cloud.bigquery.biglake.v1.MetastoreService.ListDatabases` `google.cloud.bigquery.biglake.v1.MetastoreService.ListTables` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetCatalog` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListCatalogs` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListDatabases` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListLocks` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListTables` |
| `ADMIN_WRITE` | `google.cloud.bigquery.biglake.v1.MetastoreService.CreateCatalog` `google.cloud.bigquery.biglake.v1.MetastoreService.CreateDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.CreateTable` `google.cloud.bigquery.biglake.v1.MetastoreService.DeleteCatalog` `google.cloud.bigquery.biglake.v1.MetastoreService.DeleteDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.DeleteTable` `google.cloud.bigquery.biglake.v1.MetastoreService.RenameTable` `google.cloud.bigquery.biglake.v1.MetastoreService.UpdateDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.UpdateTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CheckLock` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateCatalog` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateLock` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteCatalog` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteLock` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.RenameTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateTable` |

## API 介面稽核記錄

如要瞭解各方法所需的權限及評估方式，請參閱 BigLake 的 Identity and Access Management 說明文件。

### `google.cloud.bigquery.biglake.v1.MetastoreService`

屬於 `google.cloud.bigquery.biglake.v1.MetastoreService` 的方法會產生以下稽核記錄。

#### `CreateCatalog`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.CreateCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.CreateCatalog"`

#### `CreateDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.CreateDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.databases.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.CreateDatabase"`

#### `CreateTable`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.CreateTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.CreateTable"`

#### `DeleteCatalog`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.DeleteCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.DeleteCatalog"`

#### `DeleteDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.DeleteDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.databases.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.DeleteDatabase"`

#### `DeleteTable`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.DeleteTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.DeleteTable"`

#### `GetCatalog`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.GetCatalog`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.GetCatalog"`

#### `GetDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.GetDatabase`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.databases.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.GetDatabase"`

#### `GetTable`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.GetTable`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.GetTable"`

#### `ListCatalogs`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.ListCatalogs`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.ListCatalogs"`

#### `ListDatabases`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.ListDatabases`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.databases.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.ListDatabases"`

#### `ListTables`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.ListTables`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.ListTables"`

#### `RenameTable`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.RenameTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.RenameTable"`

#### `UpdateDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.UpdateDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.databases.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.UpdateDatabase"`

#### `UpdateTable`

* **方法**：`google.cloud.bigquery.biglake.v1.MetastoreService.UpdateTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1.MetastoreService.UpdateTable"`

### `google.cloud.bigquery.biglake.v1alpha1.MetastoreService`

屬於 `google.cloud.bigquery.biglake.v1alpha1.MetastoreService` 的方法會產生以下稽核記錄。

#### `CheckLock`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CheckLock`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.locks.check - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CheckLock"`

#### `CreateCatalog`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateCatalog"`

#### `CreateDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.databases.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateDatabase"`

#### `CreateLock`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateLock`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.locks.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateLock"`

#### `CreateTable`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateTable"`

#### `DeleteCatalog`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteCatalog"`

#### `DeleteDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.databases.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteDatabase"`

#### `DeleteLock`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteLock`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.locks.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteLock"`

#### `DeleteTable`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteTable"`

#### `GetCatalog`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetCatalog`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetCatalog"`

#### `GetDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetDatabase`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.databases.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetDatabase"`

#### `GetTable`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetTable`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetTable"`

#### `ListCatalogs`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListCatalogs`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListCatalogs"`

#### `ListDatabases`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListDatabases`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.databases.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListDatabases"`

#### `ListLocks`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListLocks`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.locks.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListLocks"`

#### `ListTables`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListTables`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListTables"`

#### `RenameTable`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.RenameTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.RenameTable"`

#### `UpdateDatabase`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.databases.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateDatabase"`

#### `UpdateTable`

* **方法**：`google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **此方法的篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateTable"`




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]