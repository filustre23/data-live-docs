Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料遮蓋簡介

**注意：** 如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

BigQuery 支援資料欄層級的[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)功能。您能針對不同使用者群組，選擇性地掩蓋特定資料欄的資料，但這些使用者還是能正常使用該資料欄。資料遮罩功能是以[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)為基礎，因此請先熟悉該功能，再繼續操作。

如果將資料遮蓋功能與資料欄層級存取控管搭配使用，您就能根據不同使用者群組的需求，設定資料欄資料的存取權範圍，從完整存取權到無存取權。舉例來說，對於稅號資料，您可能想授予會計群組完整存取權、分析師群組遮蓋存取權，以及銷售群組無存取權。

本文說明如何使用政策標記遮蓋資料。您也可以使用[資料治理標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#data-governance-tags)，這類 Resource Manager 標記可用於資料遮蓋和資料欄層級的存取權控管。

**注意：** 如要建立及管理用於資料遮蓋和資料欄層級安全防護的 Data Catalog 政策標記和分類，必須保持啟用 `datacatalog.googleapis.com` API。雖然 Data Catalog 的中繼資料搜尋和目錄功能已淘汰，並轉換至 Knowledge Catalog，但政策標記專用的 Data Catalog API 功能並未淘汰。

## 優點

資料遮蓋功能有下列優點：

* 簡化資料共用程序。您可以遮蓋機密資料欄，以便與更多人共用資料表。
* 與資料欄層級存取控管不同，您不必排除使用者無法存取的資料欄，即可修改現有查詢。設定資料遮蓋功能後，現有查詢會根據使用者獲派的角色，自動遮蓋資料欄資料。
* 您可以大規模套用資料存取政策。您可以編寫資料政策、將政策與政策標記建立關聯，然後將政策標記套用至任意數量的資料欄。
* 可啟用屬性式存取控管。附加至資料欄的政策標記會提供情境資料存取權，這項權限取決於資料政策和與該政策標記相關聯的主體。

## 資料遮蓋工作流程

如要遮蓋資料，您可以建立分類和政策標記，然後在政策標記上設定資料政策。或者，您也可以採取下列任一做法：

* **直接在資料欄上設定資料政策。**將資料遮蓋規則對應至資料，不必處理政策標記或建立其他分類。
* **使用資料治理標記。**使用[資料治理標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#data-governance-tags) (預先發布版) 進行資料欄層級存取控管和資料遮蓋。

### 直接在資料欄上設定資料政策

您可以直接在資料欄上設定動態資料遮蓋規則。如要這樣做，請按照下列步驟操作：

1. [建立資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#create-data-policies-on-column)。
2. [將資料政策指派給資料欄](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#assign-to-column)。

### 使用政策標記遮蓋資料

圖 1 顯示設定資料遮蓋的工作流程：

**圖 1.** 資料遮蓋元件。

請按照下列步驟設定資料遮蓋：

1. [設定分類和一或多個政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#create_taxonomy)。
2. 為政策標記設定*資料政策*。資料政策會將[*資料遮蓋規則*](#masking_options)和一或多個主體 (代表使用者或群組) 對應至政策標記。

   使用 Google Cloud 控制台[建立資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#create_data_policies)時，您可以在一個步驟中建立資料遮蓋規則並指定主體。使用 BigQuery Data Policy API 建立資料政策時，您可以在一個步驟中建立資料政策和資料遮蓋規則，並在第二個步驟中指定資料政策的主體。
3. 將政策標記指派給 BigQuery 資料表中的資料欄，套用資料政策。
4. 將 BigQuery 遮蓋讀取者角色指派給應有權存取遮蓋資料的使用者。最佳做法是在資料政策層級指派 BigQuery 遮蓋讀取者角色。在專案層級或更高層級指派角色，會授予使用者專案下所有資料政策的權限，這可能會導致權限過多而引發問題。

   與資料政策相關聯的政策標記，也可用於資料欄層級存取控管。在這種情況下，政策標記也會與獲派 Data Catalog 精細讀取者角色的一或多個主體建立關聯。這些主體就能存取原始的未遮蓋欄資料。

圖 2 顯示資料欄層級存取控管和資料遮蓋規則的運作方式：

**圖 2.** 資料遮蓋元件。

如要進一步瞭解角色互動，請參閱「[遮罩讀取者和精細讀取者角色的互動方式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#role-interaction)」。如要進一步瞭解政策標記沿用，請參閱「[角色和政策標記階層](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#auth-inheritance)」。

## 資料遮蓋規則

使用資料遮蓋功能時，系統會根據執行查詢的使用者角色，在查詢執行階段將資料遮蓋規則套用至資料欄。遮蓋作業優先於查詢中涉及的任何其他作業。資料遮蓋規則會決定套用至資料欄資料的遮蓋類型。

您可以使用下列資料遮蓋規則：

* **自訂遮蓋處理常式**。對資料欄套用[使用者定義函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#custom-mask) 後，傳回資料欄的值。如要管理遮蓋規則，必須具備[例行權限](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#permissions)。這項規則的設計宗旨是支援所有 [BigQuery 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)，但 `STRUCT` 資料類型除外。不過，對 `STRING` 和 `BYTES` 以外資料類型的支援有限。輸出內容取決於定義的函式。

  如要進一步瞭解如何為自訂遮蓋常式建立 UDF，請參閱「[建立自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#custom-mask)」。
* **日期年份遮罩**。將資料欄的值截斷至年份，並將所有非年份部分設為該年年初，然後傳回該值。這項規則只能用於使用 `DATE`、`DATETIME` 和 `TIMESTAMP` 資料類型的欄。例如：

  | 類型 | 原始 | 遮罩 |
  | --- | --- | --- |
  | `DATE` | 2030-07-17 | 2030-01-01 |
  | `DATETIME` | 2030-07-17T01:45:06 | 2030-01-01T00:00:00 |
  | `TIMESTAMP` | 2030-07-17 01:45:06 | 2030-01-01 00:00:00 |

  **注意：** 系統會根據世界標準時間時區截斷資料。如要變更這項設定，請使用 **@@time\_zone**
  [系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)調整預設時區。
* **預設遮蓋值**。根據資料欄的資料類型，傳回資料欄的預設遮蓋值。如要隱藏資料欄的值，但顯示資料類型，請使用這項功能。將這項資料遮蓋規則套用至資料欄後，對於具備「經過遮蓋的讀取者」存取權的使用者來說，該資料欄在查詢[`JOIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)作業中的實用性會降低。這是因為預設值不夠獨特，在彙整資料表時無法發揮作用。

  下表列出各資料類型的預設遮蓋值：

  | **資料類型** | **預設遮蓋值** |
  | --- | --- |
  | `STRING` | "" |
  | `BYTES` | b'' |
  | `INTEGER` | 0 |
  | `FLOAT` | 0.0 |
  | `NUMERIC` | 0 |
  | `BOOLEAN` | `FALSE` |
  | `TIMESTAMP` | 1970-01-01 00:00:00 UTC |
  | `DATE` | 1970-01-01 |
  | `TIME` | 00:00:00 |
  | `DATETIME` | 1970-01-01T00:00:00 |
  | `GEOGRAPHY` | POINT(0 0) |
  | `BIGNUMERIC` | 0 |
  | `ARRAY` | [] |
  | `STRUCT` | NOT\_APPLICABLE  政策標記無法套用至使用 `STRUCT` 資料類型的資料欄，但可以與這類資料欄的葉節點欄位建立關聯。 |
  | `JSON` | null |
* **電子郵件遮罩**。將有效電子郵件地址的使用者名稱替換為 `XXXXX` 後，傳回資料欄的值。如果欄的值不是有效的電子郵件地址，系統會透過 [SHA-256](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha256) 雜湊函式執行該值，然後傳回結果。這項規則只能用於採用 `STRING` 資料類型的資料欄。例如：

  | 原始 | 已遮蓋 |
  | --- | --- |
  | `abc123@gmail.com` | `XXXXX@gmail.com` |
  | `randomtext` | `jQHDyQuj7vJcveEe59ygb3Zcvj0B5FJINBzgM6Bypgw=` |
  | `test@gmail@gmail.com` | `Qdje6MO+GLwI0u+KyRyAICDjHbLF1ImxRqaW08tY52k=` |
* **前四個字元**。傳回資料欄值的前 4 個字元，並將字串的其餘部分替換為 `XXXXX`。如果資料欄的值長度等於或小於 4 個字元，系統會先透過 [SHA-256](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha256) 雜湊函式處理該值，然後傳回處理後的結果。這項規則只能用於使用 `STRING` 資料型別的資料欄。
* **雜湊 (SHA-256)**。傳回資料欄的值 (已透過 [SHA-256](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha256) 雜湊函式執行)。如要讓使用者在查詢的 [`JOIN` 作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)中使用這個資料欄，請使用這個選項。這項規則只能用於採用 `STRING` 或 `BYTES` 資料類型的資料欄。

  資料遮罩中使用的 SHA-256 函式會保留類型，因此傳回的雜湊值與資料欄值具有相同的資料類型。舉例來說，`STRING` 資料欄值的雜湊值也具有 `STRING` 資料型別。

  **重要事項：** SHA-256 是確定性雜湊函式，初始值一律會解析為相同的雜湊值。但不需要加密金鑰。這表示惡意行為人可以透過 SHA-256 演算法執行所有可能的原始值，並查看哪個值產生的雜湊與資料遮罩傳回的雜湊相符，藉此使用蠻力攻擊來判斷原始值。
* **隨機雜湊**。使用加鹽雜湊演算法，傳回資料欄值的雜湊。隨機雜湊提供的安全性比標準 `Hash
  (SHA-256)` 規則更強。這項規則只能用於使用 `STRING` 或 `BYTES` 資料類型的資料欄。

  + **非確定性：**系統會為每項查詢產生不重複的隨機值 (鹽)。相同的資料欄值在不同查詢中會產生不同的雜湊結果。這有助於防止蠻力攻擊，以及分析遮蓋資料模式。
  + **加入控制項：**
    - 只能*在同一個查詢中*，對以 `RANDOM_HASH` 遮蓋的資料欄執行聯結。
    - 由於每項查詢都有隨機鹽，因此無法跨不同查詢進行彙整。
    - 只有在套用至資料欄的資料政策屬於*同一 Google Cloud 專案*時，系統才會支援聯結。方法是在雜湊輸入內容中加入資料政策的專案 ID，藉此強制執行這項規定。
  + **限制：**
    - 隨機雜湊僅支援在資料欄上設定的資料政策，不支援政策標記。
* **最後四個字元**。傳回資料欄值的最後 4 個字元，並以 `XXXXX` 取代字串的其餘部分。如果資料欄的值長度等於或少於 4 個字元，系統會透過 [SHA-256](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha256) 雜湊函式執行該值，然後傳回結果。這項規則只能用於採用 `STRING` 資料類型的資料欄。
* **失效**。傳回 `NULL`，而不是資料欄值。如要同時隱藏資料欄的值和資料類型，請使用這個選項。如果將這項資料遮蓋規則套用至資料欄，則對於具備遮蓋讀取者存取權的使用者，該資料欄在查詢 [`JOIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types) 作業中的實用性會降低。這是因為 `NULL` 值不夠獨特，無法在彙整資料表時發揮作用。

### 資料遮蓋規則比較

下表比較 BigQuery 中可用的不同資料遮蓋選項，並考量這些選項是否可用於聯結，以及相對安全強度：

* **可聯結性：**指遮蓋資料是否可用於 SQL `JOIN` 作業。您可以使用遮蓋方法，為特定輸入內容產生一致的輸出內容 (在彙整範圍內具有確定性)，並保留足夠的獨特性。
* **安全強度：**表示防止原始資料去匿名化或反向工程的保護等級。這是相對比較。

| 遮蓋選項 | 類型 | 可加入性 | 安全強度 |
| --- | --- | --- | --- |
| 失效 | 預先定義 | 否 | **最高：**將資料替換為 `NULL`。不會洩漏原始值相關資訊。 |
| 預設遮蓋值 | 預先定義 | 否 | **最高：**根據資料類型，以預設值取代資料。不會洩漏原始值的資訊。 |
| 電子郵件遮罩 | 預先定義 | 否 | **中度：**遮蓋使用者名稱 (例如 `user@example.com` 變成 `XXXXX@example.com`)，但網域名稱仍會顯示。未遮蓋的網域可能會洩漏機構所屬關係，因此屬於敏感資訊。這項資訊可能會與其他資料相互關聯，用於去匿名化作業。如果網域內的潛在使用者人數較少，這項遮罩措施的效果就會降低，更容易推斷出原始使用者。如果值不是有效的電子郵件地址，系統會使用 SHA-256 進行雜湊處理 (**中等：**安全性強度)。 |
| 前四個字元 | 預先定義 | 否 | **低到中等：**傳回前 4 個字元，其餘字元則以 `XXXXX` 取代。如果字串長度不超過 4 個字元，則會使用 SHA-256 進行雜湊處理。在這些短字串上使用 SHA-256 時，安全性為「非常低」，因為輸入空間有限 (1 到 4 個字元)，因此計算所有可能輸入內容的彩虹表非常簡單，可進行反向查閱。 |
| 最後四個字元 | 預先定義 | 否 | **低到中等：**傳回最後 4 個字元，並在前面加上 `XXXXX` 來取代其餘字元。如果字串長度不超過 4 個字元，則會使用 SHA-256 進行雜湊處理。與「前四個字元」類似，在短字串上使用 SHA-256 時，由於容易進行反向查詢，因此安全性**極低**。 |
| 日期年份遮罩 | 預先定義 | 否 | **中等：**只顯示年份，截斷日期其餘部分 (例如 `2030-07-17` 會變成 `2030-01-01`)。會洩漏部分資訊，且容易受到統計分析。 |
| 隨機雜湊 | 預先定義 | 是 (在同一查詢中) | **高：**在雜湊運算中，服務會*針對每次查詢執行*，使用不重複的隨機密鑰。這可有效防範預先計算的資料表攻擊 (例如彩虹表)。*只有在同一個查詢執行作業中*，相同輸入值的輸出內容才會一致。由於每次查詢的鹽值都會變更，因此無法跨不同查詢執行彙整作業。 |
| 雜湊 (SHA-256) | 預先定義 | 是 | **中等：**雖然 SHA-256 在密碼學上提供強大的*抗碰撞性*，但在這種遮罩情境下，容易受到各種攻擊。由於這是確定性雜湊，因此容易受到彩虹表攻擊、已知明文攻擊和統計分析。您可以在這裡彙整不同查詢執行作業。 |
| 自訂遮蓋常式 - SHA-256 | 自訂 | 是 | **中等：**安全性屬性與預先定義的 SHA-256 相同。提供強大的*抗碰撞性*，但由於其確定性，容易受到彩虹表、已知明文和統計分析攻擊。 |
| 自訂遮蓋常式：加鹽 SHA-256 | 自訂 | 是 | **高 (取決於適當的鹽保護)：**在自訂 UDF 定義中，使用*一致的秘密*鹽硬式編碼，安全性高於標準 SHA-256。安全性取決於鹽的保密性。必須限制 UDF 定義的存取權。BigQuery 會從執行詳細資料中遮蓋常數，有助於防止鹽值外洩。與 `RANDOM_HASH` 不同的是，使用這個*特定* UDF 的查詢會採用一致的鹽值，因此支援跨查詢的聯結。 |
| 自訂遮蓋處理常式 - AEAD 加密 | 自訂 | 是 | **高 (取決於金鑰管理是否得當)：**可提供強大的安全性和可加入性。  **重要注意事項：**如要搭配使用 AEAD 加密和以 KMS 包裝的金鑰集，查詢使用者通常需要 KMS 金鑰的 `cloudkms.cryptoKeyVersions.useToDecryptViaDelegation` 權限。這項權限可讓使用者將包裝金鑰組用於加密*和*解密。因此，*包裝金鑰集*必須受到保護。如果使用者有權存取*包裝金鑰*，就能解密 (遮蓋) 機密資料欄資料。 |

### 雜湊衝突和彙整完整性

雜湊技術 (例如 SHA-256 和隨機雜湊) 有理論上的[雜湊衝突](https://en.wikipedia.org/wiki/Hash_collision)風險，也就是兩個不同的原始值會產生相同的雜湊值。如果使用這些規則遮蓋資料欄，並在後續的 `JOIN` 作業中使用，可能會發生衝突，導致查詢結果中的資料關聯不正確 (錯誤比對)。

不過，就任何實際資料集而言，SHA-256 碰撞的統計機率實際上微乎其微。因此，使用者可以非常放心地依據雜湊值遮蓋規則，確保聯結完整性。

### 資料遮蓋規則階層

您可以為政策標記設定最多九項資料政策，每項政策都與不同的資料遮蓋規則相關聯。其中一項政策會保留給[資料欄層級存取控管設定](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_up_column-level_access_control)。這樣一來，系統就能根據使用者所屬的群組，將多項資料政策套用至使用者查詢中的資料欄。發生這種情況時，BigQuery 會根據下列階層選擇要套用的資料遮蓋規則：

1. 自訂遮蓋處理常式
2. 隨機雜湊
3. 雜湊 (SHA-256)
4. 電子郵件遮罩
5. 最後四個字元
6. 前四個字元
7. 日期年份遮罩
8. 預設遮蓋值
9. 失效

舉例來說，使用者 A 同時是員工群組和會計群組的成員。使用者 A 執行查詢，其中包含已套用 `confidential` 政策標記的 `sales_total` 欄位。`confidential` 政策標記有兩項相關聯的資料政策：一項以員工角色為主體，並套用無效資料遮蓋規則；另一項以會計角色為主體，並套用雜湊 (SHA-256) 資料遮蓋規則。在這種情況下，雜湊 (SHA-256) 資料遮蓋規則的優先順序高於無效資料遮蓋規則，因此雜湊 (SHA-256) 規則會套用至使用者 A 查詢中的 `sales_total` 欄位值。

圖 3 說明瞭這種情況：

**圖 3**：資料遮蓋規則優先順序。

## 角色和權限

### 管理分類和政策標記的角色

您必須具備 Data Catalog 政策標記管理員角色，才能建立及管理分類和政策標記。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| Data Catalog 政策標記管理員 (`datacatalog.categoryAdmin`) | `datacatalog.categories.getIamPolicy`  `datacatalog.categories.setIamPolicy`  `datacatalog.taxonomies.create`  `datacatalog.taxonomies.delete`  `datacatalog.taxonomies.get`  `datacatalog.taxonomies.getIamPolicy`  `datacatalog.taxonomies.list`  `datacatalog.taxonomies.setIamPolicy`  `datacatalog.taxonomies.update`  `resourcemanager.projects.get`  `resourcemanager.projects.list` | 適用於專案層級。  這個角色可授予下列權限：   * 建立、讀取、更新及刪除分類和政策標記。 * 取得及設定政策標記的 IAM 政策。 |

### 建立及管理資料政策的角色

您必須具備下列其中一個 BigQuery 角色，才能建立及管理資料政策：

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| BigQuery 資料政策管理員 (`bigquerydatapolicy.admin`)    BigQuery 管理員 (`bigquery.admin`)    BigQuery 資料擁有者 (`bigquery.dataOwner`) | `bigquery.dataPolicies.create`  `bigquery.dataPolicies.delete`  `bigquery.dataPolicies.get`  `bigquery.dataPolicies.getIamPolicy`  `bigquery.dataPolicies.list`  `bigquery.dataPolicies.setIamPolicy`  `bigquery.dataPolicies.update` | `bigquery.dataPolicies.create` 和 `bigquery.dataPolicies.list` 權限適用於專案層級。其他權限則在資料政策層級套用。  這個角色可執行下列操作：   * 建立、讀取、更新及刪除資料政策。 * 取得及設定資料政策的 IAM 政策。 |

您也需要 `datacatalog.taxonomies.get` 權限，可從多個 [Data Catalog 預先定義角色](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw)取得。

### 可將政策標記附加至資料欄的角色

您必須具備 `datacatalog.taxonomies.get` 和 `bigquery.tables.setCategory` 權限，才能將政策標記附加至資料欄。Data Catalog 政策標記管理員和檢視者角色包含 `datacatalog.taxonomies.get`。BigQuery 管理員 (`roles/bigquery.admin`) 和 BigQuery 資料擁有者 (`roles/bigquery.dataOwner`) 角色包含 `bigquery.tables.setCategory`。

### 查詢遮罩資料的角色

如要查詢已套用資料遮蓋的資料欄資料，您需要 [BigQuery 遮蓋讀取者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquerydatapolicy.maskedReader)角色。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| 經過遮蓋的讀取者 (`bigquerydatapolicy.maskedReader`) | `bigquery.dataPolicies.maskedGet` | 這個角色只能授予 Resource Manager 資源 (專案、資料夾和組織)。  這個角色可查看與資料政策相關聯的資料欄經過遮蓋的資料。  此外，使用者必須具備適當權限才能查詢資料表。 詳情請參閱「[必要權限](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#required_permissions)」。 |

### 遮蓋資料讀取者和精細讀取者角色的互動方式

資料遮罩是以資料欄層級存取控管為基礎。對於特定資料欄，可以讓部分使用者具備 BigQuery 遮蓋讀取者角色，允許他們讀取遮蓋資料；部分使用者具備 Data Catalog 精細讀取者角色，允許他們讀取未遮蓋資料；部分使用者同時具備這兩種角色，部分使用者則不具備任何角色。這些角色之間的互動方式如下：

* 同時具備「精細讀取者」和「經過遮蓋的讀取者」角色的使用者：使用者看到的內容取決於每個角色在政策標記階層中的授權位置。詳情請參閱「[政策標記階層中的授權沿用設定](#auth-inheritance)」。
* 具備精細讀取者角色的使用者：可以查看未遮蓋 (未隱藏) 的資料欄資料。
* 具備「遮蓋讀取者」角色的使用者：可以查看遮蓋 (隱藏) 的資料欄資料。
* 不具備上述任一角色的使用者：權限遭拒。

如果資料表的資料欄受到保護，或受到保護且遮蓋，使用者必須是適當群組的成員，才能對該資料表執行 `SELECT * FROM` 陳述式，這樣他們才能在所有這些資料欄上獲得遮蓋讀取者或精細讀取者角色。

如果使用者未獲派這些角色，則必須在 `SELECT` 陳述式中僅指定有權存取的資料欄，或使用 `SELECT * EXCEPT
(restricted_columns) FROM` 排除受保護或遮蓋的資料欄。

### 政策標記階層中的授權繼承

系統會從與資料欄相關聯的政策標記開始評估角色，然後在分類的每個遞增層級檢查，直到確定使用者具備適當權限，或達到政策標記階層的頂端。

舉例來說，請參考圖 4 所示的政策標記和資料政策設定：

**圖 4**：政策標記和資料政策設定。

假設您有一個資料表資料欄，並以 `Financial` 政策標記加上註解，而某位使用者同時屬於 ftes@example.com 和 analysts@example.com 群組。當這位使用者執行包含已加上註解資料欄的查詢時，系統會根據政策標記分類中定義的階層，決定其存取權。由於使用者透過 `Financial` 政策標記獲得 Data Catalog 精細讀取者角色，因此查詢會傳回未遮蓋的資料欄資料。

如果另一個使用者僅具備 ftes@example.com 角色，並執行包含已註解資料欄的查詢，則查詢會傳回使用 SHA-256 演算法雜湊處理的資料欄資料，因為使用者透過 `Confidential` 政策標記 (`Financial` 政策標記的父項) 獲得 BigQuery 遮蓋讀取者角色。

如果使用者不屬於這兩個角色，嘗試查詢加上註解的資料欄時，就會收到存取遭拒錯誤。

與上述情境相反，請查看圖 5 所示的政策標記和資料政策設定：

**圖 5.** 政策標記和資料政策設定。

您的情況與圖 4 相同，但使用者在政策標記階層較高層級獲得「精細讀取者」角色，在政策標記階層較低層級獲得「遮蓋讀取者」角色。因此，查詢會傳回這位使用者的遮蓋資料欄資料。即使使用者在標記階層中獲得更上層的精細讀取者角色，也會發生這種情況，因為服務在政策標記階層中向上檢查使用者存取權時，會使用遇到的第一個指派角色。

如要建立單一資料政策，並將其套用至政策標記階層的多個層級，請在代表最高階層層級的政策標記上設定資料政策。舉例來說，假設分類結構如下：

* 政策標記 1
  + 政策標記 1a
    - 政策標記 1ai
  + 政策標記 1b
    - 政策標記 1bi
    - 政策標記 1bii

如要將資料政策套用至所有政策標記，請在政策標記 1 設定資料政策。如要將資料政策套用至政策標記 1b 及其子項，請在政策標記 1b 設定資料政策。

## 資料遮蓋功能與不相容的功能

當您使用[與資料遮蓋不相容的 BigQuery 功能](#compatibility)時，服務會將遮蓋的資料欄視為受保護的資料欄，且僅授予具備 Data Catalog 精細讀取者角色的使用者存取權。

舉例來說，請參考圖 6 所示的政策標記和資料政策設定：

**圖 6**：政策標記和資料政策設定。

您有一個以 `Financial` 政策標記註解的資料表欄，以及 analysts@example.com 群組的成員。如果該使用者嘗試透過不相容的功能存取加上註解的資料欄，就會收到存取遭拒錯誤。這是因為他們透過 `Financial` 政策標記取得 BigQuery 經過遮蓋的讀取者角色，但在此情況下，他們必須具備 Data Catalog 精細讀取者角色。由於服務已為使用者決定適用的角色，因此不會繼續檢查政策標記階層中更上層的其他權限。

## 資料遮蓋範例和輸出內容

如要瞭解標記、主體和角色如何搭配運作，請參考以下範例。

在 example.com，系統會透過 data-users@example.com
群組授予基本存取權。所有需要定期存取 BigQuery 資料的員工都是這個群組的成員，這個群組已獲派從資料表讀取資料的所有必要權限，以及 BigQuery 遮蓋讀取者角色。

員工會獲派至其他群組，以便存取工作所需的受保護或遮蓋資料欄。這些額外群組的所有成員也是 data-users@example.com 的成員。如要瞭解這些群組如何與適當角色建立關聯，請參閱圖 7：

**圖 7.** example.com 的政策標記和資料政策。

接著，政策標記會與資料表資料欄建立關聯，如圖 8 所示：

**圖 8.** 與資料表欄相關聯的 Example.com 政策標記。

根據與資料欄相關聯的標記，執行 `SELECT * FROM Accounts;` 會為不同群組產生下列結果：

* **data-users@example.com**：這個群組已獲得 `PII` 和 `Confidential` 政策標記的 BigQuery 遮蓋讀取者角色。系統會傳回下列結果：

  | **SSN** | **Priority** | **生命週期價值** | **建立日期** | **電子郵件** |
  | --- | --- | --- | --- | --- |
  | 空值 | "" | 0 | 1983 年 3 月 8 日 | 空值 |
  | 空值 | "" | 0 | 2009 年 12 月 29 日 | 空值 |
  | 空值 | "" | 0 | 2021 年 7 月 14 日 | 空值 |
  | 空值 | "" | 0 | 1997 年 5 月 5 日 | 空值 |
* **accounting@example.com**：這個群組已獲得 `SSN` 政策標記的 Data Catalog Fine-Grained Reader 角色。系統會傳回下列結果：

  | **SSN** | **Priority** | **生命週期價值** | **建立日期** | **NULL** |
  | --- | --- | --- | --- | --- |
  | 123-45-6789 | "" | 0 | 1983 年 3 月 8 日 | 空值 |
  | 234-56-7891 | "" | 0 | 2009 年 12 月 29 日 | 空值 |
  | 345-67-8912 | "" | 0 | 2021 年 7 月 14 日 | 空值 |
  | 456-78-9123 | "" | 0 | 1997 年 5 月 5 日 | 空值 |
* **sales-exec@example.com**：這個群組已獲得 `Confidential` 政策標記的 Data Catalog 精細讀取者角色。系統會傳回下列結果：

  | **SSN** | **Priority** | **生命週期價值** | **建立日期** | **電子郵件** |
  | --- | --- | --- | --- | --- |
  | 空值 | 高 | 90,000 | 1983 年 3 月 8 日 | 空值 |
  | 空值 | 高 | 84,875 | 2009 年 12 月 29 日 | 空值 |
  | 空值 | 中 | 38,000 | 2021 年 7 月 14 日 | 空值 |
  | 空值 | 低 | 245 | 1997 年 5 月 5 日 | 空值 |
* **fin-dev@example.com**：這個群組已獲授與政策標記的 BigQuery 遮蓋讀取者角色 (`Financial`)。系統會傳回下列結果：

  | **SSN** | **Priority** | **生命週期價值** | **建立日期** | **電子郵件** |
  | --- | --- | --- | --- | --- |
  | 空值 | "" | Zmy9vydG5q= | 1983 年 3 月 8 日 | 空值 |
  | 空值 | "" | GhwTwq6Ynm= | 2009 年 12 月 29 日 | 空值 |
  | 空值 | "" | B6y7dsgaT9= | 2021 年 7 月 14 日 | 空值 |
  | 空值 | "" | Uh02hnR1sg= | 1997 年 5 月 5 日 | 空值 |
* **所有其他使用者**：如果使用者不屬於上述任何群組，就會收到存取遭拒錯誤，因為他們未獲授與 Data Catalog 精細讀取者或 BigQuery 經過遮蓋的讀取者角色。如要查詢 `Accounts` 資料表，他們必須在 `SELECT * EXCEPT
  (restricted_columns) FROM Accounts` 中僅指定有權存取的資料欄，以排除受保護或遮蓋的資料欄。

## 費用注意事項

資料遮罩可能會間接影響處理的位元組數，進而影響查詢費用。如果使用者查詢的資料欄已透過「Nullify」或「Default Masking Value」規則遮蓋，系統就不會掃描該資料欄，因此處理的位元組數會減少。

## 規定與限制

以下各節說明資料遮蓋功能適用的限制和規定類別。

### 資料政策管理

* 如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* 每個政策標記最多可建立九項資料政策。其中一項政策會保留給[資料欄層級存取控管設定](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_up_column-level_access_control)。
* 資料政策、相關聯的政策標記，以及任何使用這些政策的常式，都必須位於同一個專案中。

### 政策標記

* 含有政策標記分類的專案必須屬於某個組織。
* 政策標記分類的範圍限定為組織。如果將專案遷移至其他機構，專案會失去原始 Data Catalog 分類架構的存取權。過時的政策標記可能仍會顯示在結構定義編輯器的資料表欄中，但會從 Google Cloud 控制台的政策標記使用者介面中移除，且無法套用至新資料表。如要將專案遷移至新組織，請務必執行下列操作：
  + 在目標組織的專案中，手動重新建立政策標記分類、政策標記和相關聯的資料政策。
  + 明確授予目的地組織中的資料夾層級 BigQuery 管理員 (`roles/bigquery.admin`) 和 Data Catalog 管理員 (`roles/datacatalog.admin` 或 `roles/datacatalog.categoryAdmin`) 角色。
  + 更新遷移專案中的資料表欄，以參照目的地機構中新建立的政策標記。
* 政策標記階層從根節點到最低層級子標記，最多只能有五個層級，如以下螢幕截圖所示：

### 設定存取控管機制

分類與至少一個政策標記建立資料政策關聯後，系統就會自動強制執行[存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#enforce_access_control)。如要關閉存取控管功能，請先刪除與分類法相關聯的所有資料政策。

### materialized view 和重複記錄遮罩查詢

如果已有 materialized view，對相關聯基礎資料表執行的重複記錄遮蓋查詢會失敗。如要解決這個問題，請刪除 materialized view。如果基於其他原因需要 materialized view，可以在其他資料集中建立。

### 查詢分區資料表中的遮罩資料欄

不支援對分區或分群資料欄進行資料遮蓋的查詢。

### SQL 方言

不支援舊版 SQL。

### 自訂遮蓋處理常式

自訂遮蓋常式有下列限制：

* 自訂資料遮蓋功能支援所有 [BigQuery 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)，但 `STRUCT` 除外，因為資料遮蓋功能只能套用至 `STRUCT` 資料類型的葉節點欄位。
* 刪除自訂遮蓋常式不會刪除使用該常式的所有資料政策。不過，使用已刪除遮蓋常式的資料政策，會留下空白的遮蓋規則。如果其他資料政策具有相同標記，且使用者具備「遮蓋資料讀取者」角色，則可查看遮蓋資料。其他人會看到訊息
  `Permission denied.` 系統會在七天後，透過自動程序清除空白遮蓋規則的懸空參照。
* 每個政策標記只能有一個自訂遮蓋處理常式。

## 與其他 BigQuery 功能的相容性

### BigQuery API

與 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 方法不相容。如要呼叫 `tabledata.list`，您必須具備這個方法傳回的所有資料欄的完整存取權。Data Catalog 精細讀取者角色可授予適當的存取權。

### BigLake 資料表

相容。資料遮蓋政策會對 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)強制執行。

### BigQuery Storage Read API

相容。BigQuery Storage Read API 會強制執行資料遮蓋政策。

### BigQuery BI Engine

相容。BI Engine 會強制執行資料遮蓋政策。
如果查詢採用資料遮罩，BI Engine 就無法加速處理。在數據分析中使用這類查詢，可能會導致相關報表或資訊主頁的速度變慢，且費用更高。

### BigQuery Omni

相容。系統會對 BigQuery Omni 資料表強制執行資料遮蓋政策。

### 定序

部分相容。您可以對彙整的資料欄套用 DDM，但系統會在彙整前套用遮蓋功能。這種作業順序可能會導致非預期的結果，因為定序可能不會按照預期影響遮蓋值 (例如，遮蓋後可能無法進行不區分大小寫的比對)。您可以採取變通做法，例如使用自訂遮蓋常式，在套用遮蓋函式前先將資料正規化。

### 複製工作

不相容。如要將資料表從來源複製到目的地，您必須擁有來源資料表所有資料欄的完整存取權。Data Catalog 精細讀取者角色可授予適當的存取權。

### 資料匯出

相容。如果您具備 BigQuery 遮蓋讀取者角色，匯出的資料會經過遮蓋。如果您具備 Data Catalog 精細讀取者角色，匯出的資料就不會遮蓋。

### 資料列層級安全性

僅適用於具有非子查詢資料列存取政策的查詢。資料遮罩會套用至資料列層級安全性。舉例來說，如果 `location = "US"` 套用了資料列存取權政策，且 `location` 已遮蓋，使用者就能看到 `location = "US"` 的資料列，但結果中的位置欄位會遭到遮蓋。

如果查詢涉及子查詢資料列存取政策，則必須具備資料列存取政策所參照資料欄的「精細讀取者」存取權。

### 在 BigQuery 中搜尋

部分相容。您可以對已套用資料遮蓋的索引或未索引資料欄，呼叫 [`SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw) 函式。

對套用資料遮蓋的資料欄呼叫 `SEARCH` 函式時，必須使用與存取層級相容的搜尋條件。舉例來說，如果您擁有「已遮蓋的讀取者」存取權，並使用「雜湊 (SHA-256)」資料遮蓋規則，您會在 `SEARCH` 子句中使用雜湊值，類似於下列範例：

```
SELECT * FROM myDataset.Customers WHERE SEARCH(Email, "sg172y34shw94fujaweu");
```

如果您具備「精細讀取者」存取權，則應在 `SEARCH` 子句中使用實際資料欄值，如下所示：

```
SELECT * FROM myDataset.Customers WHERE SEARCH(Email, "jane.doe@example.com");
```

如果您對資料欄具有「經過遮蓋的讀取者」存取權，且該資料欄使用的資料遮蓋規則為「Nullify」或「Default Masking Value」，則搜尋功能可能不太實用。這是因為您用來做為搜尋條件的遮罩結果 (例如 `NULL` 或 `""`) 不夠獨特，無法發揮作用。

在套用資料遮蓋的索引資料欄中搜尋時，只有在您具備該資料欄的 Fine-Grained Reader 存取權時，系統才會使用搜尋索引。

### 快照

不相容。如要建立資料表的快照，您必須具備來源資料表所有資料欄的完整存取權。Data Catalog 精細讀取者角色可授予適當的存取權。

### 重新命名表格

相容。資料遮罩不會影響資料表重新命名。

### 時間回溯

與[時間裝飾器](https://docs.cloud.google.com/bigquery/docs/table-decorators?hl=zh-tw#time_decorators)和 `SELECT` 陳述式中的 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 選項相容。系統會將目前資料集結構定義的政策標記套用至擷取的資料。

### 查詢快取

部分相容。BigQuery 會[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)約 24 小時，但如果在此之前資料表資料或結構定義有所變更，快取就會失效。在下列情況下，即使使用者未獲派資料欄的 Data Catalog 精細讀取者角色，仍可在執行查詢時查看資料欄資料：

1. 使用者已獲得資料欄的 Data Catalog 精細讀取者角色。
2. 使用者執行查詢，其中包含受限資料欄，且資料已快取。
3. 在步驟 2 的 24 小時內，使用者會獲得 BigQuery 遮蓋讀取者角色，並撤銷 Data Catalog 精細讀取者角色。
4. 在步驟 2 的 24 小時內，使用者執行相同查詢，系統會傳回快取資料。

### Wildcard 資料表查詢

不相容。您必須具備完整存取權，才能存取符合萬用字元查詢的所有資料表中的所有參照資料欄。Data Catalog 精細讀取者角色可授予適當的存取權。

## 後續步驟

* 請參閱逐步說明，瞭解如何啟用[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]