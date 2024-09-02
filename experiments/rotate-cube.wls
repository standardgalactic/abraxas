(* WolframScript to create a 3D animation of a rotating cube *)

frames = 50; (* Number of frames in the animation *)

(* Create a list of frames for the animation *)
framesList = Table[
   Graphics3D[
    {Opacity[0.7], Blue, 
     Cuboid[{-0.5, -0.5, -0.5}, {0.5, 0.5, 0.5}]}, 
    Boxed -> False, 
    ViewAngle -> Pi/6, 
    ViewPoint -> {Sin[t], Cos[t], 1}, 
    Lighting -> "Neutral",
    ImageSize -> Medium
    ],
   {t, 0, 2*Pi, 2*Pi/frames}
   ];

(* Export the frames as an animated GIF *)
Export["RotatingCubeAnimation.gif", framesList, "DisplayDurations" -> 0.1]
