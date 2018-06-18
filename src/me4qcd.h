*--#[ Declarations :
#include color.h

CF den, den2, num, GM, sp,w;

* SUn.prc from color.h package
CF color,Wden;
S NF,NA;
S m,ep;

#define N "10";
#do i=1,`N'
I cj`i'=NA;
I cii`i'=NF;
I cie`i'=NF;
I cji`i'=NA;
I cje`i'=NA;
I mu`i'=m;
I mui`i'=m;
I mue`i'=m;
#enddo
Set cii:cii1,...,cii`N';
Set cie:cie1,...,cie`N';
Set cji:cji1,...,cji`N';
Set cje:cje1,...,cje`N';
Set mu:mu1,...,mu`N';
Set mui:mui1,...,mui`N';
Set mue:mue1,...,mue`N';

CF e,i, a,b,c,d, te,ti;

S  Ca,Cf,Na,Tf,nf;

* QGRAF variables
S  n,eps;
CF amp,ampx;
CF VGGG,VGGGG,VGGGGi,VQQG,VQQA;

Dimension m;
#do i=0,99
I v`i'=m;
I s`i';
#enddo

V k,k1,...,k9;
set ks: k1,...,k9;
V l1,...,l9;
V r1,...,r9;
V p,p1,...,p9;
V q;

S ex,ex1,ex2;
S n1,...,n4;
*--#] Declarations :

*--#[ ColorTrace:
#do a={e,i} 
#do b={e,i} 
#do c={e,i} 
  id VQQA(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
     color(d_(ci`a'[n1],ci`b'[n2]))*VQQA(`a'(n1),k1, `b'(n2),k2, `c'(n3),k3);
  id VQQG(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
     color(T(ci`a'[n1],ci`b'[n2],cj`c'[n3]))*VQQG(`a'(n1),k1, `b'(n2),k2, `c'(n3),k3);
  id VGGG(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
     color(-i_*f(cj`a'[n1],cj`b'[n2],cj`c'[n3]))*VGGG(`a'(n1),k1, `b'(n2),k2, `c'(n3),k3);
  #do d={e,i} 
  #do i=1,`N'
  id once VGGGG(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?, `d'(n4?),k4?) = (
     color(f(cj`a'[n1],cj`b'[n2],cj`i')*f(cj`c'[n3],cj`d'[n4],cj`i')) *
       num(d_(mu`a'[n1],mu`c'[n3])*d_(mu`b'[n2],mu`d'[n4]) - d_(mu`a'[n1],mu`d'[n4])*d_(mu`b'[n2],mu`c'[n3])) +
     color(f(cj`a'[n1],cj`c'[n3],cj`i')*f(cj`b'[n2],cj`d'[n4],cj`i')) * 
       num(d_(mu`a'[n1],mu`b'[n2])*d_(mu`c'[n3],mu`d'[n4]) - d_(mu`a'[n1],mu`d'[n4])*d_(mu`b'[n2],mu`c'[n3])) +
     color(f(cj`a'[n1],cj`d'[n4],cj`i')*f(cj`b'[n2],cj`c'[n3],cj`i')) *
       num(d_(mu`a'[n1],mu`b'[n2])*d_(mu`c'[n3],mu`d'[n4]) - d_(mu`a'[n1],mu`c'[n3])*d_(mu`b'[n2],mu`d'[n4]))
  )*VGGGGi(`a'(n1),k1, `b'(n2),k2, `c'(n3),k3, `d'(n4),k4);
  #enddo
  #enddo
#enddo
#enddo
#enddo

repeat;
  id color(ex1?)*color(ex2?) = color(ex1*ex2);
endrepeat;

id color(ex?) = ex;
.sort
  
#call docolor;
id cA = Ca;
id cR = Cf;
id I2R = Tf;
id NA = Na;
id 1/NA = 1/Na;
*id Tf = Tf*nf;
*Bracket amp,VGGG,VGGGG,VQQG,VQQA;
*.sort
*Collect color;
.sort
*
*--#] ColorTrace:


*--#[ ExpandFeynmanRules:
*
*  See Peskin & Schroeder, pp. 801-802.
*
#do V={VQQG,VQQA}
#do a={e,i} 
#do b={e,i} 
* Fermion propagators
id `V'(i(n1?),k1?, `a'(n2?),k2?, `b'(n3?),k3?) =
   num((-1)^(n1-1)*i_*GM(`a'(n2),mu`b'[n3],k1,i(n1))) *
   den(sp(k1)) *
   `V'(i(n1),k1, `a'(n2),k2, `b'(n3),k3);
* Fermion polarization sum
id `V'(e(n1?),k1?, `a'(n2?),k2?, `b'(n3?),k3?) =
   num(GM(`a'(n2),mu`b'[n3],k1,e(n1))) *
   `V'(e(n1),k1, `a'(n2),k2, `b'(n3),k3);
* Boson polarization sum
id `V'(`a'(n1?),k1?, `b'(n2?),k2?, e(n3?),k3?) =
   num(i_) *
   `V'(`a'(n1),k1, `b'(n2),k2, e(n3),k3);
