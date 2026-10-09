# -*- coding: utf-8 -*-
"""Rank MathWorld almost integers.

Primary metric: surplus = n_cont - complexity/10, where n_cont = -log10|x - nint(x)|.
RIES weights are calibrated so that ~10^(c/10) expressions have complexity <= c
(ries.c: 2,236,462 expressions up to complexity 64), so 10^(c/10 - n) is the expected
number of equally good coincidences; surplus > 0 means rarer than chance.

Error-squaring amplifiers are stripped: trig(y) with y near a critical point
(cos y ~ +-1  <=>  y ~ k*pi ; sin y ~ +-1  <=>  y ~ (k+1/2)*pi) squares the error of the
underlying near-identity y ~ m*pi, so such items are scored by their core almost integer.
Pisot powers x^k (x an algebraic integer whose other conjugates all have |.| < 1) approach
integers geometrically in k while complexity grows only like log k; they are detected
automatically (findpoly on the base) and stripped as well.

complexity(): sum of RIES symbol weights (ries.c: weight_base=10 + per-symbol weight).
n: number of consecutive 0s or 9s immediately after the decimal point of |x|.
"""
import math, re, json
from mpmath import mp, mpf, pi, e, exp, log, sqrt, sin, cos, tan, cosh, tanh, asinh, gamma, findpoly, polyroots, atan2, sinh, \
    euler, catalan, khinchin, zeta, erfi, digamma, phi, nint, floor, fabs, polyroots

mp.dps = 120

# ---- RIES symbol weights (already including weight_base = 10), from ries.c add_symbol() calls ----
W = {
    '1':10,'2':13,'3':15,'4':16,'5':17,'6':18,'7':18,'8':19,'9':19,
    'phi':18,'e':16,'pi':14,
    'neg':7,'recip':7,'sq':9,'sqrt':9,'ln':13,'exp':13,
    'sin':13,'cos':13,'tan':16,'sinpi':13,'cospi':13,'tanpi':16,'W':15,
    '+':4,'-':5,'*':4,'/':5,'^':6,'root':7,'log':9,'atan2':9,
}
# ---- extensions (not in ries.c), documented assumptions ----
EXT = {
    # hyperbolic functions: same as trig (10+3)
    'cosh':13,'sinh':13,'tanh':13,'asinh':15,
    # special functions: same as LambertW (10+5)
    'Gamma':15,'digamma':15,'erfi':15,'zeta':15,
    # named constants not in ries: like phi (10+8)
    'gamma':18,'C':18,'K':18,'psi':18,
}
def wint(n):
    """Integer weight: ries table for 1..9, else 10 + round(10*log10 n) (ries.c comment:
    'weight is close to 10.0*ln(x)/ln(10)')."""
    if 1 <= n <= 9: return W[str(n)]
    return 10 + round(10*math.log10(n))
def complexity(postfix):
    tot = 0
    for t in postfix.split():
        if t in W: tot += W[t]
        elif t in EXT: tot += EXT[t]
        elif re.fullmatch(r'\d+', t): tot += wint(int(t))
        else: raise ValueError('unknown token '+t)
    return tot

def nines_zeros(x, maxd=100):
    """count consecutive 0s or 9s right after the decimal point of |x|."""
    s = mp.nstr(fabs(x), maxd, strip_zeros=False, min_fixed=-1000, max_fixed=1000)
    if 'e' in s: return 0
    frac = s.split('.')[1] if '.' in s else ''
    if not frac: return 0
    d = frac[0]
    if d not in '09': return 0
    n = 0
    for c in frac:
        if c == d: n += 1
        else: break
    return n

def n_cont(x):
    d = fabs(x - nint(x))
    return float(-log(d)/log(10)) if d != 0 else float('inf')
def n_rel(x):
    """relative precision: scale = max(|nint(x)|, 1) so near-0 / near-1 items are unchanged."""
    d = fabs(x - nint(x)) / max(fabs(nint(x)), mpf(1))
    return float(-log(d)/log(10)) if d != 0 else float('inf')

psi_sg = [r for r in polyroots([1,-1,0,-1]) if abs(r.imag) < 1e-50][0].real  # supergolden ratio
gam = euler
def ln(x): return log(x)
def log10(x): return log(x)/log(10)

items = []  # (eq, name, postfix, value, note)
def add(eq, name, postfix, val, note=''):
    items.append((eq, name, postfix, mpf(val) if not isinstance(val, mpf) else val, note))

add('1', '(1782^12+1841^12)/1922^12', '1782 12 ^ 1841 12 ^ + 1922 12 ^ /',
    (mpf(1782)**12+mpf(1841)**12)/mpf(1922)**12)
add('2', '(3987^12+4365^12)/4472^12', '3987 12 ^ 4365 12 ^ + 4472 12 ^ /',
    (mpf(3987)**12+mpf(4365)**12)/mpf(4472)**12)
# --- amplifiers (kept for reference, scored separately) ---
AMP = []
def amp(eq, name, postfix, val, core):
    AMP.append((eq, name, postfix, val, core))
