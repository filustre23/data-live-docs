Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 以事件為準的轉移

您可以使用 BigQuery 資料移轉服務建立事件驅動的移轉作業，根據事件通知自動載入資料。如果您需要以遞增方式擷取資料，並盡量節省費用，建議使用事件驅動的轉移作業。

設定以事件為準的轉移作業時，每次轉移資料之間可能會延遲幾分鐘。如需立即取得資料，建議使用 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，以盡可能最低的延遲時間，將資料直接串流至 BigQuery。Storage Write API 可為最嚴苛的用途提供即時更新。

選擇時，請考量您是否需要優先處理具成本效益的增量批次擷取作業 (透過事件驅動的轉移作業)，或是偏好使用 Storage Write API 的彈性。

## 支援事件導向移轉作業的資料來源

BigQuery 資料移轉服務可搭配下列資料來源，使用事件驅動型移轉：

* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)

## 限制

以事件為觸發條件的 BigQuery 移轉作業有下列限制：

* 觸發事件驅動型移轉後，無論事件是否在 10 分鐘內抵達，BigQuery 資料移轉服務都會等待最多 10 分鐘，才會觸發下一次移轉作業。
* 事件導向移轉作業不支援來源 URI 或資料路徑的[執行階段參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)。
* 多個事件驅動的轉移設定無法重複使用相同的 Pub/Sub 訂閱項目。

## 設定 Cloud Storage 事件驅動型轉移作業

