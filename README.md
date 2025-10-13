# Aircraft Pitch Project

Python mini-project exploring aircraft pitch dynamics.

**Modules**
- `simulate.py` — run a single pitch simulation
- `sweep.py` — parameter sweep for sensitivity
- `monte_carlo.py` — Monte Carlo sampling to estimate pass rate
- `specs.py` — requirement thresholds (`REQ`) & summarizers
- `common.py` — shared helpers

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python simulate.py
python sweep.py
python monte_carlo.py

