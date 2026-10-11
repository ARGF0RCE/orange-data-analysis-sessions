"""Execute saved Orange workflows and record their actual validation results."""
# /// script
# requires-python = ">=3.12"
# dependencies = ["Orange3==3.40.0"]
# ///
# How to run: QT_QPA_PLATFORM=offscreen <Orange bundled python> -m utils.verify_ml_workflows
# No participant workflow requires Python; this is a maintainer verification tool.
from __future__ import annotations

import importlib
from importlib.metadata import version
import json
import sys
from pathlib import Path
from typing import Final
from xml.etree import ElementTree

import numpy as np
from AnyQt.QtCore import QEventLoop, QTimer
from AnyQt.QtWidgets import QApplication
from Orange.data import Table
from Orange.evaluation import AUC, CA, F1, MAE, RMSE, R2, Results
from Orange.evaluation.scoring import Score
from Orange.widgets.data.owfile import OWFile
from Orange.widgets.evaluate.owtestandscore import InputLearner, OWTestAndScore, Try, results_merge
from Orange.widgets.widget import OWWidget
from orangecanvas.registry.base import WidgetRegistry
from orangecanvas.registry.description import WidgetDescription
from orangecanvas.scheme.signalmanager import LazyValue
from orangewidget.utils.messages import MessageGroup
from orangewidget.workflow.widgetsscheme import WidgetsScheme

from utils.build_ml_workflows import CASES, ROOT

OUTPUT: Final = ROOT / "docs/verification/ml_pipeline_results.json"


def metric_values(scorer: type[Score], results: Results, *, weighted: bool = False) -> list[float]:
    values = scorer(results, average="weighted") if weighted else scorer(results)
    assert isinstance(values, np.ndarray)
    return [float(value) for value in values]


def active_messages(widget: OWWidget, severity: int) -> list[str]:
    messages: list[str] = []
    for group in widget.message_groups:
        assert isinstance(group, MessageGroup)
        group_severity = getattr(group, "severity")
        assert isinstance(group_severity, int)
        messages.extend(str(message) for message in group.active if group_severity == severity)
    return messages


