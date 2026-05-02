import { drawField, frameStats } from './renderer.js';

const canvas  = document.getElementById("canvas");
const ctx     = canvas.getContext("2d");
const loading = document.getElementById("loading");
const ui      = document.getElementById("ui");

let W = 80, H = 60;

function resize() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

// --- state ---
let frames = [];
let currentFrame = 0;
let mode = "field";
let playing = true;
let lastFrameTime = 0;
const FPS = 18;

// derive dynamically (critical)
let TOTAL_FRAMES = 0;

const phenomenon = {
  field:         "Entropy gradients reorganize scalar potential into coherent flow.",
  trajectory:    "Vector flow reveals the directional structure of transport.",
  repair:        "Coherent structure persists where entropy has not yet propagated.",
  fragmentation: "Structure breaks down where information cannot be preserved."
};

// --- mode control ---
function setMode(m) {
  mode = m;

  document.getElementById("phenomenon").textContent = phenomenon[m];

  document.querySelectorAll(".proj").forEach(el => {
    el.classList.toggle("active", el.dataset.mode === m);
  });

  render();
}

document.querySelectorAll(".proj").forEach(el => {
  el.onclick = () => setMode(el.dataset.mode);
});

// --- scrub ---
const scrub   = document.getElementById("scrub");
const counter = document.getElementById("frame-counter");

scrub.addEventListener("input", () => {
  currentFrame = parseInt(scrub.value);
  playing = false;
  render();
});

// click canvas to play/pause
canvas.addEventListener("click", () => { playing = !playing; });

// --- render ---
function render() {
  if (!frames.length) return;

  // clamp safety (important if data changes)
  currentFrame = Math.max(0, Math.min(currentFrame, frames.length - 1));

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const frame = frames[currentFrame];

  const cw = canvas.width / W;
  const ch = canvas.height / H;

  drawField(ctx, frame, mode, W, H, cw, ch);

  scrub.value = currentFrame;
  counter.textContent = `${currentFrame} / ${TOTAL_FRAMES - 1}`;

  // update status readout
  const st = frameStats(frame);
  document.getElementById("status").innerHTML =
    `φ̄ ${st.phi}  S̄ ${st.S}<br>res ${st.res}  |v|max ${st.v}`;
}

// --- animation loop ---
function animate(ts) {
  requestAnimationFrame(animate);

  if (!frames.length) return;

  if (playing) {
    if (ts - lastFrameTime > 1000 / FPS) {
      currentFrame = (currentFrame + 1) % frames.length;
      lastFrameTime = ts;
      render();
    }
  }
}

// --- load ---
async function loadFrames() {
  const res = await fetch("assets/data/field_all.json");
  frames = await res.json();

  // derive frame count dynamically
  TOTAL_FRAMES = frames.length;
  scrub.max = TOTAL_FRAMES - 1;

  // optional: infer grid size from data (future-proofing)
  if (frames.length && frames[0].phi) {
    H = frames[0].phi.length;
    W = frames[0].phi[0].length;
  }

  loading.style.display = "none";
  ui.style.display = "flex";

  setMode("field");

  // render immediately (no perceptual delay)
  render();

  requestAnimationFrame(animate);
}

loadFrames();