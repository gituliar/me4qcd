( + amp[1,1]*color[ - 4/9*Na*Tf]*den[sp[k1 + k3]]*den[sp[k1 - q]] * ( 
          - 32*sp[k1,k2]*sp[k1,k3] + 16*sp[k1,k2]*sp[k1,k3]*m + 32*sp[
         k1,k2]*sp[k1,q] - 16*sp[k1,k2]*sp[k1,q]*m + 64*sp[k1,k2]*sp[k3
         ,q] - 40*sp[k1,k2]*sp[k3,q]*m + 4*sp[k1,k2]*sp[k3,q]*m^2 - 32*
         sp[k1,k3]*sp[k2,q] + 24*sp[k1,k3]*sp[k2,q]*m - 4*sp[k1,k3]*sp[
         k2,q]*m^2 - 32*sp[k1,q]*sp[k2,k3] + 24*sp[k1,q]*sp[k2,k3]*m - 
         4*sp[k1,q]*sp[k2,k3]*m^2 )

       + amp[1,2]*color[ - 4/9*Na*Tf]*den[sp[k1 - q]]^2 * ( 16*sp[k1,k2
         ] - 16*sp[k1,k2]*m + 4*sp[k1,k2]*m^2 - 32*sp[k1,q]*sp[k2,q] + 
         32*sp[k1,q]*sp[k2,q]*m - 8*sp[k1,q]*sp[k2,q]*m^2 )

       + amp[2,1]*color[ - 4/9*Na*Tf]*den[sp[k1 + k3]]*den[sp[ - k2 + q
      ]] * ( 16*sp[k1,k2]*sp[k3,q] - 16*sp[k1,k2]*sp[k3,q]*m + 4*sp[k1,
         k2]*sp[k3,q]*m^2 - 16*sp[k1,k3]*sp[k2,q] + 16*sp[k1,k3]*sp[k2,
         q]*m - 4*sp[k1,k3]*sp[k2,q]*m^2 - 16*sp[k1,q]*sp[k2,k3] + 16*
         sp[k1,q]*sp[k2,k3]*m - 4*sp[k1,q]*sp[k2,k3]*m^2 )

       + amp[2,2]*color[ - 4/9*Na*Tf]*den[sp[k1 - q]]*den[sp[ - k2 + q]
      ] * ( 64*sp[k1,k2] - 40*sp[k1,k2]*m + 4*sp[k1,k2]*m^2 + 32*sp[k1,
         k2]^2 - 16*sp[k1,k2]^2*m - 32*sp[k1,k2]*sp[k1,q] + 16*sp[k1,k2
         ]*sp[k1,q]*m - 32*sp[k1,k2]*sp[k2,q] + 16*sp[k1,k2]*sp[k2,q]*m
          - 64*sp[k1,q]*sp[k2,q] + 48*sp[k1,q]*sp[k2,q]*m - 8*sp[k1,q]*
         sp[k2,q]*m^2 ))
