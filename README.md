# ⚡️ Afdian-Webhook-Notifier (爱发电赞助通知助手)

一个基于 Python Flask 的轻量级 Webhook 接收端。当你在[爱发电](https://afdian.com/)收到新的赞助订单时，它可以自动将订单详情（金额、方案、单号等）实时推送到你的 **Telegram** 和 **邮箱**。

本项目专为 Serverless 架构设计，支持零成本一键部署至 Vercel，无需维护自己的云服务器。

## ✨ 特性

* 🚀 **Serverless 友好**：原生适配 Vercel，免运维，零成本 24/7 运行。
* ✈️ **Telegram 推送**：利用 Telegram Bot API 实时发送排版精美的 Markdown 通知。
* 📧 **邮件通知**：支持通过 QQ 邮箱（或其他 SMTP 服务）发送纯文本备份通知。
* 🔒 **安全可靠**：敏感凭证（Token、授权码）全部通过环境变量传入，代码可完全公开。

## 🚀 一键部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ZinhoYip/Afdian_bot)

部署过程中，Vercel 会提示你填写环境变量（Environment Variables）。请提前准备好以下信息：

### 🔑 环境变量配置项

| 变量名 | 必填 | 说明 |
| --- | --- | --- |
| `TG_BOT_TOKEN` | 是 | Telegram Bot Token (通过 @BotFather 获取) |
| `TG_CHAT_ID` | 是 | 接收通知的 Telegram Chat ID |
| `SENDER_EMAIL` | 是 | 发件箱地址 (例如：`xxx@qq.com`) |
| `SENDER_PASS` | 是 | 邮箱 SMTP 授权码 (注意：非邮箱登录密码！) |
| `RECEIVER_EMAIL` | 是 | 收件箱地址 (可以和发件箱相同) |

## 💻 本地开发与测试

如果你想在本地修改代码并进行测试，请按照以下步骤操作：

1. **克隆项目并安装依赖**
   ```bash
   git clone https://github.com/ZinhoYip/Afdian_bot.git
   cd Afdian_bot
   pip install -r requirements.txt
   ```

2. **配置本地环境变量**
   在项目根目录新建 `.env` 文件（该文件已被 `.gitignore` 忽略，不会上传到云端），填入：
   ```env
   TG_BOT_TOKEN=你的BotToken
   TG_CHAT_ID=你的ChatID
   SENDER_EMAIL=xxx@qq.com
   SENDER_PASS=你的16位授权码
   RECEIVER_EMAIL=xxx@qq.com
   ```

3. **处理本地网络环境（可选）**
   如果你在国内环境测试 Telegram 推送，请在 `api/index.py` 中修改 `PROXIES` 变量，填入你本地的代理地址及端口。部署到 Vercel 时需保持 `PROXIES = None`。

4. **启动服务**
   ```bash
   python api/index.py
   ```
   服务将在 `http://127.0.0.1:5000` 启动。

5. **内网穿透测试**
   推荐使用 Cloudflare Tunnel 进行免配置的公网映射测试：
   ```bash
   cloudflared tunnel --url http://127.0.0.1:5000
   ```
   将终端生成的 `https://xxx.trycloudflare.com` 填入爱发电进行发送测试。

## ⚙️ 爱发电 Webhook 配置

1. 登录爱发电，进入 **开发者中心**。
2. 在 **Webhook URL** 处填入你部署后的 Vercel 域名（如 `https://your-project.vercel.app/`）。
3. 点击"发送测试"，如果 Telegram 和邮箱都能收到消息，且爱发电网页提示成功，说明配置大功告成！

## 📄 License

[MIT](LICENSE)
