import json

import pytest

from todo import cli


@pytest.fixture(autouse=True)
def todo_file(tmp_path, monkeypatch):
    path = tmp_path / "todo.json"
    monkeypatch.setenv("TODO_FILE", str(path))
    return path


def test_add_persists_item(todo_file, capsys):
    assert cli.main(["add", "buy", "milk"]) == 0

    assert "buy milk" in capsys.readouterr().out
    assert json.loads(todo_file.read_text()) == [{"id": 1, "text": "buy milk", "done": False}]


def test_list_empty(capsys):
    assert cli.main(["list"]) == 0
    assert capsys.readouterr().out.strip() == "No to-dos yet."


def test_list_shows_all_items(capsys):
    cli.main(["add", "buy milk"])
    cli.main(["add", "walk dog"])
    capsys.readouterr()

    assert cli.main(["list"]) == 0
    out = capsys.readouterr().out
    assert "1. [ ] buy milk" in out
    assert "2. [ ] walk dog" in out


def test_remove_deletes_item(todo_file, capsys):
    cli.main(["add", "buy milk"])
    cli.main(["add", "walk dog"])
    capsys.readouterr()

    assert cli.main(["remove", "1"]) == 0
    assert "buy milk" in capsys.readouterr().out
    assert [item["id"] for item in json.loads(todo_file.read_text())] == [2]


def test_rm_alias(capsys):
    cli.main(["add", "buy milk"])
    capsys.readouterr()

    assert cli.main(["rm", "1"]) == 0


def test_remove_unknown_id_exits_nonzero(capsys):
    assert cli.main(["remove", "42"]) == 1
    assert "no to-do with id 42" in capsys.readouterr().out


def test_no_command_exits_with_usage_error():
    with pytest.raises(SystemExit) as excinfo:
        cli.main([])
    assert excinfo.value.code == 2
