# How the complete pipelines work

These workflows use Orange's built-in widgets and bundled datasets. Open the `.ows` file for a session in Orange; no add-ons, Python Script widget, account, or download is needed during teaching. The accompanying `implementation_guide.md` explains how to inspect or rebuild that session's workflow. The complete pipelines are locally authored teaching workflows; the older official example files remain useful smaller demonstrations.

## Six stages, with a visible result at each stage

| Stage | Orange widgets | What to check before continuing |
|---|---|---|
| 1. Load and define the problem | File, Data Table, Select Columns | One row is one example. Features describe it; the target is the outcome to predict. Check names, types, missing cells, and target role. |
| 2. Prepare data | Data Sampler, Preprocess, Select Columns | Reserve the holdout before inspecting patterns. Learn imputation, encoding, scaling, and supervised feature selection from training data only. |
| 3. Explore and select features | Distributions, Box Plot, Scatter Plot, Rank; Select Relevant Features inside Preprocess for the cleaning lesson | Explain patterns in the training rows. A high rank is a clue, not proof of causation or future usefulness. |
| 4. Train candidate models | Constant, Logistic Regression, Linear Regression, Tree, Random Forest | Start with a baseline and compare models using the same rows. The learner defines a recipe; the model is that recipe fitted to data. |
| 5. Validate and interpret | Test & Score, Confusion Matrix, ROC Analysis, Scatter Plot, Tree Viewer, coefficient Data Table | Compare cross-validation scores and inspect errors. Read uncertainty and limitations alongside a score. |
| 6. Predict on held-out examples | Separate Test & Score in Test on test data mode, Predictions, Data Table | Score and inspect predictions on the reserved rows after making training-stage decisions. Actual targets are available here so errors can be examined. |

## Follow the channel names

Orange links carry different objects. Double-click a link to inspect its source and destination channels.

- **Data** contains rows and columns. **Data Sample** is the training output of Data Sampler; **Remaining Data** is its holdout output.
- **Preprocessor** carries a recipe that can be fitted again. Connect `Preprocess.Preprocessor` to a learner's `Preprocessor` input.
- **Preprocessed Data** contains an already transformed table. The cleaning lesson sends this to a preview table only.
- **Learner** is an unfitted algorithm plus its settings. Send learners to `Test & Score.Learner` so the evaluator can fit each one independently inside each fold.
- **Model** is fitted on the training input of its learner widget. Send models to `Predictions.Predictors`; send holdout rows to `Predictions.Data`.
- **Evaluation Results** is the scored comparison. It feeds Confusion Matrix and ROC Analysis, which inspect that evaluation rather than refitting a model.

Several source widgets can connect to an input that accepts multiple learners or predictors. A line alone is not enough: check the channel names.

## Canvas caption key

The guides use familiar widget roles in their connection tables. The saved workflows use these captions to distinguish repeated widgets. To rebuild a workflow, find the widget type in Orange's toolbox, add it, and rename its canvas caption to match. Open the widget to set the parameters in the session guide, then connect the named channels.

| Guide role / widget type | Saved canvas caption |
|---|---|
| File | `1 Load iris`, `1 Load heart_disease`, or `1 Load housing` |
| Raw Data Table | `Raw data audit` |
| Select Columns / All-features Select Columns | `2 Check features and target` |
| Data Sampler | `3 Reserve 20% holdout` |
| Training Data Table | `Training rows only` |
| Holdout Data Table | `Untouched holdout rows` |
| Rank | `4 Explore feature relevance` |
| Scatter Plot / Exploratory Scatter Plot | `Training relationships` |
| Distributions | `Training distributions` |
| Box Plot | `Training summaries` |
| Logistic Preprocess / Linear Preprocess | `5 Prepare linear model` |
| Tree Preprocess | `5 Prepare tree models` |
| Constant | `6 Constant baseline` |
| Logistic Regression | `6 Logistic regression` |
| Multiple Linear Regression | `6 Multiple linear` |
| Tree | `6 Shallow tree` |
| Random Forest | `6 Random forest` |
| Cross-validation Test & Score / Main CV Test & Score | `7 CV - training only` |
| Holdout Test & Score / Main Holdout Test & Score | `7 Holdout - test once` |
| Predictions | `8 Holdout predictions` |
| Prediction Data Table | `Prediction details` |
| Tree Viewer | `8 Interpret training tree` |
| Confusion Matrix | `8 CV classification errors` |
| ROC Analysis | `8 CV ROC curves` |
| Statistics Select Rows | `EDA subgroup - glucose = 1` |
| Statistics Subgroup Data Table | `EDA subgroup rows` |
| Cleaning Preview Preprocess | `Training cleaning preview only` |
| Cleaned Data Table | `Cleaned training preview` |
| RM-training Select Columns | `RM only - training` |
| RM-holdout Select Columns | `RM only - holdout` |
| Simple Linear Regression | `6 Simple linear - RM` |
| Simple CV Test & Score | `7 Simple linear CV` |
| Simple Holdout Test & Score | `7 Simple linear holdout` |
| Multiple-coefficients Data Table | `Multiple linear coefficients` |
| Simple-coefficients Data Table | `Simple linear coefficients` |
| Prediction Scatter Plot | `CV observed vs predicted` |

