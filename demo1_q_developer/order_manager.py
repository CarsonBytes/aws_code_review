import requests

# 故意留的硬編碼 API Key（漏洞）
API_KEY = "sk-abc123def456"

# 模擬訂單資料庫
mock_db = {
    "12345": {"status": "未出貨", "delivery_date": "2026-05-10"}
}

def update_delivery_date(order_id: str, new_date: str) -> dict:
    order = mock_db.get(order_id)
    if not order:
        return {"error": "Order not found"}
    # 故意缺少「訂單已出貨時不可修改」的檢查（邏輯漏洞）
    order["delivery_date"] = new_date
    mock_db[order_id] = order
    return {"status": "updated", "new_date": new_date}

def call_payment_gateway(order_id, amount):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    requests.post("https://api.payment.com/charge", json={"order_id": order_id, "amount": amount}, headers=headers)