Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 BigQuery 共用角色

如要管理 BigQuery sharing 資料交易所和資訊的存取權，請授予 BigQuery sharing (舊稱 Analytics Hub) 的特定 Identity and Access Management (IAM) 角色。指派這些角色後，您就能控管資料的權限，確保只有授權使用者可以探索、訂閱及管理資料共用資源。

**注意：**
管理[外部身分識別提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 執行個體，替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

## BigQuery sharing 身分與存取權管理角色

以下各節說明預先定義的 BigQuery 共用使用者角色。指派這些角色，控管資料交易和房源資訊的存取權。

### Analytics Hub 管理員角色

如要[管理資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)，BigQuery 共用功能提供[Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.admin) (`roles/analyticshub.admin`)，您可以為專案或資料交換授予這個角色。這個角色可執行下列操作：

* 建立、更新及刪除資料交換。
* 建立、更新、刪除及共用房源資訊。
* 管理 BigQuery sharing 管理員、清單管理員、發布者、訂閱者和檢視者。

您將透過這個角色成為 *BigQuery 共用管理員*。

### Analytics Hub 發布者和項目管理員角色

如要[管理清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)，BigQuery sharing 提供下列預先定義的角色，您可以為專案、資料交易所或清單授予這些角色：

* [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher) (`roles/analyticshub.publisher`)，可讓您執行下列操作：

  + 建立、更新及刪除房源資訊。
  + [設定房源的 IAM 政策](#grant-role-listing)。

  您將透過這個角色成為 *BigQuery sharing 發布端*。
* [Analytics Hub 項目管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.listingAdmin)
  (`roles/analyticshub.listingAdmin`)，可執行下列操作：

  + 更新及刪除房源資訊。
  + [設定房源的 IAM 政策](#grant-role-listing)。

  您會成為 *BigQuery 共用清單管理員*。

### Analytics Hub 訂閱者和檢視者角色

如要[查看及訂閱項目和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)，BigQuery sharing 提供下列預先定義的角色，可授予專案、資料交換或項目：

* [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.subscriber) (`roles/analyticshub.subscriber`)，可查看及訂閱房源資訊。

  您會透過這個角色成為 *BigQuery sharing 訂閱者*。
* [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)，可查看商家資訊和資料交換權限。

  您會成為 *BigQuery 共用檢視者*。

### Analytics Hub 訂閱項目擁有者角色

如要[管理訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw)，BigQuery 共用功能提供下列預先定義的角色，可授予專案：

* [Analytics Hub 訂閱項目擁有者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.subscriptionOwner)
  (`roles/analyticshub.subscriptionOwner`)，可管理訂閱項目。

您會成為 *BigQuery 共用訂閱方案擁有者*。

## 授予 BigQuery 共用 IAM 角色

您可以在資源階層的下列層級授予 IAM 角色：

* **專案**。如果您授予專案的角色，該角色會套用至專案中的所有資料交易所和刊登。
* **資料交換。**如果您授予資料交換庫的角色，該角色會套用至資料交換庫中的所有清單。
* **房源資訊**。如果授予房源角色，該角色只會套用至特定房源。

### 授予專案角色

如要在專案中設定 IAM 政策，您必須具備該專案的[專案 IAM 管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.projectIamAdmin) (`roles/resourcemanager.projectIamAdmin`)。如要授予專案預先定義的 BigQuery 共用身分與存取權管理角色，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往「IAM」(身分與存取權管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。
3. 在「New principals」(新增主體) 欄位中，輸入要授予存取權的主體電子郵件地址。您可以指定下列任一主體類型：

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
5. 選用：如要進一步控管對 Google Cloud 資源的存取權，請[新增條件式角色繫結](https://docs.cloud.google.com/iam/docs/managing-conditional-role-bindings?hl=zh-tw#add)。
6. 按一下 [儲存]。

### gcloud

如要授予專案角色，請使用 [`gcloud projects add-iam-policy-binding` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw)：

```
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member='PRINCIPAL' \
    --role='roles/analyticshub.admin'
```

更改下列內容：

* `PROJECT_ID`：專案 ID，例如 `my-project-1`。
* `PRINCIPAL`：您要授予角色的有效主體。您可以指定下列任一主體類型：

  + Google 帳戶電子郵件地址：`user:test-user@gmail.com`
  + Google 群組：`group:admins@googlegroups.com`
  + 服務帳戶：`serviceAccount:server@example.gserviceaccount.com`
  + Google Workspace 網域：`domain:example.com`

### API

1. 如要讀取現有政策，請使用 [`projects.getIamPolicy` 方法](https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/getIamPolicy?hl=zh-tw)：

   ```
   POST https://cloudresourcemanager.googleapis.com/v1/projects/PROJECT_ID:getIamPolicy
   ```

   將 `PROJECT_ID` 替換為專案 ID，例如 `my-project-1`。
2. 如要新增主體及其相關聯的角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@googlegroups.com`
   * `serviceAccount:server@example.gserviceaccount.com`
   * `domain:example.com`

   舉例來說，如要將 `roles/analyticshub.admin` 角色授予 `group:admins@googlegroups.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:admins@googlegroups.com"
    ],
    "role":"roles/analyticshub.admin"
   }
   ```
3. 如要為專案設定政策，請使用 [`projects.setIamPolicy` 方法](https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/setIamPolicy?hl=zh-tw)。
   在要求主體中，提供上一個步驟中更新的 IAM 政策：

   ```
   POST https://cloudresourcemanager.googleapis.com/v1/projects/PROJECT_ID:setIamPolicy
   ```

   將 `PROJECT_ID` 替換為專案 ID，例如 `my-project-1`。

您可以使用相同的 IAM 面板更新及刪除專案角色。

### 授予資料交換的角色

授予資料交換的權限時，資源名稱中的位置必須使用小寫字母。使用大寫或大小寫混合的值可能會導致權限遭拒錯誤。

以下範例顯示有效和無效的資源名稱格式：

* 請使用：`projects/myproject/locations/us/dataExchanges/123`
* 請避免：`projects/myproject/locations/US/dataExchanges/123`
* 請避免：`projects/myproject/locations/Eu/dataExchanges/123`

如要授予資料交換的角色，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(舊稱 Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要設定權限的資料交易所名稱。
3. 點按「Details」(詳細資料) 分頁標籤。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下
   person\_add
   「新增主體」。
6. 在「New principals」(新增主體) 欄位中，輸入要授予存取權的主體電子郵件地址。您也可以使用 `allUsers` 將資源設為公開，讓網際網路上的所有人都能存取，或使用 `allAuthenticatedUsers` 將資源設為僅供已登入 Google 帳戶的使用者存取。
7. 在「Select a role」(請選擇角色) 清單中，將指標懸停在「Analytics Hub」(資料分析中心) 上，然後選取下列其中一個 IAM 角色：

   * **Analytics Hub 管理員**
   * **Analytics Hub 清單管理員**
   * **Analytics Hub 發布者**
   * **Analytics Hub 訂閱者**
   * **Analytics Hub 訂閱項目擁有者**
   * **Analytics Hub 檢視者**
8. 按一下 [儲存]。

### API

1. 如要讀取現有政策，請使用 [`projects.locations.dataExchanges.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/getIamPolicy?hl=zh-tw)：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：資料交換的位置。使用小寫英文字母。
   * `DATAEXCHANGE_ID`：資料交換 ID。

   BigQuery 共用功能會傳回目前的政策。
2. 如要新增或移除成員及其相關聯的 IAM 角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@googlegroups.com`
   * `serviceAccount:server@example.gserviceaccount.com`
   * `domain:example.com`

   舉例來說，如要將 `roles/analyticshub.subscriber` 角色授予 `group:subscribers@googlegroups.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:subscribers@googlegroups.com"
    ],
    "role":"roles/analyticshub.subscriber"
   }
   ```
3. 如要設定資料交換政策，請使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)。在要求主體中，提供上一個步驟中更新的 IAM 政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:setIamPolicy
   ```

