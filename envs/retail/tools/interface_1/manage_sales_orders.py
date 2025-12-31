import json
import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageSalesOrders(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, sales_order_id: str, status: str, cancel_reason: str = None) -> str:
        sos = data.get("sales_orders", {})
        if sales_order_id not in sos:
            return json.dumps({"success": False, "error": "Order not found"})
            
        updates = {
            "status": status,
            "updated_at": datetime.datetime.now().isoformat()
        }
        if cancel_reason:
            updates["cancel_reason"] = cancel_reason
            
        return json.dumps({
            "success": True, 
            "sales_order_id": sales_order_id, 
            "delta": {"sales_orders": {sales_order_id: updates}}
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "manage_sales_orders",
            "description": "Update Sales Order status.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string"},
                "sales_order_id": {"type": "string"},
                "status": {"type": "string"},
                "cancel_reason": {"type": "string", "optional": True}
            },
            "outputs": {"success": "boolean", "delta": "object"}
        }