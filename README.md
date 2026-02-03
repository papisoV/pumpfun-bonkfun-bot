# 🚀 Solana Pump.fun 自动化监控助手 (飞书版)

本项目是一个轻量级的 Solana 链上监控工具，专门监听 Pump.fun 的新代币创建动作。

## 🌟 核心功能
* **定时抓取**：基于 GitHub Actions 每小时自动运行一次。
* **智能推送**：只有当监测到**真正的新代币**产生时，才会向飞书群发送通知（过滤重复旧信息）。
* **精准时间**：所有推送信息均已转换为 **北京时间 (UTC+8)**。
* **零成本运行**：无需购买服务器，完全运行在 GitHub Actions 上。

## ⚙️ 配置指南
1. **GitHub Secrets 配置**:
   在仓库 `Settings > Secrets and variables > Actions` 中添加：
   - `SOLANA_RPC_URL`: 你的 Alchemy HTTPS Endpoint。
   - `FEISHU_WEBHOOK`: 飞书机器人 Webhook 地址。

2. **工作流状态**:
   - 自动运行：每小时（0分）触发。
   - 手动运行：在 `Actions` 页面选择 `Hourly Token Report` -> `Run workflow`。

## 📂 文件说明
- `feishu_summary.py`: 核心 Python 脚本，负责调用 Alchemy 接口并处理飞书逻辑。
- `.github/workflows/hourly_report.yml`: GitHub Actions 配置文件。
- `last_time.txt`: (自动生成) 用于记录最后一次发送的时间点，防止重复推送。

## ⚠️ 安全提醒
请务必确认 `.env` 和私密信息已列入 `.gitignore`。
