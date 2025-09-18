# 代码生成时间: 2025-09-18 14:06:24
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import pymysql.cursors

# 定义配置参数
define("port", default=8888, help="run on the given port", type=int)

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "db": "your_database",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

class MainHandler(tornado.web.RequestHandler):
    """
    主处理器，防止SQL注入示例。
    """
    def get(self):
        # 获取查询参数
        user_id = self.get_query_argument("user_id", None)

        # 检查user_id是否有效
        if user_id is None:
            self.write("User ID is required")
            self.set_status(400)
            return

        # 安全地查询用户信息
        user_info = self.get_user_info(int(user_id))

        # 返回查询结果
        if user_info:
            self.write(user_info)
        else:
            self.write("User not found")
            self.set_status(404)

    def get_user_info(self, user_id):
        """
        安全地查询用户信息。
        """
        try:
            # 连接数据库
            connection = pymysql.connect(**DB_CONFIG)
            try:
                with connection.cursor() as cursor:
                    # 使用参数化查询防止SQL注入
                    sql = "SELECT * FROM users WHERE id = %s"
                    cursor.execute(sql, (user_id,))
                    result = cursor.fetchone()
                    return result
            finally:
                connection.close()
        except pymysql.Error as e:
            # 记录错误信息
            print(f"Database error: {e}")
            return None

def make_app():
    """
    创建Tornado应用。
    """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    # 解析命令行参数
    tornado.options.parse_command_line()

    # 创建应用
    app = make_app()

    # 启动应用
    app.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()