amp('3',  'sin(11)',                      '11 sin',                    sin(11),                          '22/pi ~ 7')
amp('5*', 'cos(22)',                      '22 cos',                    cos(22),                          '22/pi ~ 7')
amp('4',  'sin(2017*2^(1/5))',            '2017 5 2 root * sin',       sin(2017*mpf(2)**(mpf(1)/5)),     '4034*2^(1/5)/pi ~ 1475')
amp('8',  'cos(ln(pi+20))',               'pi 20 + ln cos',            cos(log(pi+20)),                  'e^pi - pi ~ 20 (eq 6)')
amp('14', 'cos(pi cos(pi cos(ln(pi+20))))','pi 20 + ln cos cospi cospi', cos(pi*cos(pi*cos(log(pi+20)))), 'e^pi - pi ~ 20 (eq 6)')
# --- their cores ---
add('3/5', '22/pi  [core of sin 11, cos 22]', '22 pi /', 22/pi, 'core of the stripped amplifiers sin 11 and cos 22: 22 ≈ 7π, and cos(7π+ε) = −1 + ε²/2, sin²11 = (1 − cos 22)/2')
add('4c', '4034*2^(1/5)/pi  [core of sin(2017*2^(1/5))]', '4034 5 2 root * pi /', 4034*mpf(2)**(mpf(1)/5)/pi,
    'core of the stripped amplifier sin(2017·2^(1/5)): 2017·2^(1/5) ≈ 737.5π, the sine squares the error')
add('6', 'e^pi - pi  [core of eq 8, 14]', 'pi exp pi -', exp(pi)-pi, 'core of the stripped amplifiers cos(ln(π+20)) and cos(π cos(π cos(ln(π+20))))): e^π ≈ π+20 gives ln(π+20) ≈ π, each cosine squares the error')
add('11', 'e^(-pi)(8pi-2)', 'pi neg exp 8 pi * 2 - *', exp(-pi)*(8*pi-2))
v=mpf(5)
for _ in range(7): v=cos(v)
add('15', '2cos(cos(cos(cos(cos(cos(cos 5))))))^2', '5 cos cos cos cos cos cos cos sq 2 *', 2*v**2)
add('16', '22pi^4', 'pi sq sq 22 *', 22*pi**4)
add('17', '510 log10(7)', '510 10 7 log *', 510*log10(7))
add('18', '88 ln 89', '88 89 ln *', 88*log(89))
add('19', '272 log_pi(97)', '272 pi 97 log *', 272*log(97)/log(pi))
a=mpf(1)/10; b=sqrt(2)/20
add('20', '1/4[cos(1/10)+cosh(1/10)+2cos(sqrt2/20)cosh(sqrt2/20)]',
    '10 recip cos 10 recip cosh + 2 sqrt 20 / cos 2 sqrt 20 / cosh * 2 * + 4 /',
    (cos(a)+cosh(a)+2*cos(b)*cosh(b))/4)
add('21', 'e^6 - pi^4 - pi^5', '6 exp pi sq sq - pi 5 ^ -', exp(6)-pi**4-pi**5)
add('22', 'pi^9/e^8', 'pi 9 ^ 8 exp /', pi**9/exp(8))
add('23', '10 tanh(28pi/15) - pi^9/e^8', '10 28 pi * 15 / tanh * pi 9 ^ 8 exp / -',
    10*tanh(28*pi/15)-pi**9/exp(8))
add('24', '(e^pi - ln3)/ln2 - 4/5', 'pi exp 3 ln - 2 ln / 4 5 / -', (exp(pi)-log(3))/log(2)-mpf(4)/5)
add('25', '10(e^pi - ln3)/ln2', '10 pi exp 3 ln - * 2 ln /', 10*(exp(pi)-log(3))/log(2))
add('26', '5(1+sqrt5)Gamma(3/4)^2/(e^(5pi/6)sqrt(pi))', '10 phi * 3 4 / Gamma sq * 5 pi * 6 / exp pi sqrt * /',
    5*(1+sqrt(5))*gamma(mpf(3)/4)**2/(exp(5*pi/6)*sqrt(pi)))
add('27', 'ln2 + log10(2)', '2 ln 10 2 log +', log(2)+log10(2))
add('28', '163/ln(163)', '163 163 ln /', 163/log(163))
add('29', 'e C^(5/7-gamma) pi^(-(2/7+gamma))', 'e C 5 7 / gamma - ^ * pi 2 7 / gamma + neg ^ *',
    e*catalan**(mpf(5)/7-gam)*pi**(-(mpf(2)/7+gam)))
add('30', 'C^(gamma-19/7) pi^(2/7+gamma)/(2phi)', 'C gamma 19 7 / - ^ pi 2 7 / gamma + ^ * 2 phi * /',
    catalan**(gam-mpf(19)/7)*pi**(mpf(2)/7+gam)/(2*phi))
