import requests
import os
from datetime import datetime, timedelta

def get_beijing_time():
    # GitHub Actions 默认是 UTC，加 8 小时得到北京时间
    beijing_now = datetime.utcnow() + timedelta(hours=8)
    return beijing_now.strftime('%Y-%m-%d %H:%M:%S')

def get_latest_tokens():
    # 使用 Pump.fun 前端 API 获取最新创建的代币
    url = "https://frontend-api.pump.fun/coins?offset=0&limit=10&sort=created_timestamp&order=DESC"
    try:
        response = requests.get(url, timeout=10)
        coins = response.json()
        
        time_str = get_beijing_time()
        msg_lines = [f"📊 **Pump.fun 新币小时汇总**", f"⏰ 时间：{time_str} (北京时间)", "---"]
        
        for coin in coins:
            # 格式化每个代币的信息
            line = f"💎 **{coin['symbol']}**\n📍 地址: `{coin['mint']}`"
            msg_lines.append(line)
            
        return "\n\n".join(msg_lines)
    except Exception as e:
        return f"❌ 获取数据失败: {e}"

def send_feishu(content):
    webhook_url = os.getenv("FEISHU_WEBHOOK")
    if not webhook_url:
        print("未找到 FEISHU_WEBHOOK 变量")
        return
    
    payload = {
        "msg_type": "text",
        "content": {"text": content}
    }
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    summary = get_latest_tokens()
    send_feishu(summary)
    print("已发送至飞书")
