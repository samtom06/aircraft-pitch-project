# Aircraft Pitch Stability – Requirements-Based MBSE Python Model

**Tech stack:** Python • NumPy • SciPy • Matplotlib • Control theory • Monte Carlo • MBSE

**Project context:** This project supports my resume by showing requirements-based modeling and simulation of aircraft pitch stability in Python. It includes parameter sweeps and a Monte Carlo robustness study.

---

## Overview

This repository models aircraft pitch dynamics as a second-order system and evaluates transient performance against requirements. It includes:

- A pitch model that follows a spring–mass–damper analog  
- Requirements checks for overshoot, settling time, and steady-state error  
- A parameter sweep for sensitivity  
- A Monte Carlo study for robustness

---

## System Model (control theory)

Pitch angle `theta(t)` follows a second-order LTI form:


