# Study Plan — *Feedback Systems* (Åström & Murray, 2nd ed.)

Free PDF: https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers

General setup:
TODO: also consider using `robotics-toolbox-python`

```bash
pip install control matplotlib numpy scipy
```
```python
import control as ct
import numpy as np
import matplotlib.pyplot as plt
```


> Check errata page before each chapter


Legend: 📖 book · ▶️ video · 🐍 exercise · 🔗 cross-reference (Lunze / APMonitor / other)

---

## Ch. 1 — Introduction
**Topics:** what is feedback, open- vs. closed-loop, historical examples (governor, op-amps).

- ▶️ Brian Douglas — "Introduction to Control Systems" (playlist opener)
- 🔗 Lunze Kap. 1 (Einführung) covers the same ground, more formal — good second pass
- 🐍 No coding yet — just sketch 2–3 feedback loops from your daily life (thermostat, cruise control, your own body's temperature regulation) and identify sensor/actuator/controller/plant.

---

## Ch. 2 — System Modeling
**Topics:** state-space models, ODEs, linear vs. nonlinear, modeling methodology.

- ▶️ Brian Douglas — "State Space Equations" / "What Is State Space?"
- 🔗 Lunze Kap. 2–3 (Beschreibung linearer Systeme) — much more rigorous derivation, read after Åström Ch. 2 for the "why"
- 🐍 Model a spring-mass-damper as state-space, simulate with `control.forced_response`:
```python
m, b, k = 1.0, 0.5, 2.0
A = [[0, 1], [-k/m, -b/m]]
B = [[0], [1/m]]
C = [[1, 0]]
D = [[0]]
sys = ct.ss(A, B, C, D)
t = np.linspace(0, 20, 500)
u = np.ones_like(t)
t, y = ct.forced_response(sys, t, u)
plt.plot(t, y); plt.xlabel("t"); plt.ylabel("position"); plt.show()
```

---

## Ch. 3 — Examples
**Topics:** cruise control, bicycle dynamics, op-amps, populations — worked case studies.

- 🔗 APMonitor "Modeling" section (apmonitor.com/pdc) — parallel case studies but Python/optimization-flavored; compare their cruise-control-style example to Åström's
- 🐍 Reimplement the cruise-control example: build the state-space model, plot step response for different vehicle masses. Vary parameters and observe how time constant changes.

---

## Ch. 4 — Dynamic Behavior
**Topics:** solving ODEs, qualitative analysis, stability, Lyapunov functions.

- ▶️ Brian Douglas — "Stability of Dynamic Systems" / "Lyapunov Stability"
- 🔗 Lunze Kap. 4 (Stabilität) — this is where Lunze's proof-heavy style pays off; read it right after Åström's intuitive version
- 🐍 Pick a nonlinear system (e.g. pendulum) and simulate with `scipy.integrate.solve_ivp` for a few initial conditions to see qualitatively different behaviors (equilibrium, oscillation, divergence).

---

## Ch. 5 — Linear Systems
**Topics:** matrix exponential, input/output response, linearization.

- ▶️ Brian Douglas — "The Matrix Exponential" (or 3Blue1Brown's linear algebra series if the matrix exponential itself is shaky)
- 🔗 Lunze Kap. 3 also derives the state transition matrix in detail — useful second angle
- 🐍 Compute and plot the matrix exponential numerically vs. `ct.step_response`:
```python
from scipy.linalg import expm
A = np.array([[0, 1], [-2, -3]])
for t in [0, 0.5, 1, 2]:
    print(t, expm(A * t))
```
Compare simulated trajectory against the analytical `expm(A*t) @ x0`.

---

## Ch. 6 — State Feedback
**Topics:** reachability/controllability, pole placement, integral action.

- ▶️ Brian Douglas — "Controllability" and "Pole Placement"
- 🔗 Lunze Kap. 6–7 (Zustandsregelung) — Lunze's Ackermann's formula treatment is a nice complement
- 🐍 Pole placement with `control.place`:
```python
A = np.array([[0, 1], [0, 0]])   # double integrator
B = np.array([[0], [1]])
K = ct.place(A, B, [-2, -3])
sys_cl = ct.ss(A - B @ K, B, np.eye(2), 0)
t, y = ct.step_response(sys_cl)
plt.plot(t, y); plt.show()
```
Check controllability first: `ct.ctrb(A, B)` and its rank.

---

## Ch. 7 — Output Feedback
**Topics:** observability, state estimators (Luenberger observer), observer-based control.

- ▶️ Brian Douglas — "Observability" and "State Estimators"
- 🔗 Lunze Kap. 8 (Beobachter)
- 🐍 Design an observer and simulate estimation error converging to zero:
```python
L = ct.place(A.T, B.T, [-5, -6]).T  # pole placement for the dual system
```
Simulate plant + observer together, plot true state vs. estimated state.

---

## Ch. 8 — Transfer Functions
**Topics:** transfer function derivation from state-space, poles/zeros, block diagrams.

- ▶️ Brian Douglas — "Transfer Functions" and "Block Diagram Reduction"
- 🔗 Lunze Kap. 9–10 (Übertragungsfunktion) — this is Lunze's strongest chapter and matches Åström well here
- 🔗 APMonitor "Dynamic Modeling / Transfer Functions" section — practical, code-first treatment
- 🐍 Convert state-space to transfer function and back:
```python
tf_sys = ct.ss2tf(sys)
print(tf_sys)
print(ct.poles(tf_sys), ct.zeros(tf_sys))
```

---

## Ch. 9 — Frequency Domain Analysis
**Topics:** Bode plots, Nyquist criterion, frequency response.

- ▶️ Brian Douglas — "Bode Plots" and "Nyquist Stability Criterion" (the two most-watched videos in his playlist for good reason)
- 🔗 Lunze Kap. 11 (Frequenzgang)
- 🐍
```python
mag, phase, omega = ct.bode_plot(tf_sys, dB=True)
ct.nyquist_plot(tf_sys)
```
Manually compute gain margin / phase margin with `ct.margin(tf_sys)` and verify against the plot.

---

## Ch. 10 — PID Control
**Topics:** PID structure, tuning (Ziegler-Nichols), anti-windup.

- ▶️ Brian Douglas — "PID Control" series (3-part)
- 🔗 APMonitor "PID Control" section — directly hands-on tuning exercises, great complement here since Åström (co-inventor of relay auto-tuning) is light on code
- 🔗 Lunze Kap. 12 (PID-Regler)
- 🐍 Build a PID controller and tune manually, then compare to Ziegler-Nichols:
```python
Kp, Ki, Kd = 2.0, 1.0, 0.1
C = ct.tf([Kd, Kp, Ki], [1, 0])
L = C * tf_sys
T = ct.feedback(L, 1)
t, y = ct.step_response(T)
plt.plot(t, y); plt.show()
```
Sweep Kp/Ki/Kd and observe overshoot/settling-time tradeoffs.

---

## Ch. 11 — Frequency Domain Design
**Topics:** sensitivity functions, loop shaping, feedforward, fundamental limitations.

- ▶️ Brian Douglas — "Loop Shaping" and "Sensitivity Functions"
- 🔗 Lunze Kap. 13 (Reglerentwurf im Frequenzbereich)
- 🐍 Plot sensitivity and complementary sensitivity functions:
```python
S = ct.feedback(1, L)
Tcl = ct.feedback(L, 1)
ct.bode_plot([S, Tcl], dB=True)
```
Observe the tradeoff: pushing S down at low frequency vs. T down at high frequency.

---

## Ch. 12 — Robust Performance
**Topics:** model uncertainty, robustness margins, robust stability.

- ▶️ Brian Douglas — "Robust Control" intro videos
- 🔗 Lunze Kap. 14 (Robuste Regelung) if covered in your edition
- 🐍 Perturb a plant parameter (±20%) and check whether your Ch. 10/11 controller still stabilizes it — plot the family of step responses to see robustness visually.

---

## After finishing the book

- Revisit **APMonitor** (apmonitor.com/pdc) in full — MPC, optimization-based control will now make sense because you have the classical/state-space vocabulary.
- Use **Lunze** as a rigor-check/reference book on chapters where the proofs still feel shaky.
- Optional next step: Åström & Murray's *Feedback Control Theory* (older, free) or Ogata's *Modern Control Engineering* for more worked problems.

## Suggested pacing
- ~1 chapter per week alongside a full-time job/studies is realistic (12 weeks total).
- Chapters 4–7 (stability, linear systems, state feedback, observers) are the hardest — allow 1.5–2 weeks each if needed.
- Do the Python exercise *before* moving to the next chapter, not after — it's the fastest way to catch a shaky derivation.
