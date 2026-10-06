# Orange Data Analysis — four session workflows

Orange workflows for a four-part data analysis course delivered to spreadsheet-level beginners: getting started, descriptive and inferential statistics, data cleaning and EDA, and multiple-predictor regression.

## What is in this repository

| Path | What it is |
|---|---|
| `getting_started/110-file-and-data-table-widget.ows` | Official Orange example **"File and Data Table"** — `File → Data Table`. Ships with the Orange application (also in the app under **Welcome → Examples**). |
| `getting_started/120-scatterplot-data-table.ows` | Official Orange example **"Interactive Visualizations"** — `File → Scatter Plot`, with the scatter plot's **Selected Data** driving a `Data Table`. Ships with the Orange application. |
| `getting_started/slides.md`, `getting_started/getting_started.pptx` | Seven-slide introductory deck (Markdown source and PowerPoint build), original to this course. |

Both workflows read Orange's bundled **iris** dataset, so they run offline with no data files.

## Workflows to download from upstream

Sessions 2–4 use five further official examples from the Orange developers' documentation repository, [biolab/orange3-doc-visual-programming](https://github.com/biolab/orange3-doc-visual-programming). They are **not copied here** because that repository declares no licence; download them from their original locations and place them as shown:

| Place the file at | Download from |
|---|---|
| `desc_and_inf_stats/distributions.ows` | https://github.com/biolab/orange3-doc-visual-programming/raw/HEAD/source/widgets/visualize/workflows/distributions.ows |
| `desc_and_inf_stats/selectrows.ows` | https://github.com/biolab/orange3-doc-visual-programming/raw/HEAD/source/widgets/data/workflows/selectrows.ows |
| `data_cleaning_and_eda/impute.ows` | https://github.com/biolab/orange3-doc-visual-programming/raw/HEAD/source/widgets/data/workflows/impute.ows |
| `data_cleaning_and_eda/purgedomain.ows` | https://github.com/biolab/orange3-doc-visual-programming/raw/HEAD/source/widgets/data/workflows/purgedomain.ows |
| `simple_multivariate_regression/treeviewer-regression.ows` | https://github.com/biolab/orange3-doc-visual-programming/raw/HEAD/source/widgets/visualize/workflows/treeviewer-regression.ows |

Their data: `distributions.ows` and `impute.ows` read the bundled `heart_disease.tab`, `selectrows.ows` reads the bundled `zoo.tab`, and `treeviewer-regression.ows` reads the bundled `housing.tab` (numeric target) — all offline.

Note on `purgedomain.ows`: its `Datasets` widget stores `adult.tab`, which is served from Orange's **online** dataset repository and is not shipped with the application, so that workflow opens with empty downstream widgets. Add a `File` widget reading a bundled dataset (for example `heart_disease.tab`) and connect it to the `Box Plot` to use it offline.

## Running them

1. Install Orange 3.x (these were checked against 3.40.0) and open it.
2. Open a `.ows` file with `File → Open…`. In session 1 you can instead use the app's own **Examples** browser on the Welcome screen and pick "File and Data Table" or "Interactive Visualizations".
3. Everything resolves offline from Orange's bundled datasets.

## Licence and attribution

- `getting_started/110-file-and-data-table-widget.ows` and `getting_started/120-scatterplot-data-table.ows` are part of the **Orange3** distribution, which is licensed **GPL-3.0** (see <https://github.com/biolab/orange3>); they are redistributed here verbatim with attribution to the Orange project (Biolab, University of Ljubljana).
- The slides in `getting_started/` are original to this course.
- The five workflows listed under "Workflows to download from upstream" are **not** redistributed here: their upstream repository declares no licence. Obtain them from the links above and respect the upstream terms.
