* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 Colab 筆記本將地理空間分析資料視覺化 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您將使用 Colab 筆記本，以視覺化方式呈現 BigQuery 中的地理空間分析資料。

本教學課程使用下列 BigQuery [公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)：

* [舊金山 Ford GoBike Share](https://console.cloud.google.com/bigquery(cameo:product/san-francisco-public-data/sf-bike-share)?hl=zh-tw)
* [舊金山社區](https://console.cloud.google.com/bigquery?ws=%211m4%211m3%213m2%211sbigquery-public-data%212ssan_francisco_neighborhoods&hl=zh-tw)
* [舊金山警察局 (SFPD) 報告](https://console.cloud.google.com/bigquery(cameo:product/san-francisco-public-data/sfpd-reports)?hl=zh-tw)

如要瞭解如何存取這些公開資料集，請參閱[在 Google Cloud 控制台中存取公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw#public-ui)。

您可以使用公開資料集建立下列圖表：

* Ford GoBike Share 資料集的所有共享單車站點**散佈圖**
* 舊金山鄰里資料集中的**多邊形**
* 按社區劃分的共享單車租借站數量**等值線地圖**
* 舊金山警察局報告資料集的事件**熱度圖**

## 目標

* 使用 Google Cloud 設定驗證，也可以選擇使用 Google 地圖。
* 在 BigQuery 中查詢資料，並將結果下載至 Colab。
* 使用 Python 資料科學工具執行轉換和分析。
* 建立視覺化圖表，包括散布圖、多邊形、等值線圖和熱度圖。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Google Maps Platform](https://mapsplatform.google.com/pricing/?hl=zh-tw)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery and Google Maps JavaScript APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cmaps-backend.googleapis.com&hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery and Google Maps JavaScript APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cmaps-backend.googleapis.com&hl=zh-tw)

1. 請確認您具備[必要權限](#required_permissions)，可執行本文件中的工作。

### 必要的角色

如果您建立新專案，您就是專案擁有者，並會獲得完成本教學課程所需的所有 IAM 權限。

如果您使用現有專案，需要下列專案層級角色才能執行查詢工作。

請確認您在專案中具備下列角色：

* [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser) (`roles/bigquery.user`)

#### 檢查角色

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
2. 選取專案。
3. 在「主體」欄中，找出所有識別您或您所屬群組的資料列。如要瞭解自己所屬的群組，請與管理員聯絡。
4. 針對指定或包含您的所有列，請檢查「角色」欄，確認角色清單是否包含必要角色。


#### 授予角色

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
2. 選取專案。
3. 按一下person\_add「Grant access」(授予存取權)。
4. 在「New principals」(新增主體) 欄位中，輸入您的使用者 ID。 這通常是指 Google 帳戶的電子郵件地址。
5. 按一下「選取角色」，然後搜尋角色。
6. 如要授予其他角色，請按一下add「Add another role」(新增其他角色)，然後新增其他角色。
7. 按一下「Save」(儲存)。

如要進一步瞭解 BigQuery 中的角色，請參閱「[預先定義的 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)」。

## 建立 Colab 筆記本

本教學課程會建立 Colab 筆記本，以視覺化方式呈現地理空間分析資料。如要在 Colab、Colab Enterprise 或 BigQuery Studio 中開啟筆記本的預先建構版本，請按一下教學課程 GitHub 版本頂端的連結：[在 Colab 中進行 BigQuery 地理空間資料視覺化](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/notebooks/bigquery_geospatial_visualization.ipynb)。

1. 開啟 Colab。

   [開啟 Colab](https://colab.research.google.com/?hl=zh-tw)
2. 在「開啟筆記本」對話方塊中，按一下「新增筆記本」。
3. 按一下 `Untitled0.ipynb`，然後將筆記本名稱變更為 **`bigquery-geo.ipynb`**。
4. 依序選取「檔案」**>「儲存」**。

## 使用 Google Cloud 和 Google 地圖進行驗證

本教學課程會查詢 BigQuery 資料集，並使用 Google 地圖 JavaScript API。如要使用這些資源，請透過 Google Cloud 和 Maps API 驗證 Colab 執行階段。

**注意：** 您可以自由選擇是否使用 Google Maps API。您可以在不使用 Google Maps JavaScript API 的情況下，執行本教學課程中的程式碼。

### 透過 Google Cloud驗證

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要使用專案進行驗證，請輸入下列程式碼：

   ```
   # REQUIRED: Authenticate with your project.
   GCP_PROJECT_ID = "PROJECT_ID"  #@param {type:"string"}

   from google.colab import auth
   from google.colab import userdata

   auth.authenticate_user(project_id=GCP_PROJECT_ID)

   # Set GMP_API_KEY to none
   GMP_API_KEY = None
   ```

   將 PROJECT\_ID 替換為專案 ID。
3. 按一下「執行儲存格」play\_circle\_filled。
4. 出現提示時，請按一下「允許」，同意授予 Colab 憑證存取權。
5. 在「使用 Google 帳戶登入」頁面中，選擇您的帳戶。
6. 在「Sign in to Third-party authored notebook code」(登入第三方撰寫的筆記本程式碼) 頁面中，按一下「Continue」(繼續)。
7. 在「選取第三方撰寫的筆記本程式碼可存取哪些項目」頁面，按一下「全選」，然後點選「繼續」。

   完成授權流程後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。

### 選用：透過 Google 地圖驗證

如果您使用 Google 地圖平台做為基本地圖的地圖供應商，請務必提供 Google 地圖平台 API 金鑰。筆記本會從 Colab 密鑰擷取金鑰。

只有在使用 Maps API 時才需要執行這個步驟。如果沒有透過 Google 地圖平台進行驗證，`pydeck` 會改用 `carto` 地圖。

1. 按照 Google 地圖說明文件「[使用 API 金鑰](https://developers.google.com/maps/documentation/javascript/get-api-key?hl=zh-tw#create-api-keys)」頁面的操作說明，取得 Google Maps API 金鑰。
2. 切換至 Colab 筆記本，然後按一下「密碼」vpn\_key。
3. 按一下「新增密碼」。
4. 在「Name」(名稱) 中輸入 **`GMP_API_KEY`**。
5. 在「Value」部分輸入先前產生的 Maps API 金鑰值。
6. 關閉「密鑰」面板。
7. 如要插入程式碼儲存格，請按一下 add「程式碼」。
8. 如要透過 Maps API 進行驗證，請輸入下列程式碼：

   ```
   # Authenticate with the Google Maps JavaScript API.
   GMP_API_SECRET_KEY_NAME = "GMP_API_KEY" #@param {type:"string"}

   if GMP_API_SECRET_KEY_NAME:
     GMP_API_KEY = userdata.get(GMP_API_SECRET_KEY_NAME) if GMP_API_SECRET_KEY_NAME else None
   else:
     GMP_API_KEY = None
   ```
9. 如果同意，請在系統提示時按一下「授予存取權」，讓筆記本存取您的金鑰。
10. 按一下「執行儲存格」play\_circle\_filled。

    完成授權流程後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。

## 安裝 Python 套件並匯入資料科學程式庫

除了 [`colabtools` (`google.colab`)](https://github.com/googlecolab/colabtools) Python 模組，本教學課程還會使用其他 Python 套件和資料科學程式庫。

在本節中，您將安裝 `pydeck` 和 `h3` 套件。[`pydeck`](https://deckgl.readthedocs.io/en/latest/)
可透過 [`deck.gl`](https://deck.gl/) 在 Python 中提供大規模空間算繪功能。
[`h3-py`](https://uber.github.io/h3-py/intro.html) 提供 Python 版的 Uber H3 六邊形階層式地理空間索引系統。

接著匯入 `h3` 和 `pydeck` 程式庫，以及下列 Python 地理空間程式庫：

* [`geopandas`](https://geopandas.org/en/stable/index.html) 擴充 [`pandas`](https://pandas.pydata.org/) 使用的資料類型，允許對幾何類型執行空間作業。
* [`shapely`](https://shapely.readthedocs.io/en/stable/index.html)，用於操控和分析個別平面幾何物件。
* [`branca`](https://python-visualization.github.io/branca/)，即可生成 HTML 和 JavaScript 色碼表。
* [`geemap.deck`](https://geemap.org/deck/)
  ，以 `pydeck` 和 `earthengine-api` 進行視覺化。

匯入程式庫後，請為 [`pandas` Colab 中的 DataFrame 啟用互動式表格](https://colab.google/articles/alive?hl=zh-tw)。

### 安裝 `pydeck` 和 `h3` 套件

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要安裝 `pydeck` 和 `h3` 套件，請輸入下列程式碼：

   ```
   # Install pydeck and h3.
   !pip install pydeck>=0.9 h3>=4.2
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   安裝完成後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。

### 匯入 Python 程式庫

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要匯入 Python 程式庫，請輸入下列程式碼：

   ```
   # Import data science libraries.
   import branca
   import geemap.deck as gmdk
   import h3
   import pydeck as pdk
   import geopandas as gpd
   import shapely
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。

### 為 pandas DataFrame 啟用互動式表格

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要啟用 `pandas` DataFrame，請輸入下列程式碼：

   ```
   # Enable displaying pandas data frames as interactive tables by default.
   from google.colab import data_table
   data_table.enable_dataframe_formatter()
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。

## 建立共用處理常式

在本節中，您會建立共用常式，在基本地圖上算繪圖層。

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要建立共用常式，在 Google 地圖上算繪圖層，請輸入下列程式碼：

   ```
   # Set Google Maps as the base map provider.
   MAP_PROVIDER_GOOGLE = pdk.bindings.base_map_provider.BaseMapProvider.GOOGLE_MAPS.value

   # Shared routine for rendering layers on a map using geemap.deck.
   def display_pydeck_map(layers, view_state, **kwargs):
     deck_kwargs = kwargs.copy()

     # Use Google Maps as the base map only if the API key is provided.
     if GMP_API_KEY:
       deck_kwargs.update({
         "map_provider": MAP_PROVIDER_GOOGLE,
         "map_style": pdk.bindings.map_styles.GOOGLE_ROAD,
         "api_keys": {MAP_PROVIDER_GOOGLE: GMP_API_KEY},
       })

     m = gmdk.Map(initial_view_state=view_state, ee_initialize=False, **deck_kwargs)

     for layer in layers:
       m.add_layer(layer)
     return m
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。

## 建立散布圖

在本節中，您將從 `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info` 資料表擷取資料，建立舊金山 Ford GoBike Share 公開資料集中所有共享單車租借站的散佈圖。散布圖是使用 `deck.gl` 架構中的[圖層](https://deckgl.readthedocs.io/en/latest/layer.html#pydeck.bindings.layer.Layer)和[散布圖層](https://deck.gl/docs/api-reference/layers/scatterplot-layer)建立。

當您需要查看個別點的子集 (也稱為*抽查*) 時，散佈圖就派得上用場。

以下範例說明如何使用圖層和散佈圖層，將個別點算繪為圓圈。

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要查詢舊金山 Ford GoBike Share 公開資料集，請輸入下列程式碼。這段程式碼使用 [`%%bigquery` 神奇函式](https://googleapis.dev/python/bigquery-magics/latest/)執行查詢，並以 DataFrame 形式傳回結果：

   ```
   # Query the station ID, station name, station short name, and station
   # geometry from the bike share dataset.
   # NOTE: In this tutorial, the denormalized 'lat' and 'lon' columns are
   # ignored. They are decomposed components of the geometry.
   %%bigquery gdf_sf_bikestations --project {GCP_PROJECT_ID} --use_geodataframe station_geom

   SELECT
     station_id,
     name,
     short_name,
     station_geom
   FROM
     `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

   `Job ID 12345-1234-5678-1234-123456789 successfully executed: 100%`
4. 如要插入程式碼儲存格，請按一下 add「程式碼」。
5. 如要取得 DataFrame 的摘要 (包括資料欄和資料類型)，請輸入下列程式碼：

   ```
   # Get a summary of the DataFrame
   gdf_sf_bikestations.info()
   ```
6. 按一下「執行儲存格」play\_circle\_filled。

   輸出內容應如下所示：

   ```
   <class 'geopandas.geodataframe.GeoDataFrame'>
   RangeIndex: 472 entries, 0 to 471
   Data columns (total 4 columns):
   #   Column        Non-Null Count  Dtype
   ---  ------        --------------  -----
   0   station_id    472 non-null    object
   1   name          472 non-null    object
   2   short_name    472 non-null    object
   3   station_geom  472 non-null    geometry
   dtypes: geometry(1), object(3)
   memory usage: 14.9+ KB
   ```
7. 如要插入程式碼儲存格，請按一下 add「程式碼」。
8. 如要預覽 DataFrame 的前五列，請輸入下列程式碼：

   ```
   # Preview the first five rows
   gdf_sf_bikestations.head()
   ```
9. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

如要算繪點，您必須從單車共乘資料集的 `station_geom` 欄位中，將經緯度擷取為 x 和 y 座標。

由於 `gdf_sf_bikestations` 是 `geopandas.GeoDataFrame`，因此座標會直接從其 `station_geom` 幾何資料欄存取。您可以使用資料欄的 `.x` 屬性擷取經度，並使用 `.y` 屬性擷取緯度。然後儲存在新的經緯度欄中。

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要從「`station_geom`」欄擷取經緯度值，請輸入下列程式碼：

   ```
   # Extract the longitude (x) and latitude (y) from station_geom.
   gdf_sf_bikestations["longitude"] = gdf_sf_bikestations["station_geom"].x
   gdf_sf_bikestations["latitude"] = gdf_sf_bikestations["station_geom"].y
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。
4. 如要插入程式碼儲存格，請按一下 add「程式碼」。
5. 如要根據先前擷取的經緯度值，繪製自行車共享車站的散佈圖，請輸入下列程式碼：

   ```
   # Render a scatter plot using pydeck with the extracted longitude and
   # latitude columns in the gdf_sf_bikestations geopandas.GeoDataFrame.
   scatterplot_layer = pdk.Layer(
     "ScatterplotLayer",
     id="bike_stations_scatterplot",
     data=gdf_sf_bikestations,
     get_position=['longitude', 'latitude'],
     get_radius=100,
     get_fill_color=[255, 0, 0, 140],  # Adjust color as desired
     pickable=True,
   )

   view_state = pdk.ViewState(latitude=37.77613, longitude=-122.42284, zoom=12)
   display_pydeck_map([scatterplot_layer], view_state)
   ```
6. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

## 顯示多邊形

地理空間分析功能可讓您使用 `GEOGRAPHY` 資料類型和 GoogleSQL 地理函式，在 BigQuery 中分析及以圖表呈現地理空間資料。

地理空間分析中的 [`GEOGRAPHY` 資料型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)是點、線串和多邊形的集合，以地球表面的點集合或子集合表示。`GEOGRAPHY` 型別可包含下列物件：

* 資料點
* 線條
* 多邊形
* 多邊形集合

如需所有支援物件的清單，請參閱 [`GEOGRAPHY` 類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)說明文件。

如果您取得地理空間資料，但不知道預期形狀，可以將資料視覺化，找出形狀。您可以將地理資料轉換為 [`GeoJSON`](https://geojson.org/) 格式，以視覺化呈現形狀。接著，您可以使用 `deck.gl` 架構中的 [`GeoJSON` 圖層](https://deck.gl/docs/api-reference/layers/geojson-layer)，將 `GeoJSON` 資料視覺化。

在本節中，您將查詢舊金山鄰近地區資料集中的地理資料，然後以多邊形呈現這些資料。

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要查詢「舊金山鄰近地區」資料集 `bigquery-public-data.san_francisco_neighborhoods.boundaries` 資料表中的地理資料，請輸入下列程式碼。這段程式碼會使用 [`%%bigquery` magic 函式](https://googleapis.dev/python/bigquery-magics/latest/)執行查詢，並以 DataFrame 形式傳回結果：

   ```
   # Query the neighborhood name and geometry from the San Francisco
   # neighborhoods dataset.
   %%bigquery gdf_sanfrancisco_neighborhoods --project {GCP_PROJECT_ID} --use_geodataframe geometry

   SELECT
     neighborhood,
     neighborhood_geom AS geometry
   FROM
     `bigquery-public-data.san_francisco_neighborhoods.boundaries`
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

   `Job ID 12345-1234-5678-1234-123456789 successfully executed: 100%`
4. 如要插入程式碼儲存格，請按一下 add「程式碼」。
5. 如要取得 DataFrame 的摘要，請輸入下列程式碼：

   ```
   # Get a summary of the DataFrame
   gdf_sanfrancisco_neighborhoods.info()
   ```
6. 按一下「執行儲存格」play\_circle\_filled。

   結果應如下所示：

   ```
   <class 'geopandas.geodataframe.GeoDataFrame'>
   RangeIndex: 117 entries, 0 to 116
   Data columns (total 2 columns):
   #   Column        Non-Null Count  Dtype
   ---  ------        --------------  -----
   0   neighborhood  117 non-null    object
   1   geometry      117 non-null    geometry
   dtypes: geometry(1), object(1)
   memory usage: 2.0+ KB
   ```
7. 如要預覽 DataFrame 的第一列，請輸入下列程式碼：

   ```
   # Preview the first row
   gdf_sanfrancisco_neighborhoods.head(1)
   ```
8. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

   在結果中，請注意資料是多邊形。
9. 如要插入程式碼儲存格，請按一下 add「程式碼」。
10. 如要將多邊形視覺化，請輸入下列程式碼。`pydeck` 用於將幾何資料欄中的每個 `shapely` 物件例項轉換為 `GeoJSON` 格式：

    ```
    # Visualize the polygons.
    geojson_layer = pdk.Layer(
        'GeoJsonLayer',
        id="sf_neighborhoods",
        data=gdf_sanfrancisco_neighborhoods,
        get_line_color=[127, 0, 127, 255],
        get_fill_color=[60, 60, 60, 50],
        get_line_width=100,
        pickable=True,
        stroked=True,
        filled=True,
      )
    view_state = pdk.ViewState(latitude=37.77613, longitude=-122.42284, zoom=12)
    display_pydeck_map([geojson_layer], view_state)
    ```
11. 按一下「執行儲存格」play\_circle\_filled。

    輸出結果會與下列內容相似：

## 製作 choropleth 地圖

如果您要探索的資料包含難以轉換為 `GeoJSON` 格式的多邊形，可以改用 `deck.gl` 架構的[多邊形圖層](https://deck.gl/docs/api-reference/layers/polygon-layer)。多邊形圖層可以處理特定類型的輸入資料，例如點陣列。

在本節中，您將使用多邊形圖層算繪點陣列，並使用結果算繪 choropleth 地圖。等值線地圖會結合「舊金山鄰近地區」資料集和「舊金山 Ford GoBike 共享單車」資料集中的資料，顯示各鄰近地區的共享單車站密度。

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要匯總及計算每個鄰近地區的電台數量，並建立包含點陣列的 `polygon` 欄，請輸入下列程式碼：

   ```
   # Aggregate and count the number of stations per neighborhood.
   gdf_count_stations = gdf_sanfrancisco_neighborhoods.sjoin(gdf_sf_bikestations, how='left', predicate='contains')
   gdf_count_stations = gdf_count_stations.groupby(by='neighborhood')['station_id'].count().rename('num_stations')
   gdf_stations_x_neighborhood = gdf_sanfrancisco_neighborhoods.join(gdf_count_stations, on='neighborhood', how='inner')

   # To simulate non-GeoJSON input data, create a polygon column that contains
   # an array of points by using the pandas.Series.map method.
   gdf_stations_x_neighborhood['polygon'] = gdf_stations_x_neighborhood['geometry'].map(lambda g: list(g.exterior.coords))
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。
4. 如要插入程式碼儲存格，請按一下 add「程式碼」。
5. 如要為每個多邊形新增 `fill_color` 欄，請輸入下列程式碼：

   ```
   # Create a color map gradient using the branch library, and add a fill_color
   # column for each of the polygons.
   colormap = branca.colormap.LinearColormap(
     colors=["lightblue", "darkred"],
     vmin=0,
     vmax=gdf_stations_x_neighborhood['num_stations'].max(),
   )
   gdf_stations_x_neighborhood['fill_color'] = gdf_stations_x_neighborhood['num_stations'] \
     .map(lambda c: list(colormap.rgba_bytes_tuple(c)[:3]) + [0.7 * 255])   # force opacity of 0.7
   ```
6. 按一下「執行儲存格」play\_circle\_filled。

   執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。
7. 如要插入程式碼儲存格，請按一下 add「程式碼」。
8. 如要算繪多邊形圖層，請輸入下列程式碼：

   ```
   # Render the polygon layer.
   polygon_layer = pdk.Layer(
     'PolygonLayer',
     id="bike_stations_choropleth",
     data=gdf_stations_x_neighborhood,
     get_polygon='polygon',
     get_fill_color='fill_color',
     get_line_color=[0, 0, 0, 255],
     get_line_width=50,
     pickable=True,
     stroked=True,
     filled=True,
   )
   view_state = pdk.ViewState(latitude=37.77613, longitude=-122.42284, zoom=12)
   display_pydeck_map([polygon_layer], view_state)
   ```
9. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

## 建立熱視圖

如果您有已知的有意義界線，就適合使用等值線圖。如果資料沒有已知的有意義界線，可以使用熱度圖層算繪連續密度。

在以下範例中，您會查詢舊金山警察局 (SFPD) 報告資料集內 `bigquery-public-data.san_francisco_sfpd_incidents.sfpd_incidents` 資料表中的資料。這些資料用於呈現 2015 年事件的分布情形。

如果是熱視圖，建議您先量化及彙整資料，再進行算繪。在本範例中，資料會使用 Carto [H3 空間索引](https://docs.carto.com/data-and-analysis/analytics-toolbox-for-bigquery/sql-reference/h3)進行量化和匯總。
熱視圖是使用 `deck.gl` 架構的[熱視圖圖層](https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer)建立。

在本範例中，量化作業是使用 `h3` Python 程式庫完成，可將事件點匯總到六邊形中。`h3.latlng_to_cell` 函式用於將事件的位置 (緯度和經度) 對應至 H3 儲存格索引。熱度圖的 H3 解析度為 9，可提供足夠的聚合六邊形。`h3.cell_to_latlng` 函式用於判斷每個六邊形的中心。

**注意：** 您也可以使用 Carto 的 [BigQuery 專用 Analytics 工具箱](https://carto.com/blog/spatial-functions-bigquery-uber)執行類似的轉換。

1. 如要插入程式碼儲存格，請按一下 add「程式碼」。
2. 如要查詢舊金山警察局 (SFPD) 報告資料集中的資料，請輸入下列程式碼。這段程式碼會使用 [`%%bigquery` magic 函式](https://googleapis.dev/python/bigquery-magics/latest/)執行查詢，並以 DataFrame 格式傳回結果：

   ```
   # Query the incident key and location  data from the SFPD reports dataset.
   %%bigquery gdf_incidents --project {GCP_PROJECT_ID} --use_geodataframe location_geography

   SELECT
     unique_key,
     location_geography
   FROM (
     SELECT
       unique_key,
       SAFE.ST_GEOGFROMTEXT(location) AS location_geography, # WKT string to GEOMETRY
       EXTRACT(YEAR FROM timestamp) AS year,
     FROM `bigquery-public-data.san_francisco_sfpd_incidents.sfpd_incidents` incidents
   )
   WHERE year = 2015
   ```
3. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

   `Job ID 12345-1234-5678-1234-123456789 successfully executed: 100%`
4. 如要插入程式碼儲存格，請按一下 add「程式碼」。
5. 如要計算每個事件的經緯度儲存格，請匯總每個儲存格的事件、建構 `geopandas` DataFrame，並為熱度圖層新增每個六邊形的中心，然後輸入下列程式碼：

   ```
   # Compute the cell for each incident's latitude and longitude.
   H3_RESOLUTION = 9
   gdf_incidents['h3_cell'] = gdf_incidents.geometry.apply(
       lambda geom: h3.latlng_to_cell(geom.y, geom.x, H3_RESOLUTION)
   )

   # Aggregate the incidents for each hexagon cell.
   count_incidents = gdf_incidents.groupby(by='h3_cell')['unique_key'].count().rename('num_incidents')

   # Construct a new geopandas.GeoDataFrame with the aggregate results.
   # Add the center of each hexagon for the HeatmapLayer to render.
   gdf_incidents_x_cell = gpd.GeoDataFrame(data=count_incidents).reset_index()
   gdf_incidents_x_cell['h3_center'] = gdf_incidents_x_cell['h3_cell'].apply(h3.cell_to_latlng)
   gdf_incidents_x_cell.info()
   ```
6. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：

   ```
   <class 'geopandas.geodataframe.GeoDataFrame'>
   RangeIndex: 969 entries, 0 to 968
   Data columns (total 3 columns):
   #   Column         Non-Null Count  Dtype
   --  ------         --------------  -----
   0   h3_cell        969 non-null    object
   1   num_incidents  969 non-null    Int64
   2   h3_center      969 non-null    object
   dtypes: Int64(1), object(2)
   memory usage: 23.8+ KB
   ```
7. 如要插入程式碼儲存格，請按一下 add「程式碼」。
8. 如要預覽 DataFrame 的前五列，請輸入下列程式碼：

   ```
   # Preview the first five rows.
   gdf_incidents_x_cell.head()
   ```
9. 按一下「執行儲存格」play\_circle\_filled。

   輸出結果會與下列內容相似：
10. 如要插入程式碼儲存格，請按一下 add「程式碼」。
11. 如要將資料轉換為 `HeatmapLayer` 可用的 JSON 格式，請輸入下列程式碼：

    ```
    # Convert to a JSON format recognized by the HeatmapLayer.
    def _make_heatmap_datum(row) -> dict:
      return {
          "latitude": row['h3_center'][0],
          "longitude": row['h3_center'][1],
          "weight": float(row['num_incidents']),
      }

    heatmap_data = gdf_incidents_x_cell.apply(_make_heatmap_datum, axis='columns').values.tolist()
    ```
12. 按一下「執行儲存格」play\_circle\_filled。

    執行程式碼後，Colab 筆記本不會產生任何輸出內容。儲存格旁的勾號表示程式碼已順利執行。
13. 如要插入程式碼儲存格，請按一下 add「程式碼」。
14. 如要算繪熱度圖，請輸入下列程式碼：

    ```
    # Render the heatmap.
    heatmap_layer = pdk.Layer(
      "HeatmapLayer",
      id="sfpd_heatmap",
      data=heatmap_data,
      get_position=['longitude', 'latitude'],
      get_weight='weight',
      opacity=0.7,
      radius_pixels=99,  # this limitation can introduce artifacts (see above)
      aggregation='MEAN',
    )
    view_state = pdk.ViewState(latitude=37.77613, longitude=-122.42284, zoom=12)
    display_pydeck_map([heatmap_layer], view_state)
    ```
15. 按一下「執行儲存格」play\_circle\_filled。

    輸出結果會與下列內容相似：

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

### 控制台

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### gcloud

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除 Google Maps API 金鑰和筆記本

刪除 Google Cloud 專案後，如果您使用 Google 地圖 API，請從 Colab Secrets 刪除 Google 地圖 API 金鑰，然後視需要刪除筆記本。

1. 在 Colab 中，按一下「Secrets」(密鑰) vpn\_key。
2. 在 `GMP_API_KEY` 列的結尾，按一下「刪除」delete 。
3. 選用：如要刪除筆記本，請依序點選「檔案」**>「移至垃圾桶」**。

## 後續步驟

* 如要進一步瞭解 BigQuery 中的地理空間分析，請參閱「[BigQuery 地理空間分析簡介](https://docs.cloud.google.com/bigquery/docs/geospatial-intro?hl=zh-tw)」。
* 如要瞭解如何以視覺化方式呈現 BigQuery 中的地理空間資料，請參閱[以視覺化方式呈現地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw)。
* 如要進一步瞭解 `pydeck` 和其他 `deck.gl` 圖表類型，請參閱 [`pydeck` 藝廊](https://deckgl.readthedocs.io/en/latest/)、[`deck.gl` 圖層目錄](https://deck.gl/docs/api-reference/layers)和 [`deck.gl` GitHub 來源](https://github.com/visgl/deck.gl)中的範例。
* 如要進一步瞭解如何在資料框架中使用地理空間資料，請參閱 [GeoPandas 入門頁面](https://geopandas.org/en/stable/getting_started.html)和 [GeoPandas 使用者指南](https://geopandas.org/en/stable/docs/user_guide.html)。
* 如要進一步瞭解幾何物件操作，請參閱 [Shapely 使用手冊](https://shapely.readthedocs.io/en/stable/manual.html)。
* 如要瞭解如何在 BigQuery 中使用 Google Earth Engine 資料，請參閱 Google Earth Engine 說明文件中的「[匯出至 BigQuery](https://developers.google.com/earth-engine/guides/exporting_to_bigquery?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]