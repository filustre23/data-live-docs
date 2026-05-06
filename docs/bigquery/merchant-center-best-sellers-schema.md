Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 暢銷商品資料表

## 總覽

你可以使用暢銷商品報表，查看 Google 購物和購物廣告中的暢銷產品和品牌。您可以根據這份報表的資訊，瞭解哪些產品在 Google 上的成效良好，以及你是否販售這些產品。

選取要轉移的暢銷商品報表後，系統會建立五個表格。
針對特定商家 ID，報表會建立下列資料表：

* `BestSellersBrandWeekly_MERCHANT_ID`
* `BestSellersBrandMonthly_MERCHANT_ID`
* `BestSellersProductClusterWeekly_MERCHANT_ID`
* `BestSellersProductClusterMonthly_MERCHANT_ID`
* `BestSellersEntityProductMapping_MERCHANT_ID`

如果是 MCA 帳戶，報表會產生下列表格：

* `BestSellersBrandWeekly_AGGREGATOR_ID`
* `BestSellersBrandMonthly_AGGREGATOR_ID`
* `BestSellersProductClusterWeekly_AGGREGATOR_ID`
* `BestSellersProductClusterMonthly_AGGREGATOR_ID`
* `BestSellersEntityProductMapping_AGGREGATOR_ID`