Orange may display the evaluator type as **Test and Score** or **Test & Score**. Both refer here to the same widget. `5 Prepare linear model` supplies logistic regression in the classification sessions and ordinary least squares in the housing session. The Preprocess widgets connected only by their Preprocessor outputs do not need a Data input: they transmit an unfitted recipe.

## Fit, transform, and leakage

To **fit** a transformation is to learn its settings from rows: an average for a missing numeric value, a scale for a numeric feature, or the most relevant features using the target. To **transform** is to apply those learned settings to another row.

During five-fold cross-validation, each learner fits its preprocessing and model using four training folds, then transforms and predicts the fifth fold. The held-back fold must not help choose imputation values, scaling, or features. A Preprocessor connection preserves this boundary. Preparing one transformed table first and sending that table into cross-validation would allow information from validation folds into preparation.

The cleaning workflow deliberately has two branches. The preview fits preprocessing on the complete training split to show its effect in a table. The learner branches fit their own preprocessing inside cross-validation. The preview table and Rank's reduced-data output do not feed either evaluator. The target and the holdout rows must never be used as input features.

## Cross-validation and holdout answer different questions

Data Sampler reserves 20% of rows and supplies 80% for training. Its fixed, replicable split makes a demonstration repeatable. Classification uses stratification to approximately preserve class proportions; regression does not. Orange's replicable sampling uses seed 42. Exact row counts and class proportions can reflect Orange's rounding.

The **cross-validation** Test & Score receives only training rows and learners. Five folds means each training row receives a prediction from a model that was not trained on that row. Use this comparison to choose candidates and discuss settings. Scores vary with the split, sample size, and metric; replicability is not evidence of reliability on a different population.

The **holdout** Test & Score receives training rows on `Data`, reserved rows on `Test Data`, and the same learners. Set **Test on test data**. It fits each candidate on the complete training split and scores the reserved examples. The Predictions widget separately shows training-fitted models on those same held-out rows.

Repeatedly selecting settings by holdout performance turns the holdout into another tuning set. If the lesson explores settings after opening holdout results, describe this as an exploratory demonstration; a fresh final test set would be needed for an unbiased final assessment. Random row splitting also assumes examples are sufficiently independent; grouped or time-ordered data need a different split design.

## Read metrics in context

For classification, Constant supplies a majority-class baseline. **CA** is the fraction of correct predictions; compare it with class balance. **Precision** asks how often predicted positives are correct; **recall** asks how many actual positives are found. **F1** combines precision and recall. Check the selected target class and averaging convention before reading a summary. **AUC** measures ranking across thresholds, not the percentage of correct decisions. Confusion Matrix shows which labels are confused; check whether counts or proportions are displayed. ROC Analysis shows threshold trade-offs for the selected positive class; a default threshold need not suit a real decision.

For regression, Constant predicts a training-derived constant. **MAE** is average absolute error and **RMSE** weights large errors more strongly; both retain the target's units. **R²** compares squared error with a constant-reference prediction and can be negative on unseen examples. A higher R² does not prove causation or remove systematic errors. Compare models on the same rows, metric, and evaluation mode. For housing, MEDV is recorded in thousands of historical US dollars, so an MAE of 1 would mean 1,000 historical dollars; this is a unit example, not an observed score.

## Statistics, explanation, and prediction

A group mean or distribution describes the observed sample. A p-value in Box Plot evaluates a statistical null hypothesis under assumptions; it does not measure the size of an effect, the chance that the hypothesis is true, or a model's predictive accuracy. Look at group counts, distributions, missingness, effect size, and plausible confounding. Multiple exploratory comparisons increase the chance of apparently small p-values.

Tree splits, feature rankings, and regression coefficients describe fitted associations. Correlated features can share or swap apparent importance. A multiple-regression coefficient is conditional on the included features and model assumptions, whereas a simple-regression slope describes an unadjusted association. Neither alone establishes an intervention's effect.

Iris, heart disease, and housing are historical teaching datasets. Their convenience and compact size do not establish representativeness, clinical validity, fairness, or readiness for deployment. The housing dataset includes a historically problematic race-related variable, B, defined using the proportion of Black residents. Discuss its provenance and discriminatory assumptions; its inclusion here preserves a documented benchmark demonstration, not a recommended feature set for operational housing decisions. The heart workflow is a classification lesson, not a diagnostic system.

## A quick connection audit

1. Open File and confirm the bundled dataset, then inspect target roles in Select Columns.
2. Open Data Sampler: fixed proportion 80%, replicable; stratification on only for classification.
3. Trace `Data Sample` to exploration, model training, and each evaluator's `Data` input.
4. Trace `Remaining Data` only to holdout evaluation/prediction paths, including the matching one-feature selector in simple regression.
5. Check that learner preprocessing arrives on **Preprocessor**, and no transformed preview or ranked reduction reaches scoring.
6. Check five-fold cross-validation and the separate **Test on test data** evaluator. Inspect current results directly; do not substitute a historical screenshot or a promised numerical score.
