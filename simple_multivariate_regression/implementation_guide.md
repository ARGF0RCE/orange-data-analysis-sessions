# Housing: simple and multiple regression with honest comparisons

Open `housing_regression_end_to_end.ows` in Orange. Use the bundled **housing** dataset; built-in widgets are sufficient and no download, add-on, or Python Script widget is required. This workflow extends the older `treeviewer-regression.ows` example. Read [pipeline concepts](../docs/pipeline_concepts.md) for the common validation and leakage rules.

## Purpose, units, and limitations

Predict **MEDV**, the median value of owner-occupied homes in a census tract, using historical attributes. The bundled dataset has **506 rows**, **13 predictors**, and the continuous target MEDV, recorded in thousands of historical US dollars. **RM** is the average number of rooms per dwelling. The simple regression uses RM alone; the multiple regression uses all 13 supplied predictors. These are tract-level associations, not individual-home appraisals.

The historical dataset includes capped target values and a problematic race-related variable, **B**, constructed from the proportion of Black residents. Keep the documented benchmark intact for this lesson while discussing the discriminatory assumptions and limits of using it. It is not a recommended operational model or feature set for current housing decisions. Coefficients and feature ranks do not establish causal effects.

## Step by step

1. **Load and inspect.** Open File and choose the bundled housing sample. In the raw table confirm MEDV is continuous and appears as the target. In the main Select Columns retain all 13 original features and MEDV as target. Inspect Distributions, Scatter Plot, Box Plot, and Rank on the training branch after the split; try RM against MEDV and use Box Plot for a numeric summary. Do not discard a predictor simply because it is weak in a single two-variable plot.
2. **Make one shared split.** Set Data Sampler to **Fixed proportion 80%**, **Replicable sampling** (seed 42), with stratification off. Data Sample is training (**405 rows** in Orange 3.40) and Remaining Data is holdout (**101 rows**). Check that their row counts sum to 506. Both the simple and multiple regression branches must use these same row identities; do not add a second sampler.
3. **Define the simple-regression columns.** Add one Select Columns on the training output and one on the holdout output. In both keep **RM** as the only feature and **MEDV** as target. Move the other 12 features to Ignored, not Target. The two selectors change columns without changing row membership. Do not train the simple regression on a hand-picked scatter subset.
4. **Prepare inside each learner.** Both saved Preprocess recipes contain **Impute → Average/Most frequent**. Feed the linear recipe's Preprocessor output to both linear learners and the tree recipe's Preprocessor output to Tree and Random Forest. Constant uses only the training target and has no custom feature-preprocessing link. These recipes do not standardize the predictors, so displayed linear coefficients remain in original feature units. Even when no missing cells are present, this shows where imputation is fitted within a fold.
5. **Train all-feature candidates.** Constant is the mean-prediction baseline for regression. Set the multiple Linear Regression to **No regularization** (ordinary least squares), with **Fit intercept** on. Set Tree to maximum depth **3**, minimum leaf **5**, and minimum split **10**. Set Random Forest to **100 trees**, replicable training (seed **0**), maximum depth **6**, and minimum split **5**. Supply the full training output to these widgets.
6. **Train the RM-only candidate.** Connect the RM-only training selector to a second Linear Regression, also **No regularization**, **Fit intercept** on, with imputation via Preprocessor. Rename the two linear learners clearly so prediction and score columns can be distinguished. The simple learner must be evaluated on RM-only data; Test & Score refits a Learner using the evaluator's data, not the data previously sent to the learner widget.
7. **Cross-validate both feature sets.** Use **5-fold Cross-validation**, no stratification, and saved seed **42**. The main evaluator receives full training data and four learners: Constant, multiple Linear Regression, Tree, and Random Forest. A separate evaluator receives RM-only training and the simple Linear Regression learner. Because the row order, seed, and folds match, these are comparable fold assignments. Check the same metric and evaluation settings before comparing the result tables.
8. **Interpret errors and coefficients.** Compare MAE, RMSE, and R². Lower MAE/RMSE is better on the same examples; higher R² is better and it can be negative. Open the coefficient Data Tables for both linear models. Explain the intercept and RM slope in the simple model; in the multiple model, each slope is an association conditional on the other included predictors. Open Tree Viewer to inspect a trained split and leaf prediction. Coefficients and the displayed tree come from the complete training split, whereas cross-validation uses refitted models.
9. **Plot out-of-fold predictions.** Open the Scatter Plot fed by the main cross-validation Test & Score's **Predictions** output. Choose **MEDV** for the observed axis and the desired model's prediction column for the other axis. If the axes are not retained by your Orange version, select them manually. Points far from the imagined observed = predicted diagonal have large errors; curved structure or compression near the target cap suggests systematic limitations. This is a predicted-versus-observed plot, not automatically a residual plot.
10. **Evaluate once on shared holdout.** The main holdout Test & Score uses full training on Data and full holdout on Test Data, with the four all-feature learners. A separate simple-regression holdout evaluator uses RM-only training on Data and RM-only holdout on Test Data, with the simple learner. Set both to **Test on test data**. Compare metrics for the same reserved rows; do not compare a training score with a holdout score.
11. **Compare individual predictions together.** The Predictions widget receives the full holdout and five fitted models: Constant, multiple linear, RM-only linear, Tree, and Random Forest. The RM-only fitted model uses its RM feature from this table. Open the resulting Data Table and inspect examples with large disagreements or errors. Preserve target units and distinguish a model prediction from the observed MEDV.

