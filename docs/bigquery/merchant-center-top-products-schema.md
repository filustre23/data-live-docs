Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 熱門產品

## 總覽

**注意：** 自 2025 年 9 月 1 日起，BigQuery 將不再支援這個版本的熱門產品資料表。建議您改用[新版暢銷商品報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-tw)。如要進一步瞭解如何遷移至新報表，請參閱「[遷移暢銷商品報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-migration?hl=zh-tw)」。

暢銷商品資料可協助商家瞭解購物廣告中最熱銷的品牌和產品。如要進一步瞭解暢銷商品，請參閱「[支援的報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw#supported_reports)」中的說明。

資料會寫入名為 `BestSellers_TopProducts_MERCHANT_ID` 的資料表。

## 結構定義

`BestSellers_TopProducts_` 資料表具有下列結構定義：

| **欄** | **BigQuery 資料類型** | **說明** | **欄位範例** |
| --- | --- | --- | --- |
| `rank_timestamp` | `TIMESTAMP` | 發布排名的日期和時間。 | 2020 年 3 月 14 日 00:00:00 (世界標準時間) |
| `rank_id` | `STRING` | 與「產品目錄」表彙整的排名 ID。 | 2020-03-14:AU:100:2:product |
| `rank` | `INTEGER` | 產品在購物廣告中，針對「排名國家/地區」和「排名類別」的熱銷度排名。熱銷度是根據產品的預估銷售量計算而來。排名會每天更新。指標中的資料最多可能會延遲 2 天。 | 2 |
| `previous_rank` | `INTEGER` | 過去 7 天內的排名變化。 | 4 |
| `ranking_country` | `STRING` | 用於排名的國家/地區代碼。 | AU |
| `ranking_category` | `INTEGER` | 用於排名的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw) ID。 | 5181 |
| `ranking_category_path` | `RECORD,  REPEATED` | 用於排名的每個語言代碼的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw)完整路徑。 |  |
| `ranking_category_path.locale` | `STRING` |  | en-AU |
| `ranking_category_path.name` | `STRING` |  | 行李與提袋 |
| `relative_demand` | `RECORD` | 與同一類別和國家/地區中熱銷度排名最高的產品相比，某項產品的預估需求。 |  |
| `relative_demand.bucket` | `STRING` |  | 極高 |
| `relative_demand.min` | `INTEGER` |  | 51 |
| `relative_demand.max` | `INTEGER` |  | 100 |
| `previous_relative_demand` | `RECORD` | 與同一類別和國家/地區中過去 7 天熱銷度排名最高的產品相比，某項產品的預估需求。 |  |
| `previous_relative_demand.bucket` | `STRING` |  | 極高 |
| `previous_relative_demand.min` | `INTEGER` |  | 51 |
| `previous_relative_demand.max` | `INTEGER` |  | 100 |
| `product_title` | `RECORD,  REPEATED` | 產品名稱。 |  |
| `product_title.locale` | `STRING` |  | en-AU |
| `product_title.name` | `STRING` |  | ExampleBrand 後背包 |
| `gtins` | `STRING,  REPEATED` | [全球交易品項識別碼](https://support.google.com/merchants/answer/188494?hl=zh-tw#gtin) (GTIN)。 | 07392158680955 |
| `brand` | `STRING` | 商品品牌。 | ExampleBrand |
| `google_brand_id` | `STRING` | 商品的 Google 品牌 ID。 | 11887454107284768328 |
| `google_product_category` | `INTEGER` | 商品的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw) ID。 | 100 |
| `google_product_category_path` | `RECORD,  REPEATED` | 商品的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw)完整路徑。 |  |
| `google_product_category_path.locale` | `STRING` |  | en-US |
| `google_product_category_path.name` | `STRING` |  | Luggage & Bags > Backpacks |
| `price_range` | `RECORD` | 價格範圍：下限和上限 (不含小數點) 和貨幣。價格不含運費。 | 不適用 |
| `price_range.min` | `NUMERIC` |  | 115 |
| `price_range.max` | `NUMERIC` |  | 147 |
| `price_range.currency` | `STRING` |  | 澳幣 |

## 瞭解資料