add('31', 'e gamma phi (C pi)^(-(2/7+gamma))', 'e gamma * phi * C pi * 2 7 / gamma + neg ^ *',
    e*gam*phi*(catalan*pi)**(-(mpf(2)/7+gam)))
add('32', '163(pi-e)', '163 pi e - *', 163*(pi-e))
add('33', '53453/ln(53453)', '53453 53453 ln /', 53453/log(53453))
add('34', '613/37 e - 35/991', '613 37 / e * 35 991 / -', mpf(613)/37*e-mpf(35)/991)
add('37', '(91/10)^(1/4) - 33/19', '91 10 / sqrt sqrt 33 19 / -', (mpf(91)/10)**(mpf(1)/4)-mpf(33)/19)
add('38', '(23/9)^5', '23 9 / 5 ^', (mpf(23)/9)**5)
add('39', '3sqrt2(sqrt5-2)', '3 2 sqrt * 5 sqrt 2 - *', 3*sqrt(2)*(sqrt(5)-2))
add('40', 'zeta(3) - [gamma^(-1/3) + pi^(-4)(1+2gamma-2/(130+pi^2))^(-3)]',
    '3 zeta 3 gamma root recip pi sq sq recip 1 2 gamma * + 2 130 pi sq + / - 3 ^ recip * + -',
    zeta(3)-(gam**(-mpf(1)/3)+pi**(-4)*(1+2*gam-2/(130+pi**2))**(-3)), 'MathWorld alt-text reads π^(−1/4); the Apéry constant approximations page gives π^(−4), which matches the stated 4-digit accuracy')
add('41', '5 phi e/(7pi)', '5 phi * e * 7 pi * /', 5*phi*e/(7*pi))
add('42', 'ln K - ln ln K', 'K ln K ln ln -', log(khinchin)-log(log(khinchin)))
add('43', 'sqrt(45)^gamma', '45 sqrt gamma ^', sqrt(45)**gam)
add('44', 'erfi(erfi(sqrt3/3))', '3 sqrt recip erfi erfi', erfi(erfi(1/sqrt(3))))
add('45', '10(gamma^(-1/2)-1)^2', '10 gamma sqrt recip 1 - sq *', 10*(gam**(-mpf(1)/2)-1)**2)
add('46', '10/81(11-2sqrt10) - gamma', '10 81 / 11 40 sqrt - * gamma -', mpf(10)/81*(11-2*sqrt(10))-gam)
add('47', 'exp(-psi0((2+sqrt3)/4))', '2 3 sqrt + 4 / digamma neg exp', exp(-digamma((2+sqrt(3))/4)))
add('48', '7/64 ln2 - 131/1728', '7 64 / 2 ln * 131 1728 / -', mpf(7)/64*log(2)-mpf(131)/1728)
add('49', '80497/40320 - 43/144 pi^2 + 3293/1260 ln2 - 43/24 (ln2)^2',
    '80497 40320 / 43 144 / pi sq * - 3293 1260 / 2 ln * + 43 24 / 2 ln sq * -',
    mpf(80497)/40320-mpf(43)/144*pi**2+mpf(3293)/1260*log(2)-mpf(43)/24*log(2)**2)
add('50', '2411287/30240 - 100/9 pi^2 + 1877/21 ln2 - 200/3 (ln2)^2',
    '2411287 30240 / 100 9 / pi sq * - 1877 21 / 2 ln * + 200 3 / 2 ln sq * -',
    mpf(2411287)/30240-mpf(100)/9*pi**2+mpf(1877)/21*log(2)-mpf(200)/3*log(2)**2)
add('51', '1/(3^(1/3) ln2)', '3 3 root 2 ln * recip', 1/(mpf(3)**(mpf(1)/3)*log(2)))
lbar = (2+4*sqrt(2)+(4+sqrt(2))*asinh(1))/30
add('56', 'lbar - (sqrt2-1),  lbar=1/30[2+4sqrt2+(4+sqrt2)asinh 1]',
    '2 4 2 sqrt * + 4 2 sqrt + 1 asinh * + 30 / 2 sqrt - 1 +', lbar-(sqrt(2)-1))
add('57', 'phi/2^(ln2)', 'phi 2 2 ln ^ /', phi/2**log(2))
add('58', 'psi^11 (supergolden)', 'psi 11 ^', psi_sg**11)
add('59', '(sqrt2 psi)^24 - e^(pi sqrt31)', '2 sqrt psi * 24 ^ pi 31 sqrt * exp -',
    (sqrt(2)*psi_sg)**24-exp(pi*sqrt(31)))
for n in range(0, 18):
    hn = mp.factorial(n)/(2*log(2)**(n+1))
    if n == 0:
        pf = '2 2 ln * recip'
    elif n == 1:
        pf = '2 2 ln sq * recip'
    else:
        m = math.factorial(n)//2
        pf = ('%d 2 ln %d ^ /' % (m, n+1)) if m > 1 else ('2 ln %d ^ recip' % (n+1))
    add('60', 'h_%d = %d!/(2 ln2^%d)' % (n, n, n+1), pf, hn, 'Hickerson number h_n = n!/(2 (ln 2)^(n+1)), shown in lowest terms')
