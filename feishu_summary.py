import requests
import os
import json
from datetime import datetime, timedelta

def get_latest_pump_tokens():
    rpc_url = os.getenv("SOLANA_RPC_URL")
    PUMP_PROGRAM_ID = "6EF8rrecthR5DkZJ4NsuA5EBcyr9eGi6KuGp6CA29fTJ"
    
    # 1. 获取链上最新记录
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "getSignaturesForAddress",
        "params": [PUMP_PROGRAM_ID, {"limit": 10}]
    }
    
    try:
        response = requests.post(rpc_url, json=payload, timeout=15)
        signatures = response.json().get('result', [])
        if not signatures: return None

        # 2. 读取上一次发送的最后一条签名的时间戳
        last_recorded_time = 0
        if os.path.exists("last_time.txt"):
            with open("last_time.txt", "r") as f:
                last_recorded_time = int(f.read().strip())

        # 3. 筛选出比上次更新的消息（真正的新消息）
        new_txs = [tx for tx in signatures if tx['blockTime'] > last_recorded_time]
        
        if not new_txs:
            print("没有更新的消息，跳过发送。")
            return None

        # 4. 记录最新的一条时间戳供下次使用
        with open("last_time.txt", "w") as f:
            f.write(str(new_txs[0]['blockTime']))

        # 5. 格式化北京时间消息内容
        beijing_now = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
        msg = f"🔔 **Pump.fun 实时上新 (北京时间: {beijing_now})**\n"
        msg += "--------------------------------\n"
        
        for tx in new_txs:
            tx_time = datetime.fromtimestamp(tx['blockTime'] + 8*3600).strftime('%H:%M:%S')
            msg += f"🕒 {tx_time} | [查看代币详情](https://solscan.io/tx/{tx['signature']})\n"
        
        return msg
    except Exception as e:
        print(f"执行出错: {e}")
        return None

def send_to_feishu(content):
    if not content: return
    webhook = os.getenv("FEISHU_WEBHOOK")
    requests.post(webhook, json={"msg_type": "text", "content": {"text": content}})

if __name__ == "__main__":
    report = get_latest_pump_tokens()
    send_to_feishu(report)
