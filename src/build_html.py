# -*- coding: utf-8 -*-
"""Build a static gaokao recommendation page from JSON data.

The repository ships only sample data. Put full/private data in data/private/
or pass paths explicitly with --data/--tags.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PRIVATE_DIR = DATA_DIR / "private"
PUBLIC_DIR = ROOT / "public"


def read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pick_path(explicit: str | None, private_name: str, sample_name: str, use_private: bool) -> Path:
    if explicit:
        return Path(explicit)
    private_path = PRIVATE_DIR / private_name
    if use_private and private_path.exists():
        return private_path
    return DATA_DIR / sample_name


def js(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def build_html(data, tags) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>高考志愿推荐系统开源版</title>
  <style>
    :root {{
      --bg:#f6f7fb; --card:#fff; --line:#dfe5ee; --ink:#1f2937; --mut:#6b7280;
      --blue:#2454a6; --chong:#d86b2a; --wen:#b88a00; --bao:#16834a; --danger:#b91c1c;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:14px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Microsoft YaHei",sans-serif; background:var(--bg); color:var(--ink); }}
    .wrap {{ max-width:1500px; margin:0 auto; padding:18px; }}
    h1 {{ margin:0 0 4px; font-size:22px; }}
    .sub {{ color:var(--mut); margin-bottom:14px; }}
    .warn {{ border:2px solid #ef4444; background:#fff1f2; color:#991b1b; border-radius:8px; padding:10px 12px; margin-bottom:14px; font-weight:700; }}
    .warn small {{ display:block; font-weight:400; margin-top:3px; }}
    .panel {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px; margin-bottom:14px; }}
    .row {{ display:flex; flex-wrap:wrap; gap:12px 18px; align-items:end; }}
    label {{ display:block; font-size:12px; color:var(--mut); margin-bottom:4px; }}
    input, select {{ height:34px; border:1px solid var(--line); border-radius:6px; padding:0 9px; background:#fff; }}
    input[type=number] {{ width:120px; }}
    .checks {{ display:flex; flex-wrap:wrap; gap:6px; }}
    .checks label {{ display:inline-flex; gap:4px; align-items:center; height:30px; padding:0 9px; border:1px solid var(--line); border-radius:999px; background:#eef2f7; color:#374151; cursor:pointer; }}
    button {{ height:34px; border:1px solid var(--line); border-radius:6px; background:#fff; padding:0 12px; cursor:pointer; }}
    button.primary {{ background:var(--blue); color:#fff; border-color:var(--blue); font-weight:700; }}
    .summary {{ margin:8px 2px 12px; color:#374151; }}
    .tablewrap {{ overflow:auto; max-height:64vh; border:1px solid var(--line); border-radius:8px; background:#fff; }}
    table {{ width:100%; min-width:1280px; border-collapse:collapse; }}
    th, td {{ border:1px solid var(--line); padding:7px 8px; text-align:center; vertical-align:top; }}
    th {{ position:sticky; top:0; background:var(--blue); color:#fff; }}
    td.left {{ text-align:left; }}
    tr.chong {{ background:#fff3e8; }} tr.wen {{ background:#fff9df; }} tr.bao {{ background:#ecf8f0; }}
    .badge {{ display:inline-block; padding:1px 8px; border-radius:999px; color:#fff; font-size:12px; font-weight:700; }}
    .b-chong {{ background:var(--chong); }} .b-wen {{ background:var(--wen); }} .b-bao {{ background:var(--bao); }}
    .source {{ display:block; margin-top:2px; color:#8a6d3b; font-size:11px; white-space:nowrap; }}
    .source.warn {{ color:#dc2626; font-weight:bold; }}
    .tag {{ display:inline-block; margin:1px 3px 1px 0; padding:1px 6px; border-radius:999px; background:#eef2ff; color:#1d4ed8; font-size:12px; }}
    .risk {{ background:#fff1e6; color:#9a3412; }}
    .fit {{ background:#eaf7ef; color:#166534; }}
    .diff-ok {{ color:var(--bao); font-weight:700; }} .diff-bad {{ color:var(--danger); font-weight:700; }}
    .foot {{ margin-top:12px; color:var(--mut); font-size:12px; }}
  </style>
</head>
<body>
<div class="wrap">
  <h1>高考志愿推荐系统开源版</h1>
  <div class="sub">代码演示版：仓库仅包含样例数据。正式数据请放在本地私有目录，页面必须保留来源标记。</div>
  <div class="warn">仅供参考，不作为最终填报依据。
    <small>正式填报请以省教育考试院、高校招生章程、招生计划专刊和官方填报系统为准。位次、学费、标签必须核验来源。</small>
  </div>
  <div class="panel">
    <div class="row">
      <div><label>科类</label><select id="cat"></select></div>
      <div><label>我的分数</label><input id="score" type="number" value="530"></div>
      <div><label>我的位次</label><input id="rank" type="number" placeholder="可选"></div>
      <div><label>省份</label><select id="prov"></select></div>
      <div><label>城市</label><select id="city"></select></div>
      <div><label>学费上限</label><input id="feeMax" type="number" placeholder="不限"></div>
      <div><button class="primary" onclick="run()">生成推荐</button></div>
      <div><button onclick="exportCsv()">导出 CSV</button></div>
    </div>
    <div style="margin-top:12px">
      <label>院校层次</label>
      <div class="checks" id="tiers"></div>
    </div>
    <div style="margin-top:12px">
      <label>选科要求</label>
      <div class="checks" id="subjects"></div>
    </div>
    <div style="margin-top:12px" class="checks">
      <label><input type="checkbox" id="excludeZw"> 排除中外合作/学分互认</label>
      <label><input type="checkbox" id="showFar"> 显示极冲</label>
    </div>
  </div>
  <div id="out"></div>
  <div class="foot">数据来源字段由 JSON 提供：投档分、位次、学费、院校标签均应标明官方/折算/估算/人工初标等来源。</div>
</div>
<script>
const DATA = {js(data)};
const TAGS = {js(tags)};
const ORDER = {{'冲':0,'极冲':1,'稳':2,'保':3}};
let current = [];

function uniq(arr) {{ return [...new Set(arr.filter(Boolean))]; }}
function checkedValues(boxId) {{
  return [...document.querySelectorAll(`#${{boxId}} input:checked`)].map(x => x.value);
}}
function initSelect(id, values, allText='全部') {{
  const el = document.getElementById(id);
  el.innerHTML = `<option value="">${{allText}}</option>` + values.map(v => `<option>${{v}}</option>`).join('');
}}
function initChecks(id, values) {{
  const el = document.getElementById(id);
  el.innerHTML = values.map(v => `<label><input type="checkbox" value="${{v}}" checked> ${{v}}</label>`).join('');
}}
function tierOf(score, item) {{
  const diff = Number(score) - Number(item.s);
  if (diff >= 8) return '保';
  if (diff >= 0) return '稳';
  if (diff >= -12) return '冲';
  return '极冲';
}}
function fee(item) {{
  if (item.fee) return Number(item.fee);
  if (item.z === '中外合作') return 26000;
  if (item.t && item.t.includes('民办')) return 17000;
  if (item.cat && item.cat.includes('美术')) return 10000;
  return 5500;
}}
function esc(v) {{
  return String(v ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
}}
function tagHtml(item) {{
  const t = TAGS[item.n];
  if (!t) return '<span class="source">无人工标签</span>';
  const strengths = (t.strengths || []).map(x => `<span class="tag">${{esc(x)}}</span>`).join('');
  const risks = (t.risks || []).map(x => `<span class="tag risk">${{esc(x)}}</span>`).join('');
  const fit = (t.fit || []).map(x => `<span class="tag fit">${{esc(x)}}</span>`).join('');
  return `${{strengths}}${{fit}}${{risks}}<span class="source">人工初标/示例标签</span>`;
}}
function refreshFilters() {{
  const cat = document.getElementById('cat').value;
  const rows = DATA.filter(x => !cat || x.cat === cat);
  initSelect('prov', uniq(rows.map(x => x.p)));
  initSelect('city', uniq(rows.map(x => x.ct)));
}}
function run() {{
  const score = Number(document.getElementById('score').value || 0);
  const userRank = Number(document.getElementById('rank').value || 0);
  const cat = document.getElementById('cat').value;
  const prov = document.getElementById('prov').value;
  const city = document.getElementById('city').value;
  const feeMax = Number(document.getElementById('feeMax').value || 0);
  const tiers = checkedValues('tiers');
  const subjects = checkedValues('subjects');
  const excludeZw = document.getElementById('excludeZw').checked;
  const showFar = document.getElementById('showFar').checked;

  current = DATA.filter(item => {{
    if (cat && item.cat !== cat) return false;
    if (prov && item.p !== prov) return false;
    if (city && item.ct !== city) return false;
    if (tiers.length && !tiers.includes(item.t)) return false;
    if (subjects.length && !subjects.includes(item.x || '不限')) return false;
    if (excludeZw && (item.z === '中外合作' || item.z === '学分互认')) return false;
    if (feeMax && fee(item) > feeMax) return false;
    item._tier = tierOf(score, item);
    if (!showFar && item._tier === '极冲') return false;
    item._fee = fee(item);
    item._rankDiff = userRank && item.rank ? Number(item.rank) - userRank : null;
    return true;
  }}).sort((a,b) => ORDER[a._tier] - ORDER[b._tier] || b.s - a.s);

  const rows = current.map(item => {{
    const diff = Number(score) - Number(item.s);
    const rankDiff = item._rankDiff == null ? '-' : `<span class="${{item._rankDiff >= 0 ? 'diff-ok' : 'diff-bad'}}">${{item._rankDiff >= 0 ? '+' : ''}}${{item._rankDiff.toLocaleString()}}</span>`;
    return `<tr class="${{item._tier === '冲' || item._tier === '极冲' ? 'chong' : item._tier === '稳' ? 'wen' : 'bao'}}">
      <td><span class="badge b-${{item._tier === '保' ? 'bao' : item._tier === '稳' ? 'wen' : 'chong'}}">${{item._tier}}</span></td>
      <td class="left"><b>${{esc(item.n)}}</b><span class="source">${{esc(item.p)}} / ${{esc(item.ct)}} / ${{esc(item.t)}}</span></td>
      <td>${{esc(item.fc)}}</td>
      <td class="left">${{esc(item.f)}}</td>
      <td>${{esc(item.x || '不限')}}</td>
      <td>${{item.s}}<span class="source">投档分：${{esc(item.score_source || '样例/待标明')}}</span></td>
      <td>${{diff >= 0 ? '+' : ''}}${{diff}}</td>
      <td>${{item.rank ? Number(item.rank).toLocaleString() : '-'}}<span class="source">${{esc(item.rank_source || '未标明')}}</span></td>
      <td>${{rankDiff}}</td>
      <td>${{item._fee.toLocaleString()}}<span class="source${{/不可比|存疑/.test(item.fee_source||'')?' warn':''}}">${{esc(item.fee_source || '按层次估算')}}</span></td>
      <td>${{esc(item.z || '-')}}<span class="source">${{esc(item.abroad_note || '')}}</span></td>
      <td class="left">${{tagHtml(item)}}</td>
    </tr>`;
  }}).join('');

  document.getElementById('out').innerHTML = `<div class="summary">共筛出 <b>${{current.length}}</b> 条，排序为：冲 → 极冲 → 稳 → 保。</div>
    <div class="tablewrap"><table><thead><tr>
      <th>梯度</th><th>院校</th><th>专业组</th><th>专业说明</th><th>选科</th><th>投档分</th><th>分差</th><th>位次</th><th>与你位次差</th><th>学费</th><th>特殊说明</th><th>院校提示</th>
    </tr></thead><tbody>${{rows || '<tr><td colspan="12">没有匹配结果</td></tr>'}}</tbody></table></div>`;
}}
function exportCsv() {{
  const header = ['梯度','院校','专业组','专业说明','选科','投档分','位次','位次来源','学费','学费来源','特殊类型','出国说明'];
  const lines = [header].concat(current.map(x => [x._tier,x.n,x.fc,x.f,x.x,x.s,x.rank || '',x.rank_source || '',x._fee,x.fee_source || '按层次估算',x.z || '',x.abroad_note || '']));
  const csv = lines.map(row => row.map(v => `"${{String(v ?? '').replace(/"/g,'""')}}"`).join(',')).join('\\n');
  const blob = new Blob(['\\ufeff' + csv], {{type:'text/csv;charset=utf-8'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'gaokao_recommendations.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}}

initSelect('cat', uniq(DATA.map(x => x.cat)), '请选择');
initChecks('tiers', uniq(DATA.map(x => x.t)));
initChecks('subjects', uniq(DATA.map(x => x.x || '不限')));
document.getElementById('cat').addEventListener('change', refreshFilters);
refreshFilters();
run();
</script>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private", action="store_true", help="use data/private/*.json when present")
    parser.add_argument("--data", help="path to data.json")
    parser.add_argument("--tags", help="path to school_tags.json")
    parser.add_argument("--out", default=str(PUBLIC_DIR / "index.html"), help="output html path")
    args = parser.parse_args()

    data_path = pick_path(args.data, "data.json", "sample_data.json", args.private)
    tags_path = pick_path(args.tags, "school_tags.json", "sample_school_tags.json", args.private)
    data = read_json(data_path, [])
    tags = read_json(tags_path, {})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_html(data, tags), encoding="utf-8")
    print(f"built {out} with {len(data)} records")
    print(f"data: {data_path}")
    print(f"tags: {tags_path}")
    print("warning: generated html may embed private data; do not commit it unless intentionally public")


if __name__ == "__main__":
    main()
