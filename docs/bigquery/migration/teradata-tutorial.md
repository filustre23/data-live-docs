Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Teradata 遷移至 BigQuery 的教學課程

本文說明如何使用範例資料，從 Teradata [遷移至 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)。這份概念驗證文件將逐步說明如何將結構定義與資料從 Teradata 資料倉儲轉移到 BigQuery。

## 目標

* 產生合成資料並上傳到 Teradata。
* 使用 BigQuery 資料移轉服務 (BQDT)，將結構定義遷移與資料移轉至 BigQuery。
* 驗證在 Teradata 和 BigQuery 上傳回的查詢結果是否相同。

## 費用

本快速入門導覽課程使用下列 Google Cloud計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)：
  本教學課程在一次執行多個查詢時，會將大約 1 GB 的資料儲存在 BigQuery 中，且處理的資料量不到 2 GB。在Google Cloud 免費方案下，使用者可免費使用一定限度的部分 BigQuery 資源。無論免費試用期是否已結束，只要未超過用量限制就能免費使用特定資源。免費試用期過後，如果您超過用量限制，系統會根據「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」頁面列出的價格，向您收取費用。

您可以使用 [Pricing Calculator](https://cloud.google.com/products/calculator/?hl=zh-tw#id=ecd64128-f174-4af5-a383-040946a8240f)，根據您的預測使用量產生預估費用。

## 必要條件

* 確認您擁有機器上的寫入權限和執行權限，且機器可連上網際網路，以便讓您下載並執行資料產生工具。
* 確認可連線至 Teradata 資料庫。
* 確認機器已安裝 Teradata [BTEQ](https://docs.teradata.com/reader/jmAxXLdiDu6NiyjT6hhk7g/%7EHy5lbZSS5zSwwnQv7yRWg) 和 [FastLoad](https://docs.teradata.com/reader/r_6Z4JwVMhANtZFCIKEx7Q/p2GqlZ6YH6kXoLLWJn2eQA) 用戶端工具。可從 [Teradata 網站](https://downloads.teradata.com/download/tools)取得 Teradata 用戶端工具。如需安裝上述工具的相關協助，請聯絡您的系統管理員，瞭解安裝、設定和執行的詳細資料。您也可以執行下列操作，做為 BTEQ 的補充或替代方式：

  + 安裝具備圖形介面的工具，例如 [DBeaver](https://dbeaver.io/)。
  + 安裝 [Teradata SQL Driver for Python](https://downloads.teradata.com/download/connectivity/teradata-sql-driver-for-python)，編寫與 Teradata 資料庫之間的互動指令碼。
* 確認機器與Google Cloud 之間具有網路連線，如此 BigQuery 資料移轉服務代理程式才能與 BigQuery 通訊，並轉移結構定義與資料。

**注意：** 結構定義與資料的遷移操作說明於另一個教學課程中提供，本文稍後會加以說明，並提供該課程的連結。

## 簡介

本快速入門導覽課程將逐步說明遷移作業的概念驗證。在這個課程中，我們會教您如何產生合成資料，並將資料載入 Teradata。接下來再使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將結構定義和資料移至 BigQuery。最後需在兩邊執行查詢，比較查詢結果。結束狀態則是來自 Teradata 的結構定義與資料，會一對一對應至 BigQuery。

本快速入門導覽課程的對象，主要是有意使用 BigQuery 資料移轉服務遷移結構定義與資料，而且想要實作體驗的資料倉儲系統管理員、開發人員與資料從業人員。

## 產生資料

[交易處理效能委員會](http://www.tpc.org) (TPC) 是公開發表基準化規範的非營利組織。這些規範已成為資料相關基準測試的現行業界標準。

[TPC-H 規範](http://www.tpc.org/tpch/default5.asp)是一項以決策支援為主的基準。在本快速入門導覽課程中，會運用到此規範的部分，以建立資料表和產生合成資料，做為實際資料倉儲的模型。雖然該規範是為了基準化而設，但您在本快速入門導覽課程中，必須將此模型當做遷移概念驗證的一環，而非用於基準化工作。

1. 在用來連線至 Teradata 的電腦上，透過網路瀏覽器從 [TPC 網站](http://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp)下載最新版 TPC-H 工具。
2. 開啟指令終端機，變更為下載工具的目的地目錄。
3. 將下載的 ZIP 檔案解壓縮，將 file-name 更改為已下載檔案的名稱：

   ```
   unzip file-name.zip
   ```

   解壓縮的內容是名稱中含有工具版本編號的目錄。
   此目錄內含 DBGEN 資料產生工具的 TPC 原始碼，以及 TPC-H 規範。
4. 前往 `dbgen` 子目錄。使用與您的版本對應的父項目錄名稱，如以下範例所示：

   ```
   cd 2.18.0_rc2/dbgen
   ```
5. 使用提供的範本建立 makefile：

   ```
   cp makefile.suite makefile
   ```
6. 以文字編輯器編輯 makefile，例如使用 vi 來編輯檔案：

   ```
   vi makefile
   ```
7. 在 makefile 中，變更下列變數的值：

   ```
   CC       = gcc
   # TDAT -> TERADATA
   DATABASE = TDAT
   MACHINE  = LINUX
   WORKLOAD = TPCH
   ```

   C 編譯器 (`CC`) 或 `MACHINE` 的值可能因環境而異。如有需要，請洽詢您的系統管理員。
8. 儲存變更並關閉檔案。
9. 處理 makefile：

   ```
   make
   ```
10. 使用 `dbgen` 工具產生 TPC-H 資料：

    ```
    dbgen -v
    ```

    資料產生工作需要幾分鐘時間完成。`-v` (詳細資訊) 旗標可讓指令回報進度。資料產生完畢後，您會在目前的資料夾內看到 8 個 ASCII 檔案，副檔名稱為 `.tbl`。檔案內含以垂直線符號分隔的合成資料，需載入至各個 TPC-H 資料表內。

## 將範例資料上傳至 Teradata

在本節中，您需將產生的資料上傳到 Teradata 資料庫。

### 建立 TPC-H 資料庫

Teradata 用戶端名稱為 [Basic Teradata Query (BTEQ)](https://docs.teradata.com/reader/jmAxXLdiDu6NiyjT6hhk7g/%7EHy5lbZSS5zSwwnQv7yRWg)，用來與一或多個 Teradata 資料庫伺服器通訊，並在這些系統上執行 SQL 查詢。在本節中，您需使用 BTEQ 為 TPC-H 資料表建立新資料庫。

1. 開啟 Teradata BTEQ 用戶端：

   ```
   bteq
   ```
2. 登入 Teradata。將 teradata-ip 和 teradata-user 替換為您環境的對應值。

   ```
   .LOGON teradata-ip/teradata-user
   ```
3. 建立名稱為 `tpch` 的資料庫，分配 2 GB 的空間：

   ```
   CREATE DATABASE tpch
   AS PERM=2e+09;
   ```
4. 結束 BTEQ：

   ```
   .QUIT
   ```

### 載入產生的資料

在本節中，您需建立用於建立和載入範例資料表的 FastLoad 指令碼。[TPC-H 規範](http://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-h_v2.18.0.pdf)第 1.4 節有列出資料表定義。第 1.2 節則提供了整個資料庫結構定義的實體關係圖。

以下程序示範如何建立 `lineitem` 資料表，這是最大也最複雜的 TPC-H 資料表。`lineitem` 資料表處理完畢後，請重複此程序，繼續建立其他的資料表。

1. 使用文字編輯器建立名為 `fastload_lineitem.fl` 的新檔案：

   ```
   vi fastload_lineitem.fl
   ```
2. 將下列指令碼貼到檔案中，該檔案會連線到 Teradata 資料庫，並建立名稱為 `lineitem` 的資料表。

   在 `logon` 指令中，將 teradata-ip、teradata-user 和 teradata-pwd 替換為您的連線詳細資料。

   ```
   logon teradata-ip/teradata-user,teradata-pwd;

   drop table tpch.lineitem;
   drop table tpch.error_1;
   drop table tpch.error_2;

   CREATE multiset TABLE tpch.lineitem,
       NO FALLBACK,
       NO BEFORE JOURNAL,
       NO AFTER JOURNAL,
       CHECKSUM = DEFAULT,
       DEFAULT MERGEBLOCKRATIO
       (
        L_ORDERKEY INTEGER NOT NULL,
        L_PARTKEY INTEGER NOT NULL,
        L_SUPPKEY INTEGER NOT NULL,
        L_LINENUMBER INTEGER NOT NULL,
        L_QUANTITY DECIMAL(15,2) NOT NULL,
        L_EXTENDEDPRICE DECIMAL(15,2) NOT NULL,
        L_DISCOUNT DECIMAL(15,2) NOT NULL,
        L_TAX DECIMAL(15,2) NOT NULL,
        L_RETURNFLAG CHAR(1) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        L_LINESTATUS CHAR(1) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        L_SHIPDATE DATE FORMAT 'yyyy-mm-dd' NOT NULL,
        L_COMMITDATE DATE FORMAT 'yyyy-mm-dd' NOT NULL,
        L_RECEIPTDATE DATE FORMAT 'yyyy-mm-dd' NOT NULL,
        L_SHIPINSTRUCT CHAR(25) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        L_SHIPMODE CHAR(10) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        L_COMMENT VARCHAR(44) CHARACTER SET LATIN CASESPECIFIC NOT NULL)
   PRIMARY INDEX ( L_ORDERKEY )
   PARTITION BY RANGE_N(L_COMMITDATE BETWEEN DATE '1992-01-01'
                                    AND     DATE '1998-12-31'
                  EACH INTERVAL '1' DAY);
   ```

   該指令碼可確實防止出現 `lineitem` 資料表和臨時錯誤資料表，並繼續建立 `lineitem` 資料表。
3. 在同個檔案中加入下列程式碼，該程式碼會將資料載入新建的資料表。請填妥三個區塊 (`define`、`insert` 和 `values`) 的所有資料表欄位，並確定您是以 `varchar` 做為這些項目的載入資料類型。

   ```
   begin loading tpch.lineitem
   errorfiles tpch.error_1, tpch.error_2;
    set record vartext;
   define
    in_ORDERKEY(varchar(50)),
    in_PARTKEY(varchar(50)),
    in_SUPPKEY(varchar(50)),
    in_LINENUMBER(varchar(50)),
    in_QUANTITY(varchar(50)),
    in_EXTENDEDPRICE(varchar(50)),
    in_DISCOUNT(varchar(50)),
    in_TAX(varchar(50)),
    in_RETURNFLAG(varchar(50)),
    in_LINESTATUS(varchar(50)),
    in_SHIPDATE(varchar(50)),
    in_COMMITDATE(varchar(50)),
    in_RECEIPTDATE(varchar(50)),
    in_SHIPINSTRUCT(varchar(50)),
    in_SHIPMODE(varchar(50)),
    in_COMMENT(varchar(50))
    file = lineitem.tbl;
   insert into tpch.lineitem (
     L_ORDERKEY,
     L_PARTKEY,
     L_SUPPKEY,
     L_LINENUMBER,
     L_QUANTITY,
     L_EXTENDEDPRICE,
     L_DISCOUNT,
     L_TAX,
     L_RETURNFLAG,
     L_LINESTATUS,
     L_SHIPDATE,
     L_COMMITDATE,
     L_RECEIPTDATE,
     L_SHIPINSTRUCT,
     L_SHIPMODE,
     L_COMMENT
   ) values (
     :in_ORDERKEY,
     :in_PARTKEY,
     :in_SUPPKEY,
     :in_LINENUMBER,
     :in_QUANTITY,
     :in_EXTENDEDPRICE,
     :in_DISCOUNT,
     :in_TAX,
     :in_RETURNFLAG,
     :in_LINESTATUS,
     :in_SHIPDATE,
     :in_COMMITDATE,
     :in_RECEIPTDATE,
     :in_SHIPINSTRUCT,
     :in_SHIPMODE,
     :in_COMMENT
   );
   end loading;
   logoff;
   ```

   FastLoad 指令碼會從同個目錄 (名稱為 `lineitem.tbl`) 中的檔案載入資料，亦即您在上一節產生的資料。
4. 儲存變更並關閉檔案。
5. 執行 FastLoad 指令碼：

   ```
   fastload < fastload_lineitem.fl
   ```
6. 請對 TPC-H 規範第 1.4 節列出的其他 TPC-H 資料表重複進行此程序。請務必依資料表調整步驟。

## 將結構定義與資料遷移至 BigQuery

如需如何將結構定義和資料遷移至 BigQuery 的操作說明，請參閱「[從 Teradata 遷移資料](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)」教學課程。
本節將詳細介紹如何進行該教學課程的特定步驟。完成另一篇教學課程的步驟後，請回到本文繼續進行下一節：[驗證查詢結果](#verifying_query_results)。

**注意：** 您將在 [Cloud Shell](https://console.cloud.google.com/cloudshell?hl=zh-tw) 中執行本節的所有指令。

### 建立 BigQuery 資料集

在進行初始 Google Cloud 設定步驟時，系統會請您在 BigQuery 中建立一個資料集，放置遷移過來的資料表。將資料集命名為 `tpch`。本快速入門導覽課程結尾的查詢將使用此名稱，您不需進行任何修改。

```
# Use the bq utility to create the dataset
bq mk --location=US tpch
```

### 建立服務帳戶

此外，您還必須在 Google Cloud 設定步驟中建立一個 Identity and Access Management (IAM) 服務帳戶。此服務帳戶用於將資料寫入 BigQuery，並將暫存資料儲存在 [Cloud Storage](https://docs.cloud.google.com/storage?hl=zh-tw) 中。

```
# Set the PROJECT variable
export PROJECT=$(gcloud config get-value project)

# Create a service account
gcloud iam service-accounts create tpch-transfer
```

授予權限給服務帳戶，讓服務帳戶管理 BigQuery 資料集和 Cloud Storage 中的暫存區。

```
# Set TPCH_SVC_ACCOUNT = service account email
export TPCH_SVC_ACCOUNT=tpch-transfer@${PROJECT}.iam.gserviceaccount.com

# Bind the service account to the BigQuery Admin role
gcloud projects add-iam-policy-binding ${PROJECT} \
    --member serviceAccount:${TPCH_SVC_ACCOUNT} \
    --role roles/bigquery.admin

# Bind the service account to the Storage Admin role
gcloud projects add-iam-policy-binding ${PROJECT} \
    --member serviceAccount:${TPCH_SVC_ACCOUNT} \
    --role roles/storage.admin
```

### 建立暫存 Cloud Storage 值區

Google Cloud 設定中的另一項工作是建立 Cloud Storage bucket。BigQuery 資料移轉服務會使用這個值區做為暫存區，放置欲擷取至 BigQuery 的資料。

```
# Use gcloud storage to create the bucket
gcloud storage buckets create gs://${PROJECT}-tpch --location=us-central1
```

### 指定資料表名稱模式

在 BigQuery 資料移轉服務的新移轉作業設定期間，系統會要求您指定一個運算式，指明要加入移轉作業的資料表。在本快速入門導覽課程中，請加入 `tpch` 資料庫中的所有資料表。

運算式的格式為 *`database`*.*`table`*，可用萬用字元取代資料表名稱。Java 的萬用字元開頭為兩個句點 (.)，因此移轉 `tpch` 資料庫中所有資料表的運算式如下所示：

```
tpch..*
```

請注意，當中有兩個點。

## 驗證查詢結果

在這個階段，您已經依照各個教學課程的說明建立了範例資料、將資料上傳到 Teradata，也使用了 BigQuery 資料移轉服務將資料遷移至 BigQuery。在本節中，您需執行兩項 TPC-H 標準查詢，驗證 Teradata 和 BigQuery 中的結果是否相同。

### 執行價格摘要報告查詢

第一個查詢是價格摘要報告查詢 (TPC-H 規範第 2.4.1 節)。此查詢會回報截至指定日期止，已開立帳單、出貨和退貨的項目數量。

完整查詢如下：

```
SELECT
 l_returnflag,
 l_linestatus,
 SUM(l_quantity) AS sum_qty,
 SUM(l_extendedprice) AS sum_base_price,
 SUM(l_extendedprice*(1-l_discount)) AS sum_disc_price,
 SUM(l_extendedprice*(1-l_discount)*(1+l_tax)) AS sum_charge,
 AVG(l_quantity) AS avg_qty,
 AVG(l_extendedprice) AS avg_price,
 AVG(l_discount) AS avg_disc,
 COUNT(*) AS count_order
FROM tpch.lineitem
WHERE l_shipdate BETWEEN '1996-01-01' AND '1996-01-10'
GROUP BY
 l_returnflag,
 l_linestatus
ORDER BY
 l_returnflag,
 l_linestatus;
```

在 Teradata 中執行查詢：

1. 執行 BTEQ 並連線至 Teradata。詳情請參閱本文前段的「[建立 TPC-H 資料庫](#heading=h.gecocvk60w6h)」一節。
2. 將輸出顯示寬度變更為 500 字元。