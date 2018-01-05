*
* file generated by qgraf-3.1.4
* output= 'amp/a2qqggg0.h' ;
* style= 'amp/form.sty' ;
* model= 'amp/qcd.mod' ;
* in= a[q] ;
* out= q[k1], Q[k2], g[k3], g[k4], g[k5] ;
* loops= 0 ;
* loop_momentum= l ;
* options= ;
*
*--#[ d1:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 2,q-k1, 3,-q+k1+k2)
  *VGGGG(-6,-k3, -8,-k4, -10,-k5, 4,q-k1-k2)
*--#] d1:
*--#[ d2:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(1,q-k2, -2,-k1, 3,-q+k1+k2)
  *VGGGG(-6,-k3, -8,-k4, -10,-k5, 4,q-k1-k2)
*--#] d2:
*--#[ d3:
   -1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VGGG(-8,-k4, -10,-k5, 5,k4+k5)
  *VQQG(3,-k2-k3, 2,q-k1, 6,-k4-k5)
*--#] d3:
*--#[ d4:
   -1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VGGG(-6,-k3, -10,-k5, 5,k3+k5)
  *VQQG(3,-k2-k4, 2,q-k1, 6,-k3-k5)
*--#] d4:
*--#[ d5:
   -1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VGGG(-6,-k3, -8,-k4, 5,k3+k4)
  *VQQG(3,-k2-k5, 2,q-k1, 6,-k3-k4)
*--#] d5:
*--#[ d6:
   -1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k3, -2,-k1, -6,-k3)
  *VGGG(-8,-k4, -10,-k5, 5,k4+k5)
  *VQQG(1,q-k2, 4,-k1-k3, 6,-k4-k5)
*--#] d6:
*--#[ d7:
   -1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k4, -2,-k1, -8,-k4)
  *VGGG(-6,-k3, -10,-k5, 5,k3+k5)
  *VQQG(1,q-k2, 4,-k1-k4, 6,-k3-k5)
*--#] d7:
*--#[ d8:
   -1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k5, -2,-k1, -10,-k5)
  *VGGG(-6,-k3, -8,-k4, 5,k3+k4)
  *VQQG(1,q-k2, 4,-k1-k5, 6,-k3-k4)
*--#] d8:
*--#[ d9:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VQQG(5,-q+k1+k4, 2,q-k1, -8,-k4)
  *VQQG(3,-k2-k3, 6,q-k1-k4, -10,-k5)
*--#] d9:
*--#[ d10:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VQQG(5,-q+k1+k5, 2,q-k1, -10,-k5)
  *VQQG(3,-k2-k3, 6,q-k1-k5, -8,-k4)
*--#] d10:
*--#[ d11:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VQQG(5,-q+k1+k3, 2,q-k1, -6,-k3)
  *VQQG(3,-k2-k4, 6,q-k1-k3, -10,-k5)
*--#] d11:
*--#[ d12:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VQQG(5,-q+k1+k5, 2,q-k1, -10,-k5)
  *VQQG(3,-k2-k4, 6,q-k1-k5, -6,-k3)
*--#] d12:
*--#[ d13:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VQQG(5,-q+k1+k3, 2,q-k1, -6,-k3)
  *VQQG(3,-k2-k5, 6,q-k1-k3, -8,-k4)
*--#] d13:
*--#[ d14:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VQQG(5,-q+k1+k4, 2,q-k1, -8,-k4)
  *VQQG(3,-k2-k5, 6,q-k1-k4, -6,-k3)
*--#] d14:
*--#[ d15:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VGGG(-6,-k3, -8,-k4, 3,k3+k4)
  *VQQG(-4,-k2, 2,q-k1, 5,-q+k1+k2)
  *VGGG(-10,-k5, 4,-k3-k4, 6,q-k1-k2)
*--#] d15:
*--#[ d16:
   -1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VGGG(-6,-k3, -8,-k4, 3,k3+k4)
  *VQQG(5,-q+k1+k5, 2,q-k1, -10,-k5)
  *VQQG(-4,-k2, 6,q-k1-k5, 4,-k3-k4)
*--#] d16:
*--#[ d17:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VGGG(-6,-k3, -10,-k5, 3,k3+k5)
  *VQQG(-4,-k2, 2,q-k1, 5,-q+k1+k2)
  *VGGG(-8,-k4, 4,-k3-k5, 6,q-k1-k2)
*--#] d17:
*--#[ d18:
   -1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VGGG(-6,-k3, -10,-k5, 3,k3+k5)
  *VQQG(5,-q+k1+k4, 2,q-k1, -8,-k4)
  *VQQG(-4,-k2, 6,q-k1-k4, 4,-k3-k5)
*--#] d18:
*--#[ d19:
   1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VGGG(-8,-k4, -10,-k5, 3,k4+k5)
  *VQQG(-4,-k2, 2,q-k1, 5,-q+k1+k2)
  *VGGG(-6,-k3, 4,-k4-k5, 6,q-k1-k2)
