Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 總覽：將資料倉儲遷移至 BigQuery

本文將討論適用於任何資料倉儲技術的一般概念，並說明可用於規劃及建構 BigQuery 遷移作業的架構。

## 術語

討論資料倉儲遷移時，我們會使用下列術語：

用途
:   「用途」包含為實現商業價值所需的所有資料集、資料處理以及系統和使用者互動，例如追蹤某產品的長期銷售量。至於資料倉儲，用途則通常包含：

    * 可擷取各種來源 (例如客戶關係管理 (CRM) 資料庫) 原始資料的資料管道。
    * 儲存在資料倉儲中的資料。
    * 可控管、進一步處理及分析資料的指令碼和程序。
    * 可讀取或與資料互動的商務應用程式。

工作負載
:   相互連結且具備共用依附元件的一組用途。舉例來說，用途可能具備下列的關係和依附元件：

    * 採購報告可獨立呈現，有助於瞭解支出以及要求折扣。
    * 銷售報告也可獨立呈現，有利於規劃行銷廣告活動。
    * 不過損益報告需同時依據購買報告和銷售報告，因此適合用於判斷公司的產值。

商務應用程式
:   與使用者進行互動的系統，例如視覺化報告或資訊主頁。商務應用程式也可採用營運資料管道或意見回饋循環的形式。舉例來說，在計算或預測產品價格異動後，營運資料管道可能會在交易資料庫中更新新的產品價格。

上游程序
:   將資料載入資料倉儲的來源系統和資料管道。

下游程序
:   用於處理、查詢及視覺化呈現資料倉儲中資料的指令碼、程序和商務應用程式。

卸載遷移作業
:   此遷移策略的目的是協助新環境中的使用者，儘快執行設定用途，或善用新環境中可用的額外容量。如要卸除用途，請按照下列步驟操作：

    * 複製舊版資料倉儲中的結構定義和資料，然後進行同步處理。
    * 遷移下游指令碼、程序和商務應用程式。

    遷移卸載作業會增加複雜度和遷移資料管道涉及的工作。

完整遷移
:   這是與卸載遷移類似的遷移方法，只是不再採行「先複製再同步架構和資料」的途徑，而改為利用遷移設定，從上游來源系統直接將資料擷取至新的雲端資料倉儲中。換句話說，用途所需的資料管道也會跟著遷移。

企業資料倉儲 (EDW)
:   一種資料倉儲，包含分析資料庫以及多個重要分析元件和程序。包含滿足機構工作負載所需的資料管道、查詢和商務應用程式。

雲端資料倉儲 (CDW)
:   具備與 EDW 相同特色的資料倉儲，但是在雲端的全代管服務 (本例為 BigQuery) 上執行。

