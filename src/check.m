#!/usr/bin/env math-script


$Eval[got_, want_, momenta_] := Block[
  {amp, color, den, num, s, sp, r1, r2},

  sp[{Ep_,px_,py_,pz_}] := Ep^2-px^2-py^2-pz^2;
  sp[{Ep_,px_,py_,pz_},{Eq_,qx_,qy_,qz_}] := Ep*Eq-px*qx-py*qy-pz*qz;
  
  amp[_,_] := 1;
  
  color[ex_] := ex /. {
    Tf -> 1/2,
    Ca -> 3,
    Cf -> 4/3,
    Nf -> 3,
    Na -> 8};
  SUNN = 3;
  
  den[ex_] := 1/ex;
  num[ex_] := ex;
  
  k = {-q,k1,k2,k3,k4,k5};
  s[i_,j_] := sp[k[[i]]+k[[j]]];

  {got, want} /. momenta // Expand
];

$Check[got_, want_] := Module[{cgot, cwant, j, pass},
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

  pass = True;
  For[j=1, j<=Length[cgot], j++,
    gj = got[[j]];
    wj = want[[j]];
    dd = (gj-wj)/(gj+wj);
    If[
      !TrueQ[-10^-7 < dd < 10^-7]
      ,
      pass = False
    ];
  ];
  If[
    !TrueQ[pass]
    ,
    Print["[FAIL] Expressions look different"];
    Print["         got = ", got];
    Print["        want = ", want];
    Print["        diff = ", got-want];
  ];
  pass
];

got  = Get[$CommandLine[[4]]];
want = Get[$CommandLine[[5]]];
ps   = Get[$CommandLine[[6]]];

pass = True;
For[i=1, i<=Length[ps], i++,
  {ngot, nwant} = $Eval[got, want, ps[[i]]];
  pass = pass && $Check[ngot, nwant];
];
If[
  !TrueQ[pass]
  ,
  Exit[1]
];
