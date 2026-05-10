Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 啟用 BigQuery 資料移轉服務

如要使用 BigQuery 資料移轉服務，您必須以專案[擁有者](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#legacy-basic)的身分完成下列步驟：

* 建立專案並啟用 BigQuery API。
* 啟用 BigQuery 資料移轉服務。

如要進一步瞭解 Identity and Access Management (IAM) 角色，請參閱 IAM 說明文件中的「[角色和權限](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw)」。

**注意：** 如果您以程式輔助方式啟用 BigQuery 資料移轉服務後，立即呼叫 BigQuery 資料移轉服務 API，請實作重試機制，並在連續呼叫之間加入延遲時間。這是必要步驟，因為 API 啟用作業是非同步作業，且最終一致性會導致傳播延遲。

## 建立專案並啟用 BigQuery API

使用 BigQuery 資料移轉服務之前，您必須先建立專案，在大多數情況下，還必須啟用該專案的計費功能。您可以在現有專案使用 BigQuery 資料移轉服務，或建立一個新專案。若您使用現有的專案，可能還需啟用 BigQuery API。

如何建立專案並啟用 BigQuery API：

1. 前往 Google Cloud 控制台的專案選擇器頁面。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. 選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。
3. 為專案啟用計費功能，以便進行所有轉移作業。免費轉移不會產生任何費用。

   即使要從多個來源移轉資料，每個專案也只需要啟用一次計費功能。資料移轉完成後，您也必須啟用帳單，才能在 BigQuery 中查詢資料。

   [瞭解如何確認專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw)。
4. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請啟用 BigQuery API。
     
     
   [啟用 BigQuery API](https://console.cloud.google.com/apis/library/bigquery.googleapis.com?hl=zh-tw)

## 啟用 BigQuery 資料移轉服務

建立移轉之前，您必須先啟用 BigQuery 資料移轉服務。如要啟用 BigQuery 資料移轉服務，您必須取得專案的[擁有者](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#legacy-basic)角色權限。

如何啟用 BigQuery 資料移轉服務：

1. 在 API 程式庫中開啟 [BigQuery Data Transfer API](https://console.cloud.google.com/apis/library/bigquerydatatransfer.googleapis.com?hl=zh-tw) 頁面。
2. 從下拉式選單中選取適當的專案。
3. 按一下 [ENABLE] (啟用) 按鈕。

   [啟用 Data Transfer API](https://console.cloud.google.com/apis/library/bigquerydatatransfer.googleapis.com?hl=zh-tw)

## 服務代理

BigQuery 資料移轉服務會使用[服務代理程式](https://docs.cloud.google.com/iam/docs/service-account-types?hl=zh-tw#service-agents)存取及管理資源。包括但不限於下列資源：

* 擷取服務帳戶的存取權杖，以便授權資料移轉。
* 如果啟用此選項，系統會將通知發布至提供的 Pub/Sub 主題。
* 啟動 BigQuery 工作。
* 從提供的 Pub/Sub 訂閱項目擷取事件，用於 Cloud Storage 事件驅動的轉移作業

啟用 BigQuery 資料移轉服務並首次使用 API 後，系統會自動為您建立服務代理程式。服務代理建立後，Google 會自動授予預先定義的[服務代理角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)。

### 跨專案服務帳戶授權

如果您使用專案中的服務帳戶授權資料移轉，但該專案與啟用 BigQuery 資料移轉服務的專案不同，則必須使用下列 Google Cloud CLI 指令，將 `roles/iam.serviceAccountTokenCreator` 角色授予服務代理程式：

```
gcloud iam service-accounts add-iam-policy-binding service_account \
--member serviceAccount:service-project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
--role roles/iam.serviceAccountTokenCreator
```

其中：

* service\_account 是用於授權資料移轉的跨專案服務帳戶。
* project\_number 是啟用 BigQuery 資料移轉服務的專案編號。

如要進一步瞭解跨專案資源設定，請參閱 Identity and Access Management 服務帳戶模擬說明文件中的「[為不同專案中的資源設定](https://docs.cloud.google.com/iam/docs/attach-service-accounts?hl=zh-tw#attaching-different-project)」。

透過 Google Cloud 控制台啟用 BigQuery 資料移轉服務 API 時，Google 會自動嘗試授予必要權限。不過，如果您透過 Terraform、Google Cloud CLI 或其他程式輔助方法啟用 API 或建立轉移作業，則必須手動設定必要權限。如要使用其他專案的服務帳戶授權轉移作業，請注意下列事項：

* **建立跨專案移轉的權限：**如要安全地存取跨專案資料來源，請將來源服務帳戶身分識別的 `roles/iam.serviceAccountTokenCreator` 角色授予 DTS 服務代理 (位於目的地專案中)。
* **實施最小權限原則：**在資源層級 (針對使用的特定服務帳戶) 授予這個角色，而非專案層級。

### 手動建立服務代理

如要在與 API 互動前觸發服務代理建立作業 (例如需要授予服務代理額外角色)，可以使用下列其中一種方法：

* API：
  [services.GenerateServiceIdentity](https://docs.cloud.google.com/service-usage/docs/reference/rest/v1beta1/services/generateServiceIdentity?hl=zh-tw)
* gcloud CLI：
  [gcloud beta services identity create](https://docs.cloud.google.com/sdk/gcloud/reference/beta/services/identity/create?hl=zh-tw)
* Terraform 供應商：
  [google\_project\_service\_identity](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_service_identity)

手動觸發建立服務代理時，Google 不會自動授予預先定義的[服務代理角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)。您必須使用下列 Google Cloud CLI 指令，手動授予服務代理程式預先定義的角色：

```
gcloud projects add-iam-policy-binding project_number \
--member serviceAccount:service-project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
--role roles/bigquerydatatransfer.serviceAgent
```

其中：

* project\_number 是啟用 BigQuery 資料移轉服務的專案編號。

**警告：** 請勿撤銷服務代理的服務代理角色。如果撤銷角色，BigQuery 資料移轉服務將無法運作。

## 授予 `bigquery.admin` 存取權

建議將`bigquery.admin`預先定義的 IAM 角色授予建立 BigQuery 資料移轉服務移轉作業的使用者。`bigquery.admin` 角色包含執行最常見工作所需的 IAM 權限。`bigquery.admin` 角色具備下列 BigQuery 資料移轉服務權限：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

**注意：** 自 2026 年 3 月 17 日起，BigQuery 資料移轉服務將需要 `bigquery.datasets.getIamPolicy` 和 `bigquery.datasets.setIamPolicy` 權限。詳情請參閱「[資料集層級存取控管的變更](https://docs.cloud.google.com/bigquery/docs/dataset-access-control?hl=zh-tw)」。**注意：** 如果 `bigquery.admin` 角色對特定用途而言過於廣泛，您可以[建立自訂 IAM 角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)，只授予必要的權限。

在某些情況下，不同資料來源可能需要不同的權限。如需特定 IAM 資訊，請參閱各資料來源移轉指南的「必要權限」一節。舉例來說，請參閱 [Amazon S3 移轉權限](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw#required_permissions)或 [Cloud Storage 移轉權限](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#required_permissions)。

如要授予 `bigquery.admin` 角色：

### 控制台

1. 在 Google Cloud 控制台中開啟「IAM」頁面

   [開啟「IAM」頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 按一下 [Select a project] (選取專案)。
3. 選取專案並點選 [Open] (開啟)。
4. 按一下 [Add] (新增)，將新成員加入專案並設定其權限。
5. 在「Add members」(新增成員) 對話方塊中：

   * 在「Members」(成員) 專區中輸入使用者或群組的電子郵件地址。
   * 在「Select a role」(選取角色) 下拉式選單中，依序點選 [BigQuery] > [BigQuery Admin] (BigQuery 管理員)。
   * 按一下 [Add] (新增)。

### gcloud

如要授予使用者或群組 `bigquery.admin` 的角色，您可以使用 Google Cloud CLI。

**注意：**
管理[外部身分識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

如要在專案的 IAM 政策中新增單一繫結，請輸入下列指令。如要新增使用者，請提供採用 `user:user@example.com` 格式的 `--member` 旗標。如要新增群組，請提供採用 `group:group@example.com` 格式的 `--member` 旗標。

```
gcloud projects add-iam-policy-binding project_id \
--member principal:address \
--role roles/bigquery.admin
```

其中：

* project\_id 是您的專案 ID。
* principal 是 `group` 或 `user`。
* address 是使用者或群組的電子郵件地址。

例如：

```
gcloud projects add-iam-policy-binding myproject \
--member group:group@example.com \
--role roles/bigquery.admin
```

這個指令會輸出更新後的政策：

```
    bindings:
    - members:
      - group:group@example.com
        role: roles/bigquery.admin
```

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

## 後續步驟

啟用 BigQuery 資料移轉服務後，請建立資料來源的移轉作業。

* 軟體即服務 (SaaS) 平台：

+ [Salesforce](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw)
+ [Salesforce Marketing Cloud](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw)
+ [ServiceNow](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw)

* 行銷平台：

+ [Facebook 廣告](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw)
+ [HubSpot](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Klaviyo](https://docs.cloud.google.com/bigquery/docs/klaviyo-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Mailchimp](https://docs.cloud.google.com/bigquery/docs/mailchimp-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))

* 付款平台：

+ [PayPal](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Stripe](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Shopify](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))

* 資料庫和資料倉儲：

+ [Amazon Redshift](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)
+ [Apache Hive Metastore](https://docs.cloud.google.com/bigquery/docs/hdfs-data-lake-transfer?hl=zh-tw)
+ [Microsoft SQL Server](https://docs.cloud.google.com/bigquery/docs/sqlserver-transfer?hl=zh-tw) ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [MySQL](https://docs.cloud.google.com/bigquery/docs/mysql-transfer?hl=zh-tw)
+ [Oracle](https://docs.cloud.google.com/bigquery/docs/oracle-transfer?hl=zh-tw)
+ [PostgreSQL](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw)
+ [Snowflake](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Teradata](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)

* 雲端儲存空間：

+ [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)
+ [Amazon Simple Storage Service (Amazon S3)](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw)
+ [Azure Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw)

* Google 服務：

+ [Campaign Manager](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw)
+ [購物比較服務 (CSS) 中心](https://docs.cloud.google.com/bigquery/docs/css-center-transfer-schedule-transfers?hl=zh-tw) ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Display & Video 360](https://docs.cloud.google.com/bigquery/docs/display-video-transfer?hl=zh-tw)
+ [Google Ads](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)
+ [Google Ad Manager](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw)
+ [Google Analytics 4](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw)
+ [Google Merchant Center](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
+ [Search Ads 360](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw)
+ [Google Play](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw)
+ [YouTube 頻道](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw)
+ [YouTube 內容擁有者](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]