# Iris: build and read a complete classification pipeline

Open `iris_end_to_end.ows` in Orange. This guide also gives the steps to rebuild it using built-in widgets. Use Orange 3.40's bundled **iris** sample in File; no download, add-on, or Python Script widget is required. Read [pipeline concepts](../docs/pipeline_concepts.md) for the common fit/transform and validation rules.

## Purpose and expected starting data

Predict iris species from four flower measurements. One row is one flower. The shipped table has 150 rows, four numeric features, and a three-class target. Confirm these in File and Data Table; the lesson is about a reproducible process, not reaching a promised accuracy.

## Step by step

1. **Load and inspect.** Open File and select the bundled iris sample. Open the raw Data Table and identify sepal length, sepal width, petal length, petal width, and iris species. In Select Columns, retain all four measurements as features and the species variable as target. Do not turn the species into a feature.
2. **Reserve the test rows.** In Data Sampler choose **Fixed proportion of data**, **80%**, **Replicable sampling**, and **Stratify sample**. `Data Sample` is training; `Remaining Data` is holdout. Expect 120 training and 30 holdout rows. The saved workflow uses Orange's replicable seed 42.
3. **Explore training rows.** Open the training table, Distributions, Scatter Plot, Box Plot, and Rank. Try petal length versus petal width in Scatter Plot and color by species; use Box Plot to compare a measurement across species. Compare how much the groups overlap. In Rank, read the score method and ordered feature names, but keep all four features for this introductory model comparison. Do not connect a selected scatter subset or Rank's reduced output to scoring.
4. **Prepare the model recipes.** The tree preprocessing recipe has **Impute → Average/Most frequent**. The logistic recipe has **Impute → Average/Most frequent**, **Continuize → One feature per value**, then **Normalize → Standardize to μ = 0, σ² = 1**. Send each recipe's `Preprocessor` output to its learner. Iris has no expected missing cells; keeping imputation in the recipe teaches where it belongs.
5. **Train three candidates.** Constant gives a majority-class baseline. Set Tree to maximum depth **3**, minimum leaf size **5**, and minimum subset to split **10**. Set Logistic Regression to **L2 (Ridge)** and **C = 1**. The learner widgets receive training rows to produce models for Predictions. Their unfitted `Learner` outputs also feed the evaluators.
6. **Compare within training.** Open the cross-validation Test & Score: select **Cross-validation**, **5 folds**, and stratification. The saved repeatable evaluation uses seed 42. Compare Constant, Tree, and Logistic Regression using CA, AUC, precision, recall, and F1 as available. Check the class/averaging choice; Iris has three classes. Each fold fits preprocessing afresh.
7. **Explain errors.** Open Confusion Matrix from the cross-validation results, select each learner, and compare the actual-versus-predicted labels. Open ROC Analysis and select one iris class to explain the one-versus-rest trade-off. Open Tree Viewer to see the tree fitted on the complete training split. Its display explains that fitted tree, not all five cross-validation trees.
8. **Evaluate once on the reserved examples.** Open the holdout Test & Score and confirm **Test on test data**. Training comes into `Data`; holdout comes into `Test Data`. Compare its scores with cross-validation and explain possible sampling variation. Do not change settings solely to improve this score and still call it a final untouched test.
9. **Inspect individual predictions.** Open Predictions and the connected prediction table. Each holdout flower should have a true species and model outputs/probabilities. Select an error and relate it to overlapping measurements. Model confidence is not a guarantee of correctness.

## Exact channel connections

Names in this table describe the widget's role; [the canvas caption key](../docs/pipeline_concepts.md#canvas-caption-key) maps them to the saved titles. Double-click a link to inspect its channels. The `Data` inputs on learners fit a model; their `Learner` outputs let Test & Score refit independently.

| Source widget/output | Destination widget/input |
|---|---|
| File / Data | Raw Data Table / Data; Select Columns / Data |
| Select Columns / Data | Data Sampler / Data |
| Data Sampler / Data Sample | Training Data Table / Data; Distributions / Data; Scatter Plot / Data; Box Plot / Data; Rank / Data |
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

## What each stage should show

| Stage | Observable expectation |
|---|---|
| Input | 150 rows, four numeric features, one three-class target; no unexplained target-role change. |
| Split | The training and holdout outputs total 150 rows and are different subsets. |
| Exploration | Charts and ranks update from the training input; a visual selection does not shrink evaluator inputs. |
| Preparation/training | Recipes connect on Preprocessor; three model candidates are available. |
| Cross-validation | A result row for each of three candidates, with no learner error; Confusion Matrix can switch models. |
| Holdout/prediction | Three holdout result rows; Predictions receives 30 rows with predictions from the three fitted models. |

Record the numbers you actually see. This guide specifies settings and checks, not fixed observed scores.

## Interpretation and troubleshooting

The baseline tells you how much accuracy is available from class frequency alone. Petal measurements may separate species better than sepal measurements in a particular view, but a chart or rank alone does not validate a classifier. With only 150 historical observations, one split has substantial limitations and is not a deployment study.

- **File is empty or points to another computer:** reopen File and choose the bundled iris sample; Apply if offered. Do not browse to a stale absolute path.
- **No target/error in Test & Score:** inspect Select Columns; iris species must be a categorical target and the four measurements must be numeric features.
- **No scores:** confirm learners reach `Learner`, then press Apply/Start if automatic execution is off. Models are not the evaluator's learner recipes.
- **Holdout appears missing:** inspect the sampler link and use `Remaining Data → Test Data`; open the evaluator and select **Test on test data**.
- **Different chart axes or class:** explicitly select the intended variables/class in the widget. A view's saved selection can differ across Orange versions.
- **Prediction table missing models:** verify each learner has training Data and that its **Model**, not Learner, reaches Predictions.
- **Unexpected score improvement after edits:** check for target-as-feature, holdout reuse, a selected-only input, or preprocessing data connected directly to scoring. Reopen the supplied workflow to recover the intended structure.