for n in [25,37,43,58,67,74,148,163,232,268,522,652,719]:
    if n == 25:
        pf = '5 pi * exp'
    else:
        pf = 'pi %d sqrt * exp' % n
    add('Tbl', 'e^(pi sqrt%d)' % n, pf, exp(pi*sqrt(n)))
add('65', '[ln(640320^3+744)/pi]^2', '640320 3 ^ 744 + ln pi / sq', (log(mpf(640320)**3+744)/pi)**2)
q = exp(-pi*sqrt(163))
add('66', '1 - 262537412640768744 q - 196884 q^2 + 103378831900730205293632 q^3, q=e^(-pi sqrt163)',
    '1 262537412640768744 pi 163 sqrt * neg exp * - 196884 2 pi 163 sqrt * * neg exp * - '
    '103378831900730205293632 3 pi 163 sqrt * * neg exp * +',
    1-262537412640768744*q-196884*q**2+103378831900730205293632*q**3)
add('67', 'd = 1/2 sqrt(1/30(61421-23 sqrt5831385))', '61421 23 5831385 sqrt * - 30 / sqrt 2 /',
    sqrt((61421-23*sqrt(5831385))/30)/2)
add('ext', '2 (ln pi)^3  [user-supplied, not on MathWorld]', '2 pi ln 3 ^ *', 2*log(pi)**3, 'user-supplied, not on MathWorld')
add('ext', '533 cos 23  [user-supplied, not on MathWorld]', '533 23 cos *', 533*cos(23), 'user-supplied, not on MathWorld')
add('ext', '(1 + 2 sqrt21 cos(atan(sqrt3/9)/3)/3)^100  [user-supplied, not on MathWorld]',
    '1 2 21 sqrt * 3 sqrt 9 atan2 3 / cos * 3 / + 100 ^',
    (1 + 2*sqrt(21)*cos(mp.atan(sqrt(3)/9)/3)/3)**100, 'user-supplied')
def _unit(a, pf): return a + sqrt(a*a - 1), '%s %s sq 1 - sqrt +' % (pf, pf)      # a + sqrt(a^2 - 1)
with mp.workdps(400):
    _u = [_unit((23+4*sqrt(34))/2, '23 4 34 sqrt * + 2 /'), _unit((19*sqrt(2)+7*sqrt(17))/2, '19 2 sqrt * 7 17 sqrt * + 2 /'),
          _unit(429+304*sqrt(2), '429 304 2 sqrt * +'), _unit((627+442*sqrt(2))/2, '627 442 2 sqrt * + 2 /')]
    _P = _u[0][0]**2 * _u[1][0]**2 * _u[2][0] * _u[3][0]
    _cm_val = (log(((2*_P)**6 + 24)**2 - 552)/pi)**2
add('ext', '[ln(((2P)^6+24)^2 - 552)/pi]^2, P = product of quadratic units  [user-supplied, not on MathWorld]',
    '2 %s sq %s sq * %s * %s * * 6 ^ 24 + sq 552 - ln pi / sq' % tuple(x[1] for x in _u), _cm_val, 'user-supplied')

# ---------------- postfix evaluator (validates the hand-written postfix) ----------------
CONST = {'pi':pi,'e':e,'phi':phi,'gamma':euler,'C':catalan,'K':khinchin}
UN = {'neg':lambda a:-a,'recip':lambda a:1/a,'sq':lambda a:a*a,'sqrt':sqrt,'ln':log,'exp':exp,
      'sin':sin,'cos':cos,'tan':tan,'sinpi':lambda a:sin(pi*a),'cospi':lambda a:cos(pi*a),'tanpi':lambda a:tan(pi*a),
      'W':mp.lambertw,'cosh':cosh,'sinh':sinh,'tanh':tanh,'asinh':asinh,'Gamma':gamma,'digamma':digamma,'erfi':erfi,'zeta':zeta}
BIN = {'+':lambda a,b:a+b,'-':lambda a,b:a-b,'*':lambda a,b:a*b,'/':lambda a,b:a/b,'^':lambda a,b:a**b,
       'root':lambda a,b:b**(1/a),'log':lambda a,b:log(b)/log(a),'atan2':lambda y,x:atan2(y,x)}
def eval_postfix(pf):
    st = []
    for t in pf.split():
        if t == 'psi': st.append(psi_sg)
        elif t in CONST: st.append(CONST[t])
        elif re.fullmatch(r'\d+', t): st.append(mpf(int(t)))
        elif t in UN: st.append(UN[t](st.pop()))
        elif t in BIN: b = st.pop(); a = st.pop(); st.append(BIN[t](a, b))
        else: raise ValueError('unknown token ' + t)
    assert len(st) == 1, pf
    return st[0]

