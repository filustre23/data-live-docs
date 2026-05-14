Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Gemini 輔助功能編寫查詢

這份文件說明如何使用 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw) 的 AI 輔助功能，以 SQL 查詢和 Python 程式碼查詢資料。
Gemini in BigQuery 可以生成及解釋查詢與程式碼、在您輸入時補全查詢與程式碼，以及修正程式碼錯誤。

---

如要直接在 Google Cloud 控制台中，按照這項工作的逐步指南操作，請按一下「Guide me」(逐步引導)：

[逐步引導](https://console.cloud.google.com/bigquery?walkthrough_id=bigquery--write-sql-gemini&%3Bstart_index=1&hl=zh-tw)

---

未經您明確許可，Gemini for Google Cloud 不會使用您的提示或回覆內容來訓練模型。如要進一步瞭解 Google 如何使用您的資料，請參閱「[Gemini for Google Cloud 如何使用您的資料](https://docs.cloud.google.com/gemini/docs/discover/data-governance?hl=zh-tw)」一文。

**注意：** 如要選擇加入資料共用，以利改善 [預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)中的 Gemini in BigQuery 功能，請參閱「[協助改善建議](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#help_improve_suggestions_2)」一文。

Gemini in BigQuery 僅支援英文提示。

本文適用於使用 SQL 查詢和 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)的資料分析師、資料科學家和資料開發人員。本教學課程假設您瞭解如何在 BigQuery Studio 環境中查詢資料，或如何使用 Python 筆記本分析 BigQuery 資料。

## 事前準備

1. 確認已為 Google Cloud 專案設定 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)。
   這個步驟通常由管理員完成。
   完成本節的其餘步驟前，Gemini in BigQuery 功能可能會停用或無法使用。
2. 如要使用 [Gemini Cloud Assist](https://docs.cloud.google.com/cloud-assist/overview?hl=zh-tw) 在 Gemini Cloud Assist 窗格中編寫程式碼，請按照「[設定 Gemini Cloud Assist](https://docs.cloud.google.com/cloud-assist/set-up-gemini?hl=zh-tw)」一文中的步驟操作。
3. 如要在 BigQuery 的 Colab Enterprise 筆記本中使用 Gemini 解釋及修正 Python 程式碼，您也必須按照「[為專案設定 Gemini in Colab Enterprise](https://docs.cloud.google.com/colab/docs/gemini-in-colab/set-up-gemini?hl=zh-tw)」一文中的步驟操作。
4. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
5. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
6. 在 BigQuery 工具列中，點選「pen\_sparkarrow\_drop\_downGemini」**Gemini**。
7. 在功能清單中，確認已選取下列功能：

   * **SQL 查詢專用 Gemini** 清單：

     + **自動完成** (預先發布版)。在查詢編輯器中輸入內容時，Gemini 會根據目前查詢的情境，建議合理的後續步驟，或協助您反覆調整查詢。
     + **自動生成**：您可以在 BigQuery 查詢編輯器中，使用自然語言註解提示 Gemini in BigQuery 生成 SQL 查詢。
     + **SQL 生成工具**。您可以在工具中輸入自然語言文字，生成 SQL 查詢，並選擇修正查詢結果、選擇資料表來源和比較結果。
     + **說明**。您可以提示 Gemini in BigQuery，以自然語言說明 SQL 查詢。
   * **Python 筆記本專用 Gemini** 清單：

     + **程式碼自動完成** (預先發布版)。Gemini 會根據筆記本中的內容，提供符合情境的適當建議。
     + **程式碼生成**。您可以使用自然語言陳述式或問題，提示 Gemini 生成 Python 程式碼。
8. 如要完成本文中的工作，請確保您具備[必要的 Identity and Access Management (IAM) 權限](#required_permissions)。

### 必要的角色

如要取得使用 Gemini 輔助撰寫查詢所需的權限，請要求系統管理員授予專案的「Gemini for Google Cloud 使用者」 (`roles/cloudaicompanion.user`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備在 Gemini 協助下撰寫查詢所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用 Gemini 輔助功能撰寫查詢，必須具備下列權限：

* `cloudaicompanion.entitlements.get`
* `cloudaicompanion.instances.completeTask`
* 說明 SQL 查詢：
  `cloudaicompanion.companions.generateChat`
* 補全 SQL 或 Python 程式碼：
  `cloudaicompanion.instances.completeCode`
* 生成 SQL 或 Python 程式碼：
  `cloudaicompanion.instances.generateCode`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 生成 SQL 查詢

Gemini for Google Cloud產品仍處於早期技術階段，因此可能會生成看似合理卻與事實不符的輸出內容。使用輸出內容前，請一律確認 Gemini for Google Cloud 產品輸出內容是否屬實。詳情請參閱「[Gemini for Google Cloud 和負責任的 AI 技術](https://docs.cloud.google.com/gemini/docs/discover/responsible-ai?hl=zh-tw)」。

如要根據資料結構定義產生 SQL 查詢，請使用自然語言陳述句或問題 (也稱為*提示*)，要求 Gemini in BigQuery 執行這項操作。你也可以瀏覽 Gemini 提供的提示建議。即使您未編寫程式碼、不太瞭解資料結構定義，或只具備 GoogleSQL 語法的基礎知識，Gemini in BigQuery 都可以生成 SQL，協助您探索資料。

### 使用 SQL 生成工具

使用 SQL 生成工具，就能以自然語言生成最近查看或查詢過的資料表相關 SQL 查詢。您也可以使用這項工具修改現有查詢，以及手動指定要產生 SQL 的資料表。

如要使用 SQL 程式碼生成工具，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器旁，按一下「pen\_spark SQL 生成工具」。
3. 在「透過 Gemini 生成 SQL 程式碼」對話方塊中，您可以選擇：

   * 輸入您最近查看或查詢的資料表的自然語言提示詞。舉例來說，如果您最近查看了 [`bigquery-public-data.austin_bikeshare.bikeshare_trips` 資料表](https://console.cloud.google.com/bigquery?ws=%211m5%211m4%214m3%211sbigquery-public-data%212saustin_bikeshare%213sbikeshare_trips&hl=zh-tw)，可以輸入以下內容：

     ```
     Show me the duration and subscriber type for the ten longest trips.
     ```
   * 按一下 Gemini 建議的提示詞 ([預覽](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。提示詞會複製到「透過 Gemini 生成 SQL」對話方塊。
4. 點按「生成」。

   生成的 SQL 查詢大致如下：

   ```
   SELECT
       subscriber_type,
       duration_sec
     FROM
         `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
   ORDER BY
       duration_sec DESC
   LIMIT 10;
   ```

   **注意：** 每次輸入相同提示詞時，Gemini in BigQuery 可能會建議不同的語法。
5. 查看生成的 SQL 查詢，然後進行下列任一操作：

   * 如要接受生成的 SQL 查詢，請按一下「插入」，將陳述式插入查詢編輯器。然後點選「執行」，即可執行建議的 SQL 查詢。
   * 如要編輯提示，請按一下「編輯」，然後修改或替換初始提示。編輯提示後，按一下「更新」即可產生新的查詢。
   * 如要更新用來生成建議 SQL 查詢的資料表來源，請按一下「編輯資料表來源」，選取適當的核取方塊，然後按一下「套用」。
   * 如要查看生成查詢的自然語言摘要，請按一下「查詢摘要」。
   * 如要修正建議的 SQL 查詢，請在「修正」欄位中輸入任何修正內容，然後點選 send「修正」。舉例來說，輸入 `limit to 1000` 即可限制查詢結果數量。如要比較查詢的變更，請勾選「顯示差異」核取方塊。
   * 如要關閉建議查詢，請關閉 SQL 生成工具。

#### 關閉 SQL 生成工具

如要瞭解如何關閉 SQL 生成工具，請參閱「[關閉 Gemini 查詢輔助功能](#disable-gemini-features)」。

### 根據註解生成 SQL 查詢

您可以在查詢編輯器中，透過註解描述想要的查詢，藉此生成 SQL。

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，點按 add\_box「SQL query」(SQL 查詢)。
3. 在查詢編輯器中，針對您最近查看或查詢的資料表撰寫 SQL 註解。舉例來說，如果您最近查看了 [`bigquery-public-data.austin_bikeshare.bikeshare_trips` 資料表](https://console.cloud.google.com/bigquery?ws=%211m5%211m4%214m3%211sbigquery-public-data%212saustin_bikeshare%213sbikeshare_trips&hl=zh-tw)，可以撰寫以下註解：

   ```
   # Show me the duration and subscriber type for the ten longest trips.
   ```
4. 按下 `Enter` 鍵 (如使用 macOS 裝置，則按 `Return` 鍵)。

   建議的 SQL 查詢會與下列內容相似：

   ```
   # Show me the duration and subscriber type for the ten longest trips

   SELECT
     duration_sec,
     subscriber_type
     AVG(duration_minutes) AS average_trip_length
   FROM
     `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   ORDER BY
     duration_sec
   LIMIT 10;
   ```
5. 如要接受建議，請按下 `Tab` 鍵。

### 透過 Gemini Cloud Assist 生成 SQL 查詢

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意事項：**如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [gemini-in-bigquery-feedback@google.com](mailto:gemini-in-bigquery-feedback@google.com)。

您可以透過 Google Cloud 控制台的[「Cloud Assist」面板](https://docs.cloud.google.com/cloud-assist/chat-panel?hl=zh-tw)，在 BigQuery 中生成 SQL 查詢。

必須先啟用 Gemini Cloud Assist，才能透過 Gemini Cloud Assist 對話生成 SQL 查詢。詳情請參閱「[設定 Gemini Cloud Assist](https://docs.cloud.google.com/cloud-assist/set-up-gemini?hl=zh-tw)」的說明。

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，點選 add\_box「SQL query」(SQL 查詢)，開啟新的 SQL 查詢。
3. 在 Google Cloud 工具列，點選 spark「Open or close Gemini AI chat」，開啟 Gemini Cloud Assist 對話。
4. 在「Enter a prompt」(輸入提示) 欄位輸入提示，以便生成 SQL 查詢。例如：

   ```
   Generate a SQL query to show me the duration and subscriber type for the ten longest trips.
   ```
5. 點選「Send prompt」(傳送提示)。回覆中的 SQL 查詢大致如下：

   ```
   SELECT
        subscriber_type,
        duration_sec
    FROM
        `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
    ORDER BY
        duration_sec DESC
    LIMIT 10;
    ```
   ```
6. 查看生成的 SQL 查詢。
7. 如要執行生成的 SQL 查詢，請點選 content\_copy「Copy to clipboard」(複製到剪貼簿)，將生成的程式碼貼到查詢編輯器，然後點選 play\_circle「Run」(執行)。
8. 如果查詢編輯器已開啟，您可以選用下列其中一個選項：

   * 如要查看現有查詢與生成的查詢之間有何差異，請點選「Preview」(預覽)。

     比較窗格便會開啟。查看變更後，請選取下列其中一個選項：

     + 「Accept and run」(接受並執行)：接受變更並執行查詢。
     + 「Accept」(接受)：接受變更。
     + 「Decline」(拒絕)：關閉比較窗格，而不變更現有查詢。
   * 如要將查詢編輯器的內容改為生成的查詢並執行該查詢，請按一下「Apply and run」(套用並執行)。

### SQL 生成功能使用提示

下列提示可提升 Gemini in BigQuery 提供的建議品質：

* 如要手動指定要使用的資料表，您可以將完整的資料表名稱放在反引號 (`` ` ``) 中，例如 `` `PROJECT.DATASET.TABLE` ``。
* 如果資料欄名稱或語意關係很複雜或不明確，您可以在提示中提供背景資訊，引導 Gemini 提供切合需求的答案。例如，如要讓生成的查詢參照特定資料欄名稱，請描述該資料欄名稱及其與所需答案的關聯性。為了鼓勵答案參照「生命週期值」或「毛利率」等複雜字詞，請描述該概念及其與資料的關聯性，以改善 SQL 產生結果。
* 利用註解生成 SQL 時，您可以將提示分成多行，並在每行開頭加上 `#` 字元。
* 系統生成 SQL 查詢時會考量資料欄說明。為提高準確率，請在結構定義中新增資料欄說明。如要進一步瞭解資料欄說明，請參閱「指定結構定義」中的[資料欄說明](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_descriptions)一節。

### 將註解轉換為 SQL 程式碼

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意事項：**如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [gemini-in-bigquery-feedback@google.com](mailto:gemini-in-bigquery-feedback@google.com)。

您可以使用註解做為提示詞，建立 SQL 查詢，協助您探索 BigQuery 中的資料。您可以嵌入含有自然語言提示詞的註解，描述您想從資料中取得的資訊。Gemini 會傳回 SQL 程式碼，供您比較或插入查詢。自然語言運算式可協助您疊代及轉換 SQL 程式碼。自然語言運算式也能協助處理 SQL 語法，例如時間戳記和 window 函式。

如要使用自然語言 SQL 程式碼生成功能，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。**BigQuery**

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 **BigQuery Studio** 查詢編輯器中，按一下 pen\_spark，並確認已啟用 Gemini SQL 程式碼「Auto-generation」(自動產生)。
3. 在 BigQuery 查詢編輯器中，輸入 SQL 查詢，其中包含以註解形式提供的自然語言提示詞，格式為 `/* natural
   language text */`，內容是您最近查看或查詢的資料表。Gemini in BigQuery 會使用最近查詢的資料表的中繼資料，盡量找出適當的資料，因此您可以查詢資料表，協助引導回覆內容。為獲得最佳結果，自然語言提示詞應具體說明 SQL 語法和資料，而非「最佳化我的查詢」等概略的語句。

   舉例來說，如果您最近查詢了 [`bigquery-public-data.austin_bikeshare.bikeshare_trips` 資料表](https://console.cloud.google.com/bigquery?ws=%211m5%211m4%214m3%211sbigquery-public-data%212saustin_bikeshare%213sbikeshare_trips&hl=zh-tw)，可以輸入以下內容：

   ```
   SELECT
       subscriber_type,
       /* the name of the day of week of the trip start ordered longest to
        shortest trip with the trip's duration */
   FROM
       `bigquery-public-data`.`austin_bikeshare`.`bikeshare_trips`
   LIMIT 10;
   ```
4. 醒目顯示要讓 Gemini 轉換的 SQL 查詢，包括自然語言運算式。在上述範例中即為整個 SQL 範例。
5. 如要生成 SQL 程式碼，請在邊界或查詢編輯器中，點選 auto\_awesome「Gemini」，然後點選 pen\_spark「Convert comments to SQL」(將註解轉換為 SQL 程式碼)。
6. 查看生成的 SQL 查詢。「Transform SQL with Gemini」(透過 Gemini 轉換 SQL 程式碼) 輸出內容會顯示原始文字和生成文字之間的差異。生成的 SQL 查詢大致如下：

   ```
   SELECT
     subscriber_type,
     FORMAT_TIMESTAMP('%A', start_time) AS day_of_week,
     duration_minutes
   FROM
     `bigquery-public-data`.`austin_bikeshare`.`bikeshare_trips`
   ORDER BY
     duration_minutes DESC
   LIMIT
     10;
   ```
7. 如要將查詢複製到查詢編輯器，請按一下「Insert」(插入)。您先前的陳述式 (包括自然語言提示詞) 會顯示在註解中，而生成的 SQL 程式碼會複製到編輯窗格，您可以在其中執行或編輯程式碼。您也可以選取下列任一選項：

   * 「Refine」(修正)：提示 Gemini 修改生成的 SQL 程式碼
   * 「Edit Table Sources」(編輯資料表來源)：選取其他資料表
   * 「Query Summary」(查詢摘要)：請 Gemini 提供 SQL 查詢的摘要。

## 補全 SQL 查詢

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

SQL 補全功能會嘗試根據查詢編輯器中的內容，提供符合情境的適當建議。在您輸入時，Gemini 會建議與目前查詢內容相關且合理的後續步驟，或協助您疊代查詢。

如要使用 Gemini in BigQuery 的 SQL 補全功能，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，複製以下內容：

   ```
   SELECT
     subscriber_type
     , EXTRACT(HOUR FROM start_time) AS hour_of_day
     , AVG(duration_minutes) AS avg_trip_length
   FROM
     `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   ```

   錯誤訊息指出 `subscriber_type` 並未分組或匯總。這情況很常見，您需要協助來修正查詢。
3. 在 `subscriber_type` 的結尾按下`空格`鍵。

   建議的查詢修正內容可能會類似以下文字：

   ```
   GROUP BY
     subscriber_type, hour_of_day;
   ```

   您也可以按下 `Enter` 鍵 (macOS 上為 `Return` 鍵) 來生成建議。
4. 如要接受建議，請按下 `Tab` 鍵，或將游標懸停在建議文字上，然後點閱其他建議。如要關閉建議，請按下 `Esc` 鍵或繼續輸入內容。

## 說明 SQL 查詢

您可以提示 Gemini in BigQuery，用自然語言說明 SQL 查詢。此說明功能可協助您瞭解，語法、基礎結構定義和業務情境因查詢長度或複雜性而難以評估的查詢。

如要請 Gemini 說明 SQL 查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，開啟或貼上您想要 Gemini 說明的查詢。
3. 反白選取您希望 Gemini in BigQuery 說明的查詢。
4. 依序點按 astrophotography\_mode「Gemini」與「Explain this query」(說明這項查詢)。

   SQL 說明會顯示在「Cloud」面板中。

## 修正及說明 SQL 錯誤

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意事項：**如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [gemini-in-bigquery-feedback@google.com](mailto:gemini-in-bigquery-feedback@google.com)。

您可以使用 Gemini in BigQuery 修正及說明 SQL 查詢中的錯誤。如要在執行前修正查詢文字中的錯誤，請按照下列步驟操作：

1. 反白選取有錯的文字。
2. 依序按一下 auto\_awesome「Refine」(修正) 和 auto\_fix\_normal「Fix it」(修正問題)。
3. Gemini Cloud Assist 窗格隨即開啟，並顯示修正錯誤的建議查詢變更。
4. 按一下「Apply & run」(套用並執行) 即可進行變更，或按一下「Preview」(預覽) 開啟比較窗格，查看查詢與建議查詢之間的差異。

如要修正執行查詢後出現的錯誤，請按照下列步驟操作：

1. 在「Results」(結果) 窗格中，按一下錯誤旁的「Gemini suggested fixes」(Gemini 建議的修正內容)。
2. Gemini Cloud Assist 窗格隨即開啟，並顯示修正錯誤的建議查詢變更。
3. 按一下「Apply & run」(套用並執行) 即可進行變更，或按一下「Preview」(預覽) 開啟比較窗格，查看查詢與建議查詢之間的差異。

## 生成 Python 程式碼

您可以問問 Gemini in BigQuery，透過自然語言陳述式或問題生成 Python 程式碼。Gemini in BigQuery 會從 BigQuery 專案直接提取相關資料表名稱，並提供一或多個 Python 程式碼建議，生成可執行的個人化 Python 程式碼。

### 使用 Python 程式碼生成工具

在以下範例中，您會產生 BigQuery 公開資料集的程式碼 `bigquery-public-data.ml_datasets.penguins`。

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器的分頁列中，點選「SQL 查詢」add\_box旁的下拉式箭頭 arrow\_drop\_down，然後點選「Notebook」(筆記本)。

   新的筆記本隨即開啟，內含的儲存格會顯示針對 `bigquery-public-data.ml_datasets.penguins` 公開資料集執行的範例查詢。
3. 如要插入新的程式碼儲存格，請在工具列中按一下「程式碼」add。新的程式碼儲存格會顯示「開始使用 AI 編寫或生成程式碼」訊息。
4. 在新的程式碼儲存格中，按一下「生成」。
5. 在「Generate」(生成) 編輯器中，輸入下列自然語言提示：

   ```
   Using bigquery magics, query the `bigquery-public-data.ml_datasets.penguins` table
   ```
6. 按下 `Enter` 鍵 (如使用 macOS 裝置，則按 `Return` 鍵)。

   建議的 Python 程式碼大致如下：

   ```
   %%bigquery
   SELECT *
   FROM `bigquery-public-data.ml_datasets.penguins`
   LIMIT 10
   ```
7. 如要執行程式碼，請按下「Run cell」(執行儲存格)play\_circle。

### 使用 Gemini Cloud Assist 生成 Python 程式碼

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意事項：**如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [gemini-in-bigquery-feedback@google.com](mailto:gemini-in-bigquery-feedback@google.com)。

您可以在 Google Cloud 控制台使用 [Gemini Cloud Assist](https://docs.cloud.google.com/cloud-assist/overview?hl=zh-tw)，在 BigQuery 中生成 Python 程式碼。必須先啟用 Gemini Cloud Assist，才能透過 Gemini Cloud Assist 生成程式碼。詳情請參閱「[設定 Gemini Cloud Assist](https://docs.cloud.google.com/cloud-assist/set-up-gemini?hl=zh-tw)」的說明。

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器的分頁列中，點選「SQL 查詢」add\_box旁的下拉式箭頭 arrow\_drop\_down，然後點選「Notebook」(筆記本)。
3. 在 Google Cloud 工具列，點選 spark「Open or close Gemini AI chat」，開啟 Gemini Cloud Assist 對話。
4. 在「Enter a prompt」(輸入提示) 欄位輸入提示，以便生成 Python 程式碼。例如：

   ```
   Generate python code to query the `bigquery-public-data.ml_datasets.penguins`
   table using bigquery magics
   ```
5. 點選「傳送提示詞」按鈕 send。
   Gemini 會傳回類似下列的 Python 程式碼：

   ```
   %%bigquery
   SELECT *
   FROM `bigquery-public-data.ml_datasets.penguins`
   LIMIT 10
   ```
6. 查看生成的 Python 程式碼。
7. 如要執行 Python 程式碼，請點選 content\_copy「Copy to clipboard」(複製到剪貼簿)，將生成的程式碼貼到查詢編輯器，然後點選 play\_circle「Run」(執行)。

### 產生 BigQuery DataFrames 程式碼

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-notebook-python-gen-feedback@google.com](mailto:bq-notebook-python-gen-feedback@google.com)。

您可以使用 Gemini in BigQuery 生成 [BigQuery DataFrame](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw) 程式碼。如要請 Gemini 在生成的程式碼中使用 BigQuery DataFrame，請在提示中表達意圖。舉例來說，您可以從「使用 bigframes」或「利用 BigQuery DataFrames」開始提示。

BigQuery DataFrames 提供兩個程式庫：

* bigframes.pandas：提供與 pandas 相容的 API，用於資料分析。
* bigframes.ml，提供類似 scikit-learn 的機器學習 (ML) API。

Gemini 程式碼生成功能已針對 bigframes.pandas 程式庫進行最佳化。

如要進一步瞭解 BigQuery DataFrames，以及使用 BigQuery DataFrames 時所需的權限，請參閱「[BigQuery DataFrames 權限](https://docs.cloud.google.com/bigquery/docs/use-bigquery-dataframes?hl=zh-tw)」。BigQuery DataFrames 是開放原始碼套件。
您可以執行 `pip install --upgrade bigframes` 安裝最新版本。

在以下範例中，您會產生 BigQuery 公開資料集的程式碼 `bigquery-public-data.ml_datasets.penguins`。

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器的分頁列中，點選「SQL 查詢」add\_box旁的下拉式箭頭 arrow\_drop\_down，然後點選「Notebook」(筆記本)。

   系統會開啟新筆記本。
3. 如要插入新的程式碼儲存格，請在工具列中按一下「程式碼」add。
4. 新的程式碼儲存格會顯示「開始使用 AI 編寫或生成程式碼」訊息。
   在新的程式碼儲存格中，按一下「生成」。
5. 在「Generate」(生成) 編輯器中，輸入下列自然語言提示：

   ```
   Read the penguins table from the BigQuery public data using bigframes
   ```
6. 按下 `Enter` 鍵 (如使用 macOS 裝置，則按 `Return` 鍵)。

   建議的 Python 程式碼大致如下：

   ```
   import bigframes.pandas as bpd

   # Read the penguins table from the BigQuery public data using bigframes
   result = bpd.read_gbd("bigquery-public-data.ml_datasets.penguins")
   ```
7. 如要執行程式碼，請按下「Run cell」(執行儲存格)play\_circle。
8. 如要預覽結果，請在工具列中點按「程式碼」add，插入新的程式碼儲存格。
9. 在新儲存格中呼叫 `peek()` 方法 (例如 `result.peek()`)，然後按下 play\_circle「執行儲存格」。畫面上會顯示多列資料。

## 補全 Python 程式碼

Python 程式碼補全功能會嘗試根據查詢編輯器中的內容，提供符合情境的適當建議。在您輸入內容時，BigQuery 中的 Gemini 會根據目前程式碼的情境，建議合理的後續步驟，或協助您反覆調整程式碼。

如要使用 Gemini in BigQuery 的 Python 程式碼補全功能，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器的分頁列中，點選「SQL 查詢」add\_box旁的下拉式箭頭 arrow\_drop\_down，然後點選「Notebook」(筆記本)。

   系統會開啟新筆記本，其中包含的儲存格會顯示針對 `bigquery-public-data.ml_datasets.penguins` 公開資料集執行的查詢範例。
3. 在編輯器中開始輸入 Python 程式碼。例如 `%%bigquery`。Gemini in BigQuery 會在您輸入內容時，建議內嵌程式碼。
4. 如要接受建議，請按下 `Tab` 鍵。

## 說明 Python 程式碼

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以使用 Gemini in BigQuery 說明 Colab Enterprise 筆記本中的 Python 程式碼。

取得說明後，您可以在提示對話方塊中提出更多問題，以便進一步瞭解程式碼。

如要請 Gemini 說明筆記本中的 Python 程式碼，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要開啟的筆記本。
5. 醒目顯示要瞭解的 Python 儲存格。
6. 依序點選 spark「Gemini」和「說明程式碼」。

   程式碼說明會顯示在儲存格旁的面板中。
7. 選用：如要進一步瞭解程式碼，請在「在這裡輸入提示」欄位中提問。

## 修正及說明 Python 錯誤

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以使用 Gemini in BigQuery 修正及說明 Colab Enterprise 筆記本中的 Python 程式碼錯誤。

如要使用 Gemini 輔助功能修正或瞭解程式碼錯誤，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要開啟的筆記本。
5. 在筆記本的程式碼儲存格中輸入含有錯誤的程式碼，然後執行該儲存格。舉例來說，您可能會輸入 `print(1`，但缺少右括號。

   程式碼儲存格執行後，筆記本會在程式碼儲存格下方列印錯誤訊息。如果已在 Python 筆記本中啟用 Gemini，且 Gemini 建議修正或說明錯誤，系統會顯示下列其中一個選項：

   * 如果是 Python 語法錯誤，系統會顯示「修正錯誤」選項。
   * 如果是其他類型的錯誤，系統會顯示「說明錯誤」選項。
6. 如要修正語法錯誤，請按照下列步驟操作：

   1. 按一下「修正錯誤」。

      Gemini 會建議如何修正錯誤。
   2. 評估建議，然後執行下列任一操作：

      * 如要接受建議，請按一下「勾號」「接受建議」。
      * 如要拒絕建議，請依序點選「關閉」「拒絕建議」。
7. 如要修正所有其他類型的錯誤，請按照下列步驟操作：

   1. 按一下「說明錯誤」。

      系統會開啟面板，說明錯誤並建議變更。
   2. 選用：如要進一步瞭解錯誤，請在「在這裡輸入提示」欄位中提問。
   3. 如要接受建議的變更，請按一下
      library\_add
      「新增程式碼儲存格」。

## 生成 PySpark 程式碼

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以要求 Gemini Code Assist 在筆記本中生成 PySpark 程式碼。Gemini Code Assist 會擷取並使用相關的 BigQuery 和 Dataproc Metastore 資料表及其結構定義，生成程式碼回覆。Gemini Code Assist 具備結構定義知識，因此不會產生幻覺，還會建議彙整鍵和資料欄類型。

如要在筆記本中生成 Gemini Code Assist 程式碼，請按照下列步驟操作：

1. 點選工具列中的「+ Code」，插入新的程式碼儲存格。
   新的程式碼儲存格會顯示 `Start coding or generate with AI`。
   點選「生成」。
2. 在「生成」編輯器中輸入自然語言提示，然後按一下 `enter`。**請務必在提示中加入 `spark` 或 `pyspark` 關鍵字。**

   提示詞範例：

   ```
   create a spark dataframe from order_items and filter to orders created in 2024
   ```

   輸出內容範例：

   ```
   spark.read.format("bigquery").option("table", "sqlgen-testing.pysparkeval_ecommerce.order_items").load().filter("year(created_at) = 2024").createOrReplaceTempView("order_items")
   df = spark.sql("SELECT * FROM order_items")
   ```

### 使用 Gemini Code Assist 生成程式碼的提示

* 為了讓 Gemini Code Assist 擷取相關的資料表和結構定義，請為 Dataproc Metastore 執行個體啟用 [Data Catalog 同步處理功能](https://docs.cloud.google.com/dataproc-metastore/docs/data-catalog-sync?hl=zh-tw)。
* 為能順利查詢資料表，請確保使用者帳戶可以存取 Data Catalog，做法是指派 [`DataCatalog.Viewer` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw#datacatalog.viewer)。

## 關閉 Gemini 查詢輔助功能

如要關閉 Gemini in BigQuery 的特定功能，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery 工具列中，點選 pen\_sparkarrow\_drop\_down「Gemini」圖示。
3. 在清單中，移除要關閉的查詢輔助功能。

如要瞭解如何停用 Gemini in BigQuery，請參閱[停用 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw#turn-off)的相關說明。

## 停用 Gemini in Colab Enterprise

如要為 Google Cloud 專案停用 Gemini in Colab Enterprise，管理員必須停用 Gemini for Google Cloud API。詳情請參閱[停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw#disabling)的相關說明。

如要為特定使用者停用 Gemini in Colab Enterprise，管理員必須撤銷該名使用者的「Gemini for Google Cloud 使用者」(`roles/cloudaicompanion.user`) 角色。詳情請參閱[撤銷單一 IAM 角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#revoke-single-role)的相關說明。

## 提供意見回饋

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery 工具列中，點選 pen\_sparkarrow\_drop\_down「Gemini」圖示。
3. 按一下 [傳送意見]。

## 協助我們改良建議功能

您可以將提交至[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)功能的提示資料分享給 Google，協助我們提升 Gemini 建議的品質。

如要分享提示資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery 工具列中，點選 pen\_sparkarrow\_drop\_down「Gemini」圖示。
3. 選取「Share data to improve Gemini in BigQuery」(共用資料，協助改良 Gemini in BigQuery)。
4. 在「Data Use Settings」(資料使用設定) 對話方塊中，更新資料使用設定。

資料分享設定會套用至整個專案，且只有具備 `serviceusage.services.enable` 和 `serviceusage.services.list` IAM 權限的專案管理員能夠設定。如要進一步瞭解「早鳥測試者計畫」的資料使用方式，請參閱「[Gemini for Google Cloud 『早鳥測試者計畫』](https://cloud.google.com/trusted-tester/gemini-for-google-cloud-preview?hl=zh-tw)」。

## Gemini 和 BigQuery 資料

為提供準確的結果，Gemini in BigQuery 需要存取您儲存在 BigQuery 的[客戶資料](https://cloud.google.com/terms/data-processing-addendum?hl=zh-tw)和中繼資料，以便提供強化功能。詳情請參閱「[Gemini in BigQuery 如何使用您的資料](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw#data-usage)」。

## 位置

您可以在所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，使用 Gemini in BigQuery 輔助 SQL 和 Python 資料分析。如要瞭解 Gemini in BigQuery 在何處處理資料，請參閱「[Gemini in BigQuery 在何處處理資料](https://docs.cloud.google.com/bigquery/docs/gemini-locations?hl=zh-tw)」。

## 定價

如要瞭解這項功能的定價詳情，請參閱 [Gemini in BigQuery 定價總覽](https://cloud.google.com/products/gemini/pricing?hl=zh-tw#gemini-in-bigquery-pricing)。

## 後續步驟

* 閱讀 [Gemini for Google Cloud 總覽](https://docs.cloud.google.com/gemini/docs/overview?hl=zh-tw)。
* 瞭解 [Gemini for Google Cloud 如何使用您的資料](https://docs.cloud.google.com/gemini/docs/discover/data-governance?hl=zh-tw)。
* 瞭解如何[生成資料洞察以探索資料](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]