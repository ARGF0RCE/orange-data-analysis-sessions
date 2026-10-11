# Heart disease: statistics and a complete prediction pipeline

Open `heart_statistics_end_to_end.ows` in Orange. Use the bundled **heart_disease** sample in File. This is an offline teaching workflow using built-in widgets; no add-ons or Python Script widget are needed. The older `distributions.ows` and `selectrows.ows` are smaller examples. See [pipeline concepts](../docs/pipeline_concepts.md) for shared validation rules.

## Purpose and data contract

Describe measurements and groups, distinguish statistical comparisons from predictive evidence, then compare classifiers for the shipped heart-disease target. The bundled table has **303 rows**, **13 features**, and a **two-class target**, named **diameter narrowing**, with categories **0** and **1**. There are **six missing feature cells** in the complete bundled table. Check missing values and feature types in the raw table. These are historical observations; this workflow is not a diagnostic tool or evidence for a treatment decision.

## Step by step

1. **Load the complete table.** In File choose heart_disease from Orange's sample data. Inspect the raw Data Table. Retain the shipped target and all 13 predictors in Select Columns; keep category-coded variables categorical as supplied. A code such as gender or fasting blood sugar is not automatically a continuous measurement.
2. **Split before exploration.** In Data Sampler use **Fixed proportion 80%**, **Replicable sampling**, and **Stratify sample**. Seed 42 is used by Orange's replicable setting. `Data Sample` is training; `Remaining Data` is reserved holdout. In Orange 3.40 expect **243 training rows** and **60 holdout rows**; check the actual counts because rounding and stratification do not imply exact class proportions.
3. **Describe the training distribution.** In Distributions select cholesterol, age, or the target in turn. Read the horizontal variable, counts/density convention, group legend, and missingness before interpreting a pattern. Use Scatter Plot to inspect age versus cholesterol, colored by the target. The training table and Rank also receive only the training split. Rank is exploratory; all 13 predictors remain in the candidate models.
4. **Compare groups in Box Plot.** Set the measured variable to **cholesterol**, the subgroup to **gender**, and enable **Compare means**. Read each group's count, center, spread, and displayed test result. A smaller p-value is not a measure of effect size or predictive accuracy, and does not show gender causes a cholesterol difference. The saved split means these are training-sample statistics, not the full table's historical demonstration numbers. If a group is absent, check the input and category selection.
5. **Inspect a subgroup without redefining training.** In Select Rows choose the feature **fasting blood sugar > 120**, the equality condition, and its category **1**. Inspect Matching Data in the subgroup table. The feature is already an indicator of a threshold; do not set a numeric `> 120` filter on its 0/1 values. This branch answers a descriptive question only. Neither Matching Data nor Unmatched Data feeds the learners or evaluation.
6. **Prepare and train.** Set the tree recipe to **Impute → Average/Most frequent**. Set the logistic recipe to **Impute → Average/Most frequent → Continuize (One feature per value) → Normalize (standard deviation)**. Connect recipes via Preprocessor, so missing-value replacements and encoding/scaling are learned within each validation fold. Use Constant as a baseline, Tree with depth **3**, minimum leaf **5**, minimum split **10**, and Logistic Regression with **L2**, **C = 1**. All three learner widgets receive training rows.
7. **Validate within training.** In the cross-validation Test & Score use **5 folds**, stratification, and the saved seed 42. Compare all three candidates; read the target class/averaging choice alongside CA, AUC, precision, recall, and F1. In Confusion Matrix compare false positives and false negatives for the selected learner. In ROC Analysis explicitly choose the disease class as the positive class before discussing sensitivity/false-positive trade-offs. These costs require a real use context and cannot be determined from the dataset alone.
8. **Interpret the trained tree.** Open Tree Viewer. Explain a root split and a leaf's training count/class mix. This is the tree fitted to the full training split; it is not the set of fold-specific trees and a split is not a causal finding.
9. **Evaluate and predict on holdout.** In the separate holdout Test & Score select **Test on test data**. Confirm training on Data and holdout on Test Data. Open Predictions and its table to compare true labels, predicted labels, and probabilities for reserved examples. Record current scores without substituting historical screenshots. The probabilities are model estimates, not validated clinical risk estimates.

