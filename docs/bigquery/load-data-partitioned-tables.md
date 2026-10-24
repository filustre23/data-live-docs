Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料載入分區資料表

本文說明如何將資料載入分區資料表。

## 將資料寫入特定分割區

您可以使用 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令搭配分區修飾符，將資料載入特定分區。假設現有資料表已按日期分區，以下範例會將資料附加到 `20160501` (2016 年 5 月 1 日) 分區：

```
bq load --source_format=CSV 'my_dataset.my_table$20160501' data.csv
```

您也可以將查詢結果寫入特定分區：

```
bq query \
  --use_legacy_sql=false  \
  --destination_table='my_table$20160501' \
  --append_table=true \
  'SELECT * FROM my_dataset.another_table'
```

使用擷取時間分區時，您可以運用這項技巧，將較舊的資料載入對應資料原始建立時間的分區。

您也可以使用這項技術調整時區。根據預設，擷取時間分區是以世界標準時間為準。如要讓分區時間符合特定時區，可以使用分區修飾符來抵銷世界標準時間的擷取時間。舉例來說，如果您位於太平洋標準時間 (PST) 時區，可利用相應的明確分區修飾符 `$2016050123`，將太平洋標準時間 2016 年 5 月 1 日 23:30 產生的資料載入該日期的分區。如果您未使用這個明確的裝飾器，系統會改為載入 `$2016050207` (5 月 2 日 07:00 UTC)。

如果是時間單位資料欄和整數範圍分區資料表，修飾符中指定的分區 ID 必須與要寫入的資料相符。舉例來說，如果資料表是依據 `DATE` 資料欄分區，裝飾符必須與該資料欄中的值相符。否則會發生錯誤。不過，如果您事先知道資料位於單一分區，指定分區修飾符可以提升寫入效能。

上述範例會將資料附加至分區。如要改為覆寫分割區中的資料，您必須為每個指令加入不同的旗標，也就是 `bq load --replace=true ...` 和 `bq query --append_table=false ...`。
如要進一步瞭解這些指令中的標記，請參閱 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 和 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)。

如要進一步瞭解如何載入資料，請參閱[將資料載入 BigQuery 的簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)一文。

## 以串流方式將資料傳入分區資料表

如要瞭解如何使用 BigQuery Storage Write API (gRPC) 將資料串流至分區資料表，請參閱[以串流方式將資料傳入分區資料表](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#stream_into_partitioned_tables)。

## 後續步驟

如要進一步瞭解分區資料表的使用，請參閱：

* [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)
* [管理分區資料表](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw)
* [查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]