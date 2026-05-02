* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立及管理工作區

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [bigquery-repositories-feedback@google.com](mailto:%20bigquery-repositories-feedback@google.com)。

本文說明如何在 BigQuery 中使用工作區，包括下列工作：

* 建立工作區
* 刪除工作區
* 在工作區中處理檔案
* 對工作區中的檔案執行版本管控

## 事前準備

如果尚未建立 BigQuery 存放區，請先[建立](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw)。

### 必要的角色

工作區的存取權取決於上層存放區授予的角色。
詳情請參閱「[必要的角色](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#required-roles)」。

## 建立工作區

視您使用的是 BigQuery 存放區或第三方存放區，工作區的建立方式會有所不同。

### 在 BigQuery 存放區中建立工作區

如要在 BigQuery 存放區中建立新的工作區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取要建立工作區的存放區。
5. 在編輯器中，按一下「新增工作區」。
6. 在「建立開發工作區」窗格的「工作區 ID」欄位中，輸入工作區的專屬 ID。

   ID 只能使用數字、英文字母、連字號和底線。
7. 點選「建立」。

### 在第三方存放區中建立工作區

如要在第三方存放區中建立新的工作空間，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取要建立工作區的存放區。
5. 在編輯器中，按一下「新增工作區」。系統隨即會開啟「建立開發工作區」窗格。
6. 視要為工作區使用現有或新分支而定，選擇「現有遠端分支」或「新分支」圓形按鈕。
7. 指定要使用的分支版本：

   1. 如果選擇「現有的遠端分支版本」圓形按鈕，請在「遠端分支版本」欄位中選擇現有的分支版本。
   2. 如果選擇「New branch」(新分支) 單選按鈕，請在「Workspace ID」(工作區 ID) 欄位中輸入分支名稱。在第三方存放區中建立的分支版本名稱與 BigQuery 工作區 ID 相同。

      ID 只能使用數字、英文字母、連字號和底線。
8. 點選「建立」。

## 在工作區中建立目錄

如要在工作區中建立目錄，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 按一下 add
   **開啟建立選單**。
7. 按一下「在存放區中建立」**>「目錄」**。
8. 在「Add a directory path」(新增目錄路徑) 欄位中，輸入目錄路徑。
9. 按一下「建立目錄」。

## 處理工作區中的檔案

您可以在工作區中建立新檔案，或上傳現有檔案。

您可以建立或上傳下列類型的檔案至存放區：

* SQL 查詢
* Python 筆記本
* [資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)
* [準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)
* 其他類型的檔案

### 建立檔案

如要在工作區中建立檔案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 按一下 add
   **開啟建立選單**。
7. 按一下「Create in repository」(在存放區中建立)，然後點選要建立的檔案類型。
8. 在「Name」欄位中輸入檔案名稱。
9. 選用：在「Parent directory」(上層目錄) 欄位中，輸入要建立檔案的目錄路徑。
10. 按一下 [儲存]。

### 上傳檔案

如要將檔案上傳至工作區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 按一下 add
   **開啟建立選單**。
7. 按一下「上傳至存放區」，然後按一下要上傳的檔案類型。
8. 在「上傳」窗格中，執行下列任一操作：

   * 在「File upload」(檔案上傳) 欄位中，按一下「Browse」(瀏覽)，選取檔案，然後按一下「Open」(開啟)。
   * 在「網址」欄位中輸入檔案網址。
9. 選用：在「Parent directory」(上層目錄) 欄位中，輸入要建立檔案的目錄路徑。
10. 按一下「上傳」。

### 刪除檔案

如要從工作區刪除檔案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 選取要刪除的檔案，按一下 more\_vert「View actions」(查看動作)，然後按一下「Delete」(刪除)。
7. 按一下 [刪除] 加以確認。

## 使用檔案的版本管控

本節說明如何在 BigQuery 中使用版本管控功能，追蹤工作區中的檔案。

BigQuery 會使用 Git 追蹤存放區內檔案的每項變更。在 BigQuery 存放區中，您可以直接與 Git 存放區互動。在已連結的存放區中，您可以與[連結存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#connect-third-party)時設定的遠端存放區預設分支互動。

BigQuery 會根據工作區中變更的狀態，顯示版本管控選項。舉例來說，只有在工作區有未提交的本機變更時，BigQuery 才會顯示提交選項。如果工作區中的檔案與預設或預設分支完全相同，BigQuery 會顯示「最新狀態」。

BigQuery 會顯示下列版本管控選項：

修訂 X 項變更
:   在工作區或所選已變更的檔案中，提交 X 個本機變更。BigQuery 會顯示未提交的變更。

推送至預設分支版本
:   將已提交的變更推送至預設分支版本。如果工作區中沒有未提交的變更，且有未推送的提交，即可在存放區中使用這個選項。

推送至「`your-branch-name`」
:   將已提交的變更推送至 `your-branch-name`。
    如果存放區[已連線至第三方 Git 存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#connect-third-party)，且工作區中沒有未提交的變更，即可使用這個選項。第三方存放區中的遠端分支版本名稱與 BigQuery 工作區 ID 相同。

從預設分支版本提取
:   使用預設分支版本的最新變更更新工作區。如果工作區中沒有未提交的變更，存放區就會顯示這個選項。

從「`your-branch-name`」提取
:   從 `your-branch-name` 更新工作區，套用最近的變更。
    如果存放區[已連線至第三方 Git 存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#connect-third-party)，且工作區中沒有未提交的變更，即可使用這個選項。第三方存放區中的遠端分支版本名稱與 BigQuery 工作區 ID 相同。

還原為上次修訂版本
:   將工作區中的檔案還原至上次提交時的狀態。

### 提取變更

如果工作區與存放區不同步，BigQuery 會顯示「Pull」(提取) 選項。

如要將存放區中的變更提取至工作區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 在工作區窗格中執行下列操作：

   1. 如果您位於 BigQuery 存放區，請按一下「從預設分支版本提取」。
   2. 如果您位於[已連結至第三方 Git 存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#connect-third-party)的存放區中，請執行下列任一操作：

      1. 按一下「從預設分支版本提取」，從第三方存放區的預設分支版本提取。
      2. 按一下「從『`your-branch-name`』提取」，從與目前工作區對應的第三方存放區分支版本提取。

### 修訂變更

在工作區中進行變更後，BigQuery 會顯示「Commit」(提交) 選項。你可以修訂所有本機變更或選取的檔案。
您新增或修改的檔案會在工作區窗格中以藍點標示。

**注意：** BigQuery 預設會使用已驗證使用者的電子郵件地址做為修訂版本作者，但 Dataform API 允許為修訂版本作者設定自訂電子郵件地址。 Google Cloud 這項行為與 [`git commit --author` 指令](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---authorauthor)類似，只會影響 Git 提交記錄。提交作者身分未經過加密驗證。

如要將工作區的變更提交至存放區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 在工作區窗格中，按一下「提交變更」圖示 **X**。
7. 在「Commit changes」(提交變更) 窗格中，執行下列操作：

   1. 選取要修訂的已變更檔案。

      如未選取任何檔案，BigQuery 會修訂所有本機變更。您可以依檔案狀態、檔案名稱和路徑篩選變更的檔案。
   2. 在「新增提交訊息」欄位中，輸入提交的說明。
   3. 按一下「Commit All changes」或「Commit X changes」。

      按鈕名稱會因您選取的待提交檔案而異。

### 推送變更

提交變更後，BigQuery 會顯示「推送」選項。

如要將工作區的變更推送到存放區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 在工作區窗格中執行下列操作：

   1. 如果您位於 BigQuery 存放區，請按一下「Push to default branch」(推送至預設分支)。
   2. 如果您位於[已連結至第三方 Git 存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#connect-third-party)的存放區中，請執行下列任一操作：

      1. 按一下「推送至預設分支版本」，將變更推送至第三方存放區的預設分支版本。
      2. 按一下「推送至」**`your-branch-name`**，將目前工作區的內容推送至對應的第三方存放區分支。

### 還原未提交的變更

如要還原未提交的變更，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 在工作區窗格中，按一下版本管控按鈕上的 arrow\_drop\_down 箭頭下拉式選單，然後按一下「Revert to last commit」(還原至上次提交)。

### 解決合併衝突

如果工作區的本機變更與存放區預設分支版本的變更不相容，就可能發生合併衝突。如果多位使用者同時編輯同一個檔案，通常會發生合併衝突。

通常在其他使用者將衝突變更推送至同一分支後，您從該分支提取時會遇到合併衝突。您必須編輯受影響的檔案，手動解決合併衝突。

以下程式碼範例顯示 SQL 檔案中顯示的合併衝突：

```
    <<<<<<< HEAD
    SELECT 1 as CustomerOrders
    =======
    SELECT 1 as Orders
    >>>>>>> refs/heads/main
```

如要解決合併衝突，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 選取受影響的檔案，並根據所選變更進行編輯。
7. [修訂變更](#commit)。
8. 選用：[推送變更](#push)。

### 查看修訂記錄

如要查看提交記錄，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要使用的工作區的存放區。
5. 找出工作區，然後按一下「開啟」。

   工作區隨即會在「folder\_data」folder\_data**Git 存放區**窗格中開啟。
6. 在工作區窗格中，按一下版本管控按鈕上的arrow\_drop\_down箭頭下拉式選單，然後點選「查看提交記錄」。

## 刪除工作區

如要刪除工作區和所有內容，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Repositories」，在詳細資料窗格中開啟「Repositories」分頁。
4. 選取包含要刪除工作區的存放區。
5. 找出工作區，然後依序點按 more\_vert「開啟動作」**>**「刪除」。
6. 點選「刪除」。

## 後續步驟

* 瞭解如何[建立存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]