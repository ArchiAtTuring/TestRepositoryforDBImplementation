import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DiscoverPurchaseOrders(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        pos = data.get("purchase_orders", {})
        results = []
        for pid, pdata in pos.items():
            match = True
            for k, v in filters.items():
                if pdata.get(k) != v:
                    match = False
                    break
            if match:
                res = pdata.copy()
                res["purchase_order_id"] = pid
                results.append(res)
        return json.dumps({"success": True, "count": len(results), "purchase_orders": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "discover_purchase_orders",
            "description": "Searches POs.",
            "type": "getter",
            "inputs": {"filters": {"type": "object"}},
            "outputs": {"success": "boolean", "purchase_orders": "array"}
        }