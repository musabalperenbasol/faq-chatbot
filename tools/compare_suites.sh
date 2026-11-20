#!/usr/bin/env bash
# Runs mutation testing for four variants of the test suite and stores the results.
# Overwrites pyproject.toml; the last variant ("all") is left in place.
OUT=docs/ai_evidence/mutation

run_suite () {
  name="$1"; selection="$2"; extra="$3"
  cat > pyproject.toml <<TOML
[tool.mutmut]
source_paths = ["app/"]
do_not_mutate = ["app/llm_client.py"]
pytest_add_cli_args_test_selection = [$selection]
pytest_add_cli_args = [$extra]
TOML
  find . -name "__pycache__" -not -path "./.venv/*" -prune -exec rm -rf {} +
  rm -rf mutants
  echo "===== suite: $name"
  mutmut run 2>&1 | tee "$OUT/suite_${name}_run.txt"
  mutmut results 2>&1 | grep survived > "$OUT/suite_${name}_survivors.txt"
}

GAPS='"--ignore=tests/unit/test_mutation_gaps.py", "--ignore=tests/unit/test_prompt_versions.py"'
AI_FILE='"--ignore=tests/api/test_ai_generated_v1.py"'

run_suite ours     '"tests/"' "$AI_FILE, $GAPS"
run_suite ai       '"tests/api/test_ai_generated_v1.py"' ''
run_suite combined '"tests/"' "$GAPS"
run_suite all      '"tests/"' ''
