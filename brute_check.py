import numpy as np, math, json
BASE=[]
def wint(n):
    t={1:10,2:13,3:15,4:16,5:17,6:18,7:18,8:19,9:19}
    return t[n] if n<=9 else 10+round(10*math.log10(n))
wv=np.vectorize(wint)
consts={'sqrt2':(math.sqrt(2),22),'sqrt3':(math.sqrt(3),24),'phi':((1+5**.5)/2,18),'pi':(math.pi,14),'e':(math.e,16),'ln2':(math.log(2),26)}
A=np.arange(1,20001); B=np.arange(1,301)
wa=wv(A); wb=wv(B)
print('family alpha*a/b, a<=20000, b<=300  (complexity: alpha a * b /, b=1 -> alpha a *)')
allbest=[]
for name,(al,wal) in consts.items():
    x=al*A[:,None]/B[None,:]
    err=np.abs(x-np.rint(x)); err[err==0]=1e-300
    n=-np.log10(err)
    c=wal+wa[:,None]+4+np.where(B[None,:]==1,0,wb[None,:]+5)
    # skip reducible pairs (gcd>1) to avoid duplicates
    g=np.gcd(A[:,None],B[None,:]); mask=(g==1)&(x>0.5)
    s=np.where(mask,n-c/10,-99)
    idx=np.argsort(s,axis=None)[::-1][:3]
    for k in idx:
        i,j=np.unravel_index(k,s.shape)
        print('  %-6s a=%6d b=%4d  value=%18.8f  n=%5.2f c=%3d surplus=%6.2f'%(name,A[i],B[j],x[i,j],n[i,j],c[i,j],s[i,j]))
        BASE.append(dict(family='%s*a/b (a<=20000, b<=300)'%name, expr='%s*%d/%d'%(name,A[i],B[j]) if B[j]>1 else '%s*%d'%(name,A[i]), value=float(x[i,j]), n=float(n[i,j]), c=int(c[i,j]), surplus=float(s[i,j])))
    allbest.append(s.max())
print('best surplus over all six families: %.2f'%max(allbest))
print()
print('family a/ln a, a<=10^6  (complexity: a a ln /)')
A=np.arange(2,10**6+1).astype(float); x=A/np.log(A); err=np.abs(x-np.rint(x)); n=-np.log10(err)
c=2*(10+np.round(10*np.log10(A)))+18; c[A<=9]=2*wv(A[A<=9].astype(int))+18
s=n-c/10
for k in np.argsort(s)[::-1][:5]:
    print('  a=%7d  value=%16.8f n=%5.2f c=%3d surplus=%6.2f'%(A[k],x[k],n[k],c[k],s[k]))
    BASE.append(dict(family='a/ln a (a<=10^6)', expr='%d/ln %d'%(A[k],A[k]), value=float(x[k]), n=float(n[k]), c=int(c[k]), surplus=float(s[k])))
print('  (MathWorld items: 163/ln163 and 53453/ln53453 are among these)')
print()
print('family a^(1/k) integer roots? skip.  family a*e^b? --- checking a*ln b, a,b<=3000 (complexity: a b ln *)')
A=np.arange(1,3001); B=np.arange(2,3001); wa=wv(A); wb=wv(B)
x=A[:,None]*np.log(B)[None,:]; err=np.abs(x-np.rint(x)); err[err==0]=1e-300; n=-np.log10(err)
c=wa[:,None]+wb[None,:]+13+4; s=n-c/10
for k in np.argsort(s,axis=None)[::-1][:4]:
    i,j=np.unravel_index(k,s.shape); print('  a=%4d b=%4d  value=%16.8f n=%5.2f c=%3d surplus=%6.2f'%(A[i],B[j],x[i,j],n[i,j],c[i,j],s[i,j]))
    BASE.append(dict(family='a*ln b (a,b<=3000)', expr='%d*ln %d'%(A[i],B[j]), value=float(x[i,j]), n=float(n[i,j]), c=int(c[i,j]), surplus=float(s[i,j])))
print('  (MathWorld item 88 ln 89 = 395.0000005 has surplus -1.23)')

json.dump(BASE, open('brute_baseline.json','w'), indent=1)
