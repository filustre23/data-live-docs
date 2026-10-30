Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigLake 稽核記錄

BigLake 的 Cloud 稽核記錄可讓您追蹤資源的管理和資料存取作業，協助您監控存取和設定變更。您可以在 Logs Explorer 中查詢這些記錄，並查看哪些 BigLake API 方法會產生 Cloud 稽核記錄。

如要進一步瞭解 Cloud 稽核記錄，請參閱下列文件：

* [稽核記錄類型](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#types)
* [稽核記錄項目結構](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#audit_log_entry_structure)
* [儲存及轉送稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#storing_and_routing_audit_logs)
* [Cloud Logging 定價摘要](https://docs.cloud.google.com/stackdriver/pricing?hl=zh-tw#logs-pricing-summary)
* [啟用資料存取稽核記錄](https://docs.cloud.google.com/logging/docs/audit/configure-data-access?hl=zh-tw)

## 服務名稱

如要查看 BigLake 稽核記錄，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面：

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 複製下列查詢並貼到 Logs Explorer 的「Query」(查詢) 欄位，然後按一下「Run query」(執行查詢)。

   ```
       protoPayload.serviceName="biglake.googleapis.com"
   ```

## 依權限類型區分的方法

每個 IAM 權限都具有 `type` 屬性，其值為以下四個列舉值之一：`ADMIN_READ`、`ADMIN_WRITE`、`DATA_READ` 或 `DATA_WRITE`。呼叫方法時，BigLake 會產生一筆稽核記錄，類別取決於執行該方法所需權限的 `type` 屬性。若方法需要的 IAM 權限，`type` 屬性值為 `DATA_READ`、`DATA_WRITE` 或 `ADMIN_READ`，就會產生[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)稽核記錄；若所需 IAM 權限的 `type` 屬性值為 `ADMIN_WRITE`，則會產生[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)稽核記錄。

下表列出的 API 方法中，如標有 (LRO) 字樣，表示為長時間執行的作業。這類方法通常會產生兩個稽核記錄項目，作業開始和結束時各一個。詳情請參閱「[長時間執行的作業稽核記錄](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)」。

| 權限類型 | 方法 |
| --- | --- |
| `ADMIN_READ` | `google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveCatalog` `google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveDatabase` `google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveTable` `google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveCatalogs` `google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveDatabases` `google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveTables` `google.cloud.biglake.hive.v1.HiveMetastoreService.ListPartitions` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListHiveDatabases` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListPartitions` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveDatabase` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveTable` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveCatalogs` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveDatabases` `google.cloud.biglake.v1.IcebergCatalogService.GetIcebergCatalogConfig` `google.cloud.bigquery.biglake.v1.MetastoreService.GetCatalog` `google.cloud.bigquery.biglake.v1.MetastoreService.GetDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.GetTable` `google.cloud.bigquery.biglake.v1.MetastoreService.ListCatalogs` `google.cloud.bigquery.biglake.v1.MetastoreService.ListDatabases` `google.cloud.bigquery.biglake.v1.MetastoreService.ListTables` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetCatalog` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.GetTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListCatalogs` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListDatabases` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListLocks` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.ListTables` |
| `ADMIN_WRITE` | `google.cloud.biglake.hive.v1.HiveMetastoreService.BatchCreatePartitions` `google.cloud.biglake.hive.v1.HiveMetastoreService.BatchDeletePartitions` `google.cloud.biglake.hive.v1.HiveMetastoreService.BatchUpdatePartitions` `google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveCatalog` `google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveDatabase` `google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveTable` `google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveCatalog` `google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveDatabase` `google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveTable` `google.cloud.biglake.hive.v1.HiveMetastoreService.FailoverHiveCatalog` `google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveCatalog` `google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveDatabase` `google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveTable` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchCreatePartitions` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchDeletePartitions` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchUpdatePartitions` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveCatalog` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveDatabase` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveTable` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveCatalog` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveDatabase` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveTable` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.FailoverHiveCatalog` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveCatalog` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveDatabase` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveTable` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListHiveTables` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveCatalog` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveDatabase` `google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveTable` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchCreatePartitions` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchDeletePartitions` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchUpdatePartitions` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveCatalog` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveDatabase` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveTable` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveCatalog` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveDatabase` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveTable` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.FailoverHiveCatalog` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveCatalog` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveTables` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListPartitions` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveCatalog` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveDatabase` `google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveTable` `google.cloud.biglake.v1.DataProductSharingService.PublishDataProduct` `google.cloud.biglake.v1.DeltaSharingService.CreateDeltaSharingCatalog` `google.cloud.biglake.v1.DeltaSharingService.DeleteDeltaSharingCatalog` `google.cloud.biglake.v1.DeltaSharingService.UpdateDeltaSharingCatalog` `google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergCatalogIamPolicy` `google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergNamespaceIamPolicy` `google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergTableIamPolicy` `google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergCatalog` `google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergNamespace` `google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergTable` `google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergCatalog` `google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergNamespace` `google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergTable` `google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergCatalog` `google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergNamespace` `google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergTable` `google.cloud.biglake.v1alpha.DataProductSharingService.PublishDataProduct` `google.cloud.biglake.v1alpha.DataProductSharingService.UnpublishDataProduct` `google.cloud.biglake.v1alpha.DeltaSharingService.CreateDeltaSharingCatalog` `google.cloud.biglake.v1alpha.DeltaSharingService.DeleteDeltaSharingCatalog` `google.cloud.biglake.v1alpha.DeltaSharingService.UpdateDeltaSharingCatalog` `google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergCatalog` `google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergNamespace` `google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergTable` `google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergCatalog` `google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergNamespace` `google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergTable` `google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergCatalog` `google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergNamespace` `google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergTable` `google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergCatalog` `google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergNamespace` `google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergTable` `google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergCatalog` `google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergNamespace` `google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergTable` `google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergCatalog` `google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergNamespace` `google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergTable` `google.cloud.bigquery.biglake.v1.MetastoreService.CreateCatalog` `google.cloud.bigquery.biglake.v1.MetastoreService.CreateDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.CreateTable` `google.cloud.bigquery.biglake.v1.MetastoreService.DeleteCatalog` `google.cloud.bigquery.biglake.v1.MetastoreService.DeleteDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.DeleteTable` `google.cloud.bigquery.biglake.v1.MetastoreService.RenameTable` `google.cloud.bigquery.biglake.v1.MetastoreService.UpdateDatabase` `google.cloud.bigquery.biglake.v1.MetastoreService.UpdateTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CheckLock` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateCatalog` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateLock` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.CreateTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteCatalog` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteLock` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.DeleteTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.RenameTable` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateDatabase` `google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateTable` |

## API 介面稽核記錄

如要瞭解各方法所需的權限及評估方式，請參閱 BigLake 的 Identity and Access Management 說明文件。

### `google.cloud.biglake.hive.v1.HiveMetastoreService`

屬於 `google.cloud.biglake.hive.v1.HiveMetastoreService` 的方法會產生以下稽核記錄。

#### `BatchCreatePartitions`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.BatchCreatePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.createPartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.BatchCreatePartitions"`

#### `BatchDeletePartitions`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.BatchDeletePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.deletePartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.BatchDeletePartitions"`

#### `BatchUpdatePartitions`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.BatchUpdatePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.updatePartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.BatchUpdatePartitions"`

#### `CreateHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveCatalog"`

#### `CreateHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveDatabase"`

#### `CreateHiveTable`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.CreateHiveTable"`

#### `DeleteHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveCatalog"`

#### `DeleteHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveDatabase"`

#### `DeleteHiveTable`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.DeleteHiveTable"`

#### `FailoverHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.FailoverHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.FailoverHiveCatalog"`

#### `GetHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveCatalog`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveCatalog"`

#### `GetHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveDatabase`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.namespaces.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveDatabase"`

#### `GetHiveTable`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveTable`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.GetHiveTable"`

#### `ListHiveCatalogs`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveCatalogs`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveCatalogs"`

#### `ListHiveDatabases`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveDatabases`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.namespaces.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveDatabases"`

#### `ListHiveTables`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveTables`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.ListHiveTables"`

#### `ListPartitions`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.ListPartitions`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.listPartitions - ADMIN_READ`
* **方法的作業種類**：
  [**串流 RPC**](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#streaming)
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.ListPartitions"`

#### `UpdateHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveCatalog"`

#### `UpdateHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveDatabase"`

#### `UpdateHiveTable`

* **方法**：`google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1.HiveMetastoreService.UpdateHiveTable"`

### `google.cloud.biglake.hive.v1alpha.HiveMetastoreService`

屬於 `google.cloud.biglake.hive.v1alpha.HiveMetastoreService` 的方法會產生以下稽核記錄。

#### `BatchCreatePartitions`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchCreatePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.createPartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchCreatePartitions"`

#### `BatchDeletePartitions`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchDeletePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.deletePartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchDeletePartitions"`

#### `BatchUpdatePartitions`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchUpdatePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.updatePartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.BatchUpdatePartitions"`

#### `CreateHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveCatalog"`

#### `CreateHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveDatabase"`

#### `CreateHiveTable`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.CreateHiveTable"`

#### `DeleteHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveCatalog"`

#### `DeleteHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveDatabase"`

#### `DeleteHiveTable`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.DeleteHiveTable"`

#### `FailoverHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.FailoverHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.FailoverHiveCatalog"`

#### `GetHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.get - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveCatalog"`

#### `GetHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.get - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveDatabase"`

#### `GetHiveTable`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.get - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.GetHiveTable"`

#### `ListHiveDatabases`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListHiveDatabases`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListHiveDatabases"`

#### `ListHiveTables`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListHiveTables`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.list - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListHiveTables"`

#### `ListPartitions`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListPartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.listPartitions - ADMIN_READ`
* **方法的作業種類**：
  [**串流 RPC**](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#streaming)
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.ListPartitions"`

#### `UpdateHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveCatalog"`

#### `UpdateHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveDatabase"`

#### `UpdateHiveTable`

* **方法**：`google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1alpha.HiveMetastoreService.UpdateHiveTable"`

### `google.cloud.biglake.hive.v1beta.HiveMetastoreService`

屬於 `google.cloud.biglake.hive.v1beta.HiveMetastoreService` 的方法會產生以下稽核記錄。

#### `BatchCreatePartitions`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchCreatePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.createPartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchCreatePartitions"`

#### `BatchDeletePartitions`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchDeletePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.deletePartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchDeletePartitions"`

#### `BatchUpdatePartitions`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchUpdatePartitions`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.updatePartitions - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.BatchUpdatePartitions"`

#### `CreateHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveCatalog"`

#### `CreateHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveDatabase"`

#### `CreateHiveTable`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.CreateHiveTable"`

#### `DeleteHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveCatalog"`

#### `DeleteHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveDatabase"`

#### `DeleteHiveTable`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.DeleteHiveTable"`

#### `FailoverHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.FailoverHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.FailoverHiveCatalog"`

#### `GetHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveCatalog`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.get - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveCatalog"`

#### `GetHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveDatabase`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.namespaces.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveDatabase"`

#### `GetHiveTable`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveTable`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.GetHiveTable"`

#### `ListHiveCatalogs`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveCatalogs`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.catalogs.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveCatalogs"`

#### `ListHiveDatabases`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveDatabases`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.namespaces.list - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveDatabases"`

#### `ListHiveTables`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveTables`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.list - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListHiveTables"`

#### `ListPartitions`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListPartitions`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `biglake.tables.listPartitions - ADMIN_WRITE`
* **方法的作業種類**：
  [**串流 RPC**](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#streaming)
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.ListPartitions"`

#### `UpdateHiveCatalog`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveCatalog"`

#### `UpdateHiveDatabase`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveDatabase`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveDatabase"`

#### `UpdateHiveTable`

* **方法**：`google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.hive.v1beta.HiveMetastoreService.UpdateHiveTable"`

### `google.cloud.biglake.v1.DataProductSharingService`

屬於 `google.cloud.biglake.v1.DataProductSharingService` 的方法會產生以下稽核記錄。

#### `PublishDataProduct`

* **方法**：`google.cloud.biglake.v1.DataProductSharingService.PublishDataProduct`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.DataProductSharingService.PublishDataProduct"`

### `google.cloud.biglake.v1.DeltaSharingService`

屬於 `google.cloud.biglake.v1.DeltaSharingService` 的方法會產生以下稽核記錄。

#### `CreateDeltaSharingCatalog`

* **方法**：`google.cloud.biglake.v1.DeltaSharingService.CreateDeltaSharingCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.DeltaSharingService.CreateDeltaSharingCatalog"`

#### `DeleteDeltaSharingCatalog`

* **方法**：`google.cloud.biglake.v1.DeltaSharingService.DeleteDeltaSharingCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.DeltaSharingService.DeleteDeltaSharingCatalog"`

#### `UpdateDeltaSharingCatalog`

* **方法**：`google.cloud.biglake.v1.DeltaSharingService.UpdateDeltaSharingCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.DeltaSharingService.UpdateDeltaSharingCatalog"`

### `google.cloud.biglake.v1.IcebergCatalogIamService`

屬於 `google.cloud.biglake.v1.IcebergCatalogIamService` 的方法會產生以下稽核記錄。

#### `SetIcebergCatalogIamPolicy`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergCatalogIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergCatalogIamPolicy"`

#### `SetIcebergNamespaceIamPolicy`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergNamespaceIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergNamespaceIamPolicy"`

#### `SetIcebergTableIamPolicy`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergTableIamPolicy`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.setIamPolicy - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogIamService.SetIcebergTableIamPolicy"`

### `google.cloud.biglake.v1.IcebergCatalogService`

屬於 `google.cloud.biglake.v1.IcebergCatalogService` 的方法會產生以下稽核記錄。

#### `CreateIcebergCatalog`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergCatalog"`

#### `CreateIcebergNamespace`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergNamespace"`

#### `CreateIcebergTable`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.CreateIcebergTable"`

#### `DeleteIcebergCatalog`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergCatalog"`

#### `DeleteIcebergNamespace`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergNamespace"`

#### `DeleteIcebergTable`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.DeleteIcebergTable"`

#### `GetIcebergCatalogConfig`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.GetIcebergCatalogConfig`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.get - ADMIN_READ`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.GetIcebergCatalogConfig"`

#### `UpdateIcebergCatalog`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergCatalog"`

#### `UpdateIcebergNamespace`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergNamespace"`

#### `UpdateIcebergTable`

* **方法**：`google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.UpdateIcebergTable"`

### `google.cloud.biglake.v1alpha.DataProductSharingService`

屬於 `google.cloud.biglake.v1alpha.DataProductSharingService` 的方法會產生以下稽核記錄。

#### `PublishDataProduct`

* **方法**：`google.cloud.biglake.v1alpha.DataProductSharingService.PublishDataProduct`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.DataProductSharingService.PublishDataProduct"`

#### `UnpublishDataProduct`

* **方法**：`google.cloud.biglake.v1alpha.DataProductSharingService.UnpublishDataProduct`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.DataProductSharingService.UnpublishDataProduct"`

### `google.cloud.biglake.v1alpha.DeltaSharingService`

屬於 `google.cloud.biglake.v1alpha.DeltaSharingService` 的方法會產生以下稽核記錄。

#### `CreateDeltaSharingCatalog`

* **方法**：`google.cloud.biglake.v1alpha.DeltaSharingService.CreateDeltaSharingCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.DeltaSharingService.CreateDeltaSharingCatalog"`

#### `DeleteDeltaSharingCatalog`

* **方法**：`google.cloud.biglake.v1alpha.DeltaSharingService.DeleteDeltaSharingCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.DeltaSharingService.DeleteDeltaSharingCatalog"`

#### `UpdateDeltaSharingCatalog`

* **方法**：`google.cloud.biglake.v1alpha.DeltaSharingService.UpdateDeltaSharingCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.DeltaSharingService.UpdateDeltaSharingCatalog"`

### `google.cloud.biglake.v1alpha.IcebergCatalogService`

屬於 `google.cloud.biglake.v1alpha.IcebergCatalogService` 的方法會產生以下稽核記錄。

#### `CreateIcebergCatalog`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergCatalog"`

#### `CreateIcebergNamespace`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergNamespace"`

#### `CreateIcebergTable`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.CreateIcebergTable"`

#### `DeleteIcebergCatalog`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergCatalog"`

#### `DeleteIcebergNamespace`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergNamespace"`

#### `DeleteIcebergTable`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.DeleteIcebergTable"`

#### `UpdateIcebergCatalog`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergCatalog"`

#### `UpdateIcebergNamespace`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergNamespace"`

#### `UpdateIcebergTable`

* **方法**：`google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1alpha.IcebergCatalogService.UpdateIcebergTable"`

### `google.cloud.biglake.v1beta.IcebergCatalogService`

屬於 `google.cloud.biglake.v1beta.IcebergCatalogService` 的方法會產生以下稽核記錄。

#### `CreateIcebergCatalog`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergCatalog"`

#### `CreateIcebergNamespace`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergNamespace"`

#### `CreateIcebergTable`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.create - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.CreateIcebergTable"`

#### `DeleteIcebergCatalog`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergCatalog"`

#### `DeleteIcebergNamespace`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergNamespace"`

#### `DeleteIcebergTable`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.delete - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.DeleteIcebergTable"`

#### `UpdateIcebergCatalog`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergCatalog`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.catalogs.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergCatalog"`

#### `UpdateIcebergNamespace`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergNamespace`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.namespaces.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergNamespace"`

#### `UpdateIcebergTable`

* **方法**：`google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergTable`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `biglake.tables.update - ADMIN_WRITE`
* **方法的作業種類**：
  非長時間執行或串流作業。
* **篩選條件**：`protoPayload.methodName="google.cloud.biglake.v1beta.IcebergCatalogService.UpdateIcebergTable"`

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
* **篩選條件**：`protoPayload.methodName="google.cloud.bigquery.biglake.v1alpha1.MetastoreService.UpdateTable"`

## 系統事件

系統事件稽核記錄是由 GCP 系統產生，而非由使用者直接操作。詳情請參閱「[系統事件稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#system-event)」。

| 方法名稱 | 篩選這項事件 | 附註 |
| --- | --- | --- |
| google.cloud.biglake.v1.IcebergCatalogService.BackgroundRefreshCatalog | `protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.BackgroundRefreshCatalog"` |  |
| google.cloud.biglake.v1.IcebergCatalogService.BackgroundRefreshNamespace | `protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.BackgroundRefreshNamespace"` |  |
| google.cloud.biglake.v1.IcebergCatalogService.BackgroundRefreshTable | `protoPayload.methodName="google.cloud.biglake.v1.IcebergCatalogService.BackgroundRefreshTable"` |  |

## 不會產生稽核記錄的方法

某些方法可能不會產生稽核記錄，原因包括以下一或多項：

* 該方法的流量使用量高，若產生稽核記錄，會導致記錄與儲存成本過高。
* 稽核價值低。
* 其他稽核記錄或平台記錄已涵蓋該方法的活動。

下列方法不會產生稽核記錄：

* `google.cloud.biglake.v1.DeltaSharingService.ListDeltaSharingCatalogs`
* `google.cloud.biglake.v1.DeltaSharingService.ListDeltaSharingSchemas`
* `google.cloud.biglake.v1alpha.DeltaSharingService.ListDeltaSharingCatalogs`
* `google.cloud.biglake.v1alpha.DeltaSharingService.ListDeltaSharingSchemas`
* `google.cloud.biglake.v1alpha.DeltaSharingService.ListDeltaSharingShares`
* `google.cloud.biglake.v1alpha.DeltaSharingService.ListDeltaSharingTables`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.CheckIcebergNamespaceExists`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.CheckIcebergTableExists`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.FailoverIcebergCatalog`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.GetIcebergCatalog`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.GetIcebergCatalogConfig`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.GetIcebergNamespace`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.GetIcebergTable`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.ListIcebergCatalogs`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.ListIcebergNamespaces`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.ListIcebergTableIdentifiers`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.LoadIcebergTableCredentials`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.RegisterIcebergTable`
* `google.cloud.biglake.v1alpha.IcebergCatalogService.ReportIcebergTableMetrics`
* `google.cloud.biglake.v1beta.IcebergCatalogService.CheckIcebergNamespaceExists`
* `google.cloud.biglake.v1beta.IcebergCatalogService.CheckIcebergTableExists`
* `google.cloud.biglake.v1beta.IcebergCatalogService.FailoverIcebergCatalog`
* `google.cloud.biglake.v1beta.IcebergCatalogService.GetIcebergCatalog`
* `google.cloud.biglake.v1beta.IcebergCatalogService.GetIcebergNamespace`
* `google.cloud.biglake.v1beta.IcebergCatalogService.GetIcebergTable`
* `google.cloud.biglake.v1beta.IcebergCatalogService.ListIcebergCatalogs`
* `google.cloud.biglake.v1beta.IcebergCatalogService.ListIcebergNamespaces`
* `google.cloud.biglake.v1beta.IcebergCatalogService.ListIcebergTableIdentifiers`
* `google.cloud.biglake.v1beta.IcebergCatalogService.LoadIcebergTableCredentials`
* `google.cloud.biglake.v1beta.IcebergCatalogService.RegisterIcebergTable`
* `google.cloud.biglake.v1beta.IcebergCatalogService.ReportIcebergTableMetrics`




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]