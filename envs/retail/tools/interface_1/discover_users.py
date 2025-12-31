import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class DiscoverUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        """
        Searches for users based on exact match filters.
        """
        users = data.get("users", {})
        results = []
        
        for u_id, u_data in users.items():
            match = True
            for key, val in filters.items():
                if u_data.get(key) != val:
                    match = False
                    break
            if match:
                record = u_data.copy()
                if "user_id" not in record:
                    record["user_id"] = u_id
                results.append(record)
                
        return json.dumps({
            "success": True,
            "count": len(results),
            "users": results
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "discover_users",
            "description": "Searches for user records based on specific filters (email, role, name).",
            "type": "getter",
            "inputs": {
                "filters": {
                    "type": "object",
                    "description": "Key-value pairs for filtering (e.g., {'email': 'bob@example.com'})"
                }
            },
            "outputs": {
                "success": "boolean",
                "count": "integer",
                "users": "array"
            }
        }