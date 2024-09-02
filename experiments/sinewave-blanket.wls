(* WolframScript to create a 3D animation of a sine wave blanket moving in and out *)

frames = 50; (* Number of frames in the animation *)
amplitude = 0.5; (* Amplitude of the wave *)
frequency = 2; (* Frequency of the wave *)
speed = 0.2; (* Speed of the wave *)

(* Create a list of frames for the animation *)
framesList = Table[
   Graphics3D[
    {
     Opacity[0.7], Blue,
     Table[
      {EdgeForm[], 
       Polygon[
        Table[
         {x, y, amplitude * Sin[frequency * (x + t) + speed * y]},
         {x, 0, 2 * Pi, Pi/15}
        ]
       ]},
      {y, 0, 2 * Pi, Pi/15}
     ]
    },
    Boxed -> False,
    Lighting -> "Neutral",
    ViewPoint -> {1.5 * Sin[t], 1.5 * Cos[t], 1}, (* Dynamic rotating viewpoint *)
    PlotRange -> All,
    ImageSize -> Medium
    ],
   {t, 0, 2 * Pi, 2 * Pi / frames}
   ];

(* Export the frames as an animated GIF *)
Export["SineWaveBlanketAnimation.gif", framesList, "DisplayDurations" -> 0.1]
