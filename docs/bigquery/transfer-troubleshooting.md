* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解移轉設定問題

本文旨在協助您排解設定 BigQuery 資料移轉服務移轉作業時最常發生的問題。但不會列出所有可能出現的錯誤訊息或問題。

如果您遇到本文未說明的問題，可以[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

與 Cloud Customer Care 聯絡前，請先擷取移轉設定和移轉執行詳細資料。如要瞭解如何取得這些詳細資料，請參閱「[取得移轉詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#get_transfer_details)」和「[查看移轉執行作業的詳細資料與記錄訊息](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_details_and_log_messages)」。

## 檢查錯誤

如果初始移轉作業失敗，您可以查看[執行記錄](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_history)中的詳細資料。
您可參考執行記錄中列出的錯誤，並使用這份文件找出適當的解決方法。

您也可以使用 [Logs Explorer](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw) 查看特定傳輸工作的錯誤訊息。
下列 Logs Explorer 篩選器會傳回特定移轉設定工作的相關資訊，以及任何錯誤訊息：

```
resource.type="bigquery_dts_config"
labels.run_id="RUN_ID"
resource.labels.config_id="CONFIG_ID"
```

更改下列內容：

* `RUN_ID`：特定工作執行的 ID 編號
* `CONFIG_ID`：轉移設定工作的 ID 號碼

聯絡客戶服務前，請先從執行記錄或 Logs Explorer 擷取相關資訊，包括任何錯誤訊息。

如果您使用[以事件為依據的移轉作業](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw)，以事件為依據的移轉設定可能無法觸發移轉作業。您可以在[執行記錄](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_history)頁面或[設定](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#get_transfer_details)頁面頂端查看錯誤訊息。

## 一般問題

診斷一般移轉問題時，請確認下列事項：

* 針對移轉類型適用的說明文件頁面，確認是否已完成其中「事前準備」一節所述的所有步驟。
* 移轉設定屬性是否正確。
* 建立移轉作業所使用的使用者帳戶是否擁有基礎資源的存取權。

如果移轉設定正確，且取得適當權限，請參閱下列常見問題的解決方案。

發生錯誤：`An unexpected issue was encountered. If this issue persists, please contact customer support.`
:   **解決方法：**這個錯誤通常表示 BigQuery 暫時中斷服務或發生問題。請等待約 2 小時以解決問題。如果問題仍未解決，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`INTERNAL: An internal error occurred and the request could not be completed. This is usually caused by a transient issue...`
:   **解決方法：**這類錯誤通常表示發生暫時性內部問題。如果發生這個錯誤，您可以等待下一次排定的執行作業，看看問題是否解決，也可以[手動觸發受影響日期的補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。如果問題仍未解決，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`Quota Exceeded.`
:   **解決方法：**移轉作業必須符合 BigQuery 的[載入工作配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)規定。如要提高配額，請與 Google Cloud 業務代表聯絡。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

    如果您將 Cloud Billing 匯出資料載入至 BigQuery，可能會遇到 `Quota Exceeded` 錯誤。Cloud Billing 匯出資料表和 BigQuery 資料移轉服務建立的目的地 BigQuery 資料表都會經過分割。設定這類 BigQuery 資料移轉服務工作時，如果選擇「覆寫」選項，系統會根據匯出的資料量，顯示配額錯誤。如要瞭解如何排解配額問題，請參閱「[解決配額與限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。

    如果錯誤是因 Cloud Billing 匯出作業的 BigQuery 資料移轉服務工作所致，請注意，由於個別的 Cloud Billing 匯出資料表已分割，BigQuery 資料移轉服務建立的目標資料表也會分割，因此設定這類資料移轉工作時選擇「覆寫」選項，會導致 (DML) 配額錯誤，具體情況取決於帳單帳戶的建立時間。如要瞭解如何排解配額問題，請參閱「[排解配額和限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。

發生錯誤：`The caller does not have permission.`
:   **解決方法：**確認 Google Cloud 控制台中登入的帳戶，與您建立轉移作業時為 BigQuery 資料移轉服務 選取的帳戶相同。

    * 登入 Google Cloud 控制台的帳戶：
    * 選擇帳戶，繼續使用 BigQuery 資料移轉服務：

發生錯誤：`Access Denied: ... Permission bigquery.tables.get denied on table ...`
:   **解決方法：**確認 BigQuery 資料移轉服務[服務代理程式](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)已取得目標資料集的[`bigquery.dataEditor`角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)。建立及更新轉移作業時，系統會自動套用這項授權，但存取權政策可能隨後經過手動修改。如要重新授予權限，請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」一文。

發生錯誤：`region violates constraint constraints/gcp.resourceLocations on the resource projects/project_id`
:   **解決方法：**如果使用者嘗試在[位置限制機構政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw)中指定的受限位置建立移轉設定，就會發生這個錯誤。如要解決這個問題，請[變更機構政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw#setting_the_organization_policy)，允許使用該區域，或是將移轉設定變更為位於機構政策未限制區域的目的地資料集。

發生錯誤：`Please look into the errors[] collection for more details.`
:   **解決方法：**如果資料移轉失敗，就可能會發生這種錯誤。如要進一步瞭解資料移轉失敗的原因，請[使用 Cloud Logging 查看記錄](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw#logs)。您可以[搜尋特定執行作業的記錄](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw#view_transfer_run_logs)，方法是使用轉移 `run_id` 搜尋。

發生錯誤：`Network Attachment with connected endpoints cannot be deleted.`
:   **解決方法：**如果使用者在[刪除轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#delete_a_transfer)後不久，就嘗試刪除網路附件，就可能發生這個錯誤。這是因為刪除移轉後，BigQuery 資料移轉服務可能需要幾天時間，才能完全移除與移轉相關聯的所有資源，因此無法刪除網路附件。如要解決這項錯誤，請等待幾天，再嘗試刪除網路附件。如要提早刪除網路附件，請[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`Error while reading data, error message: CSV processing encountered too many errors, giving up.`
:   **解決方法：**如果資料來源中的 CSV 檔案設定與轉移設定中的 CSV 檔案設定不符，就可能發生這個錯誤。舉例來說，如果「要略過的標題列」設為 `0`，但來源 CSV 檔案包含 1 個以上的標題列，就可能發生這個錯誤。如要修正這項錯誤，請確認轉移設定中的 CSV 設定正確無誤，且與來源 CSV 檔案的設定相符。

發生錯誤：`Error 400: DTS service agent needs iam.serviceAccounts.getAccessToken permission or [SERVICE_ACCOUNT] doesn't exist.`
:   **根本原因：**這項錯誤表示 BigQuery 資料移轉服務 (DTS) 服務代理缺少必要權限，無法模擬用於移轉作業的服務帳戶。這通常發生在跨專案授權情境，或是使用 Terraform 等基礎架構即程式碼 (IaC) 工具設定轉移時。
:   **解決方法：**將服務帳戶權杖建立者角色 (`roles/iam.serviceAccountTokenCreator`) 授予 DTS 服務代理，讓該代理模擬特定服務帳戶。

    ```
    gcloud iam service-accounts add-iam-policy-binding service_account \
    --member serviceAccount:service-destination_project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
    --role roles/iam.serviceAccountTokenCreator
    ```

    其中：

* service\_account 是用來授權轉移作業的帳戶電子郵件地址。
* destination\_project\_number 是移轉設定所在的專案編號。如要瞭解如何找出專案編號，請參閱「[識別專案](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw#identifying_projects)」。

發生錯誤：`For asset "ASSET", no eligible column found for splitting (Reason: Primary or Indexed Key columns found, but none are of supported types (INTEGER, TINYINT, SMALLINT, FLOAT, REAL, DOUBLE, NUMERIC, BIGINT, DECIMAL, DATE, BOOLEAN))`
:   **解決方法：**嘗試將超過 2,000,000 筆記錄從來源資料表移轉至 BigQuery 資料表時，如果來源資料表沒有主鍵或支援資料類型的索引資料欄，就可能發生這個錯誤。如要解決這個問題，請在來源資料表中，將支援的資料類型設為其中一個資料欄的主鍵或索引資料欄。詳情請參閱移轉來源指南的限制一節。

發生錯誤：`Permission bigquery.tables.create denied.`
:   **症狀：**

    ```
    Error code 7 : Access Denied : Dataset [PROJECT_ID]:[DATASET_ID] : Permission bigquery.tables.create denied on dataset [PROJECT_ID]:[DATASET_ID] (or it may not exist).
    ```

    即使目的地資料表已存在，且服務帳戶具備標準資料編輯者角色，Cloud Storage 移轉作業仍會因資料表建立作業遭拒存取而失敗。
:   **原因：**如果 Cloud Storage 轉移作業包含超過 10,000 個檔案，且未授予 `bigquery.tables.create` 權限，就會發生這個錯誤。如果移轉的檔案超過 10,000 個，服務會將資料分片到動態建立的暫時暫存資料表。即使專案已註冊大量移轉功能 (或配額增加要求已獲准)，仍須具備 bigquery.tables.create 權限。
:   **解決方法：**如要成功移轉超過 10,000 個檔案，請確認你符合下列兩項條件：

1. **確認配額和功能註冊：**確認專案已註冊大量 Cloud Storage 轉移 (超過 10,000 個檔案)。如要轉移超過 10,000 個檔案，請[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，要求增加每次轉移作業的檔案數量上限。
2. **授予必要 IAM 權限：**將目的地資料集上的 `bigquery.tables.create` 權限，授予執行轉移作業的服務帳戶或使用者身分。這項權限包含在 BigQuery 資料編輯者 (`roles/bigquery.dataEditor`) 和 BigQuery 管理員 (`roles/bigquery.admin`) 角色中。如果授予必要權限後仍持續發生失敗情況，請[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，確認允許清單狀態。

   **替代做法：**如果無法授予必要權限或提高配額，您必須將每次轉移作業的檔案數量減少至 10,000 個以下，例如使用更具體的 URI 萬用字元，或將轉移作業分成多個較小的設定。

## 授權和權限問題

以下是從不同資料來源轉移資料時，可能會遇到的一些常見權限錯誤：

發生錯誤：`BigQuery Data Transfer Service is not enabled for <project_id>`

發生錯誤：`BigQuery Data Transfer Service has not been used in project <project_id> before or it is disabled ...`
:   **解決方法：**
    請按照下列步驟，確認服務代理角色已獲授權：

    1. 前往 Google Cloud 控制台的「IAM & Admin」(IAM 與管理) 頁面。

       [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
    2. 選取「包含  **Google提供的角色授予項目**」核取方塊。
    3. 確認系統顯示名稱為 `service-<project_number>@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com` 的服務帳戶，或該帳戶已獲授與 [BigQuery 資料移轉服務代理程式角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)。

    如果未顯示服務帳戶，或服務帳戶未獲授與 BigQuery 資料移轉服務代理人角色，請在 Google Cloud 主控台中授予預先定義的角色，或執行下列 Google Cloud CLI 指令：

    ```
    gcloud projects add-iam-policy-binding PROJECT_NUMBER \
    --member serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
    --role roles/bigquerydatatransfer.serviceAgent
    ```

    將 `PROJECT_NUMBER` 替換為與這個服務帳戶相關聯的專案編號。

發生錯誤：`There was an error loading this table. Check that the table exists and that you have the correct permissions.`
:   **解決方法：**

    1. 前往 Google Cloud 控制台的「BigQuery」頁面。

       [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
    2. 按一下轉移作業中使用的目的地資料集。
    3. 按一下「共用」選單，然後點選「權限」。
    4. 展開「BigQuery 資料編輯者」角色。
    5. 確認 BigQuery 資料移轉服務服務代理人已新增至這個角色。如果沒有，請將 BigQuery 資料編輯者 (`roles/bigquery.dataEditor`) 角色授予 BigQuery 資料移轉服務服務代理人。

發生錯誤：`A permission denied error was encountered: PERMISSION_DENIED. Please ensure that the user account setting up the transfer config has the necessary permissions, and that the configuration settings are correct`
:   **解決方法：**

    1. 前往 Google Cloud 控制台的「資料移轉」頁面。

       [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
    2. 按一下失敗的轉移作業，然後選取「設定」分頁標籤。
    3. 確認「使用者」欄位中列出的轉移擁有者具備資料來源的所有必要權限。

    如果移轉擁有者沒有所有必要權限，請[更新憑證](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_credentials)，授予必要權限。您也可以將轉移擁有者變更為其他具備必要權限的使用者。

發生錯誤：`Authentication failure: User Id not found. Error code: INVALID_USERID`
:   **解決方法：**移轉擁有者具有無效的使用者 ID。如要將轉移作業擁有者變更為其他使用者，請[更新他們的憑證](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_credentials)。如果您使用服務帳戶，也請確認執行資料移轉作業的帳戶具備[使用服務帳戶的所有必要權限](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw#required_permissions)。

發生錯誤：`The user does not have permission`
:   **解決方法：**確認轉移擁有者是服務帳戶，且服務已設定所有必要權限。另一種可能性是，使用的服務帳戶是在其他專案下建立，而非用於建立這項轉移作業的專案。如要解決跨專案權限問題，請參閱下列資源：

    * [啟用服務帳戶，以便跨專案附加](https://docs.cloud.google.com/iam/docs/attach-service-accounts?hl=zh-tw#enabling-cross-project)
    * [跨專案服務帳戶授權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#cross-project_service_account_authorization) (用於授予必要權限)

發生錯誤：`HttpError 403 when requesting returned "The caller does not have permission"`
:   `googleapiclient.errors.HttpError: <HttpError 403 when requesting returned "The caller does not have permission". Details: "The caller does not have permission">`
:   嘗試使用服務帳戶設定排程查詢時，可能會出現這則錯誤訊息。
:   **解決方法：**確認服務帳戶具備[排程或修改排程查詢所需的所有權限](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#required_permissions)，並確認設定排程查詢的使用者[有權存取服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw#service-account-permissions)。

    如果已指派所有正確權限，但仍發生錯誤，請檢查專案是否預設強制執行「停用跨專案服務帳戶」政策。如要查看政策，請前往 Google Cloud 控制台，依序選取「IAM 與管理」>「機構政策」，然後搜尋政策。

    如果強制執行「停用跨專案服務帳戶」政策，請按照下列步驟停用該政策：

    1. 使用 Google Cloud 控制台找出與專案相關聯的服務帳戶，方法是依序前往「IAM & Admin」(IAM 與管理) >「Service Accounts」(服務帳戶)。這個檢視畫面會顯示目前專案的所有服務帳戶。
    2. 在服務帳戶所在的專案中，使用下列指令停用政策。如要停用這項政策，使用者必須是[機構政策管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/orgpolicy?hl=zh-tw#orgpolicy.policyAdmin)。只有機構管理員可以授予使用者這個角色。

    ```
    gcloud resource-manager org-policies disable-enforce iam.disableCrossProjectServiceAccountUsage --project=[PROJECT-ID]
    ```

## 事件導向移轉設定問題

以下是建立事件驅動型移轉作業時可能遇到的常見問題。

發生錯誤：`Data Transfer Service is not authorized to pull message from the provided Pub/Sub subscription.`
:   **解決方法：**確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)已獲授 [`pubsub.subscriber` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber)：

    1. 前往 Google Cloud 控制台的「Pub/Sub」頁面。

       [前往 Pub/Sub](https://console.cloud.google.com/cloudpubsub/subscription/list?hl=zh-tw)
    2. 選取您在以事件為依據的移轉作業中使用的 Pub/Sub 訂閱項目。
    3. 如果資訊面板已隱藏，請按一下右上角的「顯示資訊面板」。
    4. 在「權限」分頁中，確認 BigQuery 資料移轉服務[服務代理程式](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)具有 [`pubsub.subscriber` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.subscriber)。
:   如果服務代理未獲授 `pubsub.subscriber` 角色，按一下「新增主體」person\_add，將 `pubsub.subscriber` 角色授予 `service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`

發生錯誤：`Cloud Pub/Sub API has not been used in project PROJECT_NUMBER before or it is disabled.`
:   **解決方法：**確認專案已啟用 Cloud Pub/Sub API：

    1. 在 Google Cloud 控制台中，前往「APIs & Services」(API 與服務) 頁面。

       [前往「API 與服務」頁面](https://console.cloud.google.com/apis/dashboard?hl=zh-tw)
    2. 按一下「啟用 API 和服務」。
    3. 搜尋「`Cloud Pub/Sub API`」，選取第一個結果，然後按一下「啟用」。

發生錯誤：`Data Transfer Service does not have required permission to use project quota of project PROJECT_NUMBER to access Pub/Sub.`
:   **解決方法：**確認 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)已獲授 [`serviceusage.serviceUsageConsumer` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)：

    1. 前往 Google Cloud 控制台的「IAM & Admin」(IAM 與管理) 頁面。

       [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
    2. 選取「包含  **Google提供的角色授予項目**」核取方塊。
    3. 確認系統顯示名稱為 `service-<project_number>@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com` 的服務帳戶，且該帳戶已獲授[服務用量消費者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)。

問題：使用 Cloud Storage 事件驅動的移轉作業時，在 Cloud Storage bucket 中上傳或更新檔案後，系統不會觸發任何移轉作業。
:   收到事件後，系統不會立即觸發轉移作業。觸發轉移作業可能需要幾分鐘。如要查看下次轉移作業的狀態，請查看[執行記錄](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#view_transfer_run_history)中的「下次執行目標日期」欄位。這個欄位會顯示下次執行的排定時間，如果沒有收到任何事件，則會顯示「正在等待事件，以便排定下一項執行作業」。如果您已在 Cloud Storage bucket 中上傳或更新檔案，但「下次執行的目標日期」未更新，且系統在 10 到 20 分鐘內未觸發任何執行作業，請參閱下列解決方法。
:   **解決方法：**確認移轉設定中指定的 Pub/Sub 訂閱項目是否能接收 Cloud Storage 事件發布的訊息：

    1. 前往 Google Cloud 控制台的「Pub/Sub」頁面。

       [前往 Pub/Sub](https://console.cloud.google.com/cloudpubsub/subscription/list?hl=zh-tw)
    2. 選取您在以事件為依據的移轉作業中使用的 Pub/Sub 訂閱項目。
    3. 在「指標」分頁中，查看「最舊的未確認訊息存在時間」圖表，確認是否有任何訊息。
:   如果沒有發布任何訊息，請檢查 Cloud Storage 的 Pub/Sub 通知是否已正確設定。您可以使用下列 Google Cloud CLI 指令，檢查與值區相關聯的通知設定：

    ```
    gcloud storage buckets notifications list gs://BUCKET_NAME
    ```

    將 `BUCKET_NAME` 替換為您用於通知的值區名稱。如要瞭解如何設定 Cloud Storage 的 Pub/Sub 通知，請參閱「[設定 Cloud Storage 的 Pub/Sub 通知](https://docs.cloud.google.com/storage/docs/reporting-changes?hl=zh-tw)」。
:   如有訊息，請檢查其他事件驅動的轉移設定是否使用相同的 Pub/Sub 訂閱項目。多個事件驅動的轉移設定無法重複使用同一個 Pub/Sub 訂閱項目。如要進一步瞭解事件導向移轉作業，請參閱「[事件導向移轉作業](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw)」。

## Amazon S3 移轉問題

以下是[建立 Amazon S3 移轉作業](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw)時的常見錯誤。

### Amazon S3 `PERMISSION_DENIED` 錯誤

發生錯誤：`The AWS Access Key Id you provided does not exist in our records.`
:   **解決方法：**確認存取金鑰存在且 ID 正確無誤。

發生錯誤：`The request signature we calculated does not match the signature you provided. Check your key and signing method.`
:   **解決方法：**確認移轉設定是否具有正確的對應私密存取金鑰

發生錯誤：`Failed to obtain the location of the source S3 bucket. Additional details: Access Denied`

發生錯誤：`Failed to obtain the location of the source S3 bucket. Additional details: HTTP/1.1 403 Forbidden`

錯誤：`Access Denied` (S3 錯誤訊息)
:   **解決方法：**確認 AWS IAM 使用者有權執行下列操作：

    * 列出 Amazon S3 值區。
    * 取得值區的位置。
    * 讀取值區中的物件。

發生錯誤：`Server unable to initialize object upload.; InvalidObjectState: The operation is not valid for the object's storage class`

發生錯誤：`Failed to obtain the location of the source S3 bucket. Additional details: All access to this object has been disabled`
:   **解決方法：**將任何封存於 Amazon Glacier 的物件還原。在 Amazon S3 中，封存於 Amazon Glacier 的物件在還原之前都無法存取

發生錯誤：`All access to this object has been disabled`
:   **解決方法：**確認轉移設定中的 Amazon S3 URI 正確無誤

### Amazon S3 移轉限制錯誤

發生錯誤：`Number of files in transfer exceeds limit of 10,000.`
:   **解決方法：**評估是否能將 Amazon S3 URI 中的[萬用字元](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#wildcard-support)數量減少為一個。如果可以，請使用新的轉移設定重試，因為[每次轉移作業的檔案數量上限會提高](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#quotas_and_limits)。
    您也可以評估是否能將移轉設定拆分成多個移轉設定，每個設定移轉一部分的來源資料。

發生錯誤：`Size of files in transfer exceeds limit of 16492674416640 bytes.`
:   **解決方法：**評估是否可將轉移設定拆分成多個轉移設定，每個設定轉移一部分來源資料。

### 一般 Amazon S3 問題

問題：檔案已從 Amazon S3 移轉，但未載入至 BigQuery。
:   轉移記錄可能如下所示：`Moving data from Amazon S3 to Google Cloud complete: Moved N object(s).
    No new files found matching Amazon_S3_URI.`
:   **解決方法：**確認轉移設定中的 Amazon S3 URI 正確無誤。如果移轉設定是要載入所有含有相同前置字串的檔案，請確認 Amazon S3 URI 結尾是萬用字元。舉例來說，如要載入 `s3://my-bucket/my-folder/` 中的所有檔案，移轉設定中的 Amazon S3 URI 必須是 `s3://my-bucket/my-folder/*`，而不只是 `s3://my-bucket/my-folder/`。

## Azure Blob 儲存體移轉問題

以下是[建立 Blob Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`Number of files in transfer exceeds the limit of 10,000.`
:   **解決方法：**將 Blob 儲存空間資料路徑中的[萬用字元](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#wildcard-support)數量減少至 0 或 1，檔案上限就會增加至 10,000,000 個。您也可以將來源分割成多個轉移設定，每個設定轉移一部分來源。

發生錯誤：`Size of files in transfer exceeds the limit of 15 TB.`
:   **解決方法：**分成多個移轉設定，每個設定移轉一部分來源資料。

發生錯誤：`Provided Azure SAS Token does not have required permissions.`
:   **解決方法：**確認移轉設定中的 Azure SAS 權杖正確無誤。詳情請參閱「[共用存取簽章 (SAS)](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#shared-access-signature)」。

發生錯誤：`Transfer encountered error, status:PERMISSION_DENIED, details:[This request is not authorized to perform this operation.]`
:   **解決方法：**確認 BigQuery 資料移轉服務工作站使用的 IP 範圍已加入允許的 IP 清單。詳情請參閱「[IP 限制](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#ip_restrictions)」一文。

問題：檔案已從 Blob 儲存空間轉移，但未載入 BigQuery。
:   轉移記錄可能類似以下內容：`Moving data to Google Cloud complete: Moved
    <var>N</var> object(s). No new files found matching Blob Storage data path.`
:   **解決方法：**確認轉移設定中的 Blob 儲存空間資料路徑正確無誤。

## Campaign Manager 移轉問題

以下是[建立 Campaign Manager 移轉作業](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`

發生錯誤：`No data available for the requested date. Please try an earlier run date or verify that data existence was expected.`
:   **解決方法：**確認是否使用[正確的 ID](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw#set_up_a_campaign_manager_transfer) 來執行移轉作業。如果您使用的 ID 正確無誤，請確認 Campaign Manager Cloud Storage 值區是否含有指定日期範圍內的 Data Transfer 2.0 版檔案。如果檔案存在，請排定受影響日期範圍內的補充作業。如要進一步瞭解如何建立 Campaign Manager 補充作業要求，請參閱「[手動觸發轉移或補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer_or_backfill)」。
:   您可以查看 Cloud Storage bucket 中檔案的建立時間，確認檔案在排定轉移作業時是否存在。在某些情況下，系統可能會在產生第一批 Campaign Manager 資料移轉檔案之前，排定當天的第一次移轉作業。當天和隔天後續的執行作業會載入 Campaign Manager 產生的所有檔案。

發生錯誤：`A permission denied error was encountered: PERMISSION_DENIED. Please ensure that the user account setting up the transfer config has the necessary permissions, and that the configuration settings are correct.`
:   **解決方法：**建立 Campaign Manager 移轉作業的使用者，必須能夠讀取內含資料移轉 2.0 版檔案的 [Cloud Storage 值區](https://console.cloud.google.com/storage?hl=zh-tw)。您可以向 Campaign Manager 管理員索取 Cloud Storage 值區相關資訊，並要求存取權。

## Google Ads 移轉問題

以下是[建立 Google Ads 移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)時的常見錯誤。

問題：轉移作業成功執行，但部分帳戶未顯示在目的地資料表中。
:   **解決方法：**帳戶未顯示在報表中的原因有很多，常見原因包括：

    * 如果要求當天沒有任何報表活動，系統就不會產生資料列，因此會發生這種情況。
    * 如果 Google Ads 帳戶處於閒置狀態，或`CANCELLED`，也可能發生這種情況。Google Ads API 不支援對停用帳戶的查詢，因此 Google Ads 連接器已從轉移作業中篩除停用帳戶。如要重新啟用 Google Ads 帳戶，請參閱「[重新啟用已取消的 Google Ads 帳戶](https://support.google.com/google-ads/answer/2375392?hl=zh-tw)」。

發生錯誤：`AUTH_ERROR_TWO_STEP_VERIFICATION_NOT_ENROLLED`
:   **解決方法：**這項錯誤表示用於移轉的 Google Ads 使用者未啟用兩步驟驗證。如要瞭解如何啟用兩步驟驗證，請參閱「[開啟兩步驟驗證](https://support.google.com/accounts/answer/185839?hl=zh-tw)」。

發生錯誤：`No jobs to start for run`
:   **解決方法：**這個錯誤表示由於設定無效或處理期間發生錯誤，因此系統未啟動轉移作業的載入工作。請按照下列步驟解決這項錯誤：

    * 查看移轉執行作業記錄中的錯誤和警告。
    * 如果嘗試載入的表格沒有 `segments_date`、`segments_week`、`segments_month`、`segments_quarter` 或 `segments_year` 欄，且 `run_date` 不是最新日期，系統就會略過載入作業。詳情請參閱「[手動觸發 Google Ads 轉移](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#backfill)」和「[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#custom_reports)」。
    * 如果無法找出根本原因，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`

發生錯誤：`No data available for the requested date. Please try an earlier run date or verify that data existence was expected.`
:   **解決方法：**如果您在建立 Google Ads 移轉作業時收到這個錯誤，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)並提供錯誤訊息的螢幕擷取畫面。

發生錯誤：`AuthenticationError.NOT_ADS_USER.`
:   **解決方法：**設定 Google Ads 移轉作業的使用者必須擁有 Google Ads 帳戶/登入資訊。

發生錯誤：`Request is missing required authentication credential`
:   **解決方法：**使用者或服務帳戶沒有 Ads 帳戶的存取權。按照「[必要權限](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#required_permissions)」一節的說明，授予使用者或服務帳戶必要權限。

發生錯誤：`ERROR_GETTING_RESPONSE_FROM_BACKEND.`
:   **解決方法：**如果 Google Ads 移轉作業執行失敗並傳回 `ERROR_GETTING_RESPONSE_FROM_BACKEND`，請在移轉設定中[**啟用「排除已移除/停用的項目」選項**](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer)，並[設定補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，嘗試擷取在移轉作業執行失敗影響期間內的相關資料。

警告：`Data for the report ClickStats was not available for the specified date.`

發生錯誤：`INVALID_DATE_RANGE_FOR_REPORT.`
:   **解決方法：**如果回填 [Click Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/click-performance-report?hl=zh-tw) 資料的時間超過 90 天，就會發生這種情況。在這種情況下，您會看到這則警告或錯誤訊息，且 `ClickStats` 表格不會更新指定日期的資料。

發生錯誤：`Error while processing report for table table_name for account id account_id. Http(400) Bad Request;`

發生錯誤：`AuthorizationError.TWO_STEP_VERIFICATION_NOT_ENROLLED`
:   **解決方法：**如果與這項轉移作業相關聯的使用者帳戶未啟用兩步驟驗證 (或多重驗證)，請為該帳戶[啟用兩步驟驗證](https://support.google.com/google-ads/answer/12864186?hl=zh-tw)，然後重新執行失敗的轉移作業。服務帳戶可免除兩步驟驗證規定。

發生錯誤：`Quota exceeded: Your project exceeded quota for imports per project`
:   **解決方法：**移轉作業必須符合 BigQuery 的[載入工作配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)規定。如果載入作業達到配額上限，請使用 [table\_filter](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer) 減少不必要的載入作業、刪除未使用的移轉設定，或縮短重新整理時間範圍。如要提高配額，請洽詢您的 Google Cloud 業務代表。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

## Google Ad Manager 移轉問題

以下是建立 [Google Ad Manager 移轉作業](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`Another transfer run is concurrently processing table.`
:   **解決方法：**如果目前移轉作業開始時，另一個具有相同移轉設定的移轉作業尚未完成，就可能會發生這項錯誤。

* 如果延遲是由大型 Google Ad Manager 資料移轉 (Google Ad Manager DT) 檔案所致，請考慮啟用[Parquet 格式](https://support.google.com/admanager/answer/1733124?hl=zh-tw)，這種格式的載入效能較佳。
* 如果延遲是由對照表所致，請考慮將參數 `load_match_tables` 設為 `false`，略過對照表。
* 如果轉移處理時間一律比目前的重複頻率長，請調整重複頻率。

發生錯誤：`No data available for the requested date. Please try an earlier run date or verify that data existence was expected.`

發生錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`
:   **解決方法：**確認 Google Ad Manager [Cloud Storage bucket](http://console.cloud.google.com/storage?hl=zh-tw) 含有指定日期範圍內的資料移轉檔案。您的 Google Ad Manager 管理員負責管理含有資料移轉檔案的 [Cloud Storage 值區](http://console.cloud.google.com/storage?hl=zh-tw)。建立 Google Ad Manager 移轉作業的使用者必須是 Google 網上論壇中擁有值區存取權的成員。
:   您可以試著讀取 Google Ad Manager [資料移轉 bucket](http://console.cloud.google.com/storage?hl=zh-tw)中的檔案，確認是否具備 Cloud Storage 權限。如要進一步瞭解 Google Ad Manager Cloud Storage 值區，請參閱[存取 Google Ad Manager 儲存空間值區](https://support.google.com/admanager/answer/1733127?hl=zh-tw)。
:   您可以查看 Cloud Storage bucket 中檔案的建立時間，確認檔案在排定轉移作業時是否存在。在某些情況下，系統可能會在產生第一批 Google Ad Manager 資料移轉檔案之前，排定當天的第一次移轉作業。當天和隔天後續的執行作業會載入 Google Ad Manager 產生的所有檔案。
:   如果檔案是在資料移轉值區且您有讀取權，請排定受影響日期範圍內的補充作業。如要進一步瞭解如何建立 Google Ad Manager 補充作業要求，請參閱「[設定補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)」。

發生錯誤：`AuthenticationError: NO_NETWORKS_TO_ACCESS.`
:   **解決方法：**確定您具有 Google Ad Manager 網路的讀取權限。如果您在確認網路存取權時需要協助，請與 [Google Ad Manager 支援小組](https://support.google.com/admanager/answer/3059042?hl=zh-tw)聯絡。

發生錯誤：`Error code 9 : Field field_name?field_name?field_name?RefererURL is unknown.; Table: table_name`
:   **解決方法：**確定您不是使用小寫的古英語符文字母 (þ) 分隔符號。系統不支援 thorn 分隔符號。若使用小寫的古英語符文字母，系統會在錯誤訊息中以 ? 表示。

發生錯誤：`Incompatible table partitioning specification. Destination table exists with partitioning specification interval(type:Day,field:) clustering`
:   **解決方法：**Google Ads 管理員連接器不支援將資料移轉至具有分群功能的資料集。請改用沒有叢集功能的資料集。

## Google Merchant Center 移轉問題

以下是[建立 Google Merchant Center 移轉作業](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`No data to transfer found for the Merchant account. If you have just created this transfer - you may need to wait for up to 90 minutes before the data of your Merchant account are prepared and available for the transfer.`
:   **解決方法：**如果您使用「Schedule」(排程) 專區中的預設開始日期和時間設定移轉作業，就會收到這個錯誤。如果您使用預設的排程值，第一項移轉作業會在移轉建立後立即開始執行，但由於您的商家帳戶資料尚未準備就緒，因此執行作業會失敗。請先等待 90 分鐘，然後為今日[設定補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，您也可以選擇等到明天的下一個預定移轉時間。

發生錯誤：`No data to transfer found for Merchant account. This can be because your account currently doesn't have any products.`
:   **解決方法：**這個錯誤代表你的商家帳戶沒有商品。你將產品新增至商家帳戶之後，移轉作業就會開始執行。

發生錯誤：`Transfer user doesn't have access to the Merchant account. Please verify access in the Users section of the Google Merchant Center.`
:   **解決方法：**這個錯誤表示設定移轉作業的使用者沒有移轉作業所用商家帳戶的存取權。如要解決這個問題，請前往 Google Merchant Center [驗證並授予缺少的帳戶存取權](https://support.google.com/merchants/answer/1637190?hl=zh-tw)。

發生錯誤：`Transfer user doesn't have user roles that allows access to the product data of the Merchant account. Please verify access and roles in the Users section of the Google Merchant Center.`
:   **解決方法：**這個錯誤表示設定移轉作業的使用者沒有移轉所用商家帳戶產品資料的存取權。如要解決這個問題，請前往 Google Merchant Center [驗證並授予缺少的使用者角色](https://support.google.com/merchants/answer/1637190?hl=zh-tw)。

發生錯誤：`Historical backfills are not supported.`
:   **解決方法：**如果您為前幾日[設定補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，就會收到這個錯誤。這是預期中的錯誤。系統不支援歷史補充作業。
    您只能為今日設定補充作業，在排定的每日執行作業完成後重新整理今日資料。

## Google Play 移轉問題

以下是[建立 Google Play 移轉作業](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`No jobs to start for run`
:   **解決方法：**確認使用者是否具備[啟動 Google Play 移轉作業的足夠權限](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#required_permissions)，然後確認使用者在設定移轉作業時，是否指定了正確的 Cloud Storage 值區。如果使用者仍遇到錯誤，請[要求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

問題：收益和財務報表未載入至 BigQuery
:   **解決方法：**使用者必須具備 `View financial data` 權限，才能存取 Google Play 財務報表。如要管理開發人員帳戶權限，請參閱「[新增開發人員帳戶使用者以及管理各項權限](https://support.google.com/googleplay/android-developer/answer/9844686?visit_id=638158652462486298-3898390440&%3Brd=1&hl=zh-tw)」。

## HubSpot 轉移問題

發生錯誤：`PERMISSION_DENIED: Permission denied. Your Access Token may lack required access to the provided account. Please also check for typos like whitespace or if the provided accountId even exists`
:   **解決方法：**確認私人應用程式存取權杖正確無誤、HubSpot 使用者具有**超級管理員**角色，且私人應用程式具備所有必要範圍。詳情請參閱 [HubSpot 先決條件](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw#hubspot-prerequisites)。

發生錯誤：`INVALID_ARGUMENT: Table 'NAME' does not exist in asset "ASSET"`
:   **解決方法：**確認指定的資產名稱有效，且不含任何開頭或結尾空格。[建立 HubSpot 轉移作業](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw#hubspot-transfer-setup)時，建議按一下「瀏覽」，從可用物件清單中選取資產。

發生錯誤：`FAILED_PRECONDITION: Rate limit exceeded.`
:   **解決方法：**已超過 HubSpot API 使用頻率限制。請稍候再試一次資料移轉。您也可以考慮降低資料移轉作業的頻率，並限制類似帳戶的同時移轉作業。

發生錯誤：`UNAUTHENTICATED: Authentication failed. Please verify your HubSpot access token.`
:   **解決方法：**確認私人應用程式存取權杖是否正確。詳情請參閱 [HubSpot 先決條件](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw#hubspot-prerequisites)。

發生錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認 HubSpot 私人應用程式存取權杖正確無誤，且具備存取物件所需的權限，然後重試移轉工作。

## Klaviyo 轉移問題

以下是[建立 Klaviyo 移轉作業](https://docs.cloud.google.com/bigquery/docs/klaviyo-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`PERMISSION_DENIED: Permission denied. Your API key may lack required access scopes`
:   **解決方法：**確認 Klaviyo 非公開 API 金鑰至少具有 `READ ONLY` 存取層級。詳情請參閱「[Klaviyo 先決條件](https://docs.cloud.google.com/bigquery/docs/klaviyo-transfer?hl=zh-tw#klaviyo-prerequisites)」。

發生錯誤：`FAILED_PRECONDITION`
:   **解決方法：**縮短日期範圍，然後重試轉移作業。

發生錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認帳戶的 API 金鑰有效，然後重試轉移作業。

發生錯誤：`INTERNAL: An unknown error occurred while processing the request.`
:   **解決方法：**確認帳戶的 API 金鑰有效，然後重試轉移作業。

## Microsoft SQL Server 轉移問題

以下是[建立 Microsoft SQL Server 移轉作業](https://docs.cloud.google.com/bigquery/docs/sqlserver-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`FAILED PRECONDITION: A TLS/SSL handshake error occurred: unable to find valid certification path to requested target. Please check your TLS/SSL configuration and certificate validity.`
:   **解決方法：**請按照下列步驟驗證憑證是否有效：

    1. 將 SQL Server 上的 SSL/TLS 憑證，換成由信任的 Public Certificate Authority 核發的憑證。詳情請參閱「[TLS 設定](https://docs.cloud.google.com/bigquery/docs/sqlserver-transfer?hl=zh-tw#tls_configuration)」。
    2. 確認新憑證包含完整的憑證鏈結，包括所有中繼和根憑證。
    3. 更新憑證後，請重新啟動 SQL Server 服務，套用新的 SSL/TLS 設定。
    4. 伺服器重新啟動後，請再次建立移轉設定，確認更新後的憑證是否受信任，以及 TLS/SSL 交握是否順利完成。

發生錯誤：`INVALID_ARGUMENT: Catalog 'SCHEMA' does not exist in asset "SCHEMA/TABLE"`
:   **解決方法：**確認 SQL Server 中有目錄和資料表，且拼寫正確。此外，請確認使用者擁有足夠的存取權限，可瀏覽或查詢目錄及其內容。

## Mailchimp 轉移問題

以下是[建立 Mailchimp 轉移作業](https://docs.cloud.google.com/bigquery/docs/mailchimp-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`INVALID_ARGUMENT: Invalid request. Please check the input parameters (Credentials, Table, etc.) and try again.`
:   **解決方法：**確認指定的資產名稱有效，且不含任何開頭或結尾空格。[建立 Mailchimp 轉移作業](https://docs.cloud.google.com/bigquery/docs/mailchimp-transfer?hl=zh-tw)時，建議按一下「瀏覽」，從可用物件清單中選取資產。

發生錯誤：`PERMISSION_DENIED: Permission denied. Your credentials may lack required access.`
:   **解決方法：**確認 Mailchimp 使用者具備所有必要權限。[`Admin` Mailchimp 的使用者層級](https://mailchimp.com/help/manage-user-levels-in-your-account/)必須具備最低存取權，才能轉移所有 Mailchimp 物件。

發生錯誤：`FAILED_PRECONDITION: Operation failed due to precondition violation (ex- Rate limit exceeded, Server Error). Please try again later.`
:   **解決方法：**請稍待片刻，再重試資料移轉。你也可以查看 [Mailchimp 狀態](https://status.mailchimp.com/)，瞭解是否有服務中斷的情況。

發生錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認 API 金鑰有效，且使用者具備所有必要權限，然後重試資料移轉工作。

## MySQL 轉移問題

以下是[建立 MySQL 移轉作業](https://docs.cloud.google.com/bigquery/docs/mysql-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`PERMISSION_DENIED. Failed to authenticate or permission denied with the provided credentials when starting to transfer asset asset-name.`
:   **解決方法：**檢查您提供的 `connector.authentication.username` 和 `connector.authentication.password` 參數是否有效且正常運作。

發生錯誤：`NOT_FOUND. Invalid data source configuration provided when starting to transfer asset asset-name: APPLICATION_ERROR;google.cloud.bigquery.federationv1alpha1/ConnectorService.StartQuery;INVALID_ARGUMENT:Exception was thrown by the Connector implementation: Table table-name does not exist in asset asset-name.`
:   **解決方法：**檢查資料表或檢視表名稱的拼字是否正確、參照的資料表或檢視表名稱是否存在，以及同義字 (別名) 是否指向現有的資料表或檢視表。

    如果資料表或檢視區塊存在，請確保已授予資料庫使用者存取資料表的正確權限。如果資料表或檢視區塊不存在，請建立資料表。

    如要存取其他結構定義中的資料表或檢視區塊，請確認已參照正確的結構定義，並已獲授物件存取權。

    如果提供資料表或檢視表名稱，請確保該名稱指定為 `object_name`；否則請留空。

發生錯誤：`SERVICE_UNAVAILABLE. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`

發生錯誤：`DEADLINE_EXCEEDED. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`
:   **解決方法：**檢查提供的資料庫詳細資料是否正確，並確認移轉設定使用的網路連結設定正確無誤。轉移作業也可能未在期限內完成。

發生錯誤：`INTERNAL`
:   **解決方法：**轉移失敗的原因是其他問題。如要解決這個問題，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`INVALID_ARGUMENT. Connection to the host and port failed. Please check that the host, port, encryptionMode and network attachment are correct.`
:   **解決方法：**請確認主機、通訊埠、加密模式和網路設定正確無誤。確認網路連線，以及資料庫伺服器是否可存取。如果 `EncryptionMode` 設為 `FULL`，請確認伺服器支援必要通訊協定、具有有效憑證，且允許安全連線。如果 `EncryptionMode` 設為 `DISABLE`，請確認伺服器允許非 SSL 連線。查看應用程式和資料庫記錄，瞭解連線或 SSL/TLS 相關錯誤。

## Oracle 轉移問題

以下是[建立 Oracle 移轉作業](https://docs.cloud.google.com/bigquery/docs/oracle-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`PERMISSION_DENIED. ORA-01017: invalid username/password; logon denied`
:   **解決方法：**確認提供的 Oracle 憑證有效。

發生錯誤：`PERMISSION_DENIED. ORA-01045: user lacks CREATE SESSION privilege; logon denied`
:   **解決方法：**將 `CREATE SESSION` 系統權限授予 Oracle 使用者。如要進一步瞭解如何授予 Oracle 權限，請參閱 [`GRANT`](https://docs.oracle.com/cd/B13789_01/server.101/b10759/statements_9013.htm)。

錯誤：`SERVICE_UNAVAILABLE. ORA-12541: Cannot connect. No listener at host HOSTNAME port PORT` 或 `SERVICE_UNAVAILABLE. Connection failed: IO Error. The Network Adapter could not establish the connection`
:   **解決方法：**確認提供的主機名稱和通訊埠詳細資料正確無誤，且網路連結設定正確。

發生錯誤：`NOT_FOUND. ORA-00942: table or view does not exist`
:   **解決方法：**請檢查下列各項：

* 資料表或檢視表名稱的拼字正確。
* 參照的資料表或檢視表名稱存在。
* 同義字會指向現有資料表或檢視表。如果資料表或檢視區塊確實存在，請確認已授予資料庫使用者存取資料表的正確權限。否則請建立資料表。
* 如果您嘗試存取其他結構定義中的資料表或檢視畫面，請確認已參照正確的結構定義，並已獲授物件存取權。

發生錯誤：`NOT_FOUND. Schema schema does not exist.`
:   **解決方法：**指定的結構定義不存在。

發生錯誤：`DEADLINE_EXCEEDED`
:   **解決方法：**轉移作業未在六小時內完成。將大型轉移作業分割為多個較小的作業，縮短轉移作業的執行時間。

發生錯誤：`INTERNAL`
:   **解決方法：**轉移失敗的原因是其他問題。如要解決這個問題，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`INVALID_ARGUMENT`
:   **解決方法：**移轉設定中提供的值無效，導致移轉失敗。如要瞭解有效的移轉設定值，請參閱「[設定 Oracle 轉移作業](https://docs.cloud.google.com/bigquery/docs/oracle-transfer?hl=zh-tw#oracle-transfer-setup)」。

發生錯誤：`SQL Error [1950] [42000]: ORA-01950: no privileges on tablespace 'TablespaceName'`
:   **解決方法：**將預設表空間指派給使用者。詳情請參閱「[指派預設資料表空間](https://docs.oracle.com/cd/B19306_01/network.102/b14266/admusers.htm#i1006219)」一文。

發生錯誤：`403 PERMISSION_DENIED. Required 'compute.subnetworks.use' permission for project`
:   **解決方法：**如果網路連結所在的專案與傳輸設定所在的專案不同，就可能發生這個錯誤。如要修正這個問題，您必須在網路連結所在的專案中，授予服務帳戶 (例如 `service-customer_project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`) 下列權限：

    * `compute.networkAttachments.get`
    * `compute.networkAttachments.update`
    * `compute.subnetworks.use`
    * `compute.regionOperations.get`

    如果網路附件嘗試連線至位於不同專案的虛擬私有雲 (例如共用虛擬私有雲)，也可能發生這個錯誤。在這種情況下，您必須將共用虛擬私有雲主專案的 `compute.subnetworks.use` 權限授予服務帳戶 (例如 `service-customer_project_number@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com`)。

## PayPal 轉移問題

以下是[建立 PayPal 轉移作業](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`PERMISSION_DENIED: Authorization failed due to insufficient permissions.`
:   **解決方法：**確認用戶端和用戶端密鑰具有[必要權限](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)，可存取要轉移的 PayPal 物件。

發生錯誤：`INVALID_ARGUMENT: Table 'OBJECT' does not exist in asset "OBJECT"`
:   **解決方法：**確認物件名稱是否有效。

發生錯誤：`INVALID_ARGUMENT: The given start date 'DATE' cannot be parsed. Please provide it in 'yyyy-MM-dd' format.`
:   **解決方法：**確認開始日期語法是否正確。

發生錯誤：`UNAUTHENTICATED: Please provide a valid clientId and client secret.`
:   **解決方法：**確認用戶端 ID 和用戶端密鑰是否正確。

發生錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認私密金鑰和帳戶 ID 有效，且所選物件已具備[必要權限](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)，然後重試移轉工作。如果問題持續發生，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`INTERNAL: An unknown error occurred while processing the request.`
:   **解決方法：**確認私密金鑰和帳戶 ID 有效，且所選物件已具備[必要權限](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)，然後重試移轉工作。如果問題仍未解決，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## PostgreSQL 轉移問題

以下是[建立 PostgreSQL 移轉作業](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`PERMISSION_DENIED. Failed to authenticate or permission denied with the provided credentials when starting to transfer asset asset-name.`
:   **解決方法：**檢查您提供的 `connector.authentication.username` 和 `connector.authentication.password` 參數是否有效且正常運作。

發生錯誤：`NOT_FOUND. Invalid data source configuration provided when starting to transfer asset asset-name: APPLICATION_ERROR;google.cloud.bigquery.federationv1alpha1/ConnectorService.StartQuery;INVALID_ARGUMENT:Exception was thrown by the Connector implementation: Table table-name does not exist in asset asset-name.`
:   **解決方法：**檢查資料表或檢視表名稱的拼字是否正確、參照的資料表或檢視表名稱是否存在，以及同義字 (別名) 是否指向現有的資料表或檢視表。

    如果資料表或檢視區塊存在，請確保已授予資料庫使用者存取資料表的正確權限。如果資料表或檢視區塊不存在，請建立資料表。

    如要存取其他結構定義中的資料表或檢視區塊，請確認已參照正確的結構定義，並已獲授物件存取權。

    如果提供資料表或檢視表名稱，請確保該名稱指定為 `object_name`；否則請留空。

發生錯誤：`SERVICE_UNAVAILABLE. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`

發生錯誤：`DEADLINE_EXCEEDED. Timed out when starting to transfer asset asset-name. Ensure the datasource is reachable and the datasource configuration (Credentials, Network Attachment etc.) is correct.`
:   **解決方法：**檢查提供的資料庫詳細資料是否正確，並確認移轉設定使用的網路連結設定正確無誤。轉移作業也可能未在期限內完成。

發生錯誤：`INTERNAL`
:   **解決方法：**轉移失敗的原因是其他問題。如要解決這個問題，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`INVALID_ARGUMENT. Connection to the host and port failed. Please check that the host, port, encryptionMode and network attachment are correct.`
:   **解決方法：**請確認主機、通訊埠、加密模式和網路設定正確無誤。確認網路連線，以及資料庫伺服器是否可存取。如果 `EncryptionMode` 設為 `FULL`，請確認伺服器支援必要通訊協定、具有有效憑證，且允許安全連線。如果 `EncryptionMode` 設為 `DISABLE`，請確認伺服器允許非 SSL 連線。查看應用程式和資料庫記錄，瞭解連線或 SSL/TLS 相關錯誤。

發生錯誤：`INVALID_ARGUMENT: For Asset "postgres"."auth"."sessions", row count exceeds the max supported unIndexed read size of 2000000 records.`
:   **解決方法：**如果您嘗試將超過 2,000,000 筆記錄從 PostgreSQL 資料表轉移至 BigQuery 資料表，但 PostgreSQL 資料表中沒有主鍵或索引資料欄，就可能發生這項錯誤。如要解決這個問題，請在資料表中新增主鍵或索引資料欄。詳情請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw#limitations)」一節。

## Salesforce 轉移問題

以下是[建立 Salesforce 移轉作業](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`Permission Denied: invalid_client. invalid client credentials`
:   **解決方法：**確認提供的 ClientSecret 有效。

發生錯誤：`Permission Denied: invalid_client. client identifier invalid`
:   **解決方法：**確認提供的 ClientId 有效。

發生錯誤：`Permission Denied: Error encountered while establishing connection`
:   **解決方法：**檢查提供的 Salesforce MyDomain 名稱是否正確。

發生錯誤：`NOT_FOUND. asset type asset_name is not supported. If you are attempting to use a custom object, be sure to append the "__c" after the entity name. Please reference your WSDL or use the describe call for the appropriate names.`
:   **解決方法：**按照錯誤代碼中的指引操作，並確認提供的資產名稱正確無誤。

發生錯誤：`SERVICE_UNAVAILABLE`
:   **解決方法：**這項服務暫時無法處理要求。請稍候片刻，然後再試一次。

發生錯誤：`DEADLINE_EXCEEDED`
:   **解決方法：**轉移作業未在六小時內完成。將大型轉移作業分割為多個小型作業，盡量縮短轉移作業的執行時間。

發生錯誤：`Failed to create recordReader to read partition : Batch failed. BatchId='batch_id', Reason='FeatureNotEnabled : Binary field not supported'`
:   **解決方法：**連接器不支援含有二進位欄位的 sObject 資料結構。從移轉作業中移除含有二進位欄位的 sObject 資料結構。詳情請參閱 Salesforce 說明文件中的「[Error 'Batch failed: FeatureNotEnabled: Binary field not supported' when you export related object](https://help.salesforce.com/s/articleView?id=000382669&type=1)」一文。

發生錯誤：`RESOURCE_EXHAUSTED: PrepareQuery failed : ExceededQuota : ApiBatchItems Limit exceeded`
:   **解決方法：**如果工作執行次數超過每日 `ApiBatchItems` API 限制，就會顯示這則錯誤訊息。Salesforce 設有每日 API 限制，每 24 小時會重設一次。如要解決這項錯誤，建議您將轉移作業分批進行並排定時間，以免超過每日批次 API 限制。你也可以聯絡 Salesforce 支援團隊，要求提高每日限制。

發生錯誤：`Permission Denied: invalid_grant. no client credentials user enabled`
:   **解決方法：**確認 Salesforce 連線應用程式「Client Credentials Flow」(用戶端憑證流程) 部分的「Run as」(以使用者身分執行) 欄位包含正確的使用者名稱。詳情請參閱「[建立 Salesforce 連結的應用程式](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#create-sf-app)」。

發生錯誤：`FAILED_PRECONDITION: BatchId='batch-id', Reason='InvalidBatch : Failed to process query: OPERATION_TOO_LARGE: exceeded 100000 distinct ids'`
:   **解決方法：**確認使用者的設定檔不會對擷取的 sObject 施加查詢限制。如果問題仍未解決，請使用具備系統管理員權限的 Salesforce 使用者憑證完成擷取作業。

發生錯誤：`FAILED_PRECONDITION: Batch failed. BatchId='batch-id', Reason='InvalidBatch : Failed to process query: TXN_SECURITY_NO_ACCESS: The operation you requested isn't allowed due to a security policy in your organization. Contact your administrator for more information about security policies.`
:   **解決方法：**確認使用者設定檔或權限集包含必要物件和欄位層級權限，才能擷取 sObject。請與管理員聯絡，要求對方更新這些權限，或是指派具備必要存取權的角色。

發生錯誤：`FAILED_PRECONDITION: Cannot establish connection to Salesforce to describe SObject: 'SObject_Name' due to error: TotalRequests Limit exceeded., Cause:null Retry after some time post quota reset.`
:   **解決方法：**如果[載入工作超過限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)，就可能發生這項錯誤。請等待配額重設後再試一次。

發生錯誤：`FAILED_PRECONDITION: There was an issue connecting to Salesforce Bulk API.`
:   **解決方法：**如果您在轉移作業中加入網路連結，但未設定 Public NAT 和 IP 允許清單，就可能發生這個錯誤。如要解決這項錯誤，請完成「[為 Salesforce 移轉作業設定 IP 許可清單](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#salesforce-allowlist)」一文中的所有步驟。

發生錯誤：`SYSTEM ERROR when starting to transfer asset asset_name, try again later.`
:   **解決方法：**如果 Salesforce 機構未啟用 Bulk API，就可能會發生這個錯誤。如要解決這個錯誤，請更新 Salesforce 授權，加入 Bulk API 支援。詳情請參閱「[啟用非同步 API](https://help.salesforce.com/s/articleView?id=000386981&type=1)」。

## Shopify 轉移問題

發生錯誤：`[NOT_FOUND] Your app doesn't have a publication for this shop.`
:   **解決方法：**如果自訂應用程式的設定方式有問題，就可能發生這項錯誤。建議按照下列步驟解除安裝並重新安裝自訂應用程式。

    1. [解除安裝 Shopify 應用程式](https://help.shopify.com/en/manual/apps/uninstalling-apps)。
    2. [建立自訂應用程式](https://help.shopify.com/en/manual/apps/install-setup-apps#create-and-install-a-custom-app)，並設定下列項目：
       1. 建立應用程式時，請選取「自訂發布」。請提供商店網域或管理員網址。設定完成後，Shopify 會產生連結，供你完成應用程式安裝。詳情請參閱「[選取發布方式](https://shopify.dev/docs/apps/launch/distribution/select-distribution-method)」。
       2. 建立應用程式時，按一下「API access request」，然後選取「Enable storefront」並啟用 `read_all_orders` 範圍。
       3. 安裝自訂應用程式。
    3. 重新安裝自訂應用程式後，請再次執行資料移轉。

發生錯誤：`PERMISSION_DENIED: Permission denied. Your API key may lack required access to the provided account. Please also check for typos like whitespace or if the provided accountId even exists`
:   **解決方法：**確認 Shopify Admin API 存取權杖正確無誤，並確認 Shopify 應用程式具備所有[必要存取權角色](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw#shopify-prerequisites)。

發生錯誤：`INVALID_ARGUMENT: Table 'NAME' does not exist in asset "ASSET"`
:   **解決方法：**確認指定的資產名稱有效，且開頭或結尾沒有空格。[建立 Shopify 轉移作業](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw#shopify-transfer-setup)時，建議點選「瀏覽」，從可用物件清單中選取資產。

發生錯誤：`UNAUTHENTICATED: Authentication failed. Please verify your Shopify access token.`
:   **解決方法：**檢查 Shopify 管理 API 存取權杖是否正確。詳情請參閱 [Shopify 先決條件](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw#shopify-prerequisites)。

發生錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認 Shopify Admin API 存取權杖和商店名稱正確無誤，然後重試轉移作業。如果問題仍未解決，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## Stripe 轉移問題

以下是[建立 Stripe 轉移](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`PERMISSION_DENIED: Permission denied. Your API key may lack required access to the provided account. Please also check for typos like whitespace or if the provided accountId even exists`
:   **解決方法：**如果您使用受限制的 API 金鑰，請確認該金鑰有權存取要轉移的 Stripe 物件。更新受限金鑰的權限後，請再次執行資料移轉作業。如要瞭解如何管理密鑰，請參閱「[密鑰和受限金鑰](https://docs.stripe.com/keys#secret-and-restricted-keys)」一文。

發生錯誤：`INVALID_ARGUMENT: Table 'NAME' does not exist in asset "ASSET"`
:   **解決方法：**確認指定的資產名稱有效，且開頭或結尾沒有空格。[建立 Stripe 轉移](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw)時，建議按一下「瀏覽」，從可用物件清單中選取資產。

發生錯誤：`UNAUTHENTICATED: Authentication failed. Please verify your Stripe API key.`
:   **解決方法：**確認密鑰和帳戶 ID 正確無誤。如要瞭解如何擷取這項資訊，請參閱「[Stripe 必要條件](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw#stripe-prerequisites)」一文。

發生錯誤：`RESOURCE_EXHAUSTED: Rate limit exceeded.`
:   **解決方法：**你可能超過 Stripe API 使用頻率限制。請稍候片刻，再重試資料移轉工作要求。為避免發生這個問題，建議減少資料移轉工作的頻率，並限制從相同帳戶進行的並行移轉作業。

發生錯誤：`UNAVAILABLE: Stripe service is temporarily unavailable. Please try again shortly.`
:   **解決方法：**請稍待片刻，再重試資料移轉。如要查看是否有服務中斷情形，請前往 [Stripe 狀態頁面](https://status.stripe.com/)。

發生錯誤：`UNKNOWN: An unknown error occurred while processing the request.`
:   **解決方法：**確認私密金鑰和帳戶 ID 有效，且所選物件具備必要權限，然後重試移轉作業。如果問題仍未解決，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

發生錯誤：`INTERNAL: An unknown error occurred while processing the request.`
:   **解決方法：**確認私密金鑰和帳戶 ID 有效，且所選物件具備必要權限，然後重試移轉作業。如果問題仍未解決，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## ServiceNow 轉移問題

以下是[建立 ServiceNow 轉移作業](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw)時可能遇到的常見問題。

發生錯誤：`UNAUTHENTICATED. Required authentication credentials were not provided when starting to transfer asset asset-name.`
:   **解決方法：**確認提供的憑證 (`username`、`password`、`ClientID` 和 `Client Secret`) 有效、已正確設定且未過期。

發生錯誤：`INVALID_ARGUMENT. Invalid datasource configuration provided when starting to transfer asset`

發生錯誤：`INVALID_ARGUMENT: Http call to ServiceNow instance returned status code 400.. Please make sure the instance/endpoint provided exists/is correct.`
:   **解決方法：**確認 ServiceNow 執行個體網址和 API 端點正確無誤，且參照的資料表存在，並可使用提供的憑證存取。

發生錯誤：`PERMISSION_DENIED. User credentials don't have permission or are invalid for accessing the ServiceNow asset or API.`
:   **解決方法：**確認提供的憑證正確無誤，且 ServiceNow 帳戶具備足夠的權限，可存取指定的資產或表格。

發生錯誤：`UNAVAILABLE. ServiceNow instance is temporarily unreachable or experiencing downtime.`
:   **解決方法：**確認網路連線穩定，然後過一段時間再試一次。這項錯誤可能是因為 ServiceNow 暫時服務中斷，或是連線能力暫時發生問題。

發生錯誤：`RESOURCE EXHAUSTED. ServiceNow API rate limit or quota has been exceeded, or operations are too large.`
:   **解決方法：**你已超過 ServiceNow API 配額或使用頻率限制。建議減少要求數量或頻率，然後再試一次。

發生錯誤：`FAILED_PRECONDITION: There was an issue connecting to API.`
:   **解決方法：**如果您在轉移作業中加入網路連結，但未設定 Public NAT 和 IP 允許清單，就可能發生這個錯誤。如要解決這項錯誤，請[建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw#create_a_network_attachment)，並定義靜態 IP 位址。

## Teradata 轉移問題

以下是建立 Teradata 移轉作業時可能遇到的常見問題。

發生錯誤：`Skipping extraction since table does not have change tracking column.`
:   **解決方法：**如果您嘗試使用現有的隨選轉移設定，在已遷移的資料表上執行 Teradata 轉移作業，可能會看到上述訊息。如要在已遷移的資料表上啟動新的遷移作業，請[建立新的遷移設定](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw#set_up_a_transfer)，並套用「隨選」設定。

    使用隨選移轉設定重複移轉時，BigQuery 資料移轉服務會嘗試以增量移轉方式執行，但由於移轉設定未套用正確的增量設定，因此會略過資料表。如要進一步瞭解不同類型的轉移作業，請參閱「[隨選或增量轉移](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#incremental)」。

問題：轉移 `CHAR`(N) 資料類型時，較短的字串會新增最多 N 個字元的空格。
:   **解決方法：**將 `CHAR` 資料轉換為 `VARCHAR`，並移除來源中的多餘空格。發生這個問題的原因是 [`CHAR` 是固定長度的字串](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Types-and-Literals/June-2017/Character-and-CLOB-Data-Types/Character-Data)，而 [`VARCHAR` 則應適用於長度可變的字串](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Types-and-Literals/June-2017/Character-and-CLOB-Data-Types/VARCHAR-Data-Type)。您也可以在遷移後，使用 [`RTRIM` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#rtrim)移除 BigQuery 中的空格。使用 `RTRIM` 函式的查詢類似於下列範例：

    ```
    UPDATE migrated_table
    SET migrated_char_column = RTRIM(migrated_char_column)
    WHERE true;
    ```

## YouTube 移轉問題

以下是[建立 YouTube 轉移作業](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw)時的常見錯誤。

發生錯誤：`Import failed - no data was available for import. Please verify that data existence was expected.`

發生錯誤：`No data available for requested date. Please try an earlier run date or verify that data existence was expected.`
:   **解決方法：**如果您先前未曾建立過 YouTube [報告工作](https://developers.google.com/youtube/reporting/v1/reports/?hl=zh-tw#step-3-create-a-reporting-job)，請允許 YouTube 至少有 2 天的緩衝時間，讓 BigQuery 資料移轉服務可以代表您產生報告。你不需要採取其他動作。
    前 2 天轉移會失敗，第 3 天應該就能成功。如果您之前建立過 YouTube 報告工作，請確認建立移轉作業的使用者具備報告的讀取權。
:   另請確認是否使用正確的帳戶設定移轉作業。您也必須在 OAuth 對話方塊中選取要載入資料的管道。

發生錯誤：`No reports for reporting job with name name.`
:   **解決方法：**這並不是錯誤。這是一則警告訊息，表示系統找不到指定報告的資料。您可以忽略這則警告。未來的移轉作業仍會繼續執行。

**注意：** 對 YouTube 內容管理工具來說，某些檔案每月只能取得一次。其他時間這些每月報告會顯示為「遺漏」。這是預期的行為。您無須採取任何行動，如果報告不應該遺漏，請透過[說明論壇](https://productforums.google.com/forum/?hl=zh-tw#!forum/youtube)與 YouTube 支援團隊聯絡。

問題：移轉作業建立的結果資料表不完整，或結果不如預期。
:   **解決方法：**如果您有多個帳戶，則必須在接收 YouTube 權限對話方塊中選擇正確的帳戶。

問題：YouTube 數據分析和 BigQuery YouTube 移轉的資料不一致。
:   **背景：**BigQuery YouTube 移轉作業會使用 [YouTube Reporting API](https://developers.google.com/youtube/reporting/v1/reports?hl=zh-tw)，將資料直接擷取至 BigQuery 資料集。另一方面，YouTube 數據分析資訊主頁會使用 [YouTube Analytics API](https://developers.google.com/youtube/analytics/reference?hl=zh-tw) 提取資料。YouTube 產生的 Reporting API 數據應視為最終數據，而 YouTube 數據分析資訊主頁/API 顯示的數據則應視為預估數據。這兩個 API 之間出現一定程度的差異，這是意料之中的事情。
:   **解決方法：**如果報告中的數字確實有誤，YouTube 系統和 BigQuery 資料移轉服務 YouTube 移轉作業都會設定為回填缺少的數字，並在回填日期的全新報告中提供這些數字。由於 BigQuery 資料移轉服務的 YouTube 設定會載入 YouTube Reporting API 建立的所有可用報表，因此 BigQuery 移轉作業自動匯入日後產生的 YouTube 報表時，也會將新產生和更新的資料納入考量，並將資料擷取至正確的日期分割資料表。

    **注意：** YouTube 數據分析會在當天結束後最多 24 到 48 小時內提供當天的 YouTube 資料 (有時會更久)。因此，後續產生的 YouTube 報表和 BigQuery 移轉作業也會延遲。

### YouTube 權限問題

如要移轉 YouTube 內容管理工具報表，設定移轉作業的使用者必須具備`CMS user`權限 (至少)。您必須為要建立轉移作業的每位內容管理員授予「`CMS user`」權限。

## 配額問題

發生錯誤：`Quota exceeded: Your project exceeded quota for imports per project.`
:   **解決方法：**確認專案中排定的轉移作業數量未超出上限。如需計算移轉作業啟動的載入工作數相關資訊，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]