# Almost Integer Rank

对 MathWorld [Almost Integer](https://mathworld.wolfram.com/AlmostInteger.html) 页面收录的近整数做质量排名。

网站：<https://youhuali.github.io/almost_integer_rank/>（GitHub Pages，见下文设置）

## 指标

surplus = n − complexity / 10

- **n** = −log₁₀ |x − nint(x)|，小数点后连续 0 或 9 位数的连续量版本，用绝对误差。
- **complexity** = RIES（Robert Munafo）的符号权重之和，基数 10 + 各符号权重；多位整数按 10 + round(10·log₁₀N) 外推。
- RIES 权重的校准使复杂度 ≤ c 的表达式约有 10^(c/10) 个，因此 surplus > 0 表示该巧合比同等复杂度下随机可期的更罕见。
- 三类放大器被剥离：临界点处的三角函数（误差平方）、Pisot 数的幂（几何级数收缩），以及模函数在 CM 点的代数值（$y \approx e^{\pi\sqrt r}$ 是复乘定理；外层取 ln 等于改用相对精度）。

完整规则、校准依据和 RIES 内置符号说明见网站"计算规则"页。

## 文件

| 文件 | 作用 |
|---|---|
| `rank.py` | 条目定义（RIES 后缀式 + mpmath 求值）、复杂度、放大器检测、生成 `results.md` 与 `site/data.json` |
| `results.md` | 排名表（Markdown，LaTeX 表达式） |
| `site/template.html` | 网页模板，中英双语，含 LaTeX 计算器 |
| `site/build_site.py` | 把 `data.json` 注入模板，生成根目录 `index.html` |
| `index.html` | 构建产物，单文件网站，直接可部署 |
| `enumerate_ries.py` | 枚举 RIES 全空间到指定复杂度，验证盲搜找不到正盈余 |
| `brute_check.py` | 对平凡家族（a·α/b、a/ln a、a·ln b）暴力搜索作基线 |

## 重新生成

```bash
python3 rank.py             # results.md, site/data.json
python3 site/build_site.py  # index.html
```

依赖：Python 3, mpmath, numpy（仅 brute_check.py）。网页运行时从 cdnjs 加载 MathJax 与 decimal.js。

## 部署

**GitHub Pages（推荐）**：仓库 Settings → Pages → Source 选 "Deploy from a branch"，Branch 选 `main`、目录选 `/ (root)`，保存后几分钟内可在上面的地址访问。

**Gist**：新建 public gist，文件名 `index.html`，粘贴根目录 `index.html` 的全部内容；Gist 只显示源码，用 <https://gistpreview.github.io/?GIST_ID/index.html> 渲染为网页。
