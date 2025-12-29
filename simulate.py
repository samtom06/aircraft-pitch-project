from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from common import default_params, deg2rad, step_u


def dynamics(t: float, x: np.ndarray, p: dict) -> np.ndarray:
    theta, q, e_int = x

    theta_cmd = step_u(t, deg2rad(p["theta_cmd_deg"]))
    e = theta_cmd - theta

    u_eff = p["Kp"] * e + p["Ki"] * e_int
    qdot = (-p["c"] * q - p["k"] * theta + p["K_act"] * u_eff) / p["Iyy"]

    return np.array([q, qdot, e])


def run(
    params: dict | None = None,
    x0: np.ndarray | None = None,
    make_plot: bool = True,
    save: str = "figs/step_closed.png",
) -> dict:
    p = default_params()
    if params:
        p.update(params)

    if x0 is None:
        x0 = np.array([0.0, 0.0, 0.0], dtype=float)

    t_final = float(p["T"])
    dt = float(p.get("dt", 0.001))
    t_eval = np.linspace(0.0, t_final, int(t_final / dt) + 1)

    sol = solve_ivp(
        fun=lambda ti, xi: dynamics(ti, xi, p),
        t_span=(0.0, t_final),
        y0=x0,
        t_eval=t_eval,
        rtol=1e-7,
        atol=1e-9,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    t = sol.t
    theta = sol.y[0]
    q = sol.y[1]
    e_int = sol.y[2]
    theta_cmd = step_u(t, deg2rad(p["theta_cmd_deg"]))

    if make_plot:
        title = "Pitch Command Step Response (PI-control)" if p["Ki"] != 0.0 else "Pitch Command Step Response (P-control)"
        plt.figure(figsize=(8, 4))
        plt.plot(t, np.rad2deg(theta), label=r"$\theta$ (deg)")
        plt.plot(t, np.rad2deg(theta_cmd), "--", label=r"$\theta_{cmd}$ (deg)")
        plt.xlabel("Time (s)")
        plt.ylabel("Pitch angle (deg)")
        plt.title(title)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        Path(save).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save, dpi=160, bbox_inches="tight")
        plt.close()

        print("Wrote figure to:", Path(save).resolve())

    return {"t": t, "theta": theta, "q": q, "e_int": e_int, "theta_cmd": theta_cmd, "params": p}


if __name__ == "__main__":
    run(
        params={
            "Iyy": 8000.0,
            "k": 2.5e6,
            "c": 2.4e5,
            "K_act": 5.0e5,
            "Kp": 2.0,
            "Ki": 6.0,
            "theta_cmd_deg": 1.0,
            "T": 30.0,
            "dt": 0.001,
        }
    )

