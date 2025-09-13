# 代码生成时间: 2025-09-14 05:03:55
import tornado.ioloop
import tornado.web
from html import escape

# 定义一个XSS防护函数
# 用于转义输入数据中的HTML特殊字符，防止XSS攻击
def xss_protection(data):
    return escape(str(data), quote=False)

class MainHandler(tornado.web.RequestHandler):
    # GET请求处理函数
    def get(self):
        # 演示XSS攻击防护
        self.write("<html><body><form action="/submit" method="post">"\
                + "Enter your input: <input type="text" name="user_input"><br>"\
                + "<input type="submit" value="Submit">"</form></body></html>")

    # POST请求处理函数
    def post(self):
        # 获取用户输入
        user_input = self.get_body_argument('user_input')
        # 应用XSS防护
        safe_input = xss_protection(user_input)
        # 显示转义后的用户输入
        self.write(f"<p>Your input: {safe_input}</p>")

def make_app():
    # 创建Tornado应用
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/submit", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()