## Exact channel connections

The role labels below distinguish repeated widget types; [the canvas caption key](../docs/pipeline_concepts.md#canvas-caption-key) maps them to the saved titles. Double-click links for channel names.

| Source widget/output | Destination widget/input |
|---|---|
| File / Data | Raw Data Table / Data; Select Columns / Data |
| Select Columns / Data | Data Sampler / Data |
| Data Sampler / Data Sample | Training Data Table / Data; Distributions / Data; Scatter Plot / Data; Box Plot / Data; Rank / Data; Select Rows / Data |
| Select Rows / Matching Data | Subgroup Data Table / Data |
| Data Sampler / Data Sample | Constant / Data; Tree / Data; Logistic Regression / Data |
| Tree Preprocess / Preprocessor | Tree / Preprocessor |
| Logistic Preprocess / Preprocessor | Logistic Regression / Preprocessor |
| Data Sampler / Data Sample | Cross-validation Test & Score / Data; Holdout Test & Score / Data |
| Constant / Learner; Tree / Learner; Logistic Regression / Learner | Cross-validation Test & Score / Learner; Holdout Test & Score / Learner |
| Cross-validation Test & Score / Evaluation Results | Confusion Matrix / Evaluation Results; ROC Analysis / Evaluation Results |
| Tree / Model | Tree Viewer / Tree |
| Data Sampler / Remaining Data | Holdout Data Table / Data; Holdout Test & Score / Test Data; Predictions / Data |
| Constant / Model; Tree / Model; Logistic Regression / Model | Predictions / Predictors |
| Predictions / Predictions | Prediction Data Table / Data |

## Stage checks and interpretation limits

| Stage | What to see |
|---|---|
| Load | 303 rows, 13 predictors, two target classes, visible missing cells where present. |
| Split/explore | EDA widgets use only training rows; subgroup rows are a subset of those rows. |
| Statistics | Box Plot identifies cholesterol, gender, sample counts, and the chosen comparison; report the live values with their sample definition. |
| Preparation | Two recipe outputs feed learners; no subgroup or Rank output enters evaluation. |
| Cross-validation | Three learner result rows and usable confusion/ROC views for the chosen learner/class. |
| Holdout | Three result rows in the separate evaluator and individual predictions on the reserved rows. |

A difference in sample means may reflect age, selection, treatment, measurement, or other confounding. Check the distributions and sample sizes; do not equate a low p-value with a large, useful, or causal effect. Trying many features/groups and reporting only the smallest p-value is selective reporting. The historical clinical sample may differ materially from a current population. Predictive validation on one random holdout does not resolve that limitation.

## Troubleshooting

- **Blank File:** choose Orange's bundled heart_disease sample again. Keep the original target, not a new target made from a convenient predictor.
- **Box Plot does not show a comparison:** select a numeric measurement, a categorical subgroup, and Compare means. Inspect missing rows and groups; do not quote a result from another input table.
- **Subgroup is empty:** use the indicator's category **1**, not a numeric value 120; confirm the actual field name and category in Select Rows.
- **Scores change after selecting chart points:** there should be no selected-data link to the evaluators. Restore the training output directly from Data Sampler.
- **Model errors or no scores:** confirm the categorical target, Preprocessor links, Learner links, and evaluation mode; execute Apply/Start when needed.
- **No holdout results or predictions:** connect Remaining Data to the holdout evaluator's Test Data and Predictions' Data; connect training-fitted Model outputs to Predictions.
- **A chart or statistic differs from an older script:** this pipeline explores a fixed training split. The older full-data example and its screenshot are a different sample; identify the sample before comparing values.
