set shell := ["bash", "-euo", "pipefail", "-c"]
set default-list
set minimum-version := "1.55.0"

alias qg := quality-gates

uv := require("uv")

[doc("Run the pytest suite")]
[group("quality")]
test:
    {{ uv }} run pytest

[doc("Lint src and tests with Ruff")]
[group("quality")]
lint:
    {{ uv }} run ruff check src tests

[doc("Format src and tests with Ruff")]
[group("quality")]
format:
    {{ uv }} run ruff format src tests

[doc("Check Ruff formatting without writing")]
[group("quality")]
format-check:
    {{ uv }} run ruff format --check src tests

[doc("Type-check with ty")]
[group("quality")]
typecheck:
    {{ uv }} run ty check

[doc("Lint, typecheck, format-check, and test")]
[group("quality")]
check: lint typecheck format-check test

[doc("Compatibility smoke against the demo notebook and CLI surfaces")]
[group("quality")]
smoke:
    {{ uv }} run nbops version
    {{ uv }} run nbops --version
    {{ uv }} run python -m nbops version
    {{ uv }} run nbops ops
    {{ uv }} run nbops stats examples/demo.ipynb --json
    {{ uv }} run nbops lint examples/demo.ipynb
    {{ uv }} run nbops convert examples/demo.ipynb --to py
    {{ uv }} run nbops validate examples/demo.ipynb
    {{ uv }} run nbops outputs examples/demo.ipynb --json
    {{ uv }} run nbops batch validate examples
    {{ uv }} run nbops serve --help

[doc("Full local gates: check plus compatibility smoke")]
[group("quality")]
quality-gates: check smoke

[doc("Show CLI help")]
[group("app")]
cli:
    {{ uv }} run nbops --help

[doc("Run the FastAPI app on 0.0.0.0:8000")]
[group("app")]
api:
    {{ uv }} run nbops serve --host 0.0.0.0 --port 8000
