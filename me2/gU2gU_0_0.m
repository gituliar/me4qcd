( + amp[1,1]*col[Cf*Na*Tf]*den[sp[ - k1 - k2]]*den[sp[ - p1 - p2]] * ( 
         8*sp[k1,k2] - 8*sp[k1,k2]*m + 2*sp[k1,k2]*m^2 - 16*sp[k1,p1]*
         sp[k2,p2] + 16*sp[k1,p1]*sp[k2,p2]*m - 4*sp[k1,p1]*sp[k2,p2]*
         m^2 + 16*sp[k1,p2]*sp[k2,p1] - 16*sp[k1,p2]*sp[k2,p1]*m + 4*
         sp[k1,p2]*sp[k2,p1]*m^2 )

       + amp[1,2]*col[1/2*Ca*Na*Tf]*den[sp[ - k1 + p1]]*den[sp[ - p1 - 
      p2]] * (  - 16*sp[k1,k2] + 8*sp[k1,k2]*m + 16*sp[k1,p1]*sp[k2,p2]
          - 8*sp[k1,p1]*sp[k2,p2]*m + 16*sp[k1,p2]*sp[k2,p1] - 8*sp[k1,
         p2]*sp[k2,p1]*m + 32*sp[k1,p2]*sp[k2,p2] - 16*sp[k1,p2]*sp[k2,
         p2]*m - 8*sp[k2,p1] + 4*sp[k2,p1]*m - 8*sp[k2,p2] + 4*sp[k2,p2
         ]*m )

       + amp[1,3]*col[Cf*Na*Tf - 1/2*Ca*Na*Tf]*den[sp[k1 - p2]]*den[sp[
       - p1 - p2]] * ( 16*sp[k1,k2] - 12*sp[k1,k2]*m + 2*sp[k1,k2]*m^2
          - 64*sp[k1,p1]*sp[k2,p2] + 40*sp[k1,p1]*sp[k2,p2]*m - 4*sp[k1
         ,p1]*sp[k2,p2]*m^2 + 32*sp[k1,p2]*sp[k2,p1] - 24*sp[k1,p2]*sp[
         k2,p1]*m + 4*sp[k1,p2]*sp[k2,p1]*m^2 - 32*sp[k1,p2]*sp[k2,p2]
          + 16*sp[k1,p2]*sp[k2,p2]*m + 16*sp[k2,p2] - 8*sp[k2,p2]*m )

       + amp[2,1]*col[1/2*Ca*Na*Tf]*den[sp[ - k1 - k2]]*den[sp[k1 - p1]
      ] * (  - 16*sp[k1,k2] + 8*sp[k1,k2]*m - 16*sp[k1,k2]*sp[k1,p2] + 
         8*sp[k1,k2]*sp[k1,p2]*m - 16*sp[k1,k2]*sp[k2,p2] + 8*sp[k1,k2]
         *sp[k2,p2]*m + 16*sp[k1,p1]*sp[k2,p2] - 8*sp[k1,p1]*sp[k2,p2]*
         m + 16*sp[k1,p2]*sp[k2,p1] - 8*sp[k1,p2]*sp[k2,p1]*m + 32*sp[
         k2,p1]*sp[k2,p2] - 16*sp[k2,p1]*sp[k2,p2]*m )

       + amp[2,2]*col[Ca*Na*Tf]*den[sp[ - k1 + p1]]*den[sp[k1 - p1]]
       * ( 12*sp[k1,k2] + 4*sp[k1,k2]*m - 48*sp[k1,k2]*sp[k1,p2] + 8*
         sp[k1,k2]*sp[k1,p2]*m - 88*sp[k1,p1]*sp[k2,p2] + 24*sp[k1,p1]*
         sp[k2,p2]*m + 24*sp[k1,p2]*sp[k2,p1] + 8*sp[k1,p2]*sp[k2,p1]*m
          - 24*sp[k2,p1] + 4*sp[k2,p1]*m )

       + amp[2,3]*col[ - 1/2*Ca*Na*Tf]*den[sp[k1 - p1]]*den[sp[k1 - p2]
      ] * (  - 8*sp[k1,k2] + 4*sp[k1,k2]*m + 16*sp[k1,k2]*sp[k1,p2] - 8
         *sp[k1,k2]*sp[k1,p2]*m - 16*sp[k1,p1]*sp[k2,p2] + 8*sp[k1,p1]*
         sp[k2,p2]*m + 32*sp[k1,p2]*sp[k2,p1] - 16*sp[k1,p2]*sp[k2,p1]*
         m - 16*sp[k1,p2]*sp[k2,p2] + 8*sp[k1,p2]*sp[k2,p2]*m + 16*sp[
         k2,p2] - 8*sp[k2,p2]*m )

       + amp[3,1]*col[Cf*Na*Tf - 1/2*Ca*Na*Tf]*den[sp[ - k1 - k2]]*den[
      sp[ - k2 + p1]] * ( 16*sp[k1,k2] - 12*sp[k1,k2]*m + 2*sp[k1,k2]*
         m^2 + 32*sp[k1,k2]*sp[k2,p2] - 16*sp[k1,k2]*sp[k2,p2]*m - 64*
         sp[k1,p1]*sp[k2,p2] + 40*sp[k1,p1]*sp[k2,p2]*m - 4*sp[k1,p1]*
         sp[k2,p2]*m^2 + 32*sp[k1,p2]*sp[k2,p1] - 24*sp[k1,p2]*sp[k2,p1
         ]*m + 4*sp[k1,p2]*sp[k2,p1]*m^2 - 32*sp[k2,p1]*sp[k2,p2] + 16*
         sp[k2,p1]*sp[k2,p2]*m )

       + amp[3,2]*col[ - 1/2*Ca*Na*Tf]*den[sp[ - k1 + p1]]*den[sp[ - k2
       + p1]] * (  - 8*sp[k1,k2] + 4*sp[k1,k2]*m + 32*sp[k1,k2]*sp[k2,
         p2] - 16*sp[k1,k2]*sp[k2,p2]*m - 16*sp[k1,p1]*sp[k2,p2] + 8*
         sp[k1,p1]*sp[k2,p2]*m + 32*sp[k1,p2]*sp[k2,p1] - 16*sp[k1,p2]*
         sp[k2,p1]*m + 8*sp[k2,p1] - 4*sp[k2,p1]*m - 16*sp[k2,p1]*sp[k2
         ,p2] + 8*sp[k2,p1]*sp[k2,p2]*m )

       + amp[3,3]*col[Cf*Na*Tf]*den[sp[k1 - p2]]*den[sp[ - k2 + p1]]
       * ( 8*sp[k1,k2] - 8*sp[k1,k2]*m + 2*sp[k1,k2]*m^2 - 16*sp[k1,p1]
         *sp[k2,p2] + 16*sp[k1,p1]*sp[k2,p2]*m - 4*sp[k1,p1]*sp[k2,p2]*
         m^2 + 16*sp[k1,p2]*sp[k2,p1] - 16*sp[k1,p2]*sp[k2,p1]*m + 4*
         sp[k1,p2]*sp[k2,p1]*m^2 ))
