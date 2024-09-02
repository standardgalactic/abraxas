#!/usr/bin/env wolframscript

(* This is a complete WolframScript that generates a Hasse diagram and saves it to a file. *)

(* Define the function s2v to convert a set to a vertex number *)
s2v[n_Integer?Positive, l_List] := 1 /; Length[l] == 0
s2v[n_Integer?Positive, l_List] := 2^n /; Length[l] == n
s2v[n_Integer?Positive, l_List] := Sum[Binomial[n, o], {o, 0, Length[l] - 1}] + Position[Subsets[Range[n], {Length[l]}], l][[1, 1]] /; 0 < Length[l] < n

(* Define the function zevHasseD to generate a Hasse diagram *)
zevHasseD[n_Integer?Positive, zev_List] := Module[{pS, zevS, gR, gV, gC, gH},
    pS = Subsets[Range[n]];
        gR = Flatten[Table[UndirectedEdge @@ Sort[{s2v[n, pS[[i]]], s2v[n, pS[[j]]]}], {i, Length[pS]}, {j, i + 1, Length[pS]}], 1];
            gV = Table[s2v[n, pS[[i]]] -> ToString[pS[[i]]], {i, Length[pS]}];
                gC = Table[s2v[n, pS[[i]]] -> {Mod[i, n + 1]*40, -Quotient[i, n + 1]*40}, {i, Length[pS]}];
                    zevS = Sort[s2v[n, #] & /@ zev];
                        gH = HighlightGraph[Graph[Range[2^n], gR, VertexLabels -> gV, VertexCoordinates -> gC, GraphLayout -> "LayeredDigraphEmbedding"], zevS];
                            gH
                            ];

                            (* Generate the Hasse diagram for the given sets *)
                            graph = zevHasseD[5, {{1, 5}, {1, 3, 4}, {1, 5, 3, 4}, {2, 3}, {3, 4, 5}, {2, 3, 6}}];

                            (* Export the graph to a PNG file *)
                            Export["hasseDiagram.png", graph];

                            (* Print out a confirmation message *)
                            Print["Graph exported to hasseDiagram.png"];

