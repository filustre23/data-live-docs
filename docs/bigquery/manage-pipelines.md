Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理管道

本文說明如何管理 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)，包括如何排定管道的執行時間和刪除管道。

本文也說明如何在 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 中查看及管理管道中繼資料。

管道由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供支援。

## 事前準備

1. [建立 BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
2. 如要在 Knowledge Catalog 中管理管道中繼資料，請確保專案已啟用 [Dataplex API](https://docs.cloud.google.com/dataplex/docs/enable-api?hl=zh-tw)。 Google Cloud

### 必要的角色

如要取得管理管道所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要刪除管道：
  [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Admin)  (`roles/dataform.Admin`)
  管道
* 如要查看及執行管道：
  專案的 [Dataform 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Viewer)  (`roles/dataform.Viewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要在 Knowledge Catalog 中管理管道中繼資料，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/dataplex/docs/iam-roles?hl=zh-tw)。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

**注意：** 建立管道時，BigQuery 會授予您該管道的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。在 Google Cloud 專案中獲派 Dataform 管理員角色的所有使用者，都擁有專案中所有管道的存取權。

## 查看所有管道

如要查看專案中的所有管道清單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Pipelines」。

## 查看過去的手動執行作業

如要查看所選管道過去的手動執行作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「執行」。
5. 選用：如要重新整理過往執行記錄清單，請按一下「重新整理」。

## 設定管道執行作業失敗的快訊

每個管道都有對應的 Dataform 存放區 ID。
系統會使用對應的 Dataform 存放區 ID，在 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 中記錄每次 BigQuery 管道執行作業。您可以使用 Cloud Monitoring 觀察 BigQuery 管道執行作業的 Cloud Logging 記錄趨勢，並在發生您描述的情況時收到通知。

如要在 BigQuery 管道執行失敗時收到警告，可以為對應的 Dataform 存放區 ID 建立以記錄為準的警告政策。如需操作說明，請參閱「[設定工作流程叫用失敗的快訊](https://docs.cloud.google.com/dataform/docs/monitor-runs?hl=zh-tw#configure-alerts-failed-workflow-invocations)」。

如要找出管道的 Dataform 存放區 ID，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「設定」。

   管道的 Dataform 存放區 ID 會顯示在「設定」分頁底部。

## 刪除管道

如要永久刪除管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Pipelines」。
4. 找出要刪除的管道。
5. 按一下管道旁的 more\_vert「View actions」(查看動作)，然後按一下「Delete」(刪除)。
6. 點選「刪除」。

## 管理 Knowledge Catalog 中的中繼資料

您可以使用 Knowledge Catalog 儲存及管理管道的中繼資料。根據預設，管道會顯示在 Knowledge Catalog 中，不需額外設定。

您可以使用 Knowledge Catalog 管理所有[管道位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的管道。在 Knowledge Catalog 中管理管道時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/dataplex/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從管道擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應 Google Cloud 專案

Knowledge Catalog 會將管道記錄為[項目](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entries)，並提供下列項目值：

系統項目群組
:   管道的[系統項目群組](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要查看 Knowledge Catalog 中管道項目的詳細資料，請查看 `dataform` 系統項目群組。如需查看項目群組中所有項目的清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」。�

系統項目類型
:   管道的[系統項目類型](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。如要查看管道詳細資料，您必須查看 `dataform-code-asset` 系統項目類型、使用切面篩選器篩選結果，並將 `dataform-code-asset` 切面內的 `type` 欄位設為 `WORKFLOW`。[然後選取所選管道的項目。
    如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如需查看所選項目詳細資料的操作說明，請參閱 Knowledge Catalog 說明文件中的「[查看項目的詳細資料](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw#view-entry-details)」一節。](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)

系統切面類型
:   管道的[系統切面類型](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要透過[切面](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspects)註解資料管道項目，為 Knowledge Catalog 中的管道提供額外背景資訊，請查看 `dataform-code-asset` 切面類型、使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面內的 `type` 欄位設為 `WORKFLOW`](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)。如需如何使用切面註解項目的操作說明，請參閱 Knowledge Catalog 說明文件中的「[管理切面及豐富中繼資料](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw)」一文。

類型
:   資料畫布的類型為 `WORKFLOW`。
    這類篩選器可讓您在 `dataform-code-asset` 系統項目類型和 `dataform-code-asset` 切面類型中，使用`aspect:dataplex-types.global.dataform-code-asset.type=WORKFLOW`[以切面為準的篩選器](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)查詢，篩選管道。

如需在 Knowledge Catalog 中搜尋資產的操作說明，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 中搜尋資料資產](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
* 瞭解如何[排定管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]