Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理工作負載承諾

透過 BigQuery Reservation API，您可以購買專屬運算單元 (稱為「[*承諾*](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」)、建立運算單元集區 (稱為「[*預留項目*](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」)，以及將專案、資料夾和機構指派給這些預留項目。

*容量使用承諾*是指購買 BigQuery 運算容量，但有最短承諾使用期。使用[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)建立預留項目時，您可以選擇是否購買容量承諾，但購買容量承諾可節省成本。

承諾是區域性資源。在某個區域或多區域購買的使用承諾，無法用於其他區域或多區域。使用承諾無法在區域之間移動，也無法在區域和多區域之間移動。承諾無法在專案之間轉移。

## 啟用 Reservations API

BigQuery Reservation API 與現有的 BigQuery API 不同，必須單獨啟用。詳情請參閱[啟用及停用 API](https://docs.cloud.google.com/apis/docs/getting-started?hl=zh-tw#enabling_apis)。

* API 名稱為「BigQuery Reservations API」
* BigQuery Reservation API 的端點為 `bigqueryreservation.googleapis.com`。

**注意：** 如要禁止貴機構中的使用者啟用 BigQuery Reservation API，請[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

## 購買承諾使用合約

如要預留容量一段時間，可以購買[容量使用承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)。這樣可享有折扣並節省費用。如要進一步瞭解具體費用，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」一文。

### 所需權限

如要建立容量承諾，您需要下列 Identity and Access Management (IAM) 權限：

* `bigquery.capacityCommitments.create`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 建立容量使用承諾

**注意：** 建立容量承諾前，請先瞭解[承諾方案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)和[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)的詳細資訊。

承諾是區域性資源。在某個區域或多區域購買的使用承諾無法用於其他區域或多區域。使用承諾無法在區域之間移動，也無法在區域和多區域之間移動。承諾無法在專案之間轉移。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「建立承諾」。
4. 在「設定」下方：

   1. 選取地點。
   2. 在「容量模型」部分，選取容量模型。
   3. 如果選取「自動調度資源 (版本)」選項：
      1. 從「Edition」(版本) 清單中選取版本。容量承諾僅適用於 Enterprise 和 Enterprise Plus 版本。
   4. 選取「承諾使用時間長度」，指定您的[承諾方案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)。
   5. 如果您購買**年約**，請選取**合約到期後要生效的續訂方案**：

      1. **每年續訂**。年約到期後，系統會自動續約一年。

      詳情請參閱「[預留配額承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」。
   6. 輸入要購買的**運算單元數量**。
   7. 點選「下一步」。
5. 查看預估的購買**費用**。
6. 在「確認並提交」下方：

   1. 輸入「CONFIRM」確認購買。
   2. 按一下「購買」即可購買運算單元。
7. 如要查看承諾使用合約，請按一下「查看運算單元使用承諾」。容量佈建完成後，所要求的容量使用承諾將會呈現綠色狀態。

   **注意：** 通常很快就能佈建位置，但有時可能需要數小時。如果您有重要工作負載，預期需求會增加，請至少提前一天預留運算單元。

首次購買容量時，系統會建立 `default` 保留項目。

### SQL

如要建立容量承諾，請使用 [`CREATE CAPACITY` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_capacity_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE CAPACITY
     `ADMIN_PROJECT_ID.region-LOCATION.COMMITMENT_ID`
   OPTIONS (
     slot_count = NUMBER_OF_SLOTS,
     edition = EDITION,
     plan = 'PLAN_TYPE',
     renewal_plan = 'RENEWAL_PLAN_TYPE');
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案將保有這項承諾的擁有權
   * `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `COMMITMENT_ID`：承諾 ID

     專案和位置中的名稱不得重複。開頭和結尾必須為小寫英文字母或數字，且只能包含小寫英文字母、數字和破折號。
   * `NUMBER_OF_SLOTS`：要購買的空位數量
   * `EDITION`：與容量承諾相關聯的版本。您只能透過 Enterprise 或 Enterprise Plus 版本建立容量承諾。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
   * `PLAN_TYPE`：[方案類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)。
     選項為 `ANNUAL` 或 `THREE_YEAR`。
   * `RENEWAL_PLAN_TYPE`：[續約方案類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#renew-commitments)。選項為 `NONE`、`ANNUAL` 或 `THREE_YEAR`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)並加上 [`--capacity_commitment` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-capacity-commitment)，即可購買位置。

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --capacity_commitment=true \
    --edition=EDITION \
    --plan=PLAN_TYPE \
    --renewal_plan=RENEWAL_PLAN_TYPE \
    --slots=NUMBER_OF_SLOTS
```

更改下列內容：

* `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案將保有這項承諾的擁有權
* `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `EDITION`：與容量承諾相關聯的版本。您只能透過 Enterprise 或 Enterprise Plus 版本建立容量承諾。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* `PLAN_TYPE`：[方案類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)。選項為 `ANNUAL` 或 `THREE_YEAR`。
* `RENEWAL_PLAN_TYPE`：[續約方案類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#renew-commitments)。選項為 `NONE`、`ANNUAL` 或 `THREE_YEAR`。
* `NUMBER_OF_SLOTS`：要購買的配額數量。

## 查看容量承諾

下列各節說明如何查看現有的容量承諾。

### 所需權限

如要查看約期，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.capacityCommitments.list`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`
* `BigQuery Resource Viewer`
* `BigQuery User`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 依專案查看容量使用承諾

如要依專案查看容量承諾，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元使用承諾」分頁標籤。容量使用承諾會列在「承諾」下方的表格中。

### SQL

如要查看管理專案的承諾，請查詢[`INFORMATION_SCHEMA.CAPACITY_COMMITMENTS_BY_PROJECT` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw#schema)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     capacity_commitment_id
   FROM
     `region-LOCATION`.INFORMATION_SCHEMA.CAPACITY_COMMITMENTS_BY_PROJECT
   WHERE
     project_id = 'ADMIN_PROJECT_ID'
     AND slot_count = 100;
   ```

   請替換下列項目：

   * `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `ADMIN_PROJECT_ID`：擁有承諾的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq ls` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_ls)，並加上 [`--capacity_commitment` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#ls-capacity_commitment-flag)，列出管理專案的約定。

```
bq ls \
    --capacity_commitment=true \
    --location=LOCATION \
    --project_id=ADMIN_PROJECT_ID
```

更改下列內容：

* `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `ADMIN_PROJECT_ID`：擁有承諾的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID

## 可更新容量使用承諾

您可以對容量承諾進行下列更新：

* 更新承諾使用合約的續約方案
* 將承諾轉換為使用期限較長的使用承諾合約方案。
* 將承諾使用合約分割為兩個承諾使用合約。
* 將兩份承諾使用合約合併為一份。

### 所需權限

如要更新容量承諾，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.capacityCommitments.update`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 續訂承諾使用合約

年約方案有續約計畫，您可以在建立或轉換為年約方案時指定。您可以在合約到期前隨時變更[年約續訂方案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#renew-commitments)。

### 控制台

如要變更年約的續約方案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下 [Slot commitments] (運算單元使用承諾) 分頁標籤。
4. 找出要編輯的約定。
5. 依序點按
   more\_vert
   「動作」，然後選取「編輯續約方案」選項。
6. 選取新的續訂方案。

### bq

如要變更年約方案的續約方案選項，請使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)，並加上 [`--capacity_commitment` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#update-capacity-commitment-flag)和 [`--renewal_plan` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#renewal_plan_flag)。

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --renewal_plan=PLAN_TYPE \
    --capacity_commitment=true \
    COMMITMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案將保有這項承諾的擁有權
* `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `PLAN_TYPE`：[方案類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)，例如 `ANNUAL` 或 `THREE_YEAR`。
* `COMMITMENT_ID`：承諾 ID

  如要取得 ID，請參閱「[查看已購買的承諾使用合約](#view-commitments)」。

### 將承諾使用合約轉換為較長期限

您隨時可以選擇將承諾轉換為較長期的承諾類型。即使您想從舊版方案轉換為版本，也能使用這項功能。

更新承諾後，系統會立即按照新方案的費率收費，並重設結束日期。

如要轉換約定，請使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)，並加上 [`--plan` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#update-plan-flag)。

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --plan=PLAN_TYPE \
    --renewal_plan=RENEWAL_PLAN \
    --capacity_commitment=true \
    COMMITMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `PLAN_TYPE`：[方案類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)，例如 `ANNUAL` 或 `THREE_YEAR`。
* `RENEWAL_PLAN`：[續約](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#renew-commitments)方案

  這項規定僅適用於 `PLAN_TYPE` 為 `ANNUAL` 的情況。
* `COMMITMENT_ID`：承諾 ID

  如要取得 ID，請參閱「[查看已購買的承諾使用合約](#view-commitments)」。

### 拆分承諾使用合約

您可以將承諾使用合約拆分為兩份。如果您想[續訂](#renewing-commitments)部分約期，這項功能就非常實用。舉例來說，如果您有 1,000 個運算單元的年度承諾，可以將 300 個運算單元分割到新的承諾，原承諾則保留 700 個運算單元。然後以年費率續訂 700 個名額，並將 300 個名額轉換為三年期方案。承諾的運算單元數量須為 50 的倍數。

分割承諾時，新承諾會採用與原始承諾相同的方案和承諾結束日期。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下 [Slot commitments] (運算單元使用承諾) 分頁標籤。
4. 選取要拆分的約定。
5. 按一下「分割」。
6. 在「Split commitment」(拆分承諾) 頁面中，使用「Configure split」(設定拆分) 滑桿，以 50 個運算單元為增量，選取要拆分到每個部分的運算單元數量。
7. 按一下「Split」(分割) 即可分割承諾。新承諾使用合約會列在「運算單元使用承諾」分頁中。

### bq

如要分割約期，請使用 `bq update` 指令。

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --split \
    --slots=SLOTS_TO_SPLIT \
    --capacity_commitment=true \
    COMMITMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `SLOTS_TO_SPLIT`：要從原始約期分割到新約期的配額數量
* `COMMITMENT_ID`：承諾 ID

  如要取得 ID，請參閱「[查看已購買的承諾使用合約](#view-commitments)」。

### 合併兩份承諾使用合約

您可以將多個約期合併為一個約期。合併的承諾使用合約必須屬於相同類型 (`ANNUAL` 或 `THREE_YEAR`)。合併後承諾使用合約的結束日期，是原始承諾使用合約中最晚的結束日期。如果任何承諾使用合約的結束日期較早，系統會將這些合約的結束日期延長至較晚的日期，並按比例收取這些時段的費用。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下 [Slot commitments] (運算單元使用承諾) 分頁標籤。
4. 選取要合併的承諾使用合約。
5. 按一下 [Merge] (合併)。
6. 在「合併承諾」頁面中，查看合併詳細資料，然後按一下「合併」。新的合併承諾使用合約會列在「運算單元承諾使用合約」分頁中。

### bq

如要將兩項約期合併為一項，請使用 `bq update` 指令：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --merge=true \
    --capacity_commitment=true \
    COMMITMENT1,COMMITMENT2
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：承諾的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `COMMITMENT1`：要合併的第一個承諾
* `COMMITMENT2`：要合併的第二個承諾

### 將承諾使用合約升級至新版本

您無法直接將約期方案升級至新版本。舉例來說，您無法將 Enterprise 版本的約期升級至 Enterprise Plus 版本。請改為按照下列步驟升級約期：

1. [建立新的承諾使用合約](#purchase-commitment)。選擇適當的升級版本。請注意，這項新承諾使用合約的結束日期與現有承諾使用合約不同。
2. [與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，要求取消現有約期。

## 承諾到期

承諾會在期限結束時失效。您無法刪除仍處於有效狀態的約期。如果續訂方案設為`NONE`，系統會自動刪除承諾。否則，系統會根據續約方案，以年約或三年約續約。如要將續約方案變更為 `NONE`，請按照「[續約承諾](#renewing-commitments)」中的步驟操作。

續約承諾後，「開始時間」的值不會變更。這是指原始承諾的開始時間。「結束時間」是續約承諾到期的時間。舉例來說，如果您在 2022 年 12 月 13 日建立一項年度約期，並在 2023 年 12 月 13 日續約。如果您在 2023 年 12 月 14 日查看約期詳細資料，**開始時間**的值會是 2022 年 12 月 13 日，**結束時間**的值會是 2024 年 12 月 12 日。

系統一律會收取基準運算單元費用。如果容量承諾使用合約到期，您可能需要手動調整預留項目中的基準運算單元數量，以免產生不必要的費用。舉例來說，假設您有 100 個運算單元的 1 年期承諾，以及 100 個基準運算單元的預訂。承諾使用合約到期，且沒有續約方案。承諾到期後，您需要以[即付即用費率](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)支付 100 個基準運算單元的費用。

## 控管容量使用承諾的建立作業

您可以透過 [IAM 拒絕政策](https://docs.cloud.google.com/iam/docs/deny-overview?hl=zh-tw)，進一步控管哪些使用者可以建立容量承諾。

您可以為一組使用者或所有使用者建立拒絕政策，並設定例外狀況和條件。

舉例來說，下列政策會拒絕所有使用者建立容量承諾的權限，但主體「lucian@example.com」除外：

```
{
  "deniedPrincipals": [
    "principalSet://goog/public:all"
  ],
  "deniedPermissions": [
    "bigquery.googleapis.com/capacityCommitments.create"
  ],
  "exceptionPrincipals": [
    "principal://goog/subject/lucian@example.com"
  ]
}
```

然後將這項政策附加至機構，控管可建立承諾的使用者。

請注意，這些政策的優先順序高於 IAM 角色，因此即使使用者具有 `bigquery.admin` 角色，除非刪除或修改政策，否則也無法建立承諾。

詳情請參閱「[拒絕存取資源](https://docs.cloud.google.com/iam/docs/deny-access?hl=zh-tw)」。

## 排解容量使用承諾問題

使用 BigQuery Reservations 遇到問題時，請參考本節的疑難排解步驟，或許有所助益。

### 購買的運算單元仍在處理中

運算單元是依據可用容量而定。如果您購買了運算單元承諾使用合約並透過 BigQuery 進行分配，「狀態」欄會顯示勾號。如果 BigQuery 無法立即分配要求的運算單元，則「狀態」欄會持續顯示待處理狀態。您可能必須等待數小時，直到有可用的運算單元釋出。如需提早取得空位，請嘗試下列做法：

1. 刪除待處理的承諾使用合約。
2. 購買運算單元數量較少的新承諾使用合約。視容量而定，較小的承諾可能會立即生效。
3. 以個別承諾購買剩餘的運算單元。這些運算單元可能會在「狀態」欄中顯示為待處理，但通常會在幾小時內啟用。
4. 選用：如果兩項承諾合約都適用，只要您為兩者購買相同方案，即可[合併](#merging-commitments)為單一承諾合約。

如果建立或完成時段承諾失敗或耗時過長，請考慮暫時使用[隨選價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。使用這項解決方案時，您可能需要在未指派給任何預留項目的其他專案中執行重要查詢，或是完全移除專案指派。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]