import json
import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageProducts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, name: str = "", supplier_id: str = "", 
               unit_price: float = 0.0, description: str = "", product_id: str = None) -> str:
        
        products = data.get("products", {})
        
        if action == "create":
            ids = [int(k) for k in products.keys() if k.isdigit()]
            new_id = str(max(ids) + 1) if ids else "1"
            
            new_record = {
                "product_id": new_id,
                "name": name,
                "supplier_id": supplier_id,
                "unit_price": unit_price,
                "description": description,
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat()
            }
            return json.dumps({"success": True, "product_id": new_id, "delta": {"products": {new_id: new_record}}})
            
        elif action == "update":
            if not product_id or product_id not in products:
                return json.dumps({"success": False, "error": "Invalid product_id"})
            
            updates = {}
            if name: updates["name"] = name
            if unit_price > 0: updates["unit_price"] = unit_price
            if description: updates["description"] = description
            updates["updated_at"] = datetime.datetime.now().isoformat()
            
            return json.dumps({"success": True, "product_id": product_id, "delta": {"products": {product_id: updates}}})
            
        return json.dumps({"success": False, "error": "Invalid action"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "manage_products",
            "description": "Manages product catalog.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string"},
                "name": {"type": "string"},
                "supplier_id": {"type": "string"},
                "unit_price": {"type": "number"},
                "description": {"type": "string"},
                "product_id": {"type": "string"}
            },
            "outputs": {"success": "boolean", "delta": "object"}
        }