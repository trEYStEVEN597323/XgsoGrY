# 代码生成时间: 2025-08-06 23:42:58
import tornado.ioloop
# NOTE: 重要实现细节
import tornado.web
from tornado.options import define, options

# Define the port for the Tornado application
define("port", default=8888, help="run on the given port", type=int)

# Data structure to hold inventory items
# 扩展功能模块
class InventoryItem:
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity

# Inventory management system
class InventoryManagement:
    def __init__(self):
        # Initialize an empty inventory
        self.inventory = {}

    def add_item(self, item_id, name, quantity):
        """Adds a new item to the inventory."""
        if item_id in self.inventory:
            raise ValueError(f"Item {item_id} already exists in the inventory.")
        self.inventory[item_id] = InventoryItem(item_id, name, quantity)
        return { "item_id": item_id, "name": name, "quantity": quantity }

    def update_item(self, item_id, quantity):
        """Updates the quantity of an existing item in the inventory."""
        if item_id not in self.inventory:
            raise ValueError(f"Item {item_id} does not exist in the inventory.")
        self.inventory[item_id].quantity = quantity
        return { "item_id": item_id, "name": self.inventory[item_id].name, "quantity": quantity }

    def delete_item(self, item_id):
        "