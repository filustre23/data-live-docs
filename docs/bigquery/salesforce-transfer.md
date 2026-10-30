Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Salesforce 資料載入 BigQuery

如要安排從 Salesforce Sales Cloud 到 BigQuery 的週期性資料移轉作業，請建立移轉設定，指定要移轉的資料物件，以及資料移轉作業的排程頻率。您可以使用 Google Cloud 控制台、`bq`指令列工具或 BigQuery 資料移轉服務 API 建立移轉設定。設定移轉設定後，[BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)會按照指定的時間表，將最新資料移轉至 BigQuery 資料表。

如要瞭解 Salesforce 移轉作業的運作方式，請參閱「[Salesforce 資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer-intro?hl=zh-tw)」。

## 限制

Salesforce 資料移轉作業有下列限制：

* Salesforce 連接器僅支援從 Salesforce Sales Cloud 移轉資料。
* Salesforce 連接器僅支援 Salesforce Bulk API V1 64.0 版中的欄位。系統可能不支援 Salesforce Bulk API 舊版中的某些欄位。如要進一步瞭解 Salesforce 連接器的這些異動，請參閱「[Salesforce Bulk API](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#salesforce)」。
* Salesforce 連接器會使用 Salesforce Bulk API V1 連線至 Salesforce Sales Cloud 端點，以擷取資料。

  + Salesforce 連接器僅支援 Salesforce Bulk API V1，用於連線至 Salesforce 執行個體，且僅支援傳輸 Salesforce Bulk API 支援的實體。如要進一步瞭解支援的實體，請參閱「[大量 API 不支援實體](https://help.salesforce.com/s/articleView?id=000383508&type=1)」。
* Salesforce 連接器不支援轉移下列含有二進位欄位的物件。

  + `Attachment`
  + `ContentVersion`
  + `Document`
  + `StaticResource`
  + `Scontrol`
  + `EmailCapture`
  + `MailMergeTemplate`
* 週期性資料移轉作業之間的最短間隔時間為 15 分鐘。週期性移轉作業的預設間隔為 24 小時。
* 由於 Salesforce 的處理限制，一次排定太多資料移轉作業可能會導致延遲或失敗。建議您將 Salesforce 資料移轉作業限制在下列範圍：

  + 每項移轉設定最多只能有 10 項資產。
  + 在不同的移轉設定中，一次最多只能同時執行 10 項移轉作業。
* 單一移轉設定在特定時間只能支援一項資料移轉作業。如果第二項資料移轉作業排定在第一項移轉作業完成前執行，則只有第一項資料移轉作業會完成，而與第一項移轉作業重疊的其他資料移轉作業則會略過。

  + 為避免單一移轉設定略過移轉作業，建議您設定「重複頻率」，增加大型資料移轉作業之間的時間長度。
* 如要透過網路連結移轉資料，請務必[設定公開網路位址轉譯 (NAT)](https://docs.cloud.google.com/nat/docs/set-up-manage-network-address-translation?hl=zh-tw)，並指定靜態 IP 位址。詳情請參閱「[為 Salesforce 移轉作業設定 IP 許可清單](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#salesforce-allowlist)」一文。
* 如果設定的網路連結和虛擬機器 (VM) 執行個體位於不同區域，從 Salesforce 移轉資料時，可能會發生跨區域資料移動。

### 增量移轉作業限制

Salesforce 遞增移轉作業有下列限制：

* 最多只能選擇 `TIMESTAMP` 個資料欄做為浮水印欄。
* 只有具備有效浮水印資料欄的資產，才支援增量擷取。
* 基準欄中的值必須單調遞增。
* 增量移轉作業無法同步處理來源資料表中的刪除作業。
* 單一移轉設定只能支援增量或完整擷取。
* 首次執行增量擷取後，您就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取後，您就無法變更移轉設定中的寫入模式。
* 首次執行增量擷取後，就無法變更基準值資料欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的主鍵進行分群，並受[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)規範。
* 首次將現有移轉設定更新為增量擷取模式時，更新後的第一次資料移轉會從資料來源移轉所有可用資料。後續的任何增量資料移轉作業，都只會從資料來源移轉新的和更新的資料列。

如要瞭解增量移轉作業的運作方式，請參閱「[完整或增量移轉作業](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer-intro?hl=zh-tw#full-incremental-transfers)」。

## 事前準備

以下各節說明建立 Salesforce 資料移轉作業前，必須採取的步驟。

### 建立 Salesforce 連結應用程式

您必須[建立 Salesforce 連結應用程式](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5)，並完成下列必要設定：

* 在連結的應用程式中[設定基本資訊](https://help.salesforce.com/s/articleView?id=sf.connected_app_create_basics.htm&type=5)。如要轉移 Salesforce 資料，必須填寫「Connected App Name」(連結的應用程式名稱) 和「Contact Email」(聯絡電子郵件地址) 欄位。
* [啟用 OAuth 設定](https://help.salesforce.com/s/articleView?id=sf.connected_app_create_api_integration.htm&type=5)，並進行下列設定：
  + 勾選「Enable OAuth Settings」核取方塊。
  + 在「Callback URL」(回呼網址) 欄位中，輸入下列內容：
    - 如果是正式環境，請輸入 `https://login.salesforce.com/services/oauth2/token`。
    - 如果是沙箱環境，請輸入 `https://test.salesforce.com/services/oauth2/token`。
  + 確認未勾選「Issue JSON Web Token (JWT)-based access tokens for named users」(為指定使用者核發以 JSON Web Token (JWT) 為基礎的存取權杖) 核取方塊。
* 在「Selected OAuth Scopes」(選取的 OAuth 範圍) 部分，選取「Manage user data via APIs (api)」(透過 API 管理使用者資料 (api))。
* 選取「Enable Client Credentials Flow」，然後在顯示的通知中按一下「OK」。

完成必要設定後，按一下「Save」(儲存)。系統會將您重新導向至新建立的連結應用程式詳細資料頁面。

建立連結的應用程式後，您也必須按照下列步驟設定用戶端憑證流程：

1. 點選 [設定]。
2. 在搜尋列中搜尋「Connected Apps」。
3. 依序按一下「管理應用程式」>「已連結的應用程式」。如果您使用的是 Salesforce Lightning Experience，請按一下「Manage Connected Apps」(管理連結的應用程式)。
4. 在您建立的連結應用程式上，按一下「Edit」。
5. 「App details」(應用程式詳細資料) 頁面隨即顯示。在「Client Credentials Flow」(用戶端憑證流程) 部分，於「Run As」(執行身分) 欄位輸入使用者名稱。您可以使用這個欄位中的尋找工具，確保選取正確的使用者。
6. 按一下「儲存」。

### 必要的 Salesforce 資訊

建立 Salesforce 資料移轉作業時，必須提供下列 Salesforce 資訊：

| 參數名稱 | 說明 |
| --- | --- |
| `myDomain` | Salesforce 的[我的網域](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm)。 |
| `clientId` | Salesforce 連結應用程式的用戶端金鑰。 |
| `clientSecret` | Salesforce 連結應用程式的 OAuth 用戶端密鑰或消費者密鑰。 |

如要取得 `myDomain`、`clientID` 和 `clientSecret` 值，請選取下列其中一個選項：

### Salesforce Classic

### 擷取`myDomain`詳細資料

如要找出 `myDomain`，請按照下列步驟操作：

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「*My Domain*」。
4. 在搜尋結果中，依序點選「網域管理」>「我的網域」。

在「My Domain Details」部分，「Current My Domain URL」的前置字串會顯示 `myDomain`。舉例來說，如果「我的網域」網址是 `example.my.salesforce.com`，則要使用的 `myDomain` 值為 `example`。

### 擷取 `ClientId` 和 `ClientSecret` 詳細資料

如要找出 `ClientId` 和 `ClientSecret` 值，請按照下列步驟操作：

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「應用程式」。
4. 在搜尋結果的「建構」部分，依序點選「建立」>「應用程式」。
5. 按一下「連結的應用程式名稱」。
6. 在「連結的應用程式」詳細資料頁面，點選「管理取用者詳細資料」。
7. 使用其中一種註冊方法驗證身分。您最多可以查看消費者詳細資料頁面五分鐘，之後系統會提示您再次驗證身分。
8. 在「Consumer Details」(消費者詳細資料) 頁面中，「Consumer Key」(用戶端金鑰) 是您的 `ClientId` 值。「Customer Secret」是您的 `ClientSecret` 值。

### Salesforce Lightning Experience

### 擷取`myDomain`詳細資料

如要找出 `myDomain`，請按照下列步驟操作：

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「*My Domain*」。
4. 在搜尋結果中，依序點選「Company Settings」>「My Domain」。

在「My Domain Details」部分，「Current My Domain URL」的前置字串會顯示 `myDomain`。舉例來說，如果「我的網域」網址是 `example.my.salesforce.com`，則要使用的 `myDomain` 值為 `example`。

### 擷取 `ClientId` 和 `ClientSecret` 詳細資料

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「應用程式」。
4. 在搜尋結果中，依序點選「應用程式」>「應用程式管理員」。
5. 找出連結的應用程式，然後按一下「查看」。
6. 按一下「管理取用者詳細資料」。
7. 使用其中一種註冊方法驗證身分。您最多可以查看消費者詳細資料頁面五分鐘，之後系統會提示您再次驗證身分。
8. 在「Consumer Details」(消費者詳細資料) 頁面中，「Consumer Key」(用戶端金鑰) 是您的 `ClientId` 值。「Customer Secret」是您的 `ClientSecret` 值。

### 為 Salesforce 移轉作業設定 IP 許可清單

您必須設定 Google Cloud 環境和 Salesforce 帳戶，將特定 IP 位址加入資料移轉許可清單。這可確保 Salesforce 只接受來自可信任靜態 IP 位址的連線。如果您在移轉資料時使用網路連結，就必須執行這個步驟。

如要這麼做，您必須先設定 Google Cloud 網路，使用靜態 IP 位址：

1. 在虛擬私有雲網路中，[設定公開網路位址轉譯 (NAT)](https://docs.cloud.google.com/nat/docs/set-up-manage-network-address-translation?hl=zh-tw)，並指定靜態 IP 位址。Cloud NAT 必須與這項資料移轉作業的目的地資料集位於相同區域。
2. 在同一個虛擬私有雲網路中[設定網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)。BigQuery 資料移轉服務會使用這項資源存取私人服務。

接下來，您必須[在 Salesforce 中設定信任的 IP 範圍](https://help.salesforce.com/s/articleView?id=xcloud.security_networkaccess.htm&type=5)。新增 IP 位址範圍時，請使用Google Cloud Public NAT 的靜態 IP 位址，做為 IP 範圍的起始和結束 IP 位址。

**注意：** 如要更精細地控管，可以在設定檔層級或每個 API 呼叫套用 IP 限制。詳情請參閱「[限制設定檔中的登入 IP 位址](https://help.salesforce.com/s/articleView?id=platform.login_ip_ranges.htm&type=5)」。

設定 IP 範圍後，您可以在[設定移轉設定](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#sf-transfer-setup)時，於「Network attachment」(網路連結) 欄位中選取網路連結，藉此指定靜態 IP。

### BigQuery 事前準備

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要設定 Pub/Sub 的移轉作業執行通知，請確認您具備 `pubsub.topics.setIamPolicy` Identity and Access Management (IAM) 權限。如果只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立 BigQuery 資料移轉服務資料移轉作業：

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

## 設定 Salesforce 資料移轉作業

使用下列任一選項設定移轉設定，將 Salesforce 資料新增至 BigQuery：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Salesforce」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分，從清單中選取網路連結。您必須[設定 Public NAT 並設定 IP 允許清單](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#salesforce-allowlist)，才能使用網路連結進行這項資料移轉作業。
   * 在「My Domain」(我的網域)，輸入您的 Salesforce [My Domain](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm)。
   * 在「Client ID」(用戶端 ID)，輸入與 Salesforce 連結的應用程式用戶端金鑰。
   * 在「Client secret」(用戶端密鑰)，輸入與 Salesforce 連結的應用程式用戶端密鑰。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果「Write mode」(寫入模式) 選取「Incremental」(增量)，請選取「Append」(附加) 或「Upsert」(新增或更新)。如要進一步瞭解不同的寫入模式，請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer-intro?hl=zh-tw#full-incremental-transfers)」一節。
   * 在「Salesforce objects to transfer」(要移轉的 Salesforce 物件) 部分點選「Browse」(瀏覽)：
     + 選取要轉移至 BigQuery 目的地資料集的所有物件。您也可以在這個欄位手動輸入要移轉資料的物件。
     + 如果選取「Append」(附加) 做為增量寫入模式，就必須選取一個欄做為浮水印欄。
     + 如果選取「Upsert」(新增或更新) 做為增量寫入模式，就必須選取一個欄做為浮水印欄，然後選取一或多個欄做為主鍵。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
7. 在「Schedule options」(排程選項) 專區：

   * 在「Repeat frequency」(重複執行頻率) 清單中，選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 如要針對這項移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並提供移轉作業建立旗標 `--transfer_config`：

```
bq mk
    --transfer_config
    --project_id=PROJECT_ID
    --data_source=DATA_SOURCE
    --display_name=NAME
    --target_dataset=DATASET
    --params='PARAMETERS'
```

其中：

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。
  如未提供 `--project_id` 來指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 - `salesforce`。
* NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：JSON 格式的已建立移轉設定參數。例如：`--params='{"param":"param_value"}'`。以下是 Salesforce 資料移轉作業的參數：

  + `connector.authentication.oauth.clientId`：與 Salesforce 連結的應用程式用戶端金鑰。
  + `connector.authentication.oauth.clientSecret`：Salesforce 連結應用程式的 OAuth 用戶端密鑰或消費者密鑰。
  + `connector.authentication.oauth.myDomain`：[Salesforce My Domain](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm)。舉例來說，如果網域網址是 `example.my.salesforce.com`，則值為 `example`。
  + `ingestionType`：指定 `full` 或 `incremental`。詳情請參閱「[完整或增量移轉](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer-intro?hl=zh-tw#full-incremental-transfers)」。
  + `writeMode`：指定 `WRITE_MODE_APPEND` 或 `WRITE_MODE_UPSERT`。
  + `watermarkColumns`：將資料表中的資料欄指定為浮水印資料欄。如要進行增量移轉，則必須填寫這個欄位。
  + `primaryKeys`：將資料表中的資料欄指定為主鍵。如要進行增量移轉，則必須填寫這個欄位。
  + `assets`：要移轉至 BigQuery 的 Salesforce 物件路徑。

在遞增移轉作業中指定多項資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。在以下範例中，`Id` 對應至資料表 `Account`，而 `master_label` 和 `type` 則對應至資料表 `CaseHistory`。