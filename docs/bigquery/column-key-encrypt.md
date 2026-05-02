* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Cloud KMS 進行資料欄層級加密

您可以使用 [Cloud Key Management Service (Cloud KMS)](https://docs.cloud.google.com/kms/docs/concepts?hl=zh-tw) 加密金鑰，進而加密 BigQuery 資料表中的值。您可以使用 [AEAD 加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)搭配 Cloud KMS [金鑰集](https://docs.cloud.google.com/bigquery/docs/aead-encryption-concepts?hl=zh-tw#keysets)或[包裝金鑰集](https://docs.cloud.google.com/bigquery/docs/aead-encryption-concepts?hl=zh-tw#wrapped_keysets)，在資料欄層級提供第二層防護。

## 簡介

為提供多一層保護，Cloud KMS 會使用第二個金鑰加密金鑰 (KEK) 加密資料加密金鑰 (DEK)。在 BigQuery 中，參照加密金鑰組而非明文金鑰組，有助於降低金鑰外洩風險。KEK 是對稱加密金鑰集，安全地儲存在 Cloud KMS 中，並使用 Identity and Access Management (IAM) 角色和權限進行管理。

BigQuery 支援確定性和非確定性加密函式。使用確定性加密時，如果儲存的資料和額外已驗證資料 (選用) 都相同，則密文也會相同。這可支援以加密資料欄為基礎的彙整和聯結。使用非決定性加密時，無論加密資料為何，儲存的密文都是獨一無二，可防止叢集、匯總和聯結。

在查詢執行期間，您會提供 KEK 的 Cloud KMS 資源路徑，以及來自包裝 DEK 的密文。BigQuery 會呼叫 Cloud KMS 來解除包裝 DEK，然後使用該金鑰解密查詢中的資料。DEK 的未包裝版本只會在查詢期間儲存在記憶體中，之後就會銷毀。

如果您在支援 [Cloud External Key Manager](https://docs.cloud.google.com/kms/docs/ekm?hl=zh-tw) 的[區域](https://docs.cloud.google.com/kms/docs/ekm?hl=zh-tw#regions)使用 Cloud KMS，就能在 Cloud KMS 中使用以 Cloud EKM 為基礎的金鑰。

**注意：** 使用 Cloud EKM 金鑰可能會導致每次存取金鑰時，延遲時間增加。

### 用途

使用 Cloud KMS 金鑰加密的用途包括：

* 需要儲存在 BigQuery 中的外部加密資料，但不想以純文字形式儲存金鑰集。接著，您可以從資料表匯出資料，或使用 SQL 查詢解密資料。
* 對 BigQuery 中的加密資料進行「雙重存取權控管」。使用者必須同時獲得資料表和加密金鑰的權限，才能以明文形式讀取資料。

| **使用者權限矩陣** | | |
| --- | --- | --- |
|  | **資料表權限** | **沒有資料表權限** |
| **金鑰權限** | 讀取及解密加密資料。 | 沒有存取權。 |
| **金鑰沒有權限** | 讀取加密資料。 | 沒有存取權。 |

如果使用者有權存取 KMS 金鑰，且可存取包裝後的金鑰集，SQL 函式就能解開金鑰集包裝並解密密文。使用者也可以使用 Cloud KMS [REST API](https://docs.cloud.google.com/kms/docs/reference/rest?hl=zh-tw) 或 [CLI](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 解除包裝金鑰集。  
下列查詢範例使用 KMS SQL 函式解密非確定性密文：

```
SELECT
  AEAD.DECRYPT_STRING(
    KEYS.KEYSET_CHAIN(@kms_resource_name, @first_level_keyset),
    ciphertext,
    additional_authenticated_data)
FROM
  ciphertext_table
WHERE
  ...
```

#### 用途範例

假設郵遞區號屬於私密資訊，您可以使用 AEAD 加密函式，將郵遞區號資料插入 BigQuery 資料表，藉此加密 `Zipcode` 資料欄。在本範例中，我們將 `AEAD.ENCRYPT` 函式與包裝的金鑰組管理函式搭配使用。`KEYS.KEYSET_CHAIN` 函式會使用 KEK 解密數位加密金鑰，而 `AEAD.ENCRYPT` 函式會將資訊傳遞至 KMS。

加密和解密的金鑰集鏈可確保資料加密金鑰 (DEK) 會以 KEK 加密或包裝，並與該 KEK 一併傳遞。經過包裝的 DEK 會在 SQL 函式中解密或解除包裝，然後用於加密或解密資料。

當您在資料表上執行的查詢中使用函式存取資料時，AEAD 非決定性函式可以解密資料。

當您在資料表上執行的查詢中使用 AEAD 確定性函式存取資料時，該函式可以解密資料，並支援使用加密資料進行彙整和聯結。

### 非確定性函式語法

使用非確定性函式時，支援的語法包括：

```
AEAD.ENCRYPT(
  KEYS.KEYSET_CHAIN(kms_resource_name, first_level_keyset),
  plaintext,
  additional_authenticated_data)
```

```
AEAD.DECRYPT_STRING(
  KEYS.KEYSET_CHAIN(kms_resource_name, first_level_keyset),
  ciphertext,
  additional_authenticated_data)
```

```
AEAD.DECRYPT_BYTES(
  KEYS.KEYSET_CHAIN(kms_resource_name, first_level_keyset),
  ciphertext,
  additional_authenticated_data)
```

請參閱 [`AEAD.DECRYPT_BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeaddecrypt_bytes)、[`AEAD.ENCRYPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeadencrypt)、[`AEAD.DECRYPT_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeaddecrypt_string) 和 [`KEYS.KEYSET_CHAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keyskeyset_chain) 函式語法。

### 決定性函式語法

使用確定性函式的支援語法包括：

```
DETERMINISTIC_ENCRYPT(
  KEYS.KEYSET_CHAIN(kms_resource_name, first_level_keyset),
  plaintext,
  additional_data)
```

```
DETERMINISTIC_DECRYPT_STRING(
  KEYS.KEYSET_CHAIN(kms_resource_name, first_level_keyset),
  ciphertext,
  additional_data)
```

```
DETERMINISTIC_DECRYPT_BYTES(
  KEYS.KEYSET_CHAIN(kms_resource_name, first_level_keyset),
  ciphertext,
  additional_data)
```

請參閱 [`DETERMINISTIC_DECRYPT_BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#deterministic_decrypt_bytes)、[`DETERMINISTIC_ENCRYPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#deterministic_encrypt)、[`DETERMINISTIC_DECRYPT_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#deterministic_decrypt_string) 和 [`KEYS.KEYSET_CHAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keyskeyset_chain) 函式語法。

## 角色和權限

如需 Cloud KMS 的角色清單，請參閱 [Cloud KMS 權限和角色](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles?hl=zh-tw#predefined)。

## 限制

使用 Cloud KMS 加密時，有下列限制：

* Cloud KMS 金鑰僅限於與查詢相同的[區域或多區域](https://docs.cloud.google.com/kms/docs/locations?hl=zh-tw)。基於可靠性考量，系統不允許使用全域 Cloud KMS 金鑰。
* 您無法使用 `KEYS.ROTATE_KEYSET` 函式輪替包裝的鍵集。
* BigQuery 查詢中的常數參數會顯示在[診斷查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)中。這項因素可能會影響 `KEYSET_CHAIN` 函式的 `kms_resource_name` 和 `first_level_keyset` 參數。金鑰絕不會以純文字形式公開，且必須具備 Cloud KMS 金鑰的權限，才能解密包裝的金鑰集。除非使用者有權解密金鑰集，否則這個方法可確保金鑰不會透過診斷查詢計畫公開。
* 搭配使用資料欄層級加密和類型式安全分類時，有下列限制：

  + 資料欄層級安全防護：使用者只能解密或加密允許存取的資料欄資料。
  + 資料列層級安全性：使用者只能解密允許存取的資料列。
* 與以純文字傳送金鑰資料的原始加密函式效能相比，資料欄層級的 SQL 函式對效能沒有顯著影響。

## 事前準備

如要使用 Cloud KMS 金鑰、金鑰集、加密資料表、決定性函式和非決定性函式，請先完成下列步驟 (如尚未完成)：

1. [建立 Google Cloud 專案](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw#creating_a_project)。
2. [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#create-dataset)。
3. [建立 Cloud KMS 金鑰環](https://docs.cloud.google.com/kms/docs/creating-keys?hl=zh-tw#create_a_key_ring)。
4. [建立 Cloud KMS 金鑰](https://docs.cloud.google.com/kms/docs/creating-keys?hl=zh-tw#create_a_key)，並將軟體或[硬體安全模組 (HSM)](https://docs.cloud.google.com/kms/docs/hsm?hl=zh-tw) 防護等級設為加密資料欄。
5. [授予使用者權限，以便處理 Cloud KMS 金鑰、加密和解密作業](#roles)。

請注意下列概念，因為後續章節會參考這些概念：

* `PROJECT_ID`：Google Cloud 專案的名稱。
* `DATASET_NAME`：BigQuery 資料集的名稱。
* `LOCATION_ID`：BigQuery 資料集的位置。
* `TABLE_NAME`：BigQuery 資料表的名稱。
* `KEY_RING_ID`：Cloud KMS 金鑰環的名稱。
* `KEY_ID`：Cloud KMS 金鑰的名稱。
* `KMS_KEY`：Cloud KMS 金鑰 (KEK)，格式如下：

  ```
  'gcp-kms://projects/PROJECT_ID/locations/LOCATION_ID/keyRings/KEY_RING_ID/cryptoKeys/KEY_ID'
  ```

  以下是 Cloud KMS 金鑰的範例：

  ```
  'gcp-kms://projects/myProject/locations/us/keyRings/myKeyRing/cryptoKeys/myKeyName'
  ```
* `KMS_KEY_SHORT`：與 `KMS_KEY` 類似，但格式如下：

  ```
  projects/PROJECT_ID/locations/LOCATION_ID/keyRings/KEY_RING_ID/cryptoKeys/KEY_ID
  ```
* `KEYSET_DECODED`：解碼後的鍵集，以 `BYTES` 序列表示。輸出結果與解碼後的封裝金鑰集類似。

  雖然金鑰集函式會以位元組形式傳回金鑰集，但使用者輸出內容會顯示為編碼字串。如要將編碼鍵集轉換為解碼鍵集，請參閱「[解碼 Cloud KMS 鍵集](#decode-wrapped-keyset)」一文。
* `KEYSET_ENCODED`：編碼的鍵集 (`STRING`)。輸出內容與編碼包裝鍵集類似。

  如要將編碼鍵集轉換為解碼鍵集，請參閱「[解碼 Cloud KMS 鍵集](#decode-wrapped-keyset)」一文。
* `WRAPPED_KEYSET_DECODED`：解碼後的包裝金鑰集，以 `BYTES` 序列表示。
  以下是輸出內容的範例：

  ```
  b'\x0a$\x00\xa6\xee\x12Y\x8d|l"\xf7\xfa\xc6\xeafM\xdeefy\xe9\x7f\xf2z\xb3M\
  xf6"\xd0\xe0Le\xa8\x8e\x0fR\xed\x12\xb7\x01\x00\xf0\xa80\xbd\xc1\x07Z\\
  \xd0L<\x80A0\x9ae\xfd(9\x1e\xfa\xc8\x93\xc7\xe8\...'
  ```

  雖然包裝鍵集函式會以位元組形式傳回包裝鍵集，但使用者輸出內容會顯示為編碼字串。如要將編碼的包裝金鑰集轉換為解碼的包裝金鑰集，請參閱「[解碼 Cloud KMS 金鑰集](#decode-wrapped-keyset)」一文。
* `WRAPPED_KEYSET_ENCODED`：編碼的包裝鍵集，格式為 `STRING`。
  以下是輸出內容的範例：

  ```
  'CiQApu4SWTozQ7lNwITxpEvGlo5sT2rv1tyuSv3UAMtoTq/lhDwStwEA8KgwvX7CpVVzhWWMkRw
  WZNr3pf8uBIlzHeunCy8ZsQ6CofQYFpiBRBB6k/QqATbiFV+3opnDk/6dBL/S8OO1WoDC+DdD9
  uzEFwqt5D20lTXCkGWFv1...'
  ```

  如要將編碼的包裝金鑰集轉換為解碼的包裝金鑰集，請參閱「[解碼 Cloud KMS 金鑰集](#decode-wrapped-keyset)」一文。

## 金鑰管理

以下各節說明如何使用 Cloud KMS 金鑰執行常見工作。

### 建立金鑰組

您可以建立已包裝的金鑰集或原始金鑰集。如要這樣做，請完成下列各節的步驟。

#### 建立原始金鑰組

執行下列查詢，建立含有 `DETERMINISTIC_AEAD_AES_SIV_CMAC_256` 型別金鑰的金鑰集。

```
SELECT KEYS.NEW_KEYSET('DETERMINISTIC_AEAD_AES_SIV_CMAC_256') AS raw_keyset
```

#### 建立已包裝金鑰組

執行下列查詢，使用 `DETERMINISTIC_AEAD_AES_SIV_CMAC_256` 類型的金鑰建立 Cloud KMS 包裝的金鑰集。

```
SELECT KEYS.NEW_WRAPPED_KEYSET(
  KMS_KEY,
  'DETERMINISTIC_AEAD_AES_SIV_CMAC_256')
```

### 解碼金鑰組

雖然傳回鍵集的 SQL 函式會以 `BYTES` 格式產生鍵集，但使用者看到的結果會以 `STRING` 格式編碼並顯示。如要將這個編碼字串轉換為解碼位元組序列，以便做為字面金鑰加密函式使用，請使用下列查詢。

#### 解碼包裝金鑰組

執行下列查詢，解碼 Cloud KMS 包裝金鑰集。

```
SELECT FORMAT('%T', FROM_BASE64(WRAPPED_KEYSET_ENCODED'))
```

#### 解碼原始金鑰組

執行下列查詢，解碼原始鍵集。

```
SELECT FORMAT('%T', FROM_BASE64(KEYSET_ENCODED'))
```

### 重新包裝已包裝的金鑰集

執行下列查詢，使用新的 Cloud KMS 金鑰重新包裝 Cloud KMS 包裝金鑰集。`KMS_KEY_CURRENT` 代表用於加密金鑰組的新 `KMS_KEY`。`KMS_KEY_NEW` 代表用於加密金鑰組的新 `KMS_KEY`。

```
SELECT KEYS.REWRAP_KEYSET(
  KMS_KEY_CURRENT,
  KMS_KEY_NEW,
  WRAPPED_KEYSET_DECODED)
```

### 輪替包裝金鑰集

執行下列查詢，使用 `DETERMINISTIC_AEAD_AES_SIV_CMAC_256` 類型的金鑰輪替 Cloud KMS 包裝金鑰集。

```
SELECT KEYS.ROTATE_WRAPPED_KEYSET(
  KMS_KEY,
  WRAPPED_KEYSET_DECODED,
  'DETERMINISTIC_AEAD_AES_SIV_CMAC_256')
```

### 從已包裝金鑰組產生原始金鑰組

部分加密函式需要原始金鑰集。如要解密 Cloud KMS 包裝的鍵集，產生原始鍵集，請完成下列步驟。

1. [建立已包裝的金鑰組](#wrap-keyset)。
2. 在 bq 指令列工具中輸入下列指令，將包裝過的鍵集儲存在名為 `keyset_to_unwrap` 的檔案中、解密包裝過的鍵集，並以 `KEYSET_DECODED` 格式產生輸出內容：

   ```
   echo WRAPPED_KEYSET_ENCODED | base64 -d > /tmp/decoded_wrapped_key
   ```

   ```
   gcloud kms decrypt \
   --ciphertext-file=/tmp/decoded_wrapped_key \
   --key=KMS_KEY_SHORT \
   --plaintext-file=/tmp/keyset_to_unwrap.dec \
   --project=PROJECT_ID
   ```

   ```
   od -An --format=o1 /tmp/keyset_to_unwrap.dec | tr ' ' '\'
   ```

### 從原始金鑰組產生已包裝金鑰組

部分加密功能需要 Cloud KMS 包裝的鍵集。如要加密原始金鑰集以產生包裝金鑰集，請完成下列步驟。

1. [建立原始鍵集](#raw-keyset)。
2. 在 bq 指令列工具中輸入下列指令，將原始鍵集儲存在名為 `keyset_to_wrap` 的檔案中、加密原始鍵集，並以 `WRAPPED_KEYSET_DECODED` 格式產生輸出內容：

   ```
   echo KEYSET_ENCODED | base64 -d > /tmp/decoded_key
   ```

   ```
   gcloud kms encrypt \
   --plaintext-file=/tmp/decoded_key \
   --key=KMS_KEY_SHORT \
   --ciphertext-file=/tmp/keyset_to_wrap.dec \
   --project=PROJECT_ID
   ```

   ```
   od -An --format=o1 /tmp/keyset_to_wrap.dec | tr ' ' '\'
   ```

### 為 DLP 函式產生已包裝金鑰

如要使用 [DLP 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dlp_functions?hl=zh-tw)，您需要加密編譯金鑰，然後使用該金鑰取得包裝金鑰。

1. 如要產生新的加密金鑰，請在[指令列](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)中執行下列指令。金鑰大小可以是 16、24 或 32 個位元組。
   以下範例使用 16 位元組的金鑰：

   ```
   openssl rand 16 > rand.key.16.bin
   ```
2. 使用 [KMS 金鑰](https://docs.cloud.google.com/sdk/gcloud/reference/kms/encrypt?hl=zh-tw)包裝產生的 16 位元組金鑰。
   請參閱以下範例：

   ```
   KEYRING=projects/myproject/locations/us/keyRings/kms-test
   KEY=projects/myproject/locations/us/keyRings/kms-test/cryptoKeys/test-Kek
   PROJECT="myproject"

   gcloud kms encrypt --project $PROJECT --location us --keyring $KEYRING --key $KEY --plaintext-file ./rand.key.16.bin --ciphertext-file ./rand.key.16.wrapped
   ```
3. 您現在可以取得包裝金鑰的 `BYTES` 常值，或包裝金鑰的 Base64 格式。

   * **位元組常值**

     ```
     username:~/tmp$ od -b ./rand.key.16.wrapped | cut -d ' ' -f 2- | head -n -1 | sed  -e 's/^/ /' | tr ' ' '\'
     ```

     輸出內容如下：

     ```
     \012\044\000\325\155\264\153\246\071\172\130\372\305\103\047\342\356\061\077\014\030\126\147\041\126\150\012\036\020\202\215\044\267\310\331\014\116\233\022\071\000\363\344\230\067\274\007\340\273\016\212\151\226\064\200\377\303\207\103\147\052\267\035\350\004\147\365\251\271\133\062\251\246\152\177\017\005\270\044\141\211\116\337\043\035\263\122\340\110\333\266\220\377\247\204\215\233
     ```
   * **Base64 格式**

     ```
     username:~/tmp$ base64 ./rand.key.16.wrapped
     ```

     輸出內容如下：

     ```
     CiQA1W20a6Y5elj6xUMn4u4xPwwYVmchVmgKHhCCjSS3yNkMTpsSOQDz5Jg3vAfguw6KaZY0gP/Dh0NnKrcd6ARn9am5WzKppmp/DwW4JGGJTt8jHbNS4EjbtpD/p4SNmw==
     ```

### 取得鍵組中的金鑰數量

執行下列查詢，取得原始鍵集中的金鑰數量。

1. 如果您使用的是包裝金鑰集，請先[產生原始金鑰集](#generate-raw-keyset)。
2. 使用原始鍵集執行這項查詢：

   ```
   SELECT KEYS.KEYSET_LENGTH(KEYSET_DECODED) as key_count;
   ```

### 取得鍵組的 JSON 表示法

執行下列查詢，即可查看原始金鑰組的 JSON 表示法。

1. 如果您使用的是包裝金鑰集，請先[產生原始金鑰集](#generate-raw-keyset)。
2. 使用原始鍵集執行這項查詢：

   ```
   SELECT KEYS.KEYSET_TO_JSON(KEYSET_DECODED);
   ```

## 加密與解密

您可以使用原始金鑰組或包裝金鑰組，加密表格中的資料欄。您也可以選擇在資料欄上使用確定性或非確定性加密。本節範例使用包裝過的鍵集，但您可以將包裝過的鍵集換成原始鍵集。

### 使用包裝的金鑰集，以決定性方式加密資料欄

執行下列查詢，建立資料表並在名為 `encrypted_content` 的資料欄中，儲存 Cloud KMS 包裝金鑰組和確定性加密。

1. [建立已包裝的金鑰組](#wrap-keyset)。
2. 使用包裝的金鑰集加密資料欄。

   ```
   CREATE OR REPLACE TABLE DATASET_NAME.TABLE_NAME AS
     SELECT DETERMINISTIC_ENCRYPT(
       KEYS.KEYSET_CHAIN(KMS_KEY, WRAPPED_KEYSET_DECODED),
       'plaintext',
       '') AS encrypted_content
   ```

### 使用包裝過的鍵集，以決定性方式解密資料欄

執行下列查詢，使用以 Cloud KMS 包裝的金鑰組，確定性解密含有加密內容的資料欄。這項查詢假設您參照的資料表含有名為 `encrypted_content` 的資料欄。

```
SELECT DETERMINISTIC_DECRYPT_STRING(
  KEYS.KEYSET_CHAIN(KMS_KEY, WRAPPED_KEYSET_DECODED),
  encrypted_content,
  '')
FROM DATASET_NAME.TABLE_NAME
```

### 使用包裝過的金鑰集，以非決定性方式加密資料欄

請參閱「[使用包裝鍵集確定性加密資料欄](#determine-encrypt-column)」，但請將 `DETERMINISTIC_ENCRYPT` 替換為 `AEAD.ENCRYPT`。確認金鑰集類型為 `AEAD_AES_GCM_256`。

### 使用包裝的金鑰集，以非決定性方式解密資料欄

請參閱「[使用包裝鍵集確定性解密資料欄](#determine-decrypt-column)」，但請將 `DETERMINISTIC_DECRYPT_STRING` 替換為 `AEAD.DECRYPT_STRING`。請確認金鑰集類型為 `AEAD_AES_GCM_256`。

## 後續步驟

* 進一步瞭解 [Cloud KMS](https://docs.cloud.google.com/kms/docs/resource-hierarchy?hl=zh-tw)。
  本主題包含 Google Cloud的資料欄層級加密概念資訊。
* 進一步瞭解 [BigQuery 的 AEAD 加密](https://docs.cloud.google.com/bigquery/docs/aead-encryption-concepts?hl=zh-tw)。
  本主題包含 BigQuery 專用的資料欄層級加密概念資訊。
* 進一步瞭解 [BigQuery 的 AEAD 加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)。
  本主題列出所有可用於 BigQuery 中資料欄層級加密的 SQL 函式。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]