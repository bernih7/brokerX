#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依 JSON 修正清單改寫估價刷題章節頁 ITEMS 的單一欄位（章節頁是唯一資料來源）。
用法：python3 tools/quiz_val/apply_exp_fixes.py fixes.json [--write]
fixes.json：[{"id":"VB2_100_38","field":"explains","i":1,"new":"……"}, {"id":"…","field":"note","new":"…"}, {"id":"…","field":"q","new":"…"}]
  field 預設 explains；explains／opts 需給 i（0 起算）。可另給 "old"（子字串）只替換該字串內的片段。
不加 --write 只做 dry-run（列出每筆前後差異）；任何一筆對不上整批不寫。
改完要跑：node tools/quiz_val/extract_items.js > /tmp/quiz_items.json && python3 tools/quiz_val/sync_cards.py --write && python3 tools/quiz_val/gen_data.py
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
FILES = sorted(R.glob("估價刷題練習_*.html"))
FILES = [f for f in FILES if "113真題" not in f.name]


def js_str_spans(s, start, end=None):
    """回傳從 start 起所有雙引號字串的 (內容起, 內容迄)；end=None 時遇到字串外的 ] 停止"""
    out, i = [], start
    while i < (end if end is not None else len(s)):
        if end is None and s[i] == "]":
            break
        if s[i] == '"':
            j = i + 1
            while s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            out.append((i + 1, j))
            i = j + 1
        else:
            i += 1
    return out


def enc(t):
    return json.dumps(t, ensure_ascii=False)[1:-1]


def dec(t):
    return json.loads('"' + t + '"')


def main():
    fixes = json.load(open(sys.argv[1], encoding="utf-8"))
    write = "--write" in sys.argv
    texts = {f: f.read_text(encoding="utf-8") for f in FILES}
    fail = []
    for fx in fixes:
        iid, field = fx["id"], fx.get("field", "explains")
        hits = [(f, s) for f, s in texts.items() if f'id:"{iid}"' in s]
        if len(hits) != 1:
            fail.append(f"✗ {iid}：找到 {len(hits)} 個檔")
            continue
        f, s = hits[0]
        a = s.index(f'id:"{iid}"')
        e = s.index("\n", a)
        if field in ("explains", "opts"):
            k = s.index(field + ":[", a, e) + len(field) + 2
            spans = js_str_spans(s, k)
            if fx["i"] >= len(spans):
                fail.append(f"✗ {iid} explains[{fx['i']}] 不存在")
                continue
            p, q = spans[fx["i"]]
        else:
            m = re.compile(field + r':"').search(s, a, e)
            if not m:
                fail.append(f"✗ {iid} 找不到欄位 {field}")
                continue
            p = m.end()
            q = js_str_spans(s, p - 1, e)[0][1]
        cur = dec(s[p:q])
        if "old" in fx:
            if cur.count(fx["old"]) != 1:
                fail.append(f"✗ {iid} {field}[{fx.get('i')}]：old 出現 {cur.count(fx['old'])} 次｜現文：{cur[:80]}")
                continue
            new = cur.replace(fx["old"], fx["new"])
        else:
            new = fx["new"]
        print(f"— {iid} {field}{'['+str(fx['i'])+']' if field in ('explains','opts') else ''}\n  舊：{cur}\n  新：{new}")
        texts[f] = s[:p] + enc(new) + s[q:]
    if fail:
        print("\n".join(fail))
        sys.exit("有項目對不上，全部不寫檔。")
    if write:
        for f, s in texts.items():
            if s != f.read_text(encoding="utf-8"):
                f.write_text(s, encoding="utf-8")
                print("寫入", f.name)
    else:
        print(f"dry-run OK：{len(fixes)} 筆")


main()
