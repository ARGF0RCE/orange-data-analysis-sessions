# Heart disease: cleaning and feature selection without leakage

Open `heart_cleaning_end_to_end.ows` in Orange and choose the bundled **heart_disease** sample in File if necessary. This complete workflow uses built-in widgets only. The older `impute.ows` and `purgedomain.ows` remain small examples; this guide explains how preparation belongs inside a validated model pipeline. See [pipeline concepts](../docs/pipeline_concepts.md).

## Purpose and starting point

Inspect incomplete historical clinical records, demonstrate a cleaned training table, select relevant features, and compare classification models fairly. Expect **303 rows**, **13 features**, and a **two-class target** named **diameter narrowing** (categories **0** and **1**). The full bundled table contains **six missing feature cells**. Missingness is sparse, so cleaning may visibly change only a few cells. Verify the live table instead of manufacturing defects to make cleaning look dramatic.

## Step by step

1. **Inspect the source and roles.** Open File and the raw Data Table. Look at feature names, numeric versus categorical types, target values, and missing cells. Retain the shipped target and all 13 source predictors in Select Columns. Missing is not the same as zero, and category codes are not necessarily quantities.
2. **Reserve holdout first.** In Data Sampler set **Fixed proportion 80%**, **Replicable sampling**, and **Stratify sample**. Orange's replicable sampling uses seed 42. Use `Data Sample` as training (**243 rows** in Orange 3.40) and `Remaining Data` as holdout (**60 rows**). Missing-cell counts in training can differ from those in the full table.
3. **Explore the training split.** Inspect the training Data Table, Distributions, Box Plot, and Scatter Plot. Choose variables with missing entries as well as age/cholesterol; plot age against cholesterol to inspect relationships. Read counts and category labels. In Rank examine the training feature scores. Supervised ranks use the target, so they must not be computed on the holdout to choose predictors.
4. **Build the tree recipe in Preprocess.** Add **Impute → Average/Most frequent**, then **Select Relevant Features → Gini**, selecting a fixed **8** top features. Preserve that order. The feature selector operates before any categorical expansion. The tree uses this recipe directly without scaling or one-hot encoding.
5. **Build the logistic recipe in Preprocess.** Use **Impute → Average/Most frequent**, **Select Relevant Features → Gini → fixed 8**, **Continuize → One feature per value**, then **Normalize → Standardize to μ = 0, σ² = 1**. The eight selected original predictors may expand into more than eight output columns because categorical levels become indicator features.
6. **Show a before/after preview.** The training split also enters the preview Preprocess widget, which applies **Impute → Average/Most frequent → Select Relevant Features → Gini → fixed 8** and sends **Preprocessed Data** to a cleaned Data Table. Compare the raw training table with this preview: row count should be preserved, missing feature values should be replaced, and eight original feature columns should remain. This preview uses the tree recipe, without encoding or normalization. It is fitted on the full training split only to make preparation visible. Its output must not feed a learner or evaluator.
7. **Fit and cross-validate.** Connect each recipe's **Preprocessor** output to the corresponding learner. Add Constant, Tree (depth **3**, minimum leaf **5**, minimum split **10**), and Logistic Regression (**L2**, **C = 1**). Training rows go directly to each learner and the cross-validation evaluator. Select **Cross-validation**, **5 folds**, stratification, and the saved seed 42. Every fold learns imputation and its own top eight features from its four training folds. Different folds may select different features; this is correct.
8. **Explain the results.** Compare candidates with the majority-class baseline in Test & Score. Inspect Confusion Matrix and ROC Analysis from the cross-validation results, selecting the learner and positive class explicitly. Open Tree Viewer to inspect the complete-training fitted tree. The tree's selected features need not match every fold's selection or the first few features in another ranking method.
9. **Test the full recipe on holdout.** Open the separate holdout Test & Score and select **Test on test data**. It receives training on Data and reserved rows on Test Data. The learner recipes fit using training rows and apply those fitted transformations to holdout. Open Predictions and the connected table to inspect all three fitted models on reserved rows. Do not manually clean or rank the holdout independently.

## Exact channel connections

