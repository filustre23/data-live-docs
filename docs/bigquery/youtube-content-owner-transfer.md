Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 YouTube 內容擁有者資料載入 BigQuery

您可以使用 YouTube 內容擁有者連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 YouTube 內容擁有者的資料載入 BigQuery。您可以使用 BigQuery 資料移轉服務，排定週期性移轉工作，將 YouTube 內容擁有者的最新資料新增至 BigQuery。

## 連接器總覽

YouTube 內容擁有者連接器的 BigQuery 資料移轉服務，支援下列資料移轉選項。

| 資料移轉選項 | 支援 |
| --- | --- |
| 受支援的報表 | YouTube 內容擁有者連接器支援從下列報表移轉資料：    * [內容擁有者報表](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw) * 系統代管報表：   + [總覽](https://developers.google.com/youtube/reporting/v1/reports/system_managed/reports?hl=zh-tw)   + [報告](https://developers.google.com/youtube/reporting/v1/reports/system_managed/reports?hl=zh-tw)   + [欄位](https://developers.google.com/youtube/reporting/v1/reports/system_managed/fields?hl=zh-tw)   YouTube 內容擁有者連接器支援 [2018 年 6 月 18 日](https://developers.google.com/youtube/reporting/revision_history?hl=zh-tw#june-18,-2018)的 API 版本。  如要瞭解 YouTube 內容擁有者報表如何轉換為 BigQuery 資料表和檢視表，請參閱「[YouTube 內容擁有者報表轉換](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transformation?hl=zh-tw)」。 |
| 重複頻率 | YouTube 內容擁有者連接器支援每日資料移轉。    根據預設，資料移轉作業會排定在建立資料移轉作業時執行。您可以在[設定資料移轉作業](#set_up_a_youtube_content_owner_transfer)時，設定資料移轉時間。 |
| 重新整理時間範圍 | 執行資料移轉作業時，YouTube 內容擁有者連接器最多會擷取 1 天的 YouTube 內容擁有者資料。    詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 補充資料可用性 | 在每次排定的移轉作業執行期間，YouTube 內容擁有者連接器會自動回填移轉作業執行日期前最多 60 天內新產生或更新的報表。詳情請參閱「[自動補播](#automatic-backfills)」。    您也可以[執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，手動擷取排定資料移轉作業以外的資料。您可以擷取資料來源資料保留政策允許範圍內的資料。    含有歷來資料的 YouTube 報表自產生當日起有 30 天的效期。(不含歷來資料的報表可保留 60 天)。詳情請參閱「[歷來資料](https://developers.google.com/youtube/reporting/v1/reports/?hl=zh-tw#historical-data)」。 |

## 從 YouTube 內容擁有者移轉作業擷取資料

將 YouTube 內容擁有者報表中的資料移轉至 BigQuery 時，系統會將資料載入依日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果您在同一天安排多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該日期的分區。在同一天進行多次移轉或執行補充作業，不會產生重複資料，其他日期的分區也不會受到影響。

### 重新整理時間範圍

「更新回溯期」是指資料移轉時，資料移轉作業擷取資料的天數。舉例來說，如果更新時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務會從來源資料表擷取過去三天的所有資料。在本例中，每日移轉作業執行時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分區，並複製當天的來源資料表資料，然後自動觸發補充執行作業，使用過去兩天的來源資料表資料更新 BigQuery 目的地資料表分區。自動觸發的回填執行作業會覆寫或增量更新 BigQuery 目的地資料表，具體取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉作業時，系統會擷取重新整理期間內的所有可用來源資料。舉例來說，如果更新時間範圍為三天，且您首次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

這個連接器會[自動回填](#automatic-backfills)過去 60 天內延遲或更新的報表。如要擷取更新時間範圍以外的其他資料 (例如歷來資料)，或復原任何因移轉中斷或缺漏而遺失的資料，您可以手動啟動或排定[補充執行作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

### 自動候補

如果 YouTube 內容擁有者報表延遲或重新產生，BigQuery 資料移轉服務會自動回填報表。在每次排定的移轉作業執行期間，BigQuery 資料移轉服務會檢查過去 60 天內產生的報表，以及上次排定的移轉作業執行後產生的報表。只要有新報表，BigQuery 資料移轉服務就會自動安排回填移轉作業，將更新後的資料載入對應的資料表分區。如果 YouTube 報表在這 60 天內延遲或更新，您不需要手動觸發補充。

## 限制

* 資料移轉作業的排程頻率下限為每 24 小時一次。根據預設，資料移轉作業會在您建立資料移轉作業時啟動。不過，您可以在[設定移轉作業](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#set_up_a_youtube_content_owner_transfer)時，指定移轉作業的開始時間。
* BigQuery 資料移轉服務不支援在 YouTube 內容擁有者移轉期間，進行增量資料移轉。指定資料移轉日期後，系統會移轉該日期可用的所有資料。

## 事前準備

建立 YouTube 內容擁有者資料移轉作業前，請先完成下列事項：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，用於儲存 YouTube 資料。
* 確認您擁有 [YouTube 內容擁有者](https://support.google.com/youtube/answer/6301188?hl=zh-tw)帳戶。YouTube 內容擁有者與 YouTube 頻道不同。
  通常只有管理多個不同頻道的使用者，才會有 YouTube 內容擁有者帳戶。
* 如果您想要為 Pub/Sub 設定移轉作業執行通知，您必須擁有`pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

## 所需權限

請確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

### 必要的 YouTube 角色

* YouTube 內容管理員或 YouTube 內容擁有者。

  內容管理員具有為內容擁有者管理 YouTube 內容的權限。內容擁有者是一種綜合帳戶，這個帳戶擁有一個或多個 YouTube 頻道，以及這些頻道中的影片。
* YouTube 內容擁有者報表設定中未勾選「`Hide revenue data`」。

  如要轉移收益相關報表，建立轉移作業的使用者不應勾選 YouTube 報表權限設定 `Hide revenue data`。

## 設定 YouTube 內容擁有者轉移作業

如要設定 YouTube 內容擁有者資料移轉作業，您必須具備：

* **內容擁有者 ID**：由 YouTube 提供。以內容擁有者或管理員身分登入 YouTube 時，ID 會顯示在網址中 `o=` 的後方。舉例來說，如果網址是 `https://studio.youtube.com/owner/AbCDE_8FghIjK?o=AbCDE_8FghIjK`，內容擁有者 ID 就是 `AbCDE_8FghIjK`。如要選取其他內容管理員帳戶，請參閱「[登入內容管理員帳戶](https://support.google.com/youtube/answer/6301172?hl=zh-tw)」或「[YouTube 頻道切換工具](https://www.youtube.com/channel_switcher?hl=zh-tw)」。如要進一步瞭解如何建立及管理內容管理員帳戶，請參閱「[調整內容管理員帳戶設定](https://support.google.com/youtube/topic/6032636?hl=zh-tw)」。
* **資料表後置字串**：設定移轉作業時，由您提供的頻道名稱，方便使用者辨識。這個尾碼會附加至工作 ID，以便建立表格名稱，例如 reportTypeId\_suffix。這個後置字串可防止不同的資料移轉作業寫入相同的資料表。所有將資料載入同個資料集的移轉工作，其資料表後置字串都不能重複，且後置字串應盡量簡短，避免產生過於冗長的資料表名稱。

如果您使用 [YouTube Reporting API](https://developers.google.com/youtube/reporting/v1/reference/rest/?hl=zh-tw)，且已有報表工作，BigQuery 資料移轉服務會載入報表資料。如果沒有現有的報表工作，設定資料移轉作業時，系統會自動啟用 YouTube 報表工作。

如要設定 YouTube 內容擁有者資料移轉作業，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。確認你是以內容擁有者或內容管理員的身分登入帳戶。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Transfers] (傳輸作業)。
3. 按一下 [Create Transfer] (建立移轉作業)。
4. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 區段中，針對「Source」(來源)，選擇 [YouTube Content Owner] (YouTube 內容擁有者)。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Schedule options」(排程選項) 專區：

     + 在「Repeat frequency」(重複頻率) 部分選取選項，指定資料移轉作業的執行頻率。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
     + 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 在「Destination settings」(目的地設定) 部分，「Destination dataset」(目的地資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 區段：

     + 於「Content Owner ID」(內容擁有者 ID) 部分輸入您的內容擁有者 ID。
     + 在「Table Suffix」(資料表後置字串) 部分，輸入後置字串，例如 `MT`。
   * 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

     如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立資料移轉作業。服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#required_permissions)。
   * (選用) 在「Notification options」(通知選項) 區段中：

     + 點選切換按鈕，啟用電子郵件通知。啟用這個選項之後，若資料移轉失敗，移轉作業管理員就會收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
5. 按一下「儲存」。
6. 如果是第一次登入帳戶，請選取帳戶並點選「Allow」(允許)。請選取您是內容擁有者或內容管理員的帳戶。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

選用標記：

* `--service_account_name`：指定要用於內容擁有者移轉驗證的服務帳戶，而非使用者帳戶。

```
bq mk \
--transfer_config \
--project_id=project_id \
--target_dataset=dataset \
--display_name=name \
--params='parameters' \
--data_source=data_source \
--service_account_name=service_account_name
```

其中：

* project\_id 是您的專案 ID。
* dataset 是移轉設定的目標資料集。
* name 是移轉設定的顯示名稱。資料移轉作業名稱可以是任何值，能讓您辨識移轉作業，方便您日後在必要時進行修改。
* parameters 包含所建立移轉設定的參數，格式為 JSON。例如：`--params='{"param":"param_value"}'`。如要移轉 YouTube 內容擁有者資料，您必須提供 `content_owner_id` 和 `table_suffix` 參數。您可以選擇將 `configure_jobs` 參數設為 `true`，允許 BigQuery 資料移轉服務代您管理 YouTube 報表工作。如果您的帳戶還沒有特定 YouTube 報表，必須建立新的報表工作才能移轉。
* data\_source 是資料來源：`youtube_content_owner`。
* service\_account\_name 是用於驗證資料移轉作業的服務帳戶名稱。服務帳戶應由建立移轉作業時使用的 `project_id` 擁有，且應具備所有[必要權限](#required_permissions)。

**注意：** 您無法使用指令列工具設定通知。

您還可以提供 `--project_id` 標記來指定特定專案。如果未指定 `--project_id`，系統會採用預設專案。

舉例來說，下列指令會使用內容擁有者 ID `AbCDE_8FghIjK`、資料表後置字串 `MT` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 YouTube 內容擁有者資料移轉作業。資料移轉作業會在預設專案中建立：

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"content_owner_id":"abCDE_8FghIjK","table_suffix":"MT","configure_jobs":"true"}' \
--data_source=youtube_content_owner
```

**注意：**使用指令列工具建立 YouTube 內容擁有者資料移轉作業時，系統會使用**排程**的[預設值](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#connector_overview)設定移轉設定。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.
```