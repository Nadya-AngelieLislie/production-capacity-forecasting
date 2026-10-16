"""Re-check of the notebook's numbers with a numerically stable solver.

The notebook solves the normal equations with np.linalg.inv(A.T @ A), which is badly
conditioned for high-degree polynomials in raw month units (x up to 72). This script
re-fits the same data with np.polyfit and solves f(x) = 25,000 with np.roots.
Run from the repository root:  python scripts/recheck_with_polyfit.py
"""
import numpy as np
import pandas as pd

df = pd.read_csv("data/monthly_production_aggregated.csv")
x = df["month_index"].to_numpy(float)
y = df["production"].to_numpy(float)
CAPACITY = 25_000

print("degree |   MAE    RMSE   MAPE%  | month where fit reaches capacity")
for d in range(2, 7):
    p = np.polyfit(x, y, d)
    e = y - np.polyval(p, x)
    q = p.copy()
    q[-1] -= CAPACITY
    roots = [r.real for r in np.roots(q) if abs(r.imag) < 1e-9 and r.real > x.max()]
    print(f"  {d}    | {np.mean(abs(e)):6.1f} {np.sqrt(np.mean(e**2)):6.1f} {np.mean(abs(e / y)) * 100:6.3f}  | "
          + ", ".join(f"{r:.1f}" for r in sorted(roots)))

# exponential model (log-linear least squares)
b, ln_a = np.polyfit(x, np.log(y), 1)
print(f"exponential: y = {np.exp(ln_a):.1f} * exp({b:.5f} x); reaches capacity at month {(np.log(CAPACITY) - ln_a) / b:.1f}")
print("month 1 = Jan 2018, so month 73 = Jan 2024 and month 83 = Nov 2024.")
