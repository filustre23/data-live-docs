Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用差異化隱私 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本文提供 BigQuery 差異化隱私的一般資訊。如需語法，請參閱[差異化隱私權條款](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)。如要查看可搭配這項語法使用的函式清單，請參閱[差異隱私匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-dp-functions?hl=zh-tw)。

**注意：** 本主題範例中的隱私權參數並非建議。您應與隱私或資安人員合作，為資料集和機構決定最合適的隱私參數。

## 什麼是差異化隱私？

差異化隱私是資料運算的標準，可限制輸出內容中揭露的個人資訊量。差異化隱私經常用於分享資料，以及推論使用者群組，同時避免個人相關資訊外洩。

差異化隱私的用途：

* 存在重新識別化風險。
* 量化風險與分析實用性之間的取捨。

為了進一步瞭解差異化隱私，我們來看一個簡單的例子。

這張長條圖顯示某個晚上小型餐廳的忙碌程度。許多顧客會在晚上 7 點光臨，而餐廳在凌晨 1 點完全沒有顧客：



這張圖表看起來很實用，但有個問題。有新訪客抵達時，長條圖會立即顯示這項事實。從下圖可清楚看出有新訪客，且該訪客大約在凌晨 1 點抵達：



從隱私權角度來看，顯示這項詳細資料並不理想，因為匿名統計資料不應揭露個人貢獻。將這兩個圖表並排顯示，會更加明顯：橘色長條圖在凌晨 1 點左右多了一位訪客：



這同樣不是理想的結果。如要避免這類隱私權問題，可以使用差異化隱私權，在長條圖中加入隨機雜訊。在下方的比較圖表中，結果會經過匿名處理，不再顯示個別貢獻。



## 查詢的差異化隱私權運作方式