The table uses role labels to distinguish repeated widget types; [the canvas caption key](../docs/pipeline_concepts.md#canvas-caption-key) maps them to the saved titles. The preview and learner recipe widgets can contain similar steps but serve different purposes.

| Source widget/output | Destination widget/input |
|---|---|
| File / Data | Raw Data Table / Data; Select Columns / Data |
| Select Columns / Data | Data Sampler / Data |
| Data Sampler / Data Sample | Training Data Table / Data; Distributions / Data; Scatter Plot / Data; Box Plot / Data; Rank / Data |
| Data Sampler / Data Sample | Preview Preprocess / Data |
| Preview Preprocess / Preprocessed Data | Cleaned Data Table / Data |
| Tree Preprocess / Preprocessor | Tree / Preprocessor |
| Logistic Preprocess / Preprocessor | Logistic Regression / Preprocessor |
| Data Sampler / Data Sample | Constant / Data; Tree / Data; Logistic Regression / Data |
| Data Sampler / Data Sample | Cross-validation Test & Score / Data; Holdout Test & Score / Data |
| Constant / Learner; Tree / Learner; Logistic Regression / Learner | Cross-validation Test & Score / Learner; Holdout Test & Score / Learner |
| Cross-validation Test & Score / Evaluation Results | Confusion Matrix / Evaluation Results; ROC Analysis / Evaluation Results |
| Tree / Model | Tree Viewer / Tree |
| Data Sampler / Remaining Data | Holdout Data Table / Data; Holdout Test & Score / Test Data; Predictions / Data |
| Constant / Model; Tree / Model; Logistic Regression / Model | Predictions / Predictors |
| Predictions / Predictions | Prediction Data Table / Data |

There is deliberately no connection from Rank's Reduced Data, Preview Preprocess's Preprocessed Data, or a chart's Selected Data to either evaluator. Use the saved canvas captions when checking the actual links.

## Stage expectations

| Stage | Observable check |
|---|---|
| Input | 303 historical rows, 13 original predictors, categorical target; missing values can be inspected. |
| Split/EDA | Only training rows appear in the exploration widgets; holdout remains on its own branch. |
| Cleaning preview | Training row count is unchanged; feature missingness is resolved; eight original predictors remain alongside the target. |
| Learner recipes | Both use fold-local imputation and Gini top-eight selection; only logistic adds encoding and normalization. |
| Cross-validation | Three learner result rows; usable confusion matrix and ROC results; no preview table used as evaluation data. |
| Holdout/prediction | Three independently trained candidate scores and their predictions for the same reserved rows. |

No particular score increase is guaranteed by cleaning or selecting eight predictors. The lesson's success is a correct, inspectable evaluation boundary, not making one candidate win.

## Limits and troubleshooting

Average/mode imputation is a simple baseline: it can reduce variation and hide patterns in missingness. It does not recreate the true unknown measurement. Gini ranks associations with the target, can behave differently for correlated predictors, and does not establish causation. The fixed eight-feature choice is a teaching setting, not a proven optimum. Tuning it using holdout scores would consume the holdout's independence. Historical clinical data and one random split do not establish current clinical validity.

- **No visible imputation change:** compare missing-cell counts, not just the first rows. A split may contain few affected records, and the preview also selects features.
- **More than eight preview features:** check the preview's fixed-eight selector and remove any extra encoding step. The logistic learner internally can use more than eight encoded columns; the saved preview keeps the eight original features plus the target.
- **Preview contains the target:** retaining a target column is normal; it must remain a target, never be included among Features.
- **Validation looks unusually perfect:** inspect target roles and every evaluation input. Disconnect any target-derived predictor, Rank reduction, preprocessed preview, or holdout-fed transformation.
- **Rank and model features differ:** check the score method and fold-local selection. Do not force full-data ranked columns into the evaluator to make the lists match.
- **Empty/error scores:** confirm Data Sample reaches Data, recipes reach Preprocessor, and each learner reaches Learner. Run Apply/Start if required.
- **Missing holdout/predictions:** use Remaining Data on Test Data and Predictions.Data, with fitted Model outputs on Predictions.Predictors. The recipes apply their training-fitted transformations automatically.
- **File path cannot resolve:** reopen File and choose the bundled heart_disease sample, then recheck target roles and split settings.
