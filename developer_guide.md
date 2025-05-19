# Developer guide

## Setup

[https://github.com/astral-sh/uv?tab=readme-ov-file#installation](Install `uv`) if you haven't done so already. We will use it as our dependency manager.

```
uv sync
uv run pre-commit install
uv pip install -e .
```

## Development

To install a package for temporary testing:

```
uv pip install <package>
uv pip install git+ssh://...
```

To install package AND add to project's dependencies in pyproject.toml (preferred for permanent dependencies):

```
uv add <package>
```

For development dependencies, e.g. `ruff` (already installed here):

```
uv add --dev <package>
```

For removing a package:

```
uv remove <package>
```

To run ruff and format docstrings uniformly – **do this before every commit, otherwise the pre commit config blocks the commit**:

```
uvx pyment . -o "google" -w # Fill out docstrings that are not created yet; otherwise ruff removes them in next command
uvx docformatter --style numpy --recursive . --in-place
uvx ruff format
uvx pre-commit run --all-files
```
