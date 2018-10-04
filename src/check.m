Random4Momentum[Mass_] := Module[{v1, v2, v3},
    {v1, v2, v3} = RandomReal[{-1, 1}, 3];
    {Sqrt[Mass^2 + v1^2 + v2^2 + v3^2], v1, v2, v3}
]

RandomPhasePoint[TotalE_, Masses_] := Module[{v, e, scale, sol},
    If[Length[Masses] == 1,
        {{TotalE, 0, 0, 0}},
        (* Find some arbitrary 3-momenta that sum to zero; scale
         * them by 'scale'; calculate 4-momenta from them using
         * the given masses; solve for 'scale' to obtain the
         * correct total energy.
         *)
        v = Map[RandomReal[{-1, 1}, 3]&, Masses];
        v = Map[scale*(# - Total[v]/Length[v])&, v];
        e = MapThread[Sqrt[(#1)^2 + Total[#2^2]]&, {Masses, v}];
        sol = NSolve[Total[e] == TotalE, scale];
        MapThread[Join[{#1*(1 + $MachineEpsilon)}, #2]&, {e, v}] /. RandomChoice[sol]
    ]
]

RandomDiagramMomenta[In_List, Out_List, Loop_List] := Module[{i, o, l, b},
    i = RandomPhasePoint[1.0, If[Length[In] === 1, {1.0}, Table[0.0, {Length[In]}]]];
    o = RandomPhasePoint[1.0, Table[0.0, {Length[Out]}]];
    l = Table[Random4Momentum[RandomReal[]], {Length[Loop]}];
    Join[
        MapThread[#1 -> #2&, {In, i}],
        MapThread[#1 -> #2&, {Out, o}],
        MapThread[#1 -> #2&, {Loop, l}]
    ]
]

MomentaNames[N_Integer, Prefix_String, SingleName_String] :=
    If[(N == 1),
        {ToExpression[SingleName]},
        Table[ToExpression[StringJoin[Prefix, ToString[i]]], {i, 1, N}]]

MomentaNames[Id_String, Prefix_String, SingleName_String] :=
    MomentaNames[StringLength[Id], Prefix, SingleName]

ParseDiagramId[id_String] :=
    StringCases[id,
        RegularExpression["^([auUdDg]+)2([auUdDg]+)_(\\d+)_(\\d+)(_.*)?$"] ->
            {"$1", "$2", "$3", "$4"}
    ][[1]]

RandomDiagramMomenta[id_String] := Module[{i, o, l1, l2},
    {i, o, l1, l2} = ParseDiagramId[id];
    i = MomentaNames[i, "p", "q"];
    o = MomentaNames[o, "k", "k1"];
    l1 = MomentaNames[ToExpression[l1], "l", "l1"];
    l2 = MomentaNames[ToExpression[l2], "r", "r1"];
    RandomDiagramMomenta[i, o, Join[l1, l2]]
]

$Eval[got_, want_, momenta_] := Expand[
    {got, want} /. momenta //. {
        sp[{Ep_,px_,py_,pz_}] :> Ep^2-px^2-py^2-pz^2,
        sp[{Ep_,px_,py_,pz_}, {Eq_,qx_,qy_,qz_}] :> Ep*Eq-px*qx-py*qy-pz*qz,
        amp[_, _] :> 1,
        m -> 4-2*ep,
        color[ex_] :> ex,
        Tf -> 1/2,
        Ca -> 3,
        Cf -> 4/3,
        Nf -> 3,
        Na -> 8,
        d33[c1_, c1_] :> (1/2)^3/(2*N)*(N^2 - 1)*(N^2 - 4),
        d44[c1_, c1_] :> (1/2)^4/(6*N^2)*(N^2 - 1)*(N^4 - 6*N^2 + 18),
        d55[c1_, c1_] :> (1/2)^5/(24*N^3)*(N^2 - 1)*(N^2 - 2)*(N^4 + 24),
        d433[c1_, c1_, c1_] :> (1/2)^5/(6*N^2)*(N^2 - 1)*(N^2 - 4)*(N^2 - 6),
        d66[c1_, c1_] :> (1/2)^6/(120*N^4)*(N^2 - 1)*(N^8 + 6*N^6 - 60*N^4 + 600),
        d633[c1_, c1_, c1_] :> (1/2)^6/(480*N^3)*(N^2 - 1)^2*(N^2 - 4)^2,
        d543[c1_, c1_, c1_] :> (1/2)^6/(288*N^3)*(N^2 - 1)*(N^2 - 4)*(N^4 - 6*N + 18),
        d444[c1_, c1_, c1_] :> (1/2)^6/(27*N^3)*(N^2 - 1)*(N^6 - 9*N^4 + 81*N^2 - 189),
        d3333[c1_, c1_, c1_, c1_] :> (1/2)^6/(8*N^2)*(N^2 - 1)*(N^2 - 4)*(N^2 - 12),
        SUNN -> 3,
        den[ex_] :> 1/ex,
        num[ex_] :> ex,
        NF -> 3,
        NA -> 8,
        N -> 3
    }
];

$Check[got_, want_] := Module[{cgot, cwant, pass},
  cgot  = CoefficientList[got, ep];
  cwant = CoefficientList[want, ep];
  If[
    Length[cgot] =!= Length[cwant]
    ,
    Print["[FAIL] Series of unequal order in ep"];
    Print["         got = ", got];
    Print["        want = ", want];
    Return[False];
  ];

  pass = And @@ MapThread[Abs[(#1 - #2)/(#1 + #2)] < 10^-7&, {cgot, cwant}];
  If[
    !TrueQ[pass]
    ,
    Print["[FAIL] Expressions look different"];
    Print["         got = ", got];
    Print["        want = ", want];
    Print["        diff = ", MapThread[#1-#2&, {cgot, cwant}]];
    Print["       ratio = ", MapThread[#1/#2&, {cgot, cwant}]];
  ];
  TrueQ[pass]
];

diag = $CommandLine[[4]];
got  = Get[$CommandLine[[5]]];
want = Get[$CommandLine[[6]]];

For[i = 1, i <= 20, i++,
    momenta = RandomDiagramMomenta[diag];
    {ngot, nwant} = $Eval[got, want, momenta];
    If[!$Check[ngot, nwant], Exit[1]]
];
