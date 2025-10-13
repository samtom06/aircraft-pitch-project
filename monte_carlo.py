import numpy as np
from simulate import run
from specs import summarize

REQ = dict(OS_max=30.0, ts_max=4.0, dc_gain_err_max=0.10)  # ±10%

def passes(m):
    return (m['overshoot'] <= REQ['OS_max'] and
            m['t_settle']  <= REQ['ts_max'] and
            abs(m['dc_gain_error']) <= REQ['dc_gain_err_max'])

def sample_params(p_nom, frac: float = 0.25, rng=None):
    # rng can be None, an int seed, or a numpy Generator
    r = np.random.default_rng(rng if isinstance(rng, (int, np.random.Generator)) else None)

    def scale(v):
        """Randomly scale v within ±frac (uniform)."""
        return v * r.uniform(1.0 - frac, 1.0 + frac)

    return dict(
        Iyy=scale(p_nom["Iyy"]),
        c=scale(p_nom["c"]),
        k=scale(p_nom["k"]),
        Ku=scale(p_nom["Ku"]),
        Kp=p_nom["Kp"],          # keep controller gain fixed (or scale if you want)
        u0_deg=p_nom["u0_deg"],
        T=p_nom["T"],
    )

if __name__ == "__main__":
    N = 500
    baseline  = dict(Iyy=8000.0, k=2.5e6, c=2.0e5, Ku=5e5, Kp=1.0, u0_deg=1.0, T=10.0)
    improved  = dict(Iyy=8000.0, k=2.8e6, c=2.2e5, Ku=5e5, Kp=1.3, u0_deg=1.0, T=10.0)


    for name, p0 in [("Baseline", baseline), ("Improved", improved)]:
        passes_count, os_vals, ts_vals = 0, [], []
        for _ in range(N):
            res = run(params=sample_params(p0, frac=0.15), make_plot=False)
            m = summarize(res) 
            os_vals.append(m['overshoot'])
            ts_vals.append(m['t_settle'])
            passes_count += int(passes(m))
        print(f"{name}: pass-rate = {100*passes_count/N:.1f}%  "
              f"OS mean±std = {np.mean(os_vals):.2f}±{np.std(os_vals):.2f}  "
              f"t_s mean±std = {np.mean(ts_vals):.2f}±{np.std(ts_vals):.2f}")