def run_workflow(path: Path) -> None:
    registry = WidgetRegistry()
    for element in ElementTree.parse(path).findall("./nodes/node"):
        qualified_name = element.attrib["qualified_name"]
        if registry.has_widget(qualified_name):
            continue
        module_name, class_name = qualified_name.rsplit(".", 1)
        cls = getattr(importlib.import_module(module_name), class_name)
        if not isinstance(cls, type) or not issubclass(cls, OWWidget):
            raise TypeError(qualified_name, "not an Orange widget class")
        registry.register_widget(WidgetDescription(name=cls.name, id=module_name, qualified_name=qualified_name, inputs=cls.get_signals("inputs", True), outputs=cls.get_signals("outputs", True), icon=cls.icon))
    scheme = WidgetsScheme(env={"basedir": str(path.parent)})
    loop = QEventLoop()
    timer = QTimer()
    timer.setSingleShot(True)
    _ = timer.timeout.connect(loop.quit)
    _ = scheme.signal_manager.finished.connect(loop.quit)
    with path.open("rb") as stream:
        scheme.load_from(stream, registry=registry)
    widgets: dict[str, OWWidget] = {}
    for node in scheme.nodes:
        widget = scheme.widget_for_node(node)
        assert isinstance(widget, OWWidget), (path, node.title)
        widgets[node.title] = widget
    timer.start(60000)
    _ = loop.exec()
    if not timer.isActive():
        raise TimeoutError(path)
    timer.stop()
    messages = []
    for title, widget in widgets.items():
        messages.extend((title, message) for message in active_messages(widget, widget.Error.severity))
    if messages:
        raise RuntimeError(messages)
    cv = widgets["7 CV - training only"]
    holdout = widgets["7 Holdout - test once"]
    assert isinstance(cv, OWTestAndScore)
    assert isinstance(holdout, OWTestAndScore)
    train, test = cv.data, holdout.test_data
    if not isinstance(train, Table) or not isinstance(test, Table):
        raise RuntimeError(path, "data did not reach validation")
    assert set(train.ids).isdisjoint(test.ids)
    source = widgets[next(t for t in widgets if t.startswith("1 Load"))]
    assert isinstance(source, OWFile)
    assert isinstance(source.data, Table)
    assert len(train) + len(test) == len(source.data)
    evaluations = []
    for title, widget in widgets.items():
        if isinstance(widget, OWTestAndScore):
            slots = list(widget.learners.values())
            result_values: list[Results] = []
            model_names: list[str] = []
            for slot in slots:
                assert isinstance(slot, InputLearner)
                assert isinstance(slot.results, Try.Success), (path, title, slot)
                assert isinstance(slot.results.value, Results)
                result_values.append(slot.results.value)
                model_names.append(slot.learner.name)
            results = results_merge(result_values)
            assert isinstance(results, Results), (path, title, "no evaluation output")
            assert isinstance(results.predicted, np.ndarray)
            assert isinstance(results.actual, np.ndarray)
            assert len(results.predicted) == len(widget.learners)
            assert np.isfinite(results.predicted).all()
            metrics = {"RMSE": metric_values(RMSE, results), "MAE": metric_values(MAE, results), "R2": metric_values(R2, results)} if train.domain.has_continuous_class else {"AUC": metric_values(AUC, results), "CA": metric_values(CA, results), "F1": metric_values(F1, results, weighted=True)}
            evaluations.append({"widget": title, "rows_evaluated": len(results.actual), "models": model_names, "metrics": metrics})
    if "RM only - training" in widgets:
        simple_cv = widgets["7 Simple linear CV"]
        simple_test = widgets["7 Simple linear holdout"]
        assert isinstance(simple_cv, OWTestAndScore)
        assert isinstance(simple_test, OWTestAndScore)
        assert isinstance(simple_cv.data, Table)
        assert isinstance(simple_test.test_data, Table)
        assert [v.name for v in simple_cv.data.domain.attributes] == ["RM"]
        assert np.array_equal(simple_cv.data.ids, train.ids)
        assert np.array_equal(simple_test.test_data.ids, test.ids)
    previews = []
    for link in scheme.links:
        if link.source_channel.name in ("Preprocessed Data", "Predictions", "Coefficients", "Matching Data"):
            for signal in scheme.signal_manager.signals_on_link(link):
                value = signal.value
                if LazyValue.is_lazy(value):
                    value = value.get_value()
                if isinstance(value, Table):
                    table = value
                    if link.source_node.title == "EDA subgroup - glucose = 1":
                        assert len(table) < len(train)
                        assert np.all(table.get_column("fasting blood sugar > 120") == 1)
                    previews.append({"source": link.source_node.title, "rows": len(table), "features": [v.name for v in table.domain.attributes], "metas": [v.name for v in table.domain.metas], "missing_feature_cells": int(np.isnan(table.X).sum())})
    predictions = next(v for v in previews if v["source"] == "8 Holdout predictions")
    assert predictions["rows"] == len(test)
    assert {"Constant baseline", "Shallow tree"}.issubset(predictions["metas"])
    if "Training cleaning preview only" in widgets:
        preview = next(v for v in previews if v["source"] == "Training cleaning preview only")
        assert preview["missing_feature_cells"] == 0
        assert len(preview["features"]) == 8
    record = {"workflow": str(path.relative_to(ROOT)), "nodes": len(scheme.nodes), "links": len(scheme.links), "training_rows": len(train), "holdout_rows": len(test), "training_missing_feature_cells": int(np.isnan(train.X).sum()), "disjoint_split": True, "evaluations": evaluations, "outputs": previews, "warnings": [(title, message) for title, widget in widgets.items() for message in active_messages(widget, widget.Warning.severity)]}
    records.append(record)
    print(json.dumps(record, indent=2), flush=True)
    scheme.clear()
    scheme.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    records = []
    paths = [Path(value).resolve() for value in sys.argv[1:]] or [ROOT / case[0] for case in CASES]
    for path in paths:
        run_workflow(path)
    _ = OUTPUT.write_text(json.dumps({"orange_version": version("Orange3"), "python": sys.version, "workflows": records}, indent=2) + "\n", encoding="utf-8")
