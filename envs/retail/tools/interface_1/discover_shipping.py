import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverShipping(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        """
        Searches for shipping records based on specific filters.
        """
        shipments = data.get("shipping", {})
        results = []

        for ship_id, ship_data in shipments.items():
            match = True
            for key, val in filters.items():
                if ship_data.get(key) != val:
                    match = False
                    break
            
            if match:
                record = ship_data.copy()
                if "shipping_id" not in record:
                    record["shipping_id"] = ship_id
                results.append(record)

        return json.dumps({
            "success": True,
            "count": len(results),
            "shipments": results
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "discover_shipping",
            "description": "Finds shipping records associated with a Sales Order. Used to retrieve tracking numbers or verify shipment details for returns.",
            "type": "getter",
            "inputs": {
                "filters": {
                    "type": "object",
                    "description": "Key-value pairs for filtering (e.g., {'sales_order_id': 'SO-101'}, {'tracking_number': 'TRK-999'})"
                }
            },
            "outputs": {
                "success": "boolean",
                "count": "integer",
                "shipments": "array"
            }
        }