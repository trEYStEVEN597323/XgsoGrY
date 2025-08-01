# 代码生成时间: 2025-08-01 20:54:01
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler

# 用户权限管理系统
class UserPermissionManager:
    def __init__(self):
        self.user_permissions = {}

    def add_user(self, username, permissions):
        """添加用户及其权限"""
        if username in self.user_permissions:
            raise ValueError(f"User {username} already exists.")
        self.user_permissions[username] = permissions

    def remove_user(self, username):
        """移除用户"""
        if username not in self.user_permissions:
            raise ValueError(f"User {username} does not exist.")
        del self.user_permissions[username]

    def update_permissions(self, username, permissions):
        """更新用户的权限"""
        if username not in self.user_permissions:
            raise ValueError(f"User {username} does not exist.")
        self.user_permissions[username] = permissions

    def get_permissions(self, username):
        """获取用户的权限"""
        return self.user_permissions.get(username, None)

# Tornado Request Handler
class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write("Error: 404, Resource not found")
        else:
            self.write(f"Error: {status_code}, {kwargs.get('exc', 'An error occurred')}")

class UserManagerHandler(BaseHandler):
    def initialize(self, permission_manager):
        self.permission_manager = permission_manager

    # 添加用户
    def post(self):
        data = self.get_argument('data')
        try:
            username, permissions = data.split(',')
            self.permission_manager.add_user(username, permissions)
            self.write("User added successfully")
        except ValueError as e:
            self.write(str(e))

    # 获取用户权限
    def get(self, username):
        try:
            permissions = self.permission_manager.get_permissions(username)
            if permissions is None:
                self.set_status(404)
                self.write("User not found")
            else:
                self.write(f"{username}'s permissions: {permissions}")
        except Exception as e:
            self.write(str(e))

# 启动Tornado服务
def make_app():
    permission_manager = UserPermissionManager()
    return tornado.web.Application([
        (r"/users/(\w+)/", UserManagerHandler, dict(permission_manager=permission_manager)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()