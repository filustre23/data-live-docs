* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 日常安排簡介

本文說明如何選擇常式。常式是一種資源類型，可用於在 BigQuery 中建立函式或儲存程序。

## 支援的常式

BigQuery 支援下列常式：

* [使用者定義的函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw) (UDF)
* [使用者定義的匯總函式](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw) (UDAF)
* [資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)
* [遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)
* [預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)

## 如何選擇日常安排

本節說明選擇例行程序時應考量的因素，並比較不同例行程序可執行的工作。

### 考量因素

如要選擇日常安排，請考慮下列因素，這些因素會在各類型日常安排的章節中說明：

* 要實作的工作類型。
* 要使用的程式設計語言。
* 要為常式實作的持續性類型：暫時或持續。
* 常式所需的重複使用類型：單一或多個查詢。
* 效能注意事項。
* 存取外部服務。
* 與使用者共用日常安排。

### 依工作比較常式

下表列出各類日常作業可執行的工作：

| **工作** | **常式資源類型** |
| --- | --- |
| 在 BigQuery 中建立函式，執行一般用途的工作。 | SQL 或 JavaScript UDF  SQL 或 JavaScript UDAF |
| 在 BigQuery 中建立執行一般用途工作的函式，並使用 Google Cloud [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)與外部系統通訊。 | Python UDF |
| 建立匯總資料的函式。 | UDAF |
| 使用參數建立資料表。 | 資料表函式 |
| 建立使用 BigQuery 不支援的語言、程式庫或服務的函式。這些函式會直接與 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)和 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw) 整合。 | 遠端函式 |
| 使用[程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，以多重陳述式查詢的形式，在單一查詢中執行多個陳述式。您可以使用多重陳述式查詢執行下列操作：   * 按照共用狀態的序列，執行多個陳述式。 * 自動執行建立或捨棄資料表等管理工作。 * 使用 `IF` 和 `WHILE` 等程式設計結構實作複雜邏輯。   在 BigQuery 中建立及呼叫 Apache Spark 適用的預存程序。 | 預存程序 |

## 使用者定義的函式 (UDF)

UDF 可讓您使用 SQL 運算式、JavaScript 程式碼或 Python 程式碼建立函式。UDF 可接受輸入資料欄、對輸入內容執行動作，並將執行結果以值的形式傳回。

您可以將 UDF 定義為永久或暫時函式。您可以在多項查詢中重複使用永久 UDF，而單項查詢的範圍內只能有一個暫時性 UDF。

您可以建立 UDF，搭配[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)使用，在對資料欄套用 UDF 後傳回資料欄的值。建立自訂遮蓋常式後，您可以在「建立資料政策」中將其設為遮蓋規則。

如要進一步瞭解 UDF，請參閱下列資源：

* [使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)
* [舊版 SQL 中的使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-legacy?hl=zh-tw)
* [比較 UDF 和 UDAF](#compare-udfs)

### 語言型 UDF

* *以 SQL 為基礎的 UDF* 支援[範本 UDF 參數](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#templated-sql-udf-parameters)，可在呼叫 UDF 時比對多個引數類型。SQL UDF 也可以傳回[純量子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#scalar_subquery_concepts)的值。
* *以 JavaScript 為基礎的 UDF* 可讓您從 SQL 查詢呼叫以 JavaScript 編寫的程式碼。
  + 與標準 SQL 查詢相比，JavaScript UDF 通常會耗用更多 slot 資源，導致工作效能降低。
  + 如果函式可以透過 SQL 表示，通常以標準 SQL 查詢工作執行程式碼會更有效率。
* *以 Python 為基礎的 UDF* 會在 BigQuery 管理的資源上建構及執行。您可以透過這些 UDF 在 Python 中實作函式，並在 SQL 查詢中使用。
  + 您可以使用 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)服務帳戶，從 Python UDF [存取 Google Cloud 服務或外部服務](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw#use-online-service)。
  + 您也可以從 [Python Package Index (PyPI)](https://pypi.org/) 安裝第三方程式庫。

### 社群提供的 UDF

除了您建立的 UDF 外，社群提供的 UDF 也可在`bigquery-public-data.persistent_udfs`公開資料集和開放原始碼 [`bigquery-utils` GitHub 存放區](https://github.com/GoogleCloudPlatform/bigquery-utils)中取得。

## 使用者定義的匯總函式 (UDAF)

UDAF 可讓您使用含有 SQL 或 JavaScript 程式碼的運算式建立匯總函式。UDAF 會接受輸入資料欄、一次對一組資料列執行計算，然後將計算結果以單一值的形式傳回。

UDAF 無法變動資料、與外部系統通訊，或將記錄傳送至 Google Cloud Observability 或類似應用程式。

詳情請參閱下列資源：

* [使用者定義的匯總函式](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw)
* [限制](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw#limitations)
* [SQL 聚合函式參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw)

### SQL UDAF

SQL UDAF 通常會匯總[群組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#group_by_clause)中所有資料列的函式參數。不過，您可以使用 `NOT AGGREGATE` 關鍵字，將函式參數指定為非匯總參數。非匯總函式參數是純量函式參數，在群組的所有資料列中具有常數值。SQL UDAF 可包含匯總和非匯總參數。

### JavaScript UDAF

JavaScript UDAF 可以包含 JavaScript 程式庫。JavaScript 函式主體可以包含自訂 JavaScript 程式碼，例如 JavaScript 全域變數和自訂函式。

由於以 JavaScript 為基礎的函式通常會使用更多資源，因此建議您參考這些[效能提示](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw#performance-tips)。

JavaScript UDAF 有一些限制。僅允許[特定類型的編碼](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw#javascript-type-encodings)，且序列化和還原序列化有[相關規定](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw#serialize-javascript-udaf)。

## 比較 UDF 和 UDAF

選擇 UDF 而非 UDAF，取決於您嘗試執行的特定工作。

* 如要對個別資料值執行計算或轉換，請使用 UDF。
* 如要對資料值群組執行相同作業，請使用 UDAF。

舉例來說，如要計算一欄數字的平均值，請使用 UDAF。如要將字串欄轉換為大寫，請使用 UDF。

UDF 和 UDAF 的相似之處如下：

* UDF 和 UDAF 無法變更資料、與外部系統通訊，或將記錄傳送至 Google Cloud Observability 或類似應用程式。但 Python UDF 例外，這類函式可透過 Cloud 資源連結存取外部服務。不過，Python UDF 不支援 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw) 或[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)。
* UDAF 與 UDF 有相同的限制，此外還有[一些限制](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw#limitations)。
* UDF 和 UDAF 具有相同的[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#udf_limits)。

UDF 和 UDAF 的差異如下：

| **屬性** | **UDF** | **UDAF** |
| --- | --- | --- |
| 定義 | 使用者定義函式 (UDF) 可接受輸入資料欄、對輸入內容執行動作，並將執行結果以值的形式傳回。 | 使用者定義的匯總函式 (UDAF) 會接受輸入資料欄，一次對一組資料列執行計算，然後以單一值的形式傳回計算結果。 |
| 支援的語言 | SQL、JavaScript 和 Python | SQL 和 JavaScript |
| 持續性 | * 可以是暫時性或永久性。 * 您可以在多個查詢中重複使用永久性 UDF。 * 暫時性 UDF 只能用於單一查詢。 * Python UDF 只能是永久性，不能是暫時性。 | * 可以是暫時性或永久性。 * 您可以在多個查詢中重複使用永久性 UDAF。 * 暫時性 UDAF 只能用於單一查詢、指令碼、工作階段或程序。 * 在擁有者之間共用時，可以安全地呼叫持續性 UDAF。 |
| 引數和資料類型 | UDF 接受的參數值須符合 BigQuery [資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)的 GoogleSQL。有些 SQL 類型可以直接對應至 JavaScript 類型，其他類型則不能。請參閱 [JavaScript 支援的類型](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#supported-javascript-udf-data-types)。  如為 SQL UDF，參數值可以是 `ANY TYPE`，在呼叫函式時，可以比對多個引數類型。  只有 JavaScript UDF 具有決定性指定符，可向 BigQuery 提供查詢結果是否可快取的提示。 | SQL 和 JavaScript UDAF 接受符合 BigQuery [資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)的參數值。  函式參數可以是匯總或非匯總。 |
| 用量 | UDF 通常用於資料清理、轉換和驗證。 | UDAF 通常用於計算摘要統計資料，例如平均值、總和和計數。 |

## 資料表函式

資料表函式也稱為資料表值函式 (TVF)，是一種會傳回資料表的 UDF。您可以在任何可使用表格的地方使用表格函式。
資料表函式的行為與檢視類似，但資料表函式可以採用參數。

您可以使用表格函式執行下列操作：

* 傳入多個參數。
* 在任何表格有效的環境中呼叫表格函式。
* 將資料表函式的輸出內容與另一個資料表彙整。
* 在[子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#array_subquery_concepts)中使用資料表函式。

如要進一步瞭解表格函式，請參閱「[表格函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)」、「[限制](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw#limitations)」和「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_function_limits)」。

## 遠端函式

透過遠端函式，您可以使用 SQL 和 JavaScript 以外的語言實作函式，也可以使用 BigQuery UDF 不支援的程式庫或服務。

BigQuery 遠端函式會整合 Google SQL 函式與 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)和 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw) (使用任何支援的語言)，然後從 Google SQL 查詢中叫用這些函式。

以下是可透過遠端函式執行的工作範例：

* [分析物件資料表中的非結構化資料](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)。
* [翻譯內容](https://docs.cloud.google.com/bigquery/docs/remote-functions-translation-tutorial?hl=zh-tw)。

建立遠端函式需要執行下列步驟：

1. 在 Cloud Run 函式或 Cloud Run 中建立 HTTP 端點。
2. 使用 `CLOUD_RESOURCE` 連線類型在 BigQuery 中建立遠端函式。
3. 在查詢中使用遠端函式，就像使用任何其他 BigQuery 的 UDF 一樣。

如要進一步瞭解遠端函式，請參閱「[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)」、「[限制](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#limitations)」和「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

## 預存程序

SQL 預存程序是一組陳述式，可從其他查詢或其他預存程序呼叫。您可以在 BigQuery 資料集中命名及儲存程序。

預存程序支援程序語言陳述式，可讓您執行定義變數和實作控制流程等動作。如要進一步瞭解程序語言陳述式，請參閱「[程序語言參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)」。

預存程序可以執行下列操作：

* 將輸入引數做為輸入內容，並將傳回值做為輸出內容。
* 多位使用者存取或修改多個資料集中的資料。
* 包含[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)。

部分預存程序已內建於 BigQuery，不需建立。這些程序稱為系統程序，如要進一步瞭解，請參閱「[系統程序參考資料](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw)」。

系統也支援 [BigQuery 中的 Spark](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw) 預存程序。這些程序有[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#spark-procedure)。

如要進一步瞭解預存程序，請參閱「[SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]