#!/usr/bin/env math-script
$LoadFeynArts = True;
<< FeynCalc`;

ScalarProduct[k1,k1] = 0;
ScalarProduct[k2,k2] = 0;
ScalarProduct[k3,k3] = 0;
ScalarProduct[k4,k4] = 0;
ScalarProduct[k5,k5] = 0;
ScalarProduct[p,p] = 0;
ScalarProduct[p1,p1] = 0;
ScalarProduct[p2,p2] = 0;
ScalarProduct[p3,p3] = 0;
ScalarProduct[p4,p4] = 0;
ScalarProduct[p5,p5] = 0;
SUNN = 3;

(* Split a test ID like "abc2def_n1_n2_l1+l2+l3_r1+r2" into
 * {"abc", "def", "n1", "n2", "l1+l2+l3", "r1+r2"}
 *)
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

MkAmplitude[In_, Out_, Loops_, Topologies_, LoopPrefix_, Filename_] := Module[{top, diag, famp, amp},
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
    (*
    Print["## Export diagram to ", Filename];
    Paint[diag, AutoEdit -> False, DisplayFunction -> (Export[Filename, #] &)];
    *)
    Print["## CreateFeynAmp"];
    famp = CreateFeynAmp[diag, Truncated -> False];
    Print["## FCFAConvert"];
    amp = FCFAConvert[
        famp,
        IncomingMomenta -> MomentaNames[In, "p", "q"],
        OutgoingMomenta -> MomentaNames[Out, "k", "k1"],
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
a1 = MkAmplitude[$i, $o, $l1, $s1, "l", StringJoin[$filename, "-left.pdf"]];
a2 = MkAmplitude[$i, $o, $l2, $s2, "r", StringJoin[$filename, "-right.pdf"]];
me2 = a1*(ComplexConjugate[a2] // FCRenameDummyIndices);

Print["# FermionSpinSum"];
me2 = me2 // FermionSpinSum;

Print["# SUNSimplify"];
me2 = me2 // SUNSimplify[#, SUNNToCACF -> False] &;

Print["# PropagatorDenominatorExplicit"];
me2 = me2 // PropagatorDenominatorExplicit;

(* Note: this list never includes q^2 == 0 *)
$onshell = Map[
    (Pair[Momentum[#, _], Momentum[#, _]] :> 0) &,
    Join[MomentaNames[$i, "p", "p"], MomentaNames[$o, "k", "k1"]]];
me2 = me2 /. $onshell

Print["# DiracTrace -> Tr"];
me2 = me2 /. $onshell;
me2 = me2 // ReplaceAll[#, {DiracTrace -> Tr}]&;
me2 = me2 /. $onshell;

Print["# CalcColorFactor"];
me2 = me2 // CalcColorFactor;

PolarizedMomenta[particles_String, prefix_String, singlename_String] :=
    MapThread[
        If[StringMatchQ[#1, "a" | "g"], #2, Nothing]&,
        {StringSplit[particles, ""], MomentaNames[particles, prefix, singlename]}]

(* Only a single incoming particle is virtual. The rest are real. *)
Do[
    Print["# DoPolarizationSums[..., ", moment, ", GaugeTrickN -> 4]"];
    me2 = DoPolarizationSums[me2, moment, 0, VirtualBoson -> True, GaugeTrickN -> 4];
    me2 = me2 /. $onshell,
    {moment, If[StringLength[$i] == 1, PolarizedMomenta[$i, "p", "q"], {}]}
];

Do[
    If[
       moment =!= Nothing
       ,
       Print["# DoPolarizationSums[..., ", moment, "]"];
       me2 = DoPolarizationSums[me2, moment, 0];
       me2 = me2 /. $onshell;
    ]
    ,
    {moment, Join[
        If[StringLength[$i] == 1, {}, PolarizedMomenta[$i, "p", "q"]],
        PolarizedMomenta[$o, "k", "k1"]]}
];

Print["# Expand"];
me2 = me2 /. Rule[Explicit, False] -> Rule[Explicit, True] // Expand;

Print["# Contract"];
me2 = me2 // Contract;

Print["# SUNSimplify"];
me2 = me2 // SUNSimplify[#, SUNNToCACF -> False] &;

me2 = me2 //. Pair[Momentum[a_, _], Momentum[b_, _]] -> sp[a, b];
me2 = me2 /. {n -> 4 - 2 ep, SUNN -> 3} /. $onshell;

(*Print["# Res=",me2]*)
Put[me2, $filename];
