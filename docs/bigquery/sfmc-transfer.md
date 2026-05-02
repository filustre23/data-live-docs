* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Salesforce Marketing Cloud 資料載入 BigQuery

您可以使用 Salesforce Marketing Cloud 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Salesforce Marketing Cloud 載入至 BigQuery。透過 BigQuery 資料移轉服務，您可以排定週期性移轉工作，將 Salesforce Marketing Cloud 的最新資料新增至 BigQuery。

## 限制

Salesforce Marketing Cloud 資料移轉作業會受到下列限制：

* 單一移轉設定在特定時間只能支援一次資料移轉作業。如果排定在第一次資料移轉完成前執行第二次資料移轉，則只有第一次資料移轉會完成，任何與第一次移轉重疊的資料移轉都會略過。
  + 為避免在單一轉移設定中略過轉移作業，建議您設定「重複頻率」，增加大型資料轉移作業之間的時間間隔。
* 如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)。
* 如果設定的網路連結和虛擬機器 (VM) 執行個體位於不同區域，從 Salesforce Marketing Cloud 轉移資料時，可能會發生跨區域資料移動。

## 事前準備

下列各節說明建立 Salesforce Marketing Cloud 資料轉移作業前，您需要採取的步驟。

### Salesforce Marketing Cloud 必要條件

建立 Salesforce Marketing Cloud 資料轉移作業時，您必須提供下列資訊：

