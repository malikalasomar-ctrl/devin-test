# devin-test

A tiny command-line to-do list.

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```bash
todo add "buy milk"   # or: python -m todo add "buy milk"
todo list
todo remove 1         # alias: todo rm 1
```

To-dos are stored as JSON in `~/.todo.json`. Set `TODO_FILE` to use a different path.

## Tests

```bash
pytest
ruff check .
```
