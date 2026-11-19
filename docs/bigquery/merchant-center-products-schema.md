Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 產品資料表結構定義

將 Google Merchant Center 報表資料移轉至 BigQuery 時，產品和產品問題資料的格式主要會對應至 Content API 的 [`products`](https://developers.google.com/shopping-content/reference/rest/v2.1/products?hl=zh-tw) 和 [`productstatuses`](https://developers.google.com/shopping-content/reference/rest/v2.1/productstatuses?hl=zh-tw) 資源相關欄位格式。

如果您使用的是個別商家 ID，資料會寫入名為 `Products_MERCHANT_ID` 的資料表；如果您使用的是 MCA 帳戶，資料會寫入名為 `Products_AGGREGATOR_ID` 的資料表。

**注意：**首次要求報表時，系統不會立即提供產品和產品問題資料。首次要求轉移商家或集結網站 ID 時，可能需要等待最多 1 天，才能匯出 `Products_` 資料表。

## 結構定義

`Products_` 資料表包含下列結構定義：

| 欄 | BigQuery 資料類型 | 說明 | 範例資料 |
| --- | --- | --- | --- |
| `product_data_timestamp` | `TIMESTAMP` | 產品資料的時間戳記。 | 2023-09-14 11:49:50 UTC |
| `product_id` | `STRING` | 產品的 Content API REST ID，格式為 `channel:content_language:feed_label:offer_id`。這是主鍵。 | online:en:AU:666840730 |
| `merchant_id` | `INTEGER` | 商家帳戶 ID。 | 1234 |
| `aggregator_id` | `INTEGER` | 多重客戶帳戶的集結網站帳戶 ID。 | 12345 |
| `offer_id` | `STRING` | 商家提供的[產品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-tw)。 | tddy123uk |
| `title` | `STRING` | 項目名稱。 | TN2351 黑色 USB |
| `description` | `STRING` | 項目的[說明](https://support.google.com/merchants/answer/6324468?hl=zh-tw)。 | TN2351 黑色 USB 重新定義了 XJS 對 LLCD 體驗的影響。 |
| `link` | `STRING` | 商家提供的產品[到達網頁網址](https://support.google.com/merchants/answer/6324416?hl=zh-tw)。 | https://www.example.com/tn2351-black-usb/6538811?skuId=1234 |
| `mobile_link` | `STRING` | 商家提供的[針對行動裝置最佳化版本到達網頁網址](https://support.google.com/merchants/answer/6324459?hl=zh-tw)。 | https://www.example.com/tn2351-black-usb/6538811?skuId=1234 |
| `image_link` | `STRING` | 商家提供的[主要產品圖片網址](https://support.google.com/merchants/answer/6324350?hl=zh-tw)。 | https://www.example.com/tn2351-black-usb/6538811?skuId=1234 |
| `additional_image_links` | `STRING`、`REPEATED` | 商家提供的商品圖片[其他網址](https://support.google.com/merchants/answer/6324370?hl=zh-tw)。 |  |
| `content_language` | `STRING` | 項目的雙字母 ISO 639-1 語言代碼。 | en |
| `target_country` | `STRING` | 由於產品現在可[指定多個國家/地區](https://support.google.com/merchants/answer/7448571?hl=zh-tw)，因此這項屬性已淘汰 (一律設為 NULL)。請改用下列欄位讀取各指定國家/地區的狀態：[`destinations.approved_countries`](#destinations.approved_countries)、[`destinations.pending_countries`](#destinations.pending_countries)、[`destinations.disapproved_countries`](#destinations.disapproved_countries)。問題現在可能只適用於特定指定國家/地區，如 [`issues.applicable_countries`](#issues.applicable_countries) 欄位所示。 | null |
| `feed_label` | `STRING` | 商家為商品提供的[動態饋給標籤](https://support.google.com/merchants/answer/12453549?hl=zh-tw)，如未提供則為 `-`。 | 美國 |
| `channel` | `STRING` | 項目的管道，可以是 `online` 或 `local`。 | 本地、線上 |
| `expiration_date` | `TIMESTAMP` | 商家提供的[商品到期](https://support.google.com/merchants/answer/6324499?hl=zh-tw)日期和時間，如插入時所指定。如未提供，則設為空值。 | 2023-10-14 00:00:00 UTC |
| `google_expiration_date` | `TIMESTAMP` | 商品在 Google 購物中的到期日期和時間。請勿設為空值。 | 2023-10-14 00:00:00 UTC |
| `adult` | `BOOLEAN` | 如果商品[以成人為目標對象](https://support.google.com/merchants/answer/6324508?hl=zh-tw)，請設為 true。 | true/false |
| `age_group` | `STRING` | 商家提供的商品[目標年齡層](https://support.google.com/merchants/answer/6324463?hl=zh-tw)。如未提供，則為 NULL。 | newborn、infant、toddler、kids、adult |
| `availability` | `STRING` | 商家提供的商品[供應情形](https://support.google.com/merchants/answer/6324448?hl=zh-tw)狀態。 | 有現貨、缺貨中 |
| `availability_date` | `TIMESTAMP` | 商家提供的日期和時間，[預購產品可出貨的時間](https://support.google.com/merchants/answer/6324470?hl=zh-tw)。如未提供，則為 NULL。 | 2023-10-14 00:00:00 UTC |
| `brand` | `STRING` | 商家提供的商品[品牌](https://support.google.com/merchants/answer/6324351?hl=zh-tw)。如未提供，則為 NULL。 | 品牌名稱 |
| `google_brand_id` | `STRING` | 商品的 Google 品牌 ID。 | 12759524623914508053 |
| `color` | `STRING` | 商家提供的商品[顏色](https://support.google.com/merchants/answer/6324487?hl=zh-tw)。如未提供，則為 NULL。 | 銀色、灰色、多色 |
| `condition` | `STRING` | 商家提供的商品[狀況](https://support.google.com/merchants/answer/6324469?hl=zh-tw)或狀態。 | 新品、二手、整新品 |
| `custom_labels` | `RECORD` | 商家提供的[自訂標籤](https://support.google.com/merchants/answer/6324473?hl=zh-tw)，用於在購物廣告中自訂商品分組。如未提供，則為 NULL。 |  |
| `custom_labels.label_0` | `STRING` | 自訂標籤 0。 | 我的自訂標籤 |
| `custom_labels.label_1` | `STRING` | 自訂標籤 1。 | 我的自訂標籤 |
| `custom_labels.label_2` | `STRING` | 自訂標籤 2。 | 我的自訂標籤 |
| `custom_labels.label_3` | `STRING` | 自訂標籤 3。 | 我的自訂標籤 |
| `custom_labels.label_4` | `STRING` | 自訂標籤 4。 | 我的自訂標籤 |
| `gender` | `STRING` | 商家提供的商品目標[性別](https://support.google.com/merchants/answer/6324479?hl=zh-tw)。如未提供，則為 NULL。 | 男女通用、男性、女性 |
| `gtin` | `STRING` | 商家提供的商品[全球交易品項識別碼 (GTIN)](https://support.google.com/merchants/answer/6324461?hl=zh-tw)。如未提供，則為 NULL。 | 3234567890126 |
| `item_group_id` | `STRING` | 商家為同一產品的所有子類提供的[共用 ID](https://support.google.com/merchants/answer/6324507?hl=zh-tw)。如未提供，則為 NULL。 | AB12345 |
| `material` | `STRING` | 商家提供的商品[材質](https://support.google.com/merchants/answer/6324410?hl=zh-tw)。如未提供，則為 NULL。 | 皮革 |
| `mpn` | `STRING` | 商家提供的商品[製造商零件編號](https://support.google.com/merchants/answer/6324482?hl=zh-tw) (MPN)。如未提供，則設為 NULL。 | GO12345OOGLE |
| `pattern` | `STRING` | 商家提供的[模式](https://support.google.com/merchants/answer/6324483?hl=zh-tw)。如未提供，則為 NULL。 | 條紋 |
| `price` | `RECORD` | 商家提供的商品[價格](https://support.google.com/merchants/answer/6324371?hl=zh-tw)。 |  |
| `price.value` | `NUMERIC` | 商品價格。 | 19.99 |
| `price.currency` | `STRING` | 價格的幣別。 | 美元 |
| `sale_price` | `RECORD` | 商家提供的商品[特價](https://support.google.com/merchants/answer/6324471?hl=zh-tw)。 |  |
| `sale_price.value` | `NUMERIC` | 商品的特價價格。如未提供，則為 NULL。 | 19.99 |
| `sale_price.currency` | `STRING` | 特價價格的幣別。如未提供，則為 NULL。 | 美元 |
| `sale_price_effective_start_date` | `TIMESTAMP` | 商品特價的開始日期和時間。 | 2023-10-14 00:00:00 UTC |
| `sale_price_effective_end_date` | `TIMESTAMP` | 商品特價結束日期和時間。 | 2023-10-14 00:00:00 UTC |
| `google_product_category` | `INTEGER` | 商品的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw) ID。如未提供，則為 NULL。 | 2271 |
| `google_product_category_ids` | `INTEGER, REPEATED` | 項目的 [Google 產品類別](https://support.google.com/merchants/answer/1705911?hl=zh-tw)完整路徑，以一組 ID 的形式儲存。如未提供，則為 NULL。 |  |
| `google_product_category_path` | `STRING` | 人類可讀的完整路徑版本。如未提供，則為空白。 | 服飾與配件 > 服飾 > 洋裝 |
| `product_type` | `STRING` | 商家提供的商品[類別](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 | 首頁 > 女裝 > 連身裙 > 長連身裙 |
| `additional_product_types` | `STRING`、`REPEATED` | 商品的額外類別。 |  |
| `promotion_ids` | `STRING`、`REPEATED` | 與產品相關聯的[促銷 ID](https://support.google.com/merchants/answer/7050148?hl=zh-tw) 清單。 |  |
| `destinations` | `RECORD`、`REPEATED` | 產品的預定目的地。 |  |
| `destinations.name` | `STRING` | 目的地名稱；僅支援 `Shopping`。這對應 Merchant Center 中的[行銷方式](https://support.google.com/merchants/answer/15130232?hl=zh-tw)「購物廣告」和「店面商品目錄廣告」。 | 購物 |
| `destinations.status` | `STRING` | 由於產品現在可[指定多個國家/地區](https://support.google.com/merchants/answer/7448571?hl=zh-tw)，因此這項屬性已淘汰 (一律設為 NULL)。請改用下列欄位讀取各指定國家/地區的狀態：[`destinations.approved_countries`](#destinations.approved_countries)、[`destinations.pending_countries`](#destinations.pending_countries)、[`destinations.disapproved_countries`](#destinations.disapproved_countries)。問題現在可能只適用於特定指定國家/地區，如 [`issues.applicable_countries`](#issues.applicable_countries) 欄位所示。 | 空值 |
| `destinations.approved_countries` | `STRING, REPEATED` | 商品獲准刊登的[CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | US, CH |
| `destinations.pending_countries` | `STRING, REPEATED` | 商品處於待處理狀態的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | US, CH |
| `destinations.disapproved_countries` | `STRING, REPEATED` | 商品遭拒登的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | US, CH |
| `issues` | `RECORD`、`REPEATED` | 與產品相關聯的商品層級問題清單。 |  |
| `issues.code` | `STRING` | 問題的錯誤代碼。 | image\_too\_generic |
| `issues.servability` | `STRING` | 這項問題對商品放送的影響。 | 已拒登，不受影響 |
| `issues.resolution` | `STRING` | 商家是否可以解決問題。 | merchant\_action, pending\_processing |
| `issues.attribute_name` | `STRING` | 如果問題是由單一屬性造成，則會顯示屬性名稱。否則傳回 NULL。 | 圖片連結 |
| `issues.destination` | `STRING` | 問題適用的目的地。一律設為 `Shopping`。 | 購物 |
| `issues.short_description` | `STRING` | 簡短說明問題 (英文)。 | 圖片太過籠統 |
| `issues.detailed_description` | `STRING` | 問題詳細說明 (英文)。 | 使用的圖片必須能夠如實呈現產品 |
| `issues.documentation` | `STRING` | 有助於解決這個問題的網頁網址。 | https://support.google.com/merchants/answer/6098288 |
| `issues.applicable_countries` | `STRING, REPEATED` | 問題適用的 [CLDR 地域代碼](http://www.unicode.org/repos/cldr/tags/latest/common/main/en.xml)清單。 | CH |

## 查詢範例

### 產品和產品問題統計資料

下列 SQL 範例查詢會提供產品數量、有問題的產品數量，以及每日問題數量。

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

下列 SQL 範例查詢會提供未獲准在購物廣告中顯示的產品數量，並依國家/地區區分。拒登原因可能是目的地[遭排除](https://support.google.com/merchants/answer/6324486?hl=zh-tw)，或產品有問題。

```
SELECT
  _PARTITIONDATE AS date,
  disapproved_country,
  COUNT(*) AS num_products
FROM
  dataset.Products_merchant_id,
  UNNEST(destinations) AS destination,
  UNNEST(disapproved_countries) AS
```