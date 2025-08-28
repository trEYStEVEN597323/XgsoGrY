# 代码生成时间: 2025-08-29 05:24:11
import tornado.ioloop
import tornado.web
import json

# 定义一个数学计算工具集类
class MathCalculator:
    def add(self, a, b):
        """加法运算"""
        return a + b

    def subtract(self, a, b):
        """减法运算"""
        return a - b

    def multiply(self, a, b):
        """乘法运算"""
        return a * b

    def divide(self, a, b):
        """除法运算"""
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b

# 定义一个Tornado请求处理类
class MathRequestHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            # 解析客户端请求数据
            request_data = json.loads(self.request.body)
            # 根据请求类型调用对应的计算方法
            if request_data['operation'] == 'add':
                result = MathCalculator().add(request_data['a'], request_data['b'])
            elif request_data['operation'] == 'subtract':
                result = MathCalculator().subtract(request_data['a'], request_data['b'])
            elif request_data['operation'] == 'multiply':
                result = MathCalculator().multiply(request_data['a'], request_data['b'])
            elif request_data['operation'] == 'divide':
                result = MathCalculator().divide(request_data['a'], request_data['b'])
            else:
                raise ValueError("不支持的运算类型")
            # 返回计算结果
            self.write(json.dumps({'result': result}))
        except Exception as e:
            self.write(json.dumps({'error': str(e)}))

# 设置Tornado路由
def make_app():
    return tornado.web.Application([
        (r"/math", MathRequestHandler),
    ])

# 启动Tornado服务
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Math calculator server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()