| 參數名稱 | 說明 |
| --- | --- |
| `subdomain` | API 子網域 (位於基本 URI 中)。舉例來說，在驗證基本 URI `https://SUBDOMAIN.auth.marketingcloudapis.com/` 中，SUBDOMAIN 是您的子網域值。 |
| `instance` | API 伺服器執行個體，登入 Salesforce Marketing Cloud 應用程式後，即可在網址中找到。執行個體值包含 `s`，後面接著數值。舉例來說，在網址 `https://mc.s4.exacttarget.com/` 中，執行個體值為 `s4`。詳情請參閱「[尋找 Marketing Cloud 帳戶的堆疊位置](https://help.salesforce.com/s/articleView?id=000383566&type=1)」。 |
| `clientId` | API 整合中的用戶端 ID。依序前往「設定」>「應用程式」>「已安裝的套件」，然後點選套件名稱。用戶端 ID 會列在「元件」下方。 |
| `clientSecret` | 應用程式整合項目的用戶端密鑰。依序前往「設定」>「應用程式」>「已安裝的套件」，然後點選套件名稱。用戶端密鑰會列在「元件」下方。 |
| `Salesforce Marketing Cloud objects to transfer` | 編譯要納入這項轉移作業的 Salesforce Marketing Cloud 物件清單。[設定轉移設定](#sfmc-transfer-setup)時，您可以選取物件。 如需支援的物件清單，請參閱「[支援的表格](#supported-tables)」。 |

#### 為 Salesforce Marketing Cloud 移轉作業設定 IP 許可清單

您必須設定 Google Cloud 環境和 Salesforce Marketing Cloud 帳戶，將特定 IP 位址新增至資料傳輸許可清單。這樣一來，Salesforce Marketing Cloud 就只會接受來自可信任靜態 IP 位址的連線。

如要這麼做，您必須先設定 Google Cloud 網路，使其使用靜態 IP 位址：

1. 在虛擬私有雲網路中，[設定具有靜態 IP 位址的公用網路位址轉譯 (NAT)](https://docs.cloud.google.com/nat/docs/set-up-manage-network-address-translation?hl=zh-tw)。Cloud NAT 必須在與資料移轉目的地資料集相同的區域內設定。
2. [在同一個虛擬私有雲網路中設定網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)。BigQuery 資料移轉服務會使用這項資源存取私人服務。

接著，您必須[將靜態 IP 位址新增至 Salesforce Marketing Cloud 的許可清單](https://help.salesforce.com/s/articleView?id=mktg.mc_overview_allowlist_ip.htm&language=en_US&type=5)。新增 IP 位址範圍時，請使用Google Cloud 公開 NAT 的靜態 IP 位址，做為 IP 範圍的起始和結束 IP 位址。

設定 IP 範圍後，您現在可以在[設定轉移設定](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw#sfmc-transfer-setup)時，透過在「網路附件」欄位中選取網路附件，指定靜態 IP。

#### 資料延伸模組物件規定

如要在資料轉移中加入資料擴充物件，該物件必須符合下列規定：

* 資料擴充物件的名稱必須包含 `DataExtensionObject` 前置字元，後面接著物件名稱。例如：`DataExtensionObject_DATA_EXTENSION_NAME`。
* 您必須為資料擴充物件啟用 `Read` 範圍。
* 資料擴充物件的檔案位置必須具有 `Read` 和 `Write` 範圍。

### 安裝及設定 Salesforce Marketing Cloud API 整合套件

您必須在 Salesforce Marketing Cloud 中安裝伺服器對伺服器 API 整合套件。如要在 Salesforce Marketing Cloud 中執行這項操作，請安裝新的已安裝套件，並指定「API 整合」>「伺服器對伺服器」元件。詳情請參閱「[建立及安裝套件](https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/install-packages.html)」。

安裝 API 整合套件後，您必須新增下列權限範圍：

* 存取權：`Offline Access`
* 電子郵件：`Read`
* OTT：`Read`
* 推送：`Read`
* 簡訊：`Read`
* 網頁：`Read`
* 文件和圖片：`Read`
* 已儲存的內容：`Read`
* 旅程：`Read`
* 目標對象：`Read`
* 名單和訂閱者：`Read`
* 日期擴充功能：`Read`
* 檔案位置 `Read`
* 追蹤事件：`Read`
* 回呼：`Read`
* 訂閱項目：`Read`
* 廣告活動：`Read`
* 資產：`Read`
* 帳戶：`Read`
* OTT 頻道：`Read`
* 使用者：`Read`

詳情請參閱「[API 整合權限範圍](https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/data-access-permissions.html)」。

### BigQuery 必要條件

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求系統管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 BigQuery 資料移轉服務資料移轉作業，您必須具備下列權限：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

## 設定 Salesforce Marketing Cloud 資料轉移作業

如要將 Salesforce Marketing Cloud 資料新增至 BigQuery，請使用下列任一方法設定移轉作業：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Salesforce Marketing Cloud」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分，從選單中選取網路連結。如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)。
   * 在「API Subdomain」(API 子網域) 部分，輸入[驗證基本 URI 的子網域](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw#sfmc-prereqs)。
   * 在「API instance」(API 執行個體) 部分，輸入[網址中的 API 執行個體](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw#sfmc-prereqs)，這在登入 Marketing Cloud 應用程式後即可查看。
   * 在「Client ID」(用戶端 ID) 部分，輸入 [API 整合套件中的用戶端 ID](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw#sfmc-prereqs)。
   * 在「Client Secret」(用戶端密鑰) 部分，輸入 [API 整合套件中的用戶端密鑰](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw#sfmc-prereqs)。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 如要針對這項移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-transfer-config)，並提供移轉建立標記 `--transfer_config`。

```
bq mk
    --transfer_config
    --project_id=PROJECT_ID
    --data_source=DATA_SOURCE
    --display_name=DISPLAY_NAME
    --target_dataset=DATASET
    --params='PARAMETERS'
```

更改下列內容：

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。
  如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 (例如 `saphana`)。
* DISPLAY\_NAME：移轉設定的顯示名稱。資料移轉名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 Salesforce Marketing Cloud 轉移作業的參數：
  + `connector.subdomain`：API 子網域。
  + `connector.instance`：API 執行個體值。
  + `connector.authentication.oauth.clientId`：OAuth 用戶端的應用程式 ID 名稱。
  + `connector.authentication.oauth.clientSecret`：OAuth 用戶端的應用程式密鑰。
  + `assets`：要從 Salesforce Marketing Cloud 移轉的 Salesforce Marketing Cloud 資料表名稱清單。

舉例來說，下列指令會在預設專案中建立 Salesforce Marketing Cloud 資料移轉作業，並設定所有必要參數：

```
  bq mk
      --transfer_config
      --target_dataset=mydataset
      --data_source=salesforce_marketing
      --display_name='My Transfer'
      --params='{"connector.subdomain": "abcd",
      "connector.instance": "x",
      "connector.authentication.oauth.clientId": "1234567890",
      "connector.authentication.oauth.clientSecret":"ABC12345"}'
```

### API

請使用 [`projects.locations.transferConfigs.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw)，並提供 [`TransferConfig` 資源的執行個體](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)。

儲存轉移設定後，Salesforce Marketing Cloud 連接器會根據排程選項，自動觸發轉移作業。

### 支援的資料表

每次執行移轉作業時，Salesforce Marketing Cloud 連接器都會根據 REST 介面，將 Salesforce Marketing Cloud 中的所有可用資料移轉至 BigQuery 的下列資料表：

* `Assets`
* `CampaignAssets`
* `Campaigns`
* `Categories`
* `EventDefinitions`
* `FacebookMessengerProperties`
* `JourneyActivities`
* `Journeys`
* `LineMessengerProperties`
* `SendDefinitions`
* `Subscriptions`
* `DataExtension`
* `DataExtensionObject_DATA_EXTENSION_NAME`
* `Email`
* `LinkSend`
* `List`
* `ListSubscriber`
* `Subscriber`
* `TriggeredSendDefinition`

如要在正常時間表以外手動執行資料移轉作業，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

下表列出 Salesforce Marketing Cloud 資料類型與對應的 BigQuery 資料類型。

| Salesforce Marketing Cloud 資料類型 | BigQuery 資料類型 |
| --- | --- |
| `Boolean` | `BOOLEAN` |
| `Number` | `INTEGER` |
| `Text` | `STRING` |
| `Decimal` | `FLOAT` |
| `EmailAddress` | `STRING` |
| `Phone` | `STRING` |
| `Date` | `DATE` |
| `DateTime` | `TIMESTAMP` |
| `Locale` | `STRING` |

## 排解轉移設定問題

如果無法順利設定 Salesforce Marketing Cloud 資料移轉作業，請嘗試下列疑難排解步驟：

* 確認[為 API 整合套件設定的驗證](#sfmc-prereqs)已設為「伺服器對伺服器」。
* 確認驗證應用程式已在「範圍」下方設定[必要權限](https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/data-access-permissions.html)。

### 錯誤訊息

發生錯誤：`invalid_grant. The client's IP address is unauthorized for this account. Allowlist the client's IP address in Marketing Cloud Administration.`
:   **解決方法：**請嘗試下列任一步驟：

    * 為[資源啟用所有可用的 IP 位址 Google Cloud](https://www.gstatic.com/ipranges/goog.json) 。
    * 設定 Google Cloud 環境和 Salesforce Marketing Cloud 帳戶
      ，將靜態 IP 位址新增至許可清單。詳情請參閱「[為 Salesforce Marketing Cloud 移轉作業設定 IP 許可清單](#sfmc-allowlist)」一文。

發生錯誤：`INVALID_ARGUMENT. Table tableName does not exist in asset TableName`
:   **解決方法：**請確認您已在 Salesforce Marketing Cloud 應用程式中設定正確的範圍權限。詳情請參閱 [Salesforce Marketing Cloud 必要條件](#sfmc-prereqs)。

發生錯誤：`FAILED_PRECONDITION: There was an issue connecting to API.`
:   **解決方法：**如果您在轉移作業中加入網路附件，但未設定 Public NAT 並設定 IP 允許清單，就可能發生這個錯誤。如要解決這項錯誤，請按照「[建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw#create_a_network_attachment)」一文中的步驟操作，定義靜態 IP 位址來建立網路連結。

## 定價

如要瞭解 Salesforce Marketing Cloud 移轉作業的定價資訊，請參閱「[資料移轉服務定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bqdts)」。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱「[BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)」。
* 如要瞭解如何使用資料移轉作業，包括取得移轉設定、列出移轉設定以及查看移轉設定的執行記錄，請參閱「[管理移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)」一文。
* 瞭解如何[透過跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]