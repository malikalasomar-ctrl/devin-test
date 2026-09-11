import pytest

from todo import core


def test_add_assigns_sequential_ids():
    items, first = core.add([], "buy milk")
    items, second = core.add(items, "walk dog")

    assert [first["id"], second["id"]] == [1, 2]
    assert [item["text"] for item in items] == ["buy milk", "walk dog"]
    assert all(item["done"] is False for item in items)


def test_add_strips_text_and_rejects_blank():
    _, item = core.add([], "  buy milk  ")
    assert item["text"] == "buy milk"

    with pytest.raises(ValueError):
        core.add([], "   ")


def test_add_allows_duplicate_text_with_distinct_ids():
    items, _ = core.add([], "buy milk")
    items, second = core.add(items, "buy milk")

    assert second["id"] == 2
    assert len(items) == 2


def test_remove_returns_remaining_items_and_does_not_reuse_ids():
    items, _ = core.add([], "buy milk")
    items, _ = core.add(items, "walk dog")

    items, removed = core.remove(items, 2)
    assert removed["text"] == "walk dog"
    assert [item["id"] for item in items] == [1]

    items, new = core.add(items, "write tests")
    assert new["id"] == 2


def test_remove_unknown_id_raises():
    with pytest.raises(core.ItemNotFoundError):
        core.remove([], 7)


def test_add_and_remove_do_not_mutate_input():
    original = [{"id": 1, "text": "buy milk", "done": False}]

    core.add(original, "walk dog")
    core.remove(original, 1)

    assert original == [{"id": 1, "text": "buy milk", "done": False}]


def test_format_item():
    assert core.format_item({"id": 1, "text": "buy milk", "done": False}) == "  1. [ ] buy milk"
    assert core.format_item({"id": 2, "text": "walk dog", "done": True}) == "  2. [x] walk dog"
