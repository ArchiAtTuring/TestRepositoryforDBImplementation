import json
import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManagePurchaseOrders(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, supplier_id: str = None, status: str = None,
               product_id: str = None, quantity: int = 0, purchase_order_id: str = None) -> str:
        
        pos = data.get("purchase_orders", {})
        items = data.get("purchase_order_items", {})
        
        if action == "create":
            ids = [int(k) for k in pos.keys() if k.isdigit()]
            new_id = str(max(ids) + 1) if ids else "1"
            
            new_po = {
                "purchase_order_id": new_id,
                "supplier_id": supplier_id,
                "order_date": datetime.datetime.now().date().isoformat(),
                "status": status or "pending",
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat()
            }
            return json.dumps({"success": True, "purchase_order_id": new_id, "delta": {"purchase_orders": {new_id: new_po}}})

        elif action == "update":
            if not purchase_order_id or purchase_order_id not in pos:
                return json.dumps({"success": False, "error": "Invalid PO ID"})
            
            delta = {"purchase_orders": {purchase_order_id: {
                "status": status, 
                "updated_at": datetime.datetime.now().isoformat()
            }}}
            return json.dumps({"success": True, "purchase_order_id": purchase_order_id, "delta": delta})
            
        elif action == "add_item":
            if not purchase_order_id:
                return json.dumps({"success": False, "error": "Missing PO ID"})
                
            item_ids = [int(k) for k in items.keys() if k.isdigit()]
            new_item_id = str(max(item_ids) + 1) if item_ids else "1"
            
            products = data.get("products", {})
            unit_cost = 0.0
            if product_id and product_id in products:
                unit_cost = round(products[product_id].get("unit_price", 0) * 0.7, 2)
            
            new_item = {
                "po_item_id": new_item_id,
                "purchase_order_id": purchase_order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_cost": unit_cost,
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat()
            }
            return json.dumps({"success": True, "item_id": new_item_id, "delta": {"purchase_order_items": {new_item_id: new_item}}})

        return json.dumps({"success": False, "error": "Invalid action"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "manage_purchase_orders",
            "description": "Manage PO headers and items.",
            "type": "setter",
            "inputs": {
                "action": {"type": "string", "enum": ["create", "update", "add_item"]},
                "supplier_id": {"type": "string"},
                "status": {"type": "string"},
                "product_id": {"type": "string"},
                "quantity": {"type": "integer"},
                "purchase_order_id": {"type": "string"}
            },
            "outputs": {"success": "boolean", "delta": "object"}
        }