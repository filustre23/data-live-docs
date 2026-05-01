* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料洞察總覽

本文將概略介紹資料洞察功能。這項 Gemini in BigQuery 功能可協助您在面對新資料或不熟悉的資料時，加速初步探索和分析。資料洞察功能會根據資料表和資料集的中繼資料，自動生成說明、關係圖和 SQL 查詢，以及以自然語言提出的建議問題。這項資訊可協助您快速瞭解資料結構、內容和關係，不必手動設定大量項目。

**注意：** 如要提供這項功能的意見回饋，請傳送電子郵件至 [dataplex-data-insights-help@google.com](mailto:dataplex-data-insights-help@google.com)。

## 事前準備

資料洞察資訊是使用 [Gemini in BigQuery](https://docs.cloud.google.com/gemini/docs/bigquery/overview?hl=zh-tw) 生成。
如要開始生成洞察，請先[設定 Gemini in BigQuery](https://docs.cloud.google.com/gemini/docs/bigquery/set-up-gemini?hl=zh-tw)。

**注意**：Gemini in BigQuery 屬於 Gemini for Google Cloud 的一部分，符合的法規遵循和安全性要求與 BigQuery 不同。
只有符合下列條件的 BigQuery 專案，才能設定 Gemini in BigQuery：所需[法規遵循服務都在 Gemini for Google Cloud 的支援範圍內 Google Cloud](https://docs.cloud.google.com/gemini/docs/discover/certifications?hl=zh-tw)。
如要瞭解如何停用或禁止存取 Gemini in BigQuery，請參閱「[停用 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw#turn-off)」。

## 資料洞察類型

您可以在資料表或資料集層級生成資料洞察：

* **資料表：**Gemini 會生成自然語言問題和對應的 SQL，協助您瞭解單一資料表中的資料。透過資料表洞察，您可以偵測資料表中的資料模式、異常狀況、離群值或品質問題。Gemini 也會生成資料表和資料欄說明。
* **資料集：**
  ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
  Gemini 會生成互動式關係圖，顯示跨表格關係和跨表格 SQL 查詢，協助您瞭解資料集中的表格關係。透過關係圖，您可以瞭解資料的衍生方式，有助於解決品質、一致性或備援問題。透過跨資料表查詢，您可以找出更廣泛的關係。舉例來說，您可以運用銷售資料表和顧客資料表中的資料，計算各顧客區隔的收益。

如要進一步調查，可以在[資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)中提出後續問題。

### 資料表深入分析結果

資料表洞察可協助您瞭解單一 BigQuery 資料表中的內容、品質和模式。舉例來說，您可以產生執行統計分析的查詢，並使用資料表洞察功能偵測資料模式、異常狀況和離群值。此外，資料表洞察資訊也有助於偵測品質問題，特別是當資料表提供[資料剖析掃描](https://docs.cloud.google.com/dataplex/docs/data-profiling-overview?hl=zh-tw)時。為資料表生成洞察結果時，Gemini 會根據資料表的中繼資料提供資料表說明、資料欄說明和剖析掃描輸出內容。可用的選項如下：

* **生成查詢：**建議自然語言問題，並提供對應的 SQL 查詢來回答問題。這有助於您發掘模式、評估資料品質，以及執行統計分析，無須從頭編寫 SQL。
* **生成說明：**為資料表及其資料欄生成說明。Gemini 會使用剖析掃描輸出內容 (如有)，做為生成說明時的依據。您可以查看、編輯這些說明，並發布至知識目錄，提升資料可探索性和文件品質。

### 資料集洞察

資料集洞察可協助您瞭解 BigQuery 資料集內多個資料表之間的關係和聯結路徑，全面掌握資料集內容。為資料集生成洞察資料時，Gemini 會提供下列資訊：

* **資料集說明：**提供 AI 生成的資料集摘要。
* **關係：**顯示互動式地圖，以視覺化方式呈現資料集內資料表之間的關係。將游標懸停在連線上，即可查看關係詳細資料，例如合併鍵。
* **關係表：**以表格形式呈現資料表之間的關係，包括外鍵和推斷的聯結。關係可由結構定義 (來自主鍵和外鍵限制)、根據使用情況 (來自查詢記錄)，或由 Gemini 根據資料表和資料欄名稱與說明推斷。
* **查詢建議：**根據已識別的關係，提供範例 SQL 查詢，說明如何聯結不同資料表中的資料。

## 資料表資料洞察範例

假設有一個名為 `telco_churn` 的資料表，其中包含 `CustomerID`、`Tenure`、`InternetService`、`Contract`、`MonthlyCharges` 和 `Churn` 等資料欄。
下表說明資料表的 metadata。

| 欄位名稱 | 類型 |
| --- | --- |
| `CustomerID` | `STRING` |
| `Gender` | `STRING` |
| `Tenure` | `INT64` |
| `InternetService` | `STRING` |
| `StreamingTV` | `STRING` |
| `OnlineBackup` | `STRING` |
| `Contract` | `STRING` |
| `TechSupport` | `STRING` |
| `PaymentMethod` | `STRING` |
| `MonthlyCharges` | `FLOAT64` |
| `Churn` | `BOOL` |

資料洞察會為這個資料表生成下列查詢範例：

* 找出訂閱所有進階服務，且已成為客戶超過 50 個月的使用者。

  ```
  SELECT
    CustomerID,
    Contract,
    Tenure
  FROM
    agentville_datasets.telco_churn
  WHERE
    OnlineBackup = 'Yes'
    AND TechSupport = 'Yes'
    AND StreamingTV = 'Yes'
    AND Tenure > 50;
  ```
* 找出流失最多顧客的網際網路服務。

  ```
  SELECT
    InternetService,
    COUNT(DISTINCT CustomerID) AS customers
  FROM
    agentville_datasets.telco_churn
  WHERE
    Churn = TRUE
  GROUP BY
    InternetService
  ORDER BY
    customers DESC
  LIMIT 1;
  ```

## 資料集資料洞察資訊範例

假設資料集包含 `order_items` 和 `inventory_items` 資料表。資料集洞察資料可推斷 `order_items.inventory_item_id` 與 `inventory_items.id` 相關。

根據這些關係，Gemini 可能會生成下列跨資料表查詢：

找出平均售價最高的前 5 個產品類別，以及對應的平均成本。

```
SELECT
  ii.product_category,
  AVG(oi.sale_price) AS avg_sale_price,
  AVG(ii.cost) AS avg_cost
FROM
  `ecommerce_data.order_items` AS oi
JOIN
  `ecommerce_data.inventory_items` AS ii
ON oi.inventory_item_id = ii.id
GROUP BY
  ii.product_category
ORDER BY
  avg_sale_price DESC
LIMIT 5;
```

## 資料洞察工作流程

本節將說明不同使用者角色可透過 BigQuery 的資料洞察功能執行的主要工作流程。

### 資料消費者工作流程

這些工作流程著重於資料分析師、業務分析師，以及其他需要尋找、瞭解及分析資料的使用者。

* **瞭解 BigQuery 資料表：**快速掌握特定資料表的結構定義、內容和潛在用途。在 BigQuery Studio 中選取資料表後，您可以執行下列工作：

  + 查看自動生成的資料表和資料欄說明。
  + 查看建議的自然語言問題和對應的 SQL 查詢，瞭解資料細微差異。
  + 調整並執行建議的查詢，開始進行分析。

  如要進一步瞭解如何產生及查看資料表洞察資料，請參閱「[產生資料表洞察資料](https://docs.cloud.google.com/bigquery/docs/generate-table-insights?hl=zh-tw)」。
* **探索整個資料集：**發掘資料集內各個表格之間的關係，並瞭解整體結構。在 BigQuery Studio 中選取資料集後，即可執行下列工作：

  + 產生及查看資料集洞察資訊。
  + 使用互動式關係圖，以視覺化方式呈現表格連結。
  + 分析關係資料表，找出聯結鍵和連線類型 (結構定義、以使用情況為準、LLM 推斷)。
  + 使用建議的跨資料表 SQL 查詢，有效查詢多個資料表。

  如要進一步瞭解如何產生及查看資料集洞察資料，請參閱「[產生資料集洞察資料](https://docs.cloud.google.com/bigquery/docs/generate-dataset-insights?hl=zh-tw)」。

### 資料生產者工作流程

這些工作流程適用於資料工程師、分析工程師，以及其他負責建構及管理資料資產的人員。

* **產生基準資料說明文件：**自動建立及維護必要的中繼資料說明。您可以執行下列工作：

  + 建立或修改資料表後，觸發資料洞察功能，即可生成資料表和資料欄說明。您也可以使用 [Knowledge Catalog 自動中繼資料生成 API](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#add-aspects)，大規模生成這些說明。
  + 檢查並修正 AI 生成的文字，確保技術正確性及業務相關性。

  如要進一步瞭解如何產生資料表和資料欄說明，請參閱「[產生資料表洞察](https://docs.cloud.google.com/bigquery/docs/generate-table-insights?hl=zh-tw)」。
* **協助使用者更瞭解資料集**：讓消費者更容易瞭解及使用提供的資料集。您可以執行下列工作：

  + 針對重要資料集 (尤其是關係複雜的資料集) 產生深入分析資訊。
  + 請務必在資料表上執行資料剖析掃描，以提供豐富的背景資訊，進而取得更準確實用的洞察資料。

  詳情請參閱「[產生資料集洞察](https://docs.cloud.google.com/bigquery/docs/generate-dataset-insights?hl=zh-tw)」和「[根據資料剖析結果提供洞察](https://docs.cloud.google.com/dataplex/docs/data-profiling-overview?hl=zh-tw)」。

### 資料管理員的工作流程

這些工作流程可協助資料管理員和管理團隊維護資料完整性和信任度。

* **驗證及稽核 AI 生成的中繼資料：**確保資料洞察功能生成的中繼資料準確可靠。您可以執行下列工作：

  + 定期檢查洞察功能生成的說明和關係。
  + 交叉比對關係圖中的推論關係與已建立的資料模型和商業邏輯。
  + 檢查並修正 AI 生成中繼資料的不準確之處。

  詳情請參閱「[產生資料表洞察資料](https://docs.cloud.google.com/bigquery/docs/generate-table-insights?hl=zh-tw)」和「[產生資料集洞察資料](https://docs.cloud.google.com/bigquery/docs/generate-dataset-insights?hl=zh-tw)」。

## 定價

如要瞭解這項功能的定價詳情，請參閱 [Gemini in BigQuery 定價總覽](https://docs.cloud.google.com/gemini/pricing?hl=zh-tw#gemini-in-bigquery-pricing)。

## 配額與限制

如要瞭解這項功能的配額和限制，請參閱「[Gemini in BigQuery 的配額](https://docs.cloud.google.com/gemini/docs/quotas?hl=zh-tw#bigquery)」。

## 限制

資料洞察有下列限制：

* 資料洞察功能適用於 BigQuery 資料表、BigLake 資料表、外部資料表和檢視區塊。
* 多雲端客戶無法使用其他雲端的資料。
* 資料洞察不支援 `GEO` 或 `JSON` 欄類型。
* 洞察資料執行作業不保證每次都會顯示查詢。如要提高生成更吸引人查詢的機率，請重新啟動洞察管道。
* 如果資料表設有資料欄層級存取控管機制，且使用者權限受到限制，只要您有權讀取資料表的所有資料欄，就能產生洞察資料。如要執行產生的查詢，您必須具備足夠的[權限](https://docs.cloud.google.com/bigquery/docs/generate-table-insights?hl=zh-tw#roles)。
* Gemini 最多可為資料表中的 350 個資料欄生成說明。
* 如果是資料集洞察，您無法在關係圖中編輯關係。
* 產生新的資料集洞察資料時，系統會覆寫該資料集先前的洞察資料。
* 資料集洞察不支援連結的資料集。

## 位置

您可以在所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)使用資料洞察。如要瞭解 Gemini in BigQuery 在何處處理資料，請參閱「[Gemini in BigQuery 在何處處理資料](https://docs.cloud.google.com/bigquery/docs/gemini-locations?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[生成表格洞察](https://docs.cloud.google.com/bigquery/docs/generate-table-insights?hl=zh-tw)。
* 瞭解如何[產生資料集洞察](https://docs.cloud.google.com/bigquery/docs/generate-dataset-insights?hl=zh-tw)。
* 進一步瞭解[知識目錄資料剖析](https://docs.cloud.google.com/dataplex/docs/data-profiling-overview?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中使用 Gemini 撰寫查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw)。
* 進一步瞭解 [Gemini 版 BigQuery](https://docs.cloud.google.com/gemini/docs/bigquery/overview?hl=zh-tw)。
* 瞭解如何使用 [Data Canvas](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)，以自然語言提問來反覆查詢結果。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]