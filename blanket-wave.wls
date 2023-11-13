#!/usr/bin/env wolframscript

(* Define the wave function *)
waveFunction[x_, y_, t_] := Sin[x + t] * Cos[y + t];

(* Generate and export the animation *)
Export["waveAnimation.gif", 
  Table[Plot3D[waveFunction[x, y, t], {x, -Pi, Pi}, {y, -Pi, Pi},
    PlotRange -> {-1, 1}, Mesh -> None, ColorFunction -> "Rainbow",
    Boxed -> False, Axes -> False], {t, 0, 2 Pi, 0.1}],
  "DisplayDurations" -> 0.1, "AnimationRepetitions" -> Infinity
]

