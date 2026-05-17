Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 BigQuery 共用角色

本文說明 BigQuery 共用 (舊稱 Analytics Hub) 的 Identity and Access Management (IAM) 角色，以及如何授予這些角色。詳情請參閱「[BigQuery sharing 角色和權限](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw)」。

**注意：**
管理[外部身分識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

## BigQuery sharing 身分與存取權管理角色

以下各節說明預先定義的 BigQuery 共用角色。您可以將這些角色指派給使用者，讓他們在資料交易所和房源上執行各種工作。

### Analytics Hub 管理員角色

如要[管理資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)，BigQuery sharing 功能提供[Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.admin) (`roles/analyticshub.admin`)，您可以為 Google Cloud 專案或資料交換授予這個角色。這個角色可讓使用者執行下列操作：

* 建立、更新及刪除資料交換。
* 建立、更新、刪除及共用房源資訊。
* 管理 BigQuery sharing 管理員、清單管理員、發布者、訂閱者和檢視者。

您將成為 *BigQuery sharing 管理員*。

### Analytics Hub 發布者和項目管理員角色

如要[管理清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)，Sharing 提供下列預先定義的角色，您可以為專案、資料交換或清單授予這些角色：

* [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher) (`roles/analyticshub.publisher`)，可讓使用者執行下列操作：

  + 建立、更新及刪除房源。
  + [設定房源的 IAM 政策](#grant-role-listing)。

  您將透過這個角色成為 *BigQuery sharing 發布端*。
* [Analytics Hub 清單管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.listingAdmin)
  (`roles/analyticshub.listingAdmin`)，可讓使用者執行下列操作：

  + 更新及刪除房源資訊。
  + [設定房源的 IAM 政策](#grant-role-listing)。

  您會成為 *BigQuery sharing 清單管理員*。

### Analytics Hub 訂閱者和檢視者角色

如要[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)，共用功能提供下列預先定義的角色，可授予專案、資料交換或清單：

* [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.subscriber)
  (`roles/analyticshub.subscriber`)，可供使用者查看及訂閱房源。

  您會透過這個角色成為 *BigQuery sharing 訂閱者*。
* [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)，可讓使用者查看商家資訊和資料交換權限。

  您會成為 *BigQuery sharing 檢視者*。

### Analytics Hub 訂閱項目擁有者角色

如要[管理訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw)，Sharing 提供下列預先定義的角色，您可以在專案層級授予這些角色：

* [Analytics Hub 訂閱項目擁有者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.subscriptionOwner) (`roles/analyticshub.subscriptionOwner`)，可讓使用者管理訂閱項目。

您會成為 *BigQuery sharing 訂閱方案擁有者*。

## 授予 BigQuery 共用 IAM 角色

您可以視需求在資源階層的下列層級授予 IAM 角色：

* **專案**。如果您授予專案的角色，該角色會套用至專案中的所有資料交換和刊登。
* **資料交換。**如果您授予資料交換的角色，該角色會套用至資料交換中的所有清單。
* **房源資訊**：如果授予房源角色，則只適用於該特定房源。

### 授予專案角色

如要在專案中設定 IAM 政策，您必須具備該專案的[專案 IAM 管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.projectIamAdmin) (`roles/resourcemanager.projectIamAdmin`)。如要授予專案預先定義的 BigQuery sharing 身分與存取權管理角色，請選取下列其中一個選項。

### 控制台

1. 前往專案的「IAM」頁面。

   [前往「IAM」(身分與存取權管理) 頁面](https://console.cloud.google.com/console/iam-admin/iam?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。
3. 在「New principals」(新增主體) 欄位中，輸入要授予存取權的身分電子郵件地址。例如：

   * Google 帳戶電子郵件地址：`test-user@gmail.com`
   * Google 群組：`admins@googlegroups.com`
   * 服務帳戶：`server@example.gserviceaccount.com`
   * Google Workspace 網域：`example.com`
4. 在「Select a role」(選取角色) 清單中，將指標懸停在「Analytics Hub」(數據分析中心) 上，然後選取下列其中一個角色：

   * **Analytics Hub 管理員**
   * **Analytics Hub 清單管理員**
   * **Analytics Hub 發布者**
   * **Analytics Hub 訂閱者**
   * **Analytics Hub 訂閱項目擁有者**
   * **Analytics Hub 檢視者**
5. 選用：如要進一步控管資源的存取權，請[新增條件式角色繫結](https://docs.cloud.google.com/iam/docs/managing-conditional-role-bindings?hl=zh-tw#add)。 Google Cloud
6. 儲存變更。

   您可以使用相同的 IAM 面板刪除及更新專案管理員。

### gcloud

如要在專案層級授予角色，請使用 [`gcloud projects add-iam-policy-binding` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw)：

```
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member='PRINCIPAL' \
    --role='roles/analyticshub.admin'
```

更改下列內容：

* `PROJECT_ID`：專案，例如 `my-project-1`。
* `PRINCIPAL`：您要授予角色的有效身分。例如：

  + Google 帳戶電子郵件地址：`user:user@gmail.com`
  + Google 群組：`group:admins@googlegroups.com`
  + 服務帳戶：`serviceAccount:server@example.gserviceaccount.com`
  + Google Workspace 網域：`domain:example.com`

### API

1. 使用資源的 `getIamPolicy` 方法讀取現有政策。如果是專案，請使用 [`projects.getIamPolicy` 方法](https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/getIamPolicy?hl=zh-tw)。

   ```
   POST https://cloudresourcemanager.googleapis.com/v1/projects/PROJECT_ID:getIamPolicy
   ```

   將 `PROJECT_ID` 改為專案，例如 `my-project-1`。
2. 如要新增主體及其相關聯的角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@example.com`
   * `serviceAccount:test123@example.domain.com`
   * `domain:example.domain.com`

   舉例來說，如要將 `roles/analyticshub.admin` 角色授予 `group:admins@example.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:admins@example.com"
    ],
    "role":"roles/analyticshub.admin"
   }
   ```
3. 使用 `setIamPolicy` 方法寫入更新後的政策。

   舉例來說，如要在專案層級設定政策，請使用 [`project.setIamPolicy` 方法](https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/setIamPolicy?hl=zh-tw)。在要求主體中，提供上一個步驟中更新的 IAM 政策。

   ```
   POST https://cloudresourcemanager.googleapis.com/v1/projects/PROJECT_ID:setIamPolicy
   ```

   將 `PROJECT_ID` 替換為專案 ID。

### 授予資料交換的角色

如要授予資料交換的角色，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要設定權限的資料交換名稱。
3. 前往「詳細資料」分頁。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下「新增主體」person\_add。
6. 在「New principals」(新增主體) 欄位中，新增要授予存取權的電子郵件 ID。您也可以使用 `allUsers` 將資源設為公開，讓網際網路上的所有人都能存取，或使用 `allAuthenticatedUsers` 將資源設為僅供登入 Google 的使用者存取。
7. 在「Select a role」(請選擇角色) 選單中選取「Analytics Hub」(資料分析中心)，然後選取下列任一 Identity and Access Management (IAM) 角色：

   * **Analytics Hub 管理員**
   * **Analytics Hub 清單管理員**
   * **Analytics Hub 發布者**
   * **Analytics Hub 訂閱者**
   * **Analytics Hub 訂閱項目擁有者**
   * **Analytics Hub 檢視者**
8. 按一下 [儲存]。

### API

1. 使用 [`projects.locations.dataExchanges.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/getIamPolicy?hl=zh-tw)，透過清單 `getIamPolicy` 方法讀取現有政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：資料交換的位置。使用小寫英文字母。
   * `DATAEXCHANGE_ID`：資料交換 ID。

   BigQuery sharing (舊稱 Analytics Hub) 會傳回目前的政策。
2. 如要新增或移除成員及其相關聯的身分與存取權管理 (IAM) 角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@example.com`
   * `serviceAccount:test123@example.domain.com`
   * `domain:example.domain.com`

   舉例來說，如要將 `roles/analyticshub.subscriber` 角色授予 `group:subscribers@example.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:subscribers@example.com"
    ],
    "role":"roles/analyticshub.subscriber"
   }
   ```
3. 使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)寫入更新後的政策。在要求主體中，提供上一個步驟中更新的 IAM 政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:setIamPolicy
   ```

   在要求主體中提供房源詳細資料。如果要求成功，回應主體會包含房源詳細資料。

