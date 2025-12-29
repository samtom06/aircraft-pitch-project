import numpy as np


def steady_state(y: np.ndarray) -> float:
    n = len(y)
    tail = y[int(0.9 * n) :]
    return float(np.mean(tail))


def overshoot_percent(theta: np.ndarray, theta_ss: float) -> float:
    peak = float(np.max(theta))
    denom = abs(theta_ss) if abs(theta_ss) > 1e-12 else 1.0
    return max(0.0, (peak - theta_ss) / denom * 100.0)


def settling_time(t: np.ndarray, theta: np.ndarray, theta_ss: float, band: float = 0.02) -> float:
    tol = band * (abs(theta_ss) if abs(theta_ss) > 1e-12 else 1.0)
    inside = np.abs(theta - theta_ss) <= tol
    for i in range(len(t)):
        if np.all(inside[i:]):
            return float(t[i])
    return float(t[-1])


def rise_time_10_90(t: np.ndarray, theta: np.ndarray, theta_ss: float) -> float:
    lo = 0.1 * theta_ss
    hi = 0.9 * theta_ss

    lo_mask = np.logical_and(theta[:-1] < lo, theta[1:] >= lo)
    hi_mask = np.logical_and(theta[:-1] < hi, theta[1:] >= hi)

    def first_cross(mask: np.ndarray, level: float) -> float:
        idx = np.where(mask)[0]
        if idx.size == 0:
            return float("nan")
        i = int(idx[0])
        dt = t[i + 1] - t[i]
        dtheta = theta[i + 1] - theta[i]
        if abs(dtheta) < 1e-15:
            return float(t[i])
        alpha = (level - theta[i]) / dtheta
        return float(t[i] + alpha * dt)

    t10 = first_cross(lo_mask, lo)
    t90 = first_cross(hi_mask, hi)
    return float(t90 - t10)


def rms_error(t: np.ndarray, theta: np.ndarray, theta_ref: np.ndarray) -> float:
    err = theta - theta_ref
    return float(np.sqrt(np.trapz(err**2, t) / (t[-1] - t[0])))


def dc_gain_check(params: dict, theta_ss: float) -> tuple[float, float]:
    theta_cmd_rad = float(np.deg2rad(params["theta_cmd_deg"]))
    Kp = float(params.get("Kp", 0.0))
    Ki = float(params.get("Ki", 0.0))

    if Ki != 0.0:
        theta_ss_th = theta_cmd_rad
    else:
        K_act = float(params["K_act"])
        k = float(params["k"])
        theta_ss_th = (K_act * Kp) / (k + K_act * Kp) * theta_cmd_rad

    rel_err = (theta_ss - theta_ss_th) / (theta_ss_th if abs(theta_ss_th) > 1e-12 else 1.0)
    return float(theta_ss_th), float(rel_err)


def summarize(result: dict) -> dict:
    t = result["t"]
    th = result["theta"]
    p = result["params"]

    th_ss = steady_state(th)
    os = overshoot_percent(th, th_ss)
    ts = settling_time(t, th, th_ss, band=0.02)
    tr = rise_time_10_90(t, th, th_ss)

    th_th, rel_err = dc_gain_check(p, th_ss)

    return {
        "theta_ss": th_ss,
        "overshoot": os,
        "t_settle": ts,
        "t_rise": tr,
        "theta_ss_theory": th_th,
        "dc_gain_error": rel_err,
    }


if __name__ == "__main__":
    from simulate import run

    params = dict(
        Iyy=8000.0,
        k=2.5e6,
        c=2.4e5,
        K_act=5.0e5,
        Kp=1.3,
        Ki=4.0,          
        theta_cmd_deg=1.0,
        T=30.0,
        dt=0.001,
    )

    res = run(params=params, make_plot=True)
    m = summarize(res)

    print(
        f"θ_ss (deg): {np.rad2deg(m['theta_ss']):.3f}   "
        f"theory: {np.rad2deg(m['theta_ss_theory']):.3f}   "
        f"gain error: {100*m['dc_gain_error']:.2f}%"
    )
    print(
        f"%OS: {m['overshoot']:.2f}%   "
        f"t_settle(±2%): {m['t_settle']:.3f} s   "
        f"t_rise(10→90%): {m['t_rise']:.3f} s"
    )

