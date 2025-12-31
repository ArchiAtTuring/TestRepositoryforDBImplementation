import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, user_id: str, changes: Dict[str, Any]) -> str:
        """
        Updates user profile. 
        """
        users = data.get("users", {})
        
        if user_id not in users:
            return json.dumps({"success": False, "error": f"User ID {user_id} not found."})
            
        if action != "update":
            return json.dumps({"success": False, "error": "Only 'update' action is supported."})
            
 
        delta = {"users": {user_id: changes}}
        
        return json.dumps({
            "success": True,
            "user_id": user_id,
            "delta": delta
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "manage_users",
            "description": "Updates sensitive user profile information.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string", "description": "Must be 'update'"},
                "user_id": {"type": "string", "description": "ID of the user to update"},
                "changes": {"type": "object", "description": "Dictionary of fields to change"}
            },
            "outputs": {
                "success": "boolean",
                "user_id": "string",
                "delta": "object"
            }
        }