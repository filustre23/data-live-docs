* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: models Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Model](#Model)
  + [JSON representation](#Model.SCHEMA_REPRESENTATION)
* [ModelReference](#ModelReference)
  + [JSON representation](#ModelReference.SCHEMA_REPRESENTATION)
* [ModelType](#ModelType)
* [TrainingRun](#TrainingRun)
  + [JSON representation](#TrainingRun.SCHEMA_REPRESENTATION)
* [TrainingOptions](#TrainingOptions)
  + [JSON representation](#TrainingOptions.SCHEMA_REPRESENTATION)
* [LossType](#LossType)
* [DataSplitMethod](#DataSplitMethod)
* [LearnRateStrategy](#LearnRateStrategy)
* [DistanceType](#DistanceType)
* [OptimizationStrategy](#OptimizationStrategy)
* [BoosterType](#BoosterType)
* [DartNormalizeType](#DartNormalizeType)
* [TreeMethod](#TreeMethod)
* [FeedbackType](#FeedbackType)
* [KmeansInitializationMethod](#KmeansInitializationMethod)
* [ArimaOrder](#ArimaOrder)
  + [JSON representation](#ArimaOrder.SCHEMA_REPRESENTATION)
* [DataFrequency](#DataFrequency)
* [HolidayRegion](#HolidayRegion)
* [HparamTuningObjective](#HparamTuningObjective)
* [EncodingMethod](#EncodingMethod)
* [PcaSolver](#PcaSolver)
* [ModelRegistry](#ModelRegistry)
* [IterationResult](#IterationResult)
  + [JSON representation](#IterationResult.SCHEMA_REPRESENTATION)
* [ClusterInfo](#ClusterInfo)
  + [JSON representation](#ClusterInfo.SCHEMA_REPRESENTATION)
* [ArimaResult](#ArimaResult)
  + [JSON representation](#ArimaResult.SCHEMA_REPRESENTATION)
* [ArimaModelInfo](#ArimaModelInfo)
  + [JSON representation](#ArimaModelInfo.SCHEMA_REPRESENTATION)
* [ArimaCoefficients](#ArimaCoefficients)
  + [JSON representation](#ArimaCoefficients.SCHEMA_REPRESENTATION)
* [ArimaFittingMetrics](#ArimaFittingMetrics)
  + [JSON representation](#ArimaFittingMetrics.SCHEMA_REPRESENTATION)
* [SeasonalPeriodType](#SeasonalPeriodType)
* [PrincipalComponentInfo](#PrincipalComponentInfo)
  + [JSON representation](#PrincipalComponentInfo.SCHEMA_REPRESENTATION)
* [EvaluationMetrics](#EvaluationMetrics)
  + [JSON representation](#EvaluationMetrics.SCHEMA_REPRESENTATION)
* [RegressionMetrics](#RegressionMetrics)
  + [JSON representation](#RegressionMetrics.SCHEMA_REPRESENTATION)
* [BinaryClassificationMetrics](#BinaryClassificationMetrics)
  + [JSON representation](#BinaryClassificationMetrics.SCHEMA_REPRESENTATION)
* [AggregateClassificationMetrics](#AggregateClassificationMetrics)
  + [JSON representation](#AggregateClassificationMetrics.SCHEMA_REPRESENTATION)
* [BinaryConfusionMatrix](#BinaryConfusionMatrix)
  + [JSON representation](#BinaryConfusionMatrix.SCHEMA_REPRESENTATION)
* [MultiClassClassificationMetrics](#MultiClassClassificationMetrics)
  + [JSON representation](#MultiClassClassificationMetrics.SCHEMA_REPRESENTATION)
* [ConfusionMatrix](#ConfusionMatrix)
  + [JSON representation](#ConfusionMatrix.SCHEMA_REPRESENTATION)
* [Row](#Row)
  + [JSON representation](#Row.SCHEMA_REPRESENTATION)
* [Entry](#Entry)
  + [JSON representation](#Entry.SCHEMA_REPRESENTATION)
* [ClusteringMetrics](#ClusteringMetrics)
  + [JSON representation](#ClusteringMetrics.SCHEMA_REPRESENTATION)
* [Cluster](#Cluster)
  + [JSON representation](#Cluster.SCHEMA_REPRESENTATION)
* [FeatureValue](#FeatureValue)
  + [JSON representation](#FeatureValue.SCHEMA_REPRESENTATION)
* [CategoricalValue](#CategoricalValue)
  + [JSON representation](#CategoricalValue.SCHEMA_REPRESENTATION)
* [CategoryCount](#CategoryCount)
  + [JSON representation](#CategoryCount.SCHEMA_REPRESENTATION)
* [RankingMetrics](#RankingMetrics)
  + [JSON representation](#RankingMetrics.SCHEMA_REPRESENTATION)
* [ArimaForecastingMetrics](#ArimaForecastingMetrics)
  + [JSON representation](#ArimaForecastingMetrics.SCHEMA_REPRESENTATION)
* [ArimaSingleModelForecastingMetrics](#ArimaSingleModelForecastingMetrics)
  + [JSON representation](#ArimaSingleModelForecastingMetrics.SCHEMA_REPRESENTATION)
* [DimensionalityReductionMetrics](#DimensionalityReductionMetrics)
  + [JSON representation](#DimensionalityReductionMetrics.SCHEMA_REPRESENTATION)
* [DataSplitResult](#DataSplitResult)
  + [JSON representation](#DataSplitResult.SCHEMA_REPRESENTATION)
* [GlobalExplanation](#GlobalExplanation)
  + [JSON representation](#GlobalExplanation.SCHEMA_REPRESENTATION)
* [Explanation](#Explanation)
  + [JSON representation](#Explanation.SCHEMA_REPRESENTATION)
* [TransformColumn](#TransformColumn)
  + [JSON representation](#TransformColumn.SCHEMA_REPRESENTATION)
* [HparamSearchSpaces](#HparamSearchSpaces)
  + [JSON representation](#HparamSearchSpaces.SCHEMA_REPRESENTATION)
* [DoubleHparamSearchSpace](#DoubleHparamSearchSpace)
  + [JSON representation](#DoubleHparamSearchSpace.SCHEMA_REPRESENTATION)
* [DoubleRange](#DoubleRange)
  + [JSON representation](#DoubleRange.SCHEMA_REPRESENTATION)
* [DoubleCandidates](#DoubleCandidates)
  + [JSON representation](#DoubleCandidates.SCHEMA_REPRESENTATION)
* [IntHparamSearchSpace](#IntHparamSearchSpace)
  + [JSON representation](#IntHparamSearchSpace.SCHEMA_REPRESENTATION)
* [IntRange](#IntRange)
  + [JSON representation](#IntRange.SCHEMA_REPRESENTATION)
* [IntCandidates](#IntCandidates)
  + [JSON representation](#IntCandidates.SCHEMA_REPRESENTATION)
* [IntArrayHparamSearchSpace](#IntArrayHparamSearchSpace)
  + [JSON representation](#IntArrayHparamSearchSpace.SCHEMA_REPRESENTATION)
* [IntArray](#IntArray)
  + [JSON representation](#IntArray.SCHEMA_REPRESENTATION)
* [StringHparamSearchSpace](#StringHparamSearchSpace)
  + [JSON representation](#StringHparamSearchSpace.SCHEMA_REPRESENTATION)
* [HparamTuningTrial](#HparamTuningTrial)
  + [JSON representation](#HparamTuningTrial.SCHEMA_REPRESENTATION)
* [TrialStatus](#TrialStatus)
* [RemoteModelInfo](#RemoteModelInfo)
  + [JSON representation](#RemoteModelInfo.SCHEMA_REPRESENTATION)
* [RemoteServiceType](#RemoteServiceType)
* [Methods](#METHODS_SUMMARY)

## Resource: Model

| JSON representation |
| --- |
| ``` {   "etag": string,   "modelReference": {     object (ModelReference)   },   "creationTime": string,   "lastModifiedTime": string,   "description": string,   "friendlyName": string,   "labels": {     string: string,     ...   },   "expirationTime": string,   "location": string,   "encryptionConfiguration": {     object (EncryptionConfiguration)   },   "modelType": enum (ModelType),   "trainingRuns": [     {       object (TrainingRun)     }   ],   "featureColumns": [     {       object (StandardSqlField)     }   ],   "labelColumns": [     {       object (StandardSqlField)     }   ],   "transformColumns": [     {       object (TransformColumn)     }   ],   "hparamSearchSpaces": {     object (HparamSearchSpaces)   },   "bestTrialId": string,   "defaultTrialId": string,   "hparamTrials": [     {       object (HparamTuningTrial)     }   ],   "optimalTrialIds": [     string   ],   "remoteModelInfo": {     object (RemoteModelInfo)   } } ``` |

| Fields | |
| --- | --- |
| `etag` | `string`  Output only. A hash of this resource. |
| `modelReference` | `object (ModelReference)`  Required. Unique identifier for this model. |
| `creationTime` | `string (int64 format)`  Output only. The time when this model was created, in millisecs since the epoch. |
| `lastModifiedTime` | `string (int64 format)`  Output only. The time when this model was last modified, in millisecs since the epoch. |
| `description` | `string`  Optional. A user-friendly description of this model. |
| `friendlyName` | `string`  Optional. A descriptive name for this model. |
| `labels` | `map (key: string, value: string)`  The labels associated with this model. You can use these to organize and group your models. Label keys and values can be no longer than 63 characters, can only contain lowercase letters, numeric characters, underscores and dashes. International characters are allowed. Label values are optional. Label keys must start with a letter and each label in the list must have a different key. |
| `expirationTime` | `string (int64 format)`  Optional. The time when this model expires, in milliseconds since the epoch. If not present, the model will persist indefinitely. Expired models will be deleted and their storage reclaimed. The defaultTableExpirationMs property of the encapsulating dataset can be used to set a default expirationTime on newly created models. |
| `location` | `string`  Output only. The geographic location where the model resides. This value is inherited from the dataset. |
| `encryptionConfiguration` | `object (EncryptionConfiguration)`  Custom encryption configuration (e.g., Cloud KMS keys). This shows the encryption configuration of the model data while stored in BigQuery storage. This field can be used with models.patch to update encryption key for an already encrypted model. |
| `modelType` | `enum (ModelType)`  Output only. Type of the model resource. |
| `trainingRuns[]` | `object (TrainingRun)`  Information for all training runs in increasing order of startTime. |
| `featureColumns[]` | `object (StandardSqlField)`  Output only. Input feature columns for the model inference. If the model is trained with TRANSFORM clause, these are the input of the TRANSFORM clause. |
| `labelColumns[]` | `object (StandardSqlField)`  Output only. Label columns that were used to train this model. The output of the model will have a "predicted\_" prefix to these columns. |
| `transformColumns[]` | `object (TransformColumn)`  Output only. This field will be populated if a TRANSFORM clause was used to train a model. TRANSFORM clause (if used) takes featureColumns as input and outputs transformColumns. transformColumns then are used to train the model. |
| `hparamSearchSpaces` | `object (HparamSearchSpaces)`  Output only. All hyperparameter search spaces in this model. |
| `bestTrialId (deprecated)` | `string (int64 format)`  This item is deprecated!  The best trialId across all training runs. |
| `defaultTrialId` | `string (int64 format)`  Output only. The default trialId to use in TVFs when the trialId is not passed in. For single-objective [hyperparameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview) models, this is the best trial ID. For multi-objective [hyperparameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview) models, this is the smallest trial ID among all Pareto optimal trials. |
| `hparamTrials[]` | `object (HparamTuningTrial)`  Output only. Trials of a [hyperparameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview) model sorted by trialId. |
| `optimalTrialIds[]` | `string (int64 format)`  Output only. For single-objective [hyperparameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview) models, it only contains the best trial. For multi-objective [hyperparameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview) models, it contains all Pareto optimal trials sorted by trialId. |
| `remoteModelInfo` | `object (RemoteModelInfo)`  Output only. Remote model info |

## ModelReference

Id path of a model.

| JSON representation |
| --- |
| ``` {   "projectId": string,   "datasetId": string,   "modelId": string } ``` |

| Fields | |
| --- | --- |
| `projectId` | `string`  Required. The ID of the project containing this model. |
| `datasetId` | `string`  Required. The ID of the dataset containing this model. |
| `modelId` | `string`  Required. The ID of the model. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_). The maximum length is 1,024 characters. |

## ModelType

Indicates the type of the Model.

| Enums | |
| --- | --- |
| `MODEL_TYPE_UNSPECIFIED` | Default value. |
| `LINEAR_REGRESSION` | Linear regression model. |
| `LOGISTIC_REGRESSION` | Logistic regression based classification model. |
| `KMEANS` | K-means clustering model. |
| `MATRIX_FACTORIZATION` | Matrix factorization model. |
| `DNN_CLASSIFIER` | DNN classifier model. |
| `TENSORFLOW` | An imported TensorFlow model. |
| `DNN_REGRESSOR` | DNN regressor model. |
| `XGBOOST` | An imported XGBoost model. |
| `BOOSTED_TREE_REGRESSOR` | Boosted tree regressor model. |
| `BOOSTED_TREE_CLASSIFIER` | Boosted tree classifier model. |
| `ARIMA` | ARIMA model. |
| `AUTOML_REGRESSOR` | AutoML Tables regression model. |
| `AUTOML_CLASSIFIER` | AutoML Tables classification model. |
| `PCA` | Prinpical Component Analysis model. |
| `DNN_LINEAR_COMBINED_CLASSIFIER` | Wide-and-deep classifier model. |
| `DNN_LINEAR_COMBINED_REGRESSOR` | Wide-and-deep regressor model. |
| `AUTOENCODER` | Autoencoder model. |
| `ARIMA_PLUS` | New name for the ARIMA model. |
| `ARIMA_PLUS_XREG` | ARIMA with external regressors. |
| `RANDOM_FOREST_REGRESSOR` | Random forest regressor model. |
| `RANDOM_FOREST_CLASSIFIER` | Random forest classifier model. |
| `TENSORFLOW_LITE` | An imported TensorFlow Lite model. |
| `ONNX` | An imported ONNX model. |
| `TRANSFORM_ONLY` | Model to capture the columns and logic in the TRANSFORM clause along with statistics useful for ML analytic functions. |
| `CONTRIBUTION_ANALYSIS` | The contribution analysis model. |

## TrainingRun

Information about a single training query run for the model.

| JSON representation |
| --- |
| ``` {   "trainingOptions": {     object (TrainingOptions)   },   "trainingStartTime": string,   "startTime": string,   "results": [     {       object (IterationResult)     }   ],   "evaluationMetrics": {     object (EvaluationMetrics)   },   "dataSplitResult": {     object (DataSplitResult)   },   "modelLevelGlobalExplanation": {     object (GlobalExplanation)   },   "classLevelGlobalExplanations": [     {       object (GlobalExplanation)     }   ],   "vertexAiModelId": string,   "vertexAiModelVersion": string } ``` |

| Fields | |
| --- | --- |
| `trainingOptions` | `object (TrainingOptions)`  Output only. Options that were used for this training run, includes user specified and default options that were used. |
| `trainingStartTime (deprecated)` | `string (int64 format)`  This item is deprecated!  Output only. The start time of this training run, in milliseconds since epoch. |
| `startTime` | `string (Timestamp format)`  Output only. The start time of this training run. |
| `results[]` | `object (IterationResult)`  Output only. Output of each iteration run, results.size() <= maxIterations. |
| `evaluationMetrics` | `object (EvaluationMetrics)`  Output only. The evaluation metrics over training/eval data that were computed at the end of training. |
| `dataSplitResult` | `object (DataSplitResult)`  Output only. Data split result of the training run. Only set when the input data is actually split. |
| `modelLevelGlobalExplanation` | `object (GlobalExplanation)`  Output only. Global explanation contains the explanation of top features on the model level. Applies to both regression and classification models. |
| `classLevelGlobalExplanations[]` | `object (GlobalExplanation)`  Output only. Global explanation contains the explanation of top features on the class level. Applies to classification models only. |
| `vertexAiModelId` | `string`  The model id in the [Vertex AI Model Registry](https://cloud.google.com/vertex-ai/docs/model-registry/introduction) for this training run. |
| `vertexAiModelVersion` | `string`  Output only. The model version in the [Vertex AI Model Registry](https://cloud.google.com/vertex-ai/docs/model-registry/introduction) for this training run. |

## TrainingOptions

Options used in model training.

| JSON representation |
| --- |
| ``` {   "maxIterations": string,   "lossType": enum (LossType),   "learnRate": number,   "l1Regularization": number,   "l2Regularization": number,   "minRelativeProgress": number,   "warmStart": boolean,   "earlyStop": boolean,   "inputLabelColumns": [     string   ],   "dataSplitMethod": enum (DataSplitMethod),   "dataSplitEvalFraction": number,   "dataSplitColumn": string,   "learnRateStrategy": enum (LearnRateStrategy),   "initialLearnRate": number,   "labelClassWeights": {     string: number,     ...   },   "userColumn": string,   "itemColumn": string,   "distanceType": enum (DistanceType),   "numClusters": string,   "modelUri": string,   "optimizationStrategy": enum (OptimizationStrategy),   "hiddenUnits": [     string   ],   "batchSize": string,   "dropout": number,   "maxTreeDepth": string,   "subsample": number,   "minSplitLoss": number,   "boosterType": enum (BoosterType),   "numParallelTree": string,   "dartNormalizeType": enum (DartNormalizeType),   "treeMethod": enum (TreeMethod),   "minTreeChildWeight": string,   "colsampleBytree": number,   "colsampleBylevel": number,   "colsampleBynode": number,   "numFactors": string,   "feedbackType": enum (FeedbackType),   "walsAlpha": number,   "kmeansInitializationMethod": enum (KmeansInitializationMethod),   "kmeansInitializationColumn": string,   "timeSeriesTimestampColumn": string,   "timeSeriesDataColumn": string,   "autoArima": boolean,   "nonSeasonalOrder": {     object (ArimaOrder)   },   "dataFrequency": enum (DataFrequency),   "calculatePValues": boolean,   "includeDrift": boolean,   "holidayRegion": enum (HolidayRegion),   "holidayRegions": [     enum (HolidayRegion)   ],   "timeSeriesIdColumn": string,   "timeSeriesIdColumns": [     string   ],   "forecastLimitLowerBound": number,   "forecastLimitUpperBound": number,   "horizon": string,   "autoArimaMaxOrder": string,   "autoArimaMinOrder": string,   "numTrials": string,   "maxParallelTrials": string,   "hparamTuningObjectives": [     enum (HparamTuningObjective)   ],   "decomposeTimeSeries": boolean,   "cleanSpikesAndDips": boolean,   "adjustStepChanges": boolean,   "enableGlobalExplain": boolean,   "sampledShapleyNumPaths": string,   "integratedGradientsNumSteps": string,   "categoryEncodingMethod": enum (EncodingMethod),   "tfVersion": string,   "instanceWeightColumn": string,   "trendSmoothingWindowSize": string,   "timeSeriesLengthFraction": number,   "minTimeSeriesLength": string,   "maxTimeSeriesLength": string,   "xgboostVersion": string,   "approxGlobalFeatureContrib": boolean,   "fitIntercept": boolean,   "numPrincipalComponents": string,   "pcaExplainedVarianceRatio": number,   "scaleFeatures": boolean,   "pcaSolver": enum (PcaSolver),   "autoClassWeights": boolean,   "activationFn": string,   "optimizer": string,   "budgetHours": number,   "standardizeFeatures": boolean,   "l1RegActivation": number,   "modelRegistry": enum (ModelRegistry),   "vertexAiModelVersionAliases": [     string   ],   "dimensionIdColumns": [     string   ],   "contributionMetric": string,   "isTestColumn": string,   "minAprioriSupport": number } ``` |

| Fields | |
| --- | --- |
| `maxIterations` | `string (int64 format)`  The maximum number of iterations in training. Used only for iterative training algorithms. |
| `lossType` | `enum (LossType)`  Type of loss function used during training run. |
| `learnRate` | `number`  Learning rate in training. Used only for iterative training algorithms. |
| `l1Regularization` | `number`  L1 regularization coefficient. |
| `l2Regularization` | `number`  L2 regularization coefficient. |
| `minRelativeProgress` | `number`  When earlyStop is true, stops training when accuracy improvement is less than 'minRelativeProgress'. Used only for iterative training algorithms. |
| `warmStart` | `boolean`  Whether to train a model from the last checkpoint. |
| `earlyStop` | `boolean`  Whether to stop early when the loss doesn't improve significantly any more (compared to minRelativeProgress). Used only for iterative training algorithms. |
| `inputLabelColumns[]` | `string`  Name of input label columns in training data. |
| `dataSplitMethod` | `enum (DataSplitMethod)`  The data split type for training and evaluation, e.g. RANDOM. |
| `dataSplitEvalFraction` | `number`  The fraction of evaluation data over the whole input data. The rest of data will be used as training data. The format should be double. Accurate to two decimal places. Default value is 0.2. |
| `dataSplitColumn` | `string`  The column to split data with. This column won't be used as a feature. 1. When dataSplitMethod is CUSTOM, the corresponding column should be boolean. The rows with true value tag are eval data, and the false are training data. 2. When dataSplitMethod is SEQ, the first DATA\_SPLIT\_EVAL\_FRACTION rows (from smallest to largest) in the corresponding column are used as training data, and the rest are eval data. It respects the order in Orderable data types: <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_properties> |