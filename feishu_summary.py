import requests
import os
import json
from datetime import datetime, timedelta

def get_latest_pump_tokens():
    # 你的 Alchemy 链接
    rpc_url = os.getenv("SOLANA_RPC_URL")
    beijing_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Pump.fun 的程序 ID
    PUMP_PROGRAM_ID = "6EF8rrecthR5DkZJ4NsuA5EBcyr9eGi6KuGp6CA29fTJ"
    
    # 构造 Solana RPC 请求：获取 Pump.fun 最新的签名记录
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            PUMP_PROGRAM_ID,
            {"limit": 10} # 取最近10条
        ]
    }
    
    try:
        response = requests.post(rpc_url, json=payload, timeout=15)
        signatures = response.json().get('result', [])
        
        content = f"📊 **Alchemy 实时节点报告**\n⏰ 时间: {beijing_time}\n"
        content += "--------------------------------\n"
        
        if not signatures:
            return content + "暂时没有检测到新交易。"

        # 这里我们拿到了最近的交易签名，为了简单，我们直接展示这些交易的链接
        # 点击链接即可在 Solscan 看到具体的代币
        for sig in signatures:
            content += f"🕒 交易时间: {datetime.fromtimestamp(sig['blockTime'] + 8*3600).strftime('%H:%M:%S')}\n"
            content += f"🔗 详情: `https://solscan.io/tx/{sig['signature']}`\n\n"
            
        return content
    except Exception as e:
        return f"❌ Alchemy 节点请求失败: {str(e)}"

def send_to_feishu(text):
    webhook = os.getenv("FEISHU_WEBHOOK")
    if not webhook: return
    requests.post(webhook, json={"msg_type": "text", "content": {"text": text}})

if __name__ == "__main__":
    report = get_latest_pump_tokens()
    send_to_feishu(report)
