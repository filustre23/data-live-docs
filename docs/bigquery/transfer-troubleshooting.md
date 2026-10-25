Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解移轉設定問題

檢查 BigQuery 資料移轉服務的執行記錄和記錄檔，診斷並解決常見的設定、權限、配額和排程錯誤。您可以解決一般設定問題、修正授權失敗，以及復原資料來源中失敗的移轉作業。

如果遇到本文未提及的問題，可以[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。與 Cloud Customer Care 聯絡前，請先記錄移轉設定和執行資訊。詳情請參閱「[取得移轉作業詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#get_transfer_details)」和「[查看移轉作業執行詳細資料和記錄訊息](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_details_and_log_messages)」。

## 檢查錯誤

如果初始移轉作業執行失敗，您可以在[執行記錄](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_history)中查看詳細資料。執行記錄中列出的錯誤，可協助您使用本文件找出適當的解決方法。

您也可以使用[Logs Explorer](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw)，查看特定移轉工作的錯誤訊息。下列 Logs Explorer 篩選器會傳回特定移轉設定工作的相關資訊，以及任何錯誤訊息：

```
resource.type="bigquery_dts_config"
labels.run_id="RUN_ID"
resource.labels.config_id="CONFIG_ID"
```

更改下列內容：

* `RUN_ID`：特定工作執行的 ID 號碼
* `CONFIG_ID`：移轉設定工作的 ID 號碼

與客戶服務團隊聯絡前，請先從執行記錄或記錄探索工具擷取任何相關資訊，包括任何錯誤訊息。

如果您使用[事件導向移轉作業](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw)，事件導向移轉設定可能無法觸發移轉作業。您可以在[執行記錄](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_history)頁面或[設定](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#get_transfer_details)頁面頂端查看錯誤訊息。

## 一般問題

診斷一般移轉問題時，請確認下列事項：

* 針對移轉類型適用的說明文件頁面，確認是否已完成其中「事前準備」一節所述的所有步驟。
* 移轉設定屬性是否正確。
* 建立移轉作業所使用的使用者帳戶是否擁有基礎資源的存取權。

如果移轉設定正確，且取得適當權限，請參閱下列常見問題的解決方案。

錯誤：`An unexpected issue was encountered. If this issue persists, please contact customer support.`
:   **解決方法：**這項錯誤通常表示 BigQuery 暫時中斷或發生問題。請等待約 2 小時以解決問題。如果問題仍未解決，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

錯誤：`INTERNAL: An internal error occurred and the request could not be completed. This is usually caused by a transient issue...`
:   **解決方法：**這項錯誤通常表示發生暫時性內部問題。如果遇到這項錯誤，您可以等待下次排定的執行作業，看看問題是否解決，也可以[手動觸發受影響日期的補填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。如果問題仍未解決，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

錯誤：`Quota Exceeded.`
:   **解決方法：**移轉作業須遵守 BigQuery 的[載入工作配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)。如要提高配額，請洽詢 Google Cloud 業務代表。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

    將 Cloud Billing 匯出項目載入 BigQuery 時，可能會遇到 `Quota Exceeded` 錯誤。Cloud Billing 匯出資料表和 BigQuery 資料移轉服務建立的目的地 BigQuery 資料表都會分區。設定這類 BigQuery 資料移轉服務工作時，如果選擇「overwrite」(覆寫) 選項，系統會根據匯出的資料量，產生配額錯誤。如要瞭解如何排解配額問題，請參閱「[排解配額和限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。

    如果錯誤是由 Cloud Billing 匯出作業的 BigQuery 資料移轉服務工作所造成，請注意，由於個別 Cloud Billing 匯出資料表已分區，BigQuery 資料移轉服務建立的目標資料表也會分區，因此在設定這類資料移轉工作時，選擇「覆寫」選項會導致 (DML) 配額錯誤，具體取決於帳單帳戶的使用時間。如要瞭解如何排解配額問題，請參閱「[解決配額與限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。

錯誤：`The caller does not have permission.`
:   **解決方法：**確認 Google Cloud 控制台中的登入帳戶，與建立移轉作業時為 BigQuery 資料移轉服務選取的帳戶相同。

    * Google Cloud 控制台中的登入帳戶：
    * 選擇帳戶，繼續使用 BigQuery 資料移轉服務：

錯誤：`Access Denied: ... Permission bigquery.tables.get denied on table ...`
:   **解決方法：**確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)已獲得目標資料集的 [`bigquery.dataEditor` 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)。建立及更新移轉作業時，系統會自動套用這項授權，但之後可能會手動修改存取權政策。如要重新授予權限，請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

錯誤：`region violates constraint constraints/gcp.resourceLocations on the resource projects/project_id`
:   **解決方法：**如果使用者嘗試在[位置限制組織政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw)指定的受限位置建立移轉設定，就會發生這項錯誤。如要解決這個問題，請[變更組織政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw#setting_the_organization_policy)，允許使用該區域，或將移轉設定變更為位於不受組織政策限制的區域中的目的地資料集。

錯誤：`Please look into the errors[] collection for more details.`
:   **解決方法：**資料移轉失敗時，可能會發生這項錯誤。如要進一步瞭解資料移轉失敗的原因，請[使用 Cloud Logging 查看記錄](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw#logs)。您可以使用移轉作業 `run_id` 進行搜尋，[找出特定執行作業的記錄](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw#view_transfer_run_logs)。

錯誤：`Network Attachment with connected endpoints cannot be deleted.`
:   **解決方法：**如果使用者在[刪除移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#delete_a_transfer)後，立即嘗試刪除網路連結，就可能發生這項錯誤。這是因為 BigQuery 資料移轉服務可能需要幾天時間，才能完全移除與移轉作業相關聯的所有資源，這可能會導致網路連結無法刪除。如要解決這項錯誤，請等待幾天，再嘗試刪除網路連結。如要提前刪除網路連結，請[聯絡支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

錯誤：`Error while reading data, error message: CSV processing encountered too many errors, giving up.`
:   **解決方法：**如果資料來源中的 CSV 檔案設定與移轉設定中的 CSV 設定不符，就可能發生這項錯誤。舉例來說，如果「Header rows to skip」(要略過的標頭列) 設為 `0`，但來源 CSV 檔案包含 1 個以上的標頭列，就可能發生這項錯誤。如要修正這項錯誤，請確認移轉設定中的 CSV 設定正確無誤，且與來源 CSV 檔案的設定相符。

錯誤：`Error 400: DTS service agent needs iam.serviceAccounts.getAccessToken permission or [SERVICE_ACCOUNT] doesn't exist.`
:   **根本原因：**這項錯誤表示 BigQuery 資料移轉服務 (DTS) 服務代理程式缺少必要權限，無法模擬用於移轉作業的服務帳戶。這通常發生在跨專案授權情境，或使用 Terraform 等基礎架構即程式碼 (IaC) 工具設定移轉作業時。
:   **解決方法：**將服務帳戶權杖建立者角色 (`roles/iam.serviceAccountTokenCreator`) 授予 DTS 服務代理，並指定需要模擬的服務帳戶。

    ```
    gcloud iam service-accounts add-iam-policy-binding service_account \
    --member serviceAccount:service-destination_project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
    --role roles/iam.serviceAccountTokenCreator
    ```

    其中：

* service\_account 是用於授權轉移作業的帳戶電子郵件地址。
* destination\_project\_number 是移轉設定所在的專案編號。如要瞭解如何找出專案編號，請參閱「[尋找專案名稱、編號和 ID](https://docs.cloud.google.com/resource-manager/docs/view-update-projects?hl=zh-tw#identifying_projects)」。

錯誤：`For asset "ASSET", no eligible column found for splitting (Reason: Primary or Indexed Key columns found, but none are of supported types (INTEGER, TINYINT, SMALLINT, FLOAT, REAL, DOUBLE, NUMERIC, BIGINT, DECIMAL, DATE, BOOLEAN))`
:   **解決方法：**如果嘗試從來源資料表移轉超過 2,000,000 筆記錄到 BigQuery 資料表，但來源資料表沒有主鍵或支援資料類型的索引資料欄，就可能發生這項錯誤。如要解決這個問題，請在來源資料表中，將採用其中一種支援資料類型的資料欄，設為主鍵或索引資料欄。詳情請參閱移轉來源指南的限制部分。

錯誤：`Permission bigquery.tables.create denied.`
:   **問題：**

    ```
    Error code 7 : Access Denied : Dataset [PROJECT_ID]:[DATASET_ID] : Permission bigquery.tables.create denied on dataset [PROJECT_ID]:[DATASET_ID] (or it may not exist).
    ```

    Cloud Storage 移轉作業失敗，並顯示建立資料表時存取遭拒的錯誤，即使目的地資料表已存在，且服務帳戶具備標準資料編輯者角色，也一樣。
:   **原因：**如果 Cloud Storage 移轉作業涉及超過 10,000 個檔案，且未授予 `bigquery.tables.create` 權限，就會發生這項錯誤。如果移轉的檔案超過 10,000 個，服務會將資料分割成動態建立的暫存資料表。即使專案已註冊高量移轉作業 (或已獲准提高配額)，仍須具備 bigquery.tables.create 權限才能執行這項操作。
:   **解決方法：**如要成功移轉超過 10,000 個檔案，請務必符合下列兩項規定：

1. **確認配額和功能註冊：**確認專案已註冊大量 Cloud Storage 移轉作業 (超過 10,000 個檔案)。如需轉移超過 10,000 個檔案，請[聯絡支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，要求提高每次轉移作業的檔案數量上限。
2. **授予必要的 IAM 權限：**將目的地資料集的 `bigquery.tables.create` 權限，授予執行移轉作業的服務帳戶或使用者身分。BigQuery 資料編輯者 (`roles/bigquery.dataEditor`) 和 BigQuery 管理員 (`roles/bigquery.admin`) 角色具備這項權限。如果授予必要權限後仍持續失敗，請[聯絡支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，確認許可清單狀態。

   **替代方案：**如果您無法授予必要權限，或無法等待配額增加和設定變更，請考慮下列選項：

   * 將每次轉移作業執行的檔案數量減少至 10,000 個以下，例如使用更具體的 URI 萬用字元，或將轉移作業拆分為多個較小的設定。
   * 如要進行一次性移轉或緊急載入，請使用 BigQuery [載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)或 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_data_statement)，這兩者都支援較高的[每項載入工作檔案數量上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)。

## 授權和權限問題

從不同資料來源移轉資料時，可能會遇到下列常見的權限錯誤：

錯誤：`BigQuery Data Transfer Service is not enabled for <project_id>`

錯誤：`BigQuery Data Transfer Service has not been used in project <project_id> before or it is disabled ...`
:   **解決方法：**
    請按照下列步驟，確認服務代理是否已獲派角色：

    1. 前往 Google Cloud 控制台的「IAM & Admin」(IAM 與管理) 頁面。

       [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
    2. 勾選**「包含 Google提供的角色授予項目」**核取方塊。
    3. 確認系統顯示名稱為 `service-<project_number>@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com` 的服務帳戶，或已授予 BigQuery 資料移轉服務 [BigQuery 資料移轉服務代理人角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)。

    如果畫面上未顯示服務帳戶，或該帳戶未獲派 BigQuery 資料移轉服務代理角色，請在 Google Cloud 控制台授予預先定義的角色，或執行下列 Google Cloud CLI 指令：

    ```
    gcloud projects add-iam-policy-binding PROJECT_NUMBER \
    --member serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
    --role roles/bigquerydatatransfer.serviceAgent
    ```

    將 `PROJECT_NUMBER` 替換為與這個服務帳戶相關聯的專案編號。

錯誤：`There was an error loading this table. Check that the table exists and that you have the correct permissions.`
:   **解決方法：**

    1. 前往 Google Cloud 控制台的「BigQuery」頁面。

       [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
    2. 按一下移轉作業使用的目的地資料集。
    3. 依序點選「共用」選單和「權限」。
    4. 展開「BigQuery 資料編輯者」角色。
    5. 確認 BigQuery 資料移轉服務代理已新增至這個角色。如果沒有，請將 BigQuery 資料編輯者 (`roles/bigquery.dataEditor`) 角色授予 BigQuery 資料移轉服務代理。

錯誤：`A permission denied error was encountered: PERMISSION_DENIED. Please ensure that the user account setting up the transfer config has the necessary permissions, and that the configuration settings are correct`
:   **解決方法：**

    1. 在 Google Cloud 控制台中，前往「Data Transfers」(資料移轉) 頁面。

       [前往「Data Transfers」(資料移轉)](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
    2. 按一下失敗的移轉作業，然後選取「設定」分頁標籤。
    3. 確認「User」(使用者) 欄位中列出的移轉作業擁有者具備資料來源的所有必要權限。

    如果移轉作業擁有者不具備所有必要權限，請[更新其憑證](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_credentials)，授予必要權限。您也可以將移轉作業擁有者變更為具備必要權限的其他使用者。

錯誤：`Authentication failure: User Id not found. Error code: INVALID_USERID`
:   **解決方法：**轉移作業擁有者的使用者 ID 無效。[更新憑證](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_credentials)，將轉移作業擁有者變更為其他使用者。如果您使用服務帳戶，也應確認執行資料移轉作業的帳戶具備[使用服務帳戶的所有必要權限](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw#required_permissions)。

錯誤：`The user does not have permission`
:   **解決方法：**確認移轉作業擁有者是服務帳戶，且服務已設定所有必要權限。另一個可能原因是，所用服務帳戶是在其他專案建立，而非建立這項移轉作業的專案。如要解決跨專案權限問題，請參閱下列資源：

    * [啟用跨專案附加服務帳戶的功能](https://docs.cloud.google.com/iam/docs/attach-service-accounts?hl=zh-tw#enabling-cross-project)
    * [跨專案服務帳戶授權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#cross-project_service_account_authorization) (用於授予必要權限)

錯誤：`HttpError 403 when requesting returned "The caller does not have permission"`
:   `googleapiclient.errors.HttpError: <HttpError 403 when requesting returned "The caller does not have permission". Details: "The caller does not have permission">`
:   嘗試使用服務帳戶設定排定查詢時，可能會出現這項錯誤。
:   **解決方法：**確認服務帳戶具備[排定或修改排定查詢所需的所有權限](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#required_permissions)，並確認設定排定查詢的使用者[有權存取服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw#service-account-permissions)。

    如果已指派所有正確權限，但仍發生錯誤，請檢查專案是否預設強制執行「停用跨專案服務帳戶」政策。如要查看政策，請前往 Google Cloud 控制台，依序點選「IAM & Admin」(IAM 與管理) >「Organization Policies」(組織政策)，然後搜尋政策。

    如果強制執行「停用跨專案服務帳戶」政策，您可以按照下列步驟停用政策：

    1. 使用 Google Cloud 控制台，依序前往「IAM & Admin」(IAM 與管理) >「Service Accounts」(服務帳戶)，找出與專案相關聯的服務帳戶。這個檢視畫面會顯示目前專案的所有服務帳戶。
    2. 使用下列指令，在服務帳戶所在的專案中停用政策。如要停用這項政策，使用者必須是[組織政策管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/orgpolicy?hl=zh-tw#orgpolicy.policyAdmin)。只有組織管理員可以將這個角色授予使用者。

    ```
    gcloud resource-manager org-policies disable-enforce iam.disableCrossProjectServiceAccountUsage --project=[PROJECT-ID]
    ```

## 事件導向移轉設定問題

建立事件導向移轉作業時，可能會遇到下列常見問題。

錯誤：`Data Transfer Service is not authorized to pull message from the provided Pub/Sub subscription.`
:   **解決方法：**確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)已獲派 [`pubsub.subscriber` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber)：

    1. 前往 Google Cloud 控制台的「Pub/Sub」頁面。

       [前往「Pub/Sub」頁面](https://console.cloud.google.com/cloudpubsub/subscription/list?hl=zh-tw)
    2. 選取您在以事件為依據的移轉作業中使用的 Pub/Sub 訂閱項目。
    3. 如果資訊面板未顯示，請按一下右上角的「Show info panel」(顯示資訊面板)。
    4. 在「Permissions」(權限) 分頁中，確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)具備 [`pubsub.subscriber` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber)
:   如果服務代理未取得 `pubsub.subscriber` 角色，按一下 person\_add「Add principal」(新增主體)，將 `pubsub.subscriber` 角色授予 `service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`

錯誤：`Cloud Pub/Sub API has not been used in project PROJECT_NUMBER before or it is disabled.`
:   **解決方法：**確認專案已啟用 Cloud Pub/Sub API：

    1. 在 Google Cloud 控制台中，前往「APIs & Services」(API 與服務) 頁面。

       [前往「API 與服務」頁面](https://console.cloud.google.com/apis/dashboard?hl=zh-tw)
    2. 按一下「啟用 API 和服務」。
    3. 搜尋 `Cloud Pub/Sub API`，選取第一個結果，然後按一下「啟用」。

錯誤：`Data Transfer Service does not have required permission to use project quota of project PROJECT_NUMBER to access Pub/Sub.`
:   **解決方法：**確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)已獲派 [`serviceusage.serviceUsageConsumer` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)：

    1. 前往 Google Cloud 控制台的「IAM & Admin」(IAM 與管理) 頁面。

       [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
    2. 勾選**「包含 Google提供的角色授予項目」**核取方塊。
    3. 確認系統顯示名稱為 `service-<project_number>@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com` 的服務帳戶，且該帳戶已獲派[服務使用情形消費者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)。

問題：使用 Cloud Storage 事件導向移轉作業時，在 Cloud Storage bucket 上傳或更新檔案後，系統未觸發移轉作業。
:   收到事件後，系統不會立即觸發移轉作業。轉移作業可能需要幾分鐘才會觸發。如要查看下次轉移作業執行的狀態，請查看[執行記錄](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_history)中的「Target date for next run」(下次執行的目標日期) 欄位。這個欄位會顯示下次執行的排定時間，如果未收到任何事件，則會顯示「waiting for events to schedule next run」。如果您已在 Cloud Storage bucket 中上傳或更新檔案，但「Target date for next run」(下次執行的目標日期) 並未更新，且 10 到 20 分鐘內未觸發任何執行作業，請參閱下列解決方法。
:   **解決方法：**確認移轉設定中指定的 Pub/Sub 訂閱項目，能取得 Cloud Storage 事件發布的訊息：

    1. 前往 Google Cloud 控制台的「Pub/Sub」頁面。

       [前往「Pub/Sub」頁面](https://console.cloud.google.com/cloudpubsub/subscription/list?hl=zh-tw)
    2. 選取您在以事件為依據的移轉作業中使用的 Pub/Sub 訂閱項目。
    3. 在「Metrics」(指標) 分頁中，查看「Oldest unacked message age」(最舊未確認訊息存在時間) 圖表，確認是否有任何訊息。
:   如果沒有發布任何訊息，請檢查 Cloud Storage 的 Pub/Sub 通知設定是否正確。您可以使用下列 Google Cloud CLI 指令，查看與 bucket 相關聯的通知設定：

    ```
    gcloud storage buckets notifications list gs://BUCKET_NAME
    ```

    將 `BUCKET_NAME` 替換為用於通知的值區名稱。如要瞭解如何設定 Cloud Storage 的 Pub/Sub 通知，請參閱「[設定 Cloud Storage 的 Pub/Sub 通知](https://docs.cloud.google.com/storage/docs/reporting-changes?hl=zh-tw)」。
:   如果有訊息，請檢查其他事件導向移轉設定是否使用相同的 Pub/Sub 訂閱項目。多項事件導向移轉設定無法重複使用同一個 Pub/Sub 訂閱項目。如要進一步瞭解事件導向移轉作業，請參閱「[事件導向移轉作業](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw)」。

## Amazon S3 移轉作業問題

以下是[建立 Amazon S3 移轉作業](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw)時常見的錯誤。

### Amazon S3 `PERMISSION_DENIED` 錯誤

錯誤：`The AWS Access Key Id you provided does not exist in our records.`
:   **解決方法：**確認存取金鑰存在且 ID 正確。

錯誤：`The request signature we calculated does not match the signature you provided. Check your key and signing method.`
:   **解決方法：**確認移轉設定具有正確的對應 Secret Access Key

錯誤：`Failed to obtain the location of the source S3 bucket. Additional details: Access Denied`

錯誤：`Failed to obtain the location of the source S3 bucket. Additional details: HTTP/1.1 403 Forbidden`

錯誤：`Access Denied` (S3 錯誤訊息)
:   **解決方法：**確認 AWS IAM 使用者有權執行下列操作：

    * 列出 Amazon S3 值區。
    * 取得值區的位置。
    * 讀取值區中的物件。

錯誤：`Server unable to initialize object upload.; InvalidObjectState: The operation is not valid for the object's storage class`

錯誤：`Failed to obtain the location of the source S3 bucket. Additional details: All access to this object has been disabled`
:   **解決方法：**還原封存至 Amazon Glacier 的所有物件。Amazon S3 中封存至 Amazon Glacier 的物件必須先還原，才能存取

錯誤：`All access to this object has been disabled`
:   **解決方法：**確認移轉設定中的 Amazon S3 URI 正確無誤

### Amazon S3 移轉限制錯誤

錯誤：`Number of files in transfer exceeds limit of 10,000.`
:   **解決方法：**評估是否能將 Amazon S3 URI 中的[萬用字元](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#wildcard-support)數量減少到一個。如果可以，請使用新的移轉設定重試，因為[每次移轉作業的檔案數量上限會較高](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#quotas_and_limits)。您也可以評估是否能將移轉設定拆分為多個移轉設定，每個設定分別移轉一部分的來源資料。

錯誤：`Size of files in transfer exceeds limit of 16492674416640 bytes.`
:   **解決方法：**評估是否能將移轉設定拆分為多個移轉設定，每個設定移轉一部分的來源資料。

### 一般 Amazon S3 問題

問題：檔案已從 Amazon S3 移轉，但未載入 BigQuery。
:   轉移記錄可能類似如下：`Moving data from Amazon S3 to Google Cloud complete: Moved N object(s).
    No new files found matching Amazon_S3_URI.`
:   **解決方法：**確認移轉設定中的 Amazon S3 URI 正確無誤。如果移轉設定是要載入所有具有通用前置字串的檔案，請確認 Amazon S3 URI 結尾為萬用字元。舉例來說，如要載入 `s3://my-bucket/my-folder/` 中的所有檔案，移轉設定中的 Amazon S3 URI 必須是 `s3://my-bucket/my-folder/*`，而非 `s3://my-bucket/my-folder/`。

## Azure Blob 儲存體移轉問題

以下是[建立 Blob Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`Number of files in transfer exceeds the limit of 10,000.`
:   **解決方法：**將 Blob 儲存體資料路徑中的[萬用字元](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#wildcard-support)數量減少至 0 或 1，檔案數量上限就會增加至 10,000,000。您也可以拆分成多項移轉設定，每項設定移轉一部分來源。

錯誤：`Size of files in transfer exceeds the limit of 15 TB.`
:   **解決方法：**拆分成多項移轉設定，每項設定移轉一部分來源資料。

錯誤：`Provided Azure SAS Token does not have required permissions.`
:   **解決方法：**確認移轉設定中的 Azure SAS 權杖正確無誤。詳情請參閱「[共用存取簽章 (SAS)](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#shared-access-signature)」。

錯誤：`Transfer encountered error, status:PERMISSION_DENIED, details:[This request is not authorized to perform this operation.]`
:   **解決方法：**確認 BigQuery 資料移轉服務 worker 使用的 IP 範圍已加入許可 IP 清單。詳情請參閱「[IP 限制](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#ip_restrictions)」。

問題：檔案已從 Blob Storage 轉移，但未載入 BigQuery。
:   轉移記錄可能如下所示：`Moving data to Google Cloud complete: Moved
    <var>N</var> object(s). No new files found matching Blob Storage data path.`
:   **解決方法：**確認移轉設定中的 Blob 儲存體資料路徑正確無誤。

## Campaign Manager 移轉問題

以下是[建立 Campaign Manager 移轉作業](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`

錯誤：`No data available for the requested date. Please try an earlier run date or verify that data existence was expected.`
:   **解決方法：**確認您使用的轉移[ID 正確無誤](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw#set_up_a_campaign_manager_transfer)。如果 ID 正確，請確認 Campaign Manager Cloud Storage bucket 包含指定日期範圍的 Data Transfer 2.0 版檔案。如果檔案存在，請排定受影響日期範圍內的補充作業。如要進一步瞭解如何建立 Campaign Manager 補充資料要求，請參閱「[手動觸發移轉或補充資料](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer_or_backfill)」。
:   您可以查看 Cloud Storage bucket 中檔案的建立時間，確認檔案在排定移轉作業時是否存在。在某些情況下，當天的第一次移轉作業可能會排定在第一批 Campaign Manager 資料移轉檔案產生之前。當天和隔天的後續執行作業會載入 Campaign Manager 生成的所有檔案。

錯誤：`A permission denied error was encountered: PERMISSION_DENIED. Please ensure that the user account setting up the transfer config has the necessary permissions, and that the configuration settings are correct.`
:   **解決方法：**建立 Campaign Manager 移轉作業的使用者，必須具備 [Cloud Storage bucket](https://console.cloud.google.com/storage?hl=zh-tw) 的讀取權限，才能存取 Data Transfer 2.0 版檔案。您可以取得 Cloud Storage bucket 的相關資訊，並向 Campaign Manager 管理員要求存取權。

錯誤：`Unexpected fields found: [FIELD_NAMES]; Table: 'TABLE_NAME', file: FILE_NAME`
:   **解決方法：**Campaign Manager 移轉作業支援 Campaign Manager 支援的部分欄位。如果遇到這項錯誤，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，提出功能要求。

## Google Ads 移轉問題

以下是[建立 Google Ads 移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)時常見的錯誤。

問題：移轉作業成功執行，但目的地資料表未顯示部分帳戶。
:   **解決方法：**帳戶未顯示在報表中的原因有很多，以下列舉幾個常見原因：

    * 如果指定日期沒有任何報表活動，就不會產生任何資料列。
    * 如果 Google Ads 帳戶處於閒置狀態，或`CANCELLED`，也可能發生這種情況。Google Ads API 不支援查詢停用帳戶，因此 Google Ads 連接器會從移轉作業中篩除停用帳戶。如要重新啟用 Google Ads 帳戶，請參閱「[重新啟用已取消的 Google Ads 帳戶](https://support.google.com/google-ads/answer/2375392?hl=zh-tw)」一文。

錯誤：`AUTH_ERROR_TWO_STEP_VERIFICATION_NOT_ENROLLED`
:   **解決方法：**這項錯誤表示這項移轉作業使用的 Google Ads 使用者未啟用兩步驟驗證。如要瞭解如何啟用兩步驟驗證，請參閱「[開啟兩步驟驗證](https://support.google.com/accounts/answer/185839?hl=zh-tw)」。

錯誤：`No jobs to start for run`
:   **解決方法：**這項錯誤表示設定無效，或處理期間發生錯誤，因此轉移作業未啟動載入工作。請按照下列步驟解決這項錯誤：

    * 查看移轉作業執行記錄，找出錯誤和警告。
    * 如果嘗試載入的資料表不含 `segments_date`、`segments_week`、`segments_month`、`segments_quarter` 或 `segments_year` 資料欄，且 `run_date` 不是最新日期，系統會略過載入作業。詳情請參閱「[手動觸發 Google Ads 移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#backfill)」和「[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#custom_reports)」。
    * 如果無法找出根本原因，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`

錯誤：`No data available for the requested date. Please try an earlier run date or verify that data existence was expected.`
:   **解決方法：**如果您在建立 Google Ads 移轉作業時收到這則錯誤訊息，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，並附上錯誤訊息的螢幕擷取畫面。

錯誤：`AuthenticationError.NOT_ADS_USER.`
:   **解決方法：**設定 Google Ads 移轉作業的使用者必須擁有 Google Ads 帳戶/登入資訊。

錯誤：`Request is missing required authentication credential`
:   **解決方法：**使用者或服務帳戶沒有廣告帳戶存取權。按照「[必要權限](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#required_permissions)」一節的說明，將必要權限授予使用者或服務帳戶。

錯誤：`ERROR_GETTING_RESPONSE_FROM_BACKEND.`
:   **解決方法：**如果 Google Ads 移轉作業失敗並傳回 `ERROR_GETTING_RESPONSE_FROM_BACKEND`，請在移轉設定中[啟用「Exclude Removed/Disabled Items」(排除已移除/停用的項目) 選項](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer)，並[設定補填](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，嘗試擷取移轉作業失敗當天的資料。

警告：`Data for the report ClickStats was not available for the specified date.`

錯誤：`INVALID_DATE_RANGE_FOR_REPORT.`
:   **解決方法：**如果回填超過 90 天前的[點擊成效報表](https://developers.google.com/adwords/api/docs/appendix/reports/click-performance-report?hl=zh-tw)資料，就會發生這種情況。在這種情況下，系統會顯示這則警告或錯誤，且不會更新指定日期的 `ClickStats` 資料表。

錯誤：`Error while processing report for table table_name for account id account_id. Http(400) Bad Request;`

錯誤：`AuthorizationError.TWO_STEP_VERIFICATION_NOT_ENROLLED`
:   **解決方法：**如果與這項移轉作業相關聯的使用者帳戶未啟用兩步驟驗證 (或多重驗證)，請為這個帳戶[啟用兩步驟驗證](https://support.google.com/google-ads/answer/12864186?hl=zh-tw)，然後重新執行失敗的移轉工作。服務帳戶不受兩步驟驗證規定限制。

錯誤：`Quota exceeded: Your project exceeded quota for imports per project`
:   **解決方法：**移轉作業須遵守 BigQuery 的[載入工作配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)。如果達到載入工作的配額限制，請嘗試使用 [table\_filter](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer)、刪除未使用的移轉設定或縮短更新時間範圍，減少不必要的載入作業。如要提高配額，請洽詢 Google Cloud 業務代表。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

## Google Ad Manager 移轉問題

以下是建立 [Google Ad Manager 移轉作業](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`Another transfer run is concurrently processing table.`
:   **解決方法：**如果目前移轉作業開始時，採用相同移轉設定的其他移轉作業尚未完成，就可能發生這項錯誤。

* 如果延遲是由大型 Google Ad Manager 資料移轉 (Google Ad Manager DT) 檔案造成，建議啟用載入效能較佳的 [Parquet 格式](https://support.google.com/admanager/answer/1733124?hl=zh-tw)。
* 如果延遲是由對照表造成，建議將 `load_match_tables` 參數設為 `false`，略過對照表。
* 如果轉移作業的處理時間一律長於目前的重複頻率，請調整重複頻率。

錯誤：`No data available for the requested date. Please try an earlier run date or verify that data existence was expected.`

錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`
:   **解決方法：**確認 Google Ad Manager [Cloud Storage bucket](http://console.cloud.google.com/storage?hl=zh-tw) 包含指定日期範圍的資料移轉檔案。Google Ad Manager 管理員會管理包含資料移轉檔案的 [Cloud Storage bucket](http://console.cloud.google.com/storage?hl=zh-tw)。建立 Google Ad Manager 移轉作業的使用者必須是 Google 網上論壇中擁有值區存取權的成員。
:   您可以嘗試讀取 Google Ad Manager [資料移轉 bucket](http://console.cloud.google.com/storage?hl=zh-tw) 中的檔案，驗證 Cloud Storage 權限。如要進一步瞭解 Google Ad Manager Cloud Storage bucket，請參閱「[存取 Google Ad Manager 儲存空間 bucket](https://support.google.com/admanager/answer/1733127?hl=zh-tw)」。
:   您可以查看 Cloud Storage bucket 中檔案的建立時間，確認檔案在排定移轉作業時是否存在。在某些情況下，當天第一次移轉作業的排定時間，可能會早於第一批 Google Ad Manager 資料移轉檔案的產生時間。當天和隔天後續執行時，系統會載入 Google Ad Manager 產生的所有檔案。
:   如果檔案存在於資料移轉 bucket 中，且您具備讀取的權限，請安排受影響日期範圍的補充作業。如要進一步瞭解如何建立 Google Ad Manager 候補請求，請參閱「[設定候補](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)」。

錯誤：`AuthenticationError: NO_NETWORKS_TO_ACCESS.`
:   **解決方法：**確定您具有 Google Ad Manager 網路的讀取權限。如需協助判斷網路存取權，請與 [Google Ad Manager 支援團隊](https://support.google.com/admanager/answer/3059042?hl=zh-tw)聯絡。

錯誤：`Error code 9 : Field field_name?field_name?field_name?RefererURL is unknown.; Table: table_name`
:   **解決方法：**確定您不是使用小寫的古英語符文字母 (þ) 分隔符號。不支援 thorn 分隔符號。若使用小寫的古英語符文字母，系統會在錯誤訊息中以 ? 錯誤訊息中。

錯誤：`Incompatible table partitioning specification. Destination table exists with partitioning specification interval(type:Day,field:) clustering`
:   **解決方法：**Google Ads Manager 連接器不支援將資料移轉至含有叢集的資料集。請改用未分群的資料集。

## Search Ads 360 移轉作業問題

以下是[建立 Search Ads 360 移轉作業](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`No jobs to start for run`
:   **解決方法：**如果使用表格篩選器，只篩選指標表格 (包含 `stats` 的表格)，但執行移轉作業的管理員或副管理員帳戶沒有任何相關聯的有效客戶帳戶，就會發生這項錯誤。如要解決這項錯誤，請移除資料表篩選器，或變更資料表篩選器，納入比對資料表 (不含 `stats` 的資料表)。

## Google Merchant Center 移轉問題

以下是[建立 Google Merchant Center 移轉作業](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`No data to transfer found for the Merchant account. If you have just created this transfer - you may need to wait for up to 90 minutes before the data of your Merchant account are prepared and available for the transfer.`
:   **解決方法：**如果您在「Schedule」(排程) 區段中使用預設的開始日期和時間設定移轉作業，就會收到這則錯誤訊息。如果您使用預設的排程值，第一項移轉作業會在移轉建立後立即開始執行，但由於您的商家帳戶資料尚未準備就緒，因此執行作業會失敗。等待 90 分鐘，然後[設定今天的補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，或等到明天再執行下一次排定的作業。

錯誤：`No data to transfer found for Merchant account. This can be because your account currently doesn't have any products.`
:   **解決方法：**這項錯誤表示商家帳戶中沒有產品。將產品新增至 Merchant 帳戶後，轉移作業就會開始。

錯誤：`Transfer user doesn't have access to the Merchant account. Please verify access in the Users section of the Google Merchant Center.`
:   **解決方法：**這項錯誤表示設定移轉作業的使用者，無權存取移轉作業使用的商家帳戶。如要解決問題，請在 Google Merchant Center [驗證並授予缺少的帳戶存取權](https://support.google.com/merchants/answer/1637190?hl=zh-tw)。

錯誤：`Transfer user doesn't have user roles that allows access to the product data of the Merchant account. Please verify access and roles in the Users section of the Google Merchant Center.`
:   **解決方法：**這項錯誤表示設定移轉作業的使用者，無權存取移轉作業所用商家帳戶的產品資料。如要解決這個問題，請在 Google Merchant Center 中[驗證並授予缺少的使用者角色](https://support.google.com/merchants/answer/1637190?hl=zh-tw)。

錯誤：`Historical backfills are not supported.`
:   **解決方法：**如果您[設定回填](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)前幾天的資料，就會收到這則錯誤訊息。這是預期中的錯誤。不支援歷來資料補充。您只能為今日設定補充作業，在排定的每日執行作業完成後重新整理今日資料。

## Google Play 轉移作業問題

以下是[建立 Google Play 移轉作業](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`No jobs to start for run`
:   **解決方法：**確認使用者具備[啟動 Google Play 移轉作業的足夠權限](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#required_permissions)，然後確認使用者在設定移轉作業時，是否指定正確的 Cloud Storage bucket。如果使用者仍遇到錯誤，可以[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

問題：收益和財務報表未載入 BigQuery
:   **解決方法：**使用者必須具備「`View financial data`」權限，才能存取 Google Play 財務報表。如要管理開發人員帳戶權限，請參閱「[新增開發人員帳戶使用者以及管理各項權限](https://support.google.com/googleplay/android-developer/answer/9844686?visit_id=638158652462486298-3898390440&%3Brd=1&hl=zh-tw)」。

## HubSpot 移轉問題

錯誤：`PERMISSION_DENIED: Permission denied. Your Access Token may lack required access to the provided account. Please also check for typos like whitespace or if the provided accountId even exists`
:   **解決方法：**確認私人應用程式存取權杖正確無誤、HubSpot 使用者具備**超級管理員**角色，且私人應用程式具備所有必要範圍。詳情請參閱「[HubSpot 必要條件](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw#hubspot-prerequisites)」。

錯誤：`INVALID_ARGUMENT: Table 'NAME' does not exist in asset "ASSET"`
:   **解決方法：**請確認指定的資產名稱有效，且開頭或結尾不含任何空格。[建立 HubSpot 移轉作業](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw#hubspot-transfer-setup)時，建議您按一下「Browse」(瀏覽)，從可用物件清單中選取資產。

錯誤：`FAILED_PRECONDITION: Rate limit exceeded.`
:   **解決方法：**已超過 HubSpot API 頻率限制。
    請稍候片刻，再重新嘗試轉移資料。您也可以考慮降低資料移轉工作的頻率，並限制類似帳戶同時移轉。

錯誤：`UNAUTHENTICATED: Authentication failed. Please verify your HubSpot access token.`
:   **解決方法：**確認私人應用程式存取權杖正確無誤。詳情請參閱「[HubSpot 必要條件](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw#hubspot-prerequisites)」。

錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認 HubSpot 私人應用程式存取權杖正確無誤，且您具備存取物件所需的權限，然後重試移轉工作。

## Klaviyo 移轉問題

[建立 Klaviyo 移轉作業](https://docs.cloud.google.com/bigquery/docs/klaviyo-transfer?hl=zh-tw)時，可能會遇到下列常見問題。

錯誤：`PERMISSION_DENIED: Permission denied. Your API key may lack required access scopes`
:   **解決方法：**確認 Klaviyo 非公開 API 金鑰至少具備`READ ONLY`存取層級。詳情請參閱「[Klaviyo 必要條件](https://docs.cloud.google.com/bigquery/docs/klaviyo-transfer?hl=zh-tw#klaviyo-prerequisites)」一節。

錯誤：`FAILED_PRECONDITION`
:   **解決方法：**縮短日期範圍，然後重新轉移。

錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認帳戶的 API 金鑰有效，然後重試移轉工作。

錯誤：`INTERNAL: An unknown error occurred while processing the request.`
:   **解決方法：**確認帳戶的 API 金鑰有效，然後重試移轉工作。

## Microsoft SQL Server 移轉作業問題

以下是[建立 Microsoft SQL Server 移轉作業](https://docs.cloud.google.com/bigquery/docs/sqlserver-transfer?hl=zh-tw)時可能遇到的常見問題。

錯誤：`FAILED PRECONDITION: A TLS/SSL handshake error occurred: unable to find valid certification path to requested target. Please check your TLS/SSL configuration and certificate validity.`
:   **解決方法：**請按照下列步驟驗證憑證是否有效：

    1. 將 SQL Server 上的 SSL/TLS 憑證，替換為由信任的 Public Certificate Authority 核發的憑證。詳情請參閱「[TLS 設定](https://docs.cloud.google.com/bigquery/docs/sqlserver-transfer-intro?hl=zh-tw#tls-configuration)」。
    2. 確認新憑證包含完整的憑證鏈結，包括所有中繼和根憑證。
    3. 更新憑證後，請重新啟動 SQL Server 服務，套用新的 SSL/TLS 設定。
    4. 伺服器重新啟動後，請再次建立移轉設定，確認更新後的憑證是否可信任，以及 TLS/SSL 握手是否成功完成。

錯誤：`INVALID_ARGUMENT: Catalog 'SCHEMA' does not exist in asset "SCHEMA/TABLE"`
:   **解決方法：**確認 SQL Server 中有目錄和資料表，且拼寫正確。此外，請確認使用者具備足夠的存取權限，可瀏覽或查詢目錄及其內容。

## Mailchimp 轉移問題

以下是[建立 Mailchimp 移轉作業](https://docs.cloud.google.com/bigquery/docs/mailchimp-transfer?hl=zh-tw)時可能遇到的常見問題。

錯誤：`INVALID_ARGUMENT: Invalid request. Please check the input parameters (Credentials, Table, etc.) and try again.`
:   **解決方法：**請確認指定的資產名稱有效，且開頭或結尾不含任何空格。[建立 Mailchimp 移轉作業](https://docs.cloud.google.com/bigquery/docs/mailchimp-transfer?hl=zh-tw)時，建議您按一下「Browse」(瀏覽)，從可用物件清單中選取資產。

錯誤：`PERMISSION_DENIED: Permission denied. Your credentials may lack required access.`
:   **解決方法：**確認 Mailchimp 使用者具備所有必要權限。Mailchimp 的 [`Admin` 使用者層級](https://mailchimp.com/help/manage-user-levels-in-your-account/)具備轉移所有 Mailchimp 物件的最低存取權。

錯誤：`FAILED_PRECONDITION: Operation failed due to precondition violation (ex- Rate limit exceeded, Server Error). Please try again later.`
:   **解決方法：**請稍候片刻，再重新嘗試轉移資料。您也可以查看 [Mailchimp 狀態](https://status.mailchimp.com/)，瞭解是否有任何服務中斷。

錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認 API 金鑰有效，且使用者具備所有必要權限，然後重試資料移轉工作。

## MySQL 移轉問題

以下是[建立 MySQL 移轉作業](https://docs.cloud.google.com/bigquery/docs/mysql-transfer?hl=zh-tw)時可能遇到的常見問題。

錯誤：`PERMISSION_DENIED. Failed to authenticate or permission denied with the provided credentials when starting to transfer asset asset-name.`
:   **解決方法：**請檢查您提供的 `connector.authentication.username` 和 `connector.authentication.password` 參數是否有效且可正常運作。

錯誤：`NOT_FOUND. Invalid data source configuration provided when starting to transfer asset asset-name: APPLICATION_ERROR;google.cloud.bigquery.federationv1alpha1/ConnectorService.StartQuery;INVALID_ARGUMENT:Exception was thrown by the Connector implementation: Table table-name does not exist in asset asset-name.`
:   **解決方法：**檢查資料表或檢視表名稱的拼寫是否正確、參照的資料表或檢視表名稱是否存在，以及同義詞 (別名) 是否指向現有的資料表或檢視表。

    如果資料表或檢視表存在，請確認已將正確的存取權限授予需要存取資料表的資料庫使用者。如果資料表或檢視表不存在，請建立資料表。

    如果您嘗試存取其他結構定義中的資料表或檢視表，請確認參照的結構定義正確無誤，且已授予物件存取權。

    如果提供資料表或檢視表名稱，請務必指定為 `object_name`，否則會留空。

錯誤：`SERVICE_UNAVAILABLE. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`

錯誤：`DEADLINE_EXCEEDED. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`
:   **解決方法：**請檢查提供的資料庫詳細資料是否正確，並確認移轉設定使用的網路連結設定正確。也可能是轉移作業未在期限內完成。

錯誤：`INTERNAL`
:   **解決方法：**轉移作業失敗的原因並非上述問題。
    請[聯絡 Cloud Customer Care](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw) 協助解決這個問題。

錯誤：`INVALID_ARGUMENT. Connection to the host and port failed. Please check that the host, port, encryptionMode and network attachment are correct.`
:   **解決方法：**確認主機、通訊埠、加密模式和聯播網設定皆正確無誤。請確認網路連線正常，且可存取資料庫伺服器。如果 `EncryptionMode` 設為 `FULL`，請確認伺服器支援必要通訊協定、具備有效憑證，且允許安全連線。如果 `EncryptionMode` 設為 `DISABLE`，請確認伺服器允許非 SSL 連線。查看應用程式和資料庫記錄，找出與連線或 SSL/TLS 相關的錯誤。

錯誤：`Failed to connect to MySQL instance INSTANCE_NAME. : Failed to connect to MySQL instance. Please ensure provided instance details are correct.`
:   **解決方法：**請確認移轉設定中的執行個體詳細資料正確無誤。執行個體詳細資料包括 MySQL 資料庫的名稱、主機名稱、IP 位址和通訊埠號碼等參數，或資料庫使用者的使用者名稱和密碼。

## Oracle 轉移作業問題

[建立 Oracle 移轉作業](https://docs.cloud.google.com/bigquery/docs/oracle-transfer?hl=zh-tw)時，可能會遇到下列常見問題。

錯誤：`PERMISSION_DENIED. ORA-01017: invalid username/password; logon denied`
:   **解決方法：**確認提供的 Oracle 憑證有效。

錯誤：`PERMISSION_DENIED. ORA-01045: user lacks CREATE SESSION privilege; logon denied`
:   **解決方法：**將 `CREATE SESSION` 系統權限授予 Oracle 使用者。如要進一步瞭解如何授予 Oracle 權限，請參閱 [`GRANT`](https://docs.oracle.com/cd/B13789_01/server.101/b10759/statements_9013.htm)。

錯誤：`SERVICE_UNAVAILABLE. ORA-12541: Cannot connect. No listener at host HOSTNAME port PORT` 或 `SERVICE_UNAVAILABLE. Connection failed: IO Error. The Network Adapter could not establish the connection`
:   **解決方法：**請確認提供的主機名稱和通訊埠詳細資料正確無誤，且網路連結設定正確。

錯誤：`NOT_FOUND. ORA-00942: table or view does not exist`
:   **解決方法：**請檢查下列各項：

* 資料表或檢視表名稱的拼寫正確。
* 參照的資料表或檢視表名稱已存在。
* 同義詞會指向現有的資料表或檢視表。如果資料表或檢視表確實存在，請確認已將正確的存取權限授予需要存取資料表的資料庫使用者。否則，請建立資料表。
* 如果嘗試存取其他結構定義中的資料表或檢視表，請確認參照的結構定義正確無誤，且已授予物件存取權。

錯誤：`NOT_FOUND. Schema schema does not exist.`
:   **解決方法：**指定的結構定義不存在。

錯誤：`DEADLINE_EXCEEDED`
:   **解決方法：**移轉作業未在六小時的時限內完成。將大型移轉作業拆分為多項小型作業，縮短移轉作業執行時間。

錯誤：`INTERNAL`
:   **解決方法：**轉移作業因其他原因失敗。
    [請與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，尋求協助解決這個問題。

錯誤：`INVALID_ARGUMENT`
:   **解決方法：**移轉設定中提供的值無效，導致移轉失敗。如要瞭解有效的移轉設定值，請參閱「[設定 Oracle 移轉作業](https://docs.cloud.google.com/bigquery/docs/oracle-transfer?hl=zh-tw#oracle-transfer-setup)」。

錯誤：`SQL Error [1950] [42000]: ORA-01950: no privileges on tablespace 'TablespaceName'`
:   **解決方法：**將預設資料表空間指派給使用者。詳情請參閱「[指派預設資料表空間](https://docs.oracle.com/cd/B19306_01/network.102/b14266/admusers.htm#i1006219)」。

錯誤：`403 PERMISSION_DENIED. Required 'compute.subnetworks.use' permission for project`
:   **解決方法：**如果網路連結與移轉設定位於不同專案，就可能發生這項錯誤。如要解決這個問題，您必須在網路連結所在的專案中，為服務帳戶 (例如 `service-customer_project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`) 授予下列權限：

    * `compute.networkAttachments.get`
    * `compute.networkAttachments.update`
    * `compute.subnetworks.use`
    * `compute.regionOperations.get`

    如果網路連結嘗試連線至位於不同專案的虛擬私有雲 (例如 Shared VPC)，也可能發生這項錯誤。在這種情況下，您必須將共用虛擬私有雲託管專案的 `compute.subnetworks.use` 權限，授予服務帳戶 (例如 `service-customer_project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`)。

## PayPal 轉帳問題

[建立 PayPal 轉帳](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw)時，可能會遇到下列常見問題。

錯誤：`PERMISSION_DENIED: Authorization failed due to insufficient permissions.`
:   **解決方法：**確認用戶端和用戶端密鑰具備[必要權限](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)，可存取要轉移的 PayPal 物件。

錯誤：`INVALID_ARGUMENT: Table 'OBJECT' does not exist in asset "OBJECT"`
:   **解決方法：**確認物件名稱有效。

錯誤：`INVALID_ARGUMENT: The given start date 'DATE' cannot be parsed. Please provide it in 'yyyy-MM-dd' format.`
:   **解決方法：**確認開始日期的語法正確。

錯誤：`UNAUTHENTICATED: Please provide a valid clientId and client secret.`
:   **解決方法：**確認用戶端 ID 和用戶端密鑰正確無誤。

錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認密鑰和帳戶 ID 有效，且所選物件具備[必要權限](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)，然後重試移轉工作。如果問題持續發生，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

錯誤：`INTERNAL: An unknown error occurred while processing the request.`
:   **解決方法：**確認密鑰和帳戶 ID 有效，且所選物件具備[必要權限](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)，然後重試移轉工作。如果問題持續發生，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## PostgreSQL 移轉作業問題

[建立 PostgreSQL 移轉作業](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw)時，可能會遇到下列常見問題。

錯誤：`PERMISSION_DENIED. Failed to authenticate or permission denied with the provided credentials when starting to transfer asset asset-name.`
:   **解決方法：**請檢查您提供的 `connector.authentication.username` 和 `connector.authentication.password` 參數是否有效且可正常運作。

錯誤：`NOT_FOUND. Invalid data source configuration provided when starting to transfer asset asset-name: APPLICATION_ERROR;google.cloud.bigquery.federationv1alpha1/ConnectorService.StartQuery;INVALID_ARGUMENT:Exception was thrown by the Connector implementation: Table table-name does not exist in asset asset-name.`
:   **解決方法：**檢查資料表或檢視表名稱的拼寫是否正確、參照的資料表或檢視表名稱是否存在，以及同義詞 (別名) 是否指向現有的資料表或檢視表。

    如果資料表或檢視表存在，請確認已將正確的存取權限授予需要存取資料表的資料庫使用者。如果資料表或檢視表不存在，請建立資料表。

    如果您嘗試存取其他結構定義中的資料表或檢視表，請確認參照的結構定義正確無誤，且已授予物件存取權。

    如果提供資料表或檢視表名稱，請務必指定為 `object_name`，否則會留空。

錯誤：`SERVICE_UNAVAILABLE. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`

錯誤：`DEADLINE_EXCEEDED. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`
:   **解決方法：**請檢查提供的資料庫詳細資料是否正確，並確認移轉設定使用的網路連結設定正確。也可能是轉移作業未在期限內完成。

錯誤：`INTERNAL`
:   **解決方法：**轉移作業失敗的原因並非上述問題。
    請[聯絡 Cloud Customer Care](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw) 協助解決這個問題。

錯誤：`INVALID_ARGUMENT. Connection to the host and port failed. Please check that the host, port, encryptionMode and network attachment are correct.`
:   **解決方法：**確認主機、通訊埠、加密模式和聯播網設定皆正確無誤。請確認網路連線正常，且可存取資料庫伺服器。如果 `EncryptionMode` 設為 `FULL`，請確認伺服器支援必要通訊協定、具備有效憑證，且允許安全連線。如果 `EncryptionMode` 設為 `DISABLE`，請確認伺服器允許非 SSL 連線。查看應用程式和資料庫記錄，找出與連線或 SSL/TLS 相關的錯誤。

錯誤：`INVALID_ARGUMENT: For Asset "postgres"."auth"."sessions", row count exceeds the max supported unIndexed read size of 2000000 records.`
:   **解決方法：**如果嘗試從 PostgreSQL 資料表轉移超過 2,000,000 筆記錄到 BigQuery 資料表，但 PostgreSQL 資料表中沒有主鍵或索引欄，就可能發生這項錯誤。如要解決這個問題，請在資料表中新增主鍵或索引資料欄。詳情請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw#limitations)」一節。

## Salesforce 轉移作業問題

以下是[建立 Salesforce 移轉作業](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`Permission Denied: invalid_client. invalid client credentials`
:   **解決方法：**確認提供的 ClientSecret 有效。

錯誤：`Permission Denied: invalid_client. client identifier invalid`
:   **解決方法：**確認提供的 ClientId 有效。

錯誤：`Permission Denied: Error encountered while establishing connection`
:   **解決方法：**檢查提供的 Salesforce MyDomain 名稱是否正確。

錯誤：`NOT_FOUND. asset type asset_name is not supported. If you are attempting to use a custom object, be sure to append the "__c" after the entity name. Please reference your WSDL or use the describe call for the appropriate names.`
:   **解決方法：**請按照錯誤代碼中的指引操作，並確認提供的素材資源名稱正確無誤。

錯誤：`SERVICE_UNAVAILABLE`
:   **解決方法：**服務暫時無法處理要求。請稍候幾分鐘，然後再試一次。

錯誤：`DEADLINE_EXCEEDED`
:   **解決方法：**移轉作業未在六小時的時限內完成。將大型移轉作業拆分為多個小型作業，盡可能縮短移轉作業執行時間。

錯誤：`Failed to create recordReader to read partition : Batch failed. BatchId='batch_id', Reason='FeatureNotEnabled : Binary field not supported'`
:   **解決方法：**連接器不支援含有二進位欄位的 sObject 資料結構。從移轉工作中移除含有二進位欄位的 sObject 資料結構。詳情請參閱 Salesforce 說明文件中的「[Error 'Batch failed: FeatureNotEnabled: Binary field not supported' when you export related object](https://help.salesforce.com/s/articleView?id=000382669&type=1)」(匯出相關物件時發生錯誤「Batch failed: FeatureNotEnabled: Binary field not supported」)。

錯誤：`RESOURCE_EXHAUSTED: PrepareQuery failed : ExceededQuota : ApiBatchItems Limit exceeded`
:   **解決方法：**如果工作執行的每日 `ApiBatchItems` API 限制超出上限，就會顯示這則錯誤訊息。Salesforce 設有每日 API 限制，每 24 小時重設一次。如要解決這項錯誤，建議您拆分並排定移轉作業，以免超過每日批次 API 限制。您也可以與 Salesforce 支援團隊聯絡，要求提高每日上限。

錯誤：`Permission Denied: invalid_grant. no client credentials user enabled`
:   **解決方法：**確認 Salesforce 連結應用程式的「Client Credentials Flow」(用戶端憑證流程) 部分中，「Run as」(執行身分) 欄位包含正確的使用者名稱。詳情請參閱「[建立 Salesforce 連結的應用程式](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#create-sf-app)」。

錯誤：`FAILED_PRECONDITION: BatchId='batch-id', Reason='InvalidBatch : Failed to process query: OPERATION_TOO_LARGE: exceeded 100000 distinct ids'`
:   **解決方法：**確認使用者設定檔未對擷取的 sObject 設下查詢限制。如果問題仍未解決，請使用具備系統管理員權限的 Salesforce 使用者憑證完成擷取作業。

錯誤：`FAILED_PRECONDITION: Batch failed. BatchId='batch-id', Reason='InvalidBatch : Failed to process query: TXN_SECURITY_NO_ACCESS: The operation you requested isn't allowed due to a security policy in your organization. Contact your administrator for more information about security policies.`
:   **解決方法：**請確認使用者的設定檔或權限集，包含擷取 sObject 所需的物件和欄位層級權限。請與管理員聯絡，要求更新這些權限，或指派具備必要存取權的角色。

錯誤：`FAILED_PRECONDITION: Cannot establish connection to Salesforce to describe SObject: 'SObject_Name' due to error: TotalRequests Limit exceeded., Cause:null Retry after some time post quota reset.`
:   **解決方法：**如果超過[載入工作的限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)，就可能發生這項錯誤。請等配額重設後再試。

錯誤：`FAILED_PRECONDITION: There was an issue connecting to Salesforce Bulk API.`
:   **解決方法：**如果轉移作業包含網路連結，但您未設定 Public NAT 和 IP 允許清單，就可能發生這個錯誤。如要解決這項錯誤，請完成「[為 Salesforce 移轉作業設定 IP 許可清單](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#salesforce-allowlist)」一文中的所有步驟。

錯誤：`SYSTEM ERROR when starting to transfer asset asset_name, try again later.`
:   **解決方法：**如果 Salesforce 組織未啟用 Bulk API，就可能發生這項錯誤。如要解決這項錯誤，請更新 Salesforce 授權，納入 Bulk API 支援。詳情請參閱「[啟用 Asynchronous API](https://help.salesforce.com/s/articleView?id=000386981&type=1)」。

## Shopify 轉移問題

錯誤：`[NOT_FOUND] Your app doesn't have a publication for this shop.`
:   **解決方法：**如果自訂應用程式的設定方式有問題，就可能發生這項錯誤。建議您按照下列步驟，解除安裝並重新安裝自訂應用程式。

    1. [解除安裝 Shopify 應用程式](https://help.shopify.com/en/manual/apps/uninstalling-apps)。
    2. [建立自訂應用程式](https://help.shopify.com/en/manual/apps/install-setup-apps#create-and-install-a-custom-app)，並採用下列設定。
       1. 建立應用程式時，請選取「Custom distribution」(自訂發行)。請提供商店網域或管理員網址。設定完成後，Shopify 會產生連結，供您完成應用程式安裝。詳情請參閱「[選取發布方式](https://shopify.dev/docs/apps/launch/distribution/select-distribution-method)」。
       2. 建立應用程式時，按一下「API access request」(API 存取要求)，然後選取「Enable storefront」(啟用店面)，並啟用 `read_all_orders` 範圍。
       3. 安裝自訂應用程式。
    3. 重新安裝自訂應用程式後，再次執行資料移轉作業。

錯誤：`PERMISSION_DENIED: Permission denied. Your API key may lack required access to the provided account. Please also check for typos like whitespace or if the provided accountId even exists`
:   **解決方法：**確認 Shopify Admin API 存取權杖正確無誤，且 Shopify 應用程式具備所有[必要存取角色](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw#shopify-prerequisites)。

錯誤：`INVALID_ARGUMENT: Table 'NAME' does not exist in asset "ASSET"`
:   **解決方法：**請確認指定的資產名稱有效，且開頭或結尾沒有任何空格。[建立 Shopify 移轉作業](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw#shopify-transfer-setup)時，建議您點選「Browse」(瀏覽)，從可用物件清單中選取資產。

錯誤：`UNAUTHENTICATED: Authentication failed. Please verify your Shopify access token.`
:   **解決方法：**請確認 Shopify Admin API 存取權杖正確無誤。詳情請參閱「[Shopify 必要條件](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw#shopify-prerequisites)」。

錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認 Shopify Admin API 存取權杖和商店名稱正確無誤，然後重試移轉工作。如果問題持續發生，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## Stripe 轉移問題

以下是[建立 Stripe 轉移作業](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`PERMISSION_DENIED: Permission denied. Your API key may lack required access to the provided account. Please also check for typos like whitespace or if the provided accountId even exists`
:   **解決方法：**如果您使用的是受限制的 API 金鑰，請確認該金鑰有權存取要轉移的 Stripe 物件。更新受限金鑰的權限後，請再次嘗試執行資料移轉作業。如要瞭解如何管理 Secret Key，請參閱「[Secret Key 和受限制的金鑰](https://docs.stripe.com/keys#secret-and-restricted-keys)」。

錯誤：`INVALID_ARGUMENT: Table 'NAME' does not exist in asset "ASSET"`
:   **解決方法：**確認指定的素材資源名稱有效，且開頭或結尾不含任何空格。[建立 Stripe 移轉作業](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw)時，建議您按一下「瀏覽」，從可用物件清單中選取資產。

錯誤：`UNAUTHENTICATED: Authentication failed. Please verify your Stripe API key.`
:   **解決方法：**確認密鑰和帳戶 ID 正確無誤。如要瞭解如何擷取這項資訊，請參閱「[Stripe 必要條件](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw#stripe-prerequisites)」。

錯誤：`RESOURCE_EXHAUSTED: Rate limit exceeded.`
:   **解決方法：**你可能超過 Stripe API 頻率限制。請稍候片刻，再重新嘗試資料移轉工作要求。為避免這個問題，建議您降低資料移轉工作的頻率，並限制從同一個帳戶並行移轉的數量。

錯誤：`UNAVAILABLE: Stripe service is temporarily unavailable. Please try again shortly.`
:   **解決方法：**請稍候片刻，再重新嘗試轉移資料。你可以查看 [Stripe 狀態](https://status.stripe.com/)，瞭解是否有任何服務中斷。

錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認密鑰和帳戶 ID 有效，且所選物件具備必要權限，然後重試移轉工作。如果問題仍未解決，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

錯誤：`INTERNAL: An unknown error occurred while processing the request.`
:   **解決方法：**確認密鑰和帳戶 ID 有效，且所選物件具備必要權限，然後重試移轉工作。如果問題仍未解決，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## ServiceNow 移轉作業問題

以下是[建立 ServiceNow 移轉作業](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw)時可能遇到的常見問題。

錯誤：`UNAUTHENTICATED. Required authentication credentials were not provided when starting to transfer asset asset-name.`
:   **解決方法：**確認提供的憑證 (`username`、`password`、`ClientID` 和 `Client Secret`) 有效、設定正確且未過期。

錯誤：`INVALID_ARGUMENT. Invalid datasource configuration provided when starting to transfer asset`

錯誤：`INVALID_ARGUMENT: Http call to ServiceNow instance returned status code 400.. Please make sure the instance/endpoint provided exists/is correct.`
:   **解決方法：**確認 ServiceNow 執行個體網址和 API 端點正確無誤，且參照的資料表存在，並可使用提供的憑證存取。

錯誤：`PERMISSION_DENIED. User credentials don't have permission or are invalid for accessing the ServiceNow asset or API.`
:   **解決方法：**確認提供的憑證正確無誤，且 ServiceNow 帳戶具備足夠權限，可存取指定資產或資料表。

錯誤：`UNAVAILABLE. ServiceNow instance is temporarily unreachable or experiencing downtime.`
:   **解決方法：**確認網路連線穩定，稍後再試。這項錯誤可能是 ServiceNow 暫時中斷或連線能力問題所致。

錯誤：`RESOURCE EXHAUSTED. ServiceNow API rate limit or quota has been exceeded, or operations are too large.`
:   **解決方法：**您已超過 ServiceNow API 配額或頻率限制。建議您減少要求數量或頻率，然後再試一次。

錯誤：`FAILED_PRECONDITION: There was an issue connecting to API.`
:   **解決方法：**如果轉移作業包含網路連結，但您未設定 Public NAT 和 IP 允許清單，就可能發生這個錯誤。如要解決這項錯誤，請定義靜態 IP 位址，[建立網路連結](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-tw#create-network-attachment)。

## Amazon Redshift 移轉問題

設定或執行 Amazon Redshift 移轉作業時，可能會遇到下列錯誤。

錯誤：`Cannot connect to Amazon Redshift cluster`或連線逾時
:   **解決方法：**請檢查下列各項：

    * 確認您已設定叢集的安全性群組規則，允許透過 TCP 在叢集使用的通訊埠 (預設為 `5439`) 傳入連線。詳情請參閱「[授予 Amazon Redshift 叢集的存取權](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw#grant_access_redshift_cluster)」。
    * 如果您是透過公開 IP 位址連線，請確認叢集可公開存取，且安全性群組規則允許從所有必要的 Google 遷移 IP 位址傳入連線。
    * 如果使用虛擬私有雲 (VPC) 連線，請確認虛擬私有雲和預留 IP 範圍未與任何子網路重疊、自訂路徑已 advertise，且虛擬私有雲對等互連連線處於啟用狀態。
    * 確認 JDBC 連線網址格式正確 (`jdbc:postgresql://endpoint-host:port/database-name`)。

錯誤：連結 Amazon Redshift 時發生 `Authentication failure: User Id not found` 或 `PERMISSION_DENIED`
:   **解決方法：**確認**資料庫使用者名稱**和**資料庫密碼**值屬於具備目標 Amazon Redshift 結構定義和資料表 `SELECT` 權限的資料庫使用者。此外，請確認 AWS **存取金鑰 ID** 和**私密存取金鑰**值對應的 IAM 實體有權從 Amazon Redshift `UNLOAD`資料，並將暫存檔案寫入 Amazon S3 暫存 bucket。

錯誤：存取 Amazon S3 暫存 bucket 時發生 `AccessDenied` 錯誤
:   **解決方法：**確認提供的 AWS 存取金鑰組對應至 IAM 使用者或角色，且該使用者或角色對 Amazon S3 暫存值區 (`s3://bucket-name/prefix`) 具有讀取和寫入權限 (`PutObject`、`GetObject`、`ListBucket` 和 `DeleteObject`)，以便 BigQuery 資料移轉服務將檔案移轉至 BigQuery。

錯誤：CSV 匯入失敗，因為含有 ASCII 0 (`NUL`) 字元
:   **解決方法：**如果 BigQuery 資料移轉服務將 Amazon Redshift 資料表匯出為含有 ASCII 0 字元 (`\0`) 的 CSV 檔案，則無法將這些檔案載入 BigQuery。如要解決這個問題，請改為將資料匯出至 Amazon S3，並儲存為 Parquet 檔案。詳情請參閱「[評估資料](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw#assess_your_data)」。

## Teradata 移轉問題

以下是建立 Teradata 移轉作業時可能遇到的常見問題。

錯誤：`Skipping extraction since table does not have change tracking column.`
:   **解決方法：**如果您嘗試使用現有的隨選移轉設定，對已遷移的資料表執行 Teradata 移轉作業，就可能看到上述訊息。如要對已遷移的資料表啟動新的移轉作業，請[建立新的移轉設定](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw#set_up_a_transfer)，並套用「On-demand」(隨選) 設定。

    使用隨選移轉設定重複移轉時，BigQuery 資料移轉服務會嘗試以增量移轉方式執行，但由於移轉設定未套用正確的增量設定，因此會略過資料表。如要進一步瞭解不同類型的移轉作業，請參閱「[隨選或增量移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#incremental)」。

問題：轉移 `CHAR`(N) 資料類型時，系統會為較短的字串加上空格，直到字元數達到 N。
:   **解決方法：**將 `CHAR` 資料轉換為 `VARCHAR`，並移除來源中的多餘空格。發生這個問題的原因是 [`CHAR` 是固定長度字串](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Types-and-Literals/June-2017/Character-and-CLOB-Data-Types/Character-Data)，而 [`VARCHAR` 應使用於可變長度字串](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Types-and-Literals/June-2017/Character-and-CLOB-Data-Types/VARCHAR-Data-Type)。您也可以在遷移後，使用 [`RTRIM` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#rtrim)移除 BigQuery 中的空格。使用 `RTRIM` 函式的查詢大致如下：

    ```
    UPDATE migrated_table
    SET migrated_char_column = RTRIM(migrated_char_column)
    WHERE true;
    ```

## YouTube 移轉問題

以下是[建立 YouTube 移轉作業](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw)時常見的錯誤。

錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`

錯誤：`No data available for requested date. Please try an earlier run date or verify that data existence was expected.`
:   **解決方法：**如果您先前未建立 YouTube [報表工作](https://developers.google.com/youtube/reporting/v1/reports/?hl=zh-tw#step-3-create-a-reporting-job)，請至少等待 2 天，讓 YouTube 透過 BigQuery 資料移轉服務為您產生報表。您不必採取其他動作。
    前 2 天的轉移作業會失敗，第 3 天應該會成功。如果您之前建立過 YouTube 報告工作，請確認建立移轉作業的使用者具備報告的讀取權。
:   另請確認是否使用正確的帳戶設定移轉作業。在 OAuth 對話方塊中，選取要載入資料的頻道。

錯誤：`No reports for reporting job with name name.`
:   **解決方法：**這並不是錯誤。這是一則警告訊息，表示系統找不到指定報告的資料。您可以忽略這則警告。未來的移轉作業仍會繼續執行。

**注意：** YouTube 內容管理員每月只能取得特定檔案一次。其他時間這些每月報告會顯示為「遺漏」。這是預期的行為。您無須採取任何行動，如果報表不應遺失，請透過[說明論壇](https://productforums.google.com/forum/?hl=zh-tw#!forum/youtube)與 YouTube 支援團隊聯絡。

問題：移轉作業建立的結果資料表不完整，或結果不如預期。
:   **解決方法：**如果您有多個帳戶，請務必在 YouTube 權限對話方塊中選擇正確的帳戶。

問題：YouTube 數據分析和 BigQuery YouTube 移轉作業的資料不一致。
:   **背景：**BigQuery YouTube 移轉作業會使用 [YouTube Reporting API](https://developers.google.com/youtube/reporting/v1/reports?hl=zh-tw)，將資料直接擷取至 BigQuery 資料集。另一方面，YouTube 數據分析資訊主頁則使用 [YouTube Analytics API](https://developers.google.com/youtube/analytics/reference?hl=zh-tw) 提取資料。YouTube 透過 Reporting API 產生的數據應視為最終數據，而 YouTube 數據分析資訊主頁/API 中顯示的數據則應視為預估數據。兩個 API 之間出現一定程度的差異，這是正常可預期的現象。
:   **解決方法：**如果回報的數字確實不正確，YouTube 系統和 BigQuery 資料移轉服務 YouTube 移轉作業都會設定為回填缺少的數字，並在為回填日期新產生的報表中提供這些數字。BigQuery 資料移轉服務 YouTube 設定會載入 YouTube Reporting API 建立的所有可用報表，因此當 BigQuery 移轉作業自動匯入日後產生的 YouTube 報表時，也會考量新產生和更新的資料，並將其擷取至正確的日期分區資料表。

    **注意：** YouTube 數據分析會在當天結束後 24 到 48 小時內 (有時更久)，提供當天的 YouTube 資料。因此，後續產生的 YouTube 報表和 BigQuery 移轉作業也會遵循這項延遲。

### YouTube 權限問題

如要轉移 YouTube 內容管理工具報表，設定轉移作業的使用者至少須具備 `CMS user` 權限。您必須為每位要建立移轉作業的內容管理員授予 `CMS user` 權限。

## 配額問題

錯誤：`Quota exceeded: Your project exceeded quota for imports per project.`
:   **解決方法：**確認專案中未排定過多轉入作業。如要瞭解如何計算移轉作業啟動的載入工作數量，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

錯誤：`RESOURCE_EXHAUSTED: Rate limit exceeded.` (或從 ServiceNow、Facebook Ads、Confluence 或 PayPal 等第三方應用程式移轉資料時，發生類似的頻率限制錯誤)
:   **解決方法：**使用 BigQuery 資料移轉服務從第三方應用程式擷取資料時，頻率限制錯誤可能是因為外部來源應用程式限制資料擷取，而非 BigQuery 擷取限制。如要解決這項錯誤，請執行下列操作：

    * **確認錯誤來源：**檢查移轉作業執行記錄。如果錯誤訊息提及外部連接器或第三方資料來源，則表示頻率限制是由外部平台強制執行。
    * **檢查第三方平台的 API 頻率限制：**登入外部平台，查看 API 用量和頻率限制 (例如將 Facebook 廣告應用程式升級至進階存取權，或查看 ServiceNow 的傳入 REST API 頻率限制)，並確保沒有平行工作流程共用相同憑證。
    * **降低移轉頻率或錯開排程：**修改移轉設定排程，降低執行頻率，並避免同時對同一個外部帳戶執行平行移轉。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]