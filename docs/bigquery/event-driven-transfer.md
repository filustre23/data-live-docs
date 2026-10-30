Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 事件導向移轉作業

BigQuery 資料移轉服務中的事件導向移轉作業，可讓您根據事件通知，自動將資料載入 BigQuery。如果工作負載可容忍轉移作業執行之間有幾分鐘的延遲，您可以使用這種方法，以符合成本效益的方式進行增量批次擷取。如需即時資料可用性，且延遲時間較短，請使用 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，直接將資料串流至 BigQuery。

## 支援事件導向移轉作業的資料來源

BigQuery 資料移轉服務可搭配下列資料來源，使用事件導向移轉作業：

* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)

## 限制

事件導向移轉至 BigQuery 的作業有下列限制：

* 事件導向移轉作業觸發後，BigQuery 資料移轉服務最多會等待 10 分鐘，才會觸發下一次移轉作業，無論這段期間內是否有事件發生。
* 事件導向移轉作業不支援來源 URI 或資料路徑的[執行階段參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)。
* 多項事件導向移轉設定無法重複使用同一個 Pub/Sub 訂閱項目。

## 設定 Cloud Storage 事件導向移轉作業

Cloud Storage 的事件導向移轉作業會使用 Pub/Sub 通知，瞭解來源 bucket 中的物件何時遭到修改或新增。使用[增量移轉](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#incremental_transfers)模式時，刪除來源 bucket 中的物件不會刪除目的地 BigQuery 資料表中的相關聯資料。

### 事前準備

設定 Cloud Storage 事件導向移轉作業前，請先完成下列步驟：

1. 為接收通知的專案啟用 Pub/Sub API。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=pubsub&hl=zh-tw)
2. 如果您是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，可以繼續[建立事件導向移轉設定](#create-transfer-configuration)。
3. 如果您不是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，請要求管理員授予 `roles/storage.admin` 和 `roles/pubsub.admin` 角色，或要求管理員完成下列各節的[設定 Pub/Sub](#configure-pubsub) 和[設定服務代理權限](#configure-service-agent-permissions)，並使用預先設定的 Pub/Sub 訂閱項目[建立事件導向移轉設定](#create-transfer-configuration)。
4. 設定事件導向移轉設定通知所需的詳細權限：

   * 如果您打算建立主題和訂閱項目來發布通知，則必須具備 [`pubsub.topics.create`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 和 [`pubsub.subscriptions.create`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 權限。
   * 無論您打算使用新的或現有的主題和訂閱項目，都必須具備下列權限。如果您已在 Pub/Sub 建立主題和訂閱項目，可能已具備這些權限。

     + [`pubsub.topics.getIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
     + [`pubsub.topics.setIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
     + [`pubsub.subscriptions.getIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
     + [`pubsub.subscriptions.setIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles)
   * 您必須具備下列權限，才能在 Cloud Storage bucket 設定 Pub/Sub 通知。

     + `storage.buckets.get`
     + `storage.buckets.update`
   * `pubsub.admin` 和 `storage.admin` 預先定義的 IAM 角色具備設定 Cloud Storage 事件導向移轉作業所需的所有權限。詳情請參閱「[Pub/Sub 存取控管](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#console)」。

#### 在 Cloud Storage 中設定 Pub/Sub 通知

1. 確認您已滿足搭配使用 Pub/Sub 與 Cloud Storage 的[必要條件](https://docs.cloud.google.com/storage/docs/reporting-changes?hl=zh-tw)。
2. 將通知設定套用至 Cloud Storage bucket：

   ```
   gcloud storage buckets notifications create gs://BUCKET_NAME --topic=TOPIC_NAME --event-types=OBJECT_FINALIZE
   ```

   更改下列內容：

   * `BUCKET_NAME`：要觸發檔案通知事件的 Cloud Storage bucket 名稱
   * `TOPIC_NAME`：要接收檔案通知事件的 Pub/Sub 主題名稱

   除了 gcloud CLI 之外，您也可以使用其他方法新增通知設定。詳情請參閱「[套用通知設定](https://docs.cloud.google.com/storage/docs/reporting-changes?hl=zh-tw#command-line)」。
3. 確認 Cloud Storage 的 Pub/Sub 通知設定正確。使用 `gcloud storage buckets notifications list` 指令：

   ```
   gcloud storage buckets notifications list gs://BUCKET_NAME
   ```

   如果成功，回應會與下列內容相似：

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

   將 `SUBSCRIPTION_ID` 替換為新 Pub/Sub 提取訂閱項目的名稱或 ID。

   您可以使用[其他方法](https://docs.cloud.google.com/pubsub/docs/create-subscription?hl=zh-tw#pubsub_create_pull_subscription)建立提取訂閱項目。

   **注意：** 多項以事件為依據的移轉設定，無法重複使用同一個 Pub/Sub 訂閱項目。

#### 設定服務代理權限

1. 找出專案的 [BigQuery 資料移轉服務代理程式](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)名稱：

   1. 前往「IAM & Admin」(IAM 與管理) 頁面。

      [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
   2. 勾選「包含 Google 提供的角色授予項目」核取方塊。
   3. BigQuery 資料移轉服務代理程式會列出名稱 `service-<project_number>@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`，並授予 [BigQuery 資料移轉服務代理程式角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent) (`roles/bigquerydatatransfer.serviceAgent`)。

   如要進一步瞭解服務代理，請參閱「[服務代理](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw)」。
2. 將 [Pub/Sub 訂閱者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber) (`pubsub.subscriber`) 授予 BigQuery 資料移轉服務代理。

   ### Cloud 控制台

   請按照「[透過 Google Cloud 控制台控管存取權](https://docs.cloud.google.com/pubsub/docs/access-control?hl=zh-tw#console)」中的操作說明，將 `Pub/Sub Subscriber` 角色授予 BigQuery 資料移轉服務代理。您可以在主題、訂閱項目或專案層級授予這個角色。

   ### `gcloud` CLI

   請按照「[設定政策](https://docs.cloud.google.com/pubsub/docs/access-control?hl=zh-tw#setting_a_policy)」中的操作說明，新增下列繫結：

   ```
   {
     "role": "roles/pubsub.subscriber",
     "members": [
       "serviceAccount:project-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com"
   }
   ```

   將 `PROJECT_NUMBER` 替換為託管轉移資源的[專案 ID](https://docs.cloud.google.com/resource-manager/docs/view-update-projects?hl=zh-tw#identifying_projects)，系統會建立這些資源並計費。

   **配額用量歸因：**BigQuery 資料移轉服務代理存取 Pub/Sub 訂閱項目時，配額用量會計入使用者專案。
3. 確認 BigQuery 資料移轉服務代理程式已獲派 [Pub/Sub 訂閱者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber) (`pubsub.subscriber`)。

   1. 前往 Google Cloud 控制台的「Pub/Sub」頁面。

      [前往「Pub/Sub」頁面](https://console.cloud.google.com/cloudpubsub/subscription/list?hl=zh-tw)
   2. 選取您在以事件為依據的移轉作業中使用的 Pub/Sub 訂閱項目。
   3. 如果資訊面板未顯示，請按一下右上角的「Show info panel」(顯示資訊面板)。
   4. 在「Permissions」(權限) 分頁中，確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)具備 [Pub/Sub 訂閱者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber) (`pubsub.subscriber`)。

#### 設定通知和權限的指令摘要

下列 Google Cloud CLI 指令包含設定通知和權限所需的所有指令，詳情請參閱前幾節。

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

如要建立事件導向 Cloud Storage 移轉作業，請[建立 Cloud Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#set_up_a_cloud_storage_transfer)，並選取「事件導向」做為「排程類型」。您是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，因此具備足夠權限，可讓 BigQuery 資料移轉服務自動設定 Cloud Storage 傳送通知。

如果您不是 Cloud Storage 管理員 (`roles/storage.admin`) 和 Pub/Sub 管理員 (`roles/pubsub.admin`)，則必須請管理員授予您這些角色，或請管理員完成必要的 [Cloud Storage 設定中的 Pub/Sub 通知](#configure-pubsub)和[服務代理權限設定](#configure-service-agent-permissions)，才能建立事件導向移轉作業。

**注意：** 請勿從 `pubsub.subscriber` 和 `serviceusage.serviceUsageConsumer` 預先定義的 IAM 角色中移除 [BigQuery 資料移轉服務代理程式](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw#bigquerydatatransfer.serviceAgent)。移除後，BigQuery 就無法接收 Pub/Sub 主題和訂閱項目的通知。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]