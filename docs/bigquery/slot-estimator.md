* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 估算運算單元容量需求

在 BigQuery 中購買預留運算單元時，您必須估算特定工作負載適用的運算單元數量。BigQuery 運算單元估算工具可協助您根據過往成效指標管理運算單元容量。

您可以針對版本、預留和隨選工作負載使用運算單元估算工具，執行下列工作：

針對所選[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)工作負載：

* 查看過去 30 天的運算單元容量和使用率資料，找出運算單元使用率最高的時間段。
* 查看承諾和自動調度配額的成本最佳化建議，這些配額的效能與目前配額相似。
* 查看特定版本的目前預訂設定。

特定預留項目工作負載：

* 查看過去 30 天的運算單元容量和使用率資料，找出運算單元使用率最高的時間段。
* 查看工作延遲百分位數 (P90、P95 等)，瞭解查詢效能。
* 模擬增加或減少預留運算單元上限對效能的影響。

隨選計費工作負載：

* 查看整個機構或個別專案過去 30 天的隨選運算單元用量資料。
* 如果改用 Enterprise 版，即可查看承諾用量和自動調度配額的成本最佳化建議，這些配額的效能與目前配額相似。

使用 Enterprise 版、Enterprise Plus 版或隨選計費的客戶，可以透過 BigQuery 運算單元建議工具查看運算單元用量、調整承諾用量，以及提升效能。詳情請參閱「[查看版本位置建議](https://docs.cloud.google.com/bigquery/docs/slot-recommender?hl=zh-tw)」。

## 限制

* 資料只包含過去 30 天的資料。
* 模型不包含[`ML_EXTERNAL`](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)作業。如果大部分時段都用於 `ML_EXTERNAL` 指派，模擬結果的準確度就會降低。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 所需權限

如要使用運算單元預估工具處理預留資料，您必須具備管理專案的下列 IAM 權限：

* `bigquery.reservations.list`
* `bigquery.reservationAssignments.list`
* `bigquery.capacityCommitments.list`

下列預先定義的 IAM 角色都包含使用時段預估工具所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.resourceAdmin`
* `roles/bigquery.resourceEditor`
* `roles/bigquery.resourceViewer`
* `roles/bigquery.user`

如要使用運算單元估算工具取得隨選用量資料，您需要在專案中[啟用 Reservations API](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#enabling-reservations-api)，並將該專案做為管理預留項目的管理專案。除了上述權限外，您還需要具備機構的下列其中一項 IAM 權限，才能查看機構層級資料；或具備專案的下列其中一項 IAM 權限，才能查看專案層級資料：

* `bigquery.jobs.listExecutionMetadata` (只能在機構層級套用)
* `bigquery.jobs.listAll` (可套用至機構或專案層級)

下列預先定義的 IAM 角色都包含使用時段預估工具所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.resourceAdmin`
* `roles/bigquery.resourceEditor`
* `roles/bigquery.resourceViewer`

如要查看承諾使用設定建議，您也需要[查看版本運算單元建議](https://docs.cloud.google.com/bigquery/docs/slot-recommender?hl=zh-tw#required_permissions)一文所述的權限。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 查看運算單元數量和使用率

如要查看一段時間內的運算單元數量和使用率，請前往運算單元估算工具：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 選取管理專案。

   1. 按一下頁面頂端的「Select from」下拉式清單。
   2. 在隨即顯示的「Select from」視窗中，選取所需專案。
3. 在導覽選單中，按一下「容量管理」。
4. 按一下「運算單元估算工具」分頁標籤。

使用率圖表會顯示過去 30 天的運算單元容量和使用率，
以每小時為單位計算。

「使用量和使用率 (百分比)」分頁會顯示運算單元使用率，也就是運算單元用量占運算單元上限的百分比。

「依容量劃分的使用量和使用率」分頁會以絕對值顯示最大時段數和使用量。

你可以從「來源」下拉式選單中選擇版本或隨選視訊，查看不同範圍的統計資料。選取版本後，「預留項目」下拉式選單會填入相關預留項目。

如要使用隨選選項，如果具備機構層級權限，可以從「建議對象」下拉式選單中選擇個別專案或整個機構。如果您只有專案層級的權限，則「Slot 估算器」頁面只會顯示專案層級的資訊。

「依容量的使用量和使用率」分頁的統計資料可能會因範圍不同而略有差異：

* 如果是版本來源，則會顯示整個版本的可用運算單元上限、承諾運算單元、基準運算單元總和、平均運算單元用量、P99 運算單元用量和 P50 運算單元用量。
* 針對特定預留項目，系統會顯示預留運算單元上限、基準運算單元、平均運算單元用量、P99 運算單元用量和 P50 運算單元用量。
* 如果是隨選來源，則會顯示平均運算單元用量、P99 運算單元用量和 P50 運算單元用量。

## 模型運算單元成效

選取預留項目後，您可以使用運算單元估算工具查看工作效能資料，並模擬變更運算單元數量上限的效果。運算單元預估工具可模擬不同容量等級的成效變化，範圍從觀察期內運算單元大小下限的 80%，到目前運算單元上限的 150% 都有。換句話說，選項減少幅度不得超過 30 天內最低容量的 20%，選項增加幅度則不得超過目前容量的 50%。

模型會假設過去 30 天的使用模式重現，且除了時段變更外，其他一切維持不變。

預估成效提升幅度取決於多項因素，最重要的因素是模型中的時段數，以及尖峰時段與一般時段執行的每個百分位數區間工作比例。尖峰時段是指幾乎所有時段都已使用的期間。在這些時間執行的工作最容易受到運算單元爭用影響，因此額外運算單元帶來的效能提升幅度最大。因此，視工作執行時間而定，相同容量的增加可能會對不同工作區塊產生不同影響。

**注意：** 實際的工作效能變化可能會因之後的使用情形而異。
預期效能資訊僅供參考。

如要模擬廣告空間成效，請按照下列步驟操作：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 選取管理專案。

   1. 按一下頁面頂端的「Select from」下拉式清單。
   2. 在隨即顯示的「Select from」視窗中，選取所需專案。
3. 在導覽選單中，按一下「容量管理」。
4. 按一下「運算單元估算工具」分頁標籤。
5. 在「預訂」下拉式選單中，選取特定預訂項目。模型會顯示預留項目在任何特定時間可借用的閒置運算單元數量。
6. 在「提供額外運算單元的模式 (超過運算單元數量上限)」下拉式選單中，選取一或多個要模擬的運算單元值，然後按一下「確定」。

「增加額外運算單元後的工作成效變化」下方的表格會顯示過去 30 天的工作成效資料，以及增加或減少最大運算單元數後，預估的成效變化。資料會依據在指定時間範圍內執行的所有工作，按工作時間長度分組為百分比。燈泡圖示代表的資料欄，對應所選預訂的成效提升建議。

成效資料會按百分位數細分。表格最多會將資料分成 12 個區間：P10 到 P90，加上 P95、P99 和 P100。P100 範圍代表執行時間最長的前 1% 工作；P99 包含前 96% 至 99%；P95 包含前 91% 至 95%；P90 包含 81% 至 90%，依此類推。視資料而定，表格可能會將資料分組到較少的儲存區。在這種情況下，表格包含的資料列會比較少。

表格會針對每個百分位數區間顯示下列資訊：

* 工作持續時間百分位數：這一列的百分位數特徵分塊。
* 平均工作時間長度：該百分位數區間內的工作平均執行時間。
* 工作數：該百分位數值區中的工作數。
* 各個模型中，該百分位數工作的預估平均時間。

表格也會列出各個模型的「30 天變化」預估統計資料。這個值是預估的總時數變化，代表在不同運算單元容量下，處理過去 30 天內工作的時數變化。

## 瞭解運算單元用量對模型結果的影響

如果是固定容量保留項目，啟用閒置運算單元共用功能後，該保留項目中的工作就能借用其他保留項目的閒置運算單元。因此，使用率可能會超過分配的廣告空間 100%。如果預留項目持續使用其他預留項目的閒置運算單元，表示可能需要增加預留項目大小。這點很重要，因為如果閒置時段的可用性在未來降低，工作負載的效能可能會隨之下降。另一方面，如果預留項目很少使用完整運算資源量，則可能過大。

使用[自動調度](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)功能的預留項目會依據下列優先順序使用及新增運算單元：

1. 基準運算單元。
2. 閒置運算單元共用功能 (如果已啟用)。
3. 自動調度運算單元。

如果自動調度資源預留項目持續用盡自動調度資源運算單元，這可能表示應增加預留運算單元上限。如要瞭解如何查看配額使用量，請參閱「[查看管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#view-admin-resource-charts)」。

## 定價

您可以使用位置估算工具，不需要付費。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]