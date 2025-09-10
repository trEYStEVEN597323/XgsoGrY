# 代码生成时间: 2025-09-10 15:10:32
import tornado.ioloop
import tornado.web
import re
import html

# 定义一个函数用于转义XSS攻击字符
def escape_xss(text):
    """
    转义文本以防止XSS攻击。
    
    参数:
    text (str): 需要转义的原始文本。
    
    返回:
    str: 转义后的文本。
    """
    return html.escape(text)

# 定义请求处理器
class MainHandler(tornado.web.RequestHandler):
    """
    主请求处理器，用于展示XSS防护的示例。
    """
    def get(self):
        # 显示XSS防护的示例页面
        self.write("<form action='/xss' method='post'>")
        self.write("输入内容: <input type='text' name='content'>")
        self.write("<input type='submit' value='提交'>")
        self.write("</form>")

    def post(self):
        # 获取用户输入的内容
        content = self.get_argument('content')
        # 转义XSS攻击字符
        safe_content = escape_xss(content)
        # 显示转义后的内容
        self.write(f"你输入的内容是: <p>{safe_content}</p>")

# 定义URL路由
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/xss", MainHandler),
    ])

# 主函数，启动Tornado服务器
if __name__ == "__main__":
    print("启动XSS防护服务器...")
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()