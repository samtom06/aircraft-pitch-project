import numpy as np

def deg2rad(x_deg: float) -> float:
    return np.deg2rad(x_deg)

def step_u(t, u0):
    """Unit-step of size u0 (radians) starting at t>=0."""
    return u0 * (t >= 0.0)

def default_params():
    # SI units; radians internally
    return dict(
        Iyy=8000.0,          # kg·m^2
        c=2.4e5,           # N·m·s/rad (damping)
        k=2.5e6,             # N·m/rad   (stiffness)
        Ku=5.0e5,            # N·m/rad   (control effectiveness)
        Kp=1.0,              # simple P controller on pitch command
        u0_deg=1.0,          # step command magnitude (deg)
        T=6.0                # sim time (s)
    )
