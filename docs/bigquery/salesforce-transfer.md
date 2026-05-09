Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Salesforce 資料載入 BigQuery

您可以使用 Salesforce 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Salesforce Sales Cloud 載入至 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 Salesforce Sales Cloud 的最新資料新增至 BigQuery。

## 限制

Salesforce 資料移轉作業會受到下列限制：

* Salesforce 連接器僅支援從 Salesforce Sales Cloud 轉移資料。
* Salesforce 連接器僅支援 Salesforce Bulk API V1 64.0 版中包含的欄位。系統可能不支援 Salesforce Bulk API 先前版本中的某些欄位。如要進一步瞭解 Salesforce 連接器的這些變更，請參閱「[Salesforce Bulk API](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#salesforce)」。
* Salesforce 連接器會使用 Salesforce Bulk API V1 連線至 Salesforce Sales Cloud 端點，以擷取資料。
  + Salesforce 連接器僅支援 Salesforce Bulk API V1，可連線至 Salesforce 執行個體，且僅支援傳輸 Salesforce Bulk API 支援的實體。如要進一步瞭解支援的實體，請參閱「[『Entity is not supported by the Bulk API』錯誤](https://help.salesforce.com/s/articleView?id=000383508&type=1)」。
* Salesforce 連接器不支援轉移含有二進位欄位的下列物件：
  + `Attachment`
  + `ContentVersion`
  + `Document`
  + `StaticResource`
  + `Scontrol`
  + `EmailCapture`
  + `MailMergeTemplate`
* 週期性資料轉移作業之間的最短時間間隔為 15 分鐘。重複轉移的預設間隔為 24 小時。
* 由於 Salesforce 處理限制，一次排定過多資料轉移作業可能會導致延遲或失敗。建議您將 Salesforce 資料傳輸限制為下列項目：
  + 每個移轉設定最多只能有 10 項資產。
  + 在不同的轉移設定中，最多可同時執行 10 項轉移作業。
* 單一移轉設定在特定時間只能支援一次資料移轉作業。如果排定在第一次資料移轉完成前執行第二次資料移轉，則系統只會完成第一次資料移轉，並略過任何與第一次移轉重疊的資料移轉。
  + 為避免在單一轉移設定中略過轉移作業，建議您設定「重複頻率」，增加大型資料轉移作業之間的時間間隔。
* 如果資料移轉作業使用網路連結，請務必[設定具有靜態 IP 位址的公用網路位址轉譯 (NAT)](https://docs.cloud.google.com/nat/docs/set-up-manage-network-address-translation?hl=zh-tw)。詳情請參閱「[為 Salesforce 移轉作業設定 IP 許可清單](#salesforce-allowlist)」一文。
* 如果設定的網路連結和虛擬機器 (VM) 執行個體位於不同區域，從 Salesforce 轉移資料時，可能會發生跨區域資料移動。

### 增量移轉限制

增量 Salesforce 轉移作業有下列限制：

* 浮水印欄只能選擇 `TIMESTAMP` 欄。
* 只有含有有效浮水印欄的資產，才支援增量擷取。
* 浮水印資料欄中的值必須單調遞增。
* 增量轉移作業無法同步處理來源資料表中的刪除作業。
* 單一轉移設定只能支援增量或完整擷取。
* 第一次執行增量擷取後，就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取後，就無法在轉移設定中變更寫入模式。
* 第一次執行遞增式擷取後，就無法變更時間戳記欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的主鍵叢集，並受[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)約束。
* 首次將現有轉移設定更新為增量擷取模式時，更新後的第一次資料移轉作業會移轉資料來源中的所有可用資料。後續的增量資料轉移作業只會轉移資料來源中的新資料列和更新資料列。

## 資料擷取選項

以下各節提供設定 Salesforce 資料移轉時，資料擷取選項的詳細資訊。

### 完整或累加轉移

[設定 Salesforce 移轉作業](#sf-transfer-setup)時，您可以在移轉設定中選取「完整」或「增量」寫入偏好設定，指定資料載入 BigQuery 的方式。[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量轉移。

**注意：** 如要索取有關增量移轉的意見回饋或支援，請傳送電子郵件至 [dts-preview-support@google.com](mailto:dts-preview-support@google.com)。
您可以設定*完整*資料移轉，在每次資料移轉時，移轉 Salesforce 資料集的所有資料。

或者，您也可以設定*增量*資料移轉作業 ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，只移轉上次資料移轉後變更的資料，而不是在每次資料移轉時載入整個資料集。如果為資料移轉作業選取「增量」**Incremental**，則必須指定「附加」**Append**或「插入或更新」**Upsert**寫入模式，定義在增量資料移轉期間，資料如何寫入 BigQuery。以下各節說明可用的寫入模式。

#### 附加寫入模式

附加寫入模式只會將新資料列插入目的地資料表。這個選項會嚴格附加移轉的資料，不會檢查現有記錄，因此這個模式可能會導致目的地資料表中的資料重複。

選取附加模式時，必須選取浮水印欄。Salesforce 連接器必須使用浮水印資料欄，才能追蹤來源資料表中的變更。

選取只在建立記錄時更新的水印資料欄，且不會隨著後續更新而變更。例如「`CreatedDate`」欄。

#### Upsert 寫入模式

新增或更新寫入模式會檢查主鍵，以更新資料列或在目的地資料表中插入新的資料列。您可以指定主鍵，讓 Salesforce 連接器判斷需要哪些變更，才能讓目的地資料表與來源資料表保持同步。如果在資料移轉期間，指定的主鍵出現在目標 BigQuery 資料表中，Salesforce 連接器就會使用來源資料表中的新資料更新該資料列。如果資料移轉期間沒有主鍵，Salesforce 連接器就會插入新列。

選取「新增或更新」模式時，必須選取浮水印欄和主鍵：

\* Salesforce 連接器必須有浮水印資料欄，才能追蹤來源表格的變更。
\* 選取每次修改資料列時都會更新的水印欄。建議使用 `SystemModstamp` 或 `LastModifiedDate` 欄。

* 主鍵可以是資料表中的一或多個資料欄，Salesforce 連接器必須使用這些資料欄，判斷是否需要插入或更新資料列。

  選取包含非空值的資料欄，這些值在資料表的所有資料列中都是不重複的。建議您使用包含系統產生 ID、專屬參照代碼 (例如自動遞增 ID) 或不可變動的時間序列 ID 的資料欄。

  為避免資料遺失或損毀，您選取的主鍵資料欄必須具有不重複的值。如果您對所選主鍵欄的唯一性有疑慮，建議改用附加寫入模式。

### 增量擷取行為

在資料來源中變更資料表結構定義時，這些資料表的增量資料移轉作業會以以下方式反映在 BigQuery 中：

| 資料來源異動 | 增量擷取行為 |
| --- | --- |
| 新增資料欄 | 目的地 BigQuery 資料表會新增資料欄。 這個資料欄的所有先前記錄都會有空值。 |
| 刪除資料欄 | 刪除的資料欄仍會保留在目的地 BigQuery 資料表中。系統會在新項目中填入空值。 |
| 變更資料欄中的資料類型 | 連接器僅支援 `ALTER COLUMN` DDL 陳述式支援的資料類型轉換。如果轉換成其他資料類型，資料移轉作業就會失敗。 如果遇到任何問題，建議建立新的轉移設定。 |
| 重新命名資料欄 | 原始資料欄會保留在目的地 BigQuery 資料表中，而目的地資料表會新增一個名稱更新的資料欄。 |

## 事前準備

下列各節說明建立 Salesforce 資料移轉作業前必須採取的步驟。

### 建立 Salesforce 連結的應用程式

您必須[建立 Salesforce 連線的應用程式](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5)，並完成下列必要設定：

* [在連結的應用程式中設定基本資訊](https://help.salesforce.com/s/articleView?id=sf.connected_app_create_basics.htm&type=5)。Salesforce 轉移作業需要「連結的應用程式名稱」和「聯絡人電子郵件地址」欄位。
* [啟用 OAuth 設定](https://help.salesforce.com/s/articleView?id=sf.connected_app_create_api_integration.htm&type=5)
  並進行下列設定：
  + 勾選「Enable OAuth Settings」核取方塊。
  + 在「Callback URL」(回呼網址) 欄位中，輸入下列內容：
    - 如果是正式環境，請輸入 `https://login.salesforce.com/services/oauth2/token`。
    - 如果是沙箱環境，請輸入 `https://test.salesforce.com/services/oauth2/token`。
  + 確認未選取「為具名使用者核發以 JSON Web Token(JWT) 為基礎的存取權杖」核取方塊。
* 在「Selected OAuth Scopes」部分，選取「Manage 使用者資料 via APIs (api)」。
* 取消勾選「Required Proof Key for Code Exchange (PKCE) Extension for Supported Authorization Flows」(支援的授權流程必須使用程式碼交換金鑰證明 (PKCE) 擴充功能) 核取方塊。
* 選取「Enable Client Credentials Flow」，然後按一下顯示的通知訊息中的「OK」。

設定連結的應用程式並完成必要設定後，請按一下「儲存」。系統會將您重新導向至新建立的「已連結應用程式」詳細資料頁面。

建立連結的應用程式後，您也必須設定用戶端憑證流程，方法如下：

1. 點選 [設定]。
2. 在搜尋列中搜尋「已連結的應用程式」。
3. 依序點選「管理應用程式」>「已連結的應用程式」。如果您使用 Salesforce Lightning Experience，請按一下「管理連結的應用程式」。
4. 在您建立的已連線應用程式上，按一下「編輯」。
5. 「應用程式詳細資料」頁面隨即顯示。在「Client Credentials Flow」(用戶端憑證流程) 部分，於「Run As」(以...身分執行) 欄位中輸入使用者名稱。您可以使用這個欄位的尋找工具，確保選取的使用者正確無誤。
6. 按一下 [儲存]。

### 必要的 Salesforce 資訊

建立 Salesforce 資料移轉作業時，您必須提供下列 Salesforce 資訊：

| 參數名稱 | 說明 |
| --- | --- |
| `myDomain` | Salesforce 中的「我的網域」。 |
| `clientId` | Salesforce 連結應用程式的消費者金鑰。 |
| `clientSecret` | Salesforce 連結應用程式的 OAuth 用戶端密鑰或消費者密鑰。 |

如要取得 `myDomain`、`clientID` 和 `clientSecret` 值，請選取下列任一選項：

### Salesforce Classic

### 擷取「`myDomain`」詳細資料

如要找出 `myDomain`，請按照下列步驟操作：

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「*我的網域*」。
4. 在搜尋結果中，依序點選「網域管理」>「我的網域」。

在「我的網域詳細資料」部分中，`myDomain` 會顯示為「目前的我的網域 URL」的前置字元。舉例來說，如果「我的網域」網址為 `example.my.salesforce.com`，則要使用的 `myDomain` 值為 `example`。

### 擷取 `ClientId` 和 `ClientSecret` 詳細資料

如要找出 `ClientId` 和 `ClientSecret` 值，請按照下列步驟操作：

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「應用程式」。
4. 在搜尋結果的「建構」部分，依序點選「建立」>「應用程式」。
5. 按一下「已連結的應用程式名稱」。
6. 在「連結的應用程式」詳細資料頁面，按一下「管理取用者詳細資料」。
7. 使用其中一種已註冊的方法驗證身分。您最多可以查看消費者詳細資料頁面五分鐘，之後系統會提示您再次驗證身分。
8. 在「消費者詳細資料」頁面中，「消費者金鑰」就是你的 `ClientId`
   值。「客戶密鑰」是您的 `ClientSecret` 值。

### Salesforce Lightning Experience

### 擷取「`myDomain`」詳細資料

如要找出 `myDomain`，請按照下列步驟操作：

1. 登入 Salesforce 平台。
2. 點選 [設定]。

1. 在搜尋列中搜尋「*我的網域*」。
2. 在搜尋結果中，依序點選「公司設定」>「我的網域」。

在「我的網域詳細資料」部分中，`myDomain` 會顯示為「目前的我的網域 URL」的前置字元。舉例來說，如果「我的網域」網址為 `example.my.salesforce.com`，則要使用的 `myDomain` 值為 `example`。

### 擷取 `ClientId` 和 `ClientSecret` 詳細資料

1. 登入 Salesforce 平台。
2. 點選 [設定]。
3. 在搜尋列中搜尋「應用程式」。
4. 在搜尋結果中，依序點選「應用程式」>「應用程式管理工具」。
5. 找出已連結的應用程式，然後按一下「查看」。
6. 按一下「管理取用者詳細資料」。
7. 使用其中一種已註冊的方法驗證身分。您最多可以查看消費者詳細資料頁面五分鐘，之後系統會提示您再次驗證身分。
8. 在「消費者詳細資料」頁面中，「消費者金鑰」就是你的 `ClientId`
   值。「客戶密鑰」是您的 `ClientSecret` 值。

### 為 Salesforce 移轉作業設定 IP 許可清單

您必須設定 Google Cloud 環境和 Salesforce 帳戶，才能將特定 IP 位址加入資料傳輸許可清單。這樣可確保 Salesforce 只會接受來自可信任靜態 IP 位址的連線。如果您在資料傳輸時使用網路附件，就必須執行這個步驟。

如要這麼做，您必須先設定 Google Cloud 網路，使其使用靜態 IP 位址：

1. 在虛擬私有雲網路中，[設定具有靜態 IP 位址的公用網路位址轉譯 (NAT)](https://docs.cloud.google.com/nat/docs/set-up-manage-network-address-translation?hl=zh-tw)。Cloud NAT 必須在與資料移轉目的地資料集相同的區域內設定。
2. [在同一個虛擬私有雲網路中設定網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)。BigQuery 資料移轉服務會使用這項資源存取私人服務。

接著，您必須[在 Salesforce 中設定信任的 IP 範圍](https://help.salesforce.com/s/articleView?id=xcloud.security_networkaccess.htm&type=5)。
新增 IP 位址範圍時，請使用Google Cloud 公開 NAT 的靜態 IP 位址，做為 IP 範圍的起始和結束 IP 位址。

**注意：** 如要更精細地控管，可以在設定檔層級或每個 API 呼叫中套用 IP 限制。詳情請參閱「[限制設定檔中的登入 IP 位址](https://help.salesforce.com/s/articleView?id=platform.login_ip_ranges.htm&type=5)」一文。

設定 IP 範圍後，您現在可以在[設定轉移設定](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw#sfmc-transfer-setup)時，透過在「網路附件」欄位中選取網路附件，指定靜態 IP。

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

## 設定 Salesforce 資料移轉作業

如要將 Salesforce 資料新增至 BigQuery，請使用下列任一選項設定移轉設定：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Salesforce」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分，從清單中選取網路連結。您必須[設定 Public NAT 並設定 IP 允許清單](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#salesforce-allowlist)，才能使用網路附件進行這項資料轉移作業。
   * 在「My Domain」(我的網域)，輸入您的 Salesforce [My Domain](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm)。
   * 在「Client ID」(用戶端 ID)，輸入與 Salesforce 連結的應用程式用戶端金鑰。
   * 在「Client secret」(用戶端密鑰)，輸入與 Salesforce 連結的應用程式用戶端密鑰。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果選取「Incremental」(增量) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請在「Write mode」(寫入模式) 中選取「Append」(附加) 或「Upsert」(新增或更新)。如要進一步瞭解不同的寫入模式，請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#full_or_incremental_transfers)」一節的說明。
   * 在「Salesforce objects to transfer」(要移轉的 Salesforce 物件) 部分點選「Browse」(瀏覽)：
     + 選取要轉移至 BigQuery 目的地資料集的所有物件。您也可以在這個欄位手動輸入要移轉資料的物件。
     + 如果選取「Append」(附加) 做為增量寫入模式，就必須選取一個欄做為浮水印欄。
     + 如果已選取「Upsert」(新增或更新) 做為增量寫入模式，則必須選取一個欄做為浮水印欄，然後選取一或多個欄做為主鍵。
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

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)
並加上移轉建立標記
`--transfer_config`：

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
  如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 - `salesforce`。
* NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 Salesforce 資料移轉的參數：

  + `connector.authentication.oauth.clientId`：Salesforce 連結應用程式的消費者金鑰。
  + `connector.authentication.oauth.clientSecret`：Salesforce 連線應用程式的 OAuth 用戶端密鑰或消費者密鑰。
  + `connector.authentication.oauth.myDomain`：[Salesforce 我的網域](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm)。
    舉例來說，如果網域網址為 `example.my.salesforce.com`，則值為 `example`。
  + `ingestionType`：指定 `full` 或 `incremental`。[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量轉移。詳情請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer?hl=zh-tw#full_or_incremental_transfers)」。
  + `writeMode`：指定 `WRITE_MODE_APPEND` 或 `WRITE_MODE_UPSERT`。
  + `watermarkColumns`：將資料表中的資料欄指定為浮水印資料欄。如要進行增量轉移，這個欄位為必填。
  + `primaryKeys`：將資料表中的資料欄指定為主鍵。
    如要進行增量轉移，這個欄位為必填。
  + `assets`：要移轉至 BigQuery 的 Salesforce 物件路徑。

在增量轉移期間指定多項資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。在下列範例中，`Id` 對應於資料表 `Account`，而 `master_label` 和 `type` 則對應於資料表 `CaseHistory`。

```
      "primaryKeys":[['Id'], ['master_label','type']],
      "assets":["Account","CaseHistory"],
```

下列指令會在預設專案中建立 Salesforce 增量資料移轉作業，並使用 `APPEND` 寫入模式。

```
bq mk
    --transfer_config
    --target_dataset=mydataset
    --data_source=salesforce
    --display_name='My Transfer'
    --params='{"assets": ["Account", "CaseHistory"]
        "connector.authentication.oauth.clientId": "1234567890",
        "connector.authentication.oauth.clientSecret":"ABC12345",
        "connector.authentication.oauth.myDomain":"MyDomainName",
        "connector.authentication.username":"user1@force.com",
        "connector.authentication.password":"abcdef1234",
        "ingestionType":"incremental",
        "writeMode":"WRITE_MODE_UPSERT",
        "watermarkColumns":["SystemModstamp","CreatedDate"]
        "primaryKeys":[['Id'], ['master_label','type']]}'
```

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

儲存移轉設定後，Salesforce 連接器會根據排程選項自動觸發移轉作業。每次執行移轉作業時，Salesforce 連接器都會將 Salesforce 中的所有可用資料移轉至 BigQuery。

如要在正常排程以外手動執行資料移轉作業，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

下表列出 Salesforce 資料類型對應的 BigQuery 資料類型：

| Salesforce 資料類型 | BigQuery 資料類型 |
| --- | --- |
| `_bool` | `BOOLEAN` |
| `_int` | `INTEGER` |
| `_long` | `INTEGER` |
| `_double` | `FLOAT` |
| `currency` | `FLOAT` |
| `percent` | `FLOAT` |
| `geolocation (latitude)` | `FLOAT` |
| `geolocation (longitude)` | `FLOAT` |
| `date` | `DATE` |
| `datetime` | `TIMESTAMP` |
| `time` | `TIME` |
| `picklist` | `STRING` |
| `multipicklist` | `STRING` |
| `combobox` | `STRING` |
| `reference` | `STRING` |
| `base64` | `STRING` |
| `textarea` | `STRING` |
| `phone` | `STRING` |
| `id` | `STRING` |
| `url` | `STRING` |
| `email` | `STRING` |
| `encryptedstring` | `STRING` |
| `datacategorygroupreference` | `STRING` |
| `location` | `STRING` |
| `address` | `STRING` |
| `anyType` | `STRING` |

## 定價

如要瞭解 Salesforce 轉移作業的定價資訊，請參閱[資料移轉服務定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)。

## 排解轉移設定問題

如果您無法順利設定資料移轉作業，請參閱「[Salesforce 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#salesforce-issues)」。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱「[BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)」。
* 如要瞭解如何使用移轉作業，包括取得移轉設定、列出移轉設定以及查看移轉設定的執行記錄，請參閱[使用移轉功能](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)一文。
* 瞭解如何[透過跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]