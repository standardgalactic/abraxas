import numpy as np
import json
import os

W, H = 80, 60
STEPS = 200

OUTPUT_PATH = "../docs/assets/data/field_all.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

rng = np.random.default_rng(42)

from scipy.ndimage import gaussian_filter
phi_raw = rng.random((H, W))
phi = gaussian_filter(phi_raw, sigma=3.0)
phi = (phi - phi.min()) / (phi.max() - phi.min())

vx = np.zeros((H, W))
vy = np.zeros((H, W))
S  = rng.random((H, W)) * 0.1
residue = np.zeros((H, W))

def step(phi, vx, vy, S, residue):

    # gradients
    grad_x = np.roll(phi, -1, axis=1) - np.roll(phi, 1, axis=1)
    grad_y = np.roll(phi, -1, axis=0) - np.roll(phi, 1, axis=0)

    # flow scaled by local phi availability — channels form where structure exists
    vx += 0.03 * grad_x * (0.5 + phi)
    vy += 0.03 * grad_y * (0.5 + phi)

    vx *= 0.95
    vy *= 0.95

    # divergence
    div = (np.roll(vx, -1, axis=1) - np.roll(vx, 1, axis=1) +
           np.roll(vy, -1, axis=0) - np.roll(vy, 1, axis=0))

    # entropy: rises with divergence, dissipates slowly
    S += 0.015 * np.abs(div)
    S -= 0.005 * S
    S = np.clip(S, 0, 1)

    # diffusion
    lap = (np.roll(phi,-1,axis=1) + np.roll(phi,1,axis=1) +
           np.roll(phi,-1,axis=0) + np.roll(phi,1,axis=0) - 4*phi)

    # phi: weaker divergence effect, stronger local dissipation
    phi -= 0.05 * div
    phi -= 0.025 * (vx**2 + vy**2)
    phi += 0.04 * lap
    phi = np.clip(phi, 0, 1)

    # residue: thresholded — forms only in high-S, high-flow stressed regions
    vmag = np.sqrt(vx**2 + vy**2)
    trigger = (S > 0.35) & (vmag > 0.1)
    residue += 0.01 * trigger.astype(float)
    residue *= 0.999           # slow decay prevents total saturation
    residue = np.clip(residue, 0, 1)

    return phi, vx, vy, S, residue

frames = []

for i in range(STEPS):
    frames.append({
        "phi":     phi.tolist(),
        "vx":      vx.tolist(),
        "vy":      vy.tolist(),
        "S":       S.tolist(),
        "residue": residue.tolist()
    })
    phi, vx, vy, S, residue = step(phi, vx, vy, S, residue)

with open(OUTPUT_PATH, "w") as f:
    json.dump(frames, f)

print(f"Exported {STEPS} frames to {OUTPUT_PATH}")
