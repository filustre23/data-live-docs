Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery 專用的 Simba ODBC 和 JDBC 驅動程式

BigQuery 專用的 Simba Open Database Connectivity (ODBC) 和 Java Database Connectivity (JDBC) 驅動程式可將應用程式連線至 BigQuery，讓您透過偏好的工具和基礎架構使用 BigQuery 功能。一般來說，JDBC 驅動程式用於 Java 應用程式，ODBC 驅動程式則用於其他應用程式。

Simba ODBC 和 JDBC 驅動程式是由 [insightsoftware](https://insightsoftware.com/simba/) 開發，這家公司是 [Google Cloud Ready - BigQuery 合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-overview?hl=zh-tw)。除了 Simba JDBC 驅動程式，您也可以使用[Google 開發的 BigQuery JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/jdbc-for-bigquery?hl=zh-tw)，目前為[搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。

## 限制

BigQuery 專用的 Simba ODBC 和 JDBC 驅動程式有下列限制：

* 不支援 [BigQuery 載入功能](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 不支援 [BigQuery Export 功能](https://docs.cloud.google.com/bigquery/docs/export-intro?hl=zh-tw)。
* 系統不支援[查詢前置字串](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw#sql)。
* 所有[資料操縱語言 (DML) 限制](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml-limitations)均適用。
* [參數化查詢](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)只會提供查詢驗證，查詢效能不受影響。
* 這些驅動程式專為 BigQuery 設計，無法用於其他產品或服務。

## 事前準備

使用 BigQuery 專用的 Simba ODBC 和 JDBC 驅動程式時，您可以選擇使用 BigQuery Storage Read API 讀取資料，而非標準的 BigQuery API。在 insightsoftware 說明文件中，這項功能稱為「高輸送量 API」。如要使用這項選用功能，請確認您具備[必要角色](#high-throughput-roles)。

### 高輸送量 API 的必要角色

如要取得使用高處理量 API 的必要權限，請要求系統管理員授予您 BigQuery 專案的「BigQuery 讀取工作階段使用者」 (`roles/bigquery.readSessionUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用 High-Throughput API 所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用高輸送量 API，必須具備下列權限：

* `resourcemanager.projects.get`
* `resourcemanager.projects.list`
* `bigquery.readsessions.create`
* `bigquery.readsessions.getData`
* `bigquery.readsessions.update`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 安裝及設定 BigQuery 專用的 Simba ODBC 驅動程式

1. 根據所用的作業系統下載 3.1.6.3037 版驅動程式：

   * [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.1.6.3037.msi) (`.msi` 檔案)
   * [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.1.6.3037.msi) (`.msi` 檔案)
   * [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.1.6.3037-Linux.tar.gz) (`.tar.gz` 檔案)
   * [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.1.6.3037.dmg) (`.dmg` 檔案)
2. 請按照[insightsoftware 安裝與設定指南](https://storage.googleapis.com/simba-bq-release/odbc/Simba%20Google%20BigQuery%20ODBC%20Connector%20Install%20and%20Configuration%20Guide-3.1.6.3037.pdf)中的操作說明進行。

如要瞭解功能異動和工作流程更新，請參閱 [Simba Google BigQuery ODBC 資料連接器版本資訊](https://storage.googleapis.com/simba-bq-release/odbc/release-notes-3.1.6.3037.txt)。

如要查看先前的驅動程式版本清單，請展開下列部分：

### 舊版 Simba ODBC 驅動程式

#### 3.1.6.1026

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.1.6.1026.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.1.6.1026.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.1.6.1026-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.1.6.1026.dmg)

#### 3.1.5.1022

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.1.5.1022.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.1.5.1022.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.1.5.1022-Linux.tar)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.1.5.1022.dmg)

#### 3.1.4.1020

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.1.4.1020.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.1.4.1020.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.1.4.1020-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.1.4.1020.dmg)

#### 3.1.2.1009

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.1.2.1009.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.1.2.1009.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.1.2.1009-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.1.2.1009.dmg)

#### 3.1.2.1004

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.1.2.1004.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.1.2.1004.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.1.2.1004-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.1.2.1004.dmg)

#### 3.0.7.1016

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.0.7.1016.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.0.7.1016.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.0.7.1016-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.0.7.1016.dmg)

#### 3.0.5.1011

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.0.5.1011.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.0.5.1011.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.0.5.1011-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.0.5.1011.dmg)

#### 3.0.4.1008

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.0.4.1008.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.0.4.1008.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.0.4.1008-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.0.4.1008.dmg)

#### 3.0.3.1006

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.0.3.1006.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.0.3.1006.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.0.3.1006-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.0.3.1006.dmg)

#### 3.0.2.1005

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.0.2.1005.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.0.2.1005.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.0.2.1005-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.0.2.1005.dmg)

#### 3.0.0.1001

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_3.0.0.1001.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_3.0.0.1001.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.0.0.1001-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-3.0.0.1001.dmg)

#### 2.5.2.1004

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.5.2.1004.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.5.2.1004.msi))
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.5.2.1004-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.5.2.1004.dmg)

#### 2.5.0.1001

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.5.0.1001.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.5.0.1001.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.5.0.1001-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.5.0.1001.dmg)

#### 2.4.6.1015

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.4.6.1015.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.4.6.1015.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.4.6.1015-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.4.6.1015.dmg)

#### 2.4.5.1014

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.4.5.1014.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.4.5.1014.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.4.5.1014-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.4.5.1014.dmg)

#### 2.4.3.1012

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.4.3.1012.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.4.3.1012.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.4.3.1012-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.4.3.1012.dmg)

#### 2.4.1.1009

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.4.1.1009.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.4.1.1009.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.4.1.1009-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.4.1.1009.dmg)

#### 2.4.0.1002

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.4.0.1002.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.4.0.1002.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.4.0.1002-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.4.0.1002.dmg)

#### 2.3.5.1009

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.3.5.1009.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.3.5.1009.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.3.5.1009-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.3.5.1009.dmg)

#### 2.3.3.1005

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.3.3.1005.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.3.3.1005.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.3.3.1005-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.3.3.1005.dmg)

#### 2.3.2.1003

* [Windows 32 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery32_2.3.2.1003.msi)
* [Windows 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery64_2.3.2.1003.msi)
* [Linux 32 位元和 64 位元](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_2.3.2.1003-Linux.tar.gz)
* [macOS](https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery-2.3.2.1003.dmg)

## 安裝及設定 BigQuery 專用的 Simba JDBC 驅動程式

**注意：** 除了 Simba JDBC 驅動程式，[Google 開發的 BigQuery 專用 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/jdbc-for-bigquery?hl=zh-tw)也已推出[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。

1. 下載[驅動程式 1.7.0.1001 版](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.7.0.1001.zip)。
2. 請按照[insightsoftware 安裝與設定指南](https://storage.googleapis.com/simba-bq-release/jdbc/Simba%20Google%20BigQuery%20JDBC%20Connector%20Install%20and%20Configuration%20Guide_1.7.0.1001.pdf)中的操作說明進行。

如要瞭解功能異動和工作流程更新，請參閱「[Simba Google BigQuery JDBC 資料連接器版本資訊](https://storage.googleapis.com/simba-bq-release/jdbc/release-notes_1.7.0.1001.txt)」。

如要查看先前的驅動程式版本清單，請展開下列部分：

### 舊版 Simba JDBC 驅動程式

* [1.6.5.1002](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.6.5.1002.zip)
* [1.6.5.1001](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.6.5.1001.zip)
* [1.6.3.1004](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.6.3.1004.zip)
* [1.6.2.1003](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.6.2.1003.zip)
* [1.6.1.1002](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.6.1.1002.zip)
* [1.5.4.1008](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.5.4.1008.zip)
* [1.5.0.1001](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.5.0.1001.zip)
* [1.3.3.1004](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.3.3.1004.zip)
* [1.3.2.1003](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaBigQueryJDBC42-1.3.2.1003.zip)
* [1.3.0.1001](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.3.0.1001.zip)
* [1.2.25.1029](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.25.1029.zip)
* [1.2.23.1027](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.23.1027.zip)
* [1.2.22.1026](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.22.1026.zip)
* [1.2.21.1025](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.21.1025.zip)
* [1.2.19.1023](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.19.1023.zip)
* [1.2.18.1022](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.18.1022.zip)
* [1.2.16.1020](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.16.1020.zip)
* [1.2.14.1017](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.14.1017.zip)
* [1.2.1.1001 (與 JDBC 4.2 相容)](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.1.1001.zip)
* [1.2.1.1001 (與 JDBC 4.1 相容)](https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery41_1.2.1.1001.zip)

## 支援

如需 BigQuery 的 Simba ODBC 和 JDBC 驅動程式支援，請透過標準 [Cloud Customer Care](https://docs.cloud.google.com/bigquery/support?hl=zh-tw)管道取得協助。

## 定價

您可以免費下載 BigQuery 專用的 Simba ODBC 和 JDBC 驅動程式，而且使用這些驅動程式時不需要任何額外授權。不過，使用驅動程式時，適用下列 BigQuery 價格：

* 您執行的查詢[運算價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#compute-pricing-models)。
* 如果驅動程式設定為將大型結果集寫入目的地資料表，則需按[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage-pricing)支付費用。
* 如果驅動程式使用 High-Throughput API 功能，讀取大型結果集資料時，會套用 [BigQuery Storage Read API 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data-extraction-pricing)。

## 後續步驟

* 進一步瞭解 [Google 開發的 BigQuery JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/jdbc-for-bigquery?hl=zh-tw)。
* 探索其他 [BigQuery 開發人員工具](https://docs.cloud.google.com/bigquery/docs/developer-overview?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-22 (世界標準時間)。"],[],[]]