在資源層級 (例如資料交換庫) 授予權限時，資源名稱的位置部分必須使用小寫字母。使用大寫或大小寫混合的值可能會導致 `Permission Denied` 錯誤。

* 請使用：`projects/myproject/locations/us/dataExchanges/123`
* 請避免：`projects/myproject/locations/US/dataExchanges/123`
* 請避免：`projects/myproject/locations/Eu/dataExchanges/123`

您可以使用相同的 IAM 面板刪除及更新資料交換角色。

### 授予房源角色

如要授予商家資訊的角色，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要新增使用者的房源。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下「新增主體」person\_add。
6. 在「New principals」(新增主體) 欄位中，新增要授予存取權的身分電子郵件 ID。
7. 在「Select a role」(請選擇角色) 選單中選取「Analytics Hub」(資料分析中心)，然後選取下列任一 Identity and Access Management (IAM) 角色：

   * **Analytics Hub 管理員**
   * **Analytics Hub 清單管理員**
   * **Analytics Hub 發布者**
   * **Analytics Hub 訂閱者**
   * **Analytics Hub 訂閱項目擁有者**
   * **Analytics Hub 檢視者**
8. 按一下 [儲存]。

### API

1. 使用 [`projects.locations.dataExchanges.listings.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/getIamPolicy?hl=zh-tw)，透過清單 `getIamPolicy` 方法讀取現有政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：包含房源資訊的資料交換庫位置。使用小寫英文字母。
   * `DATAEXCHANGE_ID`：資料交換 ID。
   * `LISTING_ID`：房源 ID。

   分享會傳回目前的政策。
2. 如要新增或移除成員及其相關聯的身分與存取權管理 (IAM) 角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@example.com`
   * `serviceAccount:test123@example.domain.com`
   * `domain:example.domain.com`

   舉例來說，如要將 `roles/analyticshub.publisher` 角色授予 `group:publishers@example.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:publishers@example.com"
    ],
    "role":"roles/analyticshub.publisher"
   }
   ```
3. 使用 [`projects.locations.dataExchanges.listings.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/setIamPolicy?hl=zh-tw)寫入更新後的政策。在要求主體中，提供上一個步驟中更新的 IAM 政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING-ID:setIamPolicy
   ```

   在要求主體中提供房源詳細資料。如果要求成功，回應主體會包含房源詳細資料。

在資源層級 (例如在商家資訊上) 授予權限時，資源名稱的位置部分必須使用小寫字母。使用大寫或大小寫混合的值可能會導致 `Permission Denied` 錯誤。

* 請使用：`projects/myproject/locations/us/dataExchanges/123/listings/456`
* 請避免：`projects/myproject/locations/US/dataExchanges/123/listings/456`
* 請避免：`projects/myproject/locations/Eu/dataExchanges/123/listings/456`

您可以使用相同的 IAM 面板刪除及更新商家檔案角色。

## 後續步驟

* 瞭解 [BigQuery IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
* 瞭解 [BigQuery 共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* 瞭解如何[管理資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)。
* 瞭解如何[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。
* 瞭解如何[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]