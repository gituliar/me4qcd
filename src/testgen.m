#!/usr/bin/env math-script
$LoadFeynArts = True;
<< FeynCalc`;

ScalarProduct[p,p] = 0;
ScalarProduct[p1,p1] = 0;
ScalarProduct[p2,p2] = 0;
ScalarProduct[p3,p3] = 0;
ScalarProduct[p4,p4] = 0;
ScalarProduct[p5,p5] = 0;
SUNN = 3;

ParseTestId[id_String] := Module[{i, o, l1, l2, s1, s2},
    {{i, o, l1, l2, s1, s2}} =
        StringCases[id,
            RegularExpression["^([a-z]+)2([a-z]+)_(\\d+)_(\\d+)(_([0-9+]+))?(_([0-9+]+))?$"] ->
                {"$1", "$2", "$3", "$4", "$6", "$8"}];
    {i, o, l1, l2, s1, If[s2 == "", s1, s2]}
]

MomentaNames[Prefix_String, N_Integer] :=
    If[N == 1,
        {ToExpression[Prefix]},
        Table[ToExpression[StringJoin[Prefix, ToString[i]]], {i, 1, N}]]

MomentaNames[Prefix_String, Id_String] :=
    MomentaNames[Prefix, StringLength[Id]]

Fields[Id_String] := Module[{oddq},
    oddq = False;
    Map[
        Switch[#,
            "a", V[1],
            "q", If[oddq = !oddq, F[3,{1}], -F[3,{1}]],
            "g", V[5]
        ]&,
        StringSplit[Id, ""]
    ]
]

PolVirt[Id_String, Momenta_List] :=
    MapThread[
        Switch[#1, "a", #2, _, Null]&,
        {StringSplit[Id, ""], Momenta}] //
    DeleteCases[#, Null]&

PolReal[Id_String, Momenta_List] :=
    MapThread[
        Switch[#1, "g", #2, _, Null] &,
        {StringSplit[Id, ""], Momenta}] //
    DeleteCases[#, Null]&

MkAmplitude[In_, Out_, Loops_, Topologies_, LoopPrefix_] := Module[{top, diag, famp, amp},
    Print["## CreateTopologies[", In, " -> ", Out, ", loops=", Loops, "]"];
    top = CreateTopologies[
        ToExpression[Loops],
        StringLength[In] -> StringLength[Out]
    ];
    Print["## InsertFields"];
    diag = InsertFields[
        top,
        Fields[In] -> Fields[Out],
        InsertionLevel -> {Classes},
        Model -> "SMQCD",
        ExcludeParticles -> {S, U, SV, V[1], V[2], V[3], V[4], F[1], F[2]}
    ];
    If[Topologies =!= "",
        Print["## SelectTopologies[", Topologies, "]"];
        diag = diag /.
            TopologyList[m__][ds__] :>
            TopologyList[m][
                Sequence @@ List[ds][[ToExpression[StringSplit[Topologies, "+"]]]]]];
    Print["## CreateFeynAmp"];
    famp = CreateFeynAmp[diag, Truncated -> False];
    Print["## FCFAConvert"];
    amp = FCFAConvert[
        famp,
        IncomingMomenta -> MomentaNames["q", In],
        OutgoingMomenta -> MomentaNames["p", Out],
        LoopMomenta -> MomentaNames[LoopPrefix, ToExpression[Loops]],
        UndoChiralSplittings -> True,
        DropSumOver -> True,
        ChangeDimension -> n,
        List -> False,
        SMP -> True];
    Print["## Contract, SUNSimplify"];
    amp = amp /. {SMP["g_s"] -> 1, SMP["m_u"] -> 0, SMP["e"] -> 1};
    amp = amp // Contract // SUNSimplify[#, SUNNToCACF -> False] &
]

$testid = $CommandLine[[4]];
$filename = $CommandLine[[5]];

{$i, $o, $l1, $l2, $s1, $s2} = ParseTestId[$testid];
Print["# ", $i, " -> ", $o, "; l1=", $l1, ", l2=", $l2];
a1 = MkAmplitude[$i, $o, $l1, $s1, "l"];
a2 = MkAmplitude[$i, $o, $l2, $s2, "r"];
me2 = a1*(ComplexConjugate[a2] // FCRenameDummyIndices);

Print["# SUNSimplify"];
me2 = me2 // SUNSimplify[#, SUNNToCACF -> False] &;

Print["# PropagatorDenominatorExplicit"];
me2 = me2 // PropagatorDenominatorExplicit;

$onshell = (Pair[Momentum[#, _], Momentum[#, _]] :> 0) & /@ MomentaNames["p", $o];
me2 = me2 /. $onshell

Print["# FermionSpinSum"];
me2 = me2 // FermionSpinSum;

Print["# DiracTrace -> Tr"];
me2 = me2 /. $onshell;
me2 = me2 // ReplaceAll[#, {DiracTrace -> Tr}]&;
me2 = me2 /. $onshell;

Do[
    Print["# DoPolarizationSums[..., ", p, ", GaugeTrickN -> 4]"];
    me2 = DoPolarizationSums[me2, p, 0, VirtualBoson -> True, GaugeTrickN -> 4];
    me2 = me2 /. $onshell,
    {p, PolVirt[$i, MomentaNames["q", $i]]}
];

Do[
    Print["# DoPolarizationSums[..., ", p, "]"];
    me2 = DoPolarizationSums[me2, p, 0];
    me2 = me2 /. $onshell,
    {p, PolReal[$o, MomentaNames["p", $o]]}
];

Print["# Expand"];
me2 = me2 /. Rule[Explicit, False] -> Rule[Explicit, True] // Expand;
Print["# SUNSimplify"];
me2 = me2 // SUNSimplify[#, SUNNToCACF -> False] &;

norm = 9/4;
me2 = me2 //. Pair[Momentum[k1_, _], Momentum[k2_, _]] -> sp[k1, k2];
me2 = me2 /. MapThread[#1 -> #2&, {MomentaNames["p", $o], MomentaNames["k", $o]}];
me2 = norm * me2 /. {n -> 4 - 2 ep, SUNN -> 3} /. $onshell;

(*Print["# Res=",me2]*)
Put[me2, $filename];
