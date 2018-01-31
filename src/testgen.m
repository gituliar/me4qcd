#!/usr/bin/env math-script
$LoadFeynArts = True;
<< FeynCalc`;

ScalarProduct[k,k] = 0;
ScalarProduct[k1,k1] = 0;
ScalarProduct[k2,k2] = 0;
ScalarProduct[k3,k3] = 0;
ScalarProduct[k4,k4] = 0;
ScalarProduct[k5,k5] = 0;
SUNN = 3;

ParseTestId[id_String] := Module[{i, o, l1, l2, s1, s2},
    {{i, o, l1, l2, s1, s2}} =
        StringCases[id,
            RegularExpression["^([auUdDg]+)2([auUdDg]+)_(\\d+)_(\\d+)(_([0-9+]+))?(_([0-9+]+))?$"] ->
                {"$1", "$2", "$3", "$4", "$6", "$8"}];
    {i, o, l1, l2, s1, If[s2 == "", s1, s2]}
]

MomentaNames[N_Integer, Prefix_String, SingleName_String] :=
    If[N == 1,
        {ToExpression[SingleName]},
        Table[ToExpression[StringJoin[Prefix, ToString[i]]], {i, 1, N}]]

MomentaNames[Id_String, Prefix_String, SingleName_String] :=
    MomentaNames[StringLength[Id], Prefix, SingleName]

Fields[Id_String] := Map[
    Switch[#,
        "a", V[1],
        "u", F[3, {1}],
        "U", -F[3, {1}],
        "d", F[4, {1}],
        "D", -F[4, {1}],
        "g", V[5]
    ]&,
    StringSplit[Id, ""]]

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
        IncomingMomenta -> MomentaNames[In, "p", "q"],
        OutgoingMomenta -> MomentaNames[Out, "k", "k"],
        LoopMomenta -> MomentaNames[ToExpression[Loops], LoopPrefix, StringJoin[LoopPrefix, "1"]],
        UndoChiralSplittings -> True,
        DropSumOver -> True,
        ChangeDimension -> n,
        List -> False,
        SMP -> True];
    Print["## Contract, SUNSimplify"];
    amp = amp /. {SMP["g_s"] -> 1, SMP["m_d"] -> 0, SMP["m_u"] -> 0, SMP["e"] -> 1, MQD[_] -> 0, MQU[_] -> 0};
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

$onshell = (Pair[Momentum[#, _], Momentum[#, _]] :> 0) & /@ MomentaNames[$o, "k", "k"];
me2 = me2 /. $onshell

Print["# FermionSpinSum"];
me2 = me2 // FermionSpinSum;

Print["# DiracTrace -> Tr"];
me2 = me2 /. $onshell;
me2 = me2 // ReplaceAll[#, {DiracTrace -> Tr}]&;
me2 = me2 /. $onshell;

Do[
    Print["# DoPolarizationSums[..., ", moment, ", GaugeTrickN -> 4]"];
    me2 = DoPolarizationSums[me2, moment, 0, VirtualBoson -> True, GaugeTrickN -> 4];
    me2 = me2 /. $onshell,
    {moment, Join[
        PolVirt[$i, MomentaNames[$i, "p", "q"]],
        PolVirt[$o, MomentaNames[$o, "k", "k"]]]}
];

Do[
    Print["# DoPolarizationSums[..., ", moment, "]"];
    me2 = DoPolarizationSums[me2, moment, 0];
    me2 = me2 /. $onshell,
    {moment, Join[
        PolReal[$i, MomentaNames[$i, "p", "q"]],
        PolReal[$o, MomentaNames[$o, "k", "k"]]]}
];

Print["# Expand"];
me2 = me2 /. Rule[Explicit, False] -> Rule[Explicit, True] // Expand;

Print["# Contract"];
me2 = me2 // Contract;

Print["# SUNSimplify"];
me2 = me2 // SUNSimplify[#, SUNNToCACF -> False] &;

norm = 9/4;
me2 = me2 //. Pair[Momentum[k1_, _], Momentum[k2_, _]] -> sp[k1, k2];
me2 = norm * me2 /. {n -> 4 - 2 ep, SUNN -> 3} /. $onshell;

(*Print["# Res=",me2]*)
Put[me2, $filename];
