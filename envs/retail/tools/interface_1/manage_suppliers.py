import json
import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageSuppliers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, supplier_name: str = "", contact_email: str = "", 
               address: Dict[str, Any] = None, supplier_id: str = None) -> str:
        
        suppliers = data.get("suppliers", {})
        
        safe_address = address if address else {}
        
        if action == "create":
            ids = [int(k) for k in suppliers.keys() if k.isdigit()]
            new_id = str(max(ids) + 1) if ids else "1"
            
            new_record = {
                "supplier_id": new_id,
                "name": supplier_name,
                "contact_email": contact_email,
                "address": safe_address.get("address", ""),
                "city": safe_address.get("city", ""),
                "state": safe_address.get("state", ""),
                "zip_code": safe_address.get("zip_code", ""),
                "country": safe_address.get("country", "USA"),
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat()
            }
            return json.dumps({
                "success": True, 
                "supplier_id": new_id, 
                "delta": {"suppliers": {new_id: new_record}}
            })
            
        elif action == "update":
            if not supplier_id or supplier_id not in suppliers:
                return json.dumps({"success": False, "error": "Invalid supplier_id"})
            
            updates = {}
            if supplier_name: updates["name"] = supplier_name
            if contact_email: updates["contact_email"] = contact_email
            
            if address:
                if "address" in address: updates["address"] = address["address"]
                if "city" in address: updates["city"] = address["city"]
                if "state" in address: updates["state"] = address["state"]
                if "zip_code" in address: updates["zip_code"] = address["zip_code"]
                if "country" in address: updates["country"] = address["country"]
            
            updates["updated_at"] = datetime.datetime.now().isoformat()
            
            return json.dumps({
                "success": True,
                "supplier_id": supplier_id,
                "delta": {"suppliers": {supplier_id: updates}}
            })
            
        return json.dumps({"success": False, "error": "Invalid action"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "manage_suppliers",
            "description": "Creates or updates suppliers.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string", "enum": ["create", "update"]},
                "supplier_name": {"type": "string", "optional": True},
                "contact_email": {"type": "string", "optional": True},
                "address": {
                    "type": "object", 
                    "optional": True,
                    "description": "Dictionary containing address fields: address, city, state, zip_code, country"
                },
                "supplier_id": {"type": "string", "optional": True}
            },
            "outputs": {"success": "boolean", "delta": "object"}
        }