您可以使用相同的 IAM 面板更新及刪除資料交換角色。

### 授予房源角色

授予商家資訊權限時，資源名稱中的位置必須使用小寫字母。使用大寫或大小寫混合的值可能會導致權限遭拒錯誤。

以下範例顯示有效和無效的資源名稱格式：

* 請使用：`projects/myproject/locations/us/dataExchanges/123/listings/456`
* 請避免：`projects/myproject/locations/US/dataExchanges/123/listings/456`
* 請避免：`projects/myproject/locations/Eu/dataExchanges/123/listings/456`

如要授予房源角色，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(舊稱 Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交易所名稱。
3. 按一下要設定權限的商家資訊。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下
   person\_add
   「新增主體」。
6. 在「New principals」(新增主體) 欄位中，輸入要授予存取權的主體電子郵件地址。
7. 在「Select a role」(請選擇角色) 清單中，將指標懸停在「Analytics Hub」(資料分析中心) 上，然後選取下列其中一個 IAM 角色：

   * **Analytics Hub 管理員**
   * **Analytics Hub 清單管理員**
   * **Analytics Hub 發布者**
   * **Analytics Hub 訂閱者**
   * **Analytics Hub 訂閱項目擁有者**
   * **Analytics Hub 檢視者**
8. 按一下 [儲存]。

### API

1. 如要讀取現有政策，請使用 [`projects.locations.dataExchanges.listings.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/getIamPolicy?hl=zh-tw)：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：包含房源資訊的資料交易所位置。使用小寫英文字母。
   * `DATAEXCHANGE_ID`：資料交換 ID。
   * `LISTING_ID`：房源 ID。

   BigQuery 共用功能會傳回目前的政策。
2. 如要新增或移除成員及其相關聯的 IAM 角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@googlegroups.com`
   * `serviceAccount:server@example.gserviceaccount.com`
   * `domain:example.com`

   舉例來說，如要將 `roles/analyticshub.publisher` 角色授予 `group:publishers@googlegroups.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:publishers@googlegroups.com"
    ],
    "role":"roles/analyticshub.publisher"
   }
   ```
3. 如要設定房源的政策，請使用 [`projects.locations.dataExchanges.listings.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/setIamPolicy?hl=zh-tw)。在要求主體中，提供上一個步驟中更新的 IAM 政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:setIamPolicy
   ```

您可以使用相同的 IAM 面板更新及刪除商家資訊角色。

## 後續步驟

* 進一步瞭解 [BigQuery 共用角色和權限](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw)。
* 瞭解 [BigQuery 共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* 瞭解如何[管理資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)。
* 瞭解如何[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。
* 瞭解如何[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]