Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 產品資料表結構定義

## 總覽

當你將 Google Merchant Center 報表資料移轉至 BigQuery 時，產品與產品問題資料的格式主要可對應至 Content API 中 [Products](https://developers.google.com/shopping-content/v2/reference/v2.1/products?hl=zh-tw) 和 [Productstatuses](https://developers.google.com/shopping-content/v2/reference/v2.1/productstatuses?hl=zh-tw) 資源的相關欄位格式。

如果您使用的是個別商家 ID，資料會寫入名為 `Products_MERCHANT_ID` 的資料表；如果您使用的是 MCA 帳戶，資料會寫入名為 `Products_AGGREGATOR_ID` 的資料表。

**注意：** 首次要求報表時，`Products and product issues` 資料並不會立即提供。首次針對商家或匯整 ID 要求轉移作業時，`Products_`資料表可能會延遲最多 1 天，才會開放匯出。

## 結構定義

`Products_` 資料表具有下列結構定義：

| 欄 | BigQuery 資料類型 | 說明 | 資料範例 |
| --- | --- | --- | --- |
| `product_data_timestamp` | `TIMESTAMP` | 產品資料的時間戳記。 | 2023-09-14 11:49:50 (世界標準時間) |
| `product_id` | `STRING` | 產品的 Content API REST ID，格式為：`channel:content_language:feed_label:offer_id`。這是主鍵。 | online:en:AU:666840730 |
| `merchant_id` | `INTEGER` | 商家帳戶 ID。 | 1234 |
| `aggregator_id` | `INTEGER` | 多重客戶帳戶的 Aggregator 帳戶 ID。 | 12345 |
| `offer_id` | `STRING` | 商家提供的[產品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-tw)。 | tddy123uk |
| `title` | `STRING` | 項目名稱。 | TN2351 黑色 USB |
| `description` | `STRING` | 商品的[說明](https://support.google.com/merchants/answer/6324468?hl=zh-tw)。 | TN2351 黑色 USB 重新定義了 XJS 對 LLCD 體驗的影響。 |
| `link` | `STRING` | 商家提供的產品[到達網頁網址](https://support.google.com/merchants/answer/6324416?hl=zh-tw)。 | https://www.example.com/tn2351-black-usb/6538811?skuId=1234 |
| `mobile_link` | `STRING` | 商家提供的到達網頁[行動最佳化版本網址](https://support.google.com/merchants/answer/6324459?hl=zh-tw)。 | https://www.example.com/tn2351-black-usb/6538811?skuId=1234 |
| `image_link` | `STRING` | 商家提供[主要產品圖片的網址](https://support.google.com/merchants/answer/6324350?hl=zh-tw)。 | https://www.example.com/tn2351-black-usb/6538811?skuId=1234 |
| `additional_image_links` | `STRING`、`REPEATED` | 商家提供商品圖片的[其他網址](https://support.google.com/merchants/answer/6324370?hl=zh-tw)。 |  |
| `content_language` | `STRING` | 商品的雙字母格式 ISO 639-1 語言編碼。 | en |
| `target_country` | `STRING` | 已淘汰 (一律設為空值)，這是為了讓產品[指定多個國家/地區](https://support.google.com/merchants/answer/7448571?hl=zh-tw)而做出的調整。如要讀取每個指定國家/地區的狀態，請使用下列欄位：[destinations.approved\_countries](#destinations.approved_countries)、[destinations.pending\_countries](#destinations.pending_countries)、[destinations.disapproved\_countries](#destinations.disapproved_countries)。問題現在可套用至特定的指定國家/地區，其他國家/地區則不適用，如 [issues.applicable\_countries](#issues.applicable_countries) 欄位所示。 | null |
| `feed_label` | `STRING` | 商家為商品提供[動態饋給標籤](https://support.google.com/merchants/answer/12453549?hl=zh-tw)，如果沒有提供，則為 `-`。 | 美國 |
| `channel` | `STRING` | 項目的通路，可為 `online` 或 `local`。 | 本地、線上 |
| `expiration_date` | `TIMESTAMP` | 商家提供[商品到期日](https://support.google.com/merchants/answer/6324499?hl=zh-tw) (於插播時指定)。如果未提供，則設為空值。 | 2023-10-14 00:00:00 (世界標準時間) |
| `google_expiration_date` | `TIMESTAMP` | Google 購物中商品到期的日期和時間。絕對不要設為空值。 | 2023-10-14 00:00:00 (世界標準時間) |
| `adult` | `BOOLEAN` | 如果是[成人面向的商品](https://support.google.com/merchants/answer/6324508?hl=zh-tw)，則設為 true。 | true/false |
| `age_group` | `STRING` | 商家提供的商品[目標年齡層](https://support.google.com/merchants/answer/6324463?hl=zh-tw)。如果未提供，則為 NULL。 | 新生兒、嬰兒、幼兒、兒童、成人 |
| `availability` | `STRING` | 商家提供的商品[供應情形](https://support.google.com/merchants/answer/6324448?hl=zh-tw)狀態。 | 有現貨、缺貨 |
| `availability_date` | `TIMESTAMP` | 商家提供[預購產品可出貨](https://support.google.com/merchants/answer/6324470?hl=zh-tw)的日期和時間。如果未提供，則為 NULL。 | 2023-10-14 00:00:00 (世界標準時間) |
| `brand` | `STRING` | 商家提供的商品[品牌](https://support.google.com/merchants/answer/6324351?hl=zh-tw)。如果未提供，則為 NULL。 | 品牌名稱 |
| `google_brand_id` | `STRING` | 商品的 Google 品牌 ID。 | 12759524623914508053 |
| `color` | `STRING` | 商家提供的商品[顏色](https://support.google.com/merchants/answer/6324487?hl=zh-tw)。如果未提供，則為 NULL。 | 銀色、灰色、多色 |
| `condition` | `STRING` | 商家提供的商品[狀況](https://support.google.com/merchants/answer/6324469?hl=zh-tw)或狀態。 | 全新、二手、整新 |
| `custom_labels` | `RECORD` | 商家提供[自訂標籤](https://support.google.com/merchants/answer/6324473?hl=zh-tw)，用於在購物廣告中自訂商品分組。如果未提供，則為 NULL。 |  |
| `custom_labels.label_0` | `STRING` | 自訂標籤 0。 | 我的自訂標籤 |
| `custom_labels.label_1` | `STRING` | 自訂標籤 1。 | 我的自訂標籤 |
| `custom_labels.label_2` | `STRING` | 自訂標籤 2。 | 我的自訂標籤 |
| `custom_labels.label_3` | `STRING` | 自訂標籤 3。 | 我的自訂標籤 |
| `custom_labels.label_4` | `STRING` | 自訂標籤 4。 | 我的自訂標籤 |
| `gender` | `STRING` | 商家提供的商品目標[性別](https://support.google.com/merchants/answer/6324479?hl=zh-tw)。如果未提供，則為 NULL。 | 男女通用、男性、女性 |
| `gtin` | `STRING` | 商家提供商品的[全球交易品項識別碼 (GTIN)](https://support.google.com/merchants/answer/6324461?hl=zh-tw)。如未提供，則為 NULL。 | 3234567890126 |
| `item_group_id` | `STRING` | 商家為同一產品的所有子類提供[共用 ID](https://support.google.com/merchants/answer/6324507?hl=zh-tw)。如果未提供，則為 NULL。 | AB12345 |
| `material` | `STRING` | 商家提供的[材質](https://support.google.com/merchants/answer/6324410?hl=zh-tw)，用於製作商品。如果未提供，則為 NULL。 | 皮革 |
| `mpn` | `STRING` | 商家提供商品的[製造商零件編號](https://support.google.com/merchants/answer/6324482?hl=zh-tw) (MPN)。如果未提供，則設為 NULL。 | GO12345OOGLE |
| `pattern` | `STRING` | 商家提供的[模式](https://support.google.com/merchants/answer/6324483?hl=zh-tw)。如果未提供，則為 NULL。 | 條紋 |
| `price` | `RECORD` | 商家提供的商品[價格](https://support.google.com/merchants/answer/6324371?hl=zh-tw)。 |  |
| `price.value` | `NUMERIC` | 商品價格。 | 19.99 |
| `price.currency` | `STRING` | 價格的幣別。 | 美元 |
| `sale_price` | `RECORD` | 商家提供的商品[特價](https://support.google.com/merchants/answer/6324471?hl=zh-tw)。 |  |
| `sale_price.value` | `NUMERIC` | 商品的特價。如果未提供，則為 NULL。 | 19.99 |
| `sale_price.currency` | `STRING` | 特價的幣別。如果未提供，則為 NULL。 | 美元 |
| `sale_price_effective_start_date` | `TIMESTAMP` | 商品特價的開始日期和時間。 | 2023-10-14 00:00:00 (世界標準時間) |
| `sale_price_effective_end_date` | `TIMESTAMP` | 商品特價的結束日期和時間。 | 2023-10-14 00:00:00 (世界標準時間) |
| `google_product_category` | `INTEGER` | 商品的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw) ID。如果未提供，則為 NULL。 | 2271 |
| `google_product_category_ids` | `INTEGER, REPEATED` | [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw)的完整路徑，以一組 ID 儲存。如果未提供，則為 NULL。 |  |
| `google_product_category_path` | `STRING` | 使用者可讀取的完整路徑。如未提供，則為空白。 | 服飾與配件 > 服飾 > 洋裝 |
| `product_type` | `STRING` | 商家提供的商品[類別](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 | 居家 > 女裝 > 洋裝 > 及踝洋裝 |
| `additional_product_types` | `STRING`、`REPEATED` | 商品的其他類別。 |  |
| `promotion_ids` | `STRING`、`REPEATED` | 與產品相關聯的[促銷活動 ID](https://support.google.com/merchants/answer/7050148?hl=zh-tw) 清單。 |  |
| `destinations` | `RECORD`、`REPEATED` | 產品的預定目的地。 |  |
| `destinations.name` | `STRING` | 目的地名稱；僅支援 `Shopping`。這與 Merchant Center 中的[行銷方法](https://support.google.com/merchants/answer/15130232?hl=zh-tw)「購物廣告」和「店面商品目錄廣告」相對應。 | 購物 |
| `destinations.status*` | `STRING` | 已淘汰 (一律設為空值)，這是為了讓產品[指定多個國家/地區](https://support.google.com/merchants/answer/7448571?hl=zh-tw)而做出的調整。如要讀取每個指定國家/地區的狀態，請使用下列欄位：[destinations.approved\_countries](#destinations.approved_countries)、[destinations.pending\_countries](#destinations.pending_countries)、[destinations.disapproved\_countries](#destinations.disapproved_countries)。問題現在可套用至特定的指定國家/地區，其他國家/地區則不適用，如 [issues.applicable\_countries](#issues.applicable_countries) 欄位所示。 | 空值 |
| `destinations.approved_countries` | `STRING, REPEATED` | 已核准商品的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | 美國、瑞士 |
| `destinations.pending_countries` | `STRING, REPEATED` | 待審核優惠適用的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | 美國、瑞士 |
| `destinations.disapproved_countries` | `STRING, REPEATED` | 遭拒售的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | 美國、瑞士 |
| `issues` | `RECORD`、`REPEATED` | 與產品相關聯的商品層級問題清單。 |  |
| `issues.code` | `STRING` | 問題的錯誤代碼。 | image\_too\_generic |
| `issues.servability` | `STRING` | 這個問題對優惠提供的影響程度。 | 已拒登，不受影響 |
| `issues.resolution` | `STRING` | 商家是否可解決這個問題。 | merchant\_action, pending\_processing |
| `issues.attribute_name` | `STRING` | 屬性名稱 (如果問題是因單一屬性造成)。否則為空值。 | 圖片連結 |
| `issues.destination` | `STRING` | 問題適用的目的地。一律設為 `Shopping`。 | 購物 |
| `issues.short_description` | `STRING` | 問題的簡短英文說明。 | 通用圖片 |
| `issues.detailed_description` | `STRING` | 問題的詳細英文說明。 | 請使用能夠如實呈現產品的圖片 |
| `issues.documentation` | `STRING` | 協助解決問題的說明網頁網址。 | https://support.google.com/merchants/answer/6098288 |
| `issues.applicable_countries` | `STRING, REPEATED` | 問題適用的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | CH |

## 查詢範例

### 產品和產品問題統計資料

下列 SQL 查詢範例會提供每天的產品數量、有問題的產品數量，以及問題數量。

```
SELECT
  _PARTITIONDATE AS date,
  COUNT(*) AS num_products,
  COUNTIF(ARRAY_LENGTH(issues) > 0) AS num_products_with_issues,
  SUM(ARRAY_LENGTH(issues)) AS num_issues
FROM
  dataset.Products_merchant_id
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD'
GROUP BY
  date
ORDER BY
  date DESC
```

### 遭到拒絕而無法刊登購物廣告的商品

下列 SQL 查詢範例會提供因遭到拒絕而無法刊登購物廣告的商品數量，並依國家/地區分開顯示。遭到拒登的原因可能是[不適用](https://support.google.com/merchants/answer/6324486?hl=zh-tw)，或是產品本身有問題。

```
SELECT
  _PARTITIONDATE AS date,
  disapproved_country,
  COUNT(*) AS num_products
FROM
  dataset.Products_merchant_id,
  UNNEST(destinations) AS destination,
  UNNEST(disapproved_countries) AS disapproved_country
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD'
GROUP BY
  date, disapproved_country
ORDER BY
  date DESC
```

### 有遭拒登問題的產品

下列 SQL 查詢範例會擷取有遭拒登問題的產品數量，並依國家/地區分開。

```
SELECT
  _PARTITIONDATE AS date,
  applicable_country,
  COUNT(DISTINCT CONCAT(CAST(merchant_id AS STRING), ':', product_id))
      AS num_distinct_products
FROM
  dataset.Products_merchant_id,
  UNNEST(issues) AS issue,
  UNNEST(issue.applicable_countries) as applicable_country
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD' AND
  issue.servability = 'disapproved'
GROUP BY
  date, applicable_country
ORDER BY
  date DESC
```

**注意：** 這個查詢會使用 `merchant_id` 和 `product_id` 建構唯一的金鑰。但只有在您擁有 MCA 帳戶的情況下，才需要這樣做。因為當您使用 MCA 帳戶時，多個子帳戶的 `product_id` 可能會彼此發生衝突。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]