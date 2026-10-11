# Workflow provenance and checksums

The four main pipelines use built-in Orange widgets. Five official examples provide supplementary references, and two cleaning examples have updated settings and offline data loading.

## Main course pipelines

| File | Dataset | SHA-256 |
|---|---|---|
| `getting_started/iris_end_to_end.ows` | Bundled iris | `80176288c3531651681c9857ba67b19df0247129d5681c2ca04ab50293f4cdbf` |
| `desc_and_inf_stats/heart_statistics_end_to_end.ows` | Bundled heart_disease | `ecd507ede9e2efe344413f0fca431ea16bb51aed9c3aaa3f542f13da68315d3f` |
| `data_cleaning_and_eda/heart_cleaning_end_to_end.ows` | Bundled heart_disease | `8e718bd319e06c411509821644061188a7daa0b37b268a4dcfb9d6a776c87dce` |
| `simple_multivariate_regression/housing_regression_end_to_end.ows` | Bundled housing | `644333a5e15c94c436c4d4a093291937a29f670d061fb2e3072afaf245a7ff1b` |

These are the complete session workflows for Orange 3.40.0. Their widget settings and connections are documented in the implementation guides.

## Revised cleaning supplements

| File | Current behavior | SHA-256 |
|---|---|---|
| `data_cleaning_and_eda/impute.ows` | Bundled heart data; Average/Most frequent for every predictor; raw and imputed tables | `e7eb60304610de2bb5ad502cba4570b816317548363fd1c2c2472d301ffc744d` |
| `data_cleaning_and_eda/purgedomain.ows` | Bundled heart data and training-only subgroup selection; no online Datasets widget | `3df5862306ff1b62e571faac62c0db5dcd91740f2c8d1b9d3701fdbe97bcc963` |

These examples are based on the Orange documentation workflows at `source/widgets/data/workflows/`. Purge Domain's downstream table waits for a Box Plot subgroup selection; the canvas annotation explains the action.

## Retained official references

| File | Original source | SHA-256 | Bundled data |
|---|---|---|---|
| `getting_started/110-file-and-data-table-widget.ows` | Orange 3.40.0 application, `Orange/canvas/workflows/` | `237afb20e7688c133d108c88314e2609ff52bdb09a03a247003cc91550221ce5` | iris |
| `getting_started/120-scatterplot-data-table.ows` | Orange 3.40.0 application, `Orange/canvas/workflows/` | `46c912614c8a824184291cbf089cffe525411b44472eabd54736cd716b1bd593` | iris |
| `desc_and_inf_stats/distributions.ows` | Documentation, `source/widgets/visualize/workflows/` | `907f34e47f9bbd8119366288b06cccdd00fbab60da5043b167d2710c6aac7056` | heart_disease |
| `desc_and_inf_stats/selectrows.ows` | Documentation, `source/widgets/data/workflows/` | `e73500b223976ea45ab7c112ead2495a241f89dcffeb8fc357e14235faeb71a1` | zoo |
| `simple_multivariate_regression/treeviewer-regression.ows` | Documentation, `source/widgets/visualize/workflows/` | `517a510c11b4236713c96513e1adb6e6fe5e4be835ba52ba58251ba163fba6f9` | housing |

Their checksums match the original course copies. They are small widget demonstrations; use the four main pipelines and implementation guides for the complete lessons.

## Sources and data resolution

The application examples are distributed inside [Orange3](https://github.com/biolab/orange3), and the documentation examples originated in the [Biolab visual-programming documentation repository](https://github.com/biolab/orange3-doc-visual-programming). Their original attribution is retained.

All eleven delivered workflows now load sample data through Orange's `sample-datasets` prefix. The File paths resolve against the recipient's installed Orange, rather than this Mac's filesystem. No CSV copies or online dataset choices are required for the four main lessons.

See the [review checklist and reference results](verification/ml_pipeline_verification.md) for the main workflows.
