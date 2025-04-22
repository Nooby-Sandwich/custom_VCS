import os
import json
import shutil
import pytest

# Import your commands
from commands.seed import seed
from commands.pulse import pulse
from commands.tag import tag
from commands.echo import echo
from commands.roots import roots
from commands.ripple import ripple
from commands.sprout import sprout
from commands.graft import graft
from commands.drift import drift
from commands.write import write_pulses, write_tags


@pytest.fixture(autouse=True)
def temp_repo(tmp_path, monkeypatch):
    # Switch into a fresh temp dir for each test
    monkeypatch.chdir(tmp_path)
    seed()
    yield
    # cleanup of tmp_path is automatic


def test_seed_creates_repo_structure():
    assert os.path.isdir(".wen")
    assert os.path.isdir(".wen/objects")
    assert os.path.isdir(".wen/refs")
    assert os.path.isfile(".wen/HEAD")
    assert os.path.isfile(".wen/index.json")


def test_pulse_writes_json_and_appends_message():
    pulse("Test Pulse")
    path = ".wen/pulses.json"
    assert os.path.exists(path)
    data = json.load(open(path))
    assert any(item["message"] == "Test Pulse" for item in data)


def test_tag_creates_tags_json_with_key_and_message():
    pulse("Tagged Pulse")
    tag("v1.0", "Release version 1")
    tags = json.load(open(".wen/tags.json"))
    assert "v1.0" in tags
    assert tags["v1.0"]["message"] == "Release version 1"


def test_echo_runs_and_reports_latest_pulse(capsys):
    pulse("Echo Pulse")
    echo()
    captured = capsys.readouterr()
    assert "Echoing current pulse" in captured.out
    assert "Echo Pulse" in captured.out


def test_roots_runs_without_crashing(capsys):
    # On empty pulses, roots should indicate no pulses
    roots()
    captured = capsys.readouterr()
    assert "[wen] No pulses found." in captured.out or "Pulse History" in captured.out


def test_ripple_runs_without_crashing(capsys):
    ripple()
    captured = capsys.readouterr()
    assert "[wen] Looking up pulses" in captured.out or "[wen] No pulses found." in captured.out


def test_sprout_creates_branch_file_and_contains_pulse():
    pulse("Branch Base")
    sprout("feature-xyz")
    branch_file = ".wen/branches/feature-xyz.json"
    assert os.path.isfile(branch_file)
    data = json.load(open(branch_file))
    assert data[-1]["message"] == "Branch Base"


def test_graft_merges_branch_history_without_error():
    # Make sure there is something to branch from
    pulse("Branch Base")
    sprout("dev")
    # Now add a new pulse on main
    pulse("Main Update")
    graft("dev")
    # After graft, main history should contain the original "Branch Base"
    main_history = json.load(open(".wen/pulses.json"))
    assert any(p["message"] == "Branch Base" for p in main_history)


def test_drift_updates_HEAD_with_direct_id():
    pulse("Checkout target")
    pulses = json.load(open(".wen/pulses.json"))
    # Simulate using the timestamp as an ID since that's what HEAD stores
    pulse_id = pulses[-1]["timestamp"]
    drift(pulse_id)
    head = open(".wen/HEAD").read().strip()
    assert head == pulse_id


def test_write_utilities_overwrite_files():
    sample_pulses = [{"message": "util", "id": "ID1"}]
    sample_tags = {"tagA": {"message": "m"}}
    write_pulses(sample_pulses)
    write_tags(sample_tags)

    assert json.load(open(".wen/pulses.json")) == sample_pulses
    assert json.load(open(".wen/tags.json")) == sample_tags
