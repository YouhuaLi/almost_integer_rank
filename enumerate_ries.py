"""Enumerate all RIES-alphabet expressions up to complexity CMAX, keep the cheapest postfix per
distinct value, and report almost integers with surplus = -log10|v-nint v| - c/10 > 0."""
import math, sys, time
CMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
CONST = {'1':1.0,'2':2.0,'3':3.0,'4':4.0,'5':5.0,'6':6.0,'7':7.0,'8':8.0,'9':9.0,'p':math.pi,'e':math.e,'f':(1+5**.5)/2}
WC = {'1':10,'2':13,'3':15,'4':16,'5':17,'6':18,'7':18,'8':19,'9':19,'p':14,'e':16,'f':18}
UN = {'n':(7,lambda a:-a),'r':(7,lambda a:1/a),'s':(9,lambda a:a*a),'q':(9,math.sqrt),'l':(13,math.log),'E':(13,math.exp),
      'S':(13,lambda a:math.sin(math.pi*a)),'C':(13,lambda a:math.cos(math.pi*a))}
BIN = {'+':(4,lambda a,b:a+b),'-':(5,lambda a,b:a-b),'*':(4,lambda a,b:a*b),'/':(5,lambda a,b:a/b),
       '^':(6,lambda a,b:a**b),'v':(7,lambda a,b:b**(1/a)),'L':(9,lambda a,b:math.log(b)/math.log(a))}
LIM = 1e15
def key(v): return float('%.14g' % v)
best = {}                     # key -> (c, postfix, value)
level = {c: [] for c in range(0, CMAX+1)}   # c -> list of (value, postfix) first seen at this level
def put(v, c, pf):
    if not math.isfinite(v) or abs(v) > LIM or abs(v) < 1e-9: return
    k = key(v)
    if k in best: return
    best[k] = (c, pf, v); level[c].append((v, pf))
t0 = time.time()
for c in range(10, CMAX+1):
    for s, v in CONST.items():
        if WC[s] == c: put(v, c, s)
    for s, (w, f) in UN.items():
        for v, pf in level.get(c-w, []):
            try: put(f(v), c, pf+s)
            except (ValueError, ZeroDivisionError, OverflowError): pass
    for s, (w, f) in BIN.items():
        rest = c - w
        for c1 in range(10, rest-9):
            c2 = rest - c1
            if c2 < 10: continue
            L1, L2 = level[c1], level[c2]
            if not L1 or not L2: continue
            for a, pa in L1:
                for b, pb in L2:
                    try: put(f(a, b), c, pa+pb+s)
                    except (ValueError, ZeroDivisionError, OverflowError, TypeError): pass
    print('c=%d distinct=%d (%.0fs)' % (c, len(best), time.time()-t0), file=sys.stderr)
# screen
cands = []; exactish = []
for k, (c, pf, v) in best.items():
    d = abs(v - round(v))
    if d == 0 or abs(v) < 0.5: continue
    if d < 1e-10*max(1, abs(v)): exactish.append((c, pf, v)); continue
    n = -math.log10(d)
    if n - c/10 > -1.0: cands.append((n - c/10, n, c, pf, v))
cands.sort(reverse=True)
print('distinct values:', len(best), ' float-screen candidates (surplus>-0.5):', len(cands), ' exact-looking:', len(exactish))
# verify with mpmath
from mpmath import mp, mpf, pi, e, phi, sqrt, log, exp, sin, cos, fabs, nint
mp.dps = 60
MC = {'p':pi,'e':e,'f':phi}
def ev(pf):
    st = []
    for t in pf:
        if t in CONST: st.append(MC[t] if t in MC else mpf(int(t)))
        elif t == 'n': st.append(-st.pop())
        elif t == 'r': st.append(1/st.pop())
        elif t == 's': a = st.pop(); st.append(a*a)
        elif t == 'q': st.append(sqrt(st.pop()))
        elif t == 'l': st.append(log(st.pop()))
        elif t == 'E': st.append(exp(st.pop()))
        elif t == 'S': st.append(sin(pi*st.pop()))
        elif t == 'C': st.append(cos(pi*st.pop()))
        else:
            b = st.pop(); a = st.pop()
            if t == '+': st.append(a+b)
            elif t == '-': st.append(a-b)
            elif t == '*': st.append(a*b)
            elif t == '/': st.append(a/b)
            elif t == '^': st.append(a**b)
            elif t == 'v': st.append(b**(1/a))
            elif t == 'L': st.append(log(b)/log(a))
    return st[0]
