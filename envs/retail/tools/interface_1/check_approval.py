import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CheckApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Validates if the requester is authorized for the action.
        Checks 'approvals' table for explicit approval codes or 'users' table for role-based permission.
        """
        users = data.get("users", {})
        requester = next((u for u in users.values() if u.get("email") == requester_email), None)
        
        if not requester:
            return json.dumps({
                "approved": False, 
                "reason": f"User {requester_email} not found."
            })

        role = requester.get("role", "").lower()
        
        # Define Policy Matrix 
        # Store Manager: All access
        # Fulfillment Specialist: Orders, Shipping, Receiving
        # Customer Support: Cancellations, PII Updates
        
        allowed_actions = {
            "store manager": ["*"], # Wildcard
            "fulfillment specialist": ["create_shipping", "update_order_status", "receive_inventory"],
            "customer support": ["force_cancel", "update_pii"]
        }

        user_permissions = allowed_actions.get(role, [])
        
        if "*" in user_permissions:
            return json.dumps({"approved": True, "reason": "Role authorized (Admin)"})

        if action in user_permissions:
             return json.dumps({"approved": True, "reason": "Role authorized"})

       
        approvals = data.get("approvals", {})
        for appr in approvals.values():
            if (appr.get("requester_email") == requester_email and 
                appr.get("action") == action and 
                appr.get("status") == "approved"):
                return json.dumps({"approved": True, "reason": f"Explicit approval found: {appr.get('approval_code')}"})

        return json.dumps({
            "approved": False, 
            "reason": f"Role '{role}' is not authorized for '{action}' and no explicit approval found."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "check_approval",
            "description": "Validates if the requesting user has the necessary authorization for a specific action based on their role and domain policy rules.",
            "type": "getter",
            "inputs": {
                "action": {
                    "type": "string",
                    "description": "The action being attempted (e.g., 'onboard_supplier', 'force_cancel')"
                },
                "requester_email": {
                    "type": "string",
                    "description": "Email of the user requesting the action"
                }
            },
            "outputs": {
                "approved": "boolean",
                "reason": "string"
            }
        }