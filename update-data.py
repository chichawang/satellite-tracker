#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新衛星軌道資料（data/tle.js）。只用 Python 標準函式庫，不需安裝任何套件。

用法：
    python update-data.py                 從 CelesTrak 下載最新資料（需連網）
    python update-data.py --file a.tle    改用已下載好的 TLE 檔（給不能連網的電腦用）
    python update-data.py --groups        同時更新用途群組清單（data/groups.js）
    python update-data.py --groups-only   只更新用途群組清單

注意：CelesTrak 限制同一份資料兩小時內不要重複下載，太頻繁會被暫時拒絕。
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
OUT = Path(__file__).resolve().parent / "data" / "tle.js"


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def count_satellites(tle):
    """回傳資料中的衛星數；內容不是 TLE 時回傳 0。"""
    line1 = len(re.findall(r"^1 \d{5}", tle, flags=re.M))
    line2 = len(re.findall(r"^2 \d{5}", tle, flags=re.M))
    return min(line1, line2)


def build_js(tle, stamp):
    """把 TLE 文字包成網頁用 <script> 載入的 JS 檔內容。"""
    return 'window.TLE_FETCHED="%s";\nwindow.TLE_DATA=%s;' % (stamp, json.dumps(tle))


# CelesTrak 依用途整理的群組（網頁的「依用途」分類用）。
# Starlink、OneWeb、Kuiper、千帆不下載：數量很大，而且用名稱就能準確判斷。
GROUPS = [
    "stations", "gps-ops", "glo-ops", "galileo", "beidou", "sbas", "nnss", "musson", "gnss",
    "weather", "noaa", "goes", "resource", "sarsat", "dmc", "tdrss", "argos", "planet", "spire",
    "geo", "intelsat", "ses", "eutelsat", "iridium", "iridium-NEXT", "orbcomm", "globalstar",
    "amateur", "x-comm", "other-comm", "satnogs", "gorizont", "raduga", "molniya",
    "science", "geodetic", "engineering", "education", "military", "radar", "cubesat", "other",
]
GROUP_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=%s&FORMAT=tle"
GROUPS_OUT = OUT.parent / "groups.js"


def update_groups():
    """下載各群組的衛星編號，寫成 data/groups.js。個別群組失敗時略過，全部失敗才不更新。"""
    import time
    result, failed = {}, []
    for g in GROUPS:
        try:
            ids = re.findall(r"^1 ([0-9A-Z]\d{4})", download(GROUP_URL % g).replace("\r", ""), flags=re.M)
        except (urllib.error.URLError, OSError) as e:
            ids, err = [], str(e)
        else:
            err = "沒有資料"
        if ids:
            result[g] = ids
            print("  %-14s %5d 顆" % (g, len(ids)))
        else:
            failed.append(g)
            print("  %-14s 失敗（%s）" % (g, err))
        time.sleep(0.5)       # 放慢速度，避免對 CelesTrak 造成負擔
    if not result:
        sys.exit("所有群組都下載失敗，未更新 groups.js。")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tmp = GROUPS_OUT.with_suffix(".js.tmp")
    tmp.write_text('window.GROUPS_FETCHED="%s";\nwindow.GROUPS=%s;' % (stamp, json.dumps(result, separators=(",", ":"))),
                   encoding="utf-8", newline="\n")
    tmp.replace(GROUPS_OUT)
    print("已更新 %d 個群組 → %s" % (len(result), GROUPS_OUT))
    if failed:
        print("未取得的群組：" + ", ".join(failed))


def main():
    ap = argparse.ArgumentParser(description="更新 data/tle.js 的衛星軌道資料")
    ap.add_argument("--file", help="使用本機的 TLE 檔，不連網下載")
    ap.add_argument("--url", default=URL, help="下載來源（預設為 CelesTrak 全部現役衛星）")
    ap.add_argument("--groups", action="store_true", help="同時更新用途群組清單 data/groups.js")
    ap.add_argument("--groups-only", action="store_true", help="只更新用途群組清單，不更新軌道資料")
    args = ap.parse_args()

    if args.groups_only:
        update_groups()
        return

    try:
        if args.file:
            tle = Path(args.file).read_text(encoding="utf-8", errors="replace")
        else:
            print("下載中：" + args.url)
            tle = download(args.url)
    except (urllib.error.URLError, OSError) as e:
        sys.exit("讀取資料失敗，未更新：%s" % e)

    tle = tle.replace("\r", "")
    n = count_satellites(tle)
    if n < 100:
        # CelesTrak 被拒絕時會回一段說明文字而不是 TLE；此時保留原檔不動
        sys.exit("取得的內容不是有效的 TLE 資料（只找到 %d 顆），未更新。\n內容開頭：%s" % (n, tle[:200]))

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".js.tmp")
    tmp.write_text(build_js(tle, stamp), encoding="utf-8", newline="\n")
    tmp.replace(OUT)          # 先寫暫存檔再取代，避免中途失敗留下壞檔
    print("已更新 %d 顆衛星的軌道資料（%s）→ %s" % (n, stamp, OUT))
    if args.groups:
        update_groups()


if __name__ == "__main__":
    main()
