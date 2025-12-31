import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverSalesOrders(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        """
        Searches for sales orders based on provided filters.
        """
        orders = data.get("sales_orders", {})
        results = []

        # Iterate through all orders and apply filters
        for so_id, so_data in orders.items():
            match = True
            for key, val in filters.items():
                if so_data.get(key) != val:
                    match = False
                    break
            
            if match:
                # Create a copy to avoid mutating the source data during read
                record = so_data.copy()
                # Ensure the ID is explicitly included in the returned object
                if "sales_order_id" not in record:
                    record["sales_order_id"] = so_id
                results.append(record)

        return json.dumps({
            "success": True,
            "count": len(results),
            "sales_orders": results
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "discover_sales_orders",
            "description": "Searches for sales orders (outbound B2C) to verify status for fulfillment, cancellation, or return processing.",
            "type": "getter",
            "inputs": {
                "filters": {
                    "type": "object",
                    "description": "Key-value pairs for filtering (e.g., {'sales_order_id': 'SO-101'}, {'user_id': 'USR-05'}, {'status': 'placed'})"
                }
            },
            "outputs": {
                "success": "boolean",
                "count": "integer",
                "sales_orders": "array"
            }
        }