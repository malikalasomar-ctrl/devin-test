import argparse
from collections.abc import Sequence

from todo import core, storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny command-line to-do list.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a to-do")
    add_parser.add_argument("text", nargs="+", help="what to do")

    subparsers.add_parser("list", help="list all to-dos")

    remove_parser = subparsers.add_parser("remove", aliases=["rm"], help="remove a to-do by id")
    remove_parser.add_argument("id", type=int, help="id of the to-do to remove")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    items = storage.load()

    if args.command == "add":
        items, item = core.add(items, " ".join(args.text))
        storage.save(items)
        print(f"Added {core.format_item(item).strip()}")
        return 0

    if args.command == "list":
        if not items:
            print("No to-dos yet.")
            return 0
        for item in items:
            print(core.format_item(item))
        return 0

    try:
        items, item = core.remove(items, args.id)
    except core.ItemNotFoundError as exc:
        print(f"Error: {exc}")
        return 1
    storage.save(items)
    print(f"Removed {core.format_item(item).strip()}")
    return 0
