# 数据目录

本目录只提交示例数据。完整数据不要提交到 GitHub。

## 推荐结构

```text
data/
  sample_data.json
  sample_school_tags.json
  private/              # 本地私有，git 忽略
    data.json
    school_tags.json
    group_tuition.json
    disc_eval.json
    firstrate_major.json
    firstrate_mixed.json   # 标记哪些校的一流专业为"国家级+省级"混合
```

## 主数据字段

`data.json` 是数组，每条记录代表一个院校专业组。

| 字段 | 含义 |
|---|---|
| `cat` | 科类，例如 `物理`、`历史`、`美术·历史` |
| `fc` | 院校专业组代码，例如 `1101-03` |
| `n` | 院校名称 |
| `f` | 专业组/专业说明 |
| `x` | 再选科目要求 |
| `z` | 特殊类型，例如 `中外合作`、`学分互认`，普通为空字符串 |
| `s` | 2025 投档分或综合分 |
| `rank` | 位次；如为折算值，请在 `rank_source` 标明 |
| `rank_source` | 位次来源，例如 `官方最低位次`、`一分一段折算`、`人工估算` |
| `p` | 省份 |
| `ct` | 城市 |
| `mb` | 是否民办，`1`/`0` |
| `t` | 院校层次 |
| `fee` | 学费，缺失时可由页面显示为估算 |
| `fee_source` | 学费来源，例如 `招生计划专刊`、`学校章程`、`按层次估算` |
| `abroad_note` | 中外合作/学分互认出国说明 |

字段可以继续扩展，但公开页面里要始终展示数据来源。
