* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# AEAD 加密概念 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

BigQuery 的 GoogleSQL 支援「附帶相關資料的驗證式加密」(AEAD) 加密。

本主題說明 GoogleSQL 中 AEAD 加密的相關概念。如需 GoogleSQL 支援的不同 AEAD 加密函式相關說明，請參閱 [AEAD 加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)。

### AEAD 加密的目的

BigQuery 採用靜態資料加密技術，可確保資料安全無虞。BigQuery 也支援客戶管理的加密金鑰 (CMEK)，可讓您使用特定加密金鑰將資料表加密。但在某些情況下，您可能需要加密資料表中的個別值。

例如，您希望將自己的所有顧客資料保存在通用資料表中，並使用不同金鑰為每位顧客的資料加密。您的資料分布在多個資料表中，而您希望對資料表進行「加密式刪除」作業。加密式刪除或加密式銷毀程序是指刪除加密金鑰，使以該金鑰加密的所有資料無法讀取。

AEAD 加密函式可讓您建立包含加密和解密金鑰的金鑰組、使用這些金鑰將資料表中的個別值加密和解密，以及輪替金鑰組內的金鑰。

### 金鑰組

金鑰組是一組加密編譯金鑰，其中一個金鑰是主要加密編譯金鑰，其餘金鑰 (若有) 為次要加密編譯金鑰。無論是已啟用、已停用或已刪除的金鑰，每個金鑰會針對[加密或解密演算法](#block_cipher_modes)進行編碼；未刪除的金鑰會對金鑰位元組本身進行編碼。主要加密編譯金鑰會判斷如何加密輸入明文，主要加密編譯金鑰永遠不會處於已停用狀態。次要加密編譯金鑰僅用於解密，可以是已啟用或已停用狀態。金鑰組可用於解密最初用來加密的任何資料。

GoogleSQL 金鑰組會以序列化的 [google.crypto.tink.Keyset](https://github.com/google/tink/blob/master/proto/tink.proto) 通訊協定緩衝區表示 (採用 `BYTES` 編碼)。

**範例**

以下的 AEAD 金鑰組示例是以三個金鑰表示的 JSON 字串。

```
{
  "primaryKeyId": 569259624,
  "key": [
    {
      "keyData": {
        "typeUrl": "type.googleapis.com/google.crypto.tink.AesGcmKey",
        "value": "GiDPhTp5gIhfnDb6jfKOT4SmNoriIJc7ah8uRvrCpdNihA==",
        "keyMaterialType": "SYMMETRIC"
      },
      "status": "ENABLED",
      "keyId": 569259624,
      "outputPrefixType": "TINK"
    },
    {
      "keyData": {
        "typeUrl": "type.googleapis.com/google.crypto.tink.AesGcmKey",
        "value": "GiBp6aU2cFbVfTh9dTQ1F0fqM+sGHXc56RDPryjAnzTe2A==",
        "keyMaterialType": "SYMMETRIC"
      },
      "status": "DISABLED",
      "keyId": 852264701,
      "outputPrefixType": "TINK"
    },
    {
      "status": "DESTROYED",
      "keyId": 237910588,
      "outputPrefixType": "TINK"
    }
  ]
}
```

在上面的示例中，主要加密編譯金鑰的 ID 為 `569259624`，是 JSON 字串中列出的第一個金鑰。示例中有兩個次要加密編譯金鑰，其中一個金鑰的 ID 為 `852264701`，處於已停用狀態；另一個金鑰的 ID 為 `237910588`，處於已刪除狀態。當 AEAD 加密函式使用這個金鑰組進行加密時，產生的密文會將 ID 為 `569259624` 的主要加密編譯金鑰編碼。

當 AEAD 函式使用這個金鑰組進行解密時，函式會根據在密文中編碼的金鑰 ID 選擇適當的金鑰進行解密。在上述示例中，嘗試使用金鑰 ID `852264701` 或 `237910588` 解密會發生錯誤，因為金鑰 ID `852264701` 已停用，而金鑰 ID `237910588` 已刪除。將金鑰 ID `852264701` 恢復到已啟用狀態，即可使用該金鑰進行解密。

金鑰類型會決定可搭配金鑰使用的[加密模式](#block_cipher_modes)。

如果您使用相同的金鑰組加密明文超過一次，系統通常會傳回不同的密文值，這是因為使用 OpenSSL 虛擬隨機號碼產生器所選擇的[初始向量 (IV)](#block_cipher_modes) 不同所致。

**注意：** 如果您嘗試以明文形式傳遞金鑰組做為查詢的一部分，系統可能會記錄查詢文字與搭配使用的明文金鑰組。您可以使用 BigQuery 的[參數化查詢](https://cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)，避免記錄純文字金鑰集。

### 經過包裝的金鑰集

如要安全地管理或透過不受信任的管道傳輸金鑰集，建議使用包裝金鑰集。包裝原始金鑰集時，這個程序會使用 [Cloud KMS 金鑰](#cloud_kms_protection)加密原始金鑰集。

經過包裝的金鑰集可加密及解密資料，不會洩漏金鑰集資料。雖然可能還有其他方法可限制存取欄位層級資料，但與原始鍵集相比，封裝鍵集可提供更安全的鍵集管理機制。

與[金鑰集](#keysets)一樣，經過包裝的金鑰集可以 (也應該) 定期輪替。包裝金鑰組用於 [AEAD 信封式加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)。

以下列舉幾個含有包裝鍵集的函式範例：

* [`KEYS.NEW_WRAPPED_KEYSET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keysnew_wrapped_keyset)：建立新的封裝金鑰集。
* [`KEYS.ROTATE_WRAPPED_KEYSET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keysrotate_wrapped_keyset)：輪替已包裝的金鑰集。
* [`KEYS.REWRAP_KEYSET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keysrewrap_keyset)：使用新資料重新包裝已包裝的鍵集。
* [`KEYS.KEYSET_CHAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keyskeyset_chain)：取得以 [Cloud KMS 金鑰](#cloud_kms_protection)加密的 [Tink](https://github.com/google/tink/blob/master/proto/tink.proto) 金鑰集。

### 高級加密標準 (AES)

[AEAD 加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)採用[進階加密標準 (AES) 加密技術](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)。AES 加密會將明文當做輸入，搭配一個加密編譯金鑰使用，並傳回已加密的位元組序列做為輸出。日後要解密這個位元組序列時，可使用與加密時相同的金鑰進行。AES 使用 16 位元組的區塊大小，也就是說 AES 將明文視為 16 位元組區塊的序列。密文會包含 Tink 專屬的前置字串，指出用來執行加密的金鑰。AES 加密支援多種[區塊加密模式](#block_cipher_modes)。

### 區塊加密模式

AEAD 加密函式支援兩種區塊加密模式：GCM 和 CBC。

#### GCM

[Galois/計數器模式 (GCM)](https://en.wikipedia.org/wiki/Galois%2FCounter_Mode) 是一種 AES 加密模式。函式會依序將區塊編號，然後將區塊編號與初始向量 (IV) 合併。初始向量可為隨機值或虛擬隨機值，是將明文資料隨機化的基礎。接下來，函式會使用 AES 加密合併的區塊編號和 IV。接著，函式會對加密結果和明文執行位元邏輯互斥或 (XOR) 運算，產生密文。GCM 模式使用的加密編譯金鑰長度為 128 或 256 位元。

#### CBC 模式

CBC 會針對每個明文區塊與前一個密文區塊進行 XOR 運算，然後再進行加密，藉此「鏈結」區塊。CBC 模式使用的加密編譯金鑰長度為 128、192 或 256 位元。CBC 以 16 位元組初始向量做為初始區塊，並針對這個初始區塊與第一個明文區塊進行 XOR 運算。

CBC 模式並非[密碼編譯意義上的 AEAD 方案](https://en.wikipedia.org/wiki/Authenticated_encryption)，因為它無法確保資料完整性。換句話說，系統不會偵測到加密資料遭到惡意修改，這也會損害資料機密性。因此，除非是為了相容舊版，否則不建議使用 CBC。

### 額外資料

AEAD 加密函式支援使用 `additional_data` 引數，此引數也稱為相關聯的資料 (AD) 或其他已驗證資料。
只有在解密時提供與加密時相同的額外資料，才能解密密文。因此，額外資料可用於將密文繫結至內容。

舉例來說，當您為特定顧客加密資料時，`additional_data` 可以做為 `CAST(customer_id AS STRING)` 的輸出。如此能確保解密資料前，已先使用預期的 `customer_id` 進行加密。解密時須使用相同的 `additional_data` 值。詳情請參閱 [RFC 5116](https://tools.ietf.org/html/rfc5116)。

### 解密

[`AEAD.ENCRYPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeadencrypt) 的輸出內容是密文 `BYTES`。[`AEAD.DECRYPT_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeaddecrypt_string) 或 [`AEAD.DECRYPT_BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeaddecrypt_bytes) 函式可以將此密文解密。這些函式使用的[金鑰組](#keysets)必須包含用來加密的金鑰，且該金鑰必須處於 `'ENABLED'` 狀態。此外，這些函式還必須使用加密時所用的相同 `additional_data`。

使用金鑰組進行解密時，系統會根據在密文中編碼的金鑰 ID 選擇適當的金鑰進行解密。

`AEAD.DECRYPT_STRING` 的輸出是明文 STRING，而 `AEAD.DECRYPT_BYTES` 的輸出是明文 `BYTES`。`AEAD.DECRYPT_STRING` 可以解密編碼 STRING 值的密文，`AEAD.DECRYPT_BYTES` 則可以解密編碼 `BYTES` 值的密文。若使用上述其中一個函式針對編碼錯誤資料類型的密文進行解密 (例如使用 `AEAD.DECRYPT_STRING` 解密編碼 `BYTES` 值的密文)，會產生未定義的行為，並可能導致錯誤發生。

### 金鑰輪替

輪替加密金鑰的主要目的，是減少使用任何特定金鑰加密的資料量。如此一來，即使金鑰遭盜用，攻擊者所能存取的資料也會比較少。

金鑰組輪替包含以下作業：

1. 在每個金鑰組中建立新的主要加密編譯金鑰。
2. 解密並重新加密所有已加密資料。

[`KEYS.ROTATE_KEYSET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keysrotate_keyset) 或 [`KEYS.ROTATE_WRAPPED_KEYSET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keysrotate_wrapped_keyset) 函式會執行第一個步驟，將新的主要加密編譯金鑰新增至金鑰組，並將原本的主要加密編譯金鑰變更為次要加密編譯金鑰。

### Cloud KMS 金鑰

GoogleSQL 支援使用 [Cloud KMS 金鑰](https://cloud.google.com/kms/docs/resource-hierarchy?hl=zh-tw)的 [AEAD 加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)，進一步保護資料安全。這層額外保護措施會使用金鑰加密金鑰 (KEK) 加密資料加密金鑰 (DEK)。KEK 是對稱加密金鑰集，安全地儲存在 Cloud Key Management Service 中，並使用 [Cloud KMS 權限和角色](https://cloud.google.com/kms/docs/reference/permissions-and-roles?hl=zh-tw#predefined)進行管理。

在查詢執行期間，請使用 [`KEYS.KEYSET_CHAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keyskeyset_chain) 函式提供 KEK 的 KMS 資源路徑，以及來自包裝 DEK 的密文。BigQuery 會呼叫 Cloud KMS 來解除包裝 DEK，然後使用該金鑰解密查詢中的資料。DEK 的未封裝版本只會在查詢期間儲存在記憶體中，之後就會銷毀。

詳情請參閱「[使用 Cloud KMS 金鑰進行 SQL 資料欄層級加密](https://docs.cloud.google.com/bigquery/docs/column-key-encrypt?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]