# common.py
import numpy as np


def deg2rad(x_deg: float) -> float:
    return float(np.deg2rad(x_deg))


def step_u(t: float | np.ndarray, u0: float) -> float | np.ndarray:
    return u0 * (t >= 0.0)


def default_params() -> dict:
    return {
        "Iyy": 8000.0,
        "c": 2.4e5,
        "k": 2.5e6,
        "K_act": 5.0e5,
        "Kp": 1.3,
        "Ki": 1.0,
        "theta_cmd_deg": 1.0,
        "T": 30.0,
        "dt": 0.001,
    }

