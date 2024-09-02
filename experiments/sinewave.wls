(* WolframScript to create a simple animated sine wave *)

frames = 50; (* Number of frames in the animation *)

(* Create a list of frames for the animation *)
framesList = Table[
   Plot[Sin[x - t], {x, 0, 2*Pi}, 
       PlotRange -> {-1.5, 1.5}, 
           Axes -> False, 
               PlotStyle -> {Thick, Blue},
                   ImageSize -> Medium
                       ],
                          {t, 0, 2*Pi, 2*Pi/frames}
                             ];

                             (* Export the frames as an animated GIF *)
                             Export["SimpleSineWaveAnimation.gif", framesList, "DisplayDurations" -> 0.1]

