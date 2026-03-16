# Voice AI Weekly Report

自动化语音AI行业周报系统：每周一晚8点（北京时间）自动搜集语音AI并购新闻和初创公司动态，整理后推送至指定邮箱。

## 技术栈

| 组件 | 技术 |
|------|------|
| 定时触发 | GitHub Actions (cron) |
| 新闻搜索 | Serper API (Google Search) |
| 内容整理 | DeepSeek API (deepseek-chat) |
| 邮件发送 | Resend |

## 快速开始

### 1. Fork 本仓库

### 2. 配置 GitHub Secrets

在仓库 Settings → Secrets and variables → Actions 中添加：

| Secret | 说明 | 获取方式 |
|--------|------|---------|
| `SERPER_API_KEY` | Serper API 密钥 | 注册 https://serper.dev |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 注册 https://platform.deepseek.com |
| `RESEND_API_KEY` | Resend API 密钥 | 注册 https://resend.com |

### 3. 配置 Resend 发件域名

在 Resend 控制台中验证你的发件域名（如 vocust.com），否则可以使用 Resend 提供的默认发件地址 `onboarding@resend.dev` 进行测试。

如需修改默认发件地址，编辑 `src/email_sender.py` 中的 `EMAIL_FROM` 变量。

### 4. 手动测试

在 GitHub Actions 页面，选择 "Voice AI Weekly Report" workflow，点击 "Run workflow" 手动触发一次。

### 5. 本地运行

```bash
export SERPER_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
export RESEND_API_KEY="your-key"

pip install -r requirements.txt
cd src && python main.py
```

## 自定义

- **收件人**: 修改 `src/email_sender.py` 中的 `EMAIL_TO`
- **搜索关键词**: 修改 `src/search.py` 中的 `SEARCH_QUERIES`
- **报告风格**: 修改 `src/summarize.py` 中的 `SYSTEM_PROMPT`
- **定时时间**: 修改 `.github/workflows/weekly-report.yml` 中的 cron 表达式

## 费用估算

| 服务 | 每次运行消耗 | 免费额度 |
|------|------------|---------|
| Serper | ~5 次搜索 | 2500 次免费额度（注册赠送） |
| DeepSeek API | ~4K input + ~2K output tokens | 按量计费 ~$0.002/次 |
| Resend | 1 封邮件 | 100 封/天 (免费) |
| GitHub Actions | ~2 分钟 | 2000 分钟/月 (免费) |