從 Cloud Storage 進行事件驅動移轉時，系統會使用 Pub/Sub 通知，瞭解來源 bucket 中的物件何時經過修改或新增。使用[增量移轉](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#incremental_transfers)模式時，刪除來源 bucket 中的物件不會刪除目的地 BigQuery 資料表中的相關聯資料。

### 事前準備

設定 Cloud Storage 事件驅動移轉作業前，請先完成下列步驟：

1. 針對要接收通知的專案啟用 Pub/Sub API。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=pubsub&hl=zh-tw)
2. 如果您是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，可以繼續[建立事件驅動的移轉設定](#create-transfer-configuration)。
3. 如果您不是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，請要求管理員授予您 `roles/storage.admin` 和 `roles/pubsub.admin` 角色，或請管理員完成下列章節中的「[設定 Pub/Sub](#configure-pubsub)」和「[設定服務代理程式權限](#configure-service-agent-permissions)」，並使用預先設定的 Pub/Sub 訂閱項目[建立事件驅動的轉移設定](#create-transfer-configuration)。
4. 如要設定以事件為依據的移轉設定通知，您必須具備下列權限：

   * 如果您要建立主題和訂閱項目來發布通知，則必須具備 [`pubsub.topics.create`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 和 [`pubsub.subscriptions.create`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 權限。
   * 無論您要使用新的或現有的主題和訂閱項目，都必須具備下列權限。如果您已在 Pub/Sub 中建立主題和訂閱項目，則可能已具備這些權限。

     + [`pubsub.topics.getIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
     + [`pubsub.topics.setIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
     + [`pubsub.subscriptions.getIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
     + [`pubsub.subscriptions.setIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
   * 您必須在要設定 Pub/Sub 通知功能的 Cloud Storage 值區中，擁有下列權限。

     + `storage.buckets.get`
     + `storage.buckets.update`
   * 預先定義的 `pubsub.admin` 和 `storage.admin` IAM 角色具備所有必要權限，可設定 Cloud Storage 以事件為依據的移轉作業。詳情請參閱 [Pub/Sub 存取權控管](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#console)。

#### 在 Cloud Storage 中設定 Pub/Sub 通知

1. 確認您已滿足搭配使用 Pub/Sub 與 Cloud Storage 的[必要條件](https://docs.cloud.google.com/storage/docs/reporting-changes?hl=zh-tw)。
2. 將通知設定套用至 Cloud Storage bucket：

   ```
   gcloud storage buckets notifications create gs://BUCKET_NAME --topic=TOPIC_NAME --event-types=OBJECT_FINALIZE
   ```

   更改下列內容：

   * `BUCKET_NAME`：要觸發檔案通知事件的 Cloud Storage bucket 名稱
   * `TOPIC_NAME`：要接收檔案通知事件的 Pub/Sub 主題名稱

   除了 gcloud CLI，您也可以使用其他方法新增通知設定。詳情請參閱「[套用通知設定](https://docs.cloud.google.com/storage/docs/reporting-changes?hl=zh-tw#command-line)」。
3. 確認 Cloud Storage 的 Pub/Sub 通知設定正確。
   使用 `gcloud storage buckets notifications list` 指令：

   ```
   gcloud storage buckets notifications list gs://BUCKET_NAME
   ```

   如果成功，回應會類似以下內容：

   ```
   etag: '132'
   id: '132'
   kind: storage#notification
   payload_format: JSON_API_V1
   selfLink: https://www.googleapis.com/storage/v1/b/my-bucket/notificationConfigs/132
   topic: //pubsub.googleapis.com/projects/my-project/topics/my-bucket
   ```
4. 為主題建立提取訂閱項目：

   ```
   gcloud pubsub subscriptions create SUBSCRIPTION_ID --topic=TOPIC_NAME
   ```

   將 `SUBSCRIPTION_ID` 替換為新的 Pub/Sub 提取訂閱項目名稱或 ID。

   您可以使用[其他方法](https://docs.cloud.google.com/pubsub/docs/create-subscription?hl=zh-tw#pubsub_create_pull_subscription)建立提取訂閱項目。

   **注意：** 多個以事件為依據的移轉設定無法重複使用同一個 Pub/Sub 訂閱項目。

#### 設定服務代理權限

1. 找出專案的 [BigQuery 資料移轉服務代理程式](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)名稱：

   1. 前往「IAM & Admin」(IAM 與管理) 頁面。

      [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
   2. 勾選「包含 Google 提供的角色授予項目」核取方塊。
   3. BigQuery 資料移轉服務代理程式會列出名稱，並獲派 [BigQuery 資料移轉服務代理程式角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent) (`roles/bigquerydatatransfer.serviceAgent`)。`service-<project_number>@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`

   如要進一步瞭解服務代理人，請參閱「[服務代理人](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw)」。
2. 將 [Pub/Sub 訂閱者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber) (`pubsub.subscriber`) 授予 BigQuery 資料移轉服務代理人。

   ### Cloud 控制台

   請按照「[透過 Google Cloud 控制台控管存取權](https://docs.cloud.google.com/pubsub/docs/access-control?hl=zh-tw#console)」一文中的操作說明，將 `Pub/Sub Subscriber` 角色授予 BigQuery 資料移轉服務代理程式。您可以在主題、訂閱項目或專案層級授予角色。

   ### `gcloud` CLI

   請按照「[設定政策](https://docs.cloud.google.com/pubsub/docs/access-control?hl=zh-tw#setting_a_policy)」中的操作說明，新增下列繫結：

   ```
   {
     "role": "roles/pubsub.subscriber",
     "members": [
       "serviceAccount:project-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com"
   }
   ```

   將 `PROJECT_NUMBER` 替換為用於建立及計費轉移資源的[專案 ID](https://docs.cloud.google.com/resource-manager/docs/view-update-projects?hl=zh-tw#identifying_projects)。

   **配額用量歸因：**當 BigQuery 資料移轉服務代理程式存取 Pub/Sub 訂閱項目時，配額用量會向使用者專案收費。
3. 確認 BigQuery 資料移轉服務代理已獲派 [Pub/Sub 訂閱者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber) (`pubsub.subscriber`)。

   1. 前往 Google Cloud 控制台的「Pub/Sub」頁面。

      [前往 Pub/Sub](https://console.cloud.google.com/cloudpubsub/subscription/list?hl=zh-tw)
   2. 選取您在以事件為依據的移轉作業中使用的 Pub/Sub 訂閱項目。
   3. 如果資訊面板已隱藏，請按一下右上角的「顯示資訊面板」。
   4. 在「權限」分頁中，確認 BigQuery 資料移轉服務[服務代理程式](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)具有 [Pub/Sub 訂閱者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber) (`pubsub.subscriber`)。

#### 設定通知和權限的指令摘要

下列 Google Cloud CLI 指令包含所有必要指令，可設定通知和權限，詳情請參閱前幾節。

### gcloud

```
PROJECT_ID=project_id
CONFIG_NAME=config_name
RESOURCE_NAME="bqdts-event-driven-${CONFIG_NAME}"
# Create a Pub/Sub topic.
gcloud pubsub topics create "${RESOURCE_NAME}" --project="${PROJECT_ID}"
# Create a Pub/Sub subscription.
gcloud pubsub subscriptions create "${RESOURCE_NAME}" --project="${PROJECT_ID}" --topic="projects/${PROJECT_ID}/topics/${RESOURCE_NAME}"
# Create a Pub/Sub notification.
gcloud storage buckets notifications create gs://"${RESOURCE_NAME}" --topic="projects/${PROJECT_ID}/topics/${RESOURCE_NAME}" --event-types=OBJECT_FINALIZE
# Grant roles/pubsub.subscriber permission to the DTS service agent.
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format='value(projectNumber)')
gcloud pubsub subscriptions add-iam-policy-binding "${RESOURCE_NAME}"  --project="${PROJECT_ID}"  --member=serviceAccount:service-"${PROJECT_NUMBER}"@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com  --role=roles/pubsub.subscriber
```

更改下列內容：

* `PROJECT_ID`：專案 ID。
* `CONFIG_NAME`：用於識別這項移轉設定的名稱。

### 建立移轉設定

如要建立事件驅動的 Cloud Storage 移轉作業，請[建立 Cloud Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#set_up_a_cloud_storage_transfer)，然後選取「Schedule Type」(排程類型) 的「Event-driven」(事件驅動)。身為 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，您擁有足夠的權限，可讓 BigQuery 資料移轉服務自動設定 Cloud Storage 傳送通知。

如果您不是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，則必須請管理員授予您這些角色，或請管理員完成[Cloud Storage 設定中的必要 Pub/Sub 通知](#configure-pubsub)和[服務代理程式權限設定](#configure-service-agent-permissions)，才能建立事件驅動的移轉作業。

**注意：** 請勿從 `pubsub.subscriber` 和 `serviceusage.serviceUsageConsumer` 預先定義的 IAM 角色中移除 [BigQuery 資料移轉服務代理程式](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw#bigquerydatatransfer.serviceAgent)。移除後，BigQuery 就無法再接收來自 Pub/Sub 主題和訂閱項目的通知。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]