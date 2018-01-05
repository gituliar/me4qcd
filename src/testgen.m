#!/usr/bin/env math-script

mask = $CommandLine[[4]];
fout = $CommandLine[[5]];

mask = StringSplit[mask, "_"];
pid[1] = mask[[1]] <> mask[[2]];
pid[2] = mask[[1]] <> mask[[3]];
sel[1] = {};
sel[2] = {};
ParseSelector[str_]:=ToExpression /@ StringSplit[str, "+"];
Switch[
  Length[mask]
  ,
  4,
  sel[1] = mask[[4]] // ParseSelector;
  sel[2] = mask[[4]] // ParseSelector;
  ,
  5,
  sel[1] = mask[[4]] // ParseSelector;
  sel[2] = mask[[5]] // ParseSelector;
];


$LoadFeynArts = True;
<< FeynCalc`;

ScalarProduct[p1,p1] = 0;
ScalarProduct[p2,p2] = 0;
ScalarProduct[p3,p3] = 0;
ScalarProduct[p4,p4] = 0;
ScalarProduct[p5,p5] = 0;

SUNN = 3;

For[i=1, i<=2, i++,
  Switch[
    pid[i]
    ,
    (* 1 -> 3 tree *)
    "a2qqg0",
    loop[i] = 0;
    proc[i] = {V[1]} -> {F[3,{1}], -F[3,{1}], V[5]};
    selmod[i] = {};
    momin = {q};
    momout = {p1,p2,p3};
    norm = 9/4;
    polvirt = {q};
    polreal = {p3};
    ,
    (* 1 -> 4 tree *)
    "a2qqgg0",
    loop[i] = 0;
    proc[i] = {V[1]} -> {F[3,{1}], -F[3,{1}], V[5], V[5]};
    selmod[i] = {};
    momin = {q};
    momout = {p1,p2,p3,p4};
    norm = 9/4;
    polvirt = {q};
    polreal = {p3, p4};
    ,
    (* 1 -> 4 tree *)
    "a2qqqq0",
    loop[i] = 0;
    proc[i] = {V[1]} -> {F[3,{1}], -F[3,{1}], F[3,{1}], -F[3,{1}]};
    selmod[i] = {};
    momin = {q};
    momout = {p1,p2,p3,p4};
    norm = 9/4;
    polvirt = {q};
    polreal = {};
    ,
    (* 1 -> 5 tree *)
    "a2qqqq0",
    loop[i] = 0;
    proc[i] = {V[1]} -> {F[3,{1}], -F[3,{1}], F[3,{1}], -F[3,{1}], V[5]};
    selmod[i] = {};
    momin = {q};
    momout = {p1,p2,p3,p4,p5};
    norm = 9/4;
    polvirt = {q};
    polreal = {p5};
  ];

  top[i] = CreateTopologies[
    loop[i],
    Length /@ (proc[i])
  ];
  diag[i] = InsertFields[
    top[i],
    proc[i],
    InsertionLevel -> {Classes},
    Model -> "SMQCD", 
    ExcludeParticles -> {S[1], S[2], V[1], V[2]}
  ];
  If[
    sel[i] =!= {}
    ,
    diag[i] = diag[i] /. TopologyList[m__][ds__] :> TopologyList[m][Sequence @@ List[ds][[sel[i] /. selmod[i]]]];
  ];

  amp[i] = FCFAConvert[
    CreateFeynAmp[diag[i], Truncated -> False], 
    IncomingMomenta -> momin,
    OutgoingMomenta -> momout, 
    UndoChiralSplittings -> True,
    DropSumOver -> True,
    List -> False, 
    SMP -> True] // Contract // ChangeDimension[#, n] &;
];

Print["#1"];
me2 = amp[1]*(ComplexConjugate[amp[2]] // FCRenameDummyIndices);
me2 = me2 /. {SMP["g_s"] -> 1, SMP["m_u"] -> 0, SMP["e"] -> 1};
$onshell = (Pair[Momentum[#,_],Momentum[#,_]] :> 0) & /@ {p1,p2,p3,p4,p5};
Print[$onshell];
me2 = me2 /. $onshell

Print["#2.1"];
me2 = me2 // PropagatorDenominatorExplicit;
Print["#2.2"];
me2 = me2 // FermionSpinSum;
Print["#2.3"];
me2 = me2 /. $onshell;
me2 = me2 // ReplaceAll[#, {DiracTrace -> Tr}]&;
Print[me2];
me2 = me2 /. $onshell;

Print["#3"];
For[i=1, i<=Length[polvirt], i++,
  Print["#3.",i];
  me2 = me2 // DoPolarizationSums[#, polvirt[[i]], 0, VirtualBoson -> True, GaugeTrickN -> 4]&;
(*
  Print[me2];
*)
  me2 = me2 /. $onshell;
];

Print["#4"];
For[i=1, i<=Length[polreal], i++,
  Print["#4.",i];
  me2 = me2 // DoPolarizationSums[#, polreal[[i]], 0]&;
(*
  Print[me2];
*)
  me2 = me2 /. $onshell;
];

Print["#5"];
me2 = me2 // SUNSimplify[#, SUNNToCACF -> False] &;
me2 = me2 /. Rule[Explicit, False] -> Rule[Explicit, True] // Expand // SUNSimplify[#, SUNNToCACF -> False] &;

me2 = me2 //. {Pair[Momentum[k1_, _], Momentum[k2_, _]] -> sp[k1, k2], p1 -> k1, p2 -> k2, p3 -> k3, p4 -> k4, p5 -> k5};
me2 = norm * me2 /. {n -> 4 - 2 ep, SUNN -> 3} /. $onshell;

Put[me2, fout];
