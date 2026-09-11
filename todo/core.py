from typing import Any

Item = dict[str, Any]


class ItemNotFoundError(LookupError):
    def __init__(self, item_id: int) -> None:
        super().__init__(f"no to-do with id {item_id}")
        self.item_id = item_id


def next_id(items: list[Item]) -> int:
    return max((item["id"] for item in items), default=0) + 1


def add(items: list[Item], text: str) -> tuple[list[Item], Item]:
    text = text.strip()
    if not text:
        raise ValueError("to-do text must not be empty")
    item: Item = {"id": next_id(items), "text": text, "done": False}
    return [*items, item], item


def remove(items: list[Item], item_id: int) -> tuple[list[Item], Item]:
    for index, item in enumerate(items):
        if item["id"] == item_id:
            return items[:index] + items[index + 1 :], item
    raise ItemNotFoundError(item_id)


def format_item(item: Item) -> str:
    mark = "x" if item["done"] else " "
    return f"{item['id']:>3}. [{mark}] {item['text']}"
