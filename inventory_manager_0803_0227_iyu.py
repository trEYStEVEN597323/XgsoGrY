# 代码生成时间: 2025-08-03 02:27:07
import tornado.ioloop
import tornado.web
import json

# 模拟数据库
class Database:
    def __init__(self):
        self.data = {}

    def add_item(self, item_id, quantity):
        if item_id in self.data:
            self.data[item_id] += quantity
        else:
            self.data[item_id] = quantity

    def remove_item(self, item_id, quantity):
        if item_id in self.data:
            self.data[item_id] -= quantity
            if self.data[item_id] < 0:
                raise ValueError("Insufficient inventory")
        else:
            raise ValueError("Item not found")

    def get_inventory(self):
        return self.data

# 库存管理请求处理器
class InventoryHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def post(self):
        # 解析请求体
        try:
            data = json.loads(self.request.body)
            item_id = data['item_id']
            quantity = data['quantity']
            if data['action'] == 'add':
                self.database.add_item(item_id, quantity)
                self.write({'status': 'success', 'message': 'Item added to inventory'})
            elif data['action'] == 'remove':
                self.database.remove_item(item_id, quantity)
                self.write({'status': 'success', 'message': 'Item removed from inventory'})
            else:
                self.set_status(400)
                self.write({'status': 'error', 'message': 'Invalid action'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'status': 'error', 'message': 'Invalid JSON format'})
        except ValueError as e:
            self.set_status(400)
            self.write({'status': 'error', 'message': str(e)})

    def get(self):
        inventory = self.database.get_inventory()
        self.write({'status': 'success', 'inventory': inventory})

# 创建数据库实例
database = Database()

# 设置URL路由
def make_app():
    return tornado.web.Application([
        (r"/inventory", InventoryHandler, dict(database=database)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('Starting Tornado server on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()