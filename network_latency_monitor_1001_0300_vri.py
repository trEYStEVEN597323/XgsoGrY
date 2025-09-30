# 代码生成时间: 2025-10-01 03:00:21
import tornado.ioloop
import tornado.web
import socket
import time

# 网络延迟监控器
class LatencyMonitorHandler(tornado.web.RequestHandler):
    def get(self):
        # 获取目标服务器地址
        target_url = self.get_query_argument('url')
        if not target_url:
            self.write("{"error": "URL parameter is required"}")
            return

        # 尝试连接服务器并计算延迟
        try:
            start_time = time.time()
            socket.create_connection((target_url, 80), timeout=10)
            end_time = time.time()

            # 计算延迟
            latency = (end_time - start_time) * 1000  # 转换为毫秒
            self.write(f"{{"latency": {latency:.2f}, "target_url": "{target_url}"}}")
        except socket.error as e:
            self.write(f"{{"error": "Connection error: {e}"}}")
        except Exception as e:
            self.write(f"{{"error": "Unexpected error: {e}"}}")

# Tornado应用设置
def make_app():
    return tornado.web.Application([
        (r"/latency", LatencyMonitorHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Network latency monitor running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()