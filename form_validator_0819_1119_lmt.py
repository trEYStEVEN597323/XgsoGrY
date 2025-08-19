# 代码生成时间: 2025-08-19 11:19:36
import re
from tornado.web import RequestHandler, HTTPError

# 表单数据验证器类
class FormValidator(RequestHandler):
    def validate_email(self, email):
        """验证电子邮件地址是否有效"""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise HTTPError(400, '无效的电子邮件地址')

    def validate_password(self, password):
        """验证密码是否符合安全要求"""
        if len(password) < 8:
            raise HTTPError(400, '密码长度至少为8个字符')
        if not re.search(r'[A-Z]', password):
            raise HTTPError(400, '密码至少包含一个大写字母')
        if not re.search(r'[0-9]', password):
            raise HTTPError(400, '密码至少包含一个数字')

    def validate_username(self, username):
        """验证用户名是否有效"""
        if not re.match(r'^[a-zA-Z0-9_.]+$', username):
            raise HTTPError(400, '无效的用户名')

    def get(self):
        """处理GET请求，显示表单"""
        self.render('form.html')

    def post(self):
        """处理POST请求，验证表单数据"""
        try:
            email = self.get_argument('email')
            password = self.get_argument('password')
            username = self.get_argument('username')

            # 验证表单数据
            self.validate_email(email)
            self.validate_password(password)
            self.validate_username(username)

            # 如果验证通过，处理表单数据
            self.write({'status': 'success', 'message': '表单数据验证成功'})
        except HTTPError as e:
            # 处理验证错误
            self.set_status(e.status_code)
            self.write({'status': 'error', 'message': str(e)})
        except Exception as e:
            # 处理其他错误
            self.set_status(500)
            self.write({'status': 'error', 'message': '服务器错误'})

# 配置路由
def make_app():
    return tornado.web.Application([
        (r"/", FormValidator),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("服务器运行在 http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
