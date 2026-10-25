Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控健康狀態和資源使用率

BigQuery 管理員可以透過作業健康狀態和資源使用率圖表，監控組織的健康狀態、運算單元使用情形和工作效能。BigQuery 提供可設定的圖表，協助您執行下列操作：

* **[監控 BigQuery 的作業健康狀態](#monitor-operational-health)。**BigQuery 即時作業健康狀態監控功能是集中式監控系統，可讓您在多個位置觀察整個組織的 BigQuery 使用情形。
* **[查看 BigQuery 資源使用率](#view-resource-utilization)。**
  使用歷來資料執行根本原因分析、規劃容量，以及診斷效能變化。

如要監控個別查詢工作並排解相關問題，或依擁有者、專案或預留項目匯總工作，請參閱「[監控工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)」。

## 事前準備

* 如要查看運作健康狀態，您必須使用可透過[管理專案](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw#considerations)存取的[預留項目](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw#manage_reservations)。查看資源使用率圖表時，不一定要啟用這項功能。

### 必要的角色

如要取得查看作業健康狀態和資源使用率圖表中所有資料所需的權限，請要求管理員在組織中授予您下列 IAM 角色：

* [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
* [BigQuery 中繼資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer)  (`roles/bigquery.metadataViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備必要權限，可查看作業健康狀態和資源使用率圖表中的所有資料。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能查看作業健康狀態和資源使用率圖表中的所有資料：

* 如要查看組織作業健康狀態和資源使用率圖表中的所有資料，請按照下列步驟操作：
  + `bigquery.jobs.listExecutionMetadata or bigquery.jobs.listAll`
    組織
  + 用於建立預留項目的管理專案`bigquery.reservationAssignments.list`
  + 用於建立預留項目的管理專案`bigquery.capacityCommitments.list`
* 如要以隨選使用者的身分，查看組織資源使用率圖表中的所有資料，請在組織上執行下列操作：
  `bigquery.jobs.listExecutionMetadata or bigquery.jobs.listAll`
* 如要查看 BigQuery 資料表儲存空間的作業健康狀態摘要資料：
  `bigquery.tables.get or bigquery.tables.list`
  在組織層級
* 如要在預留項目層級查看作業健康狀態和資源使用率圖表，請按照下列步驟操作：
  + 用於建立預留項目的管理專案`bigquery.reservations.list`
  + 用於建立預留項目的管理專案`bigquery.reservationAssignments.list`
* 如要查看專案層級的資源使用率圖表：
  `bigquery.jobs.listAll`
  專案

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：** 您必須定義 Google Cloud 組織，才能在作業健康狀態和資源使用率圖表中查看所有資料。

## 監控整個組織的作業健康狀態

作業健康狀態資訊主頁會顯示貴組織的重要指標，以及貴組織在所有預留位置的預留項目。您可以使用這個資訊主頁監控下列指標：

* 運算單元用量
* 重組量
* 並行工作數量
* 錯誤
* 工作時間長度
* 處理的位元組數
* 總儲存空間

**注意：** 作業健康狀態資訊主頁不會監控隨選工作負載的指標。其他圖表 (例如資源使用率圖表) 則會同時顯示隨選和依容量計費的工作負載。

### 查看作業健康狀態圖表

如要查看組織的營運健康狀態資訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 BigQuery「Monitoring」(監控) 頁面。

   [前往「Monitoring」](https://console.cloud.google.com/bigquery/admin/monitoring?hl=zh-tw)
2. 選取您用來購買運算單元及建立預留項目的管理專案。
3. 在「Monitoring」頁面中，前往「Operational health」(運作健康狀態) 分頁，查看貴組織所有位置和預留項目的重要指標摘要。
4. 選用：如要查看即時指標 (每五分鐘根據最新資料執行查詢)，請按一下「Live data」(即時資料) 切換鈕。根據預設，這項設定為關閉狀態，資料的最長過時時間約為一小時。
5. 如要篩選指標，請設定下列欄位：

   * 在「Select location」(選取位置) 清單中，選取要監控的區域。
   * 在「Select reservation」(選取預留項目) 清單中，選取預留項目。
   * 在「Select project」(選取專案) 清單中，選取專案。
   * 在「Time range」(日期範圍) 清單中選取日期範圍。
6. 選用：如要透過[資源使用率圖表](#view-admin-resource-charts)或[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)查看作業健康狀態的詳細資料，請按一下「探索更多內容」。

BigQuery 會查詢下列[`INFORMATION_SCHEMA`檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)，收集指標：

* [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)
* [`INFORMATION_SCHEMA.RESERVATIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)
* [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)

如需複製管理資源圖表中運算單元用量時間線圖的查詢範例，請參閱「[比對管理資源圖表中的運算單元用量行為](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw#charts_example)」。

### 瀏覽次數

「Operational health」(運作健康狀態) 分頁會顯示下列摘要和詳細資料檢視畫面。

#### 摘要檢視

摘要檢視畫面會顯示貴組織子系統在過去 30 分鐘內的健康狀態，包括預留項目和區域。

如要查看摘要檢視畫面，請按照下列步驟操作：

* 在「Operational health」(運作健康狀態) 分頁的「Select location」(選取位置) 清單中，選取「All locations」(所有位置)。

#### 詳細檢視

詳細檢視畫面會顯示位置或預留項目層級的不同指標詳細時間線圖。

如要查看詳細資料檢視畫面，請按照下列步驟操作：

* 在「Operational health」(運作健康狀態) 分頁的「Select location」(選取位置) 清單中，選取區域或版本。

您可以使用下列選用篩選器，調整詳細檢視畫面中顯示的資料：

* 在「Select reservation」(選取預留項目) 清單中，選取預留項目名稱。
* 在「Select project」(選取專案) 清單中，選取專案。

### 圖表

BigQuery 提供下列資料表和圖表選項，可讓您詳細探索作業健康指標。

#### 摘要表格

摘要表格會顯示下列指標：

* **運算單元用量：**運算單元平均使用率。運算單元總容量等於基準容量和自動調度資源的最大容量。
* **重組量。**所有預留項目平均重組用量比率的最大值。
* **並行。**同時執行的工作數量上限。
* **已處理的位元組數。**已完成工作處理的總位元組數。
* **工作時間長度。**已完成工作的平均執行時間，從建立工作開始計算，直到工作結束為止。
* **總儲存空間。**上次更新時的使用中邏輯位元組總數。

檢視畫面中會顯示兩個摘要表格：「Location summary」(位置摘要) 和「Reservation summary」(預留項目摘要)。表格中的每一列代表一個位置或一個預留項目的用量。

表格會顯示上次更新前 30 分鐘的指標。如果啟用「即時資料」，查詢的資料每五分鐘就會重新整理一次。如果停用「Live data」(即時資料)，資料最多一小時更新一次。

如果指標大於預先定義的門檻，且重複工作的效能深入分析數量增加，表格儲存格會以顏色標示：

* 如果上次更新前 30 分鐘的指標值大於上週當天用量的 P99 值，表格儲存格會標示深藍色背景。
* 如果 30 分鐘內的指標值介於上週當天用量的 P95 至 P99 值之間，表格儲存格會標示為淺藍色背景。

所有門檻皆為預先定義，無法自訂。如要查看門檻，請按一下「info」
。

**注意：** 「儲存空間總量」欄不支援顏色註解。

#### 篩選資料

您可以根據下列值篩選圖表中的資料：

* **位置：**系統會顯示組織在過去 30 天內有活動的區域。[摘要檢視畫面](#summary-view)會顯示表格，匯總所有有效區域的用量。
* **預訂**。這個欄位僅適用於[詳細資料檢視畫面](#detailed-view)。管理專案擁有的所有預留項目皆可使用。只能選擇一個預留項目。
* **專案。**這個欄位僅適用於[詳細資料檢視畫面](#detailed-view)。組織中所有有流量的專案都可使用。只能選取一項專案。
* **日期範圍。**這個欄位僅適用於[詳細資料檢視畫面](#detailed-view)。這項設定會影響詳細資料檢視畫面中的[指標時間軸圖表](#metric-timeline-charts)和[錯誤圓環圖](#error-donut-chart)。**指標時間線圖**中的資料比例會根據所選日期範圍自動調整。

#### 「進行中的熱門查詢」圖表

這張圖表顯示前十項含有有效資源的工作，並依遞減順序排序。在下拉式選單中，您可以根據運算單元用量或工作時間長度選取排序選項。工作 ID 和相關資源用量數字會顯示在長條圖中。選取 **探索更多內容** 或熱門執行中查詢圖表中的工作 ID，即可在[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)中查看更多詳細資料。如要進一步瞭解執行詳細資料，以及診斷 BigQuery 工作的效能問題，請參閱「[取得查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)」。

#### 錯誤圓環圖

這張圖表顯示在所選時間範圍內，主要失敗原因的比例。[摘要檢視畫面](#summary-view)預設涵蓋過去 30 分鐘的資料。在詳細檢視畫面中，日期範圍選取器會控制涵蓋範圍。您可以依類型、擁有者專案或預留項目將錯誤分組。圓環圖會顯示失敗的工作數量。

#### 指標時間線圖

圖表會顯示支援指標的總覽，最多可顯示 30 天。預設時間範圍為一小時。隨著所選時間範圍變更，圖表中每個資料點的精細程度會自動調整。

這些圖表會顯示區域或預留項目的匯總值。不支援顯示多個區域或多個預留項目的資料。

指標時間線圖支援下列指標：

* **運算單元用量：**所選時間範圍內的平均運算單元用量。分別顯示所有工作和失敗工作的整體運算單元用量。
* **並行工作數量。**在所選時間範圍內，同時執行的工作數量上限。這個圖表會以堆疊長條圖的形式，分別顯示執行中和待處理工作的數量。
* **掃描的位元組數。**在所選時間範圍內，已完成工作處理的位元組總數。
* **隨機播放。**所選時間範圍內，所有預留項目平均重組用量比率的最大值。
* **工作時間長度。**在所選時間範圍內完成的工作平均執行時間，從工作建立時間計算到工作結束時間。
* **依類型區分的錯誤。**「Error donut chart」(錯誤圓環圖) 顯示所選時間範圍內，不同失敗原因的比例。

除了指標趨勢外，圖表也會顯示上週同一天用量的 P95 和 P99 指標值參考線。「Job concurrency」(工作並行) 圖表會顯示待處理和執行中工作的總和門檻。這些參考值會做為[摘要表](#summary-view)中的顏色編碼門檻。

如要進一步瞭解圖表，請按一下「探索更多內容」。系統會將您重新導向至**「Resource utilization」(資源使用率)** 分頁。

#### 深入分析表格

這個表格匯總了所選時間範圍內，執行工作時收集到的配額錯誤、存取遭拒錯誤和效能深入分析。深入分析資料會在預留項目層級匯總。每列都會提供洞察類型、位置、預留項目、洞察詳細資料和範例工作 ID 的相關資訊。按一下工作 ID，即可在[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)中查看更多工作詳細資料。在[摘要檢視畫面](#summary-view)中，預設觀察時間範圍涵蓋過去 30 分鐘。在詳細檢視畫面中，時間範圍選取器可控制顯示觀測資料的特定時間範圍。

### 監控單一專案的作業健康狀態

如果您無法存取整個組織，或專案沒有任何預留項目，系統預設會顯示專案作業健康狀態資訊主頁。這個檢視畫面可協助專案分析師監控專案的系統健康狀態，與組織層級的作業健康狀態資訊主頁類似，但圖表和篩選器只會顯示專案層級的資料。

**注意：** 如果專案指派給其他專案擁有的預留項目，運算單元數量總覽圖表會顯示 0 運算單元。如要查看運算單元總數，請查看預留項目所屬專案的圖表。

## 查看 BigQuery 資源使用率

BigQuery 資源圖表可協助您追蹤過去的資源用量，以便規劃未來需求及排解效能問題。

圖表會查詢下列 `INFORMATION_SCHEMA` 檢視表，收集指標：

* [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)
* [`INFORMATION_SCHEMA.RESERVATION_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-changes?hl=zh-tw)

資料會即時更新，最多可回溯 30 天。

如需複製管理資源圖表中運算單元用量時間線圖的查詢範例，請參閱「[比對管理資源圖表中的運算單元用量行為](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw#charts_example)」。

查看資源使用率時，您可以設定下列項目：

* 事件時間線圖會顯示最多 30 天的資料總覽。預設值為 6 小時。
* 主要圖表會顯示組織或管理專案在一段時間內的所選指標，例如運算單元用量或已處理的位元組數。圖表圖例會提供所顯示資料的詳細資訊。
* 在「Chart configuration」(圖表設定) 窗格中，您可以選取預先定義的指標檢視畫面，或自訂檢視畫面的指標。

資源使用率圖表包含下列元素：

* 在資源使用率分頁中，將指標懸停在圖表頂端的狀態方塊上，即可顯示指標的詳細資訊。
* 狀態方塊也會顯示下列資訊：

  + 如果指標仍在載入中，則會顯示載入圖示。
  + 如果指標使用過時資料，系統會顯示時鐘圖示。
  + 如果指標因不支援的網頁層級篩選器而無法載入，指標會顯示為刪除線。
  + 如果指標無法載入，狀態方塊會醒目顯示。

### 查看及設定資源使用率圖表

如要查看及設定資源使用率圖表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 BigQuery「Monitoring」(監控) 頁面。

   [前往「Monitoring」](https://console.cloud.google.com/bigquery/admin/monitoring?hl=zh-tw)
2. 選取專案。管理員監控預留資源用量時，應選擇用於購買運算單元和建立預留項目的管理專案。資料分析師監控工作資源用量時，應選擇對應的專案。
3. 在「Monitoring」(監控) 頁面中，前往「Resource utilization」(資源使用率) 分頁，查看資源用量摘要 (依位置細分)。
4. 選擇這個檢視畫面中指標的時間範圍，例如「1 天」。如要查看即時指標 (查詢會根據最新資料執行)，請按一下「Live data」(即時資料) 切換鈕。為提升效能，這項設定預設為關閉，資料最多一小時更新一次。
5. 在「Chart configuration」(圖表設定) 窗格中，設定下列欄位：

   * 在「[**Metric view**](#metric-view)」 (指標檢視畫面) 欄位中，選取其中一個檢視畫面。
   * 在「[**指標**](#chart-options)」欄位中，選取要查看的指標。您可以新增或編輯指標。
   * 在「[**Group by**](#group-by)」(分組依據) 欄位中，選取資料分組方式。
   * 在[「Filters」(篩選器)](#filter-search) 欄位中，選取資料篩選方式。
6. 如要儲存對圖表設定所做的變更，請按一下「Apply」(套用)。

#### 指標檢視畫面

BigQuery 提供預先設定的資源使用率指標檢視畫面。以下各節將說明您可以在這些檢視畫面中設定的指標。

##### 預留項目運算單元用量

這個檢視畫面會顯示管理專案中預留項目的運算單元用量細目指標。每項指標都有下列預設設定，您可以在「Chart configuration」(圖表設定) 窗格中點選指標名稱來編輯這些設定：

* 預設用量資料來自預留資源。
* 預設範圍是專案。
* 預設匯總方式是依所選時間範圍內的平均用量。

| 指標名稱 | 說明 |
| --- | --- |
| **預留項目 - 運算單元用量** | 監控所選時間範圍內的運算單元總用量。 |
| **預留項目 - 閒置運算單元用量** | 監控指定時間範圍內，運算單元用量超出預留項目資源量的情況。這項指標可讓您監控從其他預留項目和承諾使用合約借用的閒置運算單元，或用量資料中的捨入不精確情形。後者可能會導致這項指標的值不為零，即使已停用閒置運算單元共用功能也一樣。  最近 5 分鐘的用量資料可能延遲或不完整。 |
| **預留項目 - 基準運算單元用量** | 監控預留項目基準使用的運算單元。 |
| **預留項目 - 自動調度資源運算單元用量** | 監控預留項目自動調度資源運算單元的使用量。最近 5 分鐘的用量資料可能延遲或不完整。 |

##### 版本使用率總覽

這個檢視畫面會顯示管理專案中，版本資源的運算單元用量和容量指標。每項指標都有下列預設設定，您可以在「Chart configuration」(圖表設定) 窗格中按一下指標名稱來編輯這些設定：

* 預設用量資料來自預留資源，容量資料則來自版本資源。
* 預設範圍是專案。

| 指標名稱 | 說明 |
| --- | --- |
| **預留項目 - 運算單元用量** | 監控所選時間範圍內的運算單元用量。預設匯總方式是依所選時間範圍內的第 99 百分位數運算單元用量。 |
| **預留項目 - 閒置運算單元用量** | 監控指定時間範圍內，運算單元用量超出預留項目資源量的情況。這項指標可讓您監控從其他預留項目和承諾使用合約借用的閒置運算單元，或用量資料中的捨入不精確情形。即使停用閒置運算單元共用功能，後者仍可能導致這項指標的值不為零。  閒置運算單元用量為約略值，計算依據為**運算單元用量**、**承諾使用運算單元**和**自動調度運算單元**。如果運算單元用量值超過「承諾使用量」和「自動調度運算單元」，圖表會將剩餘部分歸類為閒置運算單元。  預設匯總方式是依據所選時間範圍內的 p99 資源用量。 |
| **版本 - 基準容量** | 監控這項管理專案中預留項目的基準大小。 |
| **版本 - 容量上限** | 監控所選時間範圍內可用的運算單元數量上限。這項指標是承諾使用合約容量、基準容量和自動調度資源容量的總和。預設匯總方式是依據所選時間範圍內的最大資源用量。 |
| **版本 - 已指派容量** | 監控在所選時間範圍內，實際指派給版本資源的運算單元數量。預設匯總方式是依據所選時間範圍內的最大資源用量。 |

##### 目前專案總覽

這個檢視畫面會顯示執行查詢的專案中，工作資源的指標。每項指標都有下列預設設定，您可以在「Chart configuration」(圖表設定) 窗格中按一下指標名稱來編輯這些設定：

* 預設資源為工作資源。
* 預設範圍是專案。

| 指標名稱 | 說明 |
| --- | --- |
| **工作 - 專案 - 運算單元用量** | 監控所選時間範圍內的運算單元用量。預設匯總方式是依據所選時間範圍內的最大資源用量。 |
| **工作 - 專案 - 已處理的位元組數** | 監控在所選時間範圍內，已完成工作處理的總位元組數。預設匯總方式是依所選時間範圍內處理的位元組總數。 |
| **工作 - 專案 - 並行工作數量** | 監控所選時間範圍內同時執行的工作數量。預設匯總方式是依據所選時間範圍內的最大資源用量。 |
| **工作 - 專案 - 工作時長** | 監控所選時間範圍內已完成工作的執行時間。執行階段會測量從建立工作到完成工作的時間。預設匯總方式是依所選時間範圍內的平均執行階段。 |

##### 所擁有預留項目總覽

這個檢視畫面會顯示管理專案中，預留資源的工作活動指標。每項指標都有下列預設設定，您可以在「Chart configuration」(圖表設定) 窗格中按一下指標名稱，編輯這些設定：

* 預設資源是預留資源。
* 預設範圍是專案。

| 指標名稱 | 說明 |
| --- | --- |
| **預留項目 - 運算單元用量** | 監控所選時間範圍內的運算單元用量。預設匯總方式是依據所選時間範圍內的最大資源用量。 |
| **預留項目 - 已處理的位元組數** | 監控在所選時間範圍內，已完成工作處理的總位元組數。預設匯總方式是依所選時間範圍內處理的位元組總數。 |
| **預留項目 - 並行工作數** | 監控所選時間範圍內同時執行的工作數量。預設匯總方式是依據所選時間範圍內的最大資源用量。 |
| **預留項目 - 工作持續時間** | 監控所選時間範圍內已完成工作的執行階段。 執行階段會測量從建立工作到完成工作的時間。包括排入佇列和重試。預設匯總方式是依所選時間範圍內的平均執行階段。 |
| **預留項目 - 重組用量** | 監控所選時間範圍內的重組用量比率。預設匯總方式是依所選時間範圍內的平均用量。 |

**注意：** BigQuery 可能會分配額外的運算單元來執行工作，導致運算單元用量值超過總容量上限值，且在忽略閒置運算單元的預留項目中，借用運算單元用量值不為零。在這些情況下，超出最大容量的用量不會產生額外費用。

##### 自訂檢視模式

如要建立自訂指標檢視畫面，您可以從頭開始新增指標，也可以從預先定義的指標檢視畫面 (例如「Reservation overview」(預留總覽) 指標檢視畫面) 開始，然後自訂其中的指標。

您可以儲存自訂檢視畫面，供日後使用。儲存的檢視畫面會保留指標、分組依據和篩選器設定，但使用者電子郵件篩選器除外。已儲存的資料檢視會儲存在使用者層級。您可以建立、更新、重新命名及刪除已儲存的檢視畫面。

#### 指標

設定圖表時，您可以新增、編輯或刪除圖表監控的資源使用率指標。

如要設定資源使用率圖表指標，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，[查看 BigQuery 資源使用率圖表](#view-admin-resource-charts)。
2. 在「Chart configuration」(圖表設定) 窗格中，設定「Metrics」(指標) 欄位：

   1. 依序點選**「新增項目」>「選取指標」**。
   2. 在「選取指標」對話方塊中，選擇下列項目：

      1. 要監控的資源類型：**工作**、**預留項目**或**版本**。
      2. 要監控的範圍。舉例來說，如要監控目前專案中的工作指標，請選取「Project」(專案) 範圍。
      3. 選擇要監控的指標。例如，如要監控工作運算單元用量，請選擇「Slot usage」(運算單元用量)。
   3. 按一下「套用」。
   4. 在「New item」(新增項目) 對話方塊中，選擇匯總。舉例來說，如要監控所選時間範圍內，超出預留項目容量的運算單元用量上限，請選擇「Max」(最大值)。
   5. 按一下「完成」，儲存指標。
3. 選用：如要變更現有指標，請按一下指標名稱，然後編輯設定或刪除指標。

##### 支援的指標資源類型和範圍

資源使用率指標會依資源類型和範圍分類。

**資源類型**

您可以監控下列資源類型：

| 資源 | 說明 |
| --- | --- |
| 工作 | 指定範圍和時間範圍內 BigQuery 工作詳細資料的指標。 |
| 預留項目 | 特定範圍和時間範圍內的 BigQuery 預留項目用量指標。這些指標會依預留項目匯總工作詳細資料。 如果您只有預留項目層級的部分資料存取權，則可查看匯總的預留項目用量指標，但無法存取工作層級的詳細資料。 |
| 版本 | 特定範圍和時間範圍內的 BigQuery 版本容量指標。 |

**範圍類型**

選取指標的資源後，請選取範圍。

* 預留項目和版本資源預設為專案層級範圍。
* 工作資源可以設為專案、資料夾或組織層級範圍。如要擴大範圍，則需要額外權限。

#### 分組依據

如要將資源使用率圖表中的資料分組，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，[查看 BigQuery 資源使用率圖表](#view-admin-resource-charts)。
2. 在「Chart configuration」(圖表設定) 窗格中，選取下列其中一個選項，設定「Group by」(分組依據) 欄位：

   * **無**：這個選項可讓您概略瞭解整個組織在一段時間內所選指標的變化。
   * **專案**：這個選項會依專案分組所選指標。如果可用專案超過 50 個，系統只會顯示運算單元用量最高的前 50 個專案。
   * **所有其他分組依據選項**：這些選項與專案檢視畫面類似，資料會依據各自的維度分組。如果某個分組依據選項不支援所有選取的指標，就無法選取該選項。

#### 篩選器

設定資源使用率圖表時，您可以對資料套用篩選器，例如顯示 Enterprise 版資源的使用情形，或依資源 ID 篩選。

如要篩選圖表資料，請在篩選器窗格中套用篩選器。只有在所選指標支援篩選條件時，才能選取篩選條件。如要查看必要權限，請按一下「Filter」(篩選器) 選單。

### 查看專案層級的資源使用率資料

您可以按照查看組織層級資料的[設定步驟](#view-admin-resource-charts)，分析專案層級的資源使用率。圖表只會顯示專案層級的資料和設定選項 (組織層級選項會顯示為灰色)。這項專案層級範圍會顯示整體資源使用率，不論情境專案中的計費模式為何。

### 資源使用率圖表限制

* 頁面中間的圖表和表格會顯示與所選時間範圍和精細程度相關的指標。
* 單位相同的指標會共用相同的刻度。圖表最多支援兩種不同的刻度。

### 切換至舊版使用者介面

根據預設，從預留管理專案前往時，您可以存取版本資源圖表。您可以在預留項目管理專案 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)) 中，切換隨選資源圖表和版本資源圖表。

如要查看資源圖表，請按照下列步驟操作：

1. 前往「BigQuery」頁面  
   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在專案選單中，選取您用來購買運算單元及建立預留項目的管理專案。
3. 按一下導覽選單中的「Monitoring」。
4. 在**「Chart options」 > 「Scope」**部分，您可以從清單中選取計費模式，包括三種版本和隨選。根據預設，計費模式會設為 Enterprise 版。
5. 在**「Chart options」(圖表選項)>「Chart Configurations」(圖表設定)** 部分，執行下列操作：
   1. 從「圖表」清單中選取圖表類型。如要瞭解不同的圖表選項，請參閱「[圖表選項](#chart-options)」。
   2. 從「Metrics」(指標) 清單中，選取可用的指標類型。
   3. 從「Group by」(分組依據) 清單中，選取要用來將圖表資料分組的維度。如要瞭解不同維度，請參閱「[分組依據選項](#group-by)」。
   4. 從「篩選器」清單中選取可用的篩選器選項。如要瞭解不同的篩選器，請參閱「[篩選器和搜尋](#filter-search)」。
   5. 設定要在圖表中查看資料的時間範圍。

#### 圖表設定

您可以變更下列圖表設定選項，調整資源圖表的檢視畫面。

##### 圖表選項

BigQuery 提供下列指標類型，可在圖表中顯示：

* **運算單元用量**：平均運算單元用量。如果「Group by」(分組依據) 選項設為「Overall」(整體)，或「Filters」(篩選器) 設為「None」(無) 或單一預留項目，系統也會顯示容量和借用運算單元用量指標。
  + **總用量。**所選時間範圍內的平均運算單元用量。
  + **借用的運算單元用量。**平均用量超過預留項目的資源量。常見原因如下：向其他預留項目和承諾使用合約借用[閒置的運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)，或是用量資料捨入不精確。即使停用閒置運算單元共用功能，資源使用率圖表仍會顯示額外的閒置運算單元。閒置運算單元用量為約略值，是根據**運算單元用量**、**承諾使用運算單元**和**自動調度運算單元**計算得出。如果運算單元用量值超過「承諾使用量」，圖表會將這些運算單元歸類為閒置運算單元。
  + **承諾使用數量。**版本承諾使用規模。
  + **基準容量。**預留項目基準大小。
  + **自動調度資源容量。**自動調度資源的運算單元大小。
  + **容量上限。**使用者可存取的運算單元數量上限。

**注意：**BigQuery 有時會分配額外的運算單元來執行工作，因此「Total Usage」(總用量) 值會超過「Maximum capacity」(容量上限) 值，且在忽略閒置運算單元的預留項目中，「Borrowed Slot Usage」(借用運算單元用量) 的值不為零。在這種情況下，如果用量超過預留項目的「**Maximum Capacity**」(容量上限)，系統不會收取額外費用。

* **並行工作數。**在所選時間範圍內同時執行的工作數量上限。
* **工作效能：**已完成工作的平均執行時間，從建立工作開始計算，直到工作結束為止。
* **失敗的工作。**所選時間範圍內，失敗工作的平均運算單元用量。
* **已處理的位元組數。**在所選時間範圍內，已完成工作處理的總位元組數。
* **重組用量。**所選時間範圍內的平均重組用量比率 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。

##### 表格元件

表格會顯示與您在資源圖表中選取的時間範圍和維度相關的指標。

「Slot Usage」(運算單元用量) 圖表會顯示所選時間範圍內，所有執行中工作的「Average slot usage」(平均運算單元用量)。未在所選時間範圍內完成的工作，只會計入該時間範圍內使用的運算單元。

在「Job Performance」(工作效能) 圖表中，表格元件會顯示下列指標：

* **工作數量：**在所選時間範圍內，已完成的工作數量 (包括部分完成)。
* **平均工作時間長度。**在所選時間範圍內，至少部分執行的已完成工作平均持續時間。
* **工作時間長度中位數。**在所選時間範圍內，至少部分執行的已完成工作持續時間中位數。
* **最短工作時間長度。**在所選時間範圍內，至少部分執行的已完成工作最短持續時間。這個資料欄預設為隱藏，但您可以在「**資料欄顯示選項**」中啟用。
* **最長工作時間長度。**在所選時間範圍內，至少部分執行的已完成工作，其持續時間上限。這個資料欄預設為隱藏，但您可以在「Column display options」(資料欄顯示選項) 中啟用。

在「Failed Jobs」(失敗的工作) 圖表中，表格元件會顯示下列資料：

* **平均運算單元用量。**與「Slot Usage」(運算單元用量) 圖表相同，但僅限失敗的工作。
* **失敗的工作總數。**在所選時間範圍內失敗的工作數量。

**注意：**除了資源圖表，您也可以自行編寫查詢或建立資訊主頁。如需查詢範例和數據分析範本，請參閱「[`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw#information-schema)」。

##### 分組依據選項

視圖表類型而定，您可以在圖表檢視畫面中，依據多個維度將資料分組：

* **整體：**「整體」檢視畫面會概略呈現整個機構在一段時間內的所選指標。至於運算單元用量，容量和用量會顯示在同一張圖表，方便您瞭解一段時間內的整體運算單元使用率。
* **專案。**專案檢視畫面會顯示依專案分組的所選指標。如果組織有超過 10 項專案，則只會顯示在所選時間範圍內，運算單元用量、工作並行、工作時間長度或失敗工作最高的前 10 項專案。至於運算單元用量，所有其他專案都會歸入圖表底部的「Other」(其他) 類別，方便您與整體容量進行比較。
* 所有其他分組依據檢視畫面都與專案檢視畫面類似，資料會依據各自的維度分組。

##### 時間範圍選項

您可以透過下列方式修改時間範圍：

* 選取時間範圍，並拖曳至事件時間線圖。
* 選取時間範圍並拖曳至主圖表。

校正週期會隨著所選時間範圍的變更而自動更新。對齊週期越短，檢視畫面越詳細。如要更清楚地查看經常變更的資源 (例如「Slot Usage」(運算單元用量) 選項)，請縮短對齊週期。

**注意：**如要在運算單元用量圖表上顯示更精細的調整週期，系統可能會因資料取樣和調整，而短暫顯示超過容量的用量。

##### 篩選及搜尋

如要縮小圖表資料範圍，請在篩選器面板中套用篩選器。部分篩選器僅適用於特定圖表。「Reservations」(預留項目)、「Folders」(資料夾)、「Projects」(專案) 和「Users」(使用者) 篩選器會填入在所選時間範圍內耗用運算單元的個別資源。舉例來說，如果專案在過去 30 天內未使用，就不會顯示在專案篩選器清單中。

套用篩選器後，圖表會重新整理，顯示所選參數範圍內的資料。

**注意：**如要依特定工作篩選，請在文字欄位中輸入工作 ID，不含專案前置字元。

## 監控自動調度資源

使用[管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)監控運算單元用量時，您可能會看到擴充的運算單元數量明顯多於運算單元用量，因為圖表會平滑調整對齊期間內使用的運算單元數量。如要查看更精確的自動調度資源運算單元用量詳細資料，請縮短時間範圍。這會自動將對齊週期更新為較小的增量。

在以下範例中，圖表顯示的擴充運算單元數量遠高於工作負載需求。

不過，如果將時間範圍選項縮短，使對齊週期為兩秒，就會看到自動配置器會根據工作負載需求調整資源配置，並顯示更準確的資料。拖曳時間範圍選項的開始和結束範圍，即可調整時間範圍選項。如要顯示最準確的工作負載需求資料，請從「Metric」(指標) 清單中選取「p99」。

如要最準確地查看自動調度資源用量，請將對齊週期設為 1 到 15 秒。

如要瞭解如何查看運算單元用量，請參閱「[查看管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#view-admin-resource-charts)」。

### 監控工作成效

您可能需要調整自動調度資源`max_slots`，以免費用增加。下列查詢會提供工作效能的背景資訊，方便您為工作負載選擇正確的自動調度資源運算單元數量。

下列查詢會提供預留項目過去工作效能的詳細資料：

```
SELECT
    AVG(TIMESTAMP_DIFF(end_time, creation_time, MILLISECOND)) as avg_latency_ms,
    SUM(total_bytes_processed) as total_bytes,
    COUNT(*) as query_numbers,
FROM
    `PROJECT_ID.region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
WHERE creation_time >= START_TIME
    AND creation_time < END_TIME
    AND (statement_type != "SCRIPT" OR statement_type IS NULL)
    AND reservation_id = RESERVATION_ID
```

更改下列內容：

* `PROJECT_ID`：專案 ID
* `REGION_NAME`：專案的區域
* `START_TIME`：要開始查看資料的建立時間
* `END_TIME`：要停止查看資料的建立時間
* `RESERVATION_ID`：預留項目 ID

以下範例會取得五天內的工作詳細資料：

```
SELECT
    AVG(TIMESTAMP_DIFF(end_time, creation_time, MILLISECOND)) as avg_latency_ms,
    SUM(total_bytes_processed) as total_bytes,
    COUNT(*) as query_numbers,
FROM
    `myproject.region-us`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
WHERE creation_time >= '2024-06-25 00:00:00-07'
    AND creation_time < '2024-06-30 00:00:00-07'
    AND (statement_type != "SCRIPT" OR statement_type IS NULL)
    AND reservation_id = reservationID
```

## 疑難排解運算單元爭用問題

如果運算單元不足，無法執行所有工作，就可能發生運算單元爭用情況，導致效能問題。如要分析效能降低的原因是工作負載增加，還是環境設定變更，您可以[比較預留項目和專案的兩個系統時間間隔](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#compare_two_system_intervals)。

如要排解運算單元爭用問題，請按照下列步驟和最佳做法操作。

如果嘗試過這些最佳做法後，仍遇到工作效能問題，可以[申請支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

### 並行工作數量激增

在管理資源圖表中使用[詳細檢視畫面](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#detailed-view)，檢查工作執行次數是否突然激增，且運算單元用量同時飆升。這類尖峰可能表示有太多工作在爭奪預留項目中的可用運算單元。

**最佳做法：**建議您最佳化資源密集型查詢，或增加預留項目的運算單元容量。如要進一步瞭解如何最佳化查詢效能，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」。

### 運算單元用量偏高

請使用[詳細檢視畫面](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#detailed-view)，檢查工作時間是否增加，尤其是工作超過預留項目容量上限時。運算單元用量持續偏高，可能代表運算單元持續爭用。

**最佳做法：**使用[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)的運算單元爭用篩選器檢查查詢，找出耗用最多運算單元的查詢並加以最佳化。

### 工作時間長度過長

如果工作完成時間明顯較長，請查看[詳細檢視畫面](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#detailed-view)。工作並行率高和運算單元用量激增，可能代表運算單元發生爭用。

**最佳做法：**暫時停止較不重要的工作，或降低整體工作提交率，藉此隔離重要工作。

### 運算單元爭用訊息

[洞察資料表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#insights-table)可能會顯示 `There were NUMBER jobs detected with
slot_contention in the reservation.` 等訊息，指出運算單元爭用問題。請查看[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)，瞭解這些訊息中標記的特定工作詳細資料。

**最佳做法：**最佳化已識別的查詢，或調整預留項目的運算單元分配。

**注意：** 如要進一步瞭解這些圖表顯示的實際使用率為何可能與配額用量不同，請參閱「[瞭解運算單元指標](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw#understand_slot_metrics)」。

## 後續步驟

* 瞭解[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。
* 瞭解如何[購買運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw)。
* 瞭解如何[預估運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)。
* 瞭解如何[查看運算單元建議和深入分析](https://docs.cloud.google.com/bigquery/docs/slot-recommender?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]