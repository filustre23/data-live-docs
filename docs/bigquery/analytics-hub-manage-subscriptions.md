Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理訂閱項目

您可以在 BigQuery sharing (舊稱 Analytics Hub) 中管理訂閱項目，控管資料存取權和共用權限。訂閱者可以訂閱房源資訊、查看訂閱項目及刪除訂閱項目。發布商可以監控誰有權存取產品資訊，並視需要撤銷訂閱。BigQuery sharing 訂閱項目是區域性資源，位於訂閱者的專案中。訂閱項目會儲存訂閱者的相關資訊，並代表發布商與訂閱者之間的合約。

## 事前準備

如要開始使用 BigQuery sharing (舊稱 Analytics Hub)，請在專案中啟用 Analytics Hub API Google Cloud 。

如要啟用 Analytics Hub API，您必須具備下列 Identity and Access Management (IAM) 權限：

* `serviceUsage.services.get`
* `serviceUsage.services.list`
* `serviceUsage.services.enable`

下列預先定義的 IAM 角色包含啟用 Analytics Hub API 所需的權限：

* [服務使用情形管理員](https://docs.cloud.google.com/service-usage/docs/access-control?hl=zh-tw#serviceusage.serviceUsageAdmin) (`roles/serviceusage.serviceUsageAdmin`)

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往 **Analytics Hub API** 頁面，為 Google Cloud 專案啟用 Analytics Hub API。

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [gcloud services enable](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw) 指令：

```
gcloud services enable analyticshub.googleapis.com
```

### 必要的角色

如要取得管理訂閱項目所需的權限，請要求管理員授予您專案的[Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriptionOwner)  (`roles/analyticshub.subscriptionOwner`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 限制

訂閱方案有下列限制：

* 您只能使用 Analytics Hub API 管理 2023 年 7 月 25 日後建立的訂閱項目。在此日期前建立的連結資料集不支援這項功能，因為缺少必要的訂閱資源。

## 以訂閱者身分管理訂閱項目

以下各節說明 BigQuery 共用訂閱者如何管理訂閱項目。

### 訂閱清單

如要訂閱清單，請按照「[查看及訂閱清單和資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)」一文中的步驟操作。

### 可列出訂閱項目

如要在專案中列出訂閱項目，請呼叫 [`projects.locations.subscriptions.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/list?hl=zh-tw)：

```
GET https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/subscriptions
```

更改下列內容：

* `PROJECT_ID`：您要列出訂閱項目的專案的 Google Cloud 專案 ID。
* `LOCATION`：要列出訂閱項目的位置。如要進一步瞭解支援分享功能的地區，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。

### 重新整理訂閱方案

當發布商或資料提供者新增或移除資料時，資料交換或資料無塵室可能會過時。發生這種情況時，現有連結的資料集不會自動更新，您必須重新整理訂閱方案，才能存取新資源。

如要重新整理訂閱項目，請選取下列任一選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下「新增資料」add\_box。
3. 選取「共用 (Analytics Hub)」。系統隨即會開啟探索頁面。
4. 找出並點選您訂閱的資料無塵室或資料交換庫。
5. 按一下「訂閱」。由於你已有使用中的訂閱方案，主機會顯示「重新整理」選項。
6. 按一下「重新整理」，即可使用最新資源更新連結的資料集。

### API

如要重新整理訂閱項目，請使用 [`projects.locations.subscriptions.refresh` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/refresh?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/subscriptions/SUBSCRIPTION_ID:refresh
```

更改下列內容：

* `PROJECT_ID`：要重新整理的訂閱項目專案 ID。
* `LOCATION`：要重新整理的訂閱項目位置。
* `SUBSCRIPTION_ID`：要重新整理的訂閱項目 ID。

要求主體必須為空白。如果成功，回應主體會包含作業執行個體。

### 刪除訂閱項目

如要刪除訂閱項目，請呼叫 [`projects.locations.subscriptions.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/delete?hl=zh-tw)：

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/subscriptions/SUBSCRIPTION_ID
```

更改下列內容：

* `PROJECT_ID`：專案的 Google Cloud 專案 ID，其中包含您要刪除的訂閱項目。
* `LOCATION`：要刪除的訂閱項目位置。
* `SUBSCRIPTION_ID`：要刪除的訂閱項目 ID。

要求主體必須為空白。如果成功，回應主體會包含作業執行個體。

刪除訂閱項目時，連結的資料集也會從專案中刪除。

從多區域刊登資訊中刪除訂閱項目時，系統也會從專案中刪除所有主要和次要連結的資料集副本。

如要進一步瞭解如何使用 Analytics Hub API 管理訂閱項目，請參閱「[`projects.locations.subscriptions` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions?hl=zh-tw#methods)」。

## 以發布商身分管理訂閱項目

以下各節說明 BigQuery sharing 發布端如何管理訂閱項目。如要進一步瞭解如何管理房源訂閱項目，請參閱「[管理房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。

### 可列出訂閱項目

如要列出所有訂閱項目，請選取下列任一選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   這個頁面會列出您可存取的所有[資料交易所](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)。
2. 在資料交換庫清單中，按一下要列出訂閱項目的資料交換庫名稱。
3. 按一下「Subscriptions」(訂閱項目) 分頁標籤。

### API

[如要列出特定資料交換庫中刊登的訂閱項目，請呼叫 `projects.locations.dataExchanges.listSubscriptions` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/listSubscriptions?hl=zh-tw)：

```
GET https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:listSubscriptions
```

更改下列內容：

* `PROJECT_ID`：包含資料交換的專案 Google Cloud 專案 ID。
* `LOCATION`：資料交換庫的位置，其中包含您要列出的訂閱項目。
* `DATAEXCHANGE_ID`：要列出訂閱項目的資料交換庫 ID。

### 撤銷訂閱項目

BigQuery sharing 發布端撤銷訂閱後，訂閱端就無法再查詢連結的資料集。由於您是在訂閱者擁有的資源上啟動這項動作，因此連結的資料集會保留在訂閱者的專案中。訂閱者可以刪除資料集來移除。

從多區域項目撤銷訂閱後，訂閱者就無法再查詢任何主要或次要連結資料集副本。

**注意：** 撤銷[與 Cloud Marketplace 整合的商業訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，可能會影響客戶並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

如要撤銷訂閱項目，請選取下列任一選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   這個頁面會列出您可存取的所有[資料交易所](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)。
2. 在資料交易所清單中，按一下要撤銷訂閱的資料交易所名稱。
3. 按一下「Subscriptions」(訂閱項目) 分頁標籤。
4. 找出要撤銷的訂閱項目，逐一勾選旁邊的核取方塊。
5. 按一下「撤銷訂閱」。

### API

如要撤銷訂閱項目，請呼叫 [`projects.locations.subscriptions.revoke` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/subscriptions/SUBSCRIPTION_ID:revoke
```

更改下列內容：

* `PROJECT_ID`：包含要撤銷訂閱項目的專案的 Google Cloud 專案 ID。
* `LOCATION`：要撤銷的訂閱項目位置。
* `SUBSCRIPTION_ID`：要撤銷的訂閱項目 ID。

## 後續步驟

* 瞭解 [BigQuery sharing 架構](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#architecture)。
* 瞭解如何[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解 [BigQuery 共用使用者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)。
* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解 [BigQuery sharing 稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]