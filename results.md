# MathWorld Almost Integers ranked by surplus = n − complexity/10

- n = −log10 |x − nint(x)|, absolute precision, continuous
- complexity = sum of RIES symbol weights (ries.c: base 10 + per-symbol weight) of the cheapest postfix form. Integer N≥10 weighs 10+round(10·log10 N); cosh/sinh/tanh 13, asinh 15; Gamma/digamma/erfi/zeta 15; gamma(Euler)/Catalan C/Khinchin K/supergolden psi 18
- surplus = n − complexity/10. RIES weights are calibrated so ~10^(c/10) expressions have complexity ≤ c, so surplus > 0 means rarer than chance; brute-force search in trivial families (a·α/b, a/ln a, a·ln b) tops out at about −0.4
- Amplifiers stripped (scored by their core almost integer, or dropped when there is none): error-squaring trig near a critical point, and Pisot powers x^k (algebraic-integer base with all other conjugates inside the unit circle, detected with findpoly), and CM identities (an algebraic subexpression y, or the exponential of a rational combination of logs of algebraic numbers, with y ≈ e^(π√r): a theorem of complex multiplication, and ln y turns its relative precision into absolute precision; y an integer is scored on its core e^(π√r), otherwise dropped). Stripped: sin(11) (surplus as written 1.71); cos(22) (surplus as written 0.81); sin(2017*2^(1/5)) (surplus as written 6.97); cos(ln(pi+20)) (surplus as written 2.42); cos(pi cos(pi cos(ln(pi+20)))) (surplus as written 25.11); (sqrt2 psi)^24 - e^(pi sqrt31) (surplus as written -9.24); [ln(640320^3+744)/pi]^2 (surplus as written 11.33); 1 - 262537412640768744 q - 196884 q^2 + 103378831900730205293632 q^3, q=e^(-pi sqrt163) (surplus as written -20.81); [ln(((2P)^6+24)^2 - 552)/pi]^2, P = product of quadratic units (surplus as written 113.43); psi^11 (supergolden) (surplus as written -0.75); (1 + 2 sqrt21 cos(atan(sqrt3/9)/3)/3)^100 (surplus as written -4.81)
- Admission threshold n ≥ 2 (|x − nint x| < 0.01). Below threshold, not ranked: e gamma phi (C pi)^(-(2/7+gamma)) (n = 1.70); h_0 = 0!/(2 ln2^1) (n = 0.55); h_1 = 1!/(2 ln2^2) (n = 1.39); h_12 = 12!/(2 ln2^13) (n = 1.73); h_14 = 14!/(2 ln2^15) (n = 1.07); h_15 = 15!/(2 ln2^16) (n = 1.43); h_16 = 16!/(2 ln2^17) (n = 0.31); h_17 = 17!/(2 ln2^18) (n = 0.34)
- Structural-stability test: every constant is perturbed by ±1% (top-level additive integers exempt); if every perturbation still leaves ≥ 3 digits the near-integrality is a limit, not a coincidence, and the entry is stripped
- Excluded: infinite sums/products, non-closed forms and physical-unit items
- Only the top 50 of 71 admitted entries are listed

