Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用數據分析分析資料

您可以使用 BigQuery 搭配數據分析探索資料。數據分析是自助式商業智慧平台，可讓您建構及使用資料視覺化、資訊主頁和報表。您可以使用數據分析連結至 BigQuery 資料、建立圖表，並與他人分享深入分析。

Data Studio 提供進階版 Data Studio Pro，內含多項強化企業功能，包括透過 Identity and Access Management 管理權限、用於協作的團隊工作區、行動應用程式和技術支援。

您可以使用 BigQuery BI 引擎提升報表效能，同時降低運算成本。如要瞭解 BI Engine，請參閱「[BI Engine 簡介](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)」。

這些範例會使用 Google 數據分析，以視覺化方式呈現 BigQuery [`austin_bikeshare`](https://console.cloud.google.com/bigquery?cloudshell=false&%3Bd=austin_bikeshare&%3Bp=bigquery-public-data&%3Bt=bikeshare_trips&%3Bpage=table&%3Bws=%211m10%211m4%214m3%211sbigquery-public-data%212sfaa%213sus_airports%211m4%214m3%211sbigquery-public-data%212saustin_bikeshare%213sbikeshare_trips&hl=zh-tw) 資料集中的資料。如要進一步瞭解公開資料集，請參閱「[BigQuery 公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)」。

### 瞭解查詢結果

您可以建構任意 SQL 查詢，並在數據分析中將資料視覺化。如果您想在 BigQuery 中修改資料，再於 Google 數據分析中使用，或是只需要表格中的部分欄位，這個方法就非常實用。資訊主頁是根據查詢結果建立的暫時性資料表。臨時資料表最多可儲存 24 小時。

**注意：** 您最多可以在數據分析圖表中以視覺化方式呈現 5,000 列資料。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 選取您的[報帳專案](https://docs.cloud.google.com/billing/docs/concepts?hl=zh-tw#billing_account)。
3. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
4. 在「Explorer」窗格的搜尋欄位中，輸入 `bikeshare_trips`。
5. 依序前往「bigquery-public-data」**>「austin\_bikeshare」>「bikeshare\_trips」**。
6. 按一下 more\_vert「View actions」(查看動作)，然後按一下「Query」(查詢)。
7. 在查詢編輯器中建構查詢。例如：

   ```
   SELECT
     *
   FROM
     `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   LIMIT
     1000;
   ```
8. 按一下「執行」play\_circle。
9. 在「查詢結果」部分，依序點選「開啟方式」>「數據分析」。
10. 在「歡迎使用數據分析」頁面中，按一下「開始使用」，表示您同意 Google 數據分析和 Google 服務條款。
11. 在「授權數據分析存取權」頁面中，按一下「授權」，同意服務條款並授權連線，然後選取行銷偏好設定。除非您授予他人查看資料的權限，否則只有您能查看報表中的資料。

    報表編輯器會以數據分析圖表的形式顯示查詢結果。

下圖顯示數據分析報表的部分功能：

**圖例**：

1. 數據分析標誌和報表名稱。
   * 如要前往「數據分析」頁面，請按一下標誌。
   * 如要編輯報表名稱，請按一下名稱。
2. 數據分析工具列。「新增圖表」工具會醒目顯示。
3. 報表標題。如要編輯文字，請按一下欄位。
4. 資料表 (已選取)。選取圖表後，即可使用圖表標題中的選項與圖表互動。
5. 長條圖 (未選取)。
6. 「圖表」屬性窗格。選取圖表後，即可在「設定」和「樣式」分頁中，設定圖表的資料屬性和外觀。
7. **資料**窗格。您可以在這個窗格中存取報表要使用的欄位和資料來源。
   * 如要將資料新增至圖表，請將「資料」窗格中的欄位拖曳到圖表上。
   * 如要建立圖表，請將「資料」窗格中的欄位拖曳到畫布上。
8. **儲存並分享**。儲存這份報表，以便日後查看、編輯及與他人共用。儲存報表前，請先檢查資料來源設定和資料來源使用的憑證。

資料來源憑證擁有者可以點選資源，查看其工作統計資料、結果表格和 BI Engine 詳細資料。

#### 與圖表互動

數據分析圖表是互動式圖表，現在資料已顯示在數據分析中，您可以嘗試下列操作：

* 捲動並瀏覽表格。
* 在「Bar」(長條) 圖表中，將指標懸停在長條上，即可查看資料的詳細資料。
* 在長條圖中選取長條，即可依該維度交叉篩選表格。

#### 新增圖表

數據分析支援多種不同的圖表類型。如要在報表中新增更多圖表，請按照下列步驟操作：

1. 按一下工具列中的「新增圖表」add\_chart。
2. 選取要新增的圖表。
3. 按一下畫布，將圖表新增至報表。
4. 使用「圖表」屬性窗格設定圖表。

如要進一步瞭解如何在報表中新增圖表，請參閱「[在報表中新增圖表](https://docs.cloud.google.com/looker/docs/studio/tutorial-add-charts-to-your-report?hl=zh-tw)」一文。

### 探索資料表結構定義

您可以匯出資料表結構定義，在數據分析中查看資料的中繼資料。如果您不想在 BigQuery 中修改資料，再於 Google 數據分析中使用，這項功能就非常實用。

**注意：** BigQuery 查詢最多可傳回 20 MB 的資料。如果探索的資料表結構定義非常龐大，數據分析可能會截斷結果。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 選取您的[報帳專案](https://docs.cloud.google.com/billing/docs/concepts?hl=zh-tw#billing_account)。
3. 點選左側窗格中的 explore「Explorer」。
4. 在「Explorer」窗格的「Type to search」(輸入要搜尋的字詞) 欄位中，輸入 `bigquery-public-data`。
5. 依序前往「bigquery-public-data」**>「austin\_bikeshare」>「bikeshare\_trips」**。
6. 按一下工具列中的
   file\_upload
   「匯出」。如果沒有看到「匯出」，請選取「更多動作」，然後按一下「匯出」。more\_vert
7. 按一下「透過數據分析探索」。

### 分享報表

如要與他人共用報表，請傳送電子郵件邀請，讓對方前往數據分析。您可以邀請特定使用者或 Google 群組。如要分享給更多人，您也可以建立連結，讓任何人都能存取您的數據分析報表。

**注意：** 如要分享透過 BigQuery Export 功能建立的報表，請先按一下「儲存並分享」。

如要與他人共用報表，請按照下列步驟操作：

1. 在「數據分析」頁面標題中，按一下「分享」圖示 person\_add。
2. 在「與他人共用」對話方塊中，輸入收件者的電子郵件地址。您可以輸入多個電子郵件地址或 Google 群組地址。
3. 指定收件者是否可以查看或編輯報表。
4. 按一下 [傳送]。

[進一步瞭解如何共用報表](https://docs.cloud.google.com/looker/docs/studio/invite-others-to-your-reports?hl=zh-tw)。

由於資料來源與您的專案相關聯，因此刪除專案可避免 Google 數據分析查詢資料。如果不想刪除 Google Cloud 專案，可以改為刪除 Google 數據分析報表與資料來源。

### 查看 BigQuery 工作詳細資料

如果資料來源憑證設為目前使用者，該使用者就稱為「資料來源憑證擁有者」。資料來源憑證擁有者查看時，大多數資訊主頁元素都會顯示 BigQuery 圖示。如要在 BigQuery 中前往「工作詳細資料」，請按一下 BigQuery 圖示。

### 查看數據分析資訊結構定義詳細資料

您可以查看 [`INFORMATION_SCHEMA.JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，追蹤 BigQuery 使用的 Google 數據分析報表和資料來源。每個數據分析工作都有 `looker_studio_report_id` 和 `looker_studio_datasource_id` 標籤。開啟報表或資料來源頁面時，這些 ID 會顯示在數據分析網址的尾端。
舉例來說，網址為 `https://datastudio.google.com/navigation/reporting/1234-YYY-ZZ` 的報表，其報表 ID 為「1234-YYY-ZZ」。

下列範例說明如何查看報表和資料來源：

#### 查看數據分析 BigQuery 的工作報表和資料來源網址

如要查看每個數據分析 BigQuery 工作報表和資料來源的網址，請執行下列查詢：

```
-- Standard labels used by Data Studio.
DECLARE requestor_key STRING DEFAULT 'requestor';
DECLARE requestor_value STRING DEFAULT 'looker_studio';

CREATE TEMP FUNCTION GetLabel(labels ANY TYPE, label_key STRING)
AS (
  (SELECT l.value FROM UNNEST(labels) l WHERE l.key = label_key)
);

CREATE TEMP FUNCTION GetDatasourceUrl(labels ANY TYPE)
AS (
  CONCAT("https://datastudio.google.com/datasources/", GetLabel(labels, 'looker_studio_datasource_id'))
);

CREATE TEMP FUNCTION GetReportUrl(labels ANY TYPE)
AS (
  CONCAT("https://datastudio.google.com/reporting/", GetLabel(labels, 'looker_studio_report_id'))
);

SELECT
  job_id,
  GetDatasourceUrl(labels) AS datasource_url,
  GetReportUrl(labels) AS report_url,
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS jobs
WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND GetLabel(labels, requestor_key) = requestor_value
LIMIT
  100;
```

#### 查看使用報表和資料來源產生的工作

如要查看產生的工作，請執行下列查詢：

```
-- Specify report and data source id, which can be found in the end of Data Studio URLs.
DECLARE user_report_id STRING DEFAULT '*report id here*';
DECLARE user_datasource_id STRING DEFAULT '*datasource id here*';

-- Data Studio labels for BigQuery jobs.
DECLARE requestor_key STRING DEFAULT 'requestor';
DECLARE requestor_value STRING DEFAULT 'looker_studio';
DECLARE datasource_key STRING DEFAULT 'looker_studio_datasource_id';
DECLARE report_key STRING DEFAULT 'looker_studio_report_id';

CREATE TEMP FUNCTION GetLabel(labels ANY TYPE, label_key STRING)
AS (
  (SELECT l.value FROM UNNEST(labels) l WHERE l.key = label_key)
);

SELECT
  creation_time,
  job_id,
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS jobs
WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND GetLabel(labels, requestor_key) = requestor_value
  AND GetLabel(labels, datasource_key) = user_datasource_id
  AND GetLabel(labels, report_key) = user_report_id
ORDER BY 1
LIMIT 100;
```

## 後續步驟

* 如要進一步瞭解如何預留 BI Engine 容量，請參閱「[預留 BI Engine 容量](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)」。
* 如要進一步瞭解如何撰寫 BigQuery 查詢，請參閱「[BigQuery 數據分析總覽](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)」一文。本文說明如何執行查詢或建立使用者定義的函式 (UDF) 等工作。
* 如要探索 BigQuery 語法，請參閱「[BigQuery 中的 SQL 簡介](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw)」。在 BigQuery 中，SQL 查詢的慣用方言是標準 SQL。如需 BigQuery 舊版類 SQL 語法的說明，請參閱[舊版 SQL 函式和運算子](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw)。
* 如要進一步瞭解將 BigQuery 資料連結至數據分析 的配額和限制，請參閱「[連結至 BigQuery](https://docs.cloud.google.com/looker/docs/studio/connect-to-google-bigquery?hl=zh-tw#quotas_and_general_limits)」一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]