*--#] d19:
*--#[ d20:
   -1
  *VQQA(1,-q+k1, -2,-k1, -1,q)
  *VGGG(-8,-k4, -10,-k5, 3,k4+k5)
  *VQQG(5,-q+k1+k3, 2,q-k1, -6,-k3)
  *VQQG(-4,-k2, 6,q-k1-k3, 4,-k4-k5)
*--#] d20:
*--#[ d21:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k3, -2,-k1, -6,-k3)
  *VQQG(1,q-k2, 6,-q+k2+k4, -8,-k4)
  *VQQG(5,q-k2-k4, 4,-k1-k3, -10,-k5)
*--#] d21:
*--#[ d22:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k3, -2,-k1, -6,-k3)
  *VQQG(1,q-k2, 6,-q+k2+k5, -10,-k5)
  *VQQG(5,q-k2-k5, 4,-k1-k3, -8,-k4)
*--#] d22:
*--#[ d23:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k4, -2,-k1, -8,-k4)
  *VQQG(1,q-k2, 6,-q+k2+k3, -6,-k3)
  *VQQG(5,q-k2-k3, 4,-k1-k4, -10,-k5)
*--#] d23:
*--#[ d24:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k4, -2,-k1, -8,-k4)
  *VQQG(1,q-k2, 6,-q+k2+k5, -10,-k5)
  *VQQG(5,q-k2-k5, 4,-k1-k4, -6,-k3)
*--#] d24:
*--#[ d25:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k5, -2,-k1, -10,-k5)
  *VQQG(1,q-k2, 6,-q+k2+k3, -6,-k3)
  *VQQG(5,q-k2-k3, 4,-k1-k5, -8,-k4)
*--#] d25:
*--#[ d26:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VQQG(3,k1+k5, -2,-k1, -10,-k5)
  *VQQG(1,q-k2, 6,-q+k2+k4, -8,-k4)
  *VQQG(5,q-k2-k4, 4,-k1-k5, -6,-k3)
*--#] d26:
*--#[ d27:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VGGG(-6,-k3, -8,-k4, 3,k3+k4)
  *VQQG(1,q-k2, -2,-k1, 5,-q+k1+k2)
  *VGGG(-10,-k5, 4,-k3-k4, 6,q-k1-k2)
*--#] d27:
*--#[ d28:
   -1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VGGG(-6,-k3, -8,-k4, 3,k3+k4)
  *VQQG(1,q-k2, 6,-q+k2+k5, -10,-k5)
  *VQQG(5,q-k2-k5, -2,-k1, 4,-k3-k4)
*--#] d28:
*--#[ d29:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VGGG(-6,-k3, -10,-k5, 3,k3+k5)
  *VQQG(1,q-k2, -2,-k1, 5,-q+k1+k2)
  *VGGG(-8,-k4, 4,-k3-k5, 6,q-k1-k2)
*--#] d29:
*--#[ d30:
   -1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VGGG(-6,-k3, -10,-k5, 3,k3+k5)
  *VQQG(1,q-k2, 6,-q+k2+k4, -8,-k4)
  *VQQG(5,q-k2-k4, -2,-k1, 4,-k3-k5)
*--#] d30:
*--#[ d31:
   1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VGGG(-8,-k4, -10,-k5, 3,k4+k5)
  *VQQG(1,q-k2, -2,-k1, 5,-q+k1+k2)
  *VGGG(-6,-k3, 4,-k4-k5, 6,q-k1-k2)
*--#] d31:
*--#[ d32:
   -1
  *VQQA(-4,-k2, 2,-q+k2, -1,q)
  *VGGG(-8,-k4, -10,-k5, 3,k4+k5)
  *VQQG(1,q-k2, 6,-q+k2+k3, -6,-k3)
  *VQQG(5,q-k2-k3, -2,-k1, 4,-k4-k5)
*--#] d32:
*--#[ d33:
   1
  *VQQG(1,k1+k3, -2,-k1, -6,-k3)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VQQA(5,-q+k1+k3, 2,-k1-k3, -1,q)
  *VQQG(3,-k2-k4, 6,q-k1-k3, -10,-k5)
*--#] d33:
*--#[ d34:
   1
  *VQQG(1,k1+k3, -2,-k1, -6,-k3)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VQQG(5,k1+k3+k5, 2,-k1-k3, -10,-k5)
  *VQQA(3,-k2-k4, 6,-k1-k3-k5, -1,q)
*--#] d34:
*--#[ d35:
   1
  *VQQG(1,k1+k3, -2,-k1, -6,-k3)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VQQA(5,-q+k1+k3, 2,-k1-k3, -1,q)
  *VQQG(3,-k2-k5, 6,q-k1-k3, -8,-k4)
*--#] d35:
*--#[ d36:
   1
  *VQQG(1,k1+k3, -2,-k1, -6,-k3)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VQQG(5,k1+k3+k4, 2,-k1-k3, -8,-k4)
  *VQQA(3,-k2-k5, 6,-k1-k3-k4, -1,q)
