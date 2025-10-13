import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.ticker as mticker


from simulate import run
from specs import summarize

def sweep(k_vals, c_vals, base=None):
    """
    Run a grid sweep over stiffness k and damping c.
    Returns:
      OS:  (len(c_vals), len(k_vals)) overshoot (%)
      TS:  (len(c_vals), len(k_vals)) settling time (s)
    """
    if base is None:
        base = dict(Iyy=8000.0, Ku=5e5, Kp=1.0, u0_deg=1.0, T=10.0)

    OS = np.zeros((len(c_vals), len(k_vals)))
    TS = np.zeros_like(OS)

    for i, c in enumerate(c_vals):
        for j, k in enumerate(k_vals):
            params = dict(base, c=c, k=k)
            res = run(params=params, make_plot=False)
            m = summarize(res)
            OS[i, j] = m["overshoot"]
            TS[i, j] = m["t_settle"]

    return OS, TS


if __name__ == "__main__":
    # Choose ranges (adjust to vehicle)    
    k_vals = np.linspace(2.0e6, 3.2e6, 9) # N·m/rad
    c_vals = np.linspace(1.0e5, 3.0e5, 9)  # N·m·s/rad

    OS, TS = sweep(k_vals, c_vals)

    # Mesh for plotting with readable axes (units scaled)
    K_mesh, C_mesh = np.meshgrid(k_vals / 1e6, c_vals / 1e3)

    plt.figure(figsize=(9, 4))

    # ---- Overshoot heatmap ----
    ax1 = plt.subplot(1, 2, 1)
    pc1 = ax1.pcolormesh(K_mesh, C_mesh, OS, shading="auto")
    plt.colorbar(pc1, ax=ax1, label="%OS")
    cs1 = ax1.contour(K_mesh, C_mesh, OS, levels=[5, 10, 20, 40], colors="k", linewidths=0.6)
    ax1.clabel(cs1, fmt="%.0f%%", fontsize=8)
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(5))
    ax1.set_xlabel(r"$k$  ($\times 10^6$ N·m/rad)")
    ax1.set_ylabel(r"$c$  ($\times 10^3$ N·m·s/rad)")
    ax1.set_title("Overshoot heatmap")

    # ---- Settling time heatmap ----
    ax2 = plt.subplot(1, 2, 2)
    pc2 = ax2.pcolormesh(K_mesh, C_mesh, TS, shading="auto")
    plt.colorbar(pc2, ax=ax2, label="t_settle (s)")
    cs2 = ax2.contour(K_mesh, C_mesh, TS, levels=[1.0, 2.0, 3.0, 5.0], colors="k", linewidths=0.6)
    ax2.clabel(cs2, fmt="%.1f s", fontsize=8)
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(5))
    ax2.set_xlabel(r"$k$  ($\times 10^6$ N·m/rad)")
    ax2.set_ylabel(r"$c$  ($\times 10^3$ N·m·s/rad)")
    ax2.set_title("Settling time heatmap")

    plt.tight_layout()

    # Save
    save = "figs/tuning_heatmaps.png"
    Path(save).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save, dpi=180, bbox_inches="tight")
    plt.close()
    print("Wrote figure to:", Path(save).resolve())