#enddo
#enddo
#enddo
* More boson polarization sum
id VGGG(e(n1?),k1?, b?(n2?),k2?, c?(n3?),k3?) =
   num(i_) *
   VGGG(e(n1),k1, b(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?, e(n2?),k2?, c?(n3?),k3?) =
   num(i_) *
   VGGG(a(n1),k1, e(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?, b?(n2?),k2?, e(n3?),k3?) =
   num(i_) *
   VGGG(a(n1),k1, b(n2),k2, e(n3),k3);

* Bosonic Numerators
* gluon vertex with all momenta coming inside
#do a={e,i} 
#do b={e,i} 
#do c={e,i} 
id VGGG(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
   num(i_*(
     d_(mu`a'[n1],mu`b'[n2])*(t`b'(n2)*k2(mu`c'[n3])-t`a'(n1)*k1(mu`c'[n3])) +
     d_(mu`b'[n2],mu`c'[n3])*(t`c'(n3)*k3(mu`a'[n1])-t`b'(n2)*k2(mu`a'[n1])) +
     d_(mu`c'[n3],mu`a'[n1])*(t`a'(n1)*k1(mu`b'[n2])-t`c'(n3)*k3(mu`b'[n2])))) *
   VGGG(`a'(n1),k1, `b'(n2),k2, `c'(n3),k3);
#enddo
#enddo
#enddo
argument num;
  id ti(n1?) = +1;
  id te(n1?odd_) = +1;
  id te(n1?even_) = -1;
endargument;
id num(ex1?) = ex1;
.sort

id p1.p1 = 0;
id p2.p2 = 0;
id k1.k1 = 0;
id k2.k2 = 0;
id k3.k3 = 0;
id k4.k4 = 0;
id k5.k5 = 0;
id k6.k6 = 0;

* Bosonic Propagators
id VGGG( i(n1?),k1?, b?(n2?),k2?, c?(n3?),k3?) = den2(k1,n1) * VGGG(i(n1),k1, b(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?,  i(n2?),k2?, c?(n3?),k3?) = den2(k2,n2) * VGGG(a(n1),k1, i(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?) = den2(k3,n3) * VGGG(a(n1),k1, b(n2),k2, i(n3),k3);
id VGGGGi( i(n1?),k1?, b?(n2?),k2?, c?(n3?),k3?, d?(n4?),k4?) = den2(k1,n1) * VGGGGi(i(n1),k1, b(n2),k2, c(n3),k3, d(n4),k4);
id VGGGGi(a?(n1?),k1?,  i(n2?),k2?, c?(n3?),k3?, d?(n4?),k4?) = den2(k2,n2) * VGGGGi(a(n1),k1, i(n2),k2, c(n3),k3, d(n4),k4);
id VGGGGi(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?, d?(n4?),k4?) = den2(k3,n3) * VGGGGi(a(n1),k1, b(n2),k2, i(n3),k3, d(n4),k4);
id VGGGGi(a?(n1?),k1?, b?(n2?),k2?, c?(n3?),k3?,  i(n4?),k4?) = den2(k4,n4) * VGGGGi(a(n1),k1, b(n2),k2, c(n3),k3, i(n4),k4);
id VQQG(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?) = den2(k3,n3) * VQQG(a(n1),k1, b(n2),k2, i(n3),k3);
id VQQA(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?) = den2(k3,n3) * VQQA(a(n1),k1, b(n2),k2, i(n3),k3);
id den2(k1?,n1?)*den2(k2?,n1?) = den(sp(k1));
#do a={2,4,6,8}
id den2(k1?,n1?)^`a' = den(sp(k1))^(`a'/2);
#enddo
.sort

repeat;
  id GM(?arg1,i(n1?)) * GM(i(n1?),?arg2) = GM(?arg1, ?arg2);
  id GM(?arg1,e(n1?)) * GM(e(n1?),?arg2) = GM(?arg1, ?arg2);
endrepeat;
id GM(ex?,?arg,ex?) = GM(?arg);
.sort
*
*--#] ExpandFeynmanRules:

*--#[ GammaTrace:
repeat;
*argument num;
id once GM(?arg) = w(1,?arg);

repeat;
  id w(1,p1?,?arg) = g_(1,p1)*w(1,?arg);
  id w(1,mu1?,?arg) = g_(1,mu1)*w(1,?arg);
endrepeat;
id w(1) = 1;
tracen 1;
*endargument;
endrepeat;
.sort
*
*--#] GammaTrace:

*--#[ Clean:
id VQQA(?arg) = 1;
id VQQG(?arg) = 1;
id VGGG(?arg) = 1;
id VGGGGi(?arg) = 1;
.sort
*--#] Clean:
