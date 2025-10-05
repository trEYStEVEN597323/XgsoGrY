# 代码生成时间: 2025-10-05 22:19:55
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# 定义测试用例数据结构
class TestCase:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

# 测试用例管理模块
class TestCaseManager:
    def __init__(self):
        self.test_cases = []

    def add_test_case(self, test_case):
        """添加测试用例到列表"""
        self.test_cases.append(test_case)
        return True

    def get_test_case(self, test_case_id):
        """根据ID获取测试用例"""
        for test_case in self.test_cases:
            if test_case.id == test_case_id:
                return test_case
        return None

    def get_all_test_cases(self):
        """获取所有测试用例"""
        return self.test_cases

    def update_test_case(self, test_case_id, name=None, description=None):
        """更新测试用例信息"""
        test_case = self.get_test_case(test_case_id)
        if test_case:
            if name:
                test_case.name = name
            if description:
                test_case.description = description
            return True
        return False

    def delete_test_case(self, test_case_id):
        """删除测试用例"""
        self.test_cases = [test_case for test_case in self.test_cases if test_case.id != test_case_id]
        return True

# Tornado 路由处理函数
def make_app():
    manager = TestCaseManager()
    manager.add_test_case(TestCase(1, "Test Case 1", "Test Case 1 Description"))
    manager.add_test_case(TestCase(2, "Test Case 2", "Test Case 2 Description"))

    return tornado.web.Application([
        (r"/add", AddTestCaseHandler, dict(manager=manager)),
        (r"/get/(\d+)", GetTestCaseHandler, dict(manager=manager)),
        (r"/update/(\d+)/?", UpdateTestCaseHandler, dict(manager=manager)),
        (r"/delete/(\d+)/?", DeleteTestCaseHandler, dict(manager=manager)),
        (r"/all", GetAllTestCasesHandler, dict(manager=manager)),
    ])

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=utf-8")

class AddTestCaseHandler(BaseHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        test_case = TestCase(data["id"], data["name"], data["description"])
        result = self.application.settings["manager"].add_test_case(test_case)
        self.write({"status": "success" if result else "error"})

class GetTestCaseHandler(BaseHandler):
    def get(self, test_case_id):
        test_case = self.application.settings["manager"].get_test_case(test_case_id)
        if test_case:
            self.write(tornado.escape.json_encode(test_case.__dict__))
        else:
            self.set_status(404)
            self.write({"status": "error", "message": "Test case not found"})

class GetAllTestCasesHandler(BaseHandler):
    def get(self):
        test_cases = self.application.settings["manager"].get_all_test_cases()
        self.write(tornado.escape.json_encode([test_case.__dict__ for test_case in test_cases]))

class UpdateTestCaseHandler(BaseHandler):
    def post(self, test_case_id):
        data = tornado.escape.json_decode(self.request.body)
        result = self.application.settings["manager"].update_test_case(test_case_id, data.get("name"), data.get("description"))
        self.write({"status": "success" if result else "error"})

class DeleteTestCaseHandler(BaseHandler):
    def delete(self, test_case_id):
        result = self.application.settings["manager"].delete_test_case(test_case_id)
        self.write({"status": "success" if result else "error"})

if __name__ == "__main__":
    options.define("port", default=8888, help="run on the given port", type=int)
    define("debug", default=True, type=bool)
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.options.port)
    print("Server is running on port: %s" % options.options.port)
    tornado.ioloop.IOLoop.current().start()