# Aircraft Pitch Stability – Requirements-Based MBSE Python Model

**Tech stack:** Python • Control Theory • NumPy • SciPy • Matplotlib • Monte Carlo • MBSE

**Project context:** This project supports my resume by demonstrating requirements-based modeling and simulation of aircraft **pitch stability** in Python, including parameter sweeps and Monte Carlo robustness analysis.

---

## Overview

This repository models aircraft **pitch dynamics** as a second-order system and evaluates transient performance against **requirements** (MBSE style). It includes:

- A simplified pitch model (spring–mass–damper analog)
- Requirements verification (overshoot, settling time, steady-state error)
- **Parameter sweep** for sensitivity
- **Monte Carlo** analysis for robustness

**Why it matters:** Recruiters can see both **engineering modeling** and **software discipline**—clean code, reproducible runs, and requirements verification.

---

## System Model (Control Theory)

Pitch angle \\( \theta(t) \\) is modeled as a second-order LTI system driven by control input \\( u(t) \\):

\\[
\ddot{\theta}(t)\;+\;2\zeta\omega_n\,\dot{\theta}(t)\;+\;\omega_n^2\,\theta(t)\;=\;K\,u(t)
\\]

Where:

- \\( \zeta \\) = damping ratio  
- \\( \omega_n \\) = natural frequency (rad/s)  
- \\( K \\) = control gain / DC gain mapping  

Typical time-domain metrics used here:

- **Percent Overshoot (OS%)**
- **Settling Time (\\( t_{s} \\), 2–5%)**
- **Steady-State Error (SSE)**

---

## Requirements (MBSE Style)

Thresholds are defined in `specs.py` as a single source of truth (edit there):

- **OS%** ≤ `REQ["max_os"]`  
- **Settling Time** ≤ `REQ["max_settle_s"]`  
- **Steady-State Error** ≤ `REQ["max_sse"]`  

Each run computes the metrics and emits **PASS/FAIL** against these limits.

---

## Approach

### 1) Baseline Simulation
`simulate.py` runs a nominal case using parameters from `specs.py` and helpers in `common.py`. It prints the key metrics and pass/fail status.

### 2) Parameter Sweep (Sensitivity)
`sweep.py` varies selected parameters (e.g., \\( \zeta, \omega_n, K \\)) across grids to study how performance margins shift. Useful to visualize stability/robustness trends.

### 3) Monte Carlo (Robustness)
`monte_carlo.py` samples parameters from specified distributions and reports **pass rate** vs. requirements (e.g., “842/1000 trials passed → 84.2%”).

---

## Code Architecture