[差異化隱私](https://www.cis.upenn.edu/%7Eaaroth/Papers/privacybook.pdf)的目標是降低資料外洩風險，防止他人取得資料集中實體的相關資訊。差異化隱私權可兼顧隱私權保護和統計分析實用性。隱私權越高，統計分析實用性就越低，反之亦然。

您可以使用 BigQuery 的 GoogleSQL，透過差異隱私權匯總轉換查詢結果。執行查詢時，系統會進行下列操作：

1. 如果使用 `GROUP BY` 子句指定群組，系統會計算每個群組的實體匯總。根據`max_groups_contributed`差異化隱私權參數，限制每個實體可加入的群組數量。
2. [限制](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-dp-functions?hl=zh-tw#dp_clamping)每個實體的匯總貢獻度，使其落在限制範圍內。如果未指定箝制界限，系統會以差異隱私權方式隱含計算。
3. 匯總每個群組的實體匯總貢獻值，並限制取值範圍。
4. 在每個群組的最終匯總值中加入雜訊。隨機雜訊的規模是所有限制取值範圍和隱私權參數的函式。
5. 計算每個群組套用雜訊的實體數量，刪除實體數量較少的群組。有雜訊的實體計數有助於排除非決定性群組集。

最終結果是一個資料集，其中每個群組的匯總結果都套用雜訊，且刪除人數較少的群體。

**注意：** BigQuery 採用 [Google 的差異化隱私開放原始碼程式庫](https://github.com/google/differential-privacy)，這個程式庫提供低層級的差異化隱私基元，可用於實作端對端隱私系統。如要進一步瞭解相關保證，請參閱「[隱私權保證的限制](#privacy_guarantees)」。**注意：** BigQuery 另外也支援 BigQuery Omni 資料來源的差異化隱私，包括 Amazon Simple Storage Service (Amazon S3)。BigQuery 遠端函式也可以呼叫外部差異化隱私程式庫，例如 [Tumult Analytics](https://docs.tmlt.dev/analytics/latest/index.html)。

如要進一步瞭解差異化隱私及其用途，請參閱下列文章：

* [差異化隱私權的友善非技術簡介](https://desfontain.es/privacy/friendly-intro-to-differential-privacy.html)
* [具有有界使用者貢獻的差異隱私權 SQL](https://arxiv.org/abs/1909.01917)
* [維基百科上的差異化隱私](https://en.wikipedia.org/wiki/Differential_privacy)

## 產生有效的差異隱私查詢

差異隱私權查詢必須符合下列規則，才算有效：

* 定義[隱私權單位欄](#dp_define_privacy_unit_id)。
* `SELECT` 清單包含[差異隱私權子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)。
* 只有[差異隱私匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-dp-functions?hl=zh-tw)會出現在 `SELECT` 清單中，並附上差異隱私子句。

## 定義隱私權單位欄

隱私權單元是資料集中受保護的實體，使用差異化隱私權。實體可以是個人、公司、地點或您選擇的任何資料欄。

差異化隱私查詢必須包含一個且僅有一個*隱私單位欄*。隱私權單元資料欄是隱私權單元的專屬 ID，可存在於多個群組中。由於系統支援多個群組，隱私權單位欄的資料類型必須是[可分組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#groupable_data_types)的類型。

您可以在差異化隱私子句的 `OPTIONS` 子句中，使用專屬 ID `privacy_unit_column` 定義隱私單位欄。

在下列範例中，隱私權單位欄會新增至差異化隱私子句。`id` 代表來自名為 `students` 的資料表資料欄。

```
SELECT WITH DIFFERENTIAL_PRIVACY
  OPTIONS (epsilon=10, delta=.01, privacy_unit_column=id)
  item,
  COUNT(*, contribution_bounds_per_group=>(0, 100))
FROM students;
```

```
SELECT WITH DIFFERENTIAL_PRIVACY
  OPTIONS (epsilon=10, delta=.01, privacy_unit_column=members.id)
  item,
  COUNT(*, contribution_bounds_per_group=>(0, 100))
FROM (SELECT * FROM students) AS members;
```

## 從差異隱私權查詢中移除雜訊

如需「查詢語法」參考資料，請參閱「[移除噪音](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#eliminate_noise)」。

## 為差異隱私查詢加入雜訊

如需「查詢語法」參考資料，請參閱「[新增雜訊](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#add_noise)」。

## 限制隱私權單元 ID 可存在的群組

請參閱「查詢語法」參考資料中的「[限制隱私權單元 ID 可存在的群組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#limit_groups_for_privacy_unit)」。

## 限制

本節說明差異化隱私的限制。

### 差異化隱私對成效的影響

差異隱私權查詢的執行速度比標準查詢慢，因為系統會執行實體層級的匯總作業，並套用 `max_groups_contributed` 限制。限制貢獻範圍有助於提升差異隱私權查詢的效能。

下列查詢的效能設定檔並不相似：

```
SELECT
  WITH DIFFERENTIAL_PRIVACY OPTIONS(epsilon=1, delta=1e-10, privacy_unit_column=id)
  column_a, COUNT(column_b)
FROM table_a
GROUP BY column_a;
```

```
SELECT column_a, COUNT(column_b)
FROM table_a
GROUP BY column_a;
```

造成效能差異的原因是，差異隱私查詢會執行額外的細微粒度分組層級，因為也必須執行實體層級的匯總。

下列查詢的效能設定檔應類似，但差異化隱私查詢的速度會稍慢：

```
SELECT
  WITH DIFFERENTIAL_PRIVACY OPTIONS(epsilon=1, delta=1e-10, privacy_unit_column=id)
  column_a, COUNT(column_b)
FROM table_a
GROUP BY column_a;
```

```
SELECT column_a, id, COUNT(column_b)
FROM table_a
GROUP BY column_a, id;
```

差異化隱私查詢的執行速度較慢，因為隱私權單元資料欄有大量不重複值。

### 小型資料集的隱含邊界限制

使用大型資料集計算隱含邊界時，效果最佳。
如果資料集包含的[隱私權單位](#dp_define_privacy_unit_id)數量較少，隱含界線可能會失敗，且不會傳回任何結果。此外，如果資料集隱私權單位數量較少，隱含的界限可能會限制大部分非離群值，導致匯總資料低報，且結果受限縮影響的程度大於新增雜訊。如果資料集的隱私權單位數量偏低或分割稀疏，應使用明確而非隱含的箝制。

### 隱私權漏洞

如果分析師心懷不軌，任何差異化隱私演算法 (包括這個演算法) 都可能導致私密資料外洩，尤其是在計算總和等基本統計資料時，更會因為算術限制而有這種風險。

#### 隱私權保障的限制

雖然 BigQuery 差異化隱私會套用[差異化隱私演算法](https://arxiv.org/abs/1909.01917)，但不會保證產生的資料集具有隱私權屬性。

#### 執行階段錯誤

如果分析師心懷不軌，且有權編寫查詢或控管輸入資料，可能會在私人資料上觸發執行階段錯誤。

#### 浮點噪音

使用差異化隱私前，請先考慮與四捨五入、重複四捨五入和重新排序攻擊相關的安全性漏洞。如果攻擊者可以控制資料集的部分內容，或資料集內容的順序，這些安全漏洞就特別令人擔憂。

浮點資料類型差異化隱私雜訊的加入作業，會受到「[Widespread Underestimation of Sensitivity in Differentially Private Libraries and How to Fix It](https://arxiv.org/abs/2207.10635)」一文所述的安全性弱點影響。整數資料類型加入的雜訊不會受到論文中描述的安全性漏洞影響。

#### 時序攻擊風險

惡意分析師可能會執行足夠複雜的查詢，根據查詢的執行時間推斷輸入資料。

#### 分類錯誤

建立差異化隱私查詢時，系統會假設您的資料結構明確且易於理解。如果您對錯誤的 ID 套用差異化隱私權，例如代表交易 ID 而非個人 ID 的 ID，可能會洩漏私密資料。

如需瞭解資料的相關協助，建議使用下列服務和工具：

* [BigQuery 資料剖析器](https://docs.cloud.google.com/dlp/docs/data-profiles?hl=zh-tw)
* [重新識別化風險分析](https://docs.cloud.google.com/dlp/docs/concepts-risk-analysis?hl=zh-tw)

## 定價

使用差異化隱私功能不會產生額外費用，但分析作業仍適用標準 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]