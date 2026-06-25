# 构建与部署

## 本地构建

```bash
python src/build_html.py
```

默认使用 `data/sample_data.json`，生成 `public/index.html`。

## 使用私有完整数据

把完整数据放入：

```text
data/private/data.json
data/private/school_tags.json
```

然后执行：

```bash
python src/build_html.py --private
```

注意：生成的 `public/index.html` 会内嵌数据，默认已被 `.gitignore` 忽略，不要提交到 GitHub。

## 部署到服务器

把生成后的 HTML 上传到服务器的 Nginx 目录即可。例如：

```bash
scp public/index.html root@你的服务器IP:/usr/share/nginx/html/index.html
```

公开访问前建议：

- 保留页面顶部免责声明。
- 不收集考生姓名、身份证、手机号等个人信息。
- SSH 使用强密码或密钥，服务器安全组只开放必要端口。
- 设置云厂商流量/费用告警。