*--#] d36:
*--#[ d37:
   -1
  *VQQG(1,k1+k3, -2,-k1, -6,-k3)
  *VGGG(-8,-k4, -10,-k5, 3,k4+k5)
  *VQQA(5,-q+k1+k3, 2,-k1-k3, -1,q)
  *VQQG(-4,-k2, 6,q-k1-k3, 4,-k4-k5)
*--#] d37:
*--#[ d38:
   1
  *VQQG(1,k1+k4, -2,-k1, -8,-k4)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VQQA(5,-q+k1+k4, 2,-k1-k4, -1,q)
  *VQQG(3,-k2-k3, 6,q-k1-k4, -10,-k5)
*--#] d38:
*--#[ d39:
   1
  *VQQG(1,k1+k4, -2,-k1, -8,-k4)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VQQG(5,k1+k4+k5, 2,-k1-k4, -10,-k5)
  *VQQA(3,-k2-k3, 6,-k1-k4-k5, -1,q)
*--#] d39:
*--#[ d40:
   1
  *VQQG(1,k1+k4, -2,-k1, -8,-k4)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VQQA(5,-q+k1+k4, 2,-k1-k4, -1,q)
  *VQQG(3,-k2-k5, 6,q-k1-k4, -6,-k3)
*--#] d40:
*--#[ d41:
   1
  *VQQG(1,k1+k4, -2,-k1, -8,-k4)
  *VQQG(-4,-k2, 4,k2+k5, -10,-k5)
  *VQQG(5,k1+k3+k4, 2,-k1-k4, -6,-k3)
  *VQQA(3,-k2-k5, 6,-k1-k3-k4, -1,q)
*--#] d41:
*--#[ d42:
   -1
  *VQQG(1,k1+k4, -2,-k1, -8,-k4)
  *VGGG(-6,-k3, -10,-k5, 3,k3+k5)
  *VQQA(5,-q+k1+k4, 2,-k1-k4, -1,q)
  *VQQG(-4,-k2, 6,q-k1-k4, 4,-k3-k5)
*--#] d42:
*--#[ d43:
   1
  *VQQG(1,k1+k5, -2,-k1, -10,-k5)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VQQA(5,-q+k1+k5, 2,-k1-k5, -1,q)
  *VQQG(3,-k2-k3, 6,q-k1-k5, -8,-k4)
*--#] d43:
*--#[ d44:
   1
  *VQQG(1,k1+k5, -2,-k1, -10,-k5)
  *VQQG(-4,-k2, 4,k2+k3, -6,-k3)
  *VQQG(5,k1+k4+k5, 2,-k1-k5, -8,-k4)
  *VQQA(3,-k2-k3, 6,-k1-k4-k5, -1,q)
*--#] d44:
*--#[ d45:
   1
  *VQQG(1,k1+k5, -2,-k1, -10,-k5)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VQQA(5,-q+k1+k5, 2,-k1-k5, -1,q)
  *VQQG(3,-k2-k4, 6,q-k1-k5, -6,-k3)
*--#] d45:
*--#[ d46:
   1
  *VQQG(1,k1+k5, -2,-k1, -10,-k5)
  *VQQG(-4,-k2, 4,k2+k4, -8,-k4)
  *VQQG(5,k1+k3+k5, 2,-k1-k5, -6,-k3)
  *VQQA(3,-k2-k4, 6,-k1-k3-k5, -1,q)
*--#] d46:
*--#[ d47:
   -1
  *VQQG(1,k1+k5, -2,-k1, -10,-k5)
  *VGGG(-6,-k3, -8,-k4, 3,k3+k4)
  *VQQA(5,-q+k1+k5, 2,-k1-k5, -1,q)
  *VQQG(-4,-k2, 6,q-k1-k5, 4,-k3-k4)
*--#] d47:
*--#[ d48:
   -1
  *VQQG(-4,-k2, 2,k2+k3, -6,-k3)
  *VGGG(-8,-k4, -10,-k5, 3,k4+k5)
  *VQQA(1,-k2-k3, 6,-q+k2+k3, -1,q)
  *VQQG(5,q-k2-k3, -2,-k1, 4,-k4-k5)
*--#] d48:
*--#[ d49:
   -1
  *VQQG(-4,-k2, 2,k2+k4, -8,-k4)
  *VGGG(-6,-k3, -10,-k5, 3,k3+k5)
  *VQQA(1,-k2-k4, 6,-q+k2+k4, -1,q)
  *VQQG(5,q-k2-k4, -2,-k1, 4,-k3-k5)
*--#] d49:
*--#[ d50:
   -1
  *VQQG(-4,-k2, 2,k2+k5, -10,-k5)
  *VGGG(-6,-k3, -8,-k4, 3,k3+k4)
  *VQQA(1,-k2-k5, 6,-q+k2+k5, -1,q)
  *VQQG(5,q-k2-k5, -2,-k1, 4,-k3-k4)
*--#] d50:
*--#[ Declarations:
#$n = 50;
*--#] Declarations:
*
* end
*
