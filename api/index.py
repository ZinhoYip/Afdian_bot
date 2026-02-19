import os
import requests
import smtplib
import logging
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from flask import Flask, request, jsonify

# 引入 dotenv
from dotenv import load_dotenv

# 加载 .env 文件中的变量到系统环境变量中
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)

# ================= 配置区 (使用环境变量) =================
# os.environ.get("变量名") 会自动去系统环境里读取对应的值
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

PROXIES = None 

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")             
SENDER_PASS = os.environ.get("SENDER_PASS")        
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")           
# ========================================================

def send_to_telegram(message_text):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    try:
        # 注意：这里去掉了 proxies 参数
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info("✅ 成功转发到 Telegram！")
        else:
            logger.error(f"❌ 转发到 Telegram 失败: {response.text}")
    except Exception as e:
        logger.error(f"❌ 请求 Telegram API 发生错误: {e}")

def send_to_email(title, content):
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr((Header("爱发电监控", 'utf-8').encode(), SENDER_EMAIL))
        msg['To'] = formataddr((Header("我自己", 'utf-8').encode(), RECEIVER_EMAIL))
        msg['Subject'] = Header(title, 'utf-8')

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        logger.info("✅ 邮件通知已发送")
    except Exception as e:
        logger.error(f"❌ 邮件发送失败: {e}")

@app.route('/', methods=['POST'])
def afdian_webhook():
    data = request.json
    if data and data.get('ec') == 200:
        order_info = data.get('data', {}).get('order', {})
        out_trade_no = order_info.get('out_trade_no', '未知')
        plan_title = order_info.get('plan_title', '未知')
        total_amount = order_info.get('total_amount', '0.00')
        title = order_info.get('title', '未知')
        
        tg_msg = (
            f"🎉 收到新的爱发电赞助！\n\n"
            f"💰 金额: `{total_amount} 元`\n"
            f"🏷 方案: {plan_title}\n"
            f"📝 详情: {title}\n"
            f"🔖 单号: `{out_trade_no}`"
        )
        
        email_subject = f"🎉 收到爱发电赞助：{total_amount} 元"
        email_content = (
            f"收到新的爱发电赞助！\n\n"
            f"金额: {total_amount} 元\n"
            f"方案: {plan_title}\n"
            f"详情: {title}\n"
            f"单号: {out_trade_no}\n"
        )
        
        send_to_telegram(tg_msg)
        send_to_email(email_subject, email_content)
        
    return jsonify({"ec": 200, "em": ""})
if __name__ == '__main__':
    # 本地测试时，监听 5000 端口
    app.run(host='0.0.0.0', port=5000)