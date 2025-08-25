# 代码生成时间: 2025-08-25 09:33:21
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.httpserver
import requests
from concurrent.futures import ThreadPoolExecutor
from time import time

"""
性能测试脚本，使用Tornado框架与requests库进行并发性能测试。
"""

class MainHandler(tornado.web.RequestHandler):
    """
    主请求处理函数，返回一个简单的响应。
    """
    def get(self):
        self.write("Hello, world")

def make_request(url, session):
    """
    使用requests库进行一次HTTP GET请求。
    """
    try:
        response = session.get(url)
        response.raise_for_status()  # 检查响应状态码是否为200
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    else:
        print(f"请求成功: {response.status_code}")
        return response.elapsed.total_seconds()

def performance_test(url, num_requests, num_threads):
    """
    性能测试函数，使用多线程并发发送HTTP请求。
    """
    session = requests.Session()  # 创建Session对象以复用连接
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_request, url, session) for _ in range(num_requests)]
        times = [f.result() for f in futures if f.result() is not None]
    return times

def main():
    """
    主函数，设置Tornado服务器，并启动性能测试。
    """
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("Tornado服务器启动，监听端口8888...")

    # 性能测试参数
    url = "http://localhost:8888/"
    num_requests = 100  # 发送100个请求
    num_threads = 10  # 使用10个线程

    start_time = time()  # 记录开始时间
    times = performance_test(url, num_requests, num_threads)
    end_time = time()  # 记录结束时间

    print(f"性能测试完成，总时间：{end_time - start_time}秒")
    print(f"平均响应时间：{sum(times) / len(times)}秒")

    # 启动Tornado事件循环
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()