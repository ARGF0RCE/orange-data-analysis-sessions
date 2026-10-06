# Session 1: Getting Started with Orange

- Four sessions, one destination: confident data analysis with Orange.
- Today: Orange basics. Next: statistics, cleaning & EDA, then regression.
- Today's outcomes: read a workflow, check a table, drive a chart, save a recipe.
- Watch and discuss — no software or typing needed on your side.

# Orange vs Python

- Orange is visual data analysis: you connect widgets instead of writing code.
- Python is a programming language: you write instructions yourself.
- In Orange you change a setting and see the result immediately.
- Under the hood Orange runs Python; today you drive it through the canvas.

# The Canvas: Widgets and Connections

- Canvas: the workspace holding one analysis; saved as a single `.ows` file.
- Widget: one block, one job — read data, show a table, draw a chart.
- Connection: from a widget's output (right) to another's input (left).
- The connection carries data — a table of rows — not decoration.

# Where Today's Data Comes From

- Ships with Orange: the iris dataset — no download, no accounts.
- 150 rows: one flower measured per row.
- Four numeric measurements: sepal and petal length and width.
- One categorical outcome: the species, three values.

# Every Column Has a Role

- Feature — an input the analysis may use: the four measurements.
- Target — the column to explain: the species.
- Meta — carried along, never an input: none in today's data.
- The File window shows each column's type and role; check them first.

# Today's Workflow: Two Shipped Examples

- "File and Data Table": one block reads, one shows the rows.
- "Interactive Visualizations": File → Scatter Plot → Data Table.
- The second table is fed by the chart's Selected Data, not by the file.
- Select points in the chart; the table follows live.

# Recap and What Comes Next

- We read a workflow, checked 150 rows, 4 features, 1 outcome.
- We changed axes, selected points, and watched a table follow.
- We saved the recipe — the workflow stores structure, not rows.
- Next session: descriptive and inferential statistics on the same data.