資料管道
:   使用一系列可執行各種資料轉換類型的函式和工作，連線至資料系統的程序。詳情請參閱資料管道說明文件中的「[什麼是資料管道？](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw#what-is-a-data-pipeline)」在這個系列中。

## 遷移至 BigQuery 的理由

過去幾十年來，各機構組織都已精通資料倉儲技術，而且有越來越多機構組織針對大量儲存資料應用描述性分析，以深入分析其核心業務營運。傳統商業情報 (BI) 專注於查詢、報告和[線上分析處理](https://wikipedia.org/wiki/Online_analytical_processing)，在過去可能是攸關公司成敗的因素，但現已不足以因應需求。

現今機構不只需要描述性分析瞭解過往事件，也需利用[預測性分析](https://wikipedia.org/wiki/Predictive_analytics)；其中經常使用機器學習 (ML) 擷取資料模式，針對未來提出概率陳述。最終目標是開發[描述性分析](https://wikipedia.org/wiki/Prescriptive_analytics)，結合過去的經驗教訓和未來預測，自動引導即時動作。

一般資料倉儲實務會從各種來源 (通常是[線上交易處理 (OLTP)](https://wikipedia.org/wiki/Online_transaction_processing) 系統) 擷取原始資料。之後會分批擷取資料子集，根據定義的結構定義進行轉換，然後載入至資料倉儲。由於資料倉儲會批次擷取資料子集，並根據嚴格的結構定義儲存資料，因此不適合用於處理即時分析或回應自發查詢。Google 就是為了因應固有限制而設計了 BigQuery。

實作及維持這些傳統資料倉儲的 IT 機構規模及複雜度，通常會減緩創新概念的效率。建立可擴充、可用性高且安全的資料倉儲架構，需要花費多年時間和大量的投資成本。BigQuery 提供精密的[軟體即服務 (SaaS)](https://wikipedia.org/wiki/Cloud_computing#Software_as_a_service_.28SaaS.29) 技術，可用於無伺服器資料倉儲作業。如此一來，將基礎架構維護及平台開發作業交給 Google Cloud處理之後，您就能夠全心投入推展核心業務。

BigQuery 可彈性調整且具備成本效益，可讓使用者存取結構化資料儲存空間、處理和數據分析功能。當資料量急遽增加時，這些特色至關重要，不僅可視需要調整儲存空間和處理資源，還能讓這些資料發揮效益。此外，針對剛著手大數據分析和機器學習，且想擺脫內部部署大數據系統潛在複雜性的機構，BigQuery 提供以量計價的試驗用代管服務。

只要使用 BigQuery 就能解答過往的棘手問題，應用機器學習探索新興資料模式，並測試全新假說。因此您可以獲得及時深入分析，瞭解業務績效，藉此修改程序以獲得更理想的成果。此外，由大數據分析取得的相關深入分析，通常也能讓使用者享有更豐富的體驗。

## 遷移的內容和方式：遷移作業架構

進行遷移作業可能是一項複雜且耗時的大工程，因此建議您遵循以下架構進行組織及規劃，遷移作業可分為以下階段：

1. **準備與探索**：準備遷移作業並探索所需的[工作負載](#workload)和[用途](#use-case)。
2. **規劃**：排定用途優先順序、定義成效衡量標準，然後規劃遷移作業。
3. **執行**：從評估到驗證，逐步完成遷移作業。

### 準備與探索

在初始階段中，重點為準備與探索，讓您自己和相關人員早一步探索現有的用途、提出最初的疑慮。最重要的是，針對預期的利益進行初步分析。其中包含效能提升 (例如改善的並行效能) 以及[總持有成本](https://wikipedia.org/wiki/Total_cost_of_ownership) (TCO) 降低。這個階段相當重要，可協助您確立遷移作業的價值。

資料倉儲通常支援各種用途，並涵蓋資料分析師到商業決策者等眾多相關人員。建議您邀請這些群組的代表加入，以充分瞭解現在有哪些用途、這些用途是否可順利執行，以及相關人員是否正在規劃新的用途。

探索階段的程序包含下列工作：

1. 查看 BigQuery 的價值主張，並與舊版資料倉儲的價值主張進行比較。
2. 執行初始 TCO 分析。
3. 確認哪些用途會受到遷移作業影響。
4. 模擬您要遷移的基礎資料集和資料管道的特性，以識別依附元件。

如要深入瞭解用途，您可以開發問卷，收集各領域專家 (SME)、使用者和利害關係人的資訊。問卷應收集的資訊如下：

* 用途的目標是什麼？商業價值為何？
* 非功能性的需求為何？例如資料更新間隔、並行用量等。
* 用途是否為大型工作負載的一部分？是否仰賴其他用途？
* 用途是以哪些資料集、資料表和結構定義做為基礎？
* 您對動態饋給這些資料集的資料管道有什麼瞭解？
* 目前使用哪些 BI 工具、報告和資訊主頁？
* 目前對於作業需求、效能、驗證和網路頻寬的技術需求為何？

下圖顯示遷移作業之前的高階舊版架構，並說明可用的資料來源、舊版資料管道、舊版作業管道和意見回饋循環，以及舊版 BI 報告和資訊主頁 (由使用者存取) 之間的關聯性。

### 方案

在規劃階段中，我們對從準備及探索階段取得的輸入內容進行評估，然後用於規劃遷移作業。本階段可細分為以下工作：

1. **為各種用途建立目錄並排定優先順序**

   建議您將遷移程序拆分為多項疊代作業，然後為現有和新的用途建立目錄，並個別指派優先順序。詳情請參閱本文件的「[以疊代方法進行遷移](#migrating-using-an-iterative-approach)」和「[排定用途的優先順序](#prioritizing-use-cases)」章節。
2. **定義成效衡量標準**

   在遷移作業之前，定義如[*主要成效指標 (KPI)*](https://wikipedia.org/wiki/Performance_indicator) 這類明確的成效衡量標準會很有幫助。您可以依據您所設定的標準在每項疊代作業結束後評估遷移成效，以便於在稍後的疊代中改善遷移程序。
3. **建立「完成」的定義**

   對於複雜的遷移作業而言，特定用途的遷移完成狀態可能不易判別，因此您必須對您預期的結束狀態擬定正式定義。這必須是一般通用的定義，以便套用至您要遷移的所有用途。此外，定義應可做為最低需求條件組合，用於考量用途是否已完整遷移。這個定義通常包含查核點，確保用途已完成整合、測試與記錄。
4. **設計及建議概念驗證 (POC)、短期狀態和理想的結束狀態**

   排定用途的優先順序之後，您就可以開始思考用途在整個遷移作業期間的運作方式。您可以考慮將第一個用途遷移作業做為概念驗證 (PoC)，用於驗證初步的遷移方法。此外，請試想在前幾週乃至前幾個月內可以達成什麼樣的短期狀態。您的遷移計畫會如何對使用者造成影響？使用者會採用混合型解決方案，還是您可以先針對部分使用者遷移整個[工作負載](#workload)？
5. **建立時間和成本估算**

   為確保遷移專案順利完成，請務必估算實際情況預計的花費時間。為了達成這個目標，請與所有相關人員討論他們是否可參與，並確認整個專案的參與度。這將有助於您更準確地估算人工成本。如要估算預計的雲端資源用量相關成本，請參閱 BigQuery 說明文件中的「[估算儲存空間和查詢費用](https://docs.cloud.google.com/bigquery/docs/estimate-costs?hl=zh-tw)」和「[BigQuery 費用控管功能簡介](https://docs.cloud.google.com/bigquery/docs/controlling-costs?hl=zh-tw)」等文。
6. **找到遷移合作夥伴並吸引他們加入**

   BigQuery 說明文件介紹了許多工具和資源，可協助您執行遷移作業。然而，如果您沒有任何經驗，或貴機構不具所有必要的技術專業，要自行執行複雜的大型遷移作業並不容易，因此建議您一開始就找到遷移合作夥伴，並吸引他們參與這項作業。詳情請參閱我們的[全球合作夥伴](https://cloud.google.com/partners?hl=zh-tw)和[諮詢服務](https://cloud.google.com/consulting?hl=zh-tw)計畫。

#### 以疊代方法進行遷移

將大型資料倉儲作業遷移至雲端時，最好採取疊代的方法，因此建議您在疊代作業中移轉至 BigQuery。將遷移工作分成多項疊代作業不但可以簡化整體處理程序並降低風險，還可以從每項疊代作業中獲取學習與改進的機會。

「疊代」作業包含在一定時間內卸載或完整遷移一或多個相關[用途](#use-case)所需的工作。您可以將疊代作業視為靈活開發方法中的 [Sprint 週期](https://wikipedia.org/wiki/Scrum_(software_development)#Sprint)，其中由一或多個[使用者案例](https://wikipedia.org/wiki/User_story).組成。

為了方便進行追蹤，您可以考慮將個別用途與一或多個使用者案例建立關聯。舉例來說，假設有以下使用者案例：「身為定價分析師，我想要分析去年的產品價格異動，藉此計算未來的價格。」

對應的用途可能有以下幾項：

* 從儲存產品和價格的交易資料庫中擷取資料。
* 為每項產品將資料轉換為單一時間序列，並填補遺漏值。
* 將結果儲存在資料倉儲中一或多個資料表內。
* 透過 Python 筆記本開放結果以供存取 ([商務應用程式](#business-application))。

此用途的業務價值是支援價格分析。

和多數用途一樣，此用途可能也會支援多個使用者案例。

將用途卸載之後，可能需進行後續疊代作業，才能完整遷移用途。否則，現有的舊版資料倉儲中仍可能保留依附元件，這是因為資料是從該資料倉儲複製而來。後續的完整遷移作業即是卸載以及未先進行卸載而完整遷移之間的差異遷移；換句話說，也就是資料管道的遷移作業，藉此擷取、轉換並載入資料至資料倉儲。

#### 排定用途的優先順序

您要從哪裡開始及結束遷移，取決於您的特定業務需求。請務必對各項用途排定遷移的優先順序，因為在遷移初始階段即取得成功對於後續的雲端導入作業至關重要。在起步時遭遇失敗對整體遷移工作可說是一大挫折。您可能想體驗採用Google Cloud 和 BigQuery 所帶來的優勢，但要對所有在舊版資料倉儲中建立或代管的資料集和資料管道，依據不同的用途進行處理，可說是複雜且耗時的工作。

這個問題沒有一體適用的答案，但在您評估內部部署用途和商務應用程式時，有一些最佳作法可供使用。這類的事先規畫可簡化遷移程序，並讓整個轉換至 BigQuery 的工作更加順暢。

以下各節將探索排定用途優先順序時可使用的方法。

##### 方法：利用目前的機會

檢視目前有助於您獲得特定用途最大投資報酬率的機會。如果您在證明雲端遷移作業的商業價值時面臨壓力，這個方法特別實用。此外，這個方法還可讓您收集額外的資料點，協助評估遷移總費用。

以下提供一些範例問題，協助您找出需要優先處理的用途：

* 用途是否由目前受舊版企業資料倉儲限制的資料集或資料管道所組成？
* 您現有的企業資料倉儲是否需要更新硬體，還是需要擴充硬體？如果是的話，儘快將使用案例卸載至 BigQuery 就更有吸引力。

找出遷移機會可以快速取得成功，立即為使用者和企業帶來實質的好處。

##### 方法：先遷移分析工作負載

先遷移線上分析處理 ([OLAP](https://wikipedia.org/wiki/Online_analytical_processing)) 工作負載，再遷移線上交易處理 [(OLTP)](https://wikipedia.org/wiki/Online_transaction_processing) 工作負載。資料倉儲通常是機構中唯一擁有所有資料的地方，可協助您對機構各項作業建立單一全域資訊。因此，機構通常會有一些可連線至交易系統的資料管道，用於更新狀態或觸發程序，例如在產品庫存不足時購買更多產品。與 OLAP 相比，OLTP 工作負載通常較為複雜，且具備嚴謹的作業需求和[服務水準協議 (SLA)](https://wikipedia.org/wiki/Service-level_agreement)，因此先遷移 OLAP 工作負載也較容易。

##### 方法：著重於使用者體驗

遷移特定資料集並啟用新型的進階分析，藉此找出加強使用者體驗的機會。舉例來說，加強使用者體驗的其中一種方法就是使用即時分析。如果將[即時資料串流](https://docs.cloud.google.com/bigquery/streaming-data-into-bigquery?hl=zh-tw)與歷來資料結合，您就可依此建構精密的使用者體驗，例如：

* 後台員工在行動應用程式上接獲庫存不足警示。
* 讓線上客戶瞭解多消費一元就可進階至下個獎勵層級而受益。
* 護理師透過智慧型手錶掌握患者生命跡象警示，使用平板電腦叫出患者病歷，以採取最理想的行動。

您也可以透過預測性及描述性分析加強使用者體驗。舉例來說，您可以使用 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)、[Vertex AI AutoML 表格](https://docs.cloud.google.com/vertex-ai/docs/start/automl-model-types?hl=zh-tw#tabular)，或 Google 的預先訓練模型進行[圖片分析](https://cloud.google.com/vision/?hl=zh-tw)、[影片分析](https://cloud.google.com/video-intelligence/?hl=zh-tw)、[語音辨識](https://cloud.google.com/speech-to-text/?hl=zh-tw)、[自然語言](https://cloud.google.com/natural-language/?hl=zh-tw)和[翻譯](https://cloud.google.com/translate/?hl=zh-tw)。或者，也可以使用 [Vertex AI](https://cloud.google.com/vertex-ai?hl=zh-tw) 提供自訂訓練模型，處理因應業務需求的各項用途。可能的用途如下：

* 依據市場趨勢及使用者購買行為推薦產品。
* 預測航班延遲。
* 偵測詐騙活動。
* 標記不當內容。
* 實行其他創意概念，讓您的應用程式與競爭對手與眾不同。

##### 方法：依風險最低的用途進行排序

IT 人員可以詢問一些問題，幫助自己評估哪些用途在遷移時的風險最低，而這些用途就非常適合在遷移作業初始階段進行遷移。例如：

* 這項用途的業務重要性為何？
* 這項用途是否涉及大量的員工或客戶？
* 這項用途的目標環境 (例如開發環境或實際工作環境) 為何？
* 我們的 IT 團隊對這項用途的瞭解有多少？
* 這項用途有多少依附元件和整合項目？
* 我們的 IT 團隊是否有適合這項用途的最新完整說明文件？
* 這項用途的作業需求 (SLA) 為何？
* 這項用途的法律或政府法規遵循的規定為何？
* 存取基礎資料集的停機時間和延遲時間有哪些？
* 是否有業務線擁有者渴望並願意儘早遷移其用途？

詳閱這份問題清單可協助您將資料集和資料管道依風險最低到最高的方式進行排名。建議您先遷移低風險資產，然後再遷移高風險資產。

### 執行

收集舊版系統相關資訊並建立待處理用途的優先順序之後，就可以將這些用途組成工作負載，並在疊代作業中進行遷移。

疊代的組成內容可以是單一用途、幾項個別用途，或是單一工作負載中相關的多項用途。您可以為疊代選擇的選項取決於用途的互通連線能力、任何共用的依附元件，以及進行工作時可用的資源。

遷移作業通常包含下列步驟：

以下各節將詳細說明這些步驟。您不必針對每項疊代執行所有的步驟。舉例來說，您可以在某項疊代中選擇從舊版資料倉儲中將資料複製到 BigQuery 中；相反地，也可以在後續疊代中選擇修改原始資料來源中的擷取管道，並直接載入 BigQuery。

#### 1. 設定與資料管理

設定是讓用途在 Google Cloud上執行的必要基礎工作。設定的範疇包含Google Cloud 專案、網路、虛擬私有雲 (VPC) 和資料管理。此外，您也需要充分瞭解目前的進展，哪些可行與哪些不可行。這有助於瞭解遷移作業的要求。您可以使用 [BigQuery 遷移評估功能](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，協助完成這個步驟。

資料管理則是資料生命週期中用於管理資料的基本原則措施，套用範圍包括資料取得、資料使用和資料處理。您的資料管理計畫需明確概述與資料活動相關的各項政策、程序、責任和控管機制。這份計畫可確保資料的收集、維護、使用和發布方式符合貴機構的資料完整性和安全性需求，也能讓員工探索及運用資料，充分發揮資料的潛在效益。

[資料治理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)說明文件可協助您瞭解將地端部署資料倉儲遷移至 BigQuery 時所需的資料治理和控管機制。

#### 2. 遷移結構定義與資料

資料倉儲的結構定義會對資料結構以及資料實體之間的關係給予定義。結構定義是資料設計的核心，因此會影響上游和下游的許多程序。

[結構定義和資料移轉](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)說明文件提供如何將資料移至 BigQuery 的詳盡資訊，以及更新結構定義以充分利用 BigQuery 功能的建議內容。

#### 3. 翻譯查詢

使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 程式碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

部分舊版資料倉儲包含 SQL 標準的擴充功能，可啟用其產品的功能。BigQuery 不支援這些專屬擴充功能，而是符合 [ANSI/ISO SQL:2011](https://wikipedia.org/wiki/SQL:2011) 標準。也就是說，如果 SQL 翻譯工具無法解讀某些查詢，您可能仍需手動重構這些查詢。

#### 4. 遷移商務應用程式

[商務應用程式](#business-application)的形式有許多種，例如資訊主頁、自訂應用程式，以及為交易系統提供意見回饋循環的營運資料管道。

如要進一步瞭解使用 BigQuery 時的數據分析選項，請參閱「[BigQuery 數據分析功能總覽](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)」。本主題將概略介紹報表和分析工具，協助您從資料中取得實用洞察。

資料管道說明文件中的[意見回饋循環](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw#feedback-loops)一節，說明如何使用資料管道建立意見回饋循環，以佈建上游系統。

#### 5. 遷移資料管道

[資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)說明文件提供將舊版資料管道遷移至 Google Cloud的程序、模式和技術。這份文件可協助您瞭解資料管道為何、資料管道可以採用哪些程序與模式，以及較大型資料倉儲系統的遷移作業可以使用哪些遷移選項與技術。

#### 6. 發揮最大效能

BigQuery 可有效率地處理小型和 PB 規模資料集的資料。有了 BigQuery 的協助，資料分析工作不需經過修改，應可在剛遷移的新資料倉儲中順利運作。如果您發現在某些情況下，查詢效能與您的期望不符，請參閱「[查詢效能最佳化簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」一文。

#### 7. 檢查與驗證

在每個疊代結束時，請檢查下列事項以驗證用途遷移作業已執行成功：

* 資料和結構定義都已完整遷移。
* 資料管理相關問題都已全數解決並通過測試。
* 維護與監控程序和自動化作業都已完成建立。
* 查詢已經過正確翻譯。
* 已遷移的資料管道如預期般運作。
* 商務應用程式已正確設定，可存取已遷移的資料和查詢。

您可以先使用[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator)，這項開放原始碼 Python CLI 工具會比較來源和目標環境的資料，確保兩者相符。支援多種連線類型，以及多層驗證功能。

建議您評估用途遷移作業的影響，例如提升效能、降低成本或創造嶄新的技術或商機。然後，您就可以更加準確地量化投資報酬率的價值，並將這個價值與疊代的成功標準進行比較。

疊代作業通過驗證後，您就可以將已遷移的用途發布至實際工作環境，並開放讓使用者存取已遷移的資料集和商務應用程式。

最後，記下自這項疊代作業學習到的筆記和經驗，然後在下次疊代作業中運用這些經驗，就能加速完成遷移作業。

## 遷移工作摘要

如本文件詳述，您會在遷移期間同時執行舊版資料倉庫和 BigQuery。下圖中的參考架構強調這兩種資料倉儲都提供類似的功能和路徑，都可從來源系統擷取資料、與商務應用程式整合，並提供必要的使用者權限。重要的是，這張圖表也說明資料會從資料倉儲同步處理至 BigQuery。如此一來，您就能在遷移工作的期間內卸載用途。

假設您要從資料倉儲完整遷移至 BigQuery，遷移作業的結束狀態如下所示：

## 後續步驟

* 使用下列工具執行 BigQuery 遷移作業：

  + 執行[遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，評估將資料倉儲遷移至 BigQuery 的可行性和潛在效益。
  + 使用 SQL 翻譯工具 (例如[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)、[翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 和[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw))，自動將 SQL 查詢轉換為 GoogleSQL，包括 Gemini 輔助的 SQL 自訂功能。
  + 將資料倉儲遷移至 BigQuery 後，請執行[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)，驗證新遷移的資料。
* 如要進一步瞭解資料倉儲遷移作業，請參閱下列資源：

  + Cloud Architecture Center 提供[遷移資源](https://docs.cloud.google.com/architecture/migrations?hl=zh-tw)，協助您規劃及執行遷移至 Google Cloud的作業。
  + 瞭解如何從資料倉儲[遷移結構定義和資料](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)
  + 瞭解[如何從資料倉儲遷移資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
  + 瞭解 [BigQuery 中的資料治理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* 與專業服務團隊合作，協助規劃及部署遷移作業。 Google Cloud 詳情請參閱 [Google Cloud 專業服務](https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started?hl=zh-tw#gcp_professional_services)
* 瞭解如何從特定資料倉儲遷移至 BigQuery：

  + [從 Amazon Redshift 遷移](https://docs.cloud.google.com/bigquery/docs/migration/redshift-overview?hl=zh-tw)
  + 從 Apache Hadoop 遷移：
    - [從 Hadoop 遷移權限](https://docs.cloud.google.com/bigquery/docs/hadoop-permissions-migration?hl=zh-tw)
    - [從 HDFS 資料湖泊遷移資料表](https://docs.cloud.google.com/bigquery/docs/hdfs-data-lake-transfer?hl=zh-tw)
  + [從 Apache Hive 遷移](https://docs.cloud.google.com/bigquery/docs/migration/hive?hl=zh-tw)
  + [從 Netezza 遷移](https://docs.cloud.google.com/bigquery/docs/migration/netezza?hl=zh-tw)
  + [從 Oracle 遷移](https://docs.cloud.google.com/bigquery/docs/migration/oracle-migration?hl=zh-tw)
  + [從 Snowflake 遷移](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-migration-intro?hl=zh-tw)
  + [從 Teradata 遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]