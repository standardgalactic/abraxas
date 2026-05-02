// Color palettes per mode — diagnostic, not decorative
const PALETTE = {
  field:         (v) => `rgb(${Math.floor(v*180)}, ${Math.floor(v*200)}, ${Math.floor(v*255)})`,
  repair:        (v) => `rgb(${Math.floor(v*100)}, ${Math.floor(v*220)}, ${Math.floor(v*180)})`,
  fragmentation: (v) => `rgb(${Math.floor(v*255)}, ${Math.floor(v*160)}, ${Math.floor(v*80)})`,
};

export function drawField(ctx, frame, mode, W, H, cw, ch) {
  const color = PALETTE[mode] || PALETTE.field;

  // subtle instability for fragmentation mode
  if (mode === "fragmentation") {
    ctx.globalAlpha = 0.88 + Math.random() * 0.12;
  } else {
    ctx.globalAlpha = 1.0;
  }

  // scalar layer
  if (mode !== "trajectory") {
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {

        const phi = frame.phi[y][x];
        const S = frame.S[y][x];
        const residue = frame.residue[y][x];

        let val;

        if (mode === "field") {
          val = phi;
        }

        else if (mode === "repair") {
          val = 1 - S;
        }

        else if (mode === "fragmentation") {

          // --- CORE FIX: fragmentation as projection loss ---

          // coarse blocking (information loss)
          const blockSize = 4;
          const bx = Math.floor(x / blockSize) * blockSize;
          const by = Math.floor(y / blockSize) * blockSize;

          const blockPhi = frame.phi[by][bx];

          // interpolate between fine and coarse structure
          let degraded = blockPhi * residue + phi * (1 - residue);

          // noise proportional to residue
          degraded += (Math.random() - 0.5) * residue * 0.5;

          // dropout (missing structure)
          if (Math.random() < residue * 0.25) {
            degraded = 0;
          }

          // clamp
          val = Math.max(0, Math.min(1, degraded));
        }

        ctx.fillStyle = color(val);
        ctx.fillRect(x*cw, y*ch, cw+0.5, ch+0.5); // +0.5 prevents subpixel gaps
      }
    }
  }

  // trajectory: phi base + vector arrows
  if (mode === "trajectory") {
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const v = frame.phi[y][x] * 0.3; // dim base
        ctx.fillStyle = `rgb(${Math.floor(v*80)},${Math.floor(v*90)},${Math.floor(v*120)})`;
        ctx.fillRect(x*cw, y*ch, cw+0.5, ch+0.5);
      }
    }

    // arrow overlay — stride adaptive for legibility
    const stride = Math.max(3, Math.floor(Math.min(W, H) / 20));
    ctx.lineWidth = 0.8;

    for (let y = Math.floor(stride/2); y < H; y += stride) {
      for (let x = Math.floor(stride/2); x < W; x += stride) {

        const vx = frame.vx[y][x];
        const vy = frame.vy[y][x];
        const mag = Math.sqrt(vx*vx + vy*vy);
        if (mag < 0.01) continue;

        const alpha = Math.min(0.9, mag * 0.6);
        ctx.strokeStyle = `rgba(160,200,255,${alpha.toFixed(2)})`;

        const scale = Math.min(mag, 1.5) * cw * stride * 0.4 / mag;

        const px = x*cw + cw/2;
        const py = y*ch + ch/2;
        const tx = px + vx * scale;
        const ty = py + vy * scale;

        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(tx, ty);
        ctx.stroke();

        // arrowhead
        const angle = Math.atan2(vy, vx);
        const hs = cw * 0.7;

        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - hs * Math.cos(angle - 0.4), ty - hs * Math.sin(angle - 0.4));
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - hs * Math.cos(angle + 0.4), ty - hs * Math.sin(angle + 0.4));
        ctx.stroke();
      }
    }
  }
}

export function frameStats(frame) {
  let phiSum = 0, sSum = 0, resSum = 0, vMax = 0;

  const H = frame.phi.length;
  const W = frame.phi[0].length;
  const N = H * W;

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {

      phiSum += frame.phi[y][x];
      sSum   += frame.S[y][x];
      resSum += frame.residue[y][x];

      const v = Math.sqrt(frame.vx[y][x]**2 + frame.vy[y][x]**2);
      if (v > vMax) vMax = v;
    }
  }

  return {
    phi: (phiSum / N).toFixed(3),
    S:   (sSum   / N).toFixed(3),
    res: (resSum / N).toFixed(3),
    v:   vMax.toFixed(3)
  };
}