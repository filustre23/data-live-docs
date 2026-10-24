Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 授權帳戶進行資料移轉

BigQuery 資料移轉服務可讓您驗證及授權使用者帳戶、服務帳戶和服務代理，以便管理移轉設定及執行自動資料移轉作業。為專案帳戶授予必要權限，有助於控管來源資料和目的地資料集的存取權，以及排解常見的權限錯誤。如要瞭解資料來源專屬權限，請參閱各資料來源的移轉說明文件。

## 基本概念

BigQuery 資料移轉服務會自動將各種資料來源的資料移轉至 BigQuery。驗證和授權模型會在控制層和資料層這兩個不同階段運作，並適用於轉移建立者或轉移擁有者這兩類使用者。

### 控制層

控制層代表授權程序中的階段，通過驗證的使用者可在此階段控制及管理移轉設定和執行作業。控制層中的使用者必須具備適當的 Identity and Access Management (IAM) 權限，才能控管及管理移轉設定和執行作業：

* `bigquery.transfers.update` 權限，可讓使用者執行下列操作：
  + 設定資料移轉設定。
  + 管理現有移轉作業，例如更新、停用或刪除移轉作業。
* `bigquery.transfers.get` 權限：可讓使用者監控移轉作業，例如檢查移轉作業狀態，或查看移轉作業記錄和記錄檔。

如果您使用 Google Cloud 控制台或 bq 指令列工具建立移轉作業，也必須具備 `bigquery.transfers.get` 權限。

