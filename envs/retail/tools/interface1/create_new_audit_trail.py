import json
import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewAuditTrail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, details: Dict[str, Any], user_email: str) -> str:
        """
        Logs a state-changing event. Returns delta for 'audit_logs'.
        """
        audit_logs = data.get("audit_logs", {})
        
        current_ids = [int(k) for k in audit_logs.keys() if k.isdigit()]
        next_id = str(max(current_ids) + 1) if current_ids else "1"
        
        timestamp = datetime.datetime.now().isoformat()
        
        new_log = {
            "audit_id": next_id,
            "action": action,
            "user_email": user_email,
            "details": details,
            "timestamp": timestamp
        }
        
        delta = {"audit_logs": {next_id: new_log}}
        
        return json.dumps({
            "success": True,
            "audit_id": next_id,
            "delta": delta
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "create_new_audit_trail",
            "description": "Logs a state-changing event for compliance. Must be called after Create/Update/Delete.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string", "description": "Name of the action performed"},
                "details": {"type": "object", "description": "Specific details (e.g., ID created, fields changed)"},
                "user_email": {"type": "string", "description": "Email of the user who performed the action"}
            },
            "outputs": {
                "success": "boolean",
                "audit_id": "string",
                "delta": "object"
            }
        }