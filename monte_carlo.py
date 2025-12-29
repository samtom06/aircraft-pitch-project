import numpy as np

from simulate import run
from specs import summarize

REQ = {"OS_max": 30.0, "ts_max": 4.0, "dc_gain_err_max": 0.10}  # ±10%


def passes(m: dict) -> bool:
    return (
        m["overshoot"] <= REQ["OS_max"]
        and m["t_settle"] <= REQ["ts_max"]
        and abs(m["dc_gain_error"]) <= REQ["dc_gain_err_max"]
    )


def sample_params(p_nom: dict, frac: float = 0.25, rng=None) -> dict:
    r = rng if isinstance(rng, np.random.Generator) else np.random.default_rng(rng)

    def scale(v: float) -> float:
        return float(v) * float(r.uniform(1.0 - frac, 1.0 + frac))

    return {
        "Iyy": scale(p_nom["Iyy"]),
        "c": scale(p_nom["c"]),
        "k": scale(p_nom["k"]),
        "K_act": scale(p_nom["K_act"]),
        "Kp": float(p_nom["Kp"]),
        "Ki": float(p_nom.get("Ki", 0.0)),
        "theta_cmd_deg": float(p_nom["theta_cmd_deg"]),
        "T": float(p_nom["T"]),
        "dt": float(p_nom.get("dt", 0.001)),
    }


if __name__ == "__main__":
    N = 500
    rng = np.random.default_rng(0)

    baseline = {
        "Iyy": 8000.0,
        "k": 2.5e6,
        "c": 2.0e5,
        "K_act": 5.0e5,
        "Kp": 1.0,
        "Ki": 0.0,
        "theta_cmd_deg": 1.0,
        "T": 10.0,
        "dt": 0.001,
    }

    improved = {
        "Iyy": 8000.0,
        "k": 2.8e6,
        "c": 2.2e5,
        "K_act": 5.0e5,
        "Kp": 1.3,
        "Ki": 0.0,
        "theta_cmd_deg": 1.0,
        "T": 10.0,
        "dt": 0.001,
    }

    for name, p0 in [("Baseline", baseline), ("Improved", improved)]:
        passes_count = 0
        os_vals, ts_vals = [], []

        for _ in range(N):
            res = run(params=sample_params(p0, frac=0.15, rng=rng), make_plot=False)
            m = summarize(res)
            os_vals.append(m["overshoot"])
            ts_vals.append(m["t_settle"])
            passes_count += int(passes(m))

        print(
            f"{name}: pass-rate = {100 * passes_count / N:.1f}%  "
            f"OS mean±std = {np.mean(os_vals):.2f}±{np.std(os_vals):.2f}  "
            f"t_s mean±std = {np.mean(ts_vals):.2f}±{np.std(ts_vals):.2f}"
        )
