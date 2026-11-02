"""Run the whole Phase 1 analysis in order. Usage: $HOME/.venvs/iehp-access/bin/python -I scripts/analysis/run_all.py [--skip-figures]
Each step is re-runnable and idempotent. Raw files are never modified.  Total run time about 8-10 minutes on 16+ cores."""
import subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
STEPS = ["s01_base_table", "s02_supply", "s02b_supply_diagnostics", "s03_access", "s04_scenarios", "s05a_covariates", "s05b_correlations", "s06_ranking", "s08_figures", "s07_quality"]
if "--skip-figures" in sys.argv: STEPS.remove("s08_figures")
for st in STEPS:
    t = time.time(); print(f"== {st}", flush=True)
    r = subprocess.run([sys.executable, "-I", str(HERE / f"{st}.py")], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-3000:]); sys.exit(f"{st} failed")
    print(f"   ok in {time.time() - t:.0f}s", flush=True)
