"""Build index.html at the repo root (standalone: GitHub Pages / Gist ready) from site/template.html + site/data.json.
Also writes an artifact variant (no document skeleton) when given an output path."""
import json, re, sys, datetime
tpl = open('site/template.html', encoding='utf-8').read()
data = open('site/data.json', encoding='utf-8').read()
data = data.replace('</', '<\\/')                      # keep the JSON safe inside <script>
html = tpl.replace('__DATA__', data).replace('<span id="build"></span>',
        '<span id="build"> 生成于 %s。</span>' % datetime.date.today().isoformat())
open('index.html', 'w', encoding='utf-8').write(html)
print('index.html', len(html), 'bytes')
if len(sys.argv) > 1:
    head = re.search(r'<!--BEGIN-ARTIFACT-->(.*?)<!--END-HEAD-->', html, re.S).group(1)
    body = re.search(r'<!--BEGIN-BODY-->(.*?)<!--END-BODY-->', html, re.S).group(1)
    open(sys.argv[1], 'w', encoding='utf-8').write(head + body)
    print(sys.argv[1], 'written')