def pisot_base(pf):
    """If pf is  <expr> K ^  or  <expr> sq, return (base_value, minpoly) when base is a Pisot number, else None."""
    t = pf.split()
    if len(t) >= 3 and t[-1] == '^' and re.fullmatch(r'\d+', t[-2]): base_pf = ' '.join(t[:-2])
    elif len(t) >= 2 and t[-1] == 'sq': base_pf = ' '.join(t[:-1])
    else: return None
    x = eval_postfix(base_pf)
    with mp.workdps(60):
        p = findpoly(x, 8, maxcoeff=10**6)
    if p is None or abs(p[0]) != 1 or len(p) < 3: return None      # not an algebraic integer (or rational)
    try:
        roots = polyroots(p, maxsteps=500, extraprec=500)
    except Exception as ex:
        print('pisot_base: polyroots failed for', pf, p, ex); return None
    others = [r for r in roots if abs(r - x) > mpf(10)**-40]
    if all(abs(r) < 1 for r in others): return x, p
    return None

for eq, name, pf, val, note in items + [a[:4] + ('',) for a in AMP]:
    v = eval_postfix(pf)
    assert fabs(v - val) <= mpf(10)**-30 * max(1, fabs(val)), (eq, name, v, val)

# ---------------- CM / modular-function identities ----------------
# At a CM point a modular function takes an algebraic value y with y = e^(pi sqrt r) (1 + O(e^(-pi sqrt r))),
# r rational (j: r = D; Weber f: r = D/576).  An algebraic subexpression y with (ln y / pi)^2 ~ p/q is such
# a theorem, not a coincidence, and ln(y) turns it into relative precision.  Also caught: "log-algebraic"
# subexpressions (ln of algebraic numbers and their rational combinations), whose exponential is algebraic.
# If y is an integer the core is e^(pi sqrt r) itself, scored on its own; otherwise there is no core.
ALG_CONST = {'phi', 'psi'}
CM_MIN_LOG = math.log(10**6)       # |y| >= 10^6 (or <= 10^-6)
CM_MAXQ, CM_TOL = 576, mpf(10)**-10
# Hauptmoduln carry a constant term (j = 1/q + 744 + ..., f^24 = 1/q - 24 + ...), so ln y = pi sqrt r + c/y:
# with r = p/q, q <= 4, accept |ln|y| - pi sqrt r| < 1000/|y| as well
CM_MAXQ2, CM_C = 4, 1000
def cm_identity(pf):
    """return (r, is_int, y) for the outermost algebraic subexpression y ~ e^(pi sqrt r), r = p/q with q <= 576
    (failing that, the outermost log-algebraic one, y = its exponential); None if there is none"""
    toks = pf.split(); st = []      # node: (lo, kind, is_int, is_rat); kind in 'alg', 'log', None
    hits = []
    for i, t in enumerate(toks):
        if re.fullmatch(r'\d+', t): node = (i, 'alg', True, True)
        elif t in ALG_CONST: node = (i, 'alg', False, False)
        elif t in CONST or t == 'psi': node = (i, None, False, False)
        elif t in UN:
            lo, k, it, rt = st.pop()
            if k == 'alg' and t in ('neg', 'recip', 'sq', 'sqrt'):
                node = (lo, 'alg', it and t in ('neg', 'sq'), rt and t in ('neg', 'recip', 'sq'))
            elif k == 'alg' and t == 'ln': node = (lo, 'log', False, False)
            elif k == 'log' and t == 'neg': node = (lo, 'log', False, False)
            else: node = (lo, None, False, False)
        elif t in BIN:
            b = st.pop(); a = st.pop(); lo = a[0]; ka, kb = a[1], b[1]
            if ka == kb == 'alg' and t in ('+', '-', '*', '/'):
                node = (lo, 'alg', a[2] and b[2] and t != '/', a[3] and b[3])
            elif ka == 'alg' and b[3] and t == '^':
                node = (lo, 'alg', a[2] and b[2], a[3] and b[2])
            elif a[2] and kb == 'alg' and t == 'root': node = (lo, 'alg', False, False)
            elif ka == kb == 'log' and t in ('+', '-'): node = (lo, 'log', False, False)
            elif t == '*' and ((ka == 'log' and b[3]) or (a[3] and kb == 'log')): node = (lo, 'log', False, False)
            elif t == '/' and ka == 'log' and b[3]: node = (lo, 'log', False, False)
            else: node = (lo, None, False, False)
        else: raise ValueError(t)
        st.append(node)
        lo, k, it, rt = node
        if k is None: continue
        sub = ' '.join(toks[lo:i+1])
        with mp.workdps(200):
            v = eval_postfix(sub)
            lny = log(fabs(v)) if k == 'alg' else v
            if fabs(lny) < CM_MIN_LOG: continue
            r = (lny/pi)**2
            for q in range(1, CM_MAXQ + 1):
                p = int(nint(r*q))
                if fabs(r - mpf(p)/q) < CM_TOL or \
                   (q <= CM_MAXQ2 and fabs(fabs(lny) - pi*sqrt(mpf(p)/q)) < CM_C*exp(-fabs(lny))):
                    hits.append((k == 'alg', i - lo, (p, q), k == 'alg' and it, v if k == 'alg' else exp(v))); break
    if not hits: return None
    _, _, r, is_int, y = max(hits, key=lambda h: h[:2])
    return r, is_int, y
