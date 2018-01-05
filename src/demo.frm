Symbol n,ep;
Dimension n;
I mu=n, nu=n, ro=n;
V e0,e1,e2,e3,e4,k1,k2,k3,q,[q-k1],[q-k2],[k2+k3];

L A = G_(1, k1, mu, [q-k1], nu, [k2+k3], ro, k2, ro, [k2+k3], nu, [q-k1], mu);
L B = G_(1, k1, mu, [q-k1], nu, [k2+k3], ro, k2, mu, [q-k1], nu, [k2+k3], ro);
tracen 1;

id [q-k1] = q-k1;
id [q-k2] = q-k2;
id [k2+k3] = k2+k3;
id k1.k1 = 0;
id k2.k2 = 0;
id k3.k3 = 0;
id q.q = 1;

id n = 4-0*ep;
.sort

Print +s;
.end;
