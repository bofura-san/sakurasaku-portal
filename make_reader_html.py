#!/usr/bin/env python3
"""Generate a readable HTML page from a plain-text episode file.
Usage: make_reader_html.py <input.txt> <output.html> <ep_label> <ver_label> <lang>
- One paragraph per line. A line containing only '---' becomes a scene-break divider.
- If the first line equals the episode title given in ep_label after '｜', it is skipped as a paragraph.
"""
import html, sys

src, dst, ep_label, ver_label, lang = sys.argv[1:6]
mode = sys.argv[6] if len(sys.argv) > 6 else 'sep'  # 'break': blank line = scene break
raw = open(src, encoding='utf-8').read().replace('\r\n', '\n')
lines = []
for ln in raw.split('\n'):
    ln = ln.strip()
    if ln == '':
        if mode == 'break':
            lines.append('---')
    else:
        lines.append(ln)
# drop leading/trailing dividers, collapse repeats
clean = []
for ln in lines:
    if ln == '---' and (not clean or clean[-1] == '---'):
        continue
    clean.append(ln)
while clean and clean[-1] == '---':
    clean.pop()
# skip a duplicated title line
title = ep_label.split('｜', 1)[1] if '｜' in ep_label else ''
if clean and title and clean[0].strip('「」') == title.strip('「」'):
    clean.pop(0)

paras = []
for ln in clean:
    if ln == '---':
        paras.append('<div class="break">＊　＊　＊</div>')
    else:
        paras.append(f'<p>{html.escape(ln)}</p>')
body = '\n'.join(paras)
ep_head = ep_label.replace('｜', ' ')
page = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(ep_head)}（{html.escape(ver_label)}）｜サクラサク寮歌</title>
<style>
  :root{{--bg:#faf7f2;--ink:#2b2622;--muted:#7a6f66;--accent:#c2567a;--line:#e7ddd2}}
  @media (prefers-color-scheme: dark){{:root{{--bg:#1d1a17;--ink:#ece5dc;--muted:#a89a8c;--accent:#e08bab;--line:#453c34}}}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:"Hiragino Mincho ProN","Hiragino Mincho Pro","YuMincho","Yu Mincho",Georgia,serif;
    line-height:2.0;font-size:17px;padding:28px 18px 72px}}
  .wrap{{max-width:700px;margin:0 auto}}
  nav{{font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans",sans-serif;font-size:.85rem;margin-bottom:26px}}
  nav a{{color:var(--accent);text-decoration:none}}
  h1{{font-size:1.35rem;line-height:1.5;margin:0 0 4px}}
  .ver{{color:var(--muted);font-size:.9rem;margin-bottom:30px;
    font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans",sans-serif}}
  p{{margin:0 0 1.1em;text-align:justify}}
  .break{{text-align:center;color:var(--muted);margin:26px 0;letter-spacing:.6em}}
  footer{{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);
    color:var(--muted);font-size:.82rem;text-align:center;
    font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans",sans-serif}}
  footer a{{color:var(--accent);text-decoration:none}}
</style>
</head>
<body>
<div class="wrap">
<nav><a href="../index.html">← サクラサク寮歌 ポータルに戻る</a></nav>
<h1>{html.escape(ep_head)}</h1>
<div class="ver">{html.escape(ver_label)}</div>
{body}
<footer><a href="../index.html">サクラサク寮歌 ポータル</a></footer>
</div>
</body>
</html>
"""
open(dst, 'w', encoding='utf-8').write(page)
print('wrote', dst, len(page), 'bytes,', len(clean), 'paragraphs')
