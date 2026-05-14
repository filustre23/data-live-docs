Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Data Catalog



**注意：**Data Catalog 已[淘汰](https://docs.cloud.google.com/data-catalog/docs/deprecations?hl=zh-tw)，
建議改用 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/catalog-overview?hl=zh-tw)，
這個平台可為 Google Cloud的資料和 AI 資產提供智慧型治理功能。
BigQuery 現已整合重要的 Knowledge Catalog 功能，可供使用。如要瞭解如何使用切面豐富資料，請參閱「[管理切面及豐富中繼資料](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw)」一文。切面相當於 Data Catalog 標記。

Data Catalog 會自動分類 BigQuery 資源 (例如資料表、資料集、檢視區塊和模型) 的中繼資料，與 BigQuery 整合。本文說明如何使用 Data Catalog 搜尋這些資源、查看資料歷程，以及新增標記。

## 搜尋 BigQuery 資源

如要使用 Data Catalog 搜尋 BigQuery 資料集、資料表和已加星號的專案，請按照下列步驟操作：

1. 在 Google Cloud 控制台，前往 Data Catalog 的「Search」(搜尋) 頁面。

   [前往「搜尋」頁面](https://console.cloud.google.com/dataplex?hl=zh-tw)
2. 在「搜尋」欄位中輸入查詢，然後按一下「搜尋」。

   如要修正搜尋參數，請使用「篩選條件」面板。舉例來說，在「系統」部分，選取「BigQuery」核取方塊。結果會篩選至 BigQuery 系統。

您可以在 Data Catalog 中透過Google Cloud 控制台執行基本搜尋，如要進一步瞭解如何在 Google Cloud 控制台中搜尋，請參閱「[開啟公開資料集](https://docs.cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console?hl=zh-tw#open_a_public_dataset)」。

## 資料歷程

[資料歷程](https://docs.cloud.google.com/dataplex/docs/about-data-lineage?hl=zh-tw)是 Knowledge Catalog 的功能，可追蹤資料在系統中的移動情形，包括來源、傳遞目的地和採用的轉換作業。您可以直接從 BigQuery 存取資料歷程功能。

在 BigQuery 專案中啟用資料歷程後，Knowledge Catalog 會自動記錄下列作業所建立資料表的歷程資訊：

* [複製工作](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)。
* 在 GoogleSQL 中使用下列資料定義語言 (DDL) 或資料操作語言 (DML) 陳述式的[查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)：

  + [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) (包括 `CREATE TABLE AS SELECT` 陳述式)
  + [`INSERT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)
  + [`UPDATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#update_statement)
  + [`DELETE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#delete_statement)
  + [`MERGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#merge_statement)

### 事前準備

在本節中，您將啟用 Data Lineage API，並授予[身分與存取權管理 (IAM)](https://docs.cloud.google.com/iam/docs?hl=zh-tw) 角色，讓使用者擁有執行本文件各項工作所需的權限。

#### 啟用資料歷程

1. 在 Google Cloud 控制台的專案選取器頁面中，選取包含要追蹤歷程的資源的專案。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. 啟用 Data Lineage API 和 Dataplex API。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=datalineage.googleapis.com%2Cdataplex.googleapis.com&hl=zh-tw)

**注意：** 啟用 Data Lineage API 可能會產生額外費用。詳情請參閱「[資料歷程注意事項](https://docs.cloud.google.com/dataplex/docs/lineage-considerations?hl=zh-tw)」。

#### 必要的 IAM 角色

啟用 Data Lineage API 後，系統就會自動追蹤歷程資訊。

如要取得查看歷程圖所需的權限，請要求管理員授予您下列 IAM 角色：

* [Data Catalog 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw#datacatalog.viewer)  (`roles/datacatalog.viewer`)
  在 Data Catalog 資源專案中。
* 在您使用資料歷程支援系統的專案中，[資料歷程檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/datalineage?hl=zh-tw#datalineage.viewer)  (`roles/datalineage.viewer`)。
* [BigQuery Metadata](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer)  (`roles/bigquery.metadataViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

詳情請參閱「[資料沿革角色](https://docs.cloud.google.com/dataplex/docs/iam-roles?hl=zh-tw#lineage-roles)」。

### 在 BigQuery 中查看歷程圖

如要從 BigQuery 查看資料歷程圖，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 按一下「歷程」分頁標籤。

   系統會顯示資料歷程圖。
6. 選用：選取節點，即可查看與建構沿襲資訊相關的實體或程序其他詳細資料。

如要進一步瞭解資料歷程，請參閱「[關於資料歷程](https://docs.cloud.google.com/dataplex/docs/about-data-lineage?hl=zh-tw)」。

## 標記和標記範本

機構可透過標記，在統一服務中建立、搜尋及管理所有資料項目的中繼資料。

本節將說明兩個重要的 Data Catalog 概念：

* *標記*可讓您附加自訂中繼資料欄位，為資料項目提供背景資訊。
* *代碼範本*是可重複使用的結構，方便您快速建立新的代碼。

### 標記

Data Catalog 提供兩種標記：私人標記和公開標記。

#### 私人標記

私人標記提供嚴格的存取權控管機制。您必須具備私人代碼範本和資料項目所需的[查看權限](https://docs.cloud.google.com/data-catalog/docs/concepts/iam?hl=zh-tw#roles_to_view_public_and_private_tags)，才能搜尋或查看標記及其相關聯的資料項目。

如要在「Data Catalog」頁面搜尋私人標記，必須使用 `tag:` 搜尋語法或搜尋篩選器。

如果您需要在標記中儲存某些私密資訊，且想在檢查使用者是否具備查看標記項目的權限之外，套用額外的存取限制，就適合使用私密標記。

#### 公開標記

與私人標記相比，公開標記的搜尋和檢視存取控管較不嚴格。具備資料項目必要查看權限的使用者，都可以查看所有與該資料項目相關聯的公開標記。只有在 Data Catalog 中使用 `tag:` 語法執行搜尋，或查看未附加的代碼範本時，才需要公開標記的查看權限。

公開標記支援簡易搜尋，以及在 Data Catalog 搜尋頁面中透過述詞搜尋。建立代碼範本時， Google Cloud 控制台預設會建議您建立公開代碼範本。

舉例來說，假設您有名為 `employee data` 的公開代碼範本，並用來為名為 `Name`、`Location` 和 `Salary` 的三個資料項目建立代碼。在三筆資料中，只有名為「`HR`」的特定群組成員可以查看「`Salary`」資料。另外兩筆資料項目則開放公司全體員工檢視。

如果不是 `HR` 群組成員的員工使用 Data Catalog 搜尋頁面，並以 `employee` 一字進行搜尋，搜尋結果只會顯示 `Name` 和 `Location` 資料項目，以及相關聯的公開標記。

公開標記適用於各種情境。公開標記支援簡易搜尋和使用述詞搜尋，私人標記則僅支援使用述詞搜尋。

### 標記範本

請先建立一或多個標記範本，才能開始標記中繼資料。代碼範本可以是公開或私人代碼範本。建立代碼範本時， Google Cloud 控制台預設會建議您建立公開代碼範本。代碼範本是一組稱為「欄位」的中繼資料鍵/值組合。擁有一組範本，就好像擁有中繼資料的資料庫結構定義一樣。

您可以依主題分類標記。例如：

* `data governance` 標記，內含資料管理員、保留日期、
  刪除日期、個人識別資訊 (是或否)、資料分類 (公開、機密、
  敏感、法規) 的欄位
* `data quality` 代碼，包含品質問題、更新頻率、服務等級目標 (SLO) 資訊等欄位
* 含有熱門使用者、熱門查詢、每日平均使用者欄位的 `data usage` 標記

然後，您就可以混用代碼，只使用與每個資料資產和業務需求相關的代碼。

#### 查看代碼範本庫

為協助您入門，Data Catalog 內含範例標記範本庫，說明常見的標記用途。您可以參考這些範例，瞭解標記的強大功能、從中汲取靈感，或做為建立自有標記基礎架構的起點。

如要使用代碼範本庫，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 Knowledge Catalog「標記範本」頁面。

   [前往「代碼範本」](https://console.cloud.google.com/dataplex/templates?hl=zh-tw)
2. 按一下「建立標記範本」。

   範本庫會顯示在「建立範本」頁面中。

從範本庫選取範本後，使用方式和其他任何代碼範本完全一樣。您可以根據自己的業務需求新增及刪除屬性，以及變更範本中的任何內容。然後，您可以使用 Data Catalog 搜尋範本欄位和值。

如要進一步瞭解標記和標記範本，請參閱「[標記和標記範本](https://docs.cloud.google.com/data-catalog/docs/tags-and-tag-templates?hl=zh-tw)」。

### 地區資源

每個代碼範本和代碼都會儲存在特定[Google Cloud區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。您可以使用代碼範本在任何區域建立代碼，因此如果中繼資料項目分散在多個區域，您不需要建立範本副本。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]