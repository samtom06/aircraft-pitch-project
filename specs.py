import numpy as np
from simulate import run

def steady_state(y):
    # average last 10% of samples for numerical robustness
    n = len(y)
    tail = y[int(0.9*n):]
    return float(np.mean(tail))

def overshoot_percent(theta, theta_ss):
    peak = float(np.max(theta))
    return max(0.0, (peak - theta_ss) / abs(theta_ss) * 100.0)

def settling_time(t, theta, theta_ss, band=0.02):
    tol = band * abs(theta_ss)
    inside = np.abs(theta - theta_ss) <= tol
    # first index from which we stay inside until end
    for i in range(len(t)):
        if np.all(inside[i:]):
            return float(t[i])
    return float(t[-1])

def rise_time_10_90(t, theta, theta_ss):
    """
    10% -> 90% rise time. Works for positive or negative theta_ss.
    Finds first upward crossings and linearly interpolates between samples.
    """
    lo = 0.1 * theta_ss
    hi = 0.9 * theta_ss

    # crossings between adjacent samples (same length: N-1)
    lo_mask = np.logical_and(theta[:-1] < lo, theta[1:] >= lo)
    hi_mask = np.logical_and(theta[:-1] < hi, theta[1:] >= hi)

    # helper: first crossing time with linear interpolation
    def first_cross(mask, level):
        idx = np.where(mask)[0]
        if idx.size == 0:
            return np.nan
        i = idx[0]
        dt = t[i+1] - t[i]
        dθ = theta[i+1] - theta[i]
        α = (level - theta[i]) / dθ
        return float(t[i] + α * dt)

    t10 = first_cross(lo_mask, lo)
    t90 = first_cross(hi_mask, hi)
    return t90 - t10


def rms_error(t, theta, theta_ref):
    err = theta - theta_ref
    return float(np.sqrt(np.trapz(err**2, t) / (t[-1]-t[0])))

def dc_gain_check(params, theta_ss):
    u0_deg = params["u0_deg"]
    u0_rad = np.deg2rad(u0_deg)
    Ku = params["Ku"]
    k  = params["k"]
    Kp = params.get("Kp", 0.0)           # default 0 if not present

    # Closed-loop DC gain with P loop around θ
    theta_ss_th = (Ku*Kp) / (k + Ku*Kp) * u0_rad

    rel_err = (theta_ss - theta_ss_th) / theta_ss_th
    return theta_ss_th, rel_err


def summarize(result):
    t = result["t"]
    th = result["theta"]
    p = result["params"]
    th_ss = steady_state(th)
    os = overshoot_percent(th, th_ss)
    ts = settling_time(t, th, th_ss, band=0.02)
    tr = rise_time_10_90(t, th, th_ss)
    th_th, rel_err = dc_gain_check(p, th_ss)

    return dict(theta_ss=th_ss, overshoot=os, t_settle=ts,
                t_rise=tr, theta_ss_theory=th_th, dc_gain_error=rel_err)

if __name__ == "__main__":
    res = run(make_plot=True)
    m = summarize(res)
    # Print tidy, degrees where appropriate
    to_deg = np.rad2deg

    print(f"θ_ss (deg): {to_deg(m['theta_ss']):.3f}   "
          f"theory: {to_deg(m['theta_ss_theory']):.3f}   "
          f"gain error: {100*m['dc_gain_error']:.2f}%")
    print(f"%OS: {m['overshoot']:.2f}%   "
          f"t_settle(±2%): {m['t_settle']:.3f} s   "
          f"t_rise(10→90%): {m['t_rise']:.3f} s")
