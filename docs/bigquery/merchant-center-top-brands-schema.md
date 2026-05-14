Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 熱門品牌資料表

## 總覽

**注意：** 自 2025 年 9 月 1 日起，BigQuery 將不再支援匯出「熱門品牌」資料表的報表。建議您改用[新版暢銷商品報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-tw)。如要進一步瞭解如何遷移至新報表，請參閱「[遷移暢銷商品報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-migration?hl=zh-tw)」。

暢銷商品資料可協助商家瞭解購物廣告和免付費產品資訊中最熱銷的品牌和產品。如要進一步瞭解暢銷商品，請參閱「[支援的報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw#supported_reports)」中的說明。

資料會寫入名為 `BestSellers_TopBrands_MERCHANT_ID` 的資料表。

## 結構定義

`BestSellers_TopBrands_` 資料表具有下列結構定義：

| **欄** | **BigQuery 資料類型** | **說明** | **資料範例** |
| --- | --- | --- | --- |
| `rank_timestamp` | `TIMESTAMP` | 發布排名的日期和時間。 | 2020 年 5 月 30 日 00:00:00 (世界標準時間) |
| `rank_id` | `STRING` | 排名的專屬 ID。 | 2020-05-30:FR:264:120:brand |
| `rank` | `INTEGER` | 品牌在 `ranking_country` 和 `ranking_category` 的購物廣告和免費產品資訊中的熱銷度排名。熱銷程度是由產品的預估銷量計算而來。排名會每天更新。指標中的資料最多可能會延遲 2 天。 | 120 |
| `previous_rank` | `INTEGER` | 過去 7 天內的排名變化。 | 86 |
| `ranking_country` | `STRING` | 用於排名的國家/地區代碼。 | FR |
| `ranking_category` | `INTEGER` | 用於排名的 [Google 產品類別 ID](https://support.google.com/merchants/answer/1705911?hl=zh-tw)。 | 264 |
| `ranking_category_path` | `RECORD, REPEATED` | 用於各個語言代碼排名的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw)完整路徑。 |  |
| `ranking_category_path.locale` | `STRING` | 類別路徑的語言代碼。 | en-US |
| `ranking_category_path.name` | `STRING` | 使用者可解讀的類別路徑名稱。 | 電子器材 > 通訊設備 > 電話設備 > 手機配件 |
| `relative_demand` | `RECORD` | 與同一類別和國家/地區中熱銷度排名最高的品牌相比，某個品牌的預估需求。 |  |
| `relative_demand.bucket` | `STRING` |  | 極高 |
| `relative_demand.min` | `INTEGER` |  | 51 |
| `relative_demand.max` | `INTEGER` |  | 100 |
| `previous_relative_demand` | `RECORD` | 與同一類別和國家/地區中過去 7 天熱銷度排名最高的品牌相比，某個品牌的預估需求。 |  |
| `previous_relative_demand.bucket` | `STRING` |  | 極高 |
| `previous_relative_demand.min` | `INTEGER` |  | 51 |
| `previous_relative_demand.max` | `INTEGER` |  | 100 |
| `brand` | `STRING` | 商品品牌。 | 品牌名稱範例 |
| `google_brand_id` | `STRING` | 商品的 Google 品牌 ID。 | 11887454107284768325 |

## 查詢範例

### 特定類別和國家/地區的熱門品牌

下列 SQL 查詢會傳回美國 `Smartphones` 類別的前幾個品牌。

```
SELECT
  rank,
  previous_rank,
  brand
FROM
  dataset.BestSellers_TopBrands_merchant_id
WHERE
  _PARTITIONDATE = 'YYYY-MM-DD' AND
  ranking_category = 267 /*Smartphones*/ AND
  ranking_country = 'US'
ORDER BY
  rank
```

**注意：** 如要進一步瞭解產品類別 (包括完整的類別代碼清單)，請參閱「[定義：`google_product_category`](https://support.google.com/merchants/answer/6324436?hl=zh-tw)」。

### 商品目錄中熱門品牌的產品

以下 SQL 查詢會傳回熱門品牌的產品目錄清單，並依類別和國家/地區列出。

```
  WITH latest_top_brands AS
  (
    SELECT
      *
    FROM
      dataset.BestSellers_TopBrands_merchant_id
    WHERE
      _PARTITIONDATE = 'YYYY-MM-DD'
  ),
  latest_products AS
  (
    SELECT
      product.*,
      product_category_id
    FROM
      dataset.Products_merchant_id AS product,
      UNNEST(product.google_product_category_ids) AS product_category_id,
      UNNEST(destinations) AS destination,
      UNNEST(destination.approved_countries) AS approved_country
    WHERE
      _PARTITIONDATE = 'YYYY-MM-DD'
  )
  SELECT
    top_brands.brand,
    (SELECT name FROM top_brands.ranking_category_path
    WHERE locale = 'en-US') AS ranking_category,
    top_brands.ranking_country,
    top_brands.rank,
    products.product_id,
    products.title
  FROM
    latest_top_brands AS top_brands
  INNER JOIN
    latest_products AS products
  ON top_brands.google_brand_id = products.google_brand_id AND
     top_brands.ranking_category = product_category_id AND
     top_brands.ranking_country = products.approved_country
```

**注意：** 如要進一步瞭解產品類別 (包括完整的類別代碼清單)，請參閱「[定義：`google_product_category`](https://support.google.com/merchants/answer/6324436?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]