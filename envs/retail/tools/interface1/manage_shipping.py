import json
import datetime
import random
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageShipping(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, sales_order_id: str = None, method: str = None, 
               status: str = None, shipping_id: str = None) -> str:
        
        shipping = data.get("shipping", {})
        
        if action == "create":
            ids = [int(k) for k in shipping.keys() if k.isdigit()]
            new_id = str(max(ids) + 1) if ids else "1"
            
            tracking = f"TRK-{random.randint(100000, 999999)}"
            
            new_ship = {
                "shipping_id": new_id,
                "sales_order_id": sales_order_id,
                "method": method,
                "tracking_number": tracking,
                "status": "shipped",
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat()
            }
            return json.dumps({
                "success": True, 
                "tracking_number": tracking, 
                "shipping_id": new_id,
                "delta": {"shipping": {new_id: new_ship}}
            })
            
        elif action == "update":
            if not shipping_id or shipping_id not in shipping:
                return json.dumps({"success": False, "error": "Invalid Shipping ID"})
            
            delta = {"shipping": {shipping_id: {
                "status": status,
                "updated_at": datetime.datetime.now().isoformat()
            }}}
            return json.dumps({"success": True, "delta": delta})
            
        return json.dumps({"success": False, "error": "Invalid action"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "manage_shipping",
            "description": "Generate shipping labels.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string"},
                "sales_order_id": {"type": "string"},
                "method": {"type": "string"},
                "status": {"type": "string"},
                "shipping_id": {"type": "string"}
            },
            "outputs": {"success": "boolean", "tracking_number": "string", "delta": "object"}
        }