# Orange Data Analysis Sessions

Four Orange workflows covering data exploration, preprocessing, feature selection, model building, validation and interpretation.

## Sessions

| Session | Workflow | Implementation guide |
|---|---|---|
| Getting started: Iris classification | [iris_end_to_end.ows](getting_started/iris_end_to_end.ows) | [Guide](getting_started/implementation_guide.md) |
| Descriptive and inferential statistics | [heart_statistics_end_to_end.ows](desc_and_inf_stats/heart_statistics_end_to_end.ows) | [Guide](desc_and_inf_stats/implementation_guide.md) |
| Data cleaning and EDA | [heart_cleaning_end_to_end.ows](data_cleaning_and_eda/heart_cleaning_end_to_end.ows) | [Guide](data_cleaning_and_eda/implementation_guide.md) |
| Simple and multiple regression | [housing_regression_end_to_end.ows](simple_multivariate_regression/housing_regression_end_to_end.ows) | [Guide](simple_multivariate_regression/implementation_guide.md) |

## Run

Open a main `.ows` file in **Orange 3.40.0** using **File → Open**. The workflows use built-in widgets and bundled sample datasets; no add-ons or separate data downloads are required. Allow Test & Score to finish, then follow the session guide to inspect each stage.

Each workflow reserves a 20% holdout and uses five-fold cross-validation on the training rows. Preprocessing connects to learners so it is fitted within each training fold.

## References

- [Pipeline concepts and connections](docs/pipeline_concepts.md)
- [Review checklist and reference results](docs/verification/ml_pipeline_verification.md)
- [Workflow sources and checksums](docs/official_workflows.md)
- [Introductory presentation](getting_started/getting_started.pptx) and [slide source](getting_started/slides.md)

The smaller `.ows` files in each session folder demonstrate individual widgets. `utils/build_ml_workflows.py` and `utils/verify_ml_workflows.py` maintain and validate the main workflows.
