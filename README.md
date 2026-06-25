# 江苏高考志愿填报 2026 · Jiangsu Gaokao Volunteer Recommender

这是一个静态 HTML 志愿推荐工具的开源代码骨架。仓库只包含程序代码、数据结构说明和少量示例数据，不包含完整投档线、位次、学费、截图、PDF、Excel 或商业/人工整理数据。

## 公开范围

- `src/build_html.py`：从 JSON 数据生成单文件静态页面。
- `data/sample_data.json`：少量脱敏示例数据，用于演示字段格式。
- `data/sample_school_tags.json`：少量示例院校标签。
- `docs/DATA_POLICY.md`：数据来源、版权和准确性边界说明。
- `docs/DEPLOYMENT.md`：本地构建和服务器部署说明。

## 不公开范围

完整数据请放在 `data/private/`，该目录已被 `.gitignore` 忽略。生成出的 `public/index.html` 可能内嵌完整数据，也默认忽略，不建议提交到 GitHub。

推荐的私有文件名：

```text
data/private/data.json
data/private/school_tags.json
data/private/group_tuition.json
data/private/disc_eval.json
data/private/firstrate_major.json
```

## 快速开始

使用示例数据生成页面：

```bash
python src/build_html.py
```

生成结果：

```text
public/index.html
```

使用完整私有数据生成页面：

```bash
python src/build_html.py --private
```

也可以手动指定数据文件：

```bash
python src/build_html.py --data data/private/data.json --tags data/private/school_tags.json
```

## 数据声明

本项目不是官方填报系统。所有推荐结果仅用于初筛和交流，正式填报应以省教育考试院、招生计划专刊、高校招生章程及官方填报系统为准。

如果你公开部署页面，请务必在页面显著位置保留免责声明和数据来源标记。

## License

代码采用 MIT License。数据、截图、PDF、Excel、人工整理表格不在本开源授权范围内。
