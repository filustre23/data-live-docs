Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# API 效能提示

本文說明提升應用程式成效的幾個技巧。在某些情況下，我們會使用其他 API 或一般 API 的範例來說明這些技巧背後的概念。然而，同樣的概念也適用於 BigQuery API。

## 使用 gzip 壓縮

要減少每個要求占用的頻寬，最簡單的方法就是使用 gzip 壓縮檔。雖然此方法需要額外的 CPU 作業時間解壓縮，但相對可省下可觀的網路成本。

如果要接收以 gzip 編碼的回應，您必須執行下列兩項操作：設定 `Accept-Encoding` 標頭，並修改您的使用者代理程式來加入字串 `gzip`。以下是一個啟用 gzip 壓縮的正確 HTTP 標頭格式範例：

```
Accept-Encoding: gzip
User-Agent: my program (gzip)
```

## 使用部分資源

另一種提高 API 呼叫成效的方式，就是只收發您有興趣的資料。這麼做可避免讓您的應用程式傳輸、剖析及儲存不需要的欄位，進而更有效地使用網路、CPU 以及記憶體等資源。

部分要求分為兩類：

* [部分回應](#partial-response)：您可以在這類要求中，指定要在回應中加入哪些欄位 (使用 `fields` 要求參數)。
* [修補](#patch)：透過這類更新要求，您可以只傳送想要變更的欄位 (使用 `PATCH` HTTP 動詞)。

接下來的章節將會詳細說明如何提交部分要求。

### 部分回應

根據預設，伺服器會在處理要求後傳回完整的資源表示法。為改善成效，您可以要求伺服器只傳送您真正需要的欄位，並改為取得「部分回應」。

如果要請求部分回應，請使用 `fields` 要求參數來指定您想要傳回的欄位。您可以將此參數搭配任何會傳回回應資料的要求使用。

請注意，`fields` 參數只會影響回應資料；不會影響您需要傳送的資料 (如果有的話)。如果要減少您在修改資源時傳送的資料量，請使用[修補](#patch)要求。

#### 範例

以下範例顯示 `fields` 參數與某個通用 (虛構) 的「Demo」API 的搭配用法。

**簡易要求：**此 HTTP `GET` 要求會省略 `fields` 參數，並傳回完整的資源。

```
https://www.googleapis.com/demo/v1
```

**完整資源回應：**完整資源資料包括下列欄位 (為節省篇幅，此處省略許多其他欄位)。

```
{
  "kind": "demo",
  ...
  "items": [
  {
    "title": "First title",
    "comment": "First comment.",
    "characteristics": {
      "length": "short",
      "accuracy": "high",
      "followers": ["Jo", "Will"],
    },
    "status": "active",
    ...
  },
  {
    "title": "Second title",
    "comment": "Second comment.",
    "characteristics": {
      "length": "long",
      "accuracy": "medium"
      "followers": [ ],
    },
    "status": "pending",
    ...
  },
  ...
  ]
}
```

**要求部分回應：**以下是對相同資源發出的要求，其中使用了 `fields` 參數，以大幅減少傳回的資料量。

```
https://www.googleapis.com/demo/v1?fields=kind,items(title,characteristics/length)
```

**部分回應：**在上方的要求回應中，伺服器傳回的回應只包含種類資訊，以及經過簡化的項目陣列 (只包含個別項目的 HTML 標題和長度特性資訊)。

```
200 OK
```

```
{
  "kind": "demo",
  "items": [{
    "title": "First title",
    "characteristics": {
      "length": "short"
    }
  }, {
    "title": "Second title",
    "characteristics": {
      "length": "long"
    }
  },
  ...
  ]
}
```

請注意，回應是一個 JSON 物件，且此物件只包含選定的欄位及其所含的父項物件。

以下將詳述如何設定 `fields` 參數的格式，接著再進一步說明回應中實際傳回的內容。

#### Fields 參數語法摘要

`fields` 要求參數值的格式約略以 XPath 語法為基礎。支援的語法簡述如下，其他範例如下節所示。

* 使用以逗號分隔的清單來選取多個欄位。
* 使用 `a/b` 在 `a` 欄位的巢狀結構內選取 `b` 欄位；使用 `a/b/c` 在 `b` 的巢狀結構內選取 `c` 欄位。  

  **例外狀況：**如果 API 回應使用「data」包裝函式，也就是在 `data` 物件中建立看起來像 `data: { ... }` 的巢狀回應，請勿在 `fields` 規格中加入「`data`」。將 data 物件加入類似 `data/a/b` 的 fields 規格會造成錯誤。請改為只使用 `fields` 規格，例如 `a/b`。
* 透過在括號「`( )`」中放入運算式，使用子選擇器來要求一組指定的陣列或物件子欄位。

  例如：`fields=items(id,author/email)` 只會傳回項目陣列中各個元素的項目 ID 以及作者的電子郵件地址。您也可以指定單一子欄位，其中 `fields=items(id)` 等於 `fields=items/id`。
* 必要時，在欄位選取項目中使用萬用字元。

  例如：`fields=items/pagemap/*` 可選取網頁地圖中的所有物件。

#### 使用 fields 參數的其他範例

以下範例包含 `fields` 參數值會如何影響回應的說明。

**附註：**和所有查詢參數值一樣，`fields` 參數值也必須使用網址編碼。為方便閱讀，本文中的範例會省略編碼。

找出您要傳回的欄位，或「選取欄位」。
:   `fields` 要求參數值是以逗號分隔的欄位清單，每個欄位是根據回應的根來指定。因此，如果您執行的是清單作業，回應會是一個集合，其中通常包含資源陣列。如果您執行的作業傳回單一資源，欄位會根據該資源來指定。如果您選取的欄位是一個陣列 (或陣列的一部分)，則伺服器會傳回該陣列中所有元素的選定部分。  
      
    以下提供幾個集合層級的範例：  

    | 範例 | 效果 |
    | --- | --- |
    | `items` | 傳回項目陣列中的所有元素，包括每個元素中的所有欄位，但不包含其他欄位。 |
    | `etag,items` | 同時傳回 `etag` 欄位和項目陣列中的所有元素。 |
    | `items/title` | 只傳回項目陣列中所有元素的 `title` 欄位。    每當傳回巢狀欄位時，回應會包含其所含父項物件。父欄位不會包含任何其他的子欄位 (除非已同時明確地選擇這些欄位)。 |
    | `context/facets/label` | 只傳回 `facets` 陣列所有成員的 `label` 欄位，其本身是以巢狀結構嵌入 `context` 物件中。 |
    | `items/pagemap/*/title` | 針對項目陣列中的每個元素，只傳回屬於 `pagemap` 子項之所有物件的 `title` 欄位 (如果有的話)。 |

      
    以下提供幾個資源層級的範例：  

    | 範例 | 效果 |
    | --- | --- |
    | `title` | 傳回所要求資源的 `title` 欄位。 |
    | `author/uri` | 傳回所要求資源中 `author` 物件的 `uri` 子欄位。 |
    | `links/*/href` | 傳回屬於 `links` 子項之所有物件的 `href` 欄位。 |

使用「子選取項目」只請求指定欄位部分。
:   根據預設，如果您的要求指定特定的欄位，伺服器會傳回整個物件或陣列元素。您可以指定只包含特定子欄位的回應。方法很簡單，只要使用「`( )`」子選取項目語法即可，如下列範例所示。

    | 範例 | 效果 |
    | --- | --- |
    | `items(title,author/uri)` | 只傳回項目陣列中每個元素的 `title` 值以及作者的 `uri` 值。 |

#### 處理部分回應

伺服器處理包含 `fields` 查詢參數的有效要求後，會傳回一個 HTTP `200 OK` 狀態碼，以及所要求的資料。如果 `fields` 查詢參數發生錯誤或無效，伺服器會傳回 HTTP `400 Bad Request` 狀態碼和錯誤訊息，指出使用者選擇欄位時發生的錯誤 (例如 `"Invalid field selection a/b"`)。

以下是上方[簡介](#partial-response)一節中的部分回應範例。此要求使用 `fields` 參數來指定要傳回的欄位。

```
https://www.googleapis.com/demo/v1?fields=kind,items(title,characteristics/length)
```

部分回應的樣式如下所示：

```
200 OK
```

```
{
  "kind": "demo",
  "items": [{
    "title": "First title",
    "characteristics": {
      "length": "short"
    }
  }, {
    "title": "Second title",
    "characteristics": {
      "length": "long"
    }
  },
  ...
  ]
}
```

**附註：**如果 API 支援用於資料分頁的查詢參數 (例如 `maxResults` 和 `nextPageToken`)，請使用這些參數將每個查詢的結果減少到方便管理的大小。否則，可能無法有效提升部分回應的效能。

### 修補 (部分更新)

修改資源時，您也可以避免傳送不必要的資料。如果是僅為要變更的特定欄位傳送更新資料，請使用 HTTP `PATCH` 動詞。相較於舊版的 GData 部分更新執行方式，在本文中，「修補」一詞的語意變得更加簡單。

下面的簡短範例將會示範如何使用修補功能，在進行小規模更新時將您需要傳送的資料量減到最小。

#### 範例

此範例將會示範如何使用一段簡短的修補要求，只更新一個通用 (虛構) 的「Demo」API 資源標題。這項資源同時包含註解、一組特性、狀態以及許多其他欄位，但此要求只會傳送 `title` 欄位，因為這是唯一需要修改的欄位：

```
PATCH https://www.googleapis.com/demo/v1/324
Authorization: Bearer your_auth_token
Content-Type: application/json

{
  "title": "New title"
}
```

回應：

```
200 OK
```

```
{
  "title": "New title",
  "comment": "First comment.",
  "characteristics": {
    "length": "short",
    "accuracy": "high",
    "followers": ["Jo", "Will"],
  },
  "status": "active",
  ...
}
```

伺服器會傳回 `200 OK` 狀態碼，以及更新後資源的完整表示法。由於修補要求只包含 `title` 欄位，因此這個值是唯一與以往不同的值。

**附註：**如果您將[部分回應](#partial-response) `fields` 參數與修補一起使用，就可以進一步提高更新要求的效率。修補請求只能減少要求的大小，而部分回應則能減少回應的大小。因此，要減少雙向傳送的資料量，請將修補要求與 `fields` 參數搭配使用。

#### 修補要求的語意

修補要求的主體只包含您想要修改的資源欄位。您必須在指定欄位時加入任何其內含的父項物件，而這些欄位內含的父項物件將會連同[部分回應](#example-partial-response)一併傳回。修改後的資料會在傳送時合併至父物件的資料中 (如果有父物件存在的話)。

* **新增：**若要新增一個還不存在的欄位，請指定新的欄位及其欄位值。
* **修改：**若要變更現有欄位的值，請指定該欄位，並設為新的值。
* **刪除：**如要刪除欄位，請指定欄位並設為 `null`。例如 `"comment": null`。您也可以將可變動的物件設為 `null`，以便將整個物件刪除。如果您使用的是 [Java API 用戶端程式庫](https://docs.cloud.google.com/java/docs/reference?hl=zh-tw)，請改用 `Data.NULL_STRING`；詳情請參閱 [JSON null](https://googleapis.github.io/google-http-java-client/json.html#json-null) 的相關說明。

**有關陣列的注意事項：**含有陣列的修補要求會以您提供的陣列取代現有的陣列。您無法個別修改、新增或刪除陣列中的項目。

#### 在「讀取 - 修改 - 寫入」週期中使用修補功能

建議您可以從擷取附帶想要修改的資料的部分回應著手，特別是當資源使用 ETag 時。這是因為您必須提供 `If-Match` HTTP 標頭目前的 ETag 值，才能成功更新資源。取得資料之後，您便可以接著修改需要變更的值，並將修改過的部分表示法連同修補要求一併傳回。以下是一個假設 Demo 資源使用 ETag 的範例：

```
GET https://www.googleapis.com/demo/v1/324?fields=etag,title,comment,characteristics
Authorization: Bearer your_auth_token
```

以下是部分回應：

```
200 OK
```

```
{
  "etag": "ETagString"
  "title": "New title"
  "comment": "First comment.",
  "characteristics": {
    "length": "short",
    "level": "5",
    "followers": ["Jo", "Will"],
  }
}
```

以下修補要求是以該回應為建構依據。此要求同時使用 `fields` 參數來限制修補回應傳回的資料，如下所示：

```
PATCH https://www.googleapis.com/demo/v1/324?fields=etag,title,comment,characteristics
Authorization: Bearer your_auth_token
Content-Type: application/json
If-Match: "ETagString"
```

```
{
  "etag": "ETagString"
  "title": "",                  /* Clear the value of the title by setting it to the empty string. */
  "comment": null,              /* Delete the comment by replacing its value with null. */
  "characteristics": {
    "length": "short",
    "level": "10",              /* Modify the level value. */
    "followers": ["Jo", "Liz"], /* Replace the followers array to delete Will and add Liz. */
    "accuracy": "high"          /* Add a new characteristic. */
  },
}
```

伺服器會在回應中提供 200 OK HTTP 狀態碼，以及更新後資源的部分表示法：

```
200 OK
```

```
{
  "etag": "newETagString"
  "title": "",                 /* Title is cleared; deleted comment field is missing. */
  "characteristics": {
    "length": "short",
    "level": "10",             /* Value is updated.*/
    "followers": ["Jo" "Liz"], /* New follower Liz is present; deleted Will is missing. */
    "accuracy": "high"         /* New characteristic is present. */
  }
}
```

#### 直接建構修補要求

部分修補要求必須以您先前擷取的資料做為建構依據。舉例來說，如果您想要在陣列中新增一個項目，卻又不想失去任何現有的陣列元素，則您必須先取得現有的資料。同樣地，當 API 使用 ETag 時，您必須將先前的 ETag 值連同您的要求一起送出，才能成功更新資源。

**附註：**使用 ETag 時，您可以使用 `"If-Match: *"` HTTP 標頭強制通過修補。這麼一來，您就不需要在寫入之前先進行讀取。

然而，在其他情況下，您可以直接建構修補要求，而不需要先擷取現有的資料。舉例來說，您可以輕鬆建構一個用來更新欄位值或新增欄位的修補要求。範例如下：

```
PATCH https://www.googleapis.com/demo/v1/324?fields=comment,characteristics
Authorization: Bearer your_auth_token
Content-Type: application/json

{
  "comment": "A new comment",
  "characteristics": {
    "volume": "loud",
    "accuracy": null
  }
}
```

此要求會將註解欄位設為新的值，或是以新的值覆寫掉註解欄位現有的值。同樣地，如果有 volume 特性存在，則會覆寫掉該值；否則就會建立該特性。如果有設定好的精確度欄位存在，則會移除該欄位。

#### 處理修補回應

API 會在處理完有效的修補要求之後，傳回 `200 OK` HTTP 回應代碼以及修改後資源的完整表示法。如果 API 有使用 ETag 的話，伺服器會在成功處理完修補要求時更新 ETag 的值，就像 `PUT` 一樣。

修補要求會傳回整個資源表示法，除非您使用 `fields` 參數來減少傳回的資料量。

如果 修補 要求產生的新資源狀態具有無效的語法或語意，則伺服器會傳回 `400 Bad Request` 或 `422 Unprocessable Entity` HTTP 狀態碼，且資源狀態維持不變。舉例來說，如果您嘗試刪除必填欄位的值，則伺服器會傳回錯誤。

#### 當 PATCH HTTP 動詞未受支援時可使用的替代標示方法

如果您的防火牆禁止使用 HTTP `PATCH` 要求，請執行 HTTP `POST` 要求，並將替換標頭設定為 `PATCH`，如下所示：

```
POST https://www.googleapis.com/...
X-HTTP-Method-Override: PATCH
...
```

#### 修補和更新之間的差異

就實務層面而言，為使用了 HTTP `PUT` 動詞的更新要求傳送資料時，您只需要傳送必填或選填欄位；如果您傳送了由伺服器設定的欄位值，這些值將會遭到忽略。雖然這看起來像是執行部分更新的另一種方法，但此方法有一些限制存在。使用 HTTP `PUT` 動詞進行更新時，如果您沒有提供必要參數，則要求將會失敗；此外，如果您沒有提供選用參數，則要求將會清除先前設定的資料。

這也是在此情況下使用修補更加安全的原因。您只需要為您想要變更的欄位提供資料，而您省略的欄位將不會被清除。此規則唯一的例外便是重複元素或陣列：如果您全數省略，它們將會保持原狀；如果您提供了任何重複元素或陣列，則整組元素或陣列都會替換成您提供的組合。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]