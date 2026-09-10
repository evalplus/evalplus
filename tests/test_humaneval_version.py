import hashlib
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from evalplus.data import humaneval
from evalplus.data import utils as data_utils


@pytest.fixture
def cached_versions(monkeypatch, tmp_path):
    monkeypatch.setattr(data_utils, "CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(humaneval, "HUMANEVAL_OVERRIDE_PATH", None)
    cache = Mock()
    monkeypatch.setattr(humaneval, "make_cache", cache)
    return cache


@pytest.mark.parametrize("version", ["default", "v0.1.9"])
@pytest.mark.parametrize(
    "mini,noextreme", [(False, False), (True, False), (False, True)]
)
@pytest.mark.parametrize("operation", ["load", "hash"])
def test_humaneval_load_and_hash_use_requested_version(
    cached_versions, version, mini, noextreme, operation
):
    resolved_version = (
        humaneval.HUMANEVAL_PLUS_VERSION if version == "default" else version
    )
    url, cache_path = data_utils.get_dataset_metadata(
        "HumanEvalPlus", resolved_version, mini, noextreme
    )
    task = {
        "task_id": "HumanEval/0",
        "prompt": resolved_version,
        "contract": "",
        "canonical_solution": "pass",
        "base_input": [],
        "plus_input": [],
        "atol": 0,
    }
    content = (json.dumps(task) + "\n").encode()
    Path(cache_path).write_bytes(content)
    if resolved_version != humaneval.HUMANEVAL_PLUS_VERSION:
        _, default_path = data_utils.get_dataset_metadata(
            "HumanEvalPlus", humaneval.HUMANEVAL_PLUS_VERSION, mini, noextreme
        )
        default_task = {**task, "prompt": humaneval.HUMANEVAL_PLUS_VERSION}
        Path(default_path).write_text(json.dumps(default_task) + "\n")

    if operation == "load":
        assert humaneval.get_human_eval_plus(
            mini=mini, noextreme=noextreme, version=version
        ) == {task["task_id"]: task}
    else:
        assert (
            humaneval.get_human_eval_plus_hash(
                mini=mini, noextreme=noextreme, version=version
            )
            == hashlib.md5(content).hexdigest()
        )
    cached_versions.assert_called_once_with(url, cache_path)


def test_humaneval_override_path_takes_precedence(
    cached_versions, monkeypatch, tmp_path
):
    override_path = tmp_path / "override.jsonl"
    content = b'{"task_id":"HumanEval/0","prompt":"override"}\n'
    override_path.write_bytes(content)
    monkeypatch.setattr(humaneval, "HUMANEVAL_OVERRIDE_PATH", str(override_path))

    assert humaneval.get_human_eval_plus(err_incomplete=False, version="v0.1.9") == {
        "HumanEval/0": {"task_id": "HumanEval/0", "prompt": "override"}
    }
    assert (
        humaneval.get_human_eval_plus_hash(version="v0.1.9")
        == hashlib.md5(content).hexdigest()
    )
    cached_versions.assert_not_called()