* 排名類別可能會隨時間變更。
* `BestSellers_TopProducts_Inventory_` 表格的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)可能與 [`Products_`](https://docs.cloud.google.com/bigquery/docs/merchant-center-products-schema?hl=zh-tw) 表格的 Google 產品類別不同。`Products_` 表格會顯示零售商提供的 Google 產品類別值。
* 對於目錄中的產品，`BestSellers_TopProducts_` 中的價格範圍可能與 `Products_PriceBenchmarks_` 表格不同。價格基準指標的計算時間範圍不同。`BestSellers_TopProducts_` 中的價格範圍反映產品的不同子類價格，而 `Products_PriceBenchmarks_` 中的價格範圍只指單一子類。
* 商品目錄中的部分產品可能沒有路徑中每個類別的排名。每個類別的產品數量上限為 10,000 項，且在部分子類別中，我們不會發布任何排名。

## 範例

產品可能會在產品類別路徑中，為每個類別設定排名。舉例來說，Google Pixel 4 手機會歸類為 `Electronics >
Communications > Telephony > Mobile Phones`。Pixel 4 將分別在「電子產品」、「通訊」、「電話」和「行動電話」類別中排名。除了 `ranking_country` 之外，請使用 `ranking_category_path` 來判斷要查看哪個類別的排名。

在下方範例中，ExampleBrand 背包包含行李和背包類別的個別排名。選取「背包」和「AU」，即可查看背包類別在澳洲的排名。

### 「行李箱/袋」排名

| **product\_title** | **ExampleBrand 背包** |
| --- | --- |
| **ranking\_country** | AU |
| **ranking\_category** | 5181 |
| **ranking\_category\_path** | 行李與提袋 |
| **排名** | 40 |
| **google\_product\_category** | 100 |
| **google\_product\_category\_path** | Luggage & Bags > Backpacks |

### 排名：行李箱與提袋 > 背包

| **product\_title** | **ExampleBrand 背包** |
| --- | --- |
| **ranking\_country** | AU |
| **ranking\_category** | 100 |
| **ranking\_category\_path** | Luggage & Bags > Backpacks |
| **rank** | 4 |
| **google\_product\_category** | 100 |
| **google\_product\_category\_path** | Luggage & Bags > Backpacks |

## 查詢範例

### 特定類別和國家/地區的熱銷產品

以下 SQL 查詢會傳回美國 `Smartphones` 類別的熱門產品。

```
SELECT
  rank,
  previous_rank,
  relative_demand.bucket,
  (SELECT name FROM top_products.product_title WHERE locale = 'en-US') AS product_title,
  brand,
  price_range
FROM
  dataset.BestSellers_TopProducts_merchant_id AS top_products
WHERE
  _PARTITIONDATE = 'YYYY-MM-DD' AND
  ranking_category = 267 /*Smartphones*/ AND
  ranking_country = 'US'
ORDER BY
  rank
```

**注意：** 如要進一步瞭解產品類別 (包括完整的類別代碼清單)，請參閱「[定義：`google_product_category`](https://support.google.com/merchants/answer/6324436?hl=zh-tw)」。

### 商品目錄資料中的熱門產品

以下 SQL 查詢會彙整 `BestSellers_TopProducts_Inventory_` 和 `BestSellers_TopProducts_` 資料，傳回商品目錄中熱銷產品的清單。

```
WITH latest_top_products AS
(
  SELECT
    *
  FROM
    dataset.BestSellers_TopProducts_merchant_id
  WHERE
    _PARTITIONDATE = 'YYYY-MM-DD'
),
latest_top_products_inventory AS
(
  SELECT
    *
  FROM
    dataset.BestSellers_TopProducts_Inventory_merchant_id
  WHERE
    _PARTITIONDATE = 'YYYY-MM-DD'
)
SELECT
  top_products.rank,
  inventory.product_id,
  (SELECT ANY_VALUE(name) FROM top_products.product_title) AS product_title,
  top_products.brand,
  top_products.gtins
FROM
  latest_top_products AS top_products
INNER JOIN
  latest_top_products_inventory AS inventory
USING (rank_id)
```

**注意：** 如要進一步瞭解產品類別 (包括完整的類別代碼清單)，請參閱「[定義：`google_product_category`](https://support.google.com/merchants/answer/6324436?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]