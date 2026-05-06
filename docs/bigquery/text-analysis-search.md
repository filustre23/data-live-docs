Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用文字分析器

[`CREATE SEARCH INDEX` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_search_index_statement)、[`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw)和 [`TEXT_ANALYZE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis-functions?hl=zh-tw#text_analyze)支援進階文字分析器設定選項。瞭解 BigQuery 的文字分析器及其選項，有助於提升搜尋體驗。

本文將概述 BigQuery 中提供的各種文字分析器及其設定選項，並舉例說明文字分析器如何搭配 BigQuery 中的[搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)功能運作。如要進一步瞭解文字分析器語法，請參閱「[文字分析](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw)」。

## 文字分析工具

BigQuery 支援下列文字分析器：

* `NO_OP_ANALYZER`
* `LOG_ANALYZER`
* `PATTERN_ANALYZER`

### `NO_OP_ANALYZER`

如果您有想要完全比對的預先處理資料，請使用 `NO_OP_ANALYZER`。系統不會對文字進行斷詞或正規化處理。由於這個分析器不會執行權杖化或正規化作業，因此不接受任何設定。如要進一步瞭解 `NO_OP_ANALYZER`，請參閱[`NO_OP_ANALYZER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw#no_op_analyzer)。

### `LOG_ANALYZER`

`LOG_ANALYZER` 會透過下列方式修改資料：

* 文字會轉換為小寫。
* 大於 127 的 ASCII 值會保留原樣。
* 系統會使用下列分隔符號，將文字拆分為個別字詞，稱為「詞元」：

  ```
  [ ] < > ( ) { } | ! ; , ' " * & ? + / : = @ . - $ % \ _ \n \r \s \t %21 %26
  %2526 %3B %3b %7C %7c %20 %2B %2b %3D %3d %2520 %5D %5d %5B %5b %3A %3a %0A
  %0a %2C %2c %28 %29
  ```

  如不想使用預設分隔符號，可以將所需分隔符號指定為文字分析器選項。`LOG_ANALYZER` 可讓您設定特定分隔符號和權杖篩選器，進一步控管搜尋結果。如要進一步瞭解使用 `LOG_ANALYZER` 時可用的特定設定選項，請參閱 [`delimiters` 分析器選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw#log_analyzer_options)和 [`token_filters` 分析器選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw#token_filters_option)。

### `PATTERN_ANALYZER`

`PATTERN_ANALYZER` 文字分析器會使用規則運算式從文字中擷取符記。與 `PATTERN_ANALYZER` 搭配使用的規則運算式引擎和語法為 [RE2](https://github.com/google/re2/)。`PATTERN_ANALYZER`
會依下列順序將模式權杖化：

1. 這個函式會在字串中尋找第一個符合模式的子字串 (從左側開始)。這是要納入輸出內容的權杖。
2. 系統會從輸入字串中移除所有內容，直到步驟 1 中找到的子字串結尾為止。
3. 並重複執行程序，直到字串為空為止。

下表提供 `PATTERN_ANALYZER` 權杖擷取作業的範例：

| 模式 | 輸入文字 | 輸出內容詞元 |
| --- | --- | --- |
| ab | ababab | * ab |
| ab | abacad | * ab |
| [a-z]{2} | abacad | * ab * ac * 廣告 |
| aaa | aaaaa | * aaa |
| [a-z]/ | a/b/c/d/e | * a/ * b/ * c/ * d/ |
| /[^/]+/ | aa/bb/cc | * /bb/ |
| [0-9]+ | abc |  |
| (?:/?)[a-z] | /abc | * /abc |
| (?:/)[a-z] | /abc | * /abc |
| (?:[0-9]abc){3}(?:[a-z]000){2} | 7abc7abc7abcx000y000 | * 7abc7abc7abcx000y000 |
| ".+" | 「cats」和「dogs」 | * 「cats」和「dogs」      請注意，使用[貪婪量詞 +](https://stackoverflow.com/questions/2301285/what-do-lazy-and-greedy-mean-in-the-context-of-regular-expressions) 會比對文字中最長的字串，導致「cats」和「dogs」在文字中擷取為符記。 |
| ".+?" | 「cats」和「dogs」 | * 「cats」 * 「dogs」      請注意，使用[延遲量詞 +?](https://stackoverflow.com/questions/2301285/what-do-lazy-and-greedy-mean-in-the-context-of-regular-expressions) 會讓規則運算式比對文字中最短的字串，導致「cats」、「dogs」在文字中擷取為 2 個獨立權杖。 |

使用 `PATTERN_ANALYZER` 文字分析器搭配 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw)時，您可以進一步控管從文字中擷取的符記。下表顯示不同模式和結果如何產生不同的 `SEARCH` 結果：

| 模式 | 查詢 | 文字 | 文字的詞元 | SEARCH(text, query) | 說明 |
| --- | --- | --- | --- | --- | --- |
| abc | abcdef | abcghi | * abcghi | TRUE | 'abc' in ['abcghi'] |
| cd[a-z] | abcdef | abcghi | * abcghi | FALSE | ['abcghi'] 中的 'cde' |
| [a-z]/ | a/b/ | a/b/c/d/ | * a/ * b/ * c/ * d/ | TRUE | ['a/', 'b/', 'c/', 'd/'] 中的 'a/'，以及 ['a/', 'b/', 'c/', 'd/'] 中的 'b/' |
| /[^/]+/ | aa/bb/ | aa/bb/cc/ | * /bb/ | TRUE | ['/bb/'] 中的 '/bb/' |
| /[^/]+/ | bb | aa/bb/cc/ | * /bb/ | 錯誤 | 查詢字詞中找不到相符的項目 |
| [0-9]+ | abc | abc123 |  | 錯誤 | 查詢字詞中找不到相符的項目 |
| [0-9]+ | `abc` | abc123 |  | 錯誤 | 查詢字詞中找不到相符的內容    將反引號視為反引號，而非特殊字元。 |
| [a-z][a-z0-9]\*@google\.com | 我的電子郵件地址是 test@google.com | test@google.com | * test@google.com | TRUE | 「test@google.com」在「test@google.com」中 |
| abc | abc\ abc | abc | * abc | TRUE | ['abc']中的 'abc'    請注意，由於空格已逸出，因此在搜尋查詢剖析器剖析後，'abc abc' 是單一子查詢(即)。 |
| (?i)(?:Abc) (未正規化) | aBcd | Abc | * Abc | FALSE | ['Abc'] 中的 'aBc' |
| (?i)(?:Abc)    normalization:  lower\_case = true | aBcd | Abc | * abc | TRUE | ['abc'] 中的 'abc' |
| (?:/?)abc | bc/abc | /abc/abc/ | * /abc | TRUE | '/abc' in ['/abc'] |
| (?:/?)abc | abc | d/abc | * /abc | FALSE | 'abc' in ['/abc'] |
| ".+" | 「cats」 | 「cats」和「dogs」 | * 「cats」和「dogs」 | FALSE | '"cats"' in ['"cats" and "dogs"]    請注意，使用[貪婪量詞 +](https://stackoverflow.com/questions/2301285/what-do-lazy-and-greedy-mean-in-the-context-of-regular-expressions) 會讓規則運算式比對文字中最長的字串，導致「cats」和「dogs」在文字中以符記形式擷取。 |
| ".+?" | 「cats」 | 「cats」和「dogs」 | * 「cats」 * 「dogs」 | TRUE | ""cats"" in ['""cats""', '""dogs""]    請注意，使用[延遲量詞 +?](https://stackoverflow.com/questions/2301285/what-do-lazy-and-greedy-mean-in-the-context-of-regular-expressions) 會讓規則運算式比對文字中最短的字串，導致「cats」、「dogs」在文字中分別擷取為 2 個獨立符記。 |

## 範例

以下範例說明如何使用文字分析和自訂選項建立搜尋索引、擷取權杖，以及傳回搜尋結果。

### `LOG_ANALYZER`，並使用 NFKC ICU 正規化和停用字詞

以下範例會使用 [NFKC ICU](https://en.wikipedia.org/wiki/Unicode_equivalence) 正規化和停用字，設定 `LOG_ANALYZER` 選項。這個範例假設有下列資料表，且已填入資料：

```
CREATE TABLE dataset.data_table(
  text_data STRING
);
```

如要建立具有 NFKC ICU 正規化和停用字清單的搜尋索引，請在 [`CREATE
SEARCH INDEX` DDL 陳述式的 `analyzer_options` 選項中，建立 JSON 格式的字串](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_search_index_statement)。如要查看使用 `LOG_ANALYZER` 建立搜尋索引時可用的完整選項清單，請參閱 [`LOG_ANALYZER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw#log_analyzer)。在本例中，停用字詞為 `"the", "of", "and", "for"`。

```
CREATE OR REPLACE SEARCH INDEX `my_index` ON `dataset.data_table`(ALL COLUMNS) OPTIONS(
  analyzer='PATTERN_ANALYZER',
  analyzer_options= '''{
    "token_filters": [
      {
        "normalizer": {
          "mode": "ICU_NORMALIZE",
          "icu_normalize_mode": "NFKC",
          "icu_case_folding": true
        }
      },
      { "stop_words": ["the", "of", "and", "for"] }
    ]
  }''');
```

以上述範例為例，下表說明各種 `text_data` 值的權杖擷取作業。請注意，為區分兩個問號 (??)，本文件中的雙問號字元 (*⁇*) 已以斜體標示：

| 資料文字 | 索引的權杖 | 說明 |
| --- | --- | --- |
| The Quick Brown Fox | ["quick", "brown", "fox"] | LOG\_ANALYZER 權杖化會產生權杖 ["The", "Quick", "Brown", "Fox"]。    接著，ICU 正規化會將權杖轉換為小寫，產生 ["the", "quick", "brown", "fox"]    最後，停用字篩選器會從清單中移除「the」。`icu_case_folding = true` |
| The Ⓠuick Ⓑrown Ⓕox | ["quick", "brown", "fox"] | LOG\_ANALYZER 權杖化會產生權杖 ["The", "Ⓠuick", "Ⓑrown", "Ⓕox"]。    接著，NFKC ICU 正規化會將權杖轉換為小寫，產生 ["the", "quick", "brown", "fox"]    最後，停用字詞篩選器會從清單中移除「the」。`icu_case_folding = true` |
| Ⓠuick*⁇*Ⓕox | ["quick??fox"] | LOG\_ANALYZER 權杖化會產生權杖 ["The", "Ⓠuick*⁇*Ⓕox"]。    接著，NFKC ICU 正規化會使用 `icu_case_folding = true` 將權杖轉換為小寫，產生 ["quick??fox"]。請注意，雙問號 Unicode 已正規化為 2 個問號 ASCII 字元。    最後，由於沒有任何權杖位於篩選器清單中，停用字詞篩選器不會執行任何動作。 |

搜尋索引建立完成後，您可以使用 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw)，透過搜尋索引中指定的相同分析器設定搜尋表格。請注意，如果 `SEARCH` 函式中的分析器設定與搜尋索引的設定不符，系統就不會使用搜尋索引。請使用下列查詢：

```
SELECT
  SEARCH(
  analyzer => 'LOG_ANALYZER',
  analyzer_options => '''{
    "token_filters": [
      {
        "normalizer": {
          "mode": "ICU_NORMALIZE",
          "icu_normalize_mode": "NFKC",
          "icu_case_folding": true
        }
      },
      {
        "stop_words": ["the", "of", "and", "for"]
      }
    ]
  }''')
```

更改下列內容：

* `search_query`：要搜尋的文字。

下表根據不同的搜尋文字和 `search_query` 值，列出各種結果：

| text\_data | `search_query` | 結果 | 說明 |
| --- | --- | --- | --- |
| The Quick Brown Fox | `"Ⓠuick"` | `TRUE` | 從文字中擷取的最終詞元清單為 ["quick", "brown", "fox"]。  從文字查詢擷取的最終符記清單為 ["quick"]。    清單查詢權杖全都會出現在文字權杖中。 |
| The Ⓠuick Ⓑrown Ⓕox | `"quick"` | `TRUE` | 從文字中擷取的最終權杖清單為 ["quick", "brown", "fox"]。  從文字查詢擷取的最終符記清單為 ["quick"]。    清單查詢權杖全都會出現在文字權杖中。 |
| Ⓠuick*⁇*Ⓕox | `"quick"` | `FALSE` | 從文字中擷取的最終權杖清單為 ["quick??fox"]。    從文字查詢擷取的最終符記清單為 ["quick"]。    「quick」不在文字的權杖清單中。 |
| Ⓠuick*⁇*Ⓕox | `"quick⁇fox"` | `TRUE` | 從文字中擷取的最終權杖清單為 ["quick??fox"]。    從文字查詢擷取的最終符記清單為 ["quick??fox"]。    「quick??fox」位於文字的詞元清單中。 |
| Ⓠuick*⁇*Ⓕox | `` "`quick⁇fox`" `` | `FALSE` | 在 `LOG_ANALYZER` 中，反引號必須與文字完全相符。 |

### `PATTERN_ANALYZER`：使用停用字詞搜尋 IPv4

以下範例會設定 `PATTERN_ANALYZER` 文字分析器，在篩除特定停用字詞的同時，搜尋特定模式。在本例中，模式會比對 IPv4 位址，並忽略本機主機值 (`127.0.0.1`)。

這個範例假設以下資料表已填入資料：

```
CREATE TABLE dataset.data_table(
  text_data STRING
);
```

如要建立搜尋索引，請在 [`CREATE SEARCH
INDEX` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_search_index_statement)的 `analyzer_options` 選項中，建立 JSON 格式的字串。`pattern` 選項和停用字清單。如要查看使用 `PATTERN_ANALYZER` 建立搜尋索引時可用的完整選項清單，請參閱 [`PATTERN_ANALYZER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw#pattern_analyzer)。在本範例中，我們的停用字詞是 localhost 位址 `127.0.0.1`。

```
CREATE SEARCH INDEX my_index
ON dataset.data_table(text_data)
OPTIONS (analyzer = 'PATTERN_ANALYZER', analyzer_options = '''{
  "patterns": [
    "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
  ],
  "token_filters": [
    {
      "stop_words": [
        "127.0.0.1"
      ]
    }
  ]
}'''
);
```

使用規則運算式搭配 `analyzer_options` 時，請加入三個開頭的 `\` 符號，正確逸出包含 `\` 符號的規則運算式，例如 `\d` 或 `\b`。

下表說明各種 `text_data` 值的權杖化選項

| 資料文字 | 索引的權杖 | 說明 |
| --- | --- | --- |
| abc192.168.1.1def 172.217.20.142 | ["192.168.1.1", "172.217.20.142"] | 即使位址和文字之間沒有空格，IPv4 模式仍會擷取 IPv4 位址。 |
| 104.24.12.10abc 127.0.0.1 | ["104.24.12.10"] | 「127.0.0.1」位於停用字詞清單中，因此會遭到篩除。 |

搜尋索引建立完成後，您可以使用 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw)，根據 `analyzer_options` 中指定的權杖化方式搜尋表格。請使用下列查詢：

```
SELECT
  SEARCH(dataset.data_table.text_data
  "search_data",
  analyzer => 'PATTERN_ANALYZER',
  analyzer_options => '''{
    "patterns": [
      "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
      ],
    "token_filters": [
      {
        "stop_words": [
          "127.0.0.1"
        ]
      }
    ]
  }'''
);
```

更改下列內容：

* `search_query`：要搜尋的文字。

下表根據不同的搜尋文字和 `search_query` 值，列出各種結果：

| text\_data | `search_query` | 結果 | 說明 |
| --- | --- | --- | --- |
| 128.0.0.2 | 「127.0.0.1」 | 錯誤 | 查詢中沒有搜尋權杖。    查詢會經過文字分析器，篩除「127.0.0.1」符記。 |
| abc192.168.1.1def 172.217.20.142 | 「192.168.1.1abc」 | TRUE | 從查詢中擷取的權杖清單為 ["192.168.1.1"]。    從文字中擷取的詞元清單為 ["192.168.1.1", "172.217.20.142"]。 |
| abc192.168.1.1def 172.217.20.142 | "`192.168.1.1`" | TRUE | 從查詢中擷取的權杖清單為 ["192.168.1.1"]。    從文字中擷取的詞元清單為 ["192.168.1.1", "172.217.20.142"]。    請注意，對於 PATTERN\_ANALYZER 而言，反引號會視為一般字元。 |

## 後續步驟

* 如要瞭解搜尋索引的用途、定價、必要權限和限制，請參閱「[BigQuery 搜尋功能簡介](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)」。
* 如要瞭解如何有效率地搜尋已建立索引的資料欄，請參閱「[使用索引搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]