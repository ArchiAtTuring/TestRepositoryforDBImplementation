import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DiscoverSuppliers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        suppliers = data.get("suppliers", {})
        results = []
        for s_id, s_data in suppliers.items():
            match = True
            for k, v in filters.items():
                if s_data.get(k) != v:
                    match = False
                    break
            if match:
                res = s_data.copy()
                res["supplier_id"] = s_id
                results.append(res)
        
        return json.dumps({"success": True, "count": len(results), "suppliers": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "discover_suppliers",
            "description": "Searches for supplier records.",
            "type": "getter",
            "inputs": {"filters": {"type": "object"}},
            "outputs": {"success": "boolean", "suppliers": "array"}
        }