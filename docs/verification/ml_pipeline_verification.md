# Workflow review checklist and reference results

Reference version: Orange 3.40.0. The results below were produced by the saved workflows with their documented settings and bundled datasets. Values are rounded; read the current widget output when reviewing a workflow.

## Review checklist

1. Open the session's main workflow and follow its implementation guide.
2. Confirm the bundled dataset and the feature/target roles in Select Columns.
3. Check the training and holdout row counts below. The two partitions must contain different observations and together account for the full dataset.
4. Trace preprocessing to the learners' **Preprocessor** inputs. Rank, subgroup selections and cleaning previews must not feed Test & Score.
5. Confirm five-fold cross-validation uses training rows, while the separate holdout evaluator uses **Test on test data**.
6. Compare each learner with Constant, then inspect the interpretation widgets and the holdout Predictions table.

## Expected outputs

| Workflow | Training / holdout rows | Outputs to inspect |
|---|---|---|
| Iris | 120 / 30 | Three learners in CV and holdout scoring; 30 holdout predictions with class probabilities; Confusion Matrix, ROC Analysis and training tree |
| Heart statistics | 243 / 60 | Three evaluated learners; 60 holdout predictions; glucose-category-1 subgroup contains 42 training rows |
| Heart cleaning | 243 / 60 | Three evaluated learners; cleaning preview has eight predictors and no missing feature cells; 60 holdout predictions |
| Housing regression | 405 / 101 | Four main learners and a separate RM-only linear model; identical row partitions for both regression branches; 14 multiple-regression coefficient rows and two simple-regression coefficient rows; 101 holdout predictions |

The heart training split contains six missing feature cells before imputation. In the statistics subgroup, every retained `fasting blood sugar > 120` value is category 1. In housing, the coefficient row counts include the intercept.

## Classification accuracy

CA is the fraction of correct predictions. Check the selected target class and averaging convention when interpreting the other classification metrics.

| Workflow | Learner | Training CV CA | Holdout CA |
|---|---|---|---|
| Iris | Constant baseline | 0.3333 | 0.3333 |
| Iris | Logistic regression | 0.9417 | 1.0000 |
| Iris | Shallow tree | 0.9417 | 0.9667 |
| Heart statistics | Constant baseline | 0.5432 | 0.5333 |
| Heart statistics | Logistic regression | 0.8230 | 0.8000 |
| Heart statistics | Shallow tree | 0.7654 | 0.7833 |
| Heart cleaning | Constant baseline | 0.5432 | 0.5333 |
| Heart cleaning | Logistic regression | 0.8395 | 0.8000 |
| Heart cleaning | Shallow tree | 0.7654 | 0.7833 |

## Regression error

RMSE is in the target's units; lower is better. Use the same rows and evaluation mode when comparing models.

| Learner | Training CV RMSE | Holdout RMSE |
|---|---|---|
| Constant baseline | 9.3898 | 8.4809 |
| Simple linear, RM only | 6.7827 | 6.1224 |
| Multiple linear, all 13 predictors | 4.9579 | 4.7420 |
| Shallow tree | 5.2352 | 5.2652 |
| Random forest | 3.6722 | 3.1137 |

Both linear models use ordinary least squares with an intercept and no regularization. Their imputation-only preprocessing preserves units for coefficient interpretation. For the CV observed-versus-predicted Scatter Plot, choose MEDV and the desired model prediction as the axes.

## Supplementary examples

- `impute.ows`: compare the raw heart table with the imputed table; Average/Most frequent fills all six missing feature cells.
- `purgedomain.ows`: select `fasting blood sugar > 120` in Box Plot and click the category-1 segment. The downstream table populates after this selection. Purge Domain removes constant or unused domain values; it does not impute missing cells.
- The remaining small workflows illustrate loading, linked selection, distributions and tree inspection. Use the main workflows for complete model evaluation.

The saved workflow connections match the guides. All four main workflows completed evaluation with finite predictions and disjoint training/holdout partitions, including from a separately extracted copy of the review package. Model scores are reference observations, not guarantees for different data or settings.
