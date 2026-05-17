Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Google Analytics 4 資料載入 BigQuery

您可以使用 Google Analytics 4 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 Google Analytics 4 資料載入至 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性轉移工作，將 Google Analytics 4 的最新資料新增至 BigQuery。

## 連接器總覽

Google Analytics 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Google Analytics 連接器支援從 [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1?hl=zh-tw) 轉移報表資料。 如要瞭解 Google Analytics 報表如何轉換成 BigQuery 表格和檢視畫面，請參閱「[Google Analytics 報表轉換](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Google Analytics 連接器支援每日資料轉移。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#set-up-ga4-transfer)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | 您可以排定資料移轉作業，在執行作業時擷取最多 30 天的 Google Analytics 資料。[設定資料移轉時，您可以設定重新整理視窗的持續時間。](#set-up-ga4-transfer)    根據預設，Google Analytics 連接器的更新期為 4 天。    詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    如要瞭解 Google Analytics 的資料保留政策，請參閱「[Google Analytics 資料保留政策](https://support.google.com/analytics/answer/7667196?hl=zh-tw)」。 |

## 從 Google Analytics 4 轉移資料並擷取

將 Google Analytics 4 的資料轉移至 BigQuery 時，系統會將資料載入至按日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 事前準備

建立 Google Analytics 4 資料移轉作業前，請先詳閱下列必要條件和資訊。

### 必要條件

* 在 Google Analytics 4 中，使用者帳戶或服務帳戶必須具備移轉設定所用[資源 ID](https://developers.google.com/analytics/devguides/reporting/data/v1/property-id?hl=zh-tw) 的檢視者存取權。
* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，儲存 Google Analytics 4 資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

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

## 自訂報表

Google Analytics 適用的 BigQuery 資料移轉服務連接器支援使用自訂報表，只要在 Google Analytics 移轉設定中指定[維度和指標](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema?hl=zh-tw)即可。這些自訂報表會從 [BigQuery 資料移轉服務支援的 Google Analytics Data API 版本](#connector_overview)擷取資料。

[建立 Google Analytics 轉移作業](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw#set-up-ga4-transfer)時，可以指定自訂報表。

### 自訂報表限制

* 每個轉移設定只能有一個自訂報表。
* 每個自訂報表最多可支援 9 個維度和 10 個指標。
* 並非所有維度和指標都能彼此相容。建立轉移作業前，請先使用 [GA4 維度和指標探索工具](https://ga-dev-tools.google/ga4/dimensions-metrics-explorer/?hl=zh-tw)，驗證自訂報表的維度和指標。
* 不支援[自訂維度和指標](https://support.google.com/analytics/answer/14240153?hl=zh-tw)。

## 設定 Google Analytics 4 資料移轉

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create transfer」(建立轉移作業)頁面執行下列操作：

   * 在「來源類型」部分，針對「來源」選擇「Google Analytics 4」。
4. 在「Data source details」(資料來源詳細資料) 區段：

   * 在「資源 ID」欄位中，輸入[資源 ID](https://developers.google.com/analytics/devguides/reporting/data/v1/property-id?hl=zh-tw)。
   * 選用步驟：在「Table Filter」(資料表篩選器) 欄位，輸入要涵蓋的資料表清單 (以逗號分隔)，例如 `Audiences, Events`。您可以為這份清單加上 `-` 前置字元來排除特定資料表，例如 `-Audiences, Events`。預設會加入所有資料表。
   * 選用步驟：如要擷取自訂報表而非標準報表，請按照下列步驟操作：
     + 在「自訂報表資料表名稱」欄位中，輸入自訂報表的輸出資料表名稱。
       如要進一步瞭解有效的資料表名稱，請參閱[資料表命名](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)。
     + 在「自訂報表維度」欄位中，輸入自訂報表的維度。
       詳情請參閱「[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw#custom_reports)」。
     + 在「自訂報表指標」欄位中，輸入自訂報表的指標。
       詳情請參閱「[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw#custom_reports)」。
   * 選用：在「Refresh window」(重新整理時間範圍) 欄位中，以天為單位輸入[重新整理時間範圍](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw#refresh)的持續時間。重新整理時間範圍的預設值為 4 天，最多可設為 30 天。
5. 在「Destination settings」(目的地設定) 部分的「Destination dataset」(目的地資料集) 選單，請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 專區，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱。移轉作業名稱可以是任何值，能讓您辨識移轉作業，方便您日後在必要時進行修改。
7. 在「Schedule options」(排程選項) 專區：

   * 選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 「Repeats」請選擇您要多久移轉一次。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
8. 選用：在「Service Account」(服務帳戶) 選單中，選取與 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。所選服務帳戶必須具備[必要角色](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw#bq-roles)，才能執行這項資料移轉作業。

   如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立資料移轉作業。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。
9. 選用步驟：在「Notification options」(通知選項) 部分執行下列操作：

   * 按一下啟用電子郵件通知的切換開關。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
   * 點選切換按鈕，啟用 Pub/Sub 通知。在「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub [執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
10. 選用步驟：如果您使用 [CMEK](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，請在「Advanced options」(進階選項) 部分選取「Customer-managed key」(客戶管理的金鑰)。畫面隨即會列出可用的 CMEK 供您選擇。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定移轉作業加密金鑰](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw#CMEK)的相關說明。
11. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。必須加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

```
  bq mk --transfer_config \
  --project_id=PROJECT_ID \
  --target_dataset=DATASET \
  --display_name=NAME \
  --params='PARAMETERS' \
  --data_source=DATA_SOURCE
```

其中：

* PROJECT\_ID：專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* DATASET：資料移轉設定的目標資料集。
* NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* PARAMETERS：已建立資料移轉設定的 JSON 格式參數，例如 `--params='{"param":"param_value"}'`。如果是 Google Analytics 4 轉移作業，則必須提供參數。`property_id`
* DATA\_SOURCE：資料來源 - `ga4`。

舉例來說，下列指令會使用資源 ID `468039345` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Google Analytics 4 資料移轉作業。

資料移轉作業會在預設專案中建立：

```
  bq mk --transfer_config
  --project_id=your_project
  --target_dataset=mydataset
  --display_name=My Transfer
  --params='{"property_id":"468039345"}'
  --data_source=ga4
```

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

## 限制

* 不重複使用者和工作階段指標的匯總總計可能不準確，且可能與 Google Analytics 中的值不符。

## 指定轉移作業的加密金鑰

您可以指定[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)，加密轉移作業的資料。您可以使用 CMEK 支援從
[Google Analytics 4](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw) 轉移資料。

指定移轉作業的 CMEK 後，BigQuery 資料移轉服務會將 CMEK 套用至所有已擷取資料的中間磁碟快取，確保整個資料移轉工作流程符合 CMEK 規定。

如果轉移作業最初並非使用 CMEK 建立，您就無法更新現有轉移作業來新增 CMEK。舉例來說，您無法將原本預設加密的目的地資料表，變更為使用 CMEK 加密。反之，您也無法將 CMEK 加密的目的地資料表變更為其他類型的加密。

如果移轉設定最初是使用 CMEK 加密功能建立，您可以更新移轉的 CMEK。更新移轉作業設定的 CMEK 時，BigQuery 資料移轉服務會在下次執行移轉作業時，將 CMEK 傳播至目的地資料表。屆時，BigQuery 資料移轉服務會在移轉作業執行期間，以新的 CMEK 取代任何過時的 CMEK。詳情請參閱「[更新轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_a_transfer)」。

您也可以使用[專案預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#project_default_key)。
使用移轉作業指定專案預設金鑰時，BigQuery 資料移轉服務會將專案預設金鑰做為任何新移轉作業設定的預設金鑰。

## 定價

執行 Google Analytics 4 轉移作業不會產生任何費用。

資料移轉至 BigQuery 之後，即適用標準的 BigQuery [儲存空間](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)和[查詢](https://cloud.google.com/bigquery/pricing?hl=zh-tw#queries)計價方式。

## 配額

Google Analytics 4 轉移作業須遵守 Google Analytics 4 執行的[Analytics 資源配額](https://developers.google.com/analytics/devguides/reporting/data/v1/quotas?hl=zh-tw#analytics_property_quotas)。如要提高每個資源的配額，請升級至 [Google Analytics 360](https://marketingplatform.google.com/about/analytics-360/features/?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]