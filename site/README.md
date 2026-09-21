# Almost Integer Rank — 网站

单文件静态站点：构建产物是仓库根目录的 `index.html`，内联了排名数据，公式用 MathJax（cdnjs）渲染，计算器用 decimal.js（cdnjs）做 90 位精度计算。

## 重新生成

```bash
python3 rank.py            # 生成 results.md 与 site/data.json
python3 site/build_site.py # 把 data.json 注入 template.html，得到根目录 index.html
```

## 用 GitHub Gist 展示

1. 新建一个 gist，文件名 `index.html`，粘贴根目录 `index.html` 的全部内容，设为 public。
2. 访问 `https://gistpreview.github.io/?<gist id>/index.html`，把 `<gist id>` 换成 gist 地址末尾那串十六进制。

Gist 本身只显示源码，gistpreview 会把它当网页渲染；外部脚本（MathJax、decimal.js、Google Fonts）都能正常加载。

## 语言

页面为中英双语，右上角可切换，偏好存于 localStorage，首次访问按浏览器语言选择。静态文案用成对的 `.l-zh` / `.l-en` 元素，由根元素的 `data-lang` 控制显示；JS 生成的文字走 `I18N` 字典。

## 页面

- `#/` 排行榜：不超过 100 条，数值列高亮小数点后连续的 0/9。
- `#rules` 计算规则：n、complexity、surplus 的定义，RIES 权重表，校准依据，放大器剥离，收录范围。
- `#calc` 计算器：输入 LaTeX 表达式，显示 n、复杂度（及采用的 RIES 后缀式）、surplus 和在榜中的位置。
