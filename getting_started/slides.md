# Getting Started with Orange

- Question: can measurements predict species for unseen flowers?
- Today: one complete analysis with the bundled iris data.
- Next: statistics, cleaning and EDA, then regression.
- Watch and discuss. No installation or typing required.

# Orange and Python

- Orange connects ready-made analysis operations visually.
- Python expresses operations through code.
- A widget performs a step. A connection carries an output.
- Outputs include tables, learners, fitted models, and results.

# Six Stages of an Analysis

1. Define the question and useful evidence.
2. Understand rows, columns, and data quality.
3. Prepare features within the learning process.
4. Train a baseline and competing models.
5. Evaluate on rows withheld from fitting.
6. Interpret errors and communicate limits.

# The Iris Dataset

- Bundled with Orange. No download during class.
- 150 flowers, with four numeric measurements each.
- Three recorded species form the categorical target.
- Our expanded course workflow is `iris_end_to_end.ows`.

# Column Roles and Preparation

- Features: sepal and petal measurements.
- Target: species. Meta columns carry labels or identifiers.
- Imputation and scaling learn from training rows.
- Each validation fold fits its own preparation steps.

# Training and Evaluation

- Reserve 20% of rows as a holdout before exploration.
- Explore the 80% training portion and use five-fold CV.
- Compare Constant, Logistic Regression, and Tree.
- Report the separate holdout check after model comparison.

# Interpretation and Next Steps

- Inspect confusion patterns and individual predictions.
- Record the source, split, settings, scores, and limits.
- Save the workflow and use its implementation guide.
- Next session: statistics with the bundled heart data.
