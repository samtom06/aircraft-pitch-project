import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from common import default_params, step_u, deg2rad
from pathlib import Path


def dynamics(t, x, p):
    """
    x = [theta, q], q = d(theta)/dt
    Iyy * qdot = -c*q - k*theta + Ku * u_eff
    u_eff = Kp*(theta_cmd - theta)  (simple P loop around pitch)
    """
    theta, q = x
    u_cmd = step_u(t, deg2rad(p["u0_deg"]))   # rad
    u_eff = p["Kp"] * (u_cmd - theta)         # rad (dimensionless gain)
    qdot = (-p["c"]*q - p["k"]*theta + p["Ku"]*u_eff) / p["Iyy"]
    return np.array([q, qdot])

def run(params=None, x0=None, make_plot=True, save="figs/step_closed.png"):
    p = default_params() if params is None else params
    if x0 is None:
        x0 = np.array([0.0, 0.0])             # start at trim, not moving

    T = p["T"]
    t_eval = np.linspace(0.0, T, int(T/0.001)+1)  # ~1 ms sampling

    sol = solve_ivp(fun=lambda t,x: dynamics(t,x,p),
                    t_span=(0.0, T),
                    y0=x0, t_eval=t_eval, rtol=1e-7, atol=1e-9)

    t = sol.t
    theta = sol.y[0]
    q = sol.y[1]
    u_cmd = step_u(t, deg2rad(p["u0_deg"]))

    if make_plot:
        plt.figure(figsize=(8,4))
        plt.plot(t, np.rad2deg(theta), label=r"$\theta$ (deg)")
        plt.plot(t, np.rad2deg(u_cmd), "--", label=r"$u_{cmd}$ (deg)")
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (deg)")
        plt.title("Pitch Step Response (P-loop around SMD)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        Path(save).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save, dpi=160, bbox_inches="tight")
        plt.close()  # frees memory if you’ll generate multiple plots

        print("Wrote figure to:", Path(save).resolve())
        # plt.show()  # you can enable interactively

    return dict(t=t, theta=theta, q=q, u_cmd=u_cmd, params=p)

if __name__ == "__main__":
    run(params=dict(
        Iyy=8000.0,
        k=2.5e6,
        c=2.0e5,   # higher damping
        Ku=5e5,
        Kp=1.3,
        u0_deg=1.0,
        T=10.0     # keep or tweak
    ))

