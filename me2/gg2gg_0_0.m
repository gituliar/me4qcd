( + amp[1,1,5]*col[Ca^2*Na] * (  - 2*m + 2*m^2 )

       + amp[1,1,6]*col[1/2*Ca^2*Na] * (  - m + m^2 )

       + amp[1,1,7]*col[ - 1/2*Ca^2*Na] * ( m - m^2 )

       + amp[1,1,9]*col[1/2*Ca^2*Na] * (  - m + m^2 )

       + amp[1,1,10]*col[Ca^2*Na] * (  - 2*m + 2*m^2 )

       + amp[1,1,11]*col[1/2*Ca^2*Na] * (  - m + m^2 )

       + amp[1,1,13]*col[ - 1/2*Ca^2*Na] * ( m - m^2 )

       + amp[1,1,14]*col[1/2*Ca^2*Na] * (  - m + m^2 )

       + amp[1,1,15]*col[Ca^2*Na] * (  - 2*m + 2*m^2 )

       + amp[1,2,1]*col[Ca^2*Na]*den[sp[ - k1 - k2]] * ( 12*sp[k1,k2]
          - 12*sp[k1,k2]*m + 3*sp[k1,p1] - 3*sp[k1,p1]*m + 3*sp[k1,p2]
          - 3*sp[k1,p2]*m + 3*sp[k2,p1] - 3*sp[k2,p1]*m + 3*sp[k2,p2]
          - 3*sp[k2,p2]*m )

       + amp[1,2,2]*col[1/2*Ca^2*Na]*den[sp[ - k1 - k2]] * ( 6*sp[k1,k2
         ] - 6*sp[k1,k2]*m - sp[k1,p1] + 2*sp[k1,p1]*m - sp[k1,p1]*m^2
          + 4*sp[k1,p2] - 5*sp[k1,p2]*m + sp[k1,p2]*m^2 + 4*sp[k2,p1]
          - 5*sp[k2,p1]*m + sp[k2,p1]*m^2 - sp[k2,p2] + 2*sp[k2,p2]*m
          - sp[k2,p2]*m^2 )

       + amp[1,2,3]*col[ - 1/2*Ca^2*Na]*den[sp[ - k1 - k2]] * (  - 6*
         sp[k1,k2] + 6*sp[k1,k2]*m - 4*sp[k1,p1] + 5*sp[k1,p1]*m - sp[
         k1,p1]*m^2 + sp[k1,p2] - 2*sp[k1,p2]*m + sp[k1,p2]*m^2 + sp[k2
         ,p1] - 2*sp[k2,p1]*m + sp[k2,p1]*m^2 - 4*sp[k2,p2] + 5*sp[k2,
         p2]*m - sp[k2,p2]*m^2 )

       + amp[1,3,1]*col[1/2*Ca^2*Na]*den[sp[ - k1 + p1]] * ( 1/2 - m + 
         1/2*m^2 + sp[k1,k2] - 2*sp[k1,k2]*m + sp[k1,k2]*m^2 - 6*sp[k1,
         p1] + 6*sp[k1,p1]*m + 4*sp[k1,p2] - 5*sp[k1,p2]*m + sp[k1,p2]*
         m^2 + 4*sp[k2,p1] - 5*sp[k2,p1]*m + sp[k2,p1]*m^2 )

       + amp[1,3,2]*col[Ca^2*Na]*den[sp[ - k1 + p1]] * (  - 3/2 + 3/2*m
          - 3*sp[k1,k2] + 3*sp[k1,k2]*m - 12*sp[k1,p1] + 12*sp[k1,p1]*m
          + 3*sp[k1,p2] - 3*sp[k1,p2]*m + 3*sp[k2,p1] - 3*sp[k2,p1]*m )

       + amp[1,3,3]*col[1/2*Ca^2*Na]*den[sp[ - k1 + p1]] * (  - 2 + 5/2
         *m - 1/2*m^2 - 4*sp[k1,k2] + 5*sp[k1,k2]*m - sp[k1,k2]*m^2 - 6
         *sp[k1,p1] + 6*sp[k1,p1]*m - sp[k1,p2] + 2*sp[k1,p2]*m - sp[k1
         ,p2]*m^2 - sp[k2,p1] + 2*sp[k2,p1]*m - sp[k2,p1]*m^2 )

       + amp[1,4,1]*col[ - 1/2*Ca^2*Na]*den[sp[ - k1 + p2]] * (  - 1/2
          + m - 1/2*m^2 - sp[k1,k2] + 2*sp[k1,k2]*m - sp[k1,k2]*m^2 - 4
         *sp[k1,p1] + 5*sp[k1,p1]*m - sp[k1,p1]*m^2 + 6*sp[k1,p2] - 6*
         sp[k1,p2]*m - 4*sp[k2,p2] + 5*sp[k2,p2]*m - sp[k2,p2]*m^2 )

       + amp[1,4,2]*col[1/2*Ca^2*Na]*den[sp[ - k1 + p2]] * (  - 2 + 5/2
         *m - 1/2*m^2 - 4*sp[k1,k2] + 5*sp[k1,k2]*m - sp[k1,k2]*m^2 - 
         sp[k1,p1] + 2*sp[k1,p1]*m - sp[k1,p1]*m^2 - 6*sp[k1,p2] + 6*
         sp[k1,p2]*m - sp[k2,p2] + 2*sp[k2,p2]*m - sp[k2,p2]*m^2 )

       + amp[1,4,3]*col[Ca^2*Na]*den[sp[ - k1 + p2]] * (  - 3/2 + 3/2*m
          - 3*sp[k1,k2] + 3*sp[k1,k2]*m + 3*sp[k1,p1] - 3*sp[k1,p1]*m
          - 12*sp[k1,p2] + 12*sp[k1,p2]*m + 3*sp[k2,p2] - 3*sp[k2,p2]*m
          )

       + amp[2,1,1]*col[Ca^2*Na]*den[sp[ - p1 - p2]] * ( 6 - 6*m + 3*
         sp[k1,p1] - 3*sp[k1,p1]*m + 3*sp[k1,p2] - 3*sp[k1,p2]*m + 3*
         sp[k2,p1] - 3*sp[k2,p1]*m + 3*sp[k2,p2] - 3*sp[k2,p2]*m )

       + amp[2,1,2]*col[1/2*Ca^2*Na]*den[sp[ - p1 - p2]] * ( 3 - 3*m - 
         sp[k1,p1] + 2*sp[k1,p1]*m - sp[k1,p1]*m^2 + 4*sp[k1,p2] - 5*
         sp[k1,p2]*m + sp[k1,p2]*m^2 + 4*sp[k2,p1] - 5*sp[k2,p1]*m + 
         sp[k2,p1]*m^2 - sp[k2,p2] + 2*sp[k2,p2]*m - sp[k2,p2]*m^2 )

       + amp[2,1,3]*col[ - 1/2*Ca^2*Na]*den[sp[ - p1 - p2]] * (  - 3 + 
         3*m - 4*sp[k1,p1] + 5*sp[k1,p1]*m - sp[k1,p1]*m^2 + sp[k1,p2]
          - 2*sp[k1,p2]*m + sp[k1,p2]*m^2 + sp[k2,p1] - 2*sp[k2,p1]*m
          + sp[k2,p1]*m^2 - 4*sp[k2,p2] + 5*sp[k2,p2]*m - sp[k2,p2]*m^2
          )

       + amp[2,2]*col[Ca^2*Na]*den[sp[ - k1 - k2]]*den[sp[ - p1 - p2]]
       * ( 18*sp[k1,k2] - 2*sp[k1,k2]*m + 3*sp[k1,k2]*sp[k1,p1] + 3*sp[
         k1,k2]*sp[k1,p2] + 3*sp[k1,k2]*sp[k2,p1] + 3*sp[k1,k2]*sp[k2,
         p2] + 3/2*sp[k1,p1] - 9*sp[k1,p1]^2 + 3*sp[k1,p1]^2*m + sp[k1,
         p1]^2*m^2 - 36*sp[k1,p1]*sp[k1,p2] + 24*sp[k1,p1]*sp[k1,p2]*m
          - 2*sp[k1,p1]*sp[k1,p2]*m^2 - 36*sp[k1,p1]*sp[k2,p1] + 24*sp[
         k1,p1]*sp[k2,p1]*m - 2*sp[k1,p1]*sp[k2,p1]*m^2 - 36*sp[k1,p1]*
         sp[k2,p2] + 18*sp[k1,p1]*sp[k2,p2]*m + 2*sp[k1,p1]*sp[k2,p2]*
         m^2 + 3/2*sp[k1,p2] - 9*sp[k1,p2]^2 + 3*sp[k1,p2]^2*m + sp[k1,
         p2]^2*m^2 - 36*sp[k1,p2]*sp[k2,p1] + 18*sp[k1,p2]*sp[k2,p1]*m
          + 2*sp[k1,p2]*sp[k2,p1]*m^2 - 36*sp[k1,p2]*sp[k2,p2] + 24*sp[
         k1,p2]*sp[k2,p2]*m - 2*sp[k1,p2]*sp[k2,p2]*m^2 + 3/2*sp[k2,p1]
          - 9*sp[k2,p1]^2 + 3*sp[k2,p1]^2*m + sp[k2,p1]^2*m^2 - 36*sp[
         k2,p1]*sp[k2,p2] + 24*sp[k2,p1]*sp[k2,p2]*m - 2*sp[k2,p1]*sp[
         k2,p2]*m^2 + 3/2*sp[k2,p2] - 9*sp[k2,p2]^2 + 3*sp[k2,p2]^2*m
          + sp[k2,p2]^2*m^2 )

       + amp[2,3]*col[1/2*Ca^2*Na]*den[sp[ - k1 + p1]]*den[sp[ - p1 - 
      p2]] * ( 11/4 - 7/4*m + 5/2*sp[k1,k2] - 2*sp[k1,k2]*m + 3*sp[k1,
         k2]*sp[k1,p1] - 2*sp[k1,k2]*sp[k1,p1]*m + 6*sp[k1,k2]*sp[k1,p2
         ] - 4*sp[k1,k2]*sp[k1,p2]*m + 10*sp[k1,k2]*sp[k2,p1] - 5*sp[k1
         ,k2]*sp[k2,p1]*m + 20*sp[k1,k2]*sp[k2,p2] - 10*sp[k1,k2]*sp[k2
         ,p2]*m - sp[k1,p1] - 4*sp[k1,p1]*m + 11*sp[k1,p1]^2 - 7*sp[k1,
         p1]^2*m - 14*sp[k1,p1]*sp[k1,p2] + 6*sp[k1,p1]*sp[k1,p2]*m - 2
         *sp[k1,p1]*sp[k2,p1] - sp[k1,p1]*sp[k2,p1]*m + 5*sp[k1,p1]*sp[
         k2,p2] - 4*sp[k1,p1]*sp[k2,p2]*m + 7*sp[k1,p2] - 3*sp[k1,p2]*m
          - 18*sp[k1,p2]^2 + 10*sp[k1,p2]^2*m - 6*sp[k1,p2]*sp[k2,p1]
          + 4*sp[k1,p2]*sp[k2,p1]*m - 6*sp[k1,p2]*sp[k2,p2] + 4*sp[k1,
         p2]*sp[k2,p2]*m + sp[k2,p1] + 1/2*sp[k2,p1]*m - 14*sp[k2,p1]^2
          + 7*sp[k2,p1]^2*m - 10*sp[k2,p1]*sp[k2,p2] + 5*sp[k2,p1]*sp[
         k2,p2]*m + 3/2*sp[k2,p2] - sp[k2,p2]*m )

       + amp[2,4]*col[ - 1/2*Ca^2*Na]*den[sp[ - k1 + p2]]*den[sp[ - p1
       - p2]] * (  - 11/4 + 7/4*m - 5/2*sp[k1,k2] + 2*sp[k1,k2]*m - 6*
         sp[k1,k2]*sp[k1,p1] + 4*sp[k1,k2]*sp[k1,p1]*m - 3*sp[k1,k2]*
         sp[k1,p2] + 2*sp[k1,k2]*sp[k1,p2]*m - 20*sp[k1,k2]*sp[k2,p1]
          + 10*sp[k1,k2]*sp[k2,p1]*m - 10*sp[k1,k2]*sp[k2,p2] + 5*sp[k1
         ,k2]*sp[k2,p2]*m - 7*sp[k1,p1] + 3*sp[k1,p1]*m + 18*sp[k1,p1]^
         2 - 10*sp[k1,p1]^2*m + 14*sp[k1,p1]*sp[k1,p2] - 6*sp[k1,p1]*
         sp[k1,p2]*m + 6*sp[k1,p1]*sp[k2,p1] - 4*sp[k1,p1]*sp[k2,p1]*m
          + 6*sp[k1,p1]*sp[k2,p2] - 4*sp[k1,p1]*sp[k2,p2]*m + sp[k1,p2]
          + 4*sp[k1,p2]*m - 11*sp[k1,p2]^2 + 7*sp[k1,p2]^2*m - 5*sp[k1,
         p2]*sp[k2,p1] + 4*sp[k1,p2]*sp[k2,p1]*m + 2*sp[k1,p2]*sp[k2,p2
         ] + sp[k1,p2]*sp[k2,p2]*m - 3/2*sp[k2,p1] + sp[k2,p1]*m + 10*
         sp[k2,p1]*sp[k2,p2] - 5*sp[k2,p1]*sp[k2,p2]*m - sp[k2,p2] - 1/
         2*sp[k2,p2]*m + 14*sp[k2,p2]^2 - 7*sp[k2,p2]^2*m )

       + amp[3,1,1]*col[1/2*Ca^2*Na]*den[sp[k1 - p1]] * ( 1/2 - m + 1/2
         *m^2 + sp[k1,k2] - 2*sp[k1,k2]*m + sp[k1,k2]*m^2 - 6*sp[k1,p1]
          + 6*sp[k1,p1]*m + 4*sp[k1,p2] - 5*sp[k1,p2]*m + sp[k1,p2]*m^2
          + 4*sp[k2,p1] - 5*sp[k2,p1]*m + sp[k2,p1]*m^2 )

       + amp[3,1,2]*col[Ca^2*Na]*den[sp[k1 - p1]] * (  - 3/2 + 3/2*m - 
         3*sp[k1,k2] + 3*sp[k1,k2]*m - 12*sp[k1,p1] + 12*sp[k1,p1]*m + 
         3*sp[k1,p2] - 3*sp[k1,p2]*m + 3*sp[k2,p1] - 3*sp[k2,p1]*m )

       + amp[3,1,3]*col[1/2*Ca^2*Na]*den[sp[k1 - p1]] * (  - 2 + 5/2*m
          - 1/2*m^2 - 4*sp[k1,k2] + 5*sp[k1,k2]*m - sp[k1,k2]*m^2 - 6*
         sp[k1,p1] + 6*sp[k1,p1]*m - sp[k1,p2] + 2*sp[k1,p2]*m - sp[k1,
         p2]*m^2 - sp[k2,p1] + 2*sp[k2,p1]*m - sp[k2,p1]*m^2 )

       + amp[3,2]*col[1/2*Ca^2*Na]*den[sp[ - k1 - k2]]*den[sp[k1 - p1]]
       * ( 5/2*sp[k1,k2] - 2*sp[k1,k2]*m + 11*sp[k1,k2]^2 - 7*sp[k1,k2]
         ^2*m - 2*sp[k1,k2]*sp[k1,p1] - 8*sp[k1,k2]*sp[k1,p1]*m + 2*sp[
         k1,k2]*sp[k1,p2] + sp[k1,k2]*sp[k1,p2]*m + 14*sp[k1,k2]*sp[k2,
         p1] - 6*sp[k1,k2]*sp[k2,p1]*m + 3*sp[k1,k2]*sp[k2,p2] - 2*sp[
         k1,k2]*sp[k2,p2]*m + 3/2*sp[k1,p1] - sp[k1,p1]*m + 11*sp[k1,p1
         ]^2 - 7*sp[k1,p1]^2*m - 2*sp[k1,p1]*sp[k1,p2] - sp[k1,p1]*sp[
         k1,p2]*m - 14*sp[k1,p1]*sp[k2,p1] + 6*sp[k1,p1]*sp[k2,p1]*m + 
         5*sp[k1,p1]*sp[k2,p2] - 4*sp[k1,p1]*sp[k2,p2]*m + 5*sp[k1,p2]
          - 5/2*sp[k1,p2]*m - 14*sp[k1,p2]^2 + 7*sp[k1,p2]^2*m - 6*sp[
         k1,p2]*sp[k2,p1] + 4*sp[k1,p2]*sp[k2,p1]*m - 10*sp[k1,p2]*sp[
         k2,p2] + 5*sp[k1,p2]*sp[k2,p2]*m + 3*sp[k2,p1] - 2*sp[k2,p1]*m
          - 18*sp[k2,p1]^2 + 10*sp[k2,p1]^2*m - 6*sp[k2,p1]*sp[k2,p2]
          + 4*sp[k2,p1]*sp[k2,p2]*m + 10*sp[k2,p2] - 5*sp[k2,p2]*m )

       + amp[3,3]*col[Ca^2*Na]*den[sp[ - k1 + p1]]*den[sp[k1 - p1]]
       * ( 3 - 2*m + 1/4*m^2 - 3*sp[k1,k2] + 2*sp[k1,k2]*m + sp[k1,k2]*
         m^2 + 12*sp[k1,k2]^2 - 8*sp[k1,k2]^2*m + sp[k1,k2]^2*m^2 - 10*
         sp[k1,k2]*sp[k1,p1] + 12*sp[k1,k2]*sp[k1,p1]*m + 12*sp[k1,k2]*
         sp[k1,p2] - 14*sp[k1,k2]*sp[k1,p2]*m + 2*sp[k1,k2]*sp[k1,p2]*
         m^2 - 12*sp[k1,k2]*sp[k2,p1] + 2*sp[k1,k2]*sp[k2,p1]*m + 2*sp[
         k1,k2]*sp[k2,p1]*m^2 - 5*sp[k1,p1] + 6*sp[k1,p1]*m - 20*sp[k1,
         p1]^2 + 24*sp[k1,p1]^2*m + 10*sp[k1,p1]*sp[k1,p2] - 12*sp[k1,
         p1]*sp[k1,p2]*m + 10*sp[k1,p1]*sp[k2,p1] - 12*sp[k1,p1]*sp[k2,
         p1]*m + 16*sp[k1,p1]*sp[k2,p2] - 16*sp[k1,p1]*sp[k2,p2]*m - 6*
         sp[k1,p2] + sp[k1,p2]*m + sp[k1,p2]*m^2 + 12*sp[k1,p2]^2 - 8*
         sp[k1,p2]^2*m + sp[k1,p2]^2*m^2 - 6*sp[k1,p2]*sp[k2,p1] + 4*
         sp[k1,p2]*sp[k2,p1]*m + 2*sp[k1,p2]*sp[k2,p1]*m^2 + 6*sp[k2,p1
         ] - 7*sp[k2,p1]*m + sp[k2,p1]*m^2 + 12*sp[k2,p1]^2 - 8*sp[k2,
         p1]^2*m + sp[k2,p1]^2*m^2 )

       + amp[3,4]*col[1/2*Ca^2*Na]*den[sp[ - k1 + p2]]*den[sp[k1 - p1]]
       * (  - 9/2 + 5/2*m - 3*sp[k1,k2] + 2*sp[k1,k2]*m - 14*sp[k1,k2]^
         2 + 7*sp[k1,k2]^2*m + 2*sp[k1,k2]*sp[k1,p1] + sp[k1,k2]*sp[k1,
         p1]*m + 2*sp[k1,k2]*sp[k1,p2] + sp[k1,k2]*sp[k1,p2]*m + 10*sp[
         k1,k2]*sp[k2,p1] - 5*sp[k1,k2]*sp[k2,p1]*m + 10*sp[k1,k2]*sp[
         k2,p2] - 5*sp[k1,k2]*sp[k2,p2]*m + 7*sp[k1,p1] - 3*sp[k1,p1]*m
          + 11*sp[k1,p1]^2 - 7*sp[k1,p1]^2*m + 2*sp[k1,p1]*sp[k1,p2] + 
         8*sp[k1,p1]*sp[k1,p2]*m - 3*sp[k1,p1]*sp[k2,p1] + 2*sp[k1,p1]*
         sp[k2,p1]*m + 5*sp[k1,p1]*sp[k2,p2] - 4*sp[k1,p1]*sp[k2,p2]*m
          + 7*sp[k1,p2] - 3*sp[k1,p2]*m + 11*sp[k1,p2]^2 - 7*sp[k1,p2]^
         2*m + 5*sp[k1,p2]*sp[k2,p1] - 4*sp[k1,p2]*sp[k2,p1]*m - 3*sp[
         k1,p2]*sp[k2,p2] + 2*sp[k1,p2]*sp[k2,p2]*m + 3*sp[k2,p1] - 2*
         sp[k2,p1]*m - 20*sp[k2,p1]*sp[k2,p2] + 10*sp[k2,p1]*sp[k2,p2]*
         m + 3*sp[k2,p2] - 2*sp[k2,p2]*m )

       + amp[4,1,1]*col[ - 1/2*Ca^2*Na]*den[sp[k2 - p1]] * (  - 1/2 + m
          - 1/2*m^2 - sp[k1,k2] + 2*sp[k1,k2]*m - sp[k1,k2]*m^2 - 4*sp[
         k1,p1] + 5*sp[k1,p1]*m - sp[k1,p1]*m^2 + 6*sp[k2,p1] - 6*sp[k2
         ,p1]*m - 4*sp[k2,p2] + 5*sp[k2,p2]*m - sp[k2,p2]*m^2 )

       + amp[4,1,2]*col[1/2*Ca^2*Na]*den[sp[k2 - p1]] * (  - 2 + 5/2*m
          - 1/2*m^2 - 4*sp[k1,k2] + 5*sp[k1,k2]*m - sp[k1,k2]*m^2 - sp[
         k1,p1] + 2*sp[k1,p1]*m - sp[k1,p1]*m^2 - 6*sp[k2,p1] + 6*sp[k2
         ,p1]*m - sp[k2,p2] + 2*sp[k2,p2]*m - sp[k2,p2]*m^2 )

       + amp[4,1,3]*col[Ca^2*Na]*den[sp[k2 - p1]] * (  - 3/2 + 3/2*m - 
         3*sp[k1,k2] + 3*sp[k1,k2]*m + 3*sp[k1,p1] - 3*sp[k1,p1]*m - 12
         *sp[k2,p1] + 12*sp[k2,p1]*m + 3*sp[k2,p2] - 3*sp[k2,p2]*m )

       + amp[4,2]*col[ - 1/2*Ca^2*Na]*den[sp[ - k1 - k2]]*den[sp[k2 - 
      p1]] * (  - 5/2*sp[k1,k2] + 2*sp[k1,k2]*m - 11*sp[k1,k2]^2 + 7*
         sp[k1,k2]^2*m - 14*sp[k1,k2]*sp[k1,p1] + 6*sp[k1,k2]*sp[k1,p1]
         *m - 3*sp[k1,k2]*sp[k1,p2] + 2*sp[k1,k2]*sp[k1,p2]*m + 2*sp[k1
         ,k2]*sp[k2,p1] + 8*sp[k1,k2]*sp[k2,p1]*m - 2*sp[k1,k2]*sp[k2,
         p2] - sp[k1,k2]*sp[k2,p2]*m - 3*sp[k1,p1] + 2*sp[k1,p1]*m + 18
         *sp[k1,p1]^2 - 10*sp[k1,p1]^2*m + 6*sp[k1,p1]*sp[k1,p2] - 4*
         sp[k1,p1]*sp[k1,p2]*m + 14*sp[k1,p1]*sp[k2,p1] - 6*sp[k1,p1]*
         sp[k2,p1]*m + 6*sp[k1,p1]*sp[k2,p2] - 4*sp[k1,p1]*sp[k2,p2]*m
          - 10*sp[k1,p2] + 5*sp[k1,p2]*m - 5*sp[k1,p2]*sp[k2,p1] + 4*
         sp[k1,p2]*sp[k2,p1]*m + 10*sp[k1,p2]*sp[k2,p2] - 5*sp[k1,p2]*
         sp[k2,p2]*m - 3/2*sp[k2,p1] + sp[k2,p1]*m - 11*sp[k2,p1]^2 + 7
         *sp[k2,p1]^2*m + 2*sp[k2,p1]*sp[k2,p2] + sp[k2,p1]*sp[k2,p2]*m
          - 5*sp[k2,p2] + 5/2*sp[k2,p2]*m + 14*sp[k2,p2]^2 - 7*sp[k2,p2
         ]^2*m )

       + amp[4,3]*col[1/2*Ca^2*Na]*den[sp[ - k1 + p1]]*den[sp[k2 - p1]]
       * (  - 7/2 + 7/4*m - 3*sp[k1,k2] + 2*sp[k1,k2]*m - 18*sp[k1,k2]^
         2 + 10*sp[k1,k2]^2*m + 14*sp[k1,k2]*sp[k1,p1] - 6*sp[k1,k2]*
         sp[k1,p1]*m + 6*sp[k1,k2]*sp[k1,p2] - 4*sp[k1,k2]*sp[k1,p2]*m
          + 14*sp[k1,k2]*sp[k2,p1] - 6*sp[k1,k2]*sp[k2,p1]*m + 6*sp[k1,
         k2]*sp[k2,p2] - 4*sp[k1,k2]*sp[k2,p2]*m + sp[k1,p1] + 1/2*sp[
         k1,p1]*m + 11*sp[k1,p1]^2 - 7*sp[k1,p1]^2*m - 3*sp[k1,p1]*sp[
         k1,p2] + 2*sp[k1,p1]*sp[k1,p2]*m + 2*sp[k1,p1]*sp[k2,p1] + 8*
         sp[k1,p1]*sp[k2,p1]*m + 5*sp[k1,p1]*sp[k2,p2] - 4*sp[k1,p1]*
         sp[k2,p2]*m + 5*sp[k1,p2] - 5/2*sp[k1,p2]*m + 5*sp[k1,p2]*sp[
         k2,p1] - 4*sp[k1,p2]*sp[k2,p1]*m - 20*sp[k1,p2]*sp[k2,p2] + 10
         *sp[k1,p2]*sp[k2,p2]*m + sp[k2,p1] + 1/2*sp[k2,p1]*m + 11*sp[
         k2,p1]^2 - 7*sp[k2,p1]^2*m - 3*sp[k2,p1]*sp[k2,p2] + 2*sp[k2,
         p1]*sp[k2,p2]*m + 5*sp[k2,p2] - 5/2*sp[k2,p2]*m )

       + amp[4,4]*col[Ca^2*Na]*den[sp[ - k1 + p2]]*den[sp[k2 - p1]]
       * (  - 9/4 + 3/4*m + 1/4*m^2 - 18*sp[k1,k2] + 9*sp[k1,k2]*m + 
         sp[k1,k2]*m^2 - 9*sp[k1,k2]^2 + 3*sp[k1,k2]^2*m + sp[k1,k2]^2*
         m^2 + 36*sp[k1,k2]*sp[k1,p1] - 24*sp[k1,k2]*sp[k1,p1]*m + 2*
         sp[k1,k2]*sp[k1,p1]*m^2 + 3*sp[k1,k2]*sp[k1,p2] + 3*sp[k1,k2]*
         sp[k2,p1] + 36*sp[k1,k2]*sp[k2,p2] - 24*sp[k1,k2]*sp[k2,p2]*m
          + 2*sp[k1,k2]*sp[k2,p2]*m^2 + 18*sp[k1,p1] - 12*sp[k1,p1]*m
          + sp[k1,p1]*m^2 - 9*sp[k1,p1]^2 + 3*sp[k1,p1]^2*m + sp[k1,p1]
         ^2*m^2 - 3*sp[k1,p1]*sp[k1,p2] - 3*sp[k1,p1]*sp[k2,p1] - 36*
         sp[k1,p1]*sp[k2,p2] + 18*sp[k1,p1]*sp[k2,p2]*m + 2*sp[k1,p1]*
         sp[k2,p2]*m^2 + 3/2*sp[k1,p2] + 36*sp[k1,p2]*sp[k2,p1] - 4*sp[
         k1,p2]*sp[k2,p1]*m - 3*sp[k1,p2]*sp[k2,p2] + 3/2*sp[k2,p1] - 3
         *sp[k2,p1]*sp[k2,p2] + 18*sp[k2,p2] - 12*sp[k2,p2]*m + sp[k2,
         p2]*m^2 - 9*sp[k2,p2]^2 + 3*sp[k2,p2]^2*m + sp[k2,p2]^2*m^2 ))
