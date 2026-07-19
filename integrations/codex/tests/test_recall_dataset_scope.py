"""Regression tests for dataset-scoped managed-endpoint recall."""

import pathlib
import sys

sys.path.insert(
    0, str(pathlib.Path(__file__).resolve().parents[1] / "plugins" / "cognee" / "scripts")
)

import _plugin_common as pc  # noqa: E402


def test_recall_via_http_forwards_datasets():
    recorded = {}
    saved_request = pc._json_http_request

    def capture(path, payload, **kwargs):
        recorded.update(path=path, payload=payload, kwargs=kwargs)
        return []

    pc._json_http_request = capture
    try:
        pc.recall_via_http(
            "project marker",
            session_id="session-1",
            top_k=5,
            scope=["graph_context"],
            datasets=["agent_sessions"],
        )
    finally:
        pc._json_http_request = saved_request

    assert recorded["path"] == "/api/v1/recall"
    assert recorded["payload"]["datasets"] == ["agent_sessions"]
