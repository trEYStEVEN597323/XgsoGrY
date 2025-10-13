# 代码生成时间: 2025-10-14 03:13:24
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# 定义日志等级
define("port", default=8888, help="run on the given port", type=int)

# 职业规划类别
class CareerCategory:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

# 职业规划建议
class CareerAdvice:
    def __init__(self, id, category_id, advice):
        self.id = id
        self.category_id = category_id
        self.advice = advice

    def to_dict(self):
        return {"id": self.id, "category_id": self.category_id, "advice": self.advice}

# 职业规划数据存储
class CareerPlanningDataStore:
    def __init__(self):
        self.categories = {}
        self.advices = {}

    def add_category(self, category):
        self.categories[category.id] = category

    def add_advice(self, advice):
        self.advices[advice.id] = advice

    def get_category(self, category_id):
        return self.categories.get(category_id)

    def get_advice(self, advice_id):
        return self.advices.get(advice_id)

# API请求处理器
class CategoryHandler(tornado.web.RequestHandler):
    def get(self):
        category_id = self.get_argument("id")
        try:
            category = data_store.get_category(category_id)
            if category:
                self.write(category.to_dict())
            else:
                self.set_status(404)
                self.write({"error": "Category not found"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

class AdviceHandler(tornado.web.RequestHandler):
    def get(self):
        advice_id = self.get_argument("id")
        try:
            advice = data_store.get_advice(advice_id)
            if advice:
                self.write(advice.to_dict())
            else:
                self.set_status(404)
                self.write({"error": "Advice not found"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

# 初始化数据存储
data_store = CareerPlanningDataStore()
data_store.add_category(CareerCategory(1, "Software Engineering"))
data_store.add_advice(CareerAdvice(1, 1, "Learn Python and Tornado"))

# 路由设置
def make_app():
    return tornado.web.Application([
        (r"/category/", CategoryHandler),
        (r"/advice/", AdviceHandler),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print("Career Planning System started on port %d" % options.port)
    tornado.ioloop.IOLoop.current().start()