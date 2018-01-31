*--#[ Declarations :
#include color.h

CF den, den2, num, GM, sp,w;

* SUn.prc from color.h package
CF color,Wden;
S NF,NA;
S m,ep;

#define N "10";
#do i=1,`N'
I cii`i'=NF;
I cie`i'=NF;
I cji`i'=NA;
I cje`i'=NA;
I mu`i'=m;
#enddo
Set cii:cii1,...,cii`N';
Set cie:cie1,...,cie`N';
Set cji:cji1,...,cji`N';
Set cje:cje1,...,cje`N';
Set mu:mu1,...,mu`N';

CF e,i, a,b,c, te,ti;

S  Ca,Cf,Na,Tf,nf;

* QGRAF variables
S  n,eps;
CF amp,ampx;
CF VGGG,VGGGG,VQQG,VQQA;
CF VGGGx,VGGGGx,VQQGx,VQQAx;

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
S n1,...,n3;
*--#] Declarations :

*--#[ ImportAmplitude :
#include `filename' # Declarations
L AMPLITUDE =
#do i = 1,$n
  + amp(`i')*(
  #include `filename' # d`i'
  )
#enddo
;
#do V={VQQA, VQQG, VGGG} 
id `V'(n1?pos_,k1?, n2?,k2?, n3?,k3?) = `V'(i(n1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?pos_,k2?, n3?,k3?) = `V'(n1,k1, i(n2),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?pos_,k3?) = `V'(n1,k1, n2,k2, i(n3),k3);
id `V'(n1?neg_,k1?, n2?,k2?, n3?,k3?) = `V'(e(-n1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?neg_,k2?, n3?,k3?) = `V'(n1,k1, e(-n2),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?neg_,k3?) = `V'(n1,k1, n2,k2, e(-n3),k3);
#enddo
* In QGRAF rays with two consequtive indices are connected by a propagator,
* (1,2), (3,4), etc. Let us make this connection explicit, so that all
* internal indices are odd. We assume
*   * n1 is always odd
*   * n2 is always even
*   * n3 is odd or even
*   * n1,n2,n3 are positive for internal lines
#do V={VQQA, VQQG, VGGG} 
id `V'(n1?,k1?, i(n2?even_),k2?, n3?,k3?) = `V'(n1,k1, i(n2-1),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, i(n3?even_),k3?) = `V'(n1,k1, n2,k2, i(n3-1),k3);
#enddo
* In QGRAF all momenta go into the vertex. Let us change fermions'momentum
* to flow along the particle-number flow.
#do V={VQQA, VQQG} 
id `V'(n1?,k1?, i(n2?),k2?, n3?,k3?) = `V'(n1,k1, i(n2),-k2, n3,k3);
#enddo
* Invert momentum for final-state particles so that it is outgoing now.
#do V={VQQA,VQQG,VGGG} 
id `V'(e(n1?even_),k1?, n2?,k2?, n3?,k3?) = `V'(e(n1),-k1, n2,k2, n3,k3);
id `V'(n1?,k1?, e(n2?even_),k2?, n3?,k3?) = `V'(n1,k1, e(n2),-k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, e(n3?even_),k3?) = `V'(n1,k1, n2,k2, e(n3),-k3);
#enddo
.sort
Drop AMPLITUDE;
*--#] ImportAmplitude :

*--#[ ConjugateAmplitude:
id amp(ex?) = ampx(ex);

* Invert momentum flow for fermions.
#do V={VQQA, VQQG} 
id `V'(n1?,k1?, n2?,k2?, n3?,k3?) = `V'(n2,k2, n1,k1, n3,k3);
#enddo
* Change indexes of internal lines to be all even
#do V={VQQA,VQQG,VGGG} 
id `V'(i(n1?),k1?, n2?,k2?, n3?,k3?) = `V'(i(n1+1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, i(n2?),k2?, n3?,k3?) = `V'(n1,k1, i(n2+1),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, i(n3?),k3?) = `V'(n1,k1, n2,k2, i(n3+1),k3);
#enddo
#do V={VQQA,VQQG,VGGG} 
#enddo
.sort
*--#] ConjugateAmplitude:

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
#enddo
#enddo
#enddo

repeat;
  id color(ex1?)*color(ex2?) = color(ex1*ex2);
endrepeat;

id color(ex?) = ex;
*id color(ex?) = 1;
.sort
  
#call docolor;
id cA = Ca;
id cR = Cf;
id I2R = Tf;
id NA = Na;
*id Tf = Tf*nf;
*Bracket amp,VGGG,VGGGG,VQQG,VQQA;
*.sort
*Collect color;
.sort
*
*--#] ColorTrace:


*--#[ ExpandFeynmanRules:
*
*  Taken from Peskin & Schroeder, pp. 801-802.
*
#do V={VQQG,VQQA}
* Fermion propagators
id `V'(i(n1?),k1?, a?(n2?),k2?, b?(n3?),k3?) =
   num((-1)^(n1-1)*i_*GM(a(n2),mu[n3],k1,i(n1))) *
   den(sp(k1)) *
   `V'(i(n1),k1, a(n2),k2, b(n3),k3);
* Fermion polarization sum
id `V'(e(n1?),k1?, a?(n2?),k2?, b?(n3?),k3?) =
   num(GM(a(n2),mu[n3],k1,e(n1))) *
   `V'(e(n1),k1, a(n2),k2, b(n3),k3);
* Boson polarization sum
id `V'(a?(n1?),k1?, b?(n2?),k2?, e(n3?),k3?) =
   num(i_) *
   `V'(a(n1),k1, b(n2),k2, e(n3),k3);
#enddo
id VGGG(e(n1?),k1?, b?(n2?),k2?, c?(n3?),k3?) =
   num(i_) *
   VGGG(e(n1),k1, b(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?, e(n2?),k2?, c?(n3?),k3?) =
   num(i_) *
   VGGG(a(n1),k1, e(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?, b?(n2?),k2?, e(n3?),k3?) =
   num(i_) *
   VGGG(a(n1),k1, b(n2),k2, e(n3),k3);
* gluon vertex with all momenta coming inside
#do a={e,i} 
#do b={e,i} 
#do c={e,i} 
id VGGG(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
   num(i_*(
     d_(mu[n1],mu[n2])*(t`b'(n2)*k2(mu[n3])-t`a'(n1)*k1(mu[n3])) +
     d_(mu[n2],mu[n3])*(t`c'(n3)*k3(mu[n1])-t`b'(n2)*k2(mu[n1])) +
     d_(mu[n3],mu[n1])*(t`a'(n1)*k1(mu[n2])-t`c'(n3)*k3(mu[n2])))) *
   VGGG(`a'(n1),k1, `b'(n2),k2, `c'(n3),k3);
#enddo
#enddo
#enddo
argument num;
id ti(n1?) = +1;
id te(n1?odd_) = +1;
id te(n1?even_) = -1;
endargument;

* Boson Propagators
id VGGG( i(n1?),k1?, b?(n2?),k2?, c?(n3?),k3?) = den2(k1,n1) * VGGG(i(n1),k1, b(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?,  i(n2?),k2?, c?(n3?),k3?) = den2(k2,n2) * VGGG(a(n1),k1, i(n2),k2, c(n3),k3);
id VGGG(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?) = den2(k3,n3) * VGGG(a(n1),k1, b(n2),k2, i(n3),k3);
id VQQG(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?) = den2(k3,n3) * VQQG(a(n1),k1, b(n2),k2, i(n3),k3);
id VQQA(a?(n1?),k1?, b?(n2?),k2?,  i(n3?),k3?) = den2(k3,n3) * VQQA(a(n1),k1, b(n2),k2, i(n3),k3);
id den2(k1?,n1?)*den2(k2?,n1?) = den(sp(k1));
#do a={2,4,6,8}
id den2(k1?,n1?)^`a' = den(sp(k1))^(`a'/2);
#enddo

* collect num's
repeat;
*  id num(ex1?)*num(ex2?) = num(ex1*ex2);
  id num(ex1?)*num(ex2?) = ex1*ex2;
endrepeat;
.sort

*argument num;
  repeat;
    id GM(?arg1,i(n1?)) * GM(i(n1?),?arg2) = GM(?arg1, ?arg2);
    id GM(?arg1,e(n1?)) * GM(e(n1?),?arg2) = GM(?arg1, ?arg2);
  endrepeat;
  id GM(ex?,?arg,ex?) = GM(?arg);
*endargument;
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
*id num(0) = 0;
.sort
*--#] Clean:
