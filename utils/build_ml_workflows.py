"""Build the four teaching pipelines with Orange's native scheme serializer."""
# /// script
# requires-python = ">=3.12"
# dependencies = ["Orange3==3.40.0"]
# ///
# How to run: use the installed Orange Python, with QT_QPA_PLATFORM=offscreen.
# This preserves the application's exact widget version; it installs nothing.
from __future__ import annotations

from pathlib import Path
from typing import Final
from xml.etree import ElementTree

from AnyQt.QtWidgets import QApplication
from Orange.data import Table
from Orange.preprocess import Continuize
from Orange.widgets.data.owdatasampler import OWDataSampler
from Orange.widgets.data.owfile import OWFile
from Orange.widgets.data.owimpute import OWImpute
from Orange.widgets.data.owpreprocess import OWPreprocess
from Orange.widgets.data.owpurgedomain import OWPurgeDomain
from Orange.widgets.data.owrank import OWRank
from Orange.widgets.data.owselectcolumns import OWSelectAttributes
from Orange.widgets.data.owselectrows import OWSelectRows
from Orange.widgets.data.owtable import OWTable
from Orange.widgets.evaluate.owconfusionmatrix import OWConfusionMatrix
from Orange.widgets.evaluate.owpredictions import OWPredictions
from Orange.widgets.evaluate.owrocanalysis import OWROCAnalysis
from Orange.widgets.evaluate.owtestandscore import OWTestAndScore
from Orange.widgets.model.owconstant import OWConstant
from Orange.widgets.model.owlinearregression import OWLinearRegression
from Orange.widgets.model.owlogisticregression import OWLogisticRegression
from Orange.widgets.model.owrandomforest import OWRandomForest
from Orange.widgets.model.owtree import OWTreeLearner
from Orange.widgets.visualize.owboxplot import OWBoxPlot
from Orange.widgets.visualize.owdistributions import OWDistributions
from Orange.widgets.visualize.owscatterplot import OWScatterPlot
from Orange.widgets.visualize.owtreeviewer import OWTreeGraph
from Orange.widgets.widget import OWWidget
from orangecanvas.registry.description import WidgetDescription
from orangecanvas.scheme.annotations import SchemeTextAnnotation
from orangecanvas.scheme.link import SchemeLink
from orangecanvas.scheme.node import SchemeNode
from orangecanvas.scheme.readwrite import scheme_to_etree
from orangecanvas.scheme.scheme import Scheme
from orangewidget.utils.filedialogs import RecentPath

ROOT: Final = Path(__file__).resolve().parents[1]
CASES: Final = (
    ("getting_started/iris_end_to_end.ows", "iris", "Iris: from measurements to species"),
    ("desc_and_inf_stats/heart_statistics_end_to_end.ows", "heart_disease", "Heart data: statistics and prediction"),
    ("data_cleaning_and_eda/heart_cleaning_end_to_end.ows", "heart_disease", "Heart data: cleaning and feature selection"),
    ("simple_multivariate_regression/housing_regression_end_to_end.ows", "housing", "Housing: simple and multiple linear regression"),
)


class Pipeline:
    """Accumulate native nodes and links for one teaching artifact."""

    def __init__(self, title: str) -> None:
        self.scheme: Scheme = Scheme(title=title, description="End-to-end teaching pipeline. Follow the numbered stages and the implementation guide. EDA/preview branches are separate from validation; preprocessing is fitted inside learner training.")

    def add(self, cls: type[OWWidget], title: str, xy: tuple[int, int]) -> SchemeNode:
        desc = WidgetDescription(name=cls.name, id=cls.__module__, qualified_name=cls.__module__ + "." + cls.__name__, inputs=cls.get_signals("inputs", True), outputs=cls.get_signals("outputs", True), icon=cls.icon)
        node = SchemeNode(desc, title=title, position=xy, properties={"__version__": cls.settings_version, "context_settings": []})
        self.scheme.add_node(node)
        return node

    def connect(self, source: SchemeNode, sink: SchemeNode, channels: tuple[str, str] = ("Data", "Data")) -> None:
        self.scheme.add_link(SchemeLink(source, source.output_channel(channels[0]), sink, sink.input_channel(channels[1])))

    def note(self, text: str, rect: tuple[int, int, int, int]) -> None:
        self.scheme.add_annotation(SchemeTextAnnotation(rect, text, font={"family": "Helvetica", "size": 15}))

    def save(self, relative_path: str) -> None:
        with (ROOT / relative_path).open("wb") as stream:
            tree = scheme_to_etree(self.scheme, data_format="pickle")
            ElementTree.indent(tree, space="  ")
            tree.write(stream, encoding="utf-8", xml_declaration=True)
        print(relative_path, len(self.scheme.nodes), "widgets", len(self.scheme.links), "links")


def configure_columns(node: SchemeNode, data: Table, names: tuple[str, ...]) -> None:
    """Persist an explicit domain-role choice using Orange's context handler."""
    widget = OWSelectAttributes.__new__(OWSelectAttributes, stored_settings={"context_settings": []})
    widget.__init__()
    widget.set_data(data)
    widget.used_attrs[:] = [data.domain[name] for name in names]
    widget.available_attrs[:] = [v for v in data.domain.attributes if v.name not in names]
    widget.update_domain_role_hints()
    widget.closeContext()
    node.properties = widget.settingsHandler.pack_data(widget)
    widget.onDeleteWidget()


def build_case(case_index: int) -> None:
    relative_path, dataset, title = CASES[case_index]
    regression, cleaning = case_index == 3, case_index == 2
    data = Table(dataset)
    p = Pipeline(title)
    file = p.add(OWFile, "1 Load " + dataset, (90, 150))
    file.properties.update(recent_paths=[RecentPath("", "sample-datasets", dataset + ".tab")], source=0)
    raw = p.add(OWTable, "Raw data audit", (90, 320))
    roles = p.add(OWSelectAttributes, "2 Check features and target", (290, 150))
    configure_columns(roles, data, tuple(v.name for v in data.domain.attributes))
    split = p.add(OWDataSampler, "3 Reserve 20% holdout", (490, 150))
    split.properties.update(sampling_type=0, sampleSizePercentage=80, use_seed=True, stratify=not regression, replacement=False)
    train = p.add(OWTable, "Training rows only", (690, 150))
    test = p.add(OWTable, "Untouched holdout rows", (690, 510))
    rank = p.add(OWRank, "4 Explore feature relevance", (890, 150))
    scatter = p.add(OWScatterPlot, "Training relationships", (290, 320))
    dist = p.add(OWDistributions, "Training distributions", (490, 320))
    box = p.add(OWBoxPlot, "Training summaries", (690, 320))
    if case_index == 1:
        plot = OWBoxPlot.__new__(OWBoxPlot, stored_settings={"context_settings": []})
        plot.__init__()
        plot.set_data(data)
        plot.attribute = data.domain["cholesterol"]
        plot.group_var = data.domain["gender"]
        plot.closeContext()
        box.properties = plot.settingsHandler.pack_data(plot)
        plot.onDeleteWidget()
    p.connect(file, raw)
    p.connect(file, roles)
    p.connect(roles, split)
    for sink in (train, rank, scatter, dist, box):
        p.connect(split, sink, ("Data Sample", "Data"))
    p.connect(split, test, ("Remaining Data", "Data"))
    impute = ("orange.preprocess.impute", {"method": 2})
    selection = ("orange.preprocess.fss", {"score": 2, "strategy": 1, "k": 8})
    tree_steps = [impute] + ([selection] if cleaning else [])
    linear_steps = tree_steps if regression else tree_steps + [("orange.preprocess.continuize", {"multinomial_treatment": Continuize.Indicators}), ("orange.preprocess.scale", {"method": 2})]
    prep = p.add(OWPreprocess, "5 Prepare linear model", (890, 350))
    prep.properties.update(storedsettings={"preprocessors": linear_steps}, autocommit=True)
    tree_prep = p.add(OWPreprocess, "5 Prepare tree models", (890, 530))
    tree_prep.properties.update(storedsettings={"preprocessors": tree_steps}, autocommit=True)
    baseline = p.add(OWConstant, "6 Constant baseline", (1090, 150))
    baseline.properties.update(learner_name="Constant baseline")
    linear_cls = OWLinearRegression if regression else OWLogisticRegression
    linear = p.add(linear_cls, "6 Multiple linear" if regression else "6 Logistic regression", (1090, 320))
    linear.properties.update(learner_name="Multiple linear" if regression else "Logistic regression", reg_type=0, fit_intercept=True, penalty_type=1, C_index=61)
    tree = p.add(OWTreeLearner, "6 Shallow tree", (1090, 500))
    tree.properties.update(learner_name="Shallow tree", limit_depth=True, max_depth=3, limit_min_leaf=True, min_leaf=5, limit_min_internal=True, min_internal=10)
    cv = p.add(OWTestAndScore, "7 CV - training only", (1290, 200))
    cv.properties.update(resampling=0, n_folds=2, cv_stratified=not regression)
    holdout = p.add(OWTestAndScore, "7 Holdout - test once", (1290, 500))
    holdout.properties.update(resampling=5)
    pred = p.add(OWPredictions, "8 Holdout predictions", (1490, 500))
    pred_table = p.add(OWTable, "Prediction details", (1690, 500))
    viewer = p.add(OWTreeGraph, "8 Interpret training tree", (1090, 690))
    p.connect(prep, linear, ("Preprocessor", "Preprocessor"))
    p.connect(tree_prep, tree, ("Preprocessor", "Preprocessor"))
    for score in (cv, holdout):
        p.connect(split, score, ("Data Sample", "Data"))
    p.connect(split, holdout, ("Remaining Data", "Test Data"))
    p.connect(split, pred, ("Remaining Data", "Data"))
    p.connect(pred, pred_table, ("Predictions", "Data"))
    p.connect(tree, viewer, ("Model", "Tree"))
    learners = [baseline, linear, tree]
    if regression:
        forest = p.add(OWRandomForest, "6 Random forest", (1090, 860))
        forest.properties.update(learner_name="Random forest", n_estimators=100, use_random_state=True, use_max_depth=True, max_depth=6, use_min_samples_split=True, min_samples_split=5)
        p.connect(tree_prep, forest, ("Preprocessor", "Preprocessor"))
        learners.append(forest)
        coef = p.add(OWTable, "Multiple linear coefficients", (1490, 320))
        errors = p.add(OWScatterPlot, "CV observed vs predicted", (1490, 150))
        p.connect(linear, coef, ("Coefficients", "Data"))
        p.connect(cv, errors, ("Predictions", "Data"))
        one_train = p.add(OWSelectAttributes, "RM only - training", (290, 690))
        one_test = p.add(OWSelectAttributes, "RM only - holdout", (290, 870))
        for node in (one_train, one_test):
            configure_columns(node, data, ("RM",))
        p.connect(split, one_train, ("Data Sample", "Data"))
        p.connect(split, one_test, ("Remaining Data", "Data"))
        simple = p.add(OWLinearRegression, "6 Simple linear - RM", (490, 690))
        simple.properties.update(learner_name="Simple linear RM", reg_type=0, fit_intercept=True)
        p.connect(prep, simple, ("Preprocessor", "Preprocessor"))
        p.connect(one_train, simple)
        simple_cv = p.add(OWTestAndScore, "7 Simple linear CV", (690, 690))
        simple_cv.properties.update(resampling=0, n_folds=2, cv_stratified=False)
        simple_test = p.add(OWTestAndScore, "7 Simple linear holdout", (690, 870))
        simple_test.properties.update(resampling=5)
        for score in (simple_cv, simple_test):
            p.connect(one_train, score)
            p.connect(simple, score, ("Learner", "Learner"))
        p.connect(one_test, simple_test, ("Data", "Test Data"))
        one_coef = p.add(OWTable, "Simple linear coefficients", (490, 870))
        p.connect(simple, one_coef, ("Coefficients", "Data"))
        p.connect(simple, pred, ("Model", "Predictors"))
    else:
        confusion = p.add(OWConfusionMatrix, "8 CV classification errors", (1490, 150))
        roc = p.add(OWROCAnalysis, "8 CV ROC curves", (1490, 320))
        p.connect(cv, confusion, ("Evaluation Results", "Evaluation Results"))
        p.connect(cv, roc, ("Evaluation Results", "Evaluation Results"))
    for learner in learners:
        p.connect(split, learner, ("Data Sample", "Data"))
        for score in (cv, holdout):
            p.connect(learner, score, ("Learner", "Learner"))
        p.connect(learner, pred, ("Model", "Predictors"))
    if cleaning:
        preview = p.add(OWPreprocess, "Training cleaning preview only", (490, 690))
        preview.properties.update(storedsettings={"preprocessors": tree_steps}, autocommit=True)
        clean_table = p.add(OWTable, "Cleaned training preview", (690, 690))
        p.connect(split, preview, ("Data Sample", "Data"))
        p.connect(preview, clean_table, ("Preprocessed Data", "Data"))
    if case_index == 1:
        subgroup = p.add(OWSelectRows, "EDA subgroup - glucose = 1", (290, 690))
        widget = OWSelectRows.__new__(OWSelectRows, stored_settings={"context_settings": []})
        widget.__init__()
        widget.set_data(data)
        widget.remove_all_rows()
        widget.add_row(data.domain["fasting blood sugar > 120"], 0, (2,))
        widget.conditions_changed()
        widget.closeContext()
        subgroup.properties = widget.settingsHandler.pack_data(widget)
        widget.onDeleteWidget()
        subgroup_table = p.add(OWTable, "EDA subgroup rows", (490, 690))
        p.connect(split, subgroup, ("Data Sample", "Data"))
        p.connect(subgroup, subgroup_table, ("Matching Data", "Data"))
    p.note("1-2 Load and check roles", (10, 20, 380, 60))
    p.note("3 Split first\nTraining = Data Sample; holdout = Remaining Data", (410, 20, 400, 75))
    p.note("4-6 Explore, preprocess and build\nPreprocessor methods go to learners", (830, 20, 370, 75))
    p.note("7-8 Validate and interpret\nCV uses training only; holdout is a final check", (1230, 20, 500, 75))
    p.note("EDA and cleaning previews do not feed scoring. Rank is explanatory; learned selection belongs inside Preprocess. See implementation_guide.md for the teaching sequence and settings.", (10, 1030 if regression else 860, 1680, 65))
    p.save(relative_path)


def build_cleaning_demos() -> None:
    p = Pipeline("Impute: complete before and after preview")
    file = p.add(OWFile, "File", (90, 150))
    file.properties.update(recent_paths=[RecentPath("", "sample-datasets", "heart_disease.tab")], source=0)
    impute = p.add(OWImpute, "Impute - Average / Most frequent", (290, 150))
    impute.properties.update(_default_method_index=2, autocommit=True)
    raw = p.add(OWTable, "Raw data - 6 missing feature cells", (90, 350))
    clean = p.add(OWTable, "Imputed data - no missing features", (490, 150))
    p.connect(file, raw)
    p.connect(file, impute)
    p.connect(impute, clean)
    p.note("Cleaning preview only. For ML validation use heart_cleaning_end_to_end.ows: fit imputation inside each training fold.", (10, 30, 700, 80))
    p.save("data_cleaning_and_eda/impute.ows")
    p = Pipeline("Purge Domain: offline training subgroup demonstration")
    file = p.add(OWFile, "File - bundled heart data", (90, 150))
    file.properties.update(recent_paths=[RecentPath("", "sample-datasets", "heart_disease.tab")], source=0)
    split = p.add(OWDataSampler, "Training partition only", (290, 150))
    split.properties.update(sampling_type=0, sampleSizePercentage=80, use_seed=True, stratify=True)
    box = p.add(OWBoxPlot, "Select a categorical subgroup", (490, 150))
    purge = p.add(OWPurgeDomain, "Purge Domain", (690, 150))
    table = p.add(OWTable, "Subgroup after domain cleanup", (890, 150))
    p.connect(file, split)
    p.connect(split, box, ("Data Sample", "Data"))
    p.connect(box, purge, ("Selected Data", "Data"))
    p.connect(purge, table)
    p.note("Offline: select fasting blood sugar > 120 in Box Plot, then click the 1 segment. Purge removes constant/unused domain values; it does not repair missing cells. This EDA selection never feeds model validation.", (10, 30, 950, 85))
    p.save("data_cleaning_and_eda/purgedomain.ows")


if __name__ == "__main__":
    app = QApplication([])
    for index in range(len(CASES)):
        build_case(index)
    build_cleaning_demos()