def cm_core_pf(r):
    p, q = r; g = math.gcd(p, q); p, q = p//g, q//g
    if q == 1:
        s = math.isqrt(p)
        if s*s == p: return 'pi exp' if s == 1 else '%d pi * exp' % s
        return 'pi %d sqrt * exp' % p
    return 'pi %d %d / sqrt * exp' % (p, q)

kept = []
for it in items:
    eq, name, pf, val, note = it
    cm = cm_identity(pf)
    if cm:
        r, is_int, y = cm
        rs = '%d/%d' % r if r[1] > 1 else str(r[0])
        if is_int:
            core = cm_core_pf(r)
            AMP.append((eq, name, pf, val, 'CM identity: integer %d ~ e^(pi sqrt %s), core e^(pi sqrt %s)' % (int(nint(y)), rs, rs)))
            if not any(x[2] == core for x in items):
                kept.append(('cm', '%s  [core of eq %s]' % (core, eq), core, eval_postfix(core), 'core of the stripped CM identity eq %s' % eq))
        else:
            AMP.append((eq, name, pf, val, 'CM identity: algebraic %s ~ e^(pi sqrt %s) (no almost-integer core)' % (mp.nstr(y, 12), rs)))
    else:
        kept.append(it)
items = kept

kept = []
for it in items:
    eq, name, pf, val, note = it
    pb = pisot_base(pf)
    if pb:
        x, p = pb
        AMP.append((eq, name, pf, val, 'Pisot power: base %s, minpoly %s (no almost-integer core)' % (mp.nstr(x, 12), p)))
    else:
        kept.append(it)
items = kept

# ---------------- structural-stability test ----------------
# A genuine coincidence is destroyed when some constant in the expression is moved by 1%;
# a structural limit (1/pi^100, cos(pi/8^8), iterated cos near -1) survives any such move.
# Integer terms added/subtracted at the top level are exempt: perturbing them merely shifts the target.
CONST_TOKENS = {'pi', 'e', 'phi', 'gamma', 'C', 'K', 'psi'}
def toplevel_additive_ints(toks):
    """indices of integer tokens that are direct operands of the outermost chain of + / - / neg"""
    spans = []                       # stack of (start_index, end_index) per subexpression
    for i, t in enumerate(toks):
        if t in UN: a = spans.pop(); spans.append((a[0], i))
        elif t in BIN: b = spans.pop(); a = spans.pop(); spans.append((a[0], i))
        else: spans.append((i, i))
    out = set()
    def walk(lo, hi):
        t = toks[hi]
        if lo == hi:
            if re.fullmatch(r'\d+', t): out.add(lo)
            return
        if t in ('+', '-') or t == 'neg':
            # find split: the left operand ends where the right operand begins
            if t == 'neg': walk(lo, hi - 1); return
            depth = 0
            for j in range(hi - 1, lo - 1, -1):     # scan right operand backwards
                tj = toks[j]
                depth += 1 if (tj not in UN and tj not in BIN) else (0 if tj in UN else -1)
                if depth == 1: walk(j, hi - 1); walk(lo, j - 1); return
    walk(0, len(toks) - 1)
    return out
def digits_of(pf, dps=60):
    with mp.workdps(dps):
        try: x = eval_postfix(pf)
        except Exception: return None
        d = fabs(x - nint(x))
        return float(-log(d)/log(10)) if d != 0 else float('inf')
def stability(pf):
    """min over 1% perturbations of every constant of the remaining digits; None if nothing to perturb"""
    toks = pf.split(); exempt = toplevel_additive_ints(toks); worst = None
    for i, t in enumerate(toks):
        if i in exempt or not (re.fullmatch(r'\d+', t) or t in CONST_TOKENS): continue
        for f in ('101 100 / *', '99 100 / *'):
            v = digits_of(' '.join(toks[:i+1] + f.split() + toks[i+1:]))
            if v is None: v = 0.0
            if worst is None or v < worst: worst = v
    return worst
STABLE_DIGITS = 3.0      # every perturbation still leaves >= 3 digits  =>  structural, not a coincidence
MIN_DIGITS = 2.0         # admission threshold: |x - nint x| < 0.01

kept = []; BELOW = []
for it in items:
    eq, name, pf, val, note = it
    st = stability(pf)
    if st is not None and st >= STABLE_DIGITS:
        AMP.append((eq, name, pf, val, 'structurally stable: every constant perturbed by 1%% still leaves %.1f digits' % st))
    elif n_cont(val) < MIN_DIGITS:
        BELOW.append(it)
    else:
        kept.append(it)
items = kept