## Exact channel connections

Role labels distinguish repeated widgets; [the canvas caption key](../docs/pipeline_concepts.md#canvas-caption-key) maps them to the saved titles. Double-click the link to select its channels when rebuilding the canvas.

| Source widget/output | Destination widget/input |
|---|---|
| File / Data | Raw Data Table / Data; All-features Select Columns / Data |
| All-features Select Columns / Data | Data Sampler / Data |
| Data Sampler / Data Sample | Training Data Table / Data; Distributions / Data; Exploratory Scatter Plot / Data; Box Plot / Data; Rank / Data; RM-training Select Columns / Data |
| Data Sampler / Data Sample | Constant / Data; Multiple Linear Regression / Data; Tree / Data; Random Forest / Data |
| Linear Preprocess / Preprocessor | Multiple Linear Regression / Preprocessor; Simple Linear Regression / Preprocessor |
| Tree Preprocess / Preprocessor | Tree / Preprocessor; Random Forest / Preprocessor |
| RM-training Select Columns / Data | Simple Linear Regression / Data; Simple CV Test & Score / Data; Simple Holdout Test & Score / Data |
| Data Sampler / Data Sample | Main CV Test & Score / Data; Main Holdout Test & Score / Data |
| Constant / Learner; Multiple Linear Regression / Learner; Tree / Learner; Random Forest / Learner | Main CV Test & Score / Learner; Main Holdout Test & Score / Learner |
| Simple Linear Regression / Learner | Simple CV Test & Score / Learner; Simple Holdout Test & Score / Learner |
| Multiple Linear Regression / Coefficients | Multiple-coefficients Data Table / Data |
| Simple Linear Regression / Coefficients | Simple-coefficients Data Table / Data |
| Tree / Model | Tree Viewer / Tree |
| Main CV Test & Score / Predictions | Prediction Scatter Plot / Data |
| Data Sampler / Remaining Data | Holdout Data Table / Data; Main Holdout Test & Score / Test Data; RM-holdout Select Columns / Data; Predictions / Data |
| RM-holdout Select Columns / Data | Simple Holdout Test & Score / Test Data |
| Constant / Model; Multiple Linear Regression / Model; Simple Linear Regression / Model; Tree / Model; Random Forest / Model | Predictions / Predictors |
| Predictions / Predictions | Prediction Data Table / Data |

## Stage expectations

| Stage | Observable check |
|---|---|
| Input | 506 rows, 13 original features, numeric MEDV target. |
| Split/columns | One split; full-feature and RM-only tables retain corresponding row identities and row counts. |
| Preparation | Imputation recipes feed the four feature-based learners; Constant uses the training target; no scaled table enters scoring. |
| Cross-validation | Four result rows in the main evaluator; one simple-regression row in its evaluator, using the same fold settings. |
| Interpretation | Both coefficient tables contain an intercept and the relevant slopes; Tree Viewer opens; prediction plot axes can be selected. |
| Holdout/prediction | Four plus one held-out score rows; one combined Predictions view contains outputs from all five models for the same reserved cases. |

No score ordering is guaranteed. A flexible model can fit training patterns well and still perform poorly on reserved examples. Differences between a simple and multiple RM coefficient can reflect adjustment for correlated predictors, not a changed causal effect of adding a room.

## Troubleshooting

- **Classification metrics appear:** MEDV must be a continuous target. Check File and Select Columns rather than converting it to categories.
- **Simple model has 13 coefficients:** ensure its learner receives the RM-only selector and its evaluator also receives RM-only data. Sending a learner to the full-feature evaluator would refit it on all available features.
- **Simple/full scores are not comparable:** verify one sampler, unchanged row order, the same five-fold/seed settings, and corresponding holdout selectors. Never independently sample the RM table.
- **Coefficients look scaled:** remove normalization from the linear Preprocess recipe, keep ordinary least squares and intercept enabled, and rerun both evaluation branches.
- **Scatter Plot shows the wrong variables:** choose MEDV and a model prediction column explicitly; confirm its input is the cross-validation Predictions output, not the original training table.
- **Combined predictions omit RM-only output:** provide the simple learner with RM training data and route its fitted Model to Predictions.Predictors. The full holdout must still include RM with its original name/type.
- **Empty scores:** check Learner rather than Model channels, required training/Test Data inputs, evaluation mode, and Apply/Start.
- **File path fails:** choose the bundled housing sample again and check the named target and RM selector roles before proceeding.
