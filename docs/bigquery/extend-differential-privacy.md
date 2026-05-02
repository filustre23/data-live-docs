* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 擴大差異化隱私

本文提供 BigQuery 差異化隱私功能的差異化隱私擴充方式範例。

BigQuery 可讓您將[差異隱私權](https://docs.cloud.google.com/bigquery/docs/differential-privacy?hl=zh-tw)擴充至多雲資料來源和外部差異隱私權程式庫。本文提供範例，說明如何針對 AWS S3 等多雲資料來源，透過 BigQuery Omni 套用差異隱私權、如何使用遠端函式呼叫外部差異隱私權程式庫，以及如何使用 [PipelineDP](https://pipelinedp.io/) 是可搭配 Apache Spark 和 Apache Beam 執行的 Python 程式庫。

**注意：** 在本文件中，範例中的隱私權參數並非建議值。您應與隱私權或安全性人員合作，決定資料集和機構最適合的隱私權參數。

如要進一步瞭解差異化隱私，請參閱「[使用差異化隱私](https://docs.cloud.google.com/bigquery/docs/differential-privacy?hl=zh-tw)」。

## 透過 BigQuery Omni 實現差異化隱私權

BigQuery 差異化隱私權功能支援對 AWS S3 等多雲端資料來源的呼叫。以下範例會查詢外部資料來源 `foo.wikidata`，並套用差異化隱私技術。如要進一步瞭解差異化隱私權條款的語法，請參閱「[差異化隱私權條款](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)」。

```
SELECT
  WITH
    DIFFERENTIAL_PRIVACY
      OPTIONS (
        epsilon = 1,
        delta = 1e-5,
        privacy_unit_column = foo.wikidata.es_description)
      COUNT(*) AS results
FROM foo.wikidata;
```

這個範例會傳回類似以下的結果：

```
-- These results will change each time you run the query.
+----------+
| results  |
+----------+
| 3465     |
+----------+
```

如要進一步瞭解 BigQuery Omni 的限制，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)」一節。

## 使用遠端函式呼叫外部差異化隱私程式庫

您可以使用[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)呼叫外部差異化隱私權程式庫。下列連結會使用遠端函式呼叫由 [Tumult Analytics](https://www.tmlt.dev) 代管的外部程式庫，針對零售銷售資料集使用零集中差別隱私權。

如要瞭解如何使用 Tumult Analytics，請參閱 [Tumult Analytics 推出文章](https://www.tmlt.io/resources/gcp-launch-post) {: .external}。

## 使用 PipelineDP 進行差異化隱私匯總

PipelineDP 是執行差異化隱私匯總作業的 Python 程式庫，可搭配 Apache Spark 和 Apache Beam 執行。BigQuery 可執行以 Python 編寫的 Apache Spark 預存程序。如要進一步瞭解如何執行 Apache Spark 預存程序，請參閱「[使用 Apache Spark 預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)」。

以下範例會使用 PipelineDP 程式庫執行差異化隱私權匯總作業。這項模型會使用 [芝加哥計程車車程公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)，並為每輛計程車計算行程數量，以及這些行程的小費總和和平均值。

### 事前準備

標準 Apache Spark 映像檔不包含 PipelineDP。您必須先建立包含所有必要依附元件的 [Docker](https://www.docker.com/) 映像檔，才能執行 PipelineDP 儲存程序。本節說明如何建立 Docker 映像檔，並將其推送至 Google Cloud。

在開始之前，請確認您已在本機電腦上安裝 Docker，並設定驗證機制，以便將 Docker 映像檔推送至 [gcr.io](https://docs.cloud.google.com/artifact-registry?hl=zh-tw)。如要進一步瞭解如何推送 Docker 映像檔，請參閱「[推送及提取映像檔](https://docs.cloud.google.com/artifact-registry/docs/pushing-and-pulling?hl=zh-tw)」。

#### 建立及推送 Docker 映像檔

如要建立並推送含有必要依附元件的 Docker 映像檔，請按照下列步驟操作：

1. 建立本機資料夾 `DIR`。
2. 下載 [Miniconda 安裝程式](https://docs.conda.io/en/latest/miniconda.html#linux-installers) (含 Python 3.9 版本) 至 `DIR`。
3. 將下列文字儲存至 [Dockerfile](https://docs.docker.com/engine/reference/builder/#:%7E:text=A%20Dockerfile%20is%20a%20text,can%20use%20in%20a%20Dockerfile%20)。

   ```
     # Debian 11 is recommended.
     FROM debian:11-slim

     # Suppress interactive prompts
     ENV DEBIAN_FRONTEND=noninteractive

     # (Required) Install utilities required by Spark scripts.
     RUN apt update && apt install -y procps tini libjemalloc2

     # Enable jemalloc2 as default memory allocator
     ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2

     # Install and configure Miniconda3.
     ENV CONDA_HOME=/opt/miniconda3
     ENV PYSPARK_PYTHON=${CONDA_HOME}/bin/python
     ENV PATH=${CONDA_HOME}/bin:${PATH}
     COPY Miniconda3-py39_23.1.0-1-Linux-x86_64.sh .
     RUN bash Miniconda3-py39_23.1.0-1-Linux-x86_64.sh -b -p /opt/miniconda3 \
     && ${CONDA_HOME}/bin/conda config --system --set always_yes True \
     && ${CONDA_HOME}/bin/conda config --system --set auto_update_conda False \
     && ${CONDA_HOME}/bin/conda config --system --prepend channels conda-forge \
     && ${CONDA_HOME}/bin/conda config --system --set channel_priority strict

     # The following packages are installed in the default image, it is
     # strongly recommended to include all of them.
     RUN apt install -y python3
     RUN apt install -y python3-pip
     RUN apt install -y libopenblas-dev
     RUN pip install \
       cython \
       fastavro \
       fastparquet \
       gcsfs \
       google-cloud-bigquery-storage \
       google-cloud-bigquery[pandas] \
       google-cloud-bigtable \
       google-cloud-container \
       google-cloud-datacatalog \
       google-cloud-dataproc \
       google-cloud-datastore \
       google-cloud-language \
       google-cloud-logging \
       google-cloud-monitoring \
       google-cloud-pubsub \
       google-cloud-redis \
       google-cloud-spanner \
       google-cloud-speech \
       google-cloud-storage \
       google-cloud-texttospeech \
       google-cloud-translate \
       google-cloud-vision \
       koalas \
       matplotlib \
       nltk \
       numba \
       numpy \
       orc \
       pandas \
       pyarrow \
       pysal \
       regex \
       requests \
       rtree \
       scikit-image \
       scikit-learn \
       scipy \
       seaborn \
       sqlalchemy \
       sympy \
       tables \
       virtualenv
     RUN pip install --no-input pipeline-dp==0.2.0

     # (Required) Create the 'spark' group/user.
     # The GID and UID must be 1099. Home directory is required.
     RUN groupadd -g 1099 spark
     RUN useradd -u 1099 -g 1099 -d /home/spark -m spark
     USER spark
   ```
4. 執行下列指令。

   ```
   IMAGE=gcr.io/PROJECT_ID/DOCKER_IMAGE:0.0.1
   # Build and push the image.
   docker build -t "${IMAGE}"
   docker push "${IMAGE}"
   ```

   更改下列內容：

   * `PROJECT_ID`：您要建立 Docker 映像檔的專案。
   * `DOCKER_IMAGE`：Docker 映像檔名稱。

   圖片已上傳。

### 執行 PipelineDP 預存程序

1. 如要建立已儲存的程序，請使用 [CREATE PROCEDURE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure) 陳述式。

   ```
   CREATE OR REPLACE
   PROCEDURE
     `PROJECT_ID.DATASET_ID.pipeline_dp_example_spark_proc`()
     WITH CONNECTION `PROJECT_ID.REGION.CONNECTION_ID`
   OPTIONS (
     engine = "SPARK",
     container_image= "gcr.io/PROJECT_ID/DOCKER_IMAGE")
   LANGUAGE PYTHON AS R"""
   from pyspark.sql import SparkSession
   import pipeline_dp

   def compute_dp_metrics(data, spark_context):
   budget_accountant = pipeline_dp.NaiveBudgetAccountant(total_epsilon=10,
                                                         total_delta=1e-6)
   backend = pipeline_dp.SparkRDDBackend(spark_context)

   # Create a DPEngine instance.
   dp_engine = pipeline_dp.DPEngine(budget_accountant, backend)

   params = pipeline_dp.AggregateParams(
       noise_kind=pipeline_dp.NoiseKind.LAPLACE,
       metrics=[
           pipeline_dp.Metrics.COUNT, pipeline_dp.Metrics.SUM,
           pipeline_dp.Metrics.MEAN],
       max_partitions_contributed=1,
       max_contributions_per_partition=1,
       min_value=0,
       # Tips that are larger than 100 will be clipped to 100.
       max_value=100)
   # Specify how to extract privacy_id, partition_key and value from an
   # element of the taxi dataset.
   data_extractors = pipeline_dp.DataExtractors(
       partition_extractor=lambda x: x.taxi_id,
       privacy_id_extractor=lambda x: x.unique_key,
       value_extractor=lambda x: 0 if x.tips is None else x.tips)

   # Run aggregation.
   dp_result = dp_engine.aggregate(data, params, data_extractors)
   budget_accountant.compute_budgets()
   dp_result = backend.map_tuple(dp_result, lambda pk, result: (pk, result.count, result.sum, result.mean))
   return dp_result

   spark = SparkSession.builder.appName("spark-pipeline-dp-demo").getOrCreate()
   spark_context = spark.sparkContext

   # Load data from BigQuery.
   taxi_trips = spark.read.format("bigquery") \
   .option("table", "bigquery-public-data:chicago_taxi_trips.taxi_trips") \
   .load().rdd
   dp_result = compute_dp_metrics(taxi_trips, spark_context).toDF(["pk", "count","sum", "mean"])
   # Saving the data to BigQuery
   dp_result.write.format("bigquery") \
   .option("writeMethod", "direct") \
   .save("DATASET_ID.TABLE_NAME")
   """;
   ```

   更改下列內容：

   * `PROJECT_ID`：您要建立已儲存程序的專案。
   * `DATASET_ID`：您要建立預存程序的資料集。
   * `REGION`：專案所在的區域。
   * `DOCKER_IMAGE`：Docker 映像檔名稱。
   * `CONNECTION_ID`：連線名稱。
   * `TABLE_NAME`：資料表名稱。
2. 使用 [CALL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#call) 陳述式呼叫程序。

   ```
   CALL `PROJECT_ID.DATASET_ID.pipeline_dp_example_spark_proc`()
   ```

   更改下列內容：

   * `PROJECT_ID`：您要建立已儲存程序的專案。
   * `DATASET_ID`：您要建立預存程序的資料集。

## 後續步驟

* 瞭解如何[使用差異化隱私](https://docs.cloud.google.com/bigquery/docs/differential-privacy?hl=zh-tw)。
* 瞭解[差異隱私權條款](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)。
* 瞭解如何使用[差異性私密匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-dp-functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]