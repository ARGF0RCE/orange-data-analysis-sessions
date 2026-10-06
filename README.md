# Orange Data Analysis — four session workflows

Orange workflows for a four-part data analysis course delivered to spreadsheet-level beginners: getting started, descriptive and inferential statistics, data cleaning and EDA, and multiple-predictor regression.

## Contents

| Path | Session | What it is |
|---|---|---|
| `getting_started/110-file-and-data-table-widget.ows` | 1 | Official Orange example **"File and Data Table"** — `File → Data Table` |
| `getting_started/120-scatterplot-data-table.ows` | 1 | Official Orange example **"Interactive Visualizations"** — `File → Scatter Plot`, whose **Selected Data** drives a `Data Table` |
| `getting_started/getting_started.pptx` | 1 | Seven-slide introductory deck |
| `desc_and_inf_stats/distributions.ows` | 2 | `File → Distributions → Data Table` (heart disease) |
| `desc_and_inf_stats/selectrows.ows` | 2 | `File → Select Rows → Data Table + Box Plot` (zoo) |
| `data_cleaning_and_eda/impute.ows` | 3 | `File → Impute` with a raw and an imputed table (heart disease) |
| `data_cleaning_and_eda/purgedomain.ows` | 3 | `Datasets → Box Plot → Purge Domain → Distributions` |
| `simple_multivariate_regression/treeviewer-regression.ows` | 4 | `File → Random Forest → Pythagorean Forest → Tree Viewer` (housing, numeric target) |

## Running them

1. Install Orange 3.x (these were checked against 3.40.0) and open it.
2. Open a `.ows` file with `File → Open…`. For session 1 you can instead use the app's own **Examples** browser on the Welcome screen and pick "File and Data Table" or "Interactive Visualizations".
3. Six of the seven workflows read Orange's **bundled** sample datasets (iris, zoo, heart disease, housing) and run offline with no data files.

**Exception — `purgedomain.ows`.** Its `Datasets` widget stores `adult.tab`, which is served from Orange's **online** dataset repository and is not shipped with the application, so that workflow opens with empty downstream widgets. Add a `File` widget reading a bundled dataset (for example `heart_disease.tab`) and connect it to the `Box Plot` to use it offline.

## Provenance

- `getting_started/110-file-and-data-table-widget.ows` and `getting_started/120-scatterplot-data-table.ows` ship with the Orange application itself (`Orange/canvas/workflows/`), and are browsable in the app under **Welcome → Examples**. Orange3 is licensed GPL-3.0 (see <https://github.com/biolab/orange3>); credit the Orange project (Biolab, University of Ljubljana).
- The remaining five workflows come from the Orange developers' documentation repository [biolab/orange3-doc-visual-programming](https://github.com/biolab/orange3-doc-visual-programming), under `source/widgets/<category>/workflows/`, and are included here verbatim. That repository declares no licence of its own, so treat these files as upstream material used with attribution; check with the course owner before reusing them outside this course.
- `getting_started/getting_started.pptx` is original to this course.
