* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用第三方移轉服務

BigQuery 資料移轉服務的第三方移轉作業，可讓您自動安排及管理外部資料來源 (例如 Salesforce CRM、Adobe Analytics，以及 Facebook Ads) 的週期性載入工作。

## 事前準備

建立第三方資料移轉作業之前：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。
* 請參閱第三方資料來源的說明文件，以確保您已設定啟用移轉所需的任何權限。
* 如果您想要為 Pub/Sub 設定移轉作業執行通知，您必須擁有`pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

## 限制

第三方移轉作業有以下限制：

* 您必須使用Google Cloud 控制台建立或更新第三方移轉作業。
* 您無法使用 bq 指令列工具設定或更新第三方移轉作業。

## 設定第三方資料移轉作業

如何使用 Google Cloud 控制台建立第三方資料移轉作業：

1. 前往 Google Cloud Marketplace。

   [前往 Google Cloud Marketplace](https://console.cloud.google.com/marketplace/browse?filter=category%3Adata-transfer-services&hl=zh-tw)
2. 按一下適當的第三方供應商。
3. 在第三方供應商的說明文件頁面中，按一下 [Enroll] (註冊)。註冊過程可能需要一些時間才能完成。
4. 註冊完成後，按一下 [Configure Transfer] (設定移轉作業)。
5. 在「Create Transfer」(建立移轉作業) 頁面中：

   * 在「Source」(來源) 中，選擇適當的第三方資料來源。您可以按一下「探索資料來源」，查看 Google Cloud Marketplace 中的第三方供應商清單。
   * 在「Display name」(顯示名稱) 部分，輸入移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任何容易辨識的值，方便您日後在必要時進行修改。
   * 在 [Schedule] (排程) 中保留預設值 [Start now] (立即開始)，或按一下 [Start at a set time] (於設定的時間開始)。

     + 針對「Repeats」(重複時間間隔)，請選擇多久執行一次移轉作業的選項。選項包括：

       - 每天 (預設)
       - Weekly (每週)
       - Monthly (每月)
       - Custom (自訂)
       - On-demand (隨選)

       如果您選擇 [Daily] (每天) 以外的選項，則有其他選項可供使用。舉例來說，如果選擇 [Weekly] (每週)，則會出現一個可供選擇星期幾的選項。
     + 針對「Start date and run time」(開始日期和執行時間)，請輸入開始移轉作業的日期和時間。如果您選擇 [Start now] (立即開始)，系統就會停用這個選項。
   * 在 [Destination dataset] (目的地資料集) 選擇為了儲存資料而建立的資料集。
   * (選用) 在「Notification options」(通知選項) 區段中：

     + 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
     + 針對「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題)，請選擇您的[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是按一下 [Create a topic] (建立主題) 來建立主題。此選項會設定移轉作業的 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
6. 按一下 [Connect Source] (與來源連線)。

   **注意：** 如果未選取目的地資料集，按一下「連結來源」會產生下列錯誤：`A selected destination dataset is
   required before connecting to the source.`
7. 當系統出現提示時，按一下「接受」，即可授權 BigQuery 資料移轉服務連線到資料來源，以及在 BigQuery 中管理資料。
8. 依照後續頁面中的說明，設定與外部資料來源的連線。
9. 完成設定步驟之後，按一下 [Save] (儲存)。

## 疑難排解第三方移轉作業設定

如果您無法順利設定移轉作業，請洽詢適當的第三方供應商。聯絡資訊可在 Google Cloud Marketplace 的移轉說明文件頁面中取得。

## 查詢資料

資料移轉至 BigQuery 時，系統會將資料寫入擷取時間分區資料表。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

如果您要直接查詢資料表，而不要使用自動產生的檢視表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱
  [BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 如要瞭解如何使用移轉作業，包括取得移轉設定、列出移轉設定以及查看移轉設定的執行記錄，請參閱[使用移轉功能](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]