暢銷商品表格會根據 [Google Merchant Center](https://support.google.com/merchants/answer/9488679?hl=zh-tw) 的每月或每週暢銷商品報表 (產品和品牌) 產生。最新的每月或每週快照每天都會更新。由於資料會在每週或每月初更新，因此部分資料可能會連續幾天重複出現。系統預計每週或每月都會更新前一週期的熱銷產品資料。指標中納入的新資料最多可能需要兩週才會顯示。

對應表 `BestSellersEntityProductMapping_` 包含 `BestSellersProductCluster<Weekly/Monthly>_` 表格中的排名實體 ID，以及商家目錄中對應的產品 ID。在 MCA 層級產生時，表格會包含所有子帳戶的對應資料。這個表格用於將暢銷商品資料與 Merchant Center 轉移匯出的其他表格資訊合併，這些表格具有相同的產品 ID 格式 (產品、店面商品目錄、區域商品目錄、價格洞察、價格競爭力、產品目標對象)。

雖然品牌會依許多不同類別排名，但`Products_` 表格中的所有產品都屬於葉節點類別。如要在非葉子類別中加入品牌和產品，請使用 `google_product_category_ids` 欄位。

**注意：** 如要存取暢銷商品資料，你必須符合[市場洞察的資格規定](https://support.google.com/merchants/answer/9712881?hl=zh-tw)。

## `BestSellersProductCluster<Weekly/Monthly>_` 個資料表

| **欄** | **BigQuery 資料類型** | **說明** | **範例資料** |
| --- | --- | --- | --- |
| `country_code` | `STRING` | 產品銷售國家/地區。並非所有國家/地區都會有排名資料。詳情請參閱[適用國家/地區清單](https://support.google.com/merchants/answer/13299535?hl=zh-tw#Availability)。 | CH |
| `report_category_id` | `INTEGER` | 售出產品的 [Google 產品類別 ID](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 | 1234 |
| `title` | `STRING` | 暢銷產品叢集的標題。 | TN2351 黑色 USB |
| `brand` | `STRING` | 暢銷產品群組的品牌。如果沒有品牌，請設為空值。 | 品牌名稱 |
| `category_l1` | `STRING` | 熱銷產品群組的 Google 產品類別。如果沒有類別，請設為空字串。 | 動物與寵物用品 |
| `category_l2` | `STRING` | 熱銷產品群組的 Google 產品類別。如果沒有類別，請設為空字串。 | 寵物用品 |
| `category_l3` | `STRING` | 熱銷產品群組的 Google 產品類別。如果沒有類別，請設為空字串。 | 狗用品 |
| `category_l4` | `STRING` | 熱銷產品群組的 Google 產品類別。如果沒有類別，請設為空字串。 | 狗床 |
| `category_l5` | `STRING` | 熱銷產品群組的 Google 產品類別。 |  |
| `variant_gtins` | `STRING` | 與這個產品群組相應的商品目錄中產品的[全球交易品項識別碼](https://support.google.com/merchants/answer/6324461?hl=zh-tw)，每個識別碼之間以空格分隔。 | 3234567890126 3234567890131 |
| `product_inventory_status` | `STRING` | 產品在商品目錄中的狀態。在 MCA 層級的表格中，值一律為 `NOT_IN_INVENTORY` 或 `UNKNOWN`。如要取得子帳戶的商品目錄狀態，請將 `BestSellersEntityProductMapping_` 資料表與 `Products_` 資料表彙整。 | IN\_STOCK、NOT\_IN\_INVENTORY、OUT\_OF\_STOCK |
| `brand_inventory_status` | `STRING` | 根據這個品牌的產品狀態，顯示該品牌在您庫存中的狀態。如果沒有品牌，請設為 `UNKNOWN`。 | IN\_STOCK、NOT\_IN\_INVENTORY、OUT\_OF\_STOCK |
| `entity_id` | `STRING` | 這個排名最高的暢銷商品項目的 ID。這個資料欄用於使用 `BestSellersEntityProductMapping` 資料表，與其他資料表彙整。 | ab12345cdef6789gh |
| `rank` | `INTEGER` | 產品排名 (排名越低，表示產品越暢銷)。 | 5 |
| `previous_rank` | `INTEGER` | 產品在上一個週期 (週或月) 的排名。 | 5 |
| `relative_demand` | `STRING` | 與同一類別和國家/地區中排名最高的產品相比，某項產品的預估需求。 | VERY\_HIGH、HIGH、MEDIUM、LOW、VERY\_LOW |
| `previous_relative_demand` | `STRING` | 與前一週或前一個月相比，這項產品的相對需求值。如果沒有先前的需求，請設為 `null`。 | VERY\_HIGH、HIGH、MEDIUM、LOW、VERY\_LOW |
| `relative_demand_change` | `STRING` | 與前一週或前一個月相比，這項產品的相對需求變化。如果沒有先前的需求，請設為 `UNKNOWN`。 | FLAT、SINKER、RISER |
| `price_range` | `RECORD` | 價格範圍：下限和上限 (不含小數) 和幣別。價格不含運費。 | 不適用 |
| `price_range.min_amount_micros` | `NUMERIC` | 商品價格，以微量單位表示 (1 代表 1000000)。 | 115000000 |
| `price_range.max_amount_micros` | `NUMERIC` | 商品價格，以微量單位表示 (1 代表 1000000)。 | 147000000 |
| `price_range.currency_code` | `STRING` | 商品價格範圍的幣別。 | 澳幣 |
| `snapshot_date` | `STRING` | 計算表格的日期。每月資料表的格式為 `M%Y%m`，每週資料表的格式為 `W%Y%m%D`。 | M202601、W20260216 |

**注意：** 這些資料表沒有主鍵。

## `BestSellersBrand<Weekly/Monthly>_` 個資料表

| **欄** | **BigQuery 資料類型** | **說明** | **範例資料** |
| --- | --- | --- | --- |
| `brand` | `STRING` | 暢銷品牌。 | 品牌名稱 |
| `category_id` | `INTEGER` | 暢銷品牌的 [Google 產品類別 ID](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 | 1234 |
| `country_code` | `STRING` | 銷售暢銷品牌的國家/地區。詳情請參閱[適用國家/地區清單](https://support.google.com/merchants/answer/13299535?hl=zh-tw#Availability)。 | CH |
| `rank` | `INTEGER` | 暢銷品牌排名 (排名越低，表示銷量越高)。 | 5 |
| `previous_rank` | `INTEGER` | 上個週期 (週或月) 的暢銷品牌排名。如果沒有先前的排名，請設為 `0`。 | 5 |
| `relative_demand` | `STRING` | 與同一類別和國家/地區中排名最高的產品相比，某項產品的預估需求。 | VERY\_HIGH、HIGH、MEDIUM、LOW、VERY\_LOW |
| `previous_relative_demand` | `STRING` | 前一週或前一個月的相對需求。如果沒有先前的需求，請設為 `null`。 | VERY\_HIGH、HIGH、MEDIUM、LOW、VERY\_LOW |
| `relative_demand_change` | `STRING` | 與前一期 (週或月) 相比的需求變化。如果沒有先前的排名，請設為 `UNKNOWN`。 | FLAT、SINKER、RISER |
| `snapshot_date` | `STRING` | 計算表格的日期。每月資料表的格式為 `M%Y%m`，每週資料表的格式為 `W%Y%m%D`。 | M202601、W20260216 |

**注意：** 這些資料表沒有主鍵。

## `BestSellersEntityProductMapping_` 個資料表

| **欄** | **BigQuery 資料類型** | **說明** | **範例資料** |
| --- | --- | --- | --- |
| `merchant_id` | `INTEGER` | Merchant Center 帳戶 ID。 如果您在 MCA 層級查詢資料表，這個欄位會包含子帳戶商家 ID。如果您查詢獨立帳戶或子帳戶的資料表，這個欄位會包含商家帳戶 ID。 | 1234 |
| `product_id` | `STRING` | 產品的 REST ID，格式為：`channel:content_language:feed_label:offer_id`。這個 ID 一律會反映資料匯出至 BigQuery 時的最新產品狀態。這是與所有其他包含此格式產品 ID 的資料表聯結的鍵。 | online:en:AU:666840730 |
| `entity_id` | `STRING` | 排名最高的暢銷商品項目的 ID。這是與 `BestSellersProductCluster&ltWeekly/Monthly>_` 資料表的彙整索引鍵。 | ab12345cdef6789gh |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]