| rank | expression | value | n | complexity | surplus |
|---|---|---|---|---|---|
| 1 | $e^{\pi \sqrt{163}}$ | 262537412640768743.9999999999992500725972 | 12.12 | 72 | 4.92 |
| 2 | $e^{\pi \sqrt{652}}$ | 68925893036109279891085639286943768.0 | 9.79 | 78 | 1.99 |
| 3 | $2 \tan 281240$[^1] | 23.00000000015672286196048415286018849574 | 9.80 | 97 | 0.10 |
| 4 | $e^{\pi \sqrt{58}}$ | 24591257751.99999982221324146957619235527 | 6.75 | 68 | -0.05 |
| 5 | $22 \pi^{4}$ | 2143.000002748053619201687319151512447494 | 5.56 | 59 | -0.34 |
| 6 | $483 \ln 24$[^1] | 1535.000000058057734289472793426477762486 | 7.24 | 78 | -0.56 |
| 7 | $e^{\pi \sqrt{67}}$ | 147197952743.9999986624542245068292613126 | 5.87 | 68 | -0.93 |
| 8 | $533 \cos 23$[^1] | -283.9999998377008969299988312684790531807 | 6.79 | 78 | -1.01 |
| 9 | $88 \ln 89$ | 395.0000005364283057719677675789467313076 | 6.27 | 75 | -1.23 |
| 10 | $\operatorname{erfi}\left(\operatorname{erfi}\left(\frac{1}{\sqrt{3}}\right)\right)$ | 1.000020873638094301958790984063380991539 | 4.68 | 61 | -1.42 |
| 11 | $e^{\pi} - \pi$[^2] | 19.99909997918947576726644298466904449607 | 3.05 | 46 | -1.55 |
| 12 | $e^{5 \pi}$ | 6635623.999341134233266264067099104921836 | 3.18 | 48 | -1.62 |
| 13 | $\frac{22}{\pi}$[^3] | 7.002817496043394773830885588390631929516 | 2.55 | 42 | -1.65 |
| 14 | $\left(\sqrt{45}\right)^{\gamma}$ | 3.000060964747862089151107609187765116399 | 4.21 | 60 | -1.79 |
| 15 | $e^{\pi \sqrt{37}}$ | 199148647.9999780465518567665009238753359 | 4.66 | 66 | -1.94 |
| 16 | $\frac{4034 \sqrt[5]{2}}{\pi}$[^4] | 1475.000000004168010349241114246732487378 | 8.38 | 106 | -2.22 |
| 17 | $e^{\pi \sqrt{232}}$ | 604729957825300084759.9999921715268564303 | 5.11 | 74 | -2.29 |
| 18 | $\frac{163}{\ln 163}$ | 31.99999873849008267575839302655654794109 | 5.90 | 82 | -2.30 |
| 19 | $510 \log_{10} 7$ | 431.0000004072709836632302918822444586766 | 6.39 | 88 | -2.41 |
| 20 | $272 \log_{\pi} 97$ | 1087.000000204958515735571061137038727898 | 6.69 | 91 | -2.41 |
| 21 | $10 \left(\frac{1}{\sqrt{\gamma}} - 1\right)^{2}$ | 0.9999980360927256298925092745354615655055 | 5.71 | 82 | -2.49 |
| 22 | $2 \left(\ln \pi\right)^{3}$[^1] | 3.000122992781408643057119744480242638993 | 3.91 | 65 | -2.59 |
| 23 | $\left(\frac{23}{9}\right)^{5}$ | 109.000033870175616860573422073193449508 | 4.47 | 71 | -2.63 |
| 24 | $\frac{1}{\left(\ln 2\right)^{3}}$[^5] | 3.00278070715690544349976740721930488951 | 2.56 | 54 | -2.84 |
| 25 | $e^{\pi \sqrt{43}}$ | 884736743.9997774660349066619374620785854 | 3.65 | 66 | -2.95 |
| 26 | $e^{\pi \sqrt{719}}$ | 3842614373539548891490294277805829193.0 | 4.89 | 79 | -3.01 |
| 27 | $e^{-\psi_0\left(\frac{2 + \sqrt{3}}{4}\right)}$ | 1.999999695338384704134659354647933169161 | 6.52 | 97 | -3.18 |
| 28 | $163 \left(\pi - e\right)$ | 68.99966449631192450568401364407498298971 | 3.47 | 71 | -3.63 |
| 29 | $\frac{\phi}{2^{\ln 2}}$ | 1.00075909911140985808793904356685019454 | 3.12 | 68 | -3.68 |
| 30 | $\frac{\pi^{9}}{e^{8}}$ | 9.999838797804880181883277456812637375936 | 3.79 | 76 | -3.81 |
| 31 | $e^{\pi \sqrt{74}}$ | 545518122089.9991746788535498566430173362 | 3.08 | 69 | -3.82 |
| 32 | $e^{\pi \sqrt{268}}$ | 21667237292024856735768.00029203884241296 | 3.53 | 74 | -3.87 |
| 33 | $\ln K - \ln\left(\ln K\right)$ | 1.000074426223593005111266030438952140566 | 4.13 | 80 | -3.87 |
| 34 | $e^{\pi \sqrt{522}}$ | 14871070263238043663567627879007.99984873 | 3.82 | 77 | -3.88 |
| 35 | $\frac{1}{\sqrt[3]{3} \ln 2}$ | 1.00030887205011271050752807912612759652 | 3.51 | 74 | -3.89 |
| 36 | $\frac{10 \left(e^{\pi} - \ln 3\right)}{\ln 2}$ | 318.0000000332526559944151081114151281951 | 7.48 | 115 | -4.02 |
| 37 | $e^{\pi \sqrt{148}}$ | 39660184000219160.00096667435857524642577 | 3.01 | 72 | -4.19 |
| 38 | $\frac{3}{\left(\ln 2\right)^{4}}$[^5] | 12.9962905052769664622248845429643076305 | 2.43 | 68 | -4.37 |
| 39 | $\frac{12}{\left(\ln 2\right)^{5}}$[^5] | 74.99873544766160012763455037564470166913 | 2.90 | 75 | -4.60 |
| 40 | $\frac{e^{\pi} - \ln 3}{\ln 2} - \frac{4}{5}$ | 31.00000000332526559944151081114151281951 | 8.48 | 134 | -4.92 |
| 41 | $\ln 2 + \log_{10} 2$ | 0.9941771762239265046309710161826695948437 | 2.23 | 72 | -4.97 |
| 42 | $\frac{5 \phi e}{7 \pi}$ | 1.00000970263606061164186678785699304313 | 5.01 | 100 | -4.99 |
| 43 | $\frac{60}{\left(\ln 2\right)^{6}}$[^5] | 541.0015185164235075692027746182564709468 | 2.82 | 83 | -5.48 |
| 44 | $\sqrt[4]{\frac{91}{10}} - \frac{33}{19}$ | 0.00000003661378056258570376234316589221702231 | 7.44 | 131 | -5.66 |
| 45 | $e^{-\pi} \left(8 \pi - 2\right)$ | 0.9996563886748290424994995423837425460775 | 3.46 | 93 | -5.84 |
| 46 | $3 \sqrt{2} \left(\sqrt{5} - 2\right)$ | 1.001551606266567703186548288039967129741 | 2.81 | 89 | -6.09 |
| 47 | $\frac{613}{37} e - \frac{35}{991}$ | 44.999999999939623550123367441015885459 | 10.22 | 164 | -6.18 |
| 48 | $\frac{360}{\left(\ln 2\right)^{7}}$[^5] | 4683.001247262257437180467152479009585951 | 2.90 | 91 | -6.20 |
| 49 | $e^{6} - \pi^{4} - \pi^{5}$ | 0.00001767345123210920553781124756187587160506 | 4.75 | 110 | -6.25 |
| 50 | $\frac{2520}{\left(\ln 2\right)^{8}}$[^5] | 47292.99873131462390482283548778630880581 | 2.90 | 100 | -7.10 |

[^1]: user-supplied, not on MathWorld
[^2]: core of the stripped amplifiers cos(ln(π+20)) and cos(π cos(π cos(ln(π+20))))): e^π ≈ π+20 gives ln(π+20) ≈ π, each cosine squares the error
[^3]: core of the stripped amplifiers sin 11 and cos 22: 22 ≈ 7π, and cos(7π+ε) = −1 + ε²/2, sin²11 = (1 − cos 22)/2
[^4]: core of the stripped amplifier sin(2017·2^(1/5)): 2017·2^(1/5) ≈ 737.5π, the sine squares the error
[^5]: Hickerson number h_n = n!/(2 (ln 2)^(n+1)), shown in lowest terms
