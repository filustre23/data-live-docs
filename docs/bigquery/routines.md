Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理日常安排

在 BigQuery 中，*常式*是一種資源類型，包含下列項目：

* [預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw#writing_a_procedure)。
* [使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw) (UDF)，包括[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)和[使用者定義的匯總函式](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw)。
* [資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)。

本文說明 BigQuery 中所有常式類型通用的工作。

## 權限

如要在 SQL 查詢中參照常式，您必須具備 `bigquery.routines.get` 權限。如要授予常式存取權，請在資料集或個別常式中，授予具有 `bigquery.routines.get` 權限的 IAM 角色。在資料集層級授予存取權，可讓主體存取資料集中的所有常式。詳情請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

根據預設，您也需要有權存取常式參照的任何資源，例如資料表或檢視區塊。如果是 UDF 和資料表函式，您可以*授權*函式代表呼叫端存取這些資源。詳情請參閱「[授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-functions?hl=zh-tw)」。

## 建立處理常式

如要建立常式，必須具備 `bigquery.routines.create` 權限。

### SQL

視常式類型而定，執行下列其中一個 DDL 陳述式：

* [預存程序：`CREATE PROCEDURE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure)
* [使用者定義函式：`CREATE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement)
* [資料表函式：`CREATE TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_function_statement)
* [使用者定義的匯總函式：`CREATE AGGREGATE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#sql-create-udaf-function)

### API

使用已定義的[`Routine` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines?hl=zh-tw#Routine)呼叫 [`routines.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines/insert?hl=zh-tw)。

## 列出處理常式

如要列出資料集中的常式，您必須具備 `bigquery.routines.get` 和 `bigquery.routines.list` 權限。

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 按一下「日常安排」分頁標籤。

### SQL

查詢 [`INFORMATION_SCHEMA.ROUTINES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-routines?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     COLUMN_LIST
   FROM
      { DATASET | REGION }.INFORMATION_SCHEMA.ROUTINES;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

更改下列內容：

* COLUMN\_LIST：以半形逗號分隔的清單，列出[`INFORMATION_SCHEMA.ROUTINES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-routines?hl=zh-tw)中的資料欄。
* DATASET：專案中的資料集名稱。
* REGION：[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)。

範例：

```
SELECT
  routine_name, routine_type, routine_body
FROM
  mydataset.INFORMATION_SCHEMA.ROUTINES;
```

```
+------------------+----------------+--------------+
|   routine_name   |  routine_type  | routine_body |
+------------------+----------------+--------------+
| AddFourAndDivide | FUNCTION       | SQL          |
| create_customer  | PROCEDURE      | SQL          |
| names_by_year    | TABLE FUNCTION | SQL          |
+------------------+----------------+--------------+
```

### bq

使用 [`bq ls` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_ls)並加上 `--routines` 旗標：

```
bq ls --routines DATASET
```

更改下列內容：

* DATASET：專案中的資料集名稱。

範例：

```
bq ls --routines mydataset
```

```
         Id              Routine Type        Language    Creation Time    Last Modified Time
------------------ ----------------------- ---------- ----------------- --------------------
 AddFourAndDivide   SCALAR_FUNCTION         SQL        05 May 01:12:03   05 May 01:12:03
 create_customer    PROCEDURE               SQL        21 Apr 19:55:51   21 Apr 19:55:51
 names_by_year      TABLE_VALUED_FUNCTION   SQL        01 Sep 22:59:17   01 Sep 22:59:17
```

### API

呼叫 [`routines.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines/list?hl=zh-tw)，並傳遞資料集 ID。

## 查看日常安排的內容

如要查看常式主體，必須具備 `bigquery.routines.get` 權限。

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 按一下「日常安排」分頁標籤。
5. 選取日常安排。常式主體會列在「常式查詢」下方。

### SQL

選取「[`INFORMATION_SCHEMA.ROUTINES`」檢視畫面」的 `routine_definition` 欄：](https://docs.cloud.google.com/bigquery/docs/information-schema-routines?hl=zh-tw)

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     routine_definition
   FROM
     { DATASET | REGION }.INFORMATION_SCHEMA.ROUTINES
   WHERE
     routine_name = ROUTINE_NAME;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

更改下列內容：

* DATASET：專案中的資料集名稱。
* REGION：[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)。
* ROUTINE\_NAME：日常安排的名稱。

範例：

```
SELECT
  routine_definition
FROM
  mydataset.INFORMATION_SCHEMA.ROUTINES
WHERE
  routine_name = 'AddFourAndDivide';
```

```
+--------------------+
| routine_definition |
+--------------------+
| (x + 4) / y        |
+--------------------+
```

### bq

使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)並加上 `--routine` 旗標：

```
bq show --routine DATASET.ROUTINE_NAME
```

更改下列內容：

* DATASET：專案中的資料集名稱。
* ROUTINE\_NAME：日常安排的名稱。

範例：

```
bq show --routine mydataset.AddFourAndDivide
```

```
         Id           Routine Type     Language             Signature             Definition     Creation Time    Last Modified Time
 ------------------ ----------------- ---------- ------------------------------- ------------- ----------------- --------------------
  AddFourAndDivide   SCALAR_FUNCTION   SQL        (x INT64, y INT64) -> FLOAT64   (x + 4) / y   05 May 01:12:03   05 May 01:12:03
```

### API

呼叫 [`routines.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines/get?hl=zh-tw)，並傳遞資料集 ID 和常式名稱。常式主體會以 [`Routine` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines?hl=zh-tw#Routine)的形式傳回。

## 刪除處理常式

如要刪除日常安排，必須具備 `bigquery.routines.delete` 權限。

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 按一下「日常安排」分頁標籤。
5. 選取日常安排。
6. 在詳細資料窗格中，按一下「刪除」。
7. 在對話方塊中輸入 `"delete"`，然後按一下「刪除」確認操作。

### SQL

視常式類型而定，執行下列其中一個 DDL 陳述式：

* [預存程序：`DROP PROCEDURE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_procedure_statement)
* [使用者定義函式：`DROP FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_function_statement)
* [資料表函式：`DROP TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_table_function)

範例：

```
DROP FUNCTION IF EXISTS mydataset.AddFourAndDivide
```

### bq

使用 [`bq rm` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_rm)並加上 `--routine` 旗標：

```
bq rm --routine DATASET.ROUTINE_NAME
```

更改下列內容：

* DATASET：專案中的資料集名稱。
* ROUTINE\_NAME：日常安排的名稱。

範例：

```
bq rm --routine mydataset.AddFourAndDivide
```

### API

呼叫 [`routines.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines/delete?hl=zh-tw)，並傳遞資料集 ID 和常式名稱。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]