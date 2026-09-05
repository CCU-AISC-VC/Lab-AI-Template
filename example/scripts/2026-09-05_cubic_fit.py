"""Cubic polynomial fit of force-displacement data.

See example/plans/2026-09-05_cubic_fit.md for the plan this implements.
"""
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "example/data/cubic_measurement.csv"
FIG_PATH = "example/results/figures/2026-09-05_cubic_fit.png"
TABLE_PATH = "example/results/tables/2026-09-05_cubic_coeffs.csv"

TRUE_COEFFS = {"a": 2.0, "b": -5.0, "c": 3.0, "d": 7.0}

# Step 1: read CSV, skipping the 3-line metadata header
data = np.genfromtxt(DATA_PATH, delimiter=",", skip_header=4, names=["x_mm", "force_N"])
x = data["x_mm"]
force = data["force_N"]
print(f"Loaded {x.shape[0]} rows x 2 cols; x_mm range: {x.min():.2f} ~ {x.max():.2f}")

# Step 2: cubic polynomial fit
coeffs = np.polyfit(x, force, 3)
a, b, c, d = coeffs
print(f"Fitted coefficients: a={a:.4f}, b={b:.4f}, c={c:.4f}, d={d:.4f}")

# Step 3: compare against known ground truth
fitted = np.polyval(coeffs, x)
residuals = force - fitted
residual_std = residuals.std(ddof=1)

errors = {
    name: abs(val - TRUE_COEFFS[name]) / abs(TRUE_COEFFS[name]) * 100
    for name, val in zip("abcd", coeffs)
}
print(f"Error vs truth (%): a={errors['a']:.2f}, b={errors['b']:.2f}, "
      f"c={errors['c']:.2f}, d={errors['d']:.2f}")
print(f"Residual std: {residual_std:.4f} N (truth sigma = 2.0 N)")

# Step 4: plot measurement scatter + fitted curve, and residuals
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True)

x_smooth = np.linspace(x.min(), x.max(), 300)
ax1.scatter(x, force, s=15, color="tab:blue", label="Measured")
ax1.plot(x_smooth, np.polyval(coeffs, x_smooth), color="tab:red", label="Cubic fit")
ax1.set_ylabel("Force (N)")
ax1.set_title("Cubic fit: force vs. displacement")
ax1.legend()
ax1.grid(alpha=0.3)

ax2.axhline(0, color="black", linewidth=0.8)
ax2.scatter(x, residuals, s=15, color="tab:green")
ax2.set_xlabel("Displacement (mm)")
ax2.set_ylabel("Residual (N)")
ax2.grid(alpha=0.3)

fig.tight_layout()
fig.savefig(FIG_PATH, dpi=300)
plt.close(fig)
print(f"Saved figure to {FIG_PATH}")

# Step 5: save coefficient table with units and error columns
with open(TABLE_PATH, "w") as f:
    f.write("term,unit,fitted_value,true_value,error_pct\n")
    units = {"a": "N/mm^3", "b": "N/mm^2", "c": "N/mm", "d": "N"}
    for name, val in zip("abcd", coeffs):
        f.write(f"{name},{units[name]},{val:.6f},{TRUE_COEFFS[name]:.6f},{errors[name]:.4f}\n")
    f.write(f"residual_std,N,{residual_std:.6f},2.0,\n")
print(f"Saved coefficient table to {TABLE_PATH}")
