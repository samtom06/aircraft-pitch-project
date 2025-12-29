from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from simulate import run
from specs import summarize


def sweep(k_vals, c_vals, base=None):
    if base is None:
     base = {
        "Iyy": 8000.0,
        "K_act": 5.0e5,
        "Kp": 1.3,      
        "Ki": 4.0,      
        "theta_cmd_deg": 1.0,
        "T": 30.0,      
        "dt": 0.001,
    }


    os_mat = np.zeros((len(c_vals), len(k_vals)))
    ts_mat = np.zeros_like(os_mat)

    for i, c in enumerate(c_vals):
        for j, k in enumerate(k_vals):
            params = dict(base, c=float(c), k=float(k))
            res = run(params=params, make_plot=False)
            m = summarize(res)
            os_mat[i, j] = m["overshoot"]
            ts_mat[i, j] = m["t_settle"]

    return os_mat, ts_mat


if __name__ == "__main__":
    k_vals = np.linspace(2.00e6, 3.00e6, 11)   
    c_vals = np.linspace(1.80e5, 3.00e5, 11)   


    os_mat, ts_mat = sweep(k_vals, c_vals)

    k_mesh, c_mesh = np.meshgrid(k_vals / 1e6, c_vals / 1e3)

    plt.figure(figsize=(9, 4))

    ax1 = plt.subplot(1, 2, 1)
    pc1 = ax1.pcolormesh(k_mesh, c_mesh, os_mat, shading="auto", vmin=0.0, vmax=1.0)
    plt.colorbar(pc1, ax=ax1, label="%OS (0–1%)")
    levels_os = [0.1, 0.2, 0.5, 1.0]
    cs1 = ax1.contour(k_mesh, c_mesh, os_mat, levels=levels_os, colors="k", linewidths=0.6)
    ax1.clabel(cs1, fmt="%.1f%%", fontsize=8)

    ax1.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(5))
    ax1.set_xlabel(r"$k$  ($\times 10^6$ N·m/rad)")
    ax1.set_ylabel(r"$c$  ($\times 10^3$ N·m·s/rad)")
    ax1.set_title("Overshoot heatmap")

    ax2 = plt.subplot(1, 2, 2)
    pc2 = ax2.pcolormesh(k_mesh, c_mesh, ts_mat, shading="auto")
    plt.colorbar(pc2, ax=ax2, label="t_settle (s)")
    cs2 = ax2.contour(k_mesh, c_mesh, ts_mat, levels=[1.0, 2.0, 3.0, 5.0], colors="k", linewidths=0.6)
    ax2.clabel(cs2, fmt="%.1f s", fontsize=8)
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(5))
    ax2.set_xlabel(r"$k$  ($\times 10^6$ N·m/rad)")
    ax2.set_ylabel(r"$c$  ($\times 10^3$ N·m·s/rad)")
    ax2.set_title("Settling time heatmap")

    plt.tight_layout()

    save = "figs/tuning_heatmaps.png"
    Path(save).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save, dpi=180, bbox_inches="tight")
    plt.close()
    print("Wrote figure to:", Path(save).resolve())