def digits(pf, dps):
    with mp.workdps(dps):
        try: x = ev(pf)
        except Exception: return None, None
        d = fabs(x - nint(x))
        if d == 0: return None, x
        return float(-log(d)/log(10)), x
out = []; artifacts = 0
for c, pf in [(c, pf) for _, _, c, pf, _ in cands] + [(c, pf) for c, pf, _ in exactish]:
    n40, _ = digits(pf, 40); n120, x = digits(pf, 120)
    if n40 is None or n120 is None or abs(n120 - n40) > 0.5: artifacts += 1; continue   # exact identity in disguise
    with mp.workdps(30): out.append((n120 - c/10, n120, c, pf, mp.nstr(x, 22)))
out.sort(reverse=True)
print('verified candidates:', len(out), ' precision artifacts removed:', artifacts)
print('%8s %6s %4s  %-14s %s' % ('surplus','n','cplx','postfix','value'))
for sur, n, c, pf, x in out[:30]:
    print('%8.2f %6.2f %4d  %-14s %s' % (sur, n, c, pf, x))
print('count with surplus > 0:', sum(1 for o in out if o[0] > 0), ' > 1:', sum(1 for o in out if o[0] > 1))

# ---------------- perturbation robustness filter ----------------
# A genuine coincidence is destroyed when any constant in the expression is changed; an
# asymptotic/amplifier construction (cos(pi*tiny), a^(1/huge), Pisot powers, iterated cos) survives.
# r = max digits over all single-token perturbations; genuine digits = n - r.
PERT = {'p':['e','f'], 'e':['p','f'], 'f':['p','e']}
for d in '123456789':
    PERT[d] = [x for x in (chr(ord(d)-1), chr(ord(d)+1)) if x in '123456789']
def robust_digits(pf):
    r = 0.0; worst = None
    for i, t in enumerate(pf):
        for alt in PERT.get(t, []):
            n2, _ = digits(pf[:i] + alt + pf[i+1:], 60)
            if n2 is not None and n2 > r: r, worst = n2, pf[:i] + alt + pf[i+1:]
    return r, worst
def trig_amp(pf):
    core = pf.rstrip('nr')           # ignore trailing negate / reciprocal
    return core[-1:] in ('S', 'C')   # sinpi/cospi at a critical point: error-squaring amplifier
adj = []; trig = []
for sur, n, c, pf, x in out:
    if sur <= -1: continue
    r, worst = robust_digits(pf)
    rec = (n - r - c/10, n, r, c, pf, x, worst)
    (trig if trig_amp(pf) else adj).append(rec)
adj.sort(reverse=True)
print('\nAfter perturbation filter: adjusted surplus = (n - r) - c/10,  r = best digits among perturbed variants')
print('%8s %6s %6s %4s  %-12s %-24s %s' % ('adj','n','r','cplx','postfix','value','most robust perturbation'))
for a, n, r, c, pf, x, worst in adj[:25]:
    print('%8.2f %6.2f %6.2f %4d  %-12s %-24s %s' % (a, n, r, c, pf, x, worst))
print('count with adjusted surplus > 0 (non-trig):', sum(1 for a in adj if a[0] > 0), '   trig amplifiers set aside:', len(trig),
      ' of which adjusted > 0:', sum(1 for a in trig if a[0] > 0))