設定[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)時，不需具備 `bigquery.transfers.update` 權限。詳情請參閱排定查詢的[必要權限](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#required_permissions)。

### 資料層

資料層代表使用者無法直接控制的階段。在資料層中，BigQuery 資料移轉服務能以離線模式執行資料移轉作業，並根據使用者指定的排程自動觸發移轉作業。在資料層中，系統會使用移轉擁有者的憑證存取來源資料，並根據資料來源，使用移轉擁有者的憑證或 BigQuery 資料移轉服務[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)，啟動 BigQuery 工作並將資料寫入目的地資料集。

如要進一步瞭解必要權限，請參閱本指南的下列章節：

* [外部資料來源的讀取權限授權](#read-access-external-data)
* [啟動 BigQuery 工作的授權](#start-bq-jobs)
* [執行 BigQuery 工作並將資料寫入目的地資料集的授權](#execute-bq-jobs)

### 轉移建立者與轉移擁有者

移轉作業建立者是指建立及設定移轉設定的使用者身分。BigQuery 資料移轉服務使用者和移轉作業建立者，可以是使用者帳戶或[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。

移轉作業擁有者是指 BigQuery 資料移轉服務用來授權資料移轉作業 (特別是擷取來源資料) 的使用者身分。如果是[支援服務帳戶的資料來源](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw#data_sources_with_service_account_support)，移轉作業擁有者可以是使用者帳戶或服務帳戶。如果是其他資料來源，轉移作業擁有者必須是使用者帳戶。

轉移作業擁有者和轉移作業建立者可以具有相同的使用者身分，但這並非必要條件。如要將移轉作業擁有者設為移轉作業建立者以外的使用者，有多種方法：

* 建立移轉作業時，如果資料來源支援服務帳戶，您可以將擁有者設為服務帳戶。
* 建立移轉作業後，您可以將擁有權轉移給新的使用者帳戶 (如果資料來源支援服務帳戶，也可以轉移給服務帳戶)，該帳戶必須具備 `bigquery.transfers.update` 和 `bigquery.transfers.get` 權限。[更新憑證](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_credentials)時，必須登入新帳戶。

## 外部資料來源的讀取權限授權

讀取來源資料所需的權限可能因資料來源而異。舉例來說，如要存取 [Google Ads](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#required_permissions)，您必須具備 Google Ads 客戶 ID 的讀取權限。同樣地，[Google Play](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#required_permissions) 也需要 Google Play 管理中心的報表存取權。如要進一步瞭解資料來源專屬的權限，請參閱各資料來源的移轉指南。

視移轉擁有者的身分類型而定，您必須使用不同的授權方法，才能擷取存取權杖來存取來源資料。

### 以服務帳戶身分轉移擁有者

如果使用服務帳戶做為移轉作業擁有者，當您為專案啟用 BigQuery 資料移轉服務 API 時，系統會自動授予必要權限。BigQuery 資料移轉服務會使用[*服務代理*](https://docs.cloud.google.com/iam/docs/service-account-types?hl=zh-tw#service-agents)，取得使用者提供服務帳戶 (移轉作業擁有者) 的存取權杖。

啟用 BigQuery 資料移轉服務 API 時，系統會為專案建立[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)。系統也會授予服務代理 [BigQuery 資料移轉服務代理角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent) (`roles/bigquerydatatransfer.serviceAgent`)，其中包含 `iam.serviceAccounts.getAccessToken` 權限。這項權限可讓 BigQuery 資料移轉服務服務代理，模擬移轉擁有者服務帳戶，擷取存取權杖。

如要進一步瞭解 BigQuery 資料移轉服務服務代理，請參閱「[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)」。如要進一步瞭解如何使用服務帳戶，以及支援服務帳戶的最新資料來源清單，請參閱「[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)」。

**警告：** 請勿從服務代理移除預先定義的角色，BigQuery 資料移轉服務必須具備 [BigQuery 資料移轉服務代理角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)才能運作。

### 以使用者帳戶身分轉移擁有者

如果建立移轉設定的移轉擁有者是使用者帳戶 (而非服務帳戶)，您必須手動授予 BigQuery 資料移轉服務權限，才能取得使用者帳戶的存取權杖，並代表移轉擁有者存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。

只有在首次為特定資料來源建立移轉作業時，才需要授予 BigQuery 資料移轉服務權限。即使使用相同的資料來源，在為新使用的區域建立第一項移轉作業時，仍須再次授予權限。YouTube 頻道資料移轉作業是例外狀況，每次建立 YouTube 頻道資料移轉作業時，都必須手動授予權限核准。

如果新擁有者先前從未在該區域建立資料來源的移轉作業，則透過更新憑證變更移轉擁有者時，也需要手動核准。

下列螢幕截圖顯示建立 Google Ads 移轉作業時的 OAuth 對話方塊介面。對話方塊會顯示要授予的資料來源專屬權限：

**注意：** BigQuery 資料移轉服務不再支援 YouTube 頻道資料移轉作業的 `authorization_code` 參數。您可以使用 `version_info` 參數，將授權結果提供給轉移作業，以便取得憑證。只有在 `bq` CLI 或 API 呼叫中，才需要 `version_info` 參數。

如要撤銷已授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery 資料移轉服務」。
3. 如要撤銷權限，請按一下「移除存取權」。

**警告：** 撤銷存取權限後，這個帳戶在所有區域擁有的移轉設定，日後都無法執行移轉作業。

## 啟動 BigQuery 工作的授權

從大多數資料來源遷移時，除非使用[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或[資料集副本](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#copy-datasets)遷移，否則 BigQuery 資料移轉服務會依賴[服務代理](https://docs.cloud.google.com/iam/docs/service-account-types?hl=zh-tw#service-agents)為專案啟動 BigQuery 工作。為專案啟用 BigQuery 資料移轉服務 API 時，[服務代理](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatatransfer.serviceAgent)會自動取得必要權限 `bigquery.job.create`。詳情請參閱「[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)」。

使用[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或[資料集副本](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#copy-datasets)遷移時，BigQuery 資料移轉服務會使用移轉作業擁有者的憑證啟動 BigQuery 工作。

**警告：** 請勿從服務代理移除預先定義的角色，必須具備服務代理角色，才能使用 BigQuery 資料移轉服務。

## 執行 BigQuery 工作並將資料寫入目的地資料集的授權

從大多數資料來源遷移時，除非使用[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或[資料集副本](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#copy-datasets)遷移，否則 BigQuery 資料移轉服務會依賴服務代理，將資料寫入 BigQuery 目的地資料集。建立移轉作業時，BigQuery 資料移轉服務會將必要權限 `roles/bigquery.dataEditor` 授予服務代理。您必須具備目的地資料集的 `bigquery.datasets.update` 權限，才能成功授予權限。

使用[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或[資料集副本](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#copy-datasets)遷移時，BigQuery 資料移轉服務會使用移轉擁有者的憑證執行 BigQuery 工作，並將資料寫入 BigQuery 目的地資料集。

**注意：** 授予 BigQuery 資料移轉服務代理的 `roles/bigquery.dataEditor` 角色，僅限於移轉設定中使用的目的地資料集。同一專案下的其他 BigQuery 資料集不受影響。**警告：** 請勿從目的地資料集移除服務代理的 `roles/bigquery.dataEditor` 角色。必須具備 `roles/bigquery.dataEditor` 角色，才能使用 BigQuery 資料移轉服務。

## YouTube 頻道移轉作業的授權注意事項

在 [YouTube 頻道資料移轉](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw)中，YouTube 頻道連接器只能從與建立資料移轉的使用者憑證相關聯的 YouTube 頻道移轉資料。如要從不同的 YouTube 頻道移轉資料，您必須為每個頻道建立資料移轉作業，並為每項建立的資料移轉作業使用與該 YouTube 頻道相關聯的使用者憑證。

## 排解權限錯誤

如果移轉作業發生授權或權限相關問題，請參閱「[授權和權限問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#authorization_and_permission_issues)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]