rows = []
def score(eq, name, pf, val, note=''):
    c = complexity(pf); nc = n_cont(val)
    return dict(eq=eq, name=name, postfix=pf, value=mp.nstr(val, 40, min_fixed=-1000, max_fixed=1000),
                n_abs=nc, cplx=c, surplus=nc-c/10, note=note)
for eq, name, pf, val, note in items:
    rows.append(score(eq, name, pf, val, note))
rows.sort(key=lambda r: -r['surplus'])
TOP = 50                 # the ranking keeps only the top 50
N_ADMITTED = len(rows); rows = rows[:TOP]

amps = [dict(score(eq, name, pf, val), core=core) for eq, name, pf, val, core in AMP]
below = [score(eq, name, pf, val, note) for eq, name, pf, val, note in BELOW]
print('Below admission threshold (n < %.0f):' % MIN_DIGITS)
for r in below: print('  eq %-4s %-40s n=%6.2f' % (r['eq'], r['name'][:40], r['n_abs']))
print('Stripped amplifiers:')
for r in amps: print('  eq %-4s %-40s n=%6.2f c=%3d surplus=%7.2f -> %s' % (r['eq'], r['name'][:40], r['n_abs'], r['cplx'], r['surplus'], r['core']))
print()
print('%-4s %-5s %6s %4s %8s  %-52s %s' % ('rank','eq','n_abs','cplx','surplus','expression','value'))
for i, r in enumerate(rows, 1):
    print('%-4d %-5s %6.2f %4d %8.2f  %-52s %s' % (i, r['eq'], r['n_abs'], r['cplx'], r['surplus'], r['name'][:52], r['value'][:44]))

# ---------------- postfix -> LaTeX ----------------
# node = (latex, prec): prec 4 atom/function, 3 power, 2 product, 1 sum
CONST_TEX = {'pi':r'\pi','e':'e','phi':r'\phi','gamma':r'\gamma','C':'C','K':'K','psi':r'\psi'}
FUNC_TEX = {'ln':r'\ln','sin':r'\sin','cos':r'\cos','tan':r'\tan','cosh':r'\cosh','sinh':r'\sinh','tanh':r'\tanh',
            'asinh':r'\sinh^{-1}','Gamma':r'\Gamma','digamma':r'\psi_0','erfi':r'\operatorname{erfi}','zeta':r'\zeta','W':'W'}
def par(node, minprec):
    t, p = node
    return t if p >= minprec else r'\left(' + t + r'\right)'
def is_num(node): return re.fullmatch(r'\d+', node[0]) is not None
def base(node):
    """base of a power: only a bare number/constant stays unparenthesized"""
    if re.fullmatch(r'\\?[A-Za-z]+|\d+', node[0]) or re.fullmatch(r'\\[A-Za-z_0-9]+\\left\(.*\\right\)', node[0]):
        return node[0]          # bare symbol, or a single function call f(...)
    return r'\left(' + node[0] + r'\right)'
def to_latex(pf):
    st = []
    for t in pf.split():
        if t in CONST_TEX: st.append((CONST_TEX[t], 4))
        elif re.fullmatch(r'\d+', t): st.append((t, 4))
        elif t in FUNC_TEX:
            a = st.pop()
            bare = t in ('ln','sin','cos','tan','cosh','sinh','tanh','asinh') and re.fullmatch(r'\\?[A-Za-z]+|\d+', a[0])
            st.append((FUNC_TEX[t] + (' ' + a[0] if bare else r'\left(' + a[0] + r'\right)'), 4))
        elif t in ('sinpi', 'cospi', 'tanpi'):
            a = st.pop(); st.append(('\\' + t[:3] + r'\left(\pi ' + par(a, 2) + r'\right)', 4))
        elif t == 'exp': a = st.pop(); st.append(('e^{' + a[0] + '}', 3))
        elif t == 'neg': a = st.pop(); st.append(('-' + par(a, 2), 2))
        elif t == 'recip': a = st.pop(); st.append((r'\frac{1}{' + a[0] + '}', 4))
        elif t == 'sq':
            a = st.pop()
            m = re.fullmatch(r'(.*)\^\{(\d+)\}', a[0]) if a[1] == 3 else None
            st.append((m.group(1) + '^{%d}' % (2*int(m.group(2))), 3) if m else (base(a) + '^{2}', 3))
        elif t == 'sqrt':
            a = st.pop()
            m = re.fullmatch(r'\\sqrt\{(.*)\}', a[0])
            st.append((r'\sqrt[4]{' + m.group(1) + '}', 4) if m else (r'\sqrt{' + a[0] + '}', 4))
        elif t in ('+', '-'):
            b = st.pop(); a = st.pop()
            bt = par(b, 2) if t == '-' else par(b, 1)
            if t == '+' and bt.startswith('-'): t, bt = '-', bt[1:]
            st.append((par(a, 1) + ' ' + t + ' ' + bt, 1))
        elif t == '*':
            b = st.pop(); a = st.pop()
            if is_num(b) and not is_num(a): a, b = b, a
            sep = r' \cdot ' if is_num(a) and is_num(b) else ' '
            st.append((par(a, 2) + sep + par(b, 2), 2))
        elif t == '/': b = st.pop(); a = st.pop(); st.append((r'\frac{' + a[0] + '}{' + b[0] + '}', 4))
        elif t == '^': b = st.pop(); a = st.pop(); st.append((base(a) + '^{' + b[0] + '}', 3))
        elif t == 'root': b = st.pop(); a = st.pop(); st.append((r'\sqrt[' + a[0] + ']{' + b[0] + '}', 4))
        elif t == 'log': b = st.pop(); a = st.pop(); st.append((r'\log_{' + a[0] + '} ' + par(b, 4), 4))
        elif t == 'atan2': b = st.pop(); a = st.pop(); st.append((r'\arctan\left(\frac{' + a[0] + '}{' + b[0] + r'}\right)', 4))
        else: raise ValueError(t)
    assert len(st) == 1
    return st[0][0]

def write_results(path='results.md'):
    out = ['# MathWorld Almost Integers ranked by surplus = n − complexity/10\n',
    '- n = −log10 |x − nint(x)|, absolute precision, continuous',
    '- complexity = sum of RIES symbol weights (ries.c: base 10 + per-symbol weight) of the cheapest postfix form. Integer N≥10 weighs 10+round(10·log10 N); cosh/sinh/tanh 13, asinh 15; Gamma/digamma/erfi/zeta 15; gamma(Euler)/Catalan C/Khinchin K/supergolden psi 18',
    '- surplus = n − complexity/10. RIES weights are calibrated so ~10^(c/10) expressions have complexity ≤ c, so surplus > 0 means rarer than chance; brute-force search in trivial families (a·α/b, a/ln a, a·ln b) tops out at about −0.4',
    '- Amplifiers stripped (scored by their core almost integer, or dropped when there is none): error-squaring trig near a critical point, and Pisot powers x^k (algebraic-integer base with all other conjugates inside the unit circle, detected with findpoly), and CM identities (an algebraic subexpression y, or the exponential of a rational combination of logs of algebraic numbers, with y ≈ e^(π√r): a theorem of complex multiplication, and ln y turns its relative precision into absolute precision; y an integer is scored on its core e^(π√r), otherwise dropped). Stripped: ' + '; '.join('%s (surplus as written %.2f)' % (r['name'].split('  [')[0], r['surplus']) for r in amps),
    '- Admission threshold n ≥ 2 (|x − nint x| < 0.01). Below threshold, not ranked: ' + '; '.join('%s (n = %.2f)' % (r['name'].split('  [')[0], r['n_abs']) for r in below),
    '- Structural-stability test: every constant is perturbed by ±1% (top-level additive integers exempt); if every perturbation still leaves ≥ 3 digits the near-integrality is a limit, not a coincidence, and the entry is stripped',
    '- Excluded: infinite sums/products, non-closed forms and physical-unit items',
    '- Only the top %d of %d admitted entries are listed\n' % (TOP, N_ADMITTED),
    '| rank | expression | value | n | complexity | surplus |', '|---|---|---|---|---|---|']
    notes = {}                                   # note text -> footnote number, in order of first appearance
    for i, r in enumerate(rows, 1):
        expr = '$' + to_latex(r['postfix']) + '$'
        if r['note']:
            k = notes.setdefault(r['note'], len(notes) + 1)
            expr += '[^%d]' % k
        out.append('| %d | %s | %s | %.2f | %d | %.2f |' % (i, expr, r['value'][:46], r['n_abs'], r['cplx'], r['surplus']))
    out.append('')
    for text, k in sorted(notes.items(), key=lambda kv: kv[1]):
        out.append('[^%d]: %s' % (k, text))
    open(path, 'w').write('\n'.join(out) + '\n')
write_results()

# ---------------- data for the website ----------------
def write_site_data(path='site/data.json'):
    notes = {}
    data = []
    for i, r in enumerate(rows, 1):
        k = notes.setdefault(r['note'], len(notes) + 1) if r['note'] else None
        data.append(dict(rank=i, latex=to_latex(r['postfix']), postfix=r['postfix'], value=r['value'], n=round(r['n_abs'], 2),
                         complexity=r['cplx'], surplus=round(r['surplus'], 2), note=k))
    stripped = [dict(latex=to_latex(a['postfix']), name=a['name'], n=round(a['n_abs'], 2), complexity=a['cplx'],
                     surplus=round(a['surplus'], 2), core=a['core']) for a in amps]
    below_rows = [dict(latex=to_latex(b['postfix']), name=b['name'], n=round(b['n_abs'], 2), complexity=b['cplx'],
                       surplus=round(b['surplus'], 2), value=b['value']) for b in below]
    json.dump(dict(rows=data, notes=[t for t, k in sorted(notes.items(), key=lambda kv: kv[1])], stripped=stripped, below=below_rows),
              open(path, 'w'), indent=1, ensure_ascii=False